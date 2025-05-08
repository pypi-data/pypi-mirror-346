from typing import List, Optional, Any, TYPE_CHECKING

from PySide6.QtWidgets import QGraphicsItem, QWidget
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont
from PySide6.QtWidgets import QGraphicsSceneMouseEvent, QGraphicsSceneHoverEvent

if TYPE_CHECKING:
    from ._node import Node
    from ._connection import Connection

from ...types.enums import PortType, DataType



class Port(QGraphicsItem):
    """Port graphics item"""
    Type = QGraphicsItem.UserType + 2

    def __init__(
        self,
        node: 'Node',
        name: str = "port",
        port_type: PortType = PortType.INPUT,
        data_type: DataType = DataType.INT,
        color: QColor | str | None = None
    ) -> None:
        super().__init__(node)
        self.node: Node = node
        self.port_type: PortType = port_type
        self.name: str = name
        self.data_type: DataType = data_type
        self.radius: float = 6.0
        self.margin: float = 2.0
        
        # Set default color based on port type
        if color:
            self._color: QColor = color if isinstance(color, QColor) else QColor(color if isinstance(color, str) else "#4CAF50")
        else:
            is_output: bool = port_type is PortType.OUTPUT
            self._color: QColor = QColor("#FF5252") if is_output else QColor("#4CAF50")
            
        self._highlight_color: QColor = QColor("#FFA726")  # Highlight color
        self.connections: List[Connection] = []
        self._is_hovered: bool = False  # Mouse hover state
        self._is_targeted: bool = False  # State when connection is near
        
        # Set flags
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)  # Accept mouse hover events

    def set_color(self, color: QColor) -> None:
        """Set port color"""
        self._color = color
        self.update()

    def set_targeted(self, targeted: bool) -> None:
        """Set whether the port is targeted by a connection"""
        if self._is_targeted != targeted:
            self._is_targeted = targeted
            self.update()

    def boundingRect(self) -> QRectF:
        # Slightly larger bounding rectangle for easier mouse hover detection
        hover_margin = 4.0  # Increase bounding rectangle size to accommodate outer highlight ring
        # Extend bounding rect to include data type text
        width_extension = 50.0  # Space for data type text
        if self.port_type == PortType.INPUT:
            return QRectF(-self.radius - hover_margin, -self.radius - hover_margin, 
                         2*(self.radius + hover_margin) + width_extension, 2*(self.radius + hover_margin))
        else:  # OUTPUT
            return QRectF(-self.radius - hover_margin - width_extension, -self.radius - hover_margin, 
                         2*(self.radius + hover_margin) + width_extension, 2*(self.radius + hover_margin))

    def paint(self, painter: QPainter, option, widget: Optional[QWidget] = None) -> None:
        """Draw port"""
        # Maintain original port radius
        base_radius = self.radius
        
        # First draw the base port circle (maintain original color)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self._color))
        painter.drawEllipse(QRectF(-base_radius, -base_radius, 2*base_radius, 2*base_radius))
        
        # If in highlight state, draw outer orange ring
        if self._is_hovered or self._is_targeted:
            # Set orange ring pen
            highlight_pen = QPen(self._highlight_color)
            highlight_pen.setWidthF(1.5)  # Set ring width
            painter.setPen(highlight_pen)
            painter.setBrush(Qt.NoBrush)  # Do not fill the inside of the ring
            
            # Draw a slightly smaller ring
            ring_radius = base_radius - 1.5
            painter.drawEllipse(QRectF(-ring_radius, -ring_radius, 2*ring_radius, 2*ring_radius))
        
        # Draw data type text
        text = self.data_type.value
        font = QFont()
        font.setPointSize(8)
        painter.setFont(font)
        painter.setPen(QPen(Qt.white))
        
        # Position text based on port type
        text_margin = 4.0
        if self.port_type == PortType.INPUT:
            # For input ports, position text on the right side
            painter.drawText(base_radius + text_margin, base_radius/2, text)
        else:
            # For output ports, position text on the left side
            text_width = painter.fontMetrics().horizontalAdvance(text)
            painter.drawText(-base_radius - text_margin - text_width, base_radius/2, text)

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value: Any) -> Any:
        """Update connection position"""
        if change == QGraphicsItem.ItemScenePositionHasChanged:
            for conn in self.connections:
                conn.update_path()
        return super().itemChange(change, value)

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        """Mouse enter event"""
        self._is_hovered = True
        self.update()
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        """Mouse leave event"""
        self._is_hovered = False
        self.update()
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """Handle mouse click - start connection"""
        from ._scene import NodeScene  # Resolve circular import issue
        
        scene = self.scene()
        if isinstance(scene, NodeScene):
            if event.button() == Qt.LeftButton:
                # Prevent event from propagating to parent node to avoid node being dragged
                event.accept()

                # If input port and already has a connection, disconnect existing connection and start new connection
                if self.port_type is PortType.INPUT and self.connections:
                    existing_conn = self.connections[0] # Input port has only one connection
                    other_port = existing_conn.start_port # Get the output port on the other end

                    # Remove old connection from scene
                    scene.removeItem(existing_conn)
                    # Remove from connection lists of both ports
                    if existing_conn in self.connections:
                        self.connections.remove(existing_conn)
                    if other_port and existing_conn in other_port.connections:
                        other_port.connections.remove(existing_conn)

                    # Start new connection from the output port on the other end
                    scene.start_connection(other_port)
                    return

                # Handle existing temporary connection or create new connection
                if scene._temp_connection:
                    # If there is an existing temporary connection, try to complete the connection
                    scene.finalize_connection(self)
                else:
                    # Otherwise start a new connection
                    scene.start_connection(self)
            elif event.button() == Qt.RightButton:
                # Right-click port to disconnect all connections
                event.accept()
                
                if self.connections:
                    # Make a copy of the list to avoid modifying the list while iterating
                    conns_copy = self.connections.copy()
                    for conn in conns_copy:
                        conn.remove_connection()
            else:
                super().mousePressEvent(event)
        else:
            super().mousePressEvent(event)