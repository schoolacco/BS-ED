from tkinter import *
import math
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import inspect
import os
import ctypes
import colorama
from pathlib import Path
# Source - https://stackoverflow.com/a
# Posted by luke, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-30, License - CC BY-SA 3.0
FILE_ATTRIBUTE_HIDDEN = 0x02
FILE_ATTRIBUTE_SYSTEM = 0x04
def write_hidden(file_name, data):
    """
    Cross platform hidden file writer.
    """
    # For *nix add a '.' prefix.
    prefix = '.' if os.name != 'nt' else ''
    file_name = prefix + file_name

    # Write file.
    with open(file_name, 'w') as f:
        f.write(data)

    # For windows set file attribute.
    if os.name == 'nt':
        ret = ctypes.windll.kernel32.SetFileAttributesW(file_name,
                                                        FILE_ATTRIBUTE_HIDDEN|FILE_ATTRIBUTE_SYSTEM)
        if not ret: # There was an error.
            raise ctypes.WinError()
#End of atrributions stuff
def documents():
    # Windows & macOS: simple and correct
    base = Path.home() / "Documents"
    if base.exists():
        return base

    # Linux (XDG Documents specification)
    xdg_user_dirs = Path.home() / ".config" / "user-dirs.dirs"
    if xdg_user_dirs.exists():
        text = xdg_user_dirs.read_text()
        for line in text.splitlines():
            if line.startswith("XDG_DOCUMENTS_DIR"):
                path = line.split("=")[1].strip().strip('"')
                path = path.replace("$HOME", str(Path.home()))
                p = Path(path)
                if p.exists():
                    return p

    # Fallback
    return Path.home()
DOCUMENTS_PATH = documents()
def blinded(parent):
    if not os.path.exists(str(DOCUMENTS_PATH)+"\\toodarktosee"):
      print("Traceback (most recent call last):")
      print('  File "Module.py", line 128, in <module>')
      print("    test_function()")
      print("RuntimeError: Unexpected internal failure")
      print(colorama.Fore.BLACK + "YOU'RE JUST TOO BLIND TO SEE IT.")
      write_hidden(str(DOCUMENTS_PATH)+"\\toodarktosee", "Are you not afraid of what cannot be seen? \n You search for the impossible, what has never been found \n Yet you wish to harness its energy, the energy of DARKMATTER.")
      parent.close()
def button_inspect(cmd, btn):
    signature = inspect.signature(cmd)
    params = len(signature.parameters)
    if params == 0:
        return cmd()
    else:
        return cmd(btn)
class Mantissa:
    def __init__(self, mantissa, exponent):
        self.num = mantissa
        self.exp = exponent
    def __mul__(a, b):
      # a and b are (mantissa, exponent) tuples
      if isinstance(a, (int,float)):
          a = float_to_mantissa(a)
      if isinstance(b, (int,float)):
          b = float_to_mantissa(b)
      new_mantissa = a.num * b.num
      new_exponent = a.exp + b.exp
      
      # Normalize if mantissa >= 10
      while new_mantissa >= 10:
          new_mantissa /= 10
          new_exponent += 1
      return Mantissa(new_mantissa, new_exponent)
    def __add__(a, b):
      # Ensure a has the bigger exponent
      if isinstance(a, (int,float)):
          a = float_to_mantissa(a)
      if isinstance(b, (int,float)):
          b = float_to_mantissa(b)
      if a.exp < b.exp:
          a, b = b, a  # swap references, do not mutate
  
      diff = a.exp - b.exp
      if diff > 300:  # treat b as negligible
          return Mantissa(a.num, a.exp)
  
      # Safe addition for reasonably close exponents
      new_mantissa = a.num + b.num * 10**-diff
      while new_mantissa >= 10:
        new_mantissa /= 10
        a.exp += 1
      return Mantissa(new_mantissa, a.exp)
    def __iadd__(a, b):
        total = a + b
        return total
    def __round__(self, num):
        self.num = round(self.num, num)
        return self
    def __ge__(self, other):
        if isinstance(self, (int, float)):
            self = float_to_mantissa(self)
        if isinstance(other, (int, float)):
            other = float_to_mantissa(other)
        return True if self.exp > other.exp else True if self.exp == other.exp and self.num >= other.num else False
    def __sub__(a,b):
        b.num = -b.num
        return a + b
    def __truediv__(a,b):
        mantissa = a.num/b.num
        exp = a.exp-b.exp
        while mantissa <= 1:
            mantissa*= 10
            exp -= 1
        return Mantissa(mantissa, exp)
    def __lt__(self, other):
        return not self >= other
    def to_string(self):
       return f"{self.num:.3f}e{self.exp}"
    def to_dict(self):
        return {"__mantissa__": True, "number": self.num, "exponent": self.exp}

    @classmethod
    def from_dict(cls, data):
        return cls(data["number"], data["exponent"])
    def to_float(self):
        """Convert the Mantissa to a regular float. Warning: may overflow for huge exponents."""
        value =  self.num * (10 ** self.exp) if self.exp < 300 else self
        if not isinstance(value, Mantissa):
            if 1 <= value < 2e9:
                return int(value)
        return value
def float_to_mantissa(value: float) -> Mantissa:
      """Converts a float or int into a Mantissa representation."""
      if isinstance(value, Mantissa):
          return value
      if value == 0:
          return Mantissa(0, 0)
      exponent = int(math.floor(math.log10(abs(value))))
      mantissa = value / (10 ** exponent)
      return Mantissa(mantissa, exponent)
class tkinter_frames:


  def create_scrollable_area(parent, button_groups, bg="black", text_color="white", voltaic_radar=False):
    """
    Creates a scrollable area using PySide6 that mimics your tkinter scrollable canvas system.
    Returns: (outer_container, scroll_area, content_widget)
    """

    # --- Outer container widget ---
    outer_container = QWidget(parent)
    outer_layout = QVBoxLayout(outer_container)
    outer_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    #outer_container.setMinimumHeight(500)
    outer_layout.setContentsMargins(0, 0, 0, 0)

    # --- Scroll Area ---
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setStyleSheet(f"background-color: {bg};")
    outer_layout.addWidget(scroll_area)

    # --- Scrollable content widget ---
    content_widget = QWidget()
    content_widget.setStyleSheet(f"background-color: {bg}; color: {text_color};")

    grid = QGridLayout(content_widget)
    grid.setAlignment(Qt.AlignTop)

    scroll_area.setWidget(content_widget)
    if "Unknown" in button_groups.keys():
        parent.voltaic_random = VoltaicRandomizer(enable_count=50, interval_ms=20000, voltaic_radar=voltaic_radar, always_texts=["Spawn (req: 0 Cash)","Recover Hall (req: 0 Cash)"])
        num = 1 if voltaic_radar else 100
        if random.randint(1,num) != 1:
          del button_groups["Unknown"]
    else:
      parent.voltaic_random = None
    # --- Populate columns and buttons ---
    for col_index, (group_name, buttons) in enumerate(button_groups.items()):

        # Group Title
        group_label = QLabel(group_name)
        group_label.setStyleSheet(
            f"color: {text_color}; background-color: {bg}; font-weight: bold; font-size: 14px;"
        )
        grid.addWidget(group_label, 0, col_index, alignment=Qt.AlignHCenter)

        # Buttons inside group
        for row_index, (text, command) in enumerate(buttons, start=1):
            btn = QPushButton(text)
            btn.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {bg};
                    color: {text_color};
                    padding: 6px;
                    border: 1px solid {text_color};
                }}
                QPushButton:hover {{
                    background-color: #222;
                }}
                """
            )
            grid.addWidget(btn, row_index, col_index, alignment=Qt.AlignTop)
            if not parent.voltaic_random:  
              btn.clicked.connect(lambda _, b=btn, cmd=command: button_inspect(cmd, b))
              continue
            index = len(parent.voltaic_random.buttons)
            parent.voltaic_random.buttons.append({"btn": btn, "command": command})
            if text in parent.voltaic_random.always_texts:
              parent.voltaic_random.always_indices.add(index)
    if parent.voltaic_random:
        parent.voltaic_random.start()
        button_groups["Unknown"] = [("", lambda: blinded(parent))]
    return outer_container, scroll_area, content_widget

class GradientLabel(QLabel):
    def __init__(self, text, colors, angle_deg=90, parent=None):
        """
        text: string
        colors: list of QColor
        angle_deg: angle of gradient in degrees (0 = left→right, 90 = top→bottom)
        """
        super().__init__(text, parent)
        self.colors = colors
        self.angle_deg = angle_deg
        self.setMinimumWidth(1)

    def paintEvent(self, event):
        if (self.colors, self.angle_deg) != None:
          painter = QPainter(self)
          painter.setRenderHint(QPainter.Antialiasing)
          painter.setRenderHint(QPainter.TextAntialiasing)
  
          font = self.font()
          fm = QFontMetrics(font)
  
          # Create the text path
          path = QPainterPath()
          path.addText(0, fm.ascent(), font, self.text())
  
          # Compute gradient direction
          angle_rad = math.radians(self.angle_deg)
          w = self.width()
          h = self.height()
  
          x1 = w / 2 - math.cos(angle_rad) * w
          y1 = h / 2 - math.sin(angle_rad) * h
          x2 = w / 2 + math.cos(angle_rad) * w
          y2 = h / 2 + math.sin(angle_rad) * h
  
          gradient = QLinearGradient(QPointF(x1, y1), QPointF(x2, y2))
  
          # Distribute colors evenly
          stops = len(self.colors)
          for i, c in enumerate(self.colors):
              gradient.setColorAt(i / (stops - 1), QColor(c))
  
          painter.setBrush(gradient)
          painter.setPen(Qt.NoPen)
          painter.drawPath(path)
  
import random

class Geode:
    def __init__(self, items, cost, unit):
        """
        items: dict -> { "ItemName": rarity_weight }
        Lower weight = rarer item
        cost: Mantissa or float, automatically converted unless exponent >= 300
        unit: key in save file currency dictionary (e.g. "Gems", "Crystals")
        """
        self.items = items
        self.cost = cost.to_float() if isinstance(cost, Mantissa) and cost.exp < 300 else cost
        self.unit = unit

    def open(self, file, luck=1.0, bulk_roll=1, crit_luck=1):
      luck += (random.randint(100, 777) / 100) - 1
      for i in range(bulk_roll):
        if not isinstance(file["Main"][self.unit]["Value"],Mantissa): #Skips cost check as if value is a Mantissa cost is always negligible (prices will never be that high)
          if file["Main"][self.unit]["Value"] < self.cost:
              return file
          file["Main"][self.unit]["Value"] -= self.cost
    
        adjusted_items = {}
    
        # Adjust weights with luck (only common items)
        for item, data in self.items.items():
            weight = data["Chance"]
            if weight >= 8001:
                weight /= luck
            adjusted_items[item] = max(weight, 1e-6)
    
        # Normalize total sum to original
        Total = sum(v["Chance"] for v in self.items.values())
        new_total = sum(adjusted_items.values())
        scale = Total / new_total
        for item in adjusted_items:
            adjusted_items[item] *= scale
    
        # Convert to probabilities (inverse weighting)
        total = sum(1 / w for w in adjusted_items.values())
        probabilities = [1 / w / total for w in adjusted_items.values()]
    
        # Roll item
        item = random.choices(list(adjusted_items.keys()), weights=probabilities, k=1)[0]
        msg = f"You obtained a common {item} (1/{self.items[item]['Chance']})" if self.items[item]['Chance'] < 10000 else f"You obtained an INSANELY RARE {item} (1/{self.items[item]['Chance']})!" if self.items[item]['Chance'] >= 100000000 else f"You obtained a Rare {item} (1/{self.items[item]['Chance']})" if 10000 <= self.items[item]['Chance'] < 1000000 else f"You obtained a Very Rare {item} (1/{self.items[item]['Chance']})!"
        print(msg)
        # Add item to inventory
        if file["Main"].get(item) is not None:
            val = 2 if random.randint(1,500) == 1 else 1
            if isinstance(file["Main"][item]["Value"], Mantissa):
                val = float_to_mantissa(val)
            file["Main"][item]["Value"] += val
        elif file["Secret"].get(item) is not None: # Not the most efficient method, but I'm working with redundant code
            val = 2 if random.randint(1,500) == 1 else 1
            file["Secret"][item]["Value"] += val
        elif file["Exclusive"].get(item) is not None:
            val = 2 if random.randint(1,500) == 1 else 1
            file["Exclusive"][item]["Value"] += val
        elif file["Event"].get(item) is not None:
            val = 2 if random.randint(1,500) == 1 else 1
            file["Event"][item]["Value"] += val
        elif file["Geode"].get(item) is not None:
            file["Geode"][item]["Value"] += 2 if random.randint(1,500//crit_luck) == 1 else 1
        else:
            file["Geode"][item] = {"Multis": self.items[item]["Multis"], "Value": 1}
        file["Extra"]["Geodes Opened"]["Value"] += 1
      return file

class VoltaicRandomizer:
    def __init__(self, enable_count=10, interval_ms=20000, voltaic_radar=False, always_texts=None):
        self.enable_count = enable_count
        self.interval_ms = interval_ms
        self.buttons = []   
        self.timer = None
        self.radar = voltaic_radar
        self.always_texts = set(always_texts) if always_texts else set()
        self.always_indices = set() 

    def start(self):
        """Start the periodic reshuffling."""
        if not self.radar:
          self.shuffle()
          if self.timer is None:
              self.timer = QTimer()
              self.timer.timeout.connect(self.shuffle)
              self.timer.start(self.interval_ms)
        else:
            for i, item in enumerate(self.buttons):
              btn = item["btn"]
              cmd = item["command"]
              # ENABLED BUTTON
              btn.setEnabled(True)
              btn.setStyleSheet("""
                  QPushButton {
                      color: white;     
                      background-color: #111;
                      padding: 6px;
                      border: 1px solid white;
                  }
                  QPushButton:hover {
                      background-color: #222;
                  }
              """)
              btn.clicked.disconnect()
              btn.clicked.connect(cmd)
    def shuffle(self):
      if not self.buttons:
          return
  
      indices = list(range(len(self.buttons)))
  
      # Everything except the always-enabled ones
      random_pool = [i for i in indices if i not in self.always_indices]
  
      # How many random buttons are allowed after always-enabled ones are included
      remaining = self.enable_count - len(self.always_indices)
      remaining = max(0, remaining)
  
      enable_set = set(self.always_indices)
  
      if remaining > 0:
        enable_set |= set(random.sample(random_pool, min(remaining, len(random_pool))))

  
      # Apply styles
      for i, item in enumerate(self.buttons):
          btn = item["btn"]
          cmd = item["command"]
  
          if i in enable_set:
              btn.setEnabled(True)
              btn.setStyleSheet("""
                  QPushButton {
                      color: white;     
                      background-color: #111;
                      padding: 6px;
                      border: 1px solid white;
                  }
                  QPushButton:hover {
                      background-color: #222;
                  }
              """)
              btn.clicked.disconnect()
              btn.clicked.connect(cmd)
  
          else:
              btn.setEnabled(False)
              btn.setStyleSheet("""
                  QPushButton {
                      color: #111; 
                      background-color: #111;
                      padding: 6px;
                      border: 1px solid white;
                  }
              """)



