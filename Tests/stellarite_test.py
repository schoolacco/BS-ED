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

    rect = scene.addRect(50, 50, 100, 100)
    

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
