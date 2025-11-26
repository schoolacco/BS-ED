from PySide6.QtWidgets import *
from Module import GradientLabel
app = QApplication()

window = QMainWindow()

label = GradientLabel("Test", ["#ffffff","#00ffff" "#000000"], 6, parent=window)
label.repaint()
window.setCentralWidget(label)
window.show()
app.exec()
