from typing import Optional

from PySide6.QtWidgets import QGraphicsItem

from ..bases._node import Node
from ...types.node import NodeSize
from ...types.pos import Point



class BasicNode(Node):
    """Basic node class, providing basic input and output port functionality"""
    
    def __init__(
        self,
        title: str = "Basic Node",
        size: NodeSize = NodeSize(),
        pos: Point = Point(),
        parent: Optional[QGraphicsItem] = None
    ) -> None:
        super().__init__(title, size, pos, parent)
        self.add_input = self.__deprecated
        self.add_output = self.__deprecated
        
    
    def __deprecated(self, *args, **kwargs) -> None:
        """The functionality to add input/output ports has been deprecated"""
        raise NotImplementedError("Method is deprecated in production code.")