from typing import List, Optional

from PySide6.QtWidgets import QGraphicsScene, QMenu
from PySide6.QtCore import QPointF, Signal
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QGraphicsSceneMouseEvent

from ._port import Port
from ._connection import Connection
from ._node import Node

from ...types.enums import PortType



class NodeScene(QGraphicsScene):
    """Node editor scene"""
    connection_created = Signal(object)
    node_moved = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.grid_size: int = 20
        self._menu: QMenu = QMenu()
        self._temp_connection: Optional[Connection] = None  # Temporary connection line
        self._nodes: List[Node] = []
        self._dragging_connection: bool = False  # Flag for adding connection drag
        self._snap_distance: float = 20.0  # Snap distance threshold
        self._snapped_port: Optional[Port] = None  # Currently snapped port

    def add_node(self, node: Node) -> None:
        """Add a node to the scene"""
        self.addItem(node)
        self._nodes.append(node)
        node.setPos(*node.initial_pos)

    def _clear_temp_connection(self) -> None:
        """Clear the temporary connection line and related state"""
        if self._temp_connection:
            self.removeItem(self._temp_connection)
            if self._temp_connection in self._temp_connection.start_port.connections:
                self._temp_connection.start_port.connections.remove(self._temp_connection)
            self._temp_connection = None
        
        # Reset the highlight state of the snapped port
        if self._snapped_port:
            self._snapped_port.set_targeted(False)
            self._snapped_port = None
            
        self._dragging_connection = False

    def start_connection(self, port: Port) -> None:
        """Start creating a connection"""
        if self._temp_connection:
            self._clear_temp_connection()

        # Create a temporary connection line
        self._temp_connection = Connection(port)
        self._temp_connection.setZValue(2)  # Set the Z value of the temporary connection line to the highest

        # Immediately update the endpoint to the current mouse position to avoid initial drawing anomalies
        views = self.views()
        if views:
            view_pos = views[0].mapFromGlobal(QCursor.pos())
            scene_pos = views[0].mapToScene(view_pos)
            self._temp_connection._end_point = scene_pos
        else:
            # Fallback if no view is attached
            self._temp_connection._end_point = port.scenePos()
            
        self._temp_connection.update_path()
        self.addItem(self._temp_connection)
        self._dragging_connection = True  # Mark the start of dragging the connection

    def update_temp_connection(self, pos: QPointF) -> None:
        """Update the endpoint of the temporary connection line and implement snapping"""
        if not self._temp_connection:
            return
            
        # If there was a previously snapped port, reset its state
        if self._snapped_port:
            self._snapped_port.set_targeted(False)
            self._snapped_port = None
        
        # Find the closest compatible port
        closest_port = self.find_closest_compatible_port(pos, self._temp_connection.start_port)
        
        # If a suitable port is found, snap the connection to that port
        if closest_port:
            self._temp_connection._end_point = closest_port.scenePos()
            closest_port.set_targeted(True)  # Highlight the target port
            self._snapped_port = closest_port  # Record the currently snapped port
        else:
            # If no suitable port is found, use the mouse position
            self._temp_connection._end_point = pos
        
        self._temp_connection.update_path()

    def finalize_connection(self, port: Port) -> None:
        """Complete the connection"""
        if not self._temp_connection or self._temp_connection.start_port == port:
            self._clear_temp_connection()
            return
            
        # Check if they belong to the same node
        if self._temp_connection.start_port.node == port.node:
            # Do not allow connections within the same node
            self._clear_temp_connection()
            return
            
        valid_connection = False
        start_port = self._temp_connection.start_port
        
        # Check if the data types are compatible
        if start_port.data_type != port.data_type:
            self._clear_temp_connection()
            return
        
        # Output port connects to input port
        if start_port.port_type is PortType.OUTPUT and port.port_type is PortType.INPUT:
            # If the input port already has a connection, disconnect the original connection first
            self._disconnect_existing_connections(port)
            
            # Establish a new connection
            self._temp_connection.end_port = port
            port.connections.append(self._temp_connection)
            valid_connection = True
            
        # Input port connects to output port (reverse handling)
        elif start_port.port_type is PortType.INPUT and port.port_type is PortType.OUTPUT:
            # If the input port already has other connections, disconnect the original connection first
            # Excluding the currently created connection
            existing_conns = [conn for conn in start_port.connections if conn != self._temp_connection]
            if existing_conns:
                self._disconnect_existing_connections(start_port, exclude_conn=self._temp_connection)
            
            # Adjust the connection direction (very important)
            temp = start_port
            
            # Remove from the connections list before changing the connection object's properties
            if self._temp_connection in temp.connections:
                temp.connections.remove(self._temp_connection)
                
            # Adjust the start and end points of the connection
            self._temp_connection.start_port = port
            self._temp_connection.end_port = temp
            
            # Add the connection to the new start port's connection list
            if self._temp_connection not in port.connections:
                port.connections.append(self._temp_connection)
            
            # Add to the endpoint (original start point) list
            if self._temp_connection not in temp.connections:  
                temp.connections.append(self._temp_connection)
                
            valid_connection = True
        
        # Complete a valid connection
        if valid_connection:
            # Ensure the port state is reset
            if self._snapped_port:
                self._snapped_port.set_targeted(False)
                self._snapped_port = None
                
            self._temp_connection.setZValue(0)  # Restore the Z value of the final connection line to the default
            self._temp_connection.update_path()
            self.connection_created.emit(self._temp_connection)
            self._temp_connection = None
        else:
            # Invalid connection
            self._clear_temp_connection()
            
        self._dragging_connection = False

    def _disconnect_existing_connections(self, port: Port, exclude_conn: Optional[Connection] = None) -> None:
        """Disconnect existing connections from the port"""
        if not port.connections:
            return
            
        existing_conns = port.connections.copy()
        for conn in existing_conns:
            if exclude_conn and conn == exclude_conn:
                continue
                
            # Remove from the scene
            self.removeItem(conn)
            
            # Remove from the connected ports
            if conn.start_port and conn in conn.start_port.connections:
                conn.start_port.connections.remove(conn)
                
            if conn.end_port and conn in conn.end_port.connections:
                conn.end_port.connections.remove(conn)

    def port_at_pos(self, pos: QPointF) -> Optional[Port]:
        """Find the port at the specified position"""
        items = self.items(pos)
        for item in items:
            if isinstance(item, Port):
                return item
        return None

    def find_closest_compatible_port(self, pos: QPointF, start_port: Port) -> Optional[Port]:
        """Find the closest compatible port to the given position
        
        Compatibility means:
        - Ports are not from the same node
        - If the start port is an output port, the target must be an input port, and vice versa
        - Ports must have the same data type
        """
        closest_port = None
        min_distance = self._snap_distance
        
        # Traverse all node ports
        for node in self._nodes:
            # Check if the node is different from the start port's node
            if node == start_port.node:
                continue
                
            # Select the compatible port list
            compatible_ports = node.inputs if start_port.port_type is PortType.OUTPUT else node.outputs
            
            for port in compatible_ports:
                # Check the data type compatibility
                if port.data_type != start_port.data_type:
                    continue
                    
                port_pos = port.scenePos()
                distance = ((port_pos.x() - pos.x()) ** 2 + (port_pos.y() - pos.y()) ** 2) ** 0.5
                
                if distance < min_distance:
                    min_distance = distance
                    closest_port = port
                    
        return closest_port

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        """Handle mouse move event"""
        if self._dragging_connection:
            self.update_temp_connection(event.scenePos())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        """Handle mouse release event"""
        if self._dragging_connection and self._temp_connection:
            # If snapped to a port, use the snapped port to complete the connection
            if self._snapped_port:
                self.finalize_connection(self._snapped_port)
            else:
                # If not snapped, check if there is a port under the mouse
                port = self.port_at_pos(event.scenePos())
                if port:
                    self.finalize_connection(port)
                else:
                    self._clear_temp_connection()
        super().mouseReleaseEvent(event)