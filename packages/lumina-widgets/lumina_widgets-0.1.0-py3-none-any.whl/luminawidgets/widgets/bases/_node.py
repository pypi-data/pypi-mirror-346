import uuid

from typing import List, Optional, Tuple, Any

from PySide6.QtWidgets import (
    QStyleOptionGraphicsItem,
    QGraphicsItem, QWidget
)
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QColor, QPainterPath

from ._port import Port

from ...types.node import NodeSize
from ...types.enums import PortType, DataType
from ...types.pos import Point



class Node(QGraphicsItem):
    """Basic node graphics item"""
    Type = QGraphicsItem.UserType + 1

    def __init__(
        self,
        title: str = "Node",
        size: NodeSize = NodeSize(),
        pos: Point = Point(),
        parent: Optional[QGraphicsItem] = None
    ) -> None:
        super().__init__(parent)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setZValue(1) # <--- Set the Z value of the node to 1 (higher than the connection line)

        # Node properties
        self.uuid: str = str(uuid.uuid4())
        self.title: str = title
        self.width: int = size.width
        self.height: int = size.height
        self.radius: float = size.radius
        self.title_height: float = size.title_height
        self.port_spacing: float = size.port_spacing
        self.initial_pos: Tuple[int, int] = (pos.x, pos.y)

        # Style
        self._color_background: QColor = QColor("#3D3D3D")
        self._color_title: QColor = QColor("#2D2D30")

        # Port management
        self.inputs: List[Port] = []
        self.outputs: List[Port] = []
        self.init_ports()
        self._update_port_positions()

    def init_ports(self) -> None:
        """Initialize ports"""
        self.add_port("Input 1", PortType.INPUT, DataType.INT, QColor("#4CAF50"))
        self.add_port("Output 1", PortType.OUTPUT, DataType.INT, QColor("#FF5252"))

    def add_port(
        self,
        name: str = "port",
        port_type: PortType = PortType.INPUT,
        data_type: DataType = DataType.INT,
        color: Optional[QColor] = None
    ) -> None:
        port = Port(self, name, port_type, data_type, color)
        if port_type is PortType.INPUT:
            self.inputs.append(port)
        else:
            self.outputs.append(port)
        self._update_port_positions()

    def _update_port_positions(self) -> None:
        """Update the positions of all ports"""
        # Input port positions - left side
        for i, port in enumerate(self.inputs):
            port_y = self.title_height + self.port_spacing * (i + 1)
            port.setPos(0, port_y)

        # Output port positions - right side
        for i, port in enumerate(self.outputs):
            port_y = self.title_height + self.port_spacing * (i + 1)
            port.setPos(self.width, port_y)

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self.width, self.height).normalized()

    def paint(self, painter: QPainter, option: 'QStyleOptionGraphicsItem', widget: Optional['QWidget'] = None) -> None:
        """Draw the node"""
        # Draw the main body
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width, self.height, self.radius, self.radius)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._color_background)
        painter.drawPath(path.simplified())

        # Draw the title bar
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width, self.title_height, 
                          self.radius, self.radius)
        painter.setBrush(self._color_title)
        painter.drawPath(path.simplified())

        # Draw the title text
        painter.setPen(QColor("#FFFFFF"))
        painter.drawText(QRectF(0, 0, self.width, self.title_height), 
                        Qt.AlignCenter, self.title)

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value: Any) -> Any:
        """Handle position changes"""
        if change == QGraphicsItem.ItemPositionHasChanged:
            for port in self.inputs + self.outputs:
                for conn in port.connections:
                    conn.update_path()
        return super().itemChange(change, value)
