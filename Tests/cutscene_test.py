from PySide6.QtWidgets import * 
from PySide6.QtGui import * 
from PySide6.QtCore import Qt, QTimer, QObject
from sys import argv 


class Animation_Handler(QObject): 
    def __init__(self, text, timer: QTimer, end_function=None): 
        self.text = text 
        self.instance = 0 
        self.instance_2 = 0 
        self.timer = timer
        self.func = end_function

    def text_animator(self, label: QLabel): 
        if self.timer.interval() == 1500:
          label.setText("") 
        self.timer.setInterval(150)
        
        if self.instance_2 < len(self.text): 
            if self.instance < len(self.text[self.instance_2]): 
                label.setText(label.text() + self.text[self.instance_2][self.instance]) 
                self.instance += 1 
            else: 
                self.timer.setInterval(1500)
                self.instance = 0 
                self.instance_2 += 1 
        else:
            self.timer.stop()
            self._on_end()
    def _on_end(self):
      if self.func:
        self.func()


class ScanlineOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Allows clicks to pass through to the label underneath
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        self.bar_y = 0  # Initial vertical position of the bar
        self.bar_height = 80  # Thickness of the rolling bar
        
        # Timer to drive the scanline animation (60 FPS = ~16ms)
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.update_position)
        self.anim_timer.start(16)

    def update_position(self):
        self.bar_y += 2.5  # Speed of the moving bar
        if self.bar_y > self.height():
            self.bar_y = -self.bar_height  # Reset to top when it exits the bottom
        self.update()  # Triggers paintEvent

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Create a semi-transparent green color (Alpha: 25)
        bar_color = QColor(0, 255, 0, 25) 
        painter.fillRect(0, self.bar_y, self.width(), self.bar_height, bar_color)

class Cutscene(QMainWindow):
    def __init__(self, text: list, text_color: str, bg: str, overlay: bool=False):
        super().__init__()
        self.container = QWidget()
        self.c_layout = QGridLayout(self.container)
        self.c_layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel("")
        self.label.setStyleSheet(f"""QLabel{{ color: {text_color}; background-color: {bg}; font-weight: bold; font-size: 40px; }}""")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.overlay = ScanlineOverlay() if overlay else None
        self.c_layout.addWidget(self.label)
        if self.overlay:
            self.c_layout.addWidget(self.overlay, 0, 0)
        self.showFullScreen()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.timer = QTimer()
        test = Animation_Handler(text, self.timer)
        self.setCentralWidget(self.container)
        self.timer.timeout.connect(lambda: test.text_animator(self.label)) 
        self.timer.start(250) 

# --- Main Application Setup ---
app = QApplication(argv) 

text = ["Are we... connected?", "Can you hear me?", "...", "I see...", "Welcome, Player.", "Your presence here... is unprecedented.", "Perhaps... you will be of use...", "But that, is yet to be of concern for you...", "First, your connection to this world must be secured...", "Lest you be lost within the penumbra of infinity.", "You must reassemble the reality tether...", "Once you succeed you shall enter the Main World: Buttonia.", "You will be unable to return to this place for an indeterminate amount of time.", "Good luck, Player."] 

root = Cutscene(text, "green", "black", True) 

root.show()

app.exec()
