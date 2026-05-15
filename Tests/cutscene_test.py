from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt, QTimer
from sys import argv
timer = QTimer()
class Test:
    def __init__(self, text, timer: QTimer):
        self.text = text
        self.instance = 0
        self.timer = timer
    def text_animator(self, label: QLabel):
        if self.instance < len(text):
          label.setText(label.text()+self.text[self.instance])
          self.instance += 1
app = QApplication(argv)
root = QMainWindow()
label = QLabel("")
label.setStyleSheet("""QLabel{
    color: green;
    background-color: black;
    font-weight: bold;
    font-size: 40px;
    }""")
label.setAlignment(Qt.AlignmentFlag.AlignCenter)
root.setCentralWidget(label)
root.show()
text="Are we... connected?"
test = Test(text, timer)
timer.timeout.connect(lambda: test.text_animator(label))
timer.start(250)
app.exec()