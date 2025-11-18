from PySide6.QtWidgets import *
from PySide6.QtCore import *
import sys

app = QApplication(sys.argv)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BS:ED but less bad")

        button = QPushButton("Press Me!")
        self.setFixedSize(QSize(400,300))
        self.setCentralWidget(button)

window = MainWindow()
window.show()

app.exec()