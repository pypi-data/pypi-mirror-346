from math import sqrt
from typing import Optional, TYPE_CHECKING

from PySide6.QtWidgets import QGraphicsItem, QGraphicsPathItem
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QColor, QPen, QPainterPath
from PySide6.QtWidgets import QGraphicsSceneMouseEvent

if TYPE_CHECKING:
    from ._port import Port

from ...types.enums import PortType


class Connection(QGraphicsPathItem):
    """Connection line graphics item"""
    Type = QGraphicsItem.UserType + 3

    def __init__(self, start_port: 'Port', end_port: Optional['Port'] = None) -> None:
        super().__init__()
        self.start_port: Port = start_port
        self.end_port: Optional[Port] = end_port
        self._color: QColor = QColor("#FFA726")
        self.setZValue(0)  # Set the default Z value of the connection line to 0 (below nodes)

        # Ensure the connection is only added once to the start_port's connections
        if self not in self.start_port.connections:
            self.start_port.connections.append(self)
        if self.end_port and self not in self.end_port.connections:
            self.end_port.connections.append(self)

        # Temporary endpoint - initially set to the start position to avoid abnormal curve during initial drawing
        self._end_point: QPointF = self.start_port.scenePos()
        
        # Set flag to ensure the connection line is not selectable
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)

        self.update_path()

    def update_path(self) -> None:
        """Update the connection line path"""
        # Safety check to ensure the ports still exist
        if not self.start_port:
            return
            
        path = QPainterPath()
        sp = self.start_port.scenePos()
        ep = self.end_port.scenePos() if self.end_port else self._end_point
        
        # Simplified Bezier curve control point calculation
        se_distance = sqrt((sp.x() - ep.x()) ** 2 + (sp.y() - ep.y()) ** 2) 
        cp_distance = se_distance / 2.0
        
        # Set the start control point
        if self.start_port.port_type is PortType.OUTPUT:
            # Output port control point to the right
            ctrl1 = QPointF(sp.x() + cp_distance, sp.y())
        else:
            # Input port control point to the left
            ctrl1 = QPointF(sp.x() - cp_distance, sp.y())
        
        # Set the end control point
        if self.end_port:
            # If there is a definite end port
            if self.end_port.port_type is PortType.OUTPUT:
                # End port is an output port, control point to the right
                ctrl2 = QPointF(ep.x() + cp_distance, ep.y())
            else:
                # End port is an input port, control point to the left
                ctrl2 = QPointF(ep.x() - cp_distance, ep.y())
        else:
            # Temporary connection to the mouse position control point
            # Calculate the midpoint from the start to the mouse
            mid_x = (sp.x() + ep.x()) / 2
            # Use a simple control point to make the curve more natural
            ctrl2 = QPointF(mid_x, ep.y())

        path.moveTo(sp)
        path.cubicTo(ctrl1, ctrl2, ep)
        self.setPath(path)

        # Update style
        pen = QPen(self._color)
        pen.setWidthF(2.0)
        self.setPen(pen)
        self.setBrush(Qt.NoBrush)
        
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """Handle mouse click event"""
        super().mousePressEvent(event)
        
        # If right-clicked, pop up the context menu to allow deletion of the connection
        if event.button() == Qt.RightButton:
            self.remove_connection()
            event.accept()
            
    def remove_connection(self) -> None:
        """Remove the current connection"""
        scene = self.scene()
        if not scene:
            return
            
        # Remove from the scene
        scene.removeItem(self)
        
        # Remove from the connection list of both ports
        if self.start_port and self in self.start_port.connections:
            self.start_port.connections.remove(self)
            
        if self.end_port and self in self.end_port.connections:
            self.end_port.connections.remove(self)