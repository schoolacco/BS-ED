from Module import Gluttony
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
app = QApplication(sys.argv)
root = QMainWindow()
test = Gluttony(["Fat Orange (Outermost Layer): 10 HP", "Fat Orange (Outer Layer): 5 HP", "Fat Orange (Inner Layer): 3 HP", "Fat Orange (Innermost Layer): 1 HP"], 0, root)
root.setCentralWidget(test)
root.show()
app.exec()