import math
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import scipy.special as sci
import inspect
import os
import ctypes
import colorama
from pathlib import Path
import random
import sys
import numpy as np
import re
from functools import partial
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
# Source - https://stackoverflow.com/a
# Posted by luke, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-30, License - CC BY-SA 3.0
FILE_ATTRIBUTE_HIDDEN = 0x02
FILE_ATTRIBUTE_SYSTEM = 0x04
def write_hidden(file_name: str, data: str) -> None:
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
def documents() -> str:
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
def blinded(parent: QMainWindow) -> str:
    if not os.path.exists(str(DOCUMENTS_PATH)+"\\toodarktosee"):
      print("Traceback (most recent call last):")
      print('  File "Module.py", line 128, in <module>')
      print("    test_function()")
      print("RuntimeError: Unexpected internal failure")
      print(colorama.Fore.BLACK + "YOU'RE JUST TOO BLIND TO SEE IT.")
      write_hidden(str(DOCUMENTS_PATH)+"\\toodarktosee", "Are you not afraid of what cannot be seen? \n You search for the impossible, what has never been found \n Yet you wish to harness its energy, the energy of DARKMATTER.")
      parent.close()
def button_inspect(cmd, btn: QPushButton):
    signature = inspect.signature(cmd)
    params = len(signature.parameters)
    if params == 0:
        return cmd()
    else:
        return cmd(btn)
def find_key_path(nested_dict: dict, target_key_name: str, current_path: dict|None=None) -> list:
    """
    Recursively searches for a specific key name in a nested dictionary
    and returns the full path of keys to that key's location.
    """
    if current_path is None:
        current_path = []

    for key, value in nested_dict.items():
        new_path = current_path + [key]

        if key == target_key_name:
            # The key name matches our target! Return the path up to this point.
            return new_path
        
        elif isinstance(value, dict):
            # Recursively search in nested dictionaries
            found_path = find_key_path(value, target_key_name, new_path)
            if found_path:
                return found_path
    
    # Key not found in this branch
    return None

class Mantissa:
    def __init__(self, mantissa: int|float, exponent: int) -> object:
        self.num = mantissa
        self.exp = exponent
    def __mul__(a: int|float|object, b: int|float|object) -> object:
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
    def __add__(a: int|float|object, b: int|float|object) -> object:
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
    def __iadd__(a: int|float|object, b: int|float|object) -> object:
        total = a + b
        return total
    def __round__(self: object, num: int) -> object:
        self.num = round(self.num, num)
        return self
    def __ge__(self: object, other: int|float|object) -> bool:
        if other == math.inf: return False
        if isinstance(self, (int, float)):
            self = float_to_mantissa(self)
        if isinstance(other, (int, float)):
            other = float_to_mantissa(other)
        return True if self.exp > other.exp else True if self.exp == other.exp and self.num >= other.num else False
    def __sub__(a: int|float|object,b: int|float|object) -> object:
        if isinstance(a, (int,float)):
          a = float_to_mantissa(a)
        if isinstance(b, (int,float)):
          b = float_to_mantissa(b)
        b.num = -b.num
        return a + b
    def __truediv__(a: int|float|object,b: int|float|object) -> object:
        if isinstance(a, (int,float)):
          a = float_to_mantissa(a)
        if isinstance(b, (int,float)):
          b = float_to_mantissa(b)
        mantissa = a.num/b.num
        exp = a.exp-b.exp
        while mantissa <= 1:
            mantissa*= 10
            exp -= 1
        return Mantissa(mantissa, exp)
    def __lt__(self: object, other: int|float|object) -> bool:
        return not self >= other
    def __gt__(self: object, other: int|float|object) -> bool:
        return not self <= other
    def __le__(self: object, other: int|float|object) -> bool:
        return not self > other
    def to_string(self: object) -> str:
       return f"{self.num:.2f}e+{self.exp}"
    def to_dict(self: object) -> dict:
        return {"__mantissa__": True, "number": self.num, "exponent": self.exp}
    @classmethod
    def from_string(cls, string: str) -> object:
        segments = string.split("e")
        segments = [i.strip("+") for i in segments]
        for segment in segments:
            try:
                segments.remove(segment)
                segments.append(int(round(float(segment))))
            except ValueError:
                return None #Invalid input
        if len(segments) != 2:
            return None #Invalid input
        return cls(segments[1], int(segments[0]))
    @classmethod
    def from_dict(cls, data: dict) -> object:
        return cls(data["number"], data["exponent"])
    def to_float(self: object) -> float | object:
        """Convert the Mantissa to a regular float. Warning: may overflow for huge exponents."""
        value =  self.num * (10 ** self.exp) if self.exp < 300 else self
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
  '''Not renaming this'''

  def create_scrollable_area(parent: QMainWindow, button_groups: list[QPushButton], bg: str="black", text_colour: str="white", voltaic_radar: bool=False) -> tuple:
    """
    Creates a scrollable area using PySide6.
    Returns: (outer_container: QWidget, scroll_area: QScrollArea, content_widget: QWidget)
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
    content_widget.setStyleSheet(f"background-color: {bg}; color: {text_colour};")

    grid = QGridLayout(content_widget)
    grid.setAlignment(Qt.AlignTop)

    scroll_area.setWidget(content_widget)
    if "Unknown" in button_groups.keys():
        parent.voltaic_random = VoltaicRandomizer(enable_count=50, interval_ms=20000, voltaic_radar=voltaic_radar, always_texts=["Spawn (req: 0 Cash)","Recover Hall (req: 0 Cash)"])
        num = 10 if voltaic_radar else 100
        if random.randint(1,num) != 1:
          del button_groups["Unknown"]
    else:
      parent.voltaic_random = None
    # --- Populate columns and buttons ---
    for col_index, (group_name, buttons) in enumerate(button_groups.items()):

        # Group Title
        group_label = QLabel(group_name)
        group_label.setStyleSheet(
            f"color: {text_colour}; background-color: {bg}; font-weight: bold; font-size: 14px;"
        )
        grid.addWidget(group_label, 0, col_index, alignment=Qt.AlignHCenter)

        # Buttons inside group
        for row_index, (text, command, type) in enumerate(buttons, start=1):
            if type == "Button":
              obj = QPushButton(text)
            elif type == "Label":
              obj = QLabel(text)
            obj.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {bg};
                    color: {text_colour};
                    padding: 6px;
                    border: 1px solid {text_colour};
                }}
                QPushButton:hover {{
                    background-color: #222;
                }}
                QLabel {{
                    background-color: {bg};
                    color: {text_colour}
                }}
                """
            )
            grid.addWidget(obj, row_index, col_index, alignment=Qt.AlignTop)
            if type == "Button":
              if not parent.voltaic_random:  
                obj.clicked.connect(lambda _, b=obj, cmd=command: button_inspect(cmd, b))
                continue
              index = len(parent.voltaic_random.buttons)
              parent.voltaic_random.buttons.append({"btn": obj, "command": command})
              if text in parent.voltaic_random.always_texts:
                parent.voltaic_random.always_indices.add(index)
    if parent.voltaic_random:
        parent.voltaic_random.start()
        button_groups["Unknown"] = [("", lambda: blinded(parent))]
    return outer_container, scroll_area, content_widget

class GradientLabel(QLabel):
    def __init__(self,text: str,colors: list[str],angle_deg: int|float=90,parent: QObject=None,stroke_color: str=None,stroke_width: int|float=0):
        super().__init__(text, parent)

        self.colors = colors
        self.angle_deg = angle_deg
        self.stroke_color = QColor(stroke_color) if stroke_color else None
        self.stroke_width = stroke_width

        font = self.font()
        font.setPointSizeF(font.pointSizeF() * 1.25)
        font.setHintingPreference(QFont.HintingPreference.PreferFullHinting)
        font.setBold(True)
        self.setFont(font)


        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, event):
        '''Paint = on label change/creation'''
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.Antialiasing |
            QPainter.TextAntialiasing |
            QPainter.SmoothPixmapTransform
        )

        font = self.font()
        fm = QFontMetrics(font)

        # ---- Build text path ----
        path = QPainterPath()
        path.addText(0, fm.ascent(), font, self.text())

        bounds = path.boundingRect()

        # Center text
        dx = (self.width()  - bounds.width())  / 2 - bounds.x()
        dy = (self.height() - bounds.height()) / 2 - bounds.y()
        path.translate(dx, dy)
        bounds.translate(dx, dy)

        # ---- Optional stroke ----
        if self.stroke_color and self.stroke_width > 0:
            pen = QPen(self.stroke_color, self.stroke_width)
            pen.setJoinStyle(Qt.RoundJoin)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(path)

        # ---- Gradient bound to TEXT ----
        angle = math.radians(90 - self.angle_deg)
        cx = bounds.center().x()
        cy = bounds.center().y()

        length = max(bounds.width(), bounds.height()) * 0.75
        x1 = cx - math.cos(angle) * length
        y1 = cy - math.sin(angle) * length * -1
        x2 = cx + math.cos(angle) * length
        y2 = cy + math.sin(angle) * length * -1

        gradient = QLinearGradient(QPointF(x1, y1), QPointF(x2, y2))

        stops = len(self.colors)
        for i, col in enumerate(self.colors):
            gradient.setColorAt(i / (stops - 1), QColor(col))

        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.drawPath(path)

class Geode:
    def __init__(self, items: dict, cost: Mantissa|float|int, unit: str) -> object:
        """
        items: dict -> { "ItemName": rarity_weight }
        Lower weight = rarer item
        cost: Mantissa or float, automatically converted unless exponent >= 300
        unit: key in save file currency dictionary (e.g. "Gems", "Crystals")
        """
        self.items = items
        self.cost = cost.to_float() if isinstance(cost, Mantissa) and cost.exp < 300 else cost
        self.unit = unit

    def open(self, file: dict, luck: float=1.0, bulk_roll: int=1, crit_luck: int=1):
      luck += (random.randint(100, 777) / 100) - 1 #Something that was meant to be an event, but is now permanent
      for i in range(bulk_roll):
        if not isinstance(file["Stats"][self.unit],Mantissa): #Skips cost check as if value is a Mantissa cost is always negligible (prices will never be that high)
          if file["Stats"][self.unit] < self.cost:
              return file
          file["Stats"][self.unit] -= self.cost
    
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
        if luck > Total:
            probabilities = [1 for i in range(len(adjusted_items.values()))]
        # Roll item
        item = random.choices(list(adjusted_items.keys()), weights=probabilities, k=1)[0]
        msg = f"You obtained a common {item} (1/{self.items[item]['Chance']})" if self.items[item]['Chance'] < 10000 else f"You obtained an INSANELY RARE {item} (1/{self.items[item]['Chance']})!" if self.items[item]['Chance'] >= 100000000 else f"You obtained a Rare {item} (1/{self.items[item]['Chance']})" if 10000 <= self.items[item]['Chance'] < 1000000 else f"You obtained a Very Rare {item} (1/{self.items[item]['Chance']})!"
        if "rare" in msg.lower():
            print(msg)
        # Add item to inventory
        if file["Stats"].get(item):
          file["Stats"][item] += 2 if random.randint(1,int(500//crit_luck)) == 1 else 1
        else:
          file["Stats"][item] = 2 if random.randint(1,int(500//crit_luck)) == 1 else 1
        file["Stats"]["Geodes Opened"] += 1
      return file

class VoltaicRandomizer:
    def __init__(self, enable_count: int=10, interval_ms: int=20000, voltaic_radar: bool=False, always_texts: list|None=None):
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


class RotatedLabel(QLabel):
    def __init__(self, text: str="", angle: int=0, parent: QObject|None=None):
        super().__init__(text, parent)
        self.angle = angle

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self.angle)
        painter.translate(-self.width() / 2, -self.height() / 2)

        painter.setFont(self.font())
        painter.setPen(self.palette().color(QPalette.WindowText))

        painter.drawText(self.rect(), self.alignment(), self.text())

def build_cythrex_index(stat_info: dict, meta_data: dict) -> dict:
    index = {}

    def walk(tree: dict):
        for key, value in tree.items():
            if isinstance(value, dict):
                # leaf stat = has Multis
                if "Multis" in value:
                    yield key
                else:
                    yield from walk(value)

    for stat in walk(stat_info):
        meta = meta_data.get(stat, {})

        index[stat.lower()] = {
            "name": stat,
            "tags": [t.lower() for t in meta.get("tags", [])],
            "has_meta": stat in meta_data
        }

    return index

def resolve_search(query: str, index: dict) -> list:
    query = query.strip().lower()
    if not query:
        return []

    words = query.split()
    results = []
    seen = set()

    # 1. Exact name match (highest priority)
    if query in index:
        results.append(index[query]["name"])
        seen.add(query)

    # 2. Partial name OR tag matching
    for key, entry in index.items():
        if key in seen:
            continue

        name_match = any(word in key.split(" ") for word in words)
        tag_match = any(
            word in tag.split(" ")
            for word in words
            for tag in entry["tags"]
        )

        if name_match or tag_match:
            results.append(entry["name"])
            seen.add(key)
    # 3. Lowest priority, name in search, allows for results for partial searches only triggers if there have been no results so far.
    if results == []:
      for key, entry in index.items():
          if key in seen:
              continue
  
          name_match = any(word in key for word in words)
  
          if name_match:
              results.append(entry["name"])
              seen.add(key)
    return results



def find_key_path(nested_dict: dict, target_key_name: str, current_path: list|None=None) -> list|None:
    """
    Recursively searches for a specific key name in a nested dictionary
    and returns the full path of keys to that key's location.
    """
    if current_path is None:
        current_path = []

    for key, value in nested_dict.items():
        if key != "Multis": # Don't take the wrong path
          new_path = current_path + [key]

          if key == target_key_name:
              # The key name matches our target! Return the path up to this point.
              return new_path
          
          elif isinstance(value, dict):
              # Recursively search in nested dictionaries
              found_path = find_key_path(value, target_key_name, new_path)
              if found_path:
                  return found_path
    
    # Key not found in this branch
    return None
class BootScreen(QDialog):
    finished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: black;")
        self.setWindowTitle("Loading...")
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # ── Rotated title ───────────────────────
        self.title = RotatedLabel("CYTHERAX-47", angle=20)
        self.title.setFont(QFont("Consolas", 32, QFont.Bold))
        self.title.setStyleSheet("color: #00ff00;")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFixedSize(400, 200)
        
        
        layout.addStretch()
        layout.addWidget(self.title)
        layout.addStretch()

        # ── Loading bar ────────────────────────
        self.bar_container = QHBoxLayout()
        self.bar_container.setSpacing(4)
        self.bar_container.setAlignment(Qt.AlignCenter)

        self.chunks = []
        self.chunk_count = 16

        for _ in range(self.chunk_count):
            chunk = QFrame()
            chunk.setFixedSize(20, 20)
            chunk.setStyleSheet("""
                QFrame {
                    background-color: #002200;
                    border: 1px solid #005500;
                }
            """)
            self.chunks.append(chunk)
            self.bar_container.addWidget(chunk)

        layout.addLayout(self.bar_container)

        # ── Animation timer ────────────────────
        self.index = 0
        self.timer = QTimer(self)
        self.timer.singleShot(random.randint(100,1000), self.advance)

    def advance(self):
        if self.index < len(self.chunks):
            self.chunks[self.index].setStyleSheet("""
                QFrame {
                    background-color: #00ff00;
                    border: 1px solid #00aa00;
                }
            """)
            self.index += 1
            self.timer.singleShot(random.randint(50,500), self.advance)
        else:
            self.timer.stop()
            QTimer.singleShot(300, self.finish)

    def finish(self):
        self.finished.emit()
        self.close()
class CY47Window(QDialog):
    def __init__(self, stat_info, meta_data, stat_list, stat_gradients, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CY-47 :: SYSTEM INTERFACE")
        self.resize(1000, 650)
        self.stat_info = stat_info
        self.meta_data = meta_data
        self.stat_list = stat_list
        self.gradients = stat_gradients
        self.index = build_cythrex_index(self.stat_info, self.meta_data)
        self.root = QVBoxLayout(self)
        self.root.setSpacing(8)
        self.setStyleSheet('''QWidget {
            background-color: black;
            }''')

        # ── Header ─────────────────────────────────────────────
        header = QHBoxLayout()

        title = QLabel("Cythrex-47")
        title.setStyleSheet('''QLabel {
            color: green;
            background-color: black;
            }''')
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search database…")
        self.search.returnPressed.connect(self.on_search)
        self.search.setStyleSheet('''QLineEdit {
            color: green;
            background-color: black;
            }''')

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.search, 2)

        self.root.addLayout(header)
        
        self.page_container = QVBoxLayout()
        self.root.addLayout(self.page_container)
        
        self.current_page = None
        self.show_default_page()
        self.image = None
    def _clear_layout(self, layout):
      while layout.count():
          item = layout.takeAt(0)
  
          widget = item.widget()
          child_layout = item.layout()
  
          if widget is not None:
              widget.setParent(None)
              widget.deleteLater()
  
          elif child_layout is not None:
              self._clear_layout(child_layout)

    def clear_page(self):
      if self.current_page is not None:
          self._clear_layout(self.current_page)
          self.current_page.setParent(None)
          self.current_page = None

    def show_default_page(self):
      self.clear_page()
  
      layout = QVBoxLayout()
  
      title = QLabel("CY-47 DATABASE INTERFACE")
      title.setFont(QFont("Segoe UI", 20, QFont.Bold))
      title.setAlignment(Qt.AlignCenter)
      title.setStyleSheet("color: green;")
  
      subtitle = QLabel(
          "Awaiting query...\n\n"
          "• Search for a stat by name\n"
          "• Use tags to discover related entries\n"
          "• CY-47 © AIHA Corp."
      )
      subtitle.setAlignment(Qt.AlignCenter)
      subtitle.setStyleSheet("color: green;")
  
      layout.addStretch()
      layout.addWidget(title)
      layout.addSpacing(10)
      layout.addWidget(subtitle)
      layout.addStretch()
  
      self.page_container.addLayout(layout)
      self.current_page = layout

    def generate_content(self, stat):
        # Right: main info panel
        if stat not in self.meta_data:
          self.show_default_page()
          return

        self.clear_page()
        self.content = QHBoxLayout()
        self.right_panel = QVBoxLayout()

        # Stat name (gradient handled later via stylesheet)
        self.stat_name = GradientLabel(stat, self.gradients.get(stat, self.gradients["Default"])["Colours"], self.gradients.get(stat, self.gradients["Default"])["Angle"], stroke_color=self.gradients.get(stat, self.gradients["Default"]).get("S_Colour", None), stroke_width=self.gradients.get(stat, self.gradients["Default"]).get("S_Width", None))
        self.stat_name.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.stat_name.setAlignment(Qt.AlignCenter)

        self.right_panel.addWidget(self.stat_name)

        # Image + info row
        mid_row = QHBoxLayout()
        path = find_key_path(self.stat_info, stat)
        # Left text
        left_info = QVBoxLayout()
        self.stat_type = QLabel(f"Type: {path[0]}")
        self.stat_type.setFont(QFont("Segoe UI", 10))
        self.stat_type.setStyleSheet('''QLabel {
            color: green;
            background-color: black;
            }''')

        self.lore = QTextEdit()
        self.lore.setStyleSheet('''QTextEdit {
            color: green;
            background-color: black;
            }''')
        self.lore.setReadOnly(True)
        self.lore.setText(self.meta_data[stat]["lore"])

        left_info.addWidget(self.stat_type)
        left_info.addWidget(self.lore)

        mid_row.addLayout(left_info, 3)

        # Right image
        self.image = QLabel(self)
        image = self.gradients.get(stat, self.gradients["Default"]).get("File", None)
        if image == None:
          files = [f for f in os.listdir("Program/Stats") if os.path.isfile(os.path.join("Program/Stats", f))]
          if f"{stat}.webp" in files:
            self.image.setPixmap(QPixmap(f"Program/Stats/{stat}.webp"). scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
          else:
            self.image.setPixmap(QPixmap(f"Program/Stats/Missing.webp"). scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.image.setPixmap(QPixmap(f"Program/Stats/{image}.webp"). scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.image.setFixedSize(500,500)
        self.image.setFrameShape(QFrame.Box)
        self.image.setAlignment(Qt.AlignCenter)
        self.image.setStyleSheet('''QLabel {
            background-color: black;
            }''')
        mid_row.addWidget(self.image, 2)

        self.right_panel.addLayout(mid_row)

        # Bottom: obtainment
        self.obtainment = QFrame()
        self.obtainment.setFrameShape(QFrame.StyledPanel)
        self.obtainment_layout = QVBoxLayout(self.obtainment)

        self.obtainment_label = QTextEdit()
        self.obtainment_label.setReadOnly(True)
        self.obtainment_label.setText(self.meta_data[stat]["obtainment"])
        self.obtainment_label.setStyleSheet('''QTextEdit {
            color: green;
            background-color: black;
            }''')

        self.obtainment_layout.addWidget(self.obtainment_label)

        self.right_panel.addWidget(self.obtainment)
        
        self.left_panel = QVBoxLayout()
        
        # Left: multipliers
        self.multiplier_list = QListWidget()
        self.multiplier_list.setFixedWidth(260)
        if len(path) == 2:
          if self.stat_info[path[0]][stat]["Multis"]:
            for Stat, multi in self.stat_info[path[0]][stat]["Multis"].items():
                if Stat and multi:
                  self.multiplier_list.addItem(f"{Stat} x{multi if not isinstance(multi, Mantissa) else multi.to_string()}")
          else:
              self.multiplier_list.addItem("Nothing")
        else:
            if self.stat_info[path[0]][path[1]][stat]["Multis"]:
              for Stat, multi in self.stat_info[path[0]][path[1]][stat]["Multis"].items():
                  if Stat and multi:
                    multi_text = f"{Stat} x{multi if not isinstance(multi, Mantissa) else multi.to_string()}" if multi < 1e6 else f"{Stat} x{'{:.2e}'.format(multi) if not isinstance(multi, Mantissa) else multi.to_string()}"
                    self.multiplier_list.addItem(multi_text)
            else:
                self.multiplier_list.addItem("Nothing")
        self.multiplier_list.setStyleSheet('''QListWidget {
            color: green;
            background-color: black;
            }''')
        self.multiplier_header = QLabel("Stat Multipliers:")
        self.multiplier_header.setStyleSheet('''QLabel {
            color: green;
            background-color: black;
            }''')
        self.content.addLayout(self.right_panel, 1)
        
        self.left_panel.addWidget(self.multiplier_header, 1)
        
        self.left_panel.addWidget(self.multiplier_list, 20)
        
        self.content.addLayout(self.left_panel, 1)
        
        self.page_container.addLayout(self.content)
        self.current_page = self.content

    def show_no_results_page(self, query):
        self.clear_page()
    
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
    
        title = QLabel("NO MATCHING ENTRIES FOUND")
        title.setFont(QFont("Consolas", 18, QFont.Bold))
        title.setStyleSheet("color: red;")
    
        subtitle = QLabel(f"Query: \"{query}\"")
        subtitle.setFont(QFont("Consolas", 10))
        subtitle.setStyleSheet("color: green;")
    
        hint = QLabel("Refine query or search by known designation.")
        hint.setStyleSheet("color: #00aa00;")
    
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(12)
        layout.addWidget(hint)
    
        self.page_container.addLayout(layout)
        self.current_page = layout

    
    def on_search(self):
      query = self.search.text().strip()
  
      if not query:
          self.show_default_page()
          return
  
      results = resolve_search(query, self.index)
  
      if results:
          if len(results) == 1 and results[0].lower() == query.lower():
              self.generate_content(results[0])
          else:
              self.show_results_page(results, query)

      else:
          self.show_no_results_page(query)

    def show_results_page(self, results, query):
      self.clear_page()
  
      outer = QVBoxLayout()
  
      header = QLabel(f'SEARCH RESULTS FOR: "{query}"')
      header.setFont(QFont("Consolas", 14, QFont.Bold))
      header.setStyleSheet("color: green;")
      
      count = QLabel(f"{len(results)} ENTR{'Y' if len(results) == 1 else 'IES'} FOUND")
      count.setFont(QFont("Consolas", 10))
      count.setStyleSheet("color: #00aa00;")
      
      outer.addWidget(header)
      outer.addWidget(count)
  
      scroll = QScrollArea()
      scroll.setWidgetResizable(True)
      scroll.setStyleSheet("border: none;")
  
      container = QWidget()
      layout = QVBoxLayout(container)
  
      for result in results:
          btn = QPushButton()
          btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
          btn.setMinimumHeight(40)
          
          label = QLabel(result)
          label.setWordWrap(True)
          label.setStyleSheet("color: green;")
          label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
          
          layout_inner = QHBoxLayout(btn)
          layout_inner.setContentsMargins(8, 4, 8, 4)
          layout_inner.addWidget(label)

  
          btn.setStyleSheet("""
              QPushButton {
                  color: green;
                  background-color: black;
                  border: 1px solid green;
                  padding: 6px;
                  text-align: left;
              }
              QPushButton:hover {
                  background-color: #002200;
              }
          """)
  
          btn.clicked.connect(lambda _, r=result: self.generate_content(r))
          btn.setFont(QFont("Consolas", 10))
          btn.setCursor(Qt.PointingHandCursor)
          layout.addWidget(btn)
  
      layout.addStretch()
      scroll.setWidget(container)
  
      outer.addWidget(scroll)
      self.page_container.addLayout(outer)
      self.current_page = outer
    def closeEvent(self, event: QCloseEvent):
        event.ignore()
        self.hide()

#----- Graphite Minigame -----
np.seterr(all="ignore")
stylesheet = open(r"Program\graphite.qss", "r")
stylesheet = stylesheet.read()
# ---------- CONFIG ----------

TOLERANCE = 0.01  # Allowed error for match check
MODE_NORMAL = "normal"
MODE_SKY_HIGH = "sky_high"

# ---------- UTILITY: preprocess input ----------
def preprocess_for_eval(expr: str) -> str:
    expr = expr.replace(" ", "")
    expr = expr.replace("^", "**")
    #while "|" in expr:
    #    expr = re.sub(r"\|([^|]+)\|", r"abs(\1)", expr)
    funcs = "|".join(["sin","cos","tan","abs","pi","sinh","cosh","tanh","e", "sqrt", "exp"])
    expr = re.sub(rf"(\d+(\.\d+)?)(?=(x|\(|{funcs})\b)", r"\1*", expr)
    expr = re.sub(r"([x)])(\d+(\.\d+)?)", r"\1*\2", expr)
    expr = re.sub(rf"([x)])(?=({funcs})\()", r"\1*", expr)
    expr = re.sub(r"\)\(", r")*(", expr)
    return expr
def break_asymptotes(y: np.ndarray[np.any], threshold: int=10):
    '''
    Break any asymptotes by turning extremely large jumps into NaNs, y is an np array
    '''
    y = y.astype(float).copy()

    # Break on non-finite values
    y[~np.isfinite(y)] = np.nan

    # Detect large jumps between consecutive points
    dy = np.abs(np.diff(y))

    # Insert NaNs AFTER large jumps
    jump_indices = np.where(dy > threshold)[0] + 1
    y[jump_indices] = np.nan

    return y
# ---------- SAFE EVAL ENV ----------
SAFE_ENV = {
    "sin": np.sin, "cos": np.cos, "tan": np.tan,
    "abs": np.abs, "pi": np.pi,
    "sinh": np.sinh, "cosh": np.cosh, "tanh": np.tanh,
    "e": np.e, "sqrt": np.sqrt, "exp": np.exp, "ln": np.log,
    "arcsin": np.arcsin, "arccos": np.arccos, "arctan": np.arctan,
    "arcsinh": np.arcsinh, "arccosh": np.arccosh, "arctanh": np.arctanh,
    "erf": sci.erf, "gamma": sci.gamma
}

def eval_expr(expr: str, x: np.ndarray[np.float64]):
    expr = preprocess_for_eval(expr)
    env = SAFE_ENV.copy()
    env["x"] = x
    return eval(expr, {"__builtins__": {}}, env)

# ---------- RANDOM EQUATION GENERATOR ----------
LINEAR_FUNCS = ["linear"]
POLYNOMIAL_FUNCS = ["quadratic","cubic","quartic"]
HYPERBOLAS = ["1/x","1/x^2","1/(x+a)^2"]
TRIG_FUNCS = ["sin","cos","tan"]
HYPERBOLIC_FUNCS = ["sinh","cosh","tanh"]
OTHER_FUNCS = ["abs","sqrt","exp", "ln", "arcsin", "arccos", "arctan", "arcsinh", "arccosh", "arctanh", "erf", "gamma"]

def random_constant(low: int=-5, high: int=5, allow_float: bool=True):
    constant = 0
    while constant == 0:
      constant =  round(random.uniform(low, high), 1) if allow_float else random.randint(low, high)
    return constant

def generate_linear():
    a = random.randint(-10,10)
    b = random.randint(-10,10)
    return f"{a}*x + {b}"

def generate_polynomial():
    degree = random.randint(2,4)
    factors = [f"(x - {random.randint(-5,5)})" for _ in range(degree)]
    a = random.choice([-3,-2,-1,1,2,3])
    return f"{a}*{'*'.join(factors)}"

def generate_hyperbola(chain: bool=True):
    eq = "x"
    for _ in range(random.randint(1,2) if chain else 1):
        shift = random.choice([-1,1,2])
        power = random.choice([1,2])
        eq = f"1/({eq}+{shift})**{power}"
    return eq

def generate_trig(chained: bool=False):
    func = random.choice(TRIG_FUNCS)
    a = random.choice([-2,-1,1,2])
    freq = random.randint(1,3)
    shift = random.choice([-2,-1,1,2])
    inner = "x"
    if chained:
        inner = f"{random.choice([lambda: f'x**{random.randint(2,4)}', lambda: generate_hyperbola(chain=True), lambda: generate_trig(chained=True)])()}"  # can chain with simple expressions
    return f"{a}*{func}({freq}*{inner} + {shift})"

def generate_hyper_trig(chained: bool=False):
    func = random.choice(HYPERBOLIC_FUNCS)
    a = random_constant(-2,2)
    freq = random_constant(1,3)
    shift = random_constant(-2,2)
    inner = "x"
    if chained:
        inner = f"{random.choice([lambda: f'x**{random.randint(2,4)}',lambda: f'x{random.randint(-10,10)}', lambda: generate_trig(chained=True), lambda: generate_hyper_trig(chained=True), lambda: generate_hyperbola(chain=True)])()}"
    return f"{a}*{func}({freq}*{inner} + {shift})"

def generate_other_func(chained: bool=False):
    func = random.choice(OTHER_FUNCS)
    a = random_constant(-2,2)
    inside = f"x + {random_constant(-2,2)}"
    if chained:
        inside = f"{random.choice([lambda:generate_trig(chained=True), lambda:generate_hyper_trig(chained=True), lambda: f'x**{random.randint(2,10)}', lambda: generate_hyperbola(chain=True), lambda:generate_other_func(chained=True)])()}"
    return f"{a}*{func}({inside})"

def generate_level_equation(level: int, bonus: bool=False):
    """
    Generates an equation according to the rules for levels 1-10.
    If bonus=True, derivative/integral mode (not implemented).
    """
    terms = []

    if level == 1:
        # Linear only
        return generate_linear()
    elif level == 2:
        # Quadratics–quartics
        return generate_polynomial()
    elif level == 3:
        # Hyperbolas, can chain but no addition
        return generate_hyperbola(chain=True)
    elif level == 4:
        # Trig & hyperbolic trig, addition allowed, no chaining
        for _ in range(random.randint(2,4)):
            terms.append(random.choice([generate_trig, generate_hyper_trig])(chained=False))
        return " + ".join(terms)
    elif level == 5:
        # Linear + trig/hyperbolic trig, addition + chaining allowed
        linear = generate_linear()
        trig_term = random.choice([generate_trig, generate_hyper_trig])(chained=True)
        return f"{linear} + {trig_term}"
    elif level == 6:
        # Trig/hyperbolic + powers + hyperbolas, chaining allowed, no linear or addition
        choices = [lambda: generate_trig(chained=True), lambda: generate_hyper_trig(chained=True), lambda: generate_hyperbola(chain=True)]
        return random.choice(choices)()
    elif level == 7:
        # Chaining of all prior content, no addition
        choices = [lambda: generate_hyperbola(chain=True),
                   lambda: generate_trig(chained=True),
                   lambda: generate_hyper_trig(chained=True)]
        return random.choice(choices)()
    elif level == 8:
        # Level 7 + other functions, chaining allowed
        choices = [lambda: generate_other_func(chained=True)]
        return random.choice(choices)()
    elif level == 9:
        # Addition of functions, no chaining
        for _ in range(random.randint(4,8)):
            choices = [generate_linear, generate_polynomial,
                       lambda: generate_trig(chained=False),
                       lambda: generate_hyper_trig(chained=False),
                       generate_hyperbola, lambda: generate_other_func(chained=False)]
            terms.append(random.choice(choices)())
        return " + ".join(terms)
    elif level == 10:
        # Addition of chained + unchained functions
        for _ in range(random.randint(8,15)):
            choices = [generate_linear, generate_polynomial, generate_hyperbola,
                       lambda: generate_trig(chained=True),
                       lambda: generate_hyper_trig(chained=True),
                       lambda: generate_other_func(chained=True)]
            terms.append(random.choice(choices)())
        return " + ".join(terms)
    else:
        return generate_linear()  # fallback

# ---------- NUMERIC MATCH CHECK ----------
def check_match_numeric(target_expr: str, player_expr: str, x: np.ndarray[np.float64], tol: float=TOLERANCE):
    try:
        y_target = np.array(eval_expr(target_expr, x), dtype=float)
        y_player = np.array(eval_expr(player_expr, x), dtype=float)
        y_target[~np.isfinite(y_target)] = np.nan
        y_player[~np.isfinite(y_player)] = np.nan
        error = np.nanmean(np.abs(y_target - y_player))
        return error < tol
    except Exception:
        return False
#(15/100^0.4) * x^0.4 + 0.85x
def max_gradient_percentile(x: np.ndarray[np.float64], y: np.ndarray[np.any], percentile: int=95, xmin: int=0, xmax: int=100):
    mask = (x >= xmin) & (x <= xmax) & np.isfinite(y)
    if np.count_nonzero(mask) < 2:
        return np.inf

    dy_dx = np.gradient(y[mask], x[mask])
    slopes = np.abs(dy_dx)

    return np.nanpercentile(slopes, percentile)

def reaches_height(x: np.ndarray[np.float64], y: np.ndarray[np.any], target: int=100, xmin: int=0, xmax: int=100):
    mask = (x >= xmin) & (x <= xmax) & np.isfinite(y)
    if not np.any(mask):
        return False
    return np.nanmax(y[mask]) >= target

def is_trivial_linear(x: np.ndarray[np.float64], y: np.ndarray[np.any], tol: float=1e-3):
    finite = np.isfinite(y)
    if np.count_nonzero(finite) < 3:
        return False

    dx = np.diff(x[finite])
    dy = np.diff(y[finite])

    slopes = dy / dx
    return np.all(np.abs(slopes - 1) < tol)


def sky_high_check(x: np.ndarray[np.float64], y: np.ndarray[np.any]):
    if not np.any(np.isfinite(y)):
        return False, "Graph is empty"
    
    if is_trivial_linear(x, y):
        return False, "Trivial linear solution (y = x) is not allowed"
    
    if max_gradient_percentile(x, y) > 1.22:
        return False, "Gradient exceeded maximum angle (approx 50°)"

    if not reaches_height(x, y):
        return False, "Did not reach y = 100"
    # Must touch origin
    idx = np.argmin(np.abs(x - 0))
    y_at_zero = y[idx]
    
    if not np.isfinite(y_at_zero) or abs(y_at_zero) > 1e-2:
        return False, "Graph must pass through the origin (0, 0)"

    return True, "Sky High Structuring complete, perhaps you are worthy of Esadrhium."


# ---------- GUI ----------
class GameState:
    def __init__(self, mode: str=MODE_NORMAL):
        self.points = 0
        self.level = 1
        self.unlocks = {"sky_high": False}
        self.mode = mode
class BolicalWorld(QDialog):
        def __init__(self, stat_data: dict, parent: QObject|None=None, game_state: GameState|None=None) -> object:
            super().__init__(parent)
            self.data = stat_data
            self.setStyleSheet(stylesheet)
            self.setWindowTitle("Bolical World")
            self.resize(900,700)
            self.state = game_state or GameState()
            self.state.points = self.data["Keys"]["Bolical Points"]
            self.stack = QStackedWidget(self) # Things don't die now
            layout = QVBoxLayout(self)
            layout.addWidget(self.stack)
            self.menu = self.create_menu()
            self.guide = self.create_guide()
            self.shop = ShopPage(game_state=self.state, parent=self)
            self.difficulty_select = self.create_difficulty_select()
            self.graph = GraphPuzzle(game_state=self.state, parent=self)
            
            for page in [self.menu, self.guide, self.shop, self.difficulty_select, self.graph]:
                self.stack.addWidget(page)
            self.stack.setCurrentWidget(self.menu)
        def create_menu(self):
            page = QWidget()
            layout = QVBoxLayout(page)
            layout.setAlignment(Qt.AlignCenter)
            
            title = QLabel("Bolical World")
            title.setStyleSheet("color: #00ff88; font-size: 32px; font-weight: bold;")
            title.setAlignment(Qt.AlignCenter)
            layout.addWidget(title)
            
            play = QPushButton("Play")
            guide = QPushButton("Guide")
            shop = QPushButton("Shop")
            self.structure = QPushButton("Sky High Structuring")
            self.structure.hide()
            for btn in (play, guide, shop, self.structure):
                btn.setFixedSize(200, 50)
                layout.addWidget(btn)
            play.clicked.connect(lambda: self.stack.setCurrentWidget(self.difficulty_select))
            guide.clicked.connect(lambda: self.stack.setCurrentWidget(self.guide))
            shop.clicked.connect(lambda: self.open_shop())
            self.structure.clicked.connect(lambda: self.start_structuring())
            
            return page
        def create_guide(self):
            page = QWidget()
            layout = QVBoxLayout(page)
            
            guide = QLabel("Goal: Guess the equation of the graph. Use sin, cos, tan, etc.\nYou earn points by matching the target equation. Difficulty increases points although graphs will become exponentially harder.\nLevel 1 graphs give you 1 point\nLevel 2 graphs give you 3 points\nLevel 3 graphs give you 5 points\nLevel 4 graphs give you 10 points\nLevel 5 graphs give you 30 points\nLevel 6 graphs give you 50 points\nLevel 7 graphs give you 100 points\nLevel 8 graphs give you 500 points\nLevel 9 graphs give you 10,000 points and are not recommended\nLevel 10 graphs give you 1,000,000 points but are nearly imposssible to crack.")
            guide.setWordWrap(True)
            guide.setStyleSheet("color: #00ff88; font-size: 14px;")
            layout.addWidget(guide)
            
            back = QPushButton("Back")
            back.clicked.connect(lambda: self.stack.setCurrentWidget(self.menu))
            layout.addWidget(back)
            return page
        def create_difficulty_select(self):
            page = QWidget()
            layout = QVBoxLayout(page)
            layout.setAlignment(Qt.AlignCenter)
            
            label = QLabel("Select Difficulty")
            label.setStyleSheet("color: #00ff88; font-size: 24px;")
            layout.addWidget(label)
            
            for i in range(1, 11):
                btn = QPushButton(f"Level {i}")
                btn.setFixedSize(150, 40)
                btn.clicked.connect(lambda checked, lvl=i: self.start_game(lvl))
                layout.addWidget(btn)
            
            back = QPushButton("Back")
            back.clicked.connect(lambda: self.stack.setCurrentWidget(self.menu))
            layout.addWidget(back)
            return page
        def start_game(self, level: int):
            self.state.level = level
            # recreate the graph puzzle with new difficulty
            self.graph.next_graph(level)
            self.graph.title.setText(f"Bolical World | LEVEL {level}")
            self.stack.setCurrentWidget(self.graph)
        def start_structuring(self):
            self.state.mode = MODE_SKY_HIGH
            self.graph.reset_sky_high()
            self.stack.setCurrentWidget(self.graph)
        def open_shop(self):
            self.shop.points_label.setText(f"Points: {self.state.points}")
            self.stack.setCurrentWidget(self.shop)
        def closeEvent(self, event: QCloseEvent):
            self.data["Keys"]["Bolical Points"] = self.state.points
            event.accept()
class ShopPage(QWidget):
    def __init__(self, game_state: GameState, parent: QObject|None=None) -> object:
        super().__init__(parent)
        self.state = game_state
        self.parentwin = parent
        self.setStyleSheet("background-color: black;")
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        # Title
        title = QLabel("Shop")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #00ff88; font-size: 20px; font-weight: bold;")
        self.layout.addWidget(title)

        # Points display
        self.points_label = QLabel(f"Points: {self.state.points}")
        self.points_label.setAlignment(Qt.AlignCenter)
        self.points_label.setStyleSheet("color: #00ffaa; font-size: 14px;")
        self.layout.addWidget(self.points_label)

        # Scrollable area for items
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        self.shop_widget = QWidget()
        self.shop_layout = QGridLayout(self.shop_widget)
        self.shop_layout.setContentsMargins(10, 10, 10, 10)
        self.shop_layout.setSpacing(15)
        
        self.scroll_area.setWidget(self.shop_widget)
        self.layout.addWidget(self.scroll_area)
        self.item_buttons = {}

        # Sop items
        self.items = [
            {"name": "Tetra", "price": 5, "type": "infinite", "purchased": False},
            {"name": "Sky High Structuring", "price": 100, "type": "1 purchase", "purchased": False},
            {"name": "Graphite", "price": 500, "type": "1 purchase", "purchased": False},
            {"name": "Master Tetra", "price": 5000, "type": "infinite", "purchased": False},
            {"name": "Tesseract", "price": 1000000, "type": "1 purchase", "purchased": False}
        ]

        self.item_buttons = {}
        self.build_shop()

        # Back button
        back_btn = QPushButton("Back to Menu")
        back_btn.setStyleSheet(stylesheet)
        back_btn.clicked.connect(self.go_back)
        self.layout.addWidget(back_btn)

    def build_shop(self):
      self.item_buttons = {}
      for row, item in enumerate(self.items):
          name_label = QLabel(item["name"])
          name_label.setStyleSheet("color: #00ffaa; font-size: 14px;")
          self.shop_layout.addWidget(name_label, row, 0)
  
          price_btn = QPushButton()
          price_btn.setStyleSheet(stylesheet)
          price_btn.clicked.connect(partial(self.buy_item, item))
  
          self.shop_layout.addWidget(price_btn, row, 1)
          self.item_buttons[item["name"]] = price_btn
  
          self.update_item_button(item)
      if self.parentwin.data["Keys"]["Sky-High Structuring"]:
          self.item_buttons["Sky High Structuring"].setEnabled(False)
          self.items[1]["purchased"] = True
          self.parentwin.structure.show()
      if self.parentwin.data["Stats"]["Graphite"] >= 1:
          self.item_buttons["Graphite"].setEnabled(False)
          self.items[2]["purchased"] = True
      if self.parentwin.data["Stats"]["Tesseract"] >= 1:
          self.item_buttons["Tesseract"].setEnabled(False)
          self.items[3]["purchased"] = True
    
    def showEvent(self, event: QShowEvent):
       super().showEvent(event)
       self.update_points()
    
    def update_item_button(self, item: dict):
        btn = self.item_buttons[item["name"]]
        if item["type"] == "1 purchase" and item["purchased"]:
            btn.setText("Purchased")
            btn.setEnabled(False)
            btn.setStyleSheet("color: #555; background-color: #001100; border: 1px solid #004400; padding: 8px; font-size: 14px;")
        else:
            btn.setText(f"{item['price']} pts")
            btn.setEnabled(self.state.points >= item["price"])

    def buy_item(self, item: dict):
        if item["type"] == "1 purchase" and item["purchased"]:
            return  # Safety check

        if self.state.points >= item["price"]:
            self.state.points -= item["price"]

            if item["type"] == "1 purchase":
                item["purchased"] = True

            if item["name"] == "Sky High Structuring":
                self.state.unlocks["sky_high"] = True
                self.parentwin.structure.show()
                self.parentwin.data["Keys"]["Sky-High Structuring"] = True
            elif item["name"] == "Tetra":
                self.parentwin.data["Stats"]["Tetra"] += 1
            elif item["name"] == "Graphite":
                self.parentwin.data["Stats"]["Graphite"] = 1 if self.parentwin.data["Stats"]["Graphite"] < 1 else self.parentwin.data["Stats"]["Graphite"]
            elif item["name"] == "Tesseract":
                self.parentwin.data["Stats"]["Tesseract"] = 1 if self.parentwin.data["Stats"]["Tesseract"] < 1 else self.parentwin.data["Stats"]["Tesseract"]
            self.update_points()

    def update_points(self):
        self.points_label.setText(f"Points: {self.state.points}")
        for item in self.items:
            self.update_item_button(item)

    def go_back(self):
        if self.parent():
            self.parent().setCurrentWidget(self.parent().parent().menu)
class GraphPuzzle(QWidget):
    def __init__(self, game_state: GameState, parent: QObject|None=None):
        super().__init__(parent)
        self.state = game_state
        self.parentwin = parent
        self.setWindowTitle("Bolical World")
        self.resize(800,600)
        self.setStyleSheet("background-color: black;")

        layout = QVBoxLayout(self)
        layout.setSpacing(6)

        # Title
        self.title = QLabel(f"Bolical World | LEVEL {'?'}")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: #00ff88; font-size: 18px; font-weight: bold;")
        layout.addWidget(self.title)

        # Hint
        hint = QLabel("Enter an equation f(x). Allowed: sin, cos, tan, abs, pi, e, sinh, cosh, tanh, sqrt, exp, ln, inverse trig/hyperbolic, erf, gamma")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet("color: #00aa66; font-size: 11px;")
        layout.addWidget(hint)

        # Input
        self.input = QLineEdit()
        self.input.setPlaceholderText("e.g. sin(x) + 0.5*cos(2*x)")
        self.input.setStyleSheet(stylesheet)
        layout.addWidget(self.input)

        # Canvas
        self.fig = Figure(facecolor="black")
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setFocusPolicy(Qt.StrongFocus)
        self.canvas.setFocus()
        layout.addWidget(self.canvas, 1)
        self.canvas.mpl_connect("scroll_event", self.on_scroll)
        self._press_event = None
        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("button_release_event", self.on_release)
        self.canvas.mpl_connect("motion_notify_event", self.on_motion)
        self.canvas.mpl_connect("key_press_event", self.on_key)
        self.ax = self.fig.add_subplot(111)
        self._style_axes()

        # Back/Skip buttons
        btn_layout = QHBoxLayout()
        back_btn = QPushButton("Back")
        skip_btn = QPushButton("Skip")
        back_btn.clicked.connect(self.go_back)
        skip_btn.clicked.connect(lambda: self.next_graph(skip=True))
        self.skip_btn = skip_btn
        btn_layout.addWidget(back_btn)
        btn_layout.addWidget(skip_btn)
        layout.addLayout(btn_layout)

        # Data
        self.points_per_level = {1:1,2:3,3:5,4:10,5:30,6:50,7:100,8:500,9:10000,10:1000000}
        self.x_sky = np.linspace(0, 100, 20000)
        self.x_norm = np.linspace(-10, 10, 20000)

        # Target
        #self.target_equation = equation
        #self.y_target = eval_expr(self.target_equation, self.x)
        #y_target = np.array(self.y_target, dtype=float)
        #y_target[~np.isfinite(y_target)] = np.nan
        #y_target = break_asymptotes(y_target)
        #self.y_target = y_target
        #self.target_line, = self.ax.plot(self.x, self.y_target,
        #                                 linestyle="--", linewidth=1.5,
        #                                 color="#007744", alpha=0.8)
        self.player_line, = self.ax.plot([],[], linewidth=2, color="#00ff88")
#
        self.canvas.draw()
        self.solved = False

        self.input.textChanged.connect(self.update_graph)
        
        self.next_button = QPushButton("Next Challenge")
        self.next_button.setStyleSheet(stylesheet)
        self.next_button.clicked.connect(lambda: self.next_graph(skip=False))
        self.next_button.hide()
        self.sky_lbl = QLabel()
        self.sky_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.sky_lbl)
        if self.state.mode == MODE_SKY_HIGH:
            self.sky_lbl.setText("Sky High Structuring | Max slope ≤ 1 | Reach y = 100 between x = 0 and 100")
        else:
            self.sky_lbl.hide()
        layout.addWidget(self.next_button)
    def _style_axes(self): 
        self.ax.set_facecolor("black") 
        self.ax.grid(True, color="#003322", linewidth=0.5) 
        for spine in self.ax.spines.values(): 
            spine.set_color("#006644") 
        self.ax.tick_params(colors="#00aa66") 
        if self.state.mode == MODE_SKY_HIGH:
            self.ax.set_xlim(0,100)
            self.ax.set_ylim(0,110)
        else:
            self.ax.set_xlim(-10,10) 
            self.ax.set_ylim(-20,20)
    def update_graph(self): 
        if self.solved: 
            return 
        self._style_axes()
        expr = self.input.text().strip() 
        if not expr: 
            self.player_line.set_data([],[]) 
            self.canvas.draw_idle() 
            return 
        try: 
          sanitized_expr = preprocess_for_eval(expr) 
          x = self.x_sky if self.state.mode == MODE_SKY_HIGH else self.x_norm
          y_player = eval_expr(sanitized_expr, x)
          y_player = np.array(y_player, dtype=float)
          y_player[~np.isfinite(y_player)] = np.nan
          y_player = break_asymptotes(y_player)
          
          self.player_line.set_data(x, y_player)

          if self.state.mode == MODE_SKY_HIGH:
             success, reason = sky_high_check(x, y_player)
             self.sky_lbl.setText(reason)
             if success:
                 self.on_success()
          elif check_match_numeric(self.target_equation, expr, self.x_norm): 
              self.on_success() 
          self.canvas.draw_idle() 
        except Exception: 
            pass
    # ----- NEW METHODS ADDED -----
    def go_back(self):
      if self.parent():
          if self.state.mode == MODE_SKY_HIGH:
              self.state.mode = MODE_NORMAL
              self.parent().setCurrentWidget(self.parent().parent().menu)
          else:
              self.parent().setCurrentWidget(self.parent().parent().difficulty_select)

    def next_graph(self, skip: bool=False):
        """Generate next graph. If skip=True, no points are awarded."""
        # Award points if not skipped and puzzle solved
        # Clear old UI state
        self.ax.cla()
        self._style_axes()
        self.solved = False
        self.input.setDisabled(False)
        self.input.clear()

        if hasattr(self, "success"):
              self.success.hide()
        if hasattr(self, "sky_lbl"):
            self.sky_lbl.hide()
        self.next_button.hide()
        if self.state.mode == MODE_SKY_HIGH:
            return
        # Generate new equation
        global equation
        equation = generate_level_equation(self.state.level)
        equation = preprocess_for_eval(equation)

        # Numeric evaluation
        self.target_equation = equation
        self.y_target = eval_expr(self.target_equation, self.x_norm)
        y_target = np.array(self.y_target, dtype=float)
        y_target[~np.isfinite(y_target)] = np.nan
        y_target = break_asymptotes(y_target)
        if not np.any(np.isfinite(y_target)):
            self.next_graph(skip=True)
            return
        if np.count_nonzero(np.isfinite(y_target)) < 10:
            self.next_graph(skip=True)
            return
        self.y_target = y_target
        self.target_line, = self.ax.plot(self.x_norm, self.y_target,
                                         linestyle="--", linewidth=1.5,
                                         color="#007744", alpha=0.8)
        self.player_line, = self.ax.plot([],[], linewidth=2, color="#00ff88")

        self.ax.relim()
        self.ax.autoscale_view()
        self.ax.set_autoscale_on(False)
        self.skip_btn.setDisabled(self.state.mode == MODE_SKY_HIGH)
        self.canvas.draw_idle()

    def on_success(self):
        """Call when player matches the equation."""
        self.solved = True
        self.input.setDisabled(True)
        self.player_line.set_color("#00ffaa")
        self.target_line.set_alpha(0.3)

        # Award points immediately
        if self.state.mode == MODE_NORMAL:
          self.state.points += self.points_per_level[self.state.level]
          self.success = QLabel(f"MATCH CONFIRMED! Points: {self.state.points}")
          self.success.setAlignment(Qt.AlignCenter)
          self.success.setStyleSheet("color: #00ffaa; font-size: 16px; font-weight: bold;")
          self.layout().addWidget(self.success)
          self.next_button.show()
          self.canvas.draw_idle()
        else:
          self.parentwin.data["Stats"]["Esadrhium"] = 1 if self.parentwin.data["Stats"]["Esadrhium"] < 1 else self.parentwin.data["Stats"]["Esadrhium"]
    def on_scroll(self, event): 
        if event.inaxes != self.ax: 
            return # Ignore scrolls outside the graph 
        base_scale = 1.2 
        ax = self.ax 
        cur_xlim = ax.get_xlim() 
        cur_ylim = ax.get_ylim() 
        xdata = event.xdata 
        ydata = event.ydata 
        if xdata is None or ydata is None: 
            return 
        scale_factor = 1 / base_scale if event.button == "up" else base_scale 
        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor 
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor 
        relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0]) 
        rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0]) 
        ax.set_xlim( xdata - new_width * (1 - relx), xdata + new_width * relx ) 
        ax.set_ylim( ydata - new_height * (1 - rely), ydata + new_height * rely ) 
        self.canvas.draw_idle() 
    def on_press(self, event): 
        if event.inaxes != self.ax: 
            return 
        self._press_event = event.xdata, event.ydata, self.ax.get_xlim(), self.ax.get_ylim() 
    def on_release(self, event): 
        self._press_event = None 
    def on_motion(self, event): 
        if self._press_event is None or event.inaxes != self.ax: 
            return 
        xpress, ypress, (x0, x1), (y0, y1) = self._press_event 
        dx = xpress - event.xdata 
        dy = ypress - event.ydata 
        self.ax.set_xlim(x0 + dx, x1 + dx) 
        self.ax.set_ylim(y0 + dy, y1 + dy) 
        self.canvas.draw_idle()
    def on_key(self, event): 
        if event.key == "enter" and self.solved: self.next_graph()
    def reset_sky_high(self):
      self.next_graph(True)
      self.solved = False
      self.input.setDisabled(False)
      self.input.clear()
  
      self.ax.cla()
      self._style_axes()
  
      self.title.setText("SKY HIGH STRUCTURING")
  
      self.sky_lbl.setText(
          "Goal: Reach y = 100\n"
          "Constraints:\n"
          "• Mustn't be overly steep a majority of the time (max = approx 50°)\n"
          "• 0 ≤ x ≤ 100\n"
          "• Must touch origin (0,0)\n"
          "• No skipping allowed\n"
          "• Solution requires level of creativity, cheap solutions are disallowed"
      )
      self.sky_lbl.show()
  
      self.next_button.hide()
  
      self.player_line, = self.ax.plot([], [], linewidth=2, color="#00ff88")
      self.skip_btn.setDisabled(True)
      self.canvas.draw_idle()

# ---------- RUN ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BolicalWorld(stat_data={"Stats": {"Graphite": 0, "Tesseract": 0, "Tetra": 0, "Master Tetra": 0}, "Keys": {"Bolical Points": 0, "Sky-High Structuring": False}})
    window.show()
    sys.exit(app.exec())
