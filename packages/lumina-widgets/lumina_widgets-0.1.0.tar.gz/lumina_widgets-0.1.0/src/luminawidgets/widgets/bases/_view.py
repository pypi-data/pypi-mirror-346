from PySide6.QtWidgets import QGraphicsView
from PySide6.QtGui import QPainter, QWheelEvent

from ._scene import NodeScene


class NodeView(QGraphicsView):
    """Node editor view"""
    def __init__(self, scene: NodeScene) -> None:
        super().__init__(scene)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.scale(1.2, 1.2)

    def wheelEvent(self, event: QWheelEvent) -> None:
        """Handle zooming"""
        factor = 1.2 ** (event.angleDelta().y() / 240)
        self.scale(factor, factor)