import sys
from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView
from PySide6.QtGui import QColor, QPen, QBrush
from PySide6.QtCore import Qt

def main():
    app = QApplication(sys.argv)

    # 1. Create the QGraphicsScene (the surface for items)
    scene = QGraphicsScene()
    
    # Optional: Set the scene's size
    scene.setSceneRect(0, 0, 400, 300) 

    # 2. Define pen and brush for drawing
    # Create a pen for the outline (blue, solid line, 2 pixels width)
    pen = QPen(QColor(Qt.GlobalColor.blue))
    pen.setWidth(2)
    
    # Create a brush for the fill color (cyan)
    brush = QBrush(QColor(Qt.GlobalColor.cyan))

    # 3. Add an item to the scene (a rectangle)
    # addRect(x, y, width, height, pen, brush)
    rect = scene.addRect(50, 50, 100, 100, pen, brush)
    
    # Optional: Make the item movable
    rect.setFlag(QGraphicsItem.ItemIsMovable) # Note: QGraphicsItem needs to be imported

    # 4. Create the QGraphicsView (the widget that visualizes the scene)
    view = QGraphicsView(scene)
    
    # Optional: Enable antialiasing for smoother rendering
    view.setRenderHint(QPainter.Antialiasing) # Note: QPainter needs to be imported

    # 5. Display the view
    view.setWindowTitle("PySide6 QGraphicsView Example")
    view.resize(500, 400)
    view.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    # Import necessary classes within the script for clarity
    from PySide6.QtWidgets import QGraphicsItem
    from PySide6.QtGui import QPainter
    main()
