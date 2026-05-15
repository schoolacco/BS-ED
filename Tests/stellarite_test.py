import sys
from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QMainWindow, QGraphicsRectItem, QGraphicsPixmapItem, QGraphicsSceneMouseEvent
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QTransform, QBrush
class CustomScene(QGraphicsScene):
    def mousePressEvent(self: QGraphicsScene, event: QGraphicsSceneMouseEvent):
        # Determine which item was clicked
        item = self.itemAt(event.scenePos(), QTransform())
        if item:
            pass
            # Run specific logic
        super().mousePressEvent(event)

# Set up the scene and add items
app = QApplication(sys.argv)
scene = CustomScene(0, 0, 400, 300)
item = scene.addPixmap(QPixmap("Program/Stats/Starglass.webp"))
item.setFlag(QGraphicsPixmapItem.ItemIsMovable, True)
item.setScale(0.1)
brush = QBrush(QPixmap("Program/Stats/gullibilius"))
scene.setBackgroundBrush(brush)
# Create view to display the scene
view = QGraphicsView(scene)
view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
view.setWindowTitle("QGraphicsScene Example")
view.resize(420, 320)
view.show()
sys.exit(app.exec())
