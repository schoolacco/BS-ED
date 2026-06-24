from __future__ import annotations
import math
import copy
from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget, QScrollArea, QVBoxLayout, QHBoxLayout, QSizePolicy, QGridLayout, QLabel, QDialog, QFrame, QLineEdit, QLayout, QTextEdit, QListWidget, QTextBrowser, QStackedWidget, QApplication, QMessageBox
from PySide6.QtGui import QColor, QFont, QPainter, QFontMetrics, QPainterPath, QPen, QLinearGradient, QPalette, QCloseEvent, QPixmap, QShowEvent, QPaintEvent, QEnterEvent, QKeyEvent, QBrush
from PySide6.QtCore import Qt, QObject, QPointF, QTimer, Signal, QUrl, QRectF, QEvent, QThread, QRect
from PySide6.QtTest import QSignalSpy
import scipy.special as sci
import inspect
import os
import ctypes
import time
import colorama
from pathlib import Path
import random
import sys
import numpy as np
import re
from functools import partial
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor
import weakref
from typing import Callable, Any, Optional, Union
import bcrypt
from data import stat_gradients, def_stat_increment
import db
from dataclasses import dataclass, field
from session import validate_session, create_session
from Mantissa import Mantissa
from enum import Enum
Numeric = Union[int, float, Mantissa]
global_path_reference = Path(__file__).resolve().parent.parent
general_stylesheet = open(f"{global_path_reference}/Program/general.qss", "r")
general_stylesheet = general_stylesheet.read() 
cytherax_stylesheet = open(f"{global_path_reference}/Program/cytherax.qss", "r")
cytherax_stylesheet = cytherax_stylesheet.read()
# Source - https://stackoverflow.com/a
# Posted by luke, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-30, License - CC BY-SA 3.0
FILE_ATTRIBUTE_HIDDEN = 0x02
FILE_ATTRIBUTE_SYSTEM = 0x04
def darken(hex: str, factor: float=0.7) -> str:
    hex = hex.lstrip('#')
    
    # Convert hex to RGB
    rgb = [int(hex[i:i+2], 16) for i in (0, 2, 4)]
    
    darkened_rgb = [int(max(0, min(255, val * factor))) for val in rgb]
    
    # Format back to hex
    return "#%02x%02x%02x" % tuple(darkened_rgb)
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
def button_inspect(cmd: Callable, btn: QPushButton):
    '''Inspects the lambda commands to know if the button must be passed as an argument within the function'''
    signature = inspect.signature(cmd)
    params = len(signature.parameters)
    if params == 0:
        return cmd()
    else:
        return cmd(btn)
def find_key_path(nested_dict: dict, target_key_name: str, current_path: Optional[dict]=None) -> list:
    """
    Recursively searches for a specific key name in a nested dictionary
    and returns the full path of keys to that key's location.
    """
    if current_path is None:
        current_path = []

    for key, value in nested_dict.items():
        if key not in ["Multis", "Recipe"]:
          new_path = current_path + [key]
  
          if key == target_key_name:
              # The key name matches target. Return the path up to this point.
              return new_path
          
          elif isinstance(value, dict):
              # Recursively search in nested dictionaries
              found_path = find_key_path(value, target_key_name, new_path)
              if found_path:
                  return found_path
    
    # Key not found in this branch
    return None
def find_value_path(nested_dict: dict, target_value: Any, current_path: Optional[dict]=None) -> list:
    """
    Recursively searches for a specific value name in a nested dictionary
    and returns the full path of keys to that value's location.
    Definitely not directly copy and pasted from find_key_path
    """
    if current_path is None:
        current_path = []

    for key, value in nested_dict.items():
        new_path = current_path + [key]
        if isinstance(value, dict):
            # Recursively search in nested dictionaries
            found_path = find_value_path(value, target_value, new_path)
            if found_path:
                return found_path
        else:
            if nested_dict[key] == target_value:
                new_path = current_path + [key]
                return new_path
    
    # Key not found in this branch
    return None
def multi_func(functions: list[Callable], conditions: list[bool]):
    '''An extremely complex function that returns the results of multiple functions'''
    return tuple(function() if condition else None for function, condition in zip(functions, conditions))
class Realm:
  '''A realm containing a set of buttons and stat requirements for access.
  Parameters:
  parent       : Parent window in which the Realm is contained
  button_groups: The groups of buttons to be created
  requirement  : Amount required, may be a list to allow alternative requirements
  unit         : Unit for the requirement amount
  name         : The ID of the Realm for quick reference
  bg           : Background colour
  fg           : Foreground colour
  text_colour  : Text colour
  voltaic_radar: The voltaic_radar gamepass, only necessary for Voltaic Sector
  on_leave     : Function to be executed upon leaving, was made for the Greed puzzle, unimplemented'''
  instances = set()
  def __init__(self, parent: QMainWindow, button_groups: dict[str: list[tuple]], requirement: Numeric|list[Numeric]=0, unit: str|list[str]="Cash", name: str="Placeholder", bg: str="black", text_color: str="white", voltaic_radar: bool=False, on_leave: Optional[Callable]=None, *args, **kwargs) -> Realm:
      super().__init__(*args, **kwargs)
      self.parent = parent
      self.btn_groups = button_groups
      if isinstance(requirement, Numeric):
          requirement = [requirement]
      self.req = requirement
      if isinstance(unit, str):
          unit = [unit]
      self.unit = unit
      self.id = name
      self.bg = bg
      self.color = text_color
      self.voltaic = voltaic_radar
      self.instances.add(self)
  
  def create_scrollable_area(self) -> tuple[QWidget,QScrollArea,QWidget]:
    """
    Creates a scrollable area using PySide6.
    Returns: (outer_container: QWidget, scroll_area: QScrollArea, content_widget: QWidget)
    """

    # --- Outer container widget ---
    parent = self.parent #Defining arguments as I'm too lazy to add self to everything after the revamp of this class
    button_groups = self.btn_groups
    bg = self.bg
    text_color = self.color
    voltaic_radar = self.voltaic
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
    if self == self.get_instance_by_id("VS"):
        parent.voltaic_random = VoltaicRandomiser(enable_count=50, interval_ms=20000, voltaic_radar=voltaic_radar, always_texts=["Spawn (req: 0 Cash)","Recover Hall (req: 0 Cash)"])
        num = 10 if voltaic_radar else 100
        #if random.randint(1,num) != 1:
        #  del button_groups["Unknown"]
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
        for row_index, tuple_reference in enumerate(buttons, start=1):
            if len(tuple_reference) == 2:
                (text, command) = tuple_reference
                obj = Button(text, command, bg=bg, text_color=text_color)
            else:
                (text, command, type) = tuple_reference
                if type == "Label":
                  obj = QLabel(text)
                elif type.split(" ")[0] == "Hold":
                    obj = HoldButton(text, command, int(type.split(" ")[1]), bg=bg, text_color=text_color)
                elif type.split(" ")[0] == "Gluttony":
                    obj = Gluttony(text, int(type.split(" ")[1]))
            if isinstance(obj, QLabel):
              obj.setStyleSheet(
                  f"""
                  QLabel {{
                      background-color: {bg};
                      color: {text_color}
                  }}
                  """
              )
            grid.addWidget(obj, row_index, col_index, alignment=Qt.AlignTop)
            if len(tuple_reference) == 2:
              if not parent.voltaic_random:  
                continue
              index = len(parent.voltaic_random.buttons)
              parent.voltaic_random.buttons.append({"btn": obj, "command": command})
              if text in parent.voltaic_random.always_texts:
                parent.voltaic_random.always_indices.add(index)
    if parent.voltaic_random:
        parent.voltaic_random.start()
        #button_groups["Unknown"] = [Button("", lambda: blinded(parent))]
    return outer_container, scroll_area, content_widget
  @classmethod
  def get_instance_by_id(cls, id: str) -> Realm:
      instances = list(cls.instances)
      for item in instances:
          if item.id == id:
              return item
  @classmethod
  def load_realm(cls, stat_increment: dict, name: str) -> tuple[QWidget, QScrollArea, QWidget, dict]|bool:
    self = cls.get_instance_by_id(name)
    for unit, req in zip(self.unit, self.req):
      amount = stat_increment["Stats"][unit]
      req = Mantissa.float_to_mantissa(req) if isinstance(amount, Mantissa) else req
      if amount >= req:
        container, scroll_area, content = self.create_scrollable_area()
        return container, scroll_area, content, stat_increment
      else:
        return False
class World(Realm):
  weakref.WeakSet()
  instances = weakref.WeakSet()
  def __init__(self, parent: QMainWindow, initial_area: str, cash: str="Cash", multiplier: str="Multiplier", rebirths: str="Rebirths", gems: str="Gems", reset: str="Main Progression", world_name: str="Buttonia", event_power: str|bool=False, multi_logic: bool=True, upgrade_reference: str="", voltaic_radar: bool=False, requirement: Numeric|list[Numeric]=0, unit: str|list[str]="Cash", bg: str="black", text_color: str="white", *args, **kwargs):
      super().__init__(parent, requirement, unit, bg, text_color, voltaic_radar,  *args, **kwargs)
      self.area = initial_area
      self.cash = cash
      self.multi = multiplier
      self.rebirth = rebirths
      self.gem = gems
      self.e_power = event_power
      self.reset = reset
      self.name = world_name
      self.m_logic = multi_logic
      self.upgrade_ref = upgrade_reference
  def load_world(self) -> tuple[Realm,str,str,str,str,str|bool,str,bool,str,str,str]:
      path = f"{global_path_reference}/Program/Music/{self.name}" if Path(f"{global_path_reference}/Program/Music/{self.name}").exists() else f"{global_path_reference}/Program/Music/Buttonia"
      return Realm.get_instance_by_id(self.area), self.cash, self.multi, self.rebirth, self.gem, self.e_power, self.reset, self.m_logic, self.name, self.upgrade_ref, path
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
    def __init__(self, items: dict, cost: Mantissa|float|int, unit: str) -> Geode:
        """
        items: dict -> { "ItemName": rarity }
        rarity = 1/rarity
        cost: Mantissa or float, automatically converted unless exponent >= 300
        unit: key in save file
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
class VoltaicRandomiser:
    '''The single use gimmick that is only used in Voltaic Sector... why did I bother again?'''
    def __init__(self, enable_count: int=10, interval_ms: int=20000, voltaic_radar: bool=False, always_texts: Optional[list]=None) -> VoltaicRandomiser:
        self.enable_count = enable_count
        self.interval_ms = interval_ms
        self.buttons = []   
        self.timer = None
        self.radar = voltaic_radar
        self.always_texts = set(always_texts) if always_texts else set()
        self.always_indices = set() 

    def start(self):
        """Start periodic reshuffling"""
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
              btn.setEnabled(True)
              btn.clicked.disconnect()
              btn.clicked.connect(cmd)
    def shuffle(self):
      if not self.buttons:
          return
  
      indices = list(range(len(self.buttons)))
  
      # Everything except the always-enabled ones (i.e. the realm teleports)
      random_pool = [i for i in indices if i not in self.always_indices]
  
      # How many random buttons are allowed after always-enabled ones are included
      remaining = self.enable_count - len(self.always_indices)
      remaining = max(0, remaining)
  
      enable_set = set(self.always_indices)
  
      if remaining > 0:
        enable_set |= set(random.sample(random_pool, min(remaining, len(random_pool))))

  
      for i, item in enumerate(self.buttons):
          btn: Button = item["btn"] #I admittedly haven't checked if the logic still works with the new button classes, if not, oh well
          cmd = item["command"]
  
          if i in enable_set:
              btn._voltaic_disabled = False
              btn.setEnabled(True)
              btn.clicked.disconnect()
              btn.clicked.connect(cmd)
  
          else:
              btn._voltaic_disabled = True
              btn.setEnabled(False)
class Button(QPushButton):
    '''Custom button class, made for  subworld that was never going to be added here'''
    execution = False
    def __init__(self, text: str, function: Callable, death: bool=False, bg: str="black", text_color: str="white") -> Button:
        super().__init__(text)
        self.txt = text
        self.func = function 
        self.death = death
        self.text_colour = text_color
        self.hover = False
        self._voltaic_disabled = False
        self.clicked.connect(self.execute) 
        self.setStyleSheet(
                f"""
                QPushButton {{
                    padding: 6px;
                    border: 1px solid {text_color};
                }}
                """
            )
        try:
          #self.gradient = stat_gradients[(lambda b=[(re.sub(r'\)','', re.sub(r' \(Fetch\)', '', re.sub(r' \(Sets\)', '',item)))) for item in re.split(r'\s*[a-zA-Z]*\d+[a-zA-Z]*\s*', self.txt) if item]: b[len(b)-1])()]
          self.gradient = stat_gradients[self._parse_text()]
        except KeyError as e:
            self.gradient = None
            if "C0RR8PT10N" in re.sub(r'\)', '', re.sub(r'\(', '', self.text())).split(" "):
                self.gradient = stat_gradients["C0RR8PT10N"]
            else:
              for item in ["TRU3_W0RLD"]: #Exceptions for stat that explicitly have numbers within their names, more will be added as I think of them (never)
                if item in [text.strip(")") for text in self.text().split(" ")]:
                    self.gradient = stat_gradients[item]
        
            self.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {bg};
                    color: {text_color};
                    padding: 6px;
                    border: 1px solid {text_color};
                }}
                QPushButton::hover {{
                    background-color: #222
                }}
                """
            )
    def execute(self):
        '''Kill it'''
        if self.death and self.execution:
            self.destroy()
        else:
            func = lambda _, b=self, cmd=self.func: button_inspect(cmd, b)
            try:
              func(self)
            except TypeError:
                pass
    def enterEvent(self, event: QEnterEvent):
        self.hover = True
        self.update()
    def leaveEvent(self, event: QEvent):
        self.hover = False
        self.update()
    def _parse_text(self):
        def _match(text: str) -> str|None:
          stats = list(def_stat_increment["Stats"].keys())
          text = re.sub(r'^\s*\d+(?:\.\d+)?[A-Za-z]*\s*', "", text, 1).strip(' :()"\'').strip()
          p_stat = None
          for stat in stats:
              if text == stat or text.startswith(stat):
                  tail = text[len(stat):]
                  if tail == '' or tail[0] in ' (:.':
                      if p_stat is None or len(stat) > len(p_stat):
                          p_stat = stat
          return p_stat
        text = self.text()
        parsed_text = None
        if ":" in text:
            left, right = text.split(':', 1)
        else:
            left, right = text, ''
        right_str = _match(right) if right else None
        if right_str:
            parsed_text = right_str
        left_str = _match(left) if left else None
        if left_str:
            parsed_text = left_str
        return parsed_text
    def paintEvent(self, event: QPaintEvent):
        if not self._voltaic_disabled:
          if self.gradient:
            self.angle_deg = self.gradient["Angle"]
            self.colors = [darken(colour, 0.6) for colour in self.gradient["Colours"]]
            if self.isEnabled():
              if self.hover:
                  self.colors = [darken(colour, 0.9) for colour in self.colors]
            else:
              self.colors = [darken(colour, 0.5) for colour in self.colors]
            painter = QPainter(self)
            painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
            
            # Convert angle to radians (0 deg is left-to-right, 90 deg is top-to-bottom)
            angle = math.radians(self.angle_deg)
            cx = self.width() / 2
            cy = self.height() / 2
            
            length = math.sqrt(self.width()**2 + self.height()**2) / 2
            
            x1 = cx - math.cos(angle) * length
            y1 = cy - math.sin(angle) * length
            x2 = cx + math.cos(angle) * length
            y2 = cy + math.sin(angle) * length #Maths :D
        
            gradient = QLinearGradient(QPointF(x1, y1), QPointF(x2, y2))
            stops = len(self.colors)
            for i, col in enumerate(self.colors):
                gradient.setColorAt(i / (stops - 1), QColor(col))
            rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
            border_color = QColor(self.text_colour)   
            painter.setPen(QPen(border_color, 1))
            painter.setBrush(gradient)
            painter.drawRect(rect)
            
            painter.setPen(QPen(QColor(self.text_colour)))
            painter.setFont(self.font())
            painter.drawText(self.rect(), Qt.AlignCenter, self.text())
        
          else:
              super().paintEvent(event)
        else:
            painter = QPainter(self)
            painter.fillRect(self.rect(), "#000000")
            border_color = QColor(self.text_colour)  
            rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5) 
            painter.setPen(QPen(border_color, 1))
            painter.drawRect(rect)
class RotatedLabel(QLabel):
    '''Perhaps the most under-utilised class in my program'''
    def __init__(self, text: str="", angle: int=0, parent: Optional[QObject]=None) -> RotatedLabel:
        super().__init__(text, parent)
        self.angle = angle

    def paintEvent(self, event: QPaintEvent):
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

    def walk(tree):
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
    keys = []
    for cat, item in stat_info.items():
      if cat not in ("Geode", "Afterlife Domain (Geode)"):
        for key in item.keys():
            keys.append(key)
      else:
        for g_cat, g_item in item.items():
            for key in g_item.keys():
              keys.append(key)
    for item in list(set(meta_data.keys()) ^ set(keys)):
        index[item.lower()] = {
            "name": item,
            "tags": [t.lower() for t in meta_data.get(stat, {}).get("tags", [])],
            "has_meta": True
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

    # 2. Partial name or tag matching
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
class BootScreen(QDialog):
    finished = Signal()
    closed = Signal() #I don't even know if this is necessary anymore

    def __init__(self, parent: Optional[QObject]=None) -> BootScreen:
        super().__init__(parent, Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self.spy = QSignalSpy(self.finished)
        self.setStyleSheet("background-color: black;")
        self.setWindowTitle("Loading...")
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        self.showFullScreen()

        self.title = RotatedLabel("CYTHERAX-47", angle=20)
        self.title.setFont(QFont("Consolas", 64, QFont.Bold))
        self.title.setStyleSheet("color: #00ff00;")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFixedSize(800, 400)
        
        
        layout.addStretch()
        layout.addWidget(self.title)
        layout.addStretch()

        self.bar_container = QHBoxLayout()
        self.bar_container.setSpacing(8)
        self.bar_container.setAlignment(Qt.AlignCenter)

        self.chunks = []
        self.chunk_count = 16

        for _ in range(self.chunk_count):
            chunk = QFrame()
            chunk.setFixedSize(40, 40)
            chunk.setStyleSheet("""
                QFrame {
                    background-color: #002200;
                    border: 1px solid #005500;
                }
            """)
            self.chunks.append(chunk)
            self.bar_container.addWidget(chunk)

        layout.addLayout(self.bar_container)

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
            try:
              self.timer.stop()
              QTimer.singleShot(300, self.finish)
            except RuntimeError:
                pass

    def finish(self):
        self.finished.emit()
        self.close()
    def closeEvent(self, event: QCloseEvent):
        if self.spy.count() < 1 and self.parent():
            self.parent().show()
            self.parent().showNormal()
            self.closed.emit()
        self.timer.stop()
        self.timer.deleteLater()
        event.accept()
        return None
class CY47Window(QDialog):
    '''Super cool database interface...
    In the original game CY47 was an entire OS system
    No elaboration needed there'''
    def __init__(self, stat_info: dict, meta_data: dict, stat_list: list, stat_gradients: dict, parent: Optional[QObject]=None, whitelist: Optional[list[str]]=None, blacklist: Optional[list[str]]=None) -> CY47Window:
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("CY-47 :: SYSTEM INTERFACE")
        self.showMaximized()
        self.stat_info = stat_info
        self.meta_data = meta_data
        self.stat_list = stat_list
        self.gradients = stat_gradients
        self.wl = whitelist
        self.bl = blacklist
        self.index = build_cythrex_index(self.stat_info, self.meta_data)
        self.root = QVBoxLayout(self)
        self.root.setSpacing(8)
        self.setStyleSheet(cytherax_stylesheet)

        header = QHBoxLayout()

        title = QLabel("Cythrex-47")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search database…")
        self.search.returnPressed.connect(self.on_search)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.search, 2)

        self.root.addLayout(header)
        
        self.page_container = QVBoxLayout()
        self.root.addLayout(self.page_container)
        
        self.current_page = None
        self.show_default_page()
        self.image = None
    def _clear_layout(self, layout: QLayout):
      while layout.count():
          item = layout.takeAt(0)
  
          widget = item.widget()
          child_layout = item.layout()
  
          if widget is not None:
              widget.setParent(None)
              widget.deleteLater()
  
          elif child_layout is not None:
              self._clear_layout(child_layout)
    @staticmethod
    def _parse_text(text: str) -> str:
        pattern = r"\{(.*?)\|(.*?)\}"
        
        def repl(match):
            command = match.group(1)
            text = match.group(2)
            return f'<a href="{command}" style="color:#00ff00; text-decoration:none;">{text}</a>'
        html = re.sub(pattern, repl, text)
        html = html.replace("<h1>", '<div style="font-size:24px; font-weight:bold;"><br>').replace("</h1>", "</div>") #Fixing weird scaling issues
        return f"""
        <div style="font-family: Consolas; font-size: 14px;">
        {html}
        </div>
        """
    def handle_link(self, url: QUrl):
        command = url.toString() #List of special commands
        if command.startswith("stat:"):
            stat = command.split(":", 1)[1]
            self.generate_content(stat)
        elif command == "back":
            self.show_default_page()
        elif command.startswith("search:"):
            query = command.split(":", 1)[1]
            self.search.setText(query)
            self.on_search()
        elif command.startswith("link:"):
            page = command.split(":", 1)[1]
            self.build_page(self.meta_data[page]["raw_text"])
        elif command.startswith("exec:"):
            command = command.split(":", 1)[1]
            exec(command)
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
  
      subtitle = QLabel(
          "Awaiting query...\n\n"
          "• Search for a stat by name\n"
          "• Use tags to discover related entries\n"
          "• CY-47 © AIHA Corp."
      )
      subtitle.setAlignment(Qt.AlignCenter)
  
      layout.addStretch()
      layout.addWidget(title)
      layout.addSpacing(10)
      layout.addWidget(subtitle)
      layout.addStretch()
  
      self.page_container.addLayout(layout)
      self.current_page = layout
    def generate_content(self, stat: str):
        # Main info panel
        if stat not in self.meta_data:
          self.show_default_page()
          return

        self.clear_page()
        self.content = QHBoxLayout()
        self.right_panel = QVBoxLayout()

        # Stat name with gradient
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

        self.lore = QTextEdit()
        self.lore.setReadOnly(True)
        self.lore.setText(self.meta_data[stat]["lore"])

        left_info.addWidget(self.stat_type)
        left_info.addWidget(self.lore)

        mid_row.addLayout(left_info, 3)

        # Centre image
        self.image = QLabel(self)
        image = self.gradients.get(stat, self.gradients["Default"]).get("File", None)
        if image == None:
          files = [f for f in os.listdir(f"{global_path_reference}/Program/Stats") if os.path.isfile(os.path.join(f"{global_path_reference}/Program/Stats", f))]
          if f"{stat}.webp" in files:
            self.image.setPixmap(QPixmap(f"{global_path_reference}/Program/Stats/{stat}.webp"). scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
          else:
            self.image.setPixmap(QPixmap(f"{global_path_reference}/Program/Stats/Missing.webp"). scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.image.setPixmap(QPixmap(f"{global_path_reference}/Program/Stats/{image}.webp"). scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.image.setFixedSize(500,500)
        self.image.setFrameShape(QFrame.Box)
        self.image.setAlignment(Qt.AlignCenter)
        self.image.setStyleSheet('''QLabel {background-color: black;}''')
        mid_row.addWidget(self.image, 2)

        self.right_panel.addLayout(mid_row)

        # Obtainment
        self.obtainment = QFrame()
        self.obtainment.setFrameShape(QFrame.StyledPanel)
        self.obtainment_layout = QVBoxLayout(self.obtainment)

        self.obtainment_label = QTextEdit()
        self.obtainment_label.setReadOnly(True)
        self.obtainment_label.setText(self.meta_data[stat]["obtainment"])

        self.obtainment_layout.addWidget(self.obtainment_label)

        self.right_panel.addWidget(self.obtainment)
        
        self.left_panel = QVBoxLayout()
        
        # Multipliers
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
        self.multiplier_header = QLabel("Stat Multipliers:")
        self.content.addLayout(self.right_panel, 1)
        
        self.left_panel.addWidget(self.multiplier_header, 1)
        
        self.left_panel.addWidget(self.multiplier_list, 20)
        
        self.content.addLayout(self.left_panel, 1)
        
        self.page_container.addLayout(self.content)
        self.current_page = self.content    
    def build_page(self, text: str):
      #Text pages
      self.clear_page()
      
      layout = QVBoxLayout()
      layout.setAlignment(Qt.AlignCenter)
      
      parsed_text = self._parse_text(text)
  
      content = QTextBrowser()
      content.setHtml(parsed_text)
  
      content.setOpenExternalLinks(False)
      content.setOpenLinks(False)
      content.anchorClicked.connect(self.handle_link)
      content.viewport().setCursor(Qt.ArrowCursor)
  
      layout.addWidget(content)
  
      self.page_container.addLayout(layout)
      self.current_page = layout
    def show_no_results_page(self, query: str):
        self.clear_page()
    
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
    
        title = QLabel("NO MATCHING ENTRIES FOUND")
        title.setFont(QFont("Consolas", 18, QFont.Bold))
        title.setStyleSheet("color: red;")
    
        subtitle = QLabel(f"Query: \"{query}\"")
        subtitle.setFont(QFont("Consolas", 10))
    
        hint = QLabel("Refine query or search by known designation.")
    
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
      if self.wl:
          results = [result for result in results if result in self.wl]
      if self.bl:
          results = [result for result in results if result not in self.bl]
      if results:
          if len(results) == 1 and results[0].lower() == query.lower():
              func = lambda r=results[0]: self.generate_content(r) if "Stats" in self.meta_data[r]["tags"] else self.build_page(self.meta_data[r]["raw_text"])
              func()
          else:
              self.show_results_page(results, query)

      else:
          self.show_no_results_page(query)
    def show_results_page(self, results: list, query: str):
      self.clear_page()
  
      outer = QVBoxLayout()
  
      header = QLabel(f'SEARCH RESULTS FOR: "{query}"')
      header.setFont(QFont("Consolas", 14, QFont.Bold))
      
      count = QLabel(f"{len(results)} ENTR{'Y' if len(results) == 1 else 'IES'} FOUND")
      count.setFont(QFont("Consolas", 10))
      
      outer.addWidget(header)
      outer.addWidget(count)
  
      scroll = QScrollArea()
      scroll.setWidgetResizable(True)
  
      container = QWidget()
      layout = QVBoxLayout(container)
  
      for result in results:
          btn = QPushButton()
          btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
          btn.setMinimumHeight(40)
          
          label = QLabel(result)
          label.setWordWrap(True)
          label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
          
          layout_inner = QHBoxLayout(btn)
          layout_inner.setContentsMargins(8, 4, 8, 4)
          layout_inner.addWidget(label)
  
          btn.clicked.connect(lambda _, r=result: self.generate_content(r) if "Stats" in self.meta_data[r]["tags"] else self.build_page(self.meta_data[r]["raw_text"]))
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
        self.parent().show()
        self.parent().showNormal()
        event.accept()
        
#Graphite puzzle, that actually has to do with graphs
np.seterr(all="ignore")
stylesheet = open(f"{global_path_reference}/Program/graphite.qss", "r")
stylesheet = stylesheet.read()
#GUI
class GameState: #This could be a data class... yeah I'm too lazy for that
    def __init__(self, mode: GraphPuzzle.Mode=0):
        self.points = 0
        self.level = 1
        self.unlocks = {"sky_high": False}
        self.mode = mode
class BolicalWorld(QDialog):
        '''
        Far better than the original, not even a comparison
        '''
        def __init__(self, stat_data: dict, parent: Optional[QObject]=None, game_state: Optional[GameState]=None) -> BolicalWorld:
            super().__init__(parent)
            if parent:
              self.parent().hide()
              for child in self.parent().children():
                if isinstance(child, (QDialog, QMainWindow)) and child != self:
                    child.hide()
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
            
            for page in [self.menu, self.guide, self.shop, self.difficulty_select, self.graph]: #Optimisation?
                self.stack.addWidget(page)
            self.stack.setCurrentWidget(self.menu)
        def create_menu(self) -> QWidget:
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
        def create_guide(self) -> QWidget:
            page = QWidget()
            layout = QVBoxLayout(page)
            
            guide = QLabel("Goal: Guess the equation of the graph. Use sin, cos, tan, etc.\nYou earn points by matching the target equation. Difficulty increases points although graphs will become exponentially harder.\nLevel 1 graphs give you 1 point\nLevel 2 graphs give you 3 points\nLevel 3 graphs give you 5 points\nLevel 4 graphs give you 10 points\nLevel 5 graphs give you 30 points\nLevel 6 graphs give you 50 points\nLevel 7 graphs give you 100 points\nLevel 8 graphs give you 500 points\nLevel 9 graphs give you 10,000 points and are not recommended\nLevel 10 graphs give you 1,000,000 points but are nearly imposssible to crack.\nAll graphs will display values within the domain: x ∈ [-50,50]")
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
            self.state.mode = GraphPuzzle.Mode.MODE_SKY_HIGH
            self.graph.reset_sky_high()
            self.stack.setCurrentWidget(self.graph)
        def open_shop(self):
            self.shop.points_label.setText(f"Points: {self.state.points}")
            self.stack.setCurrentWidget(self.shop)
        def closeEvent(self, event: QCloseEvent):
            self.data["Keys"]["Bolical Points"] = self.state.points
            if self.parent():
              self.parent().show()
            event.accept()
class ShopPage(QWidget):
    def __init__(self, game_state: GameState, parent: Optional[QObject]=None) -> ShopPage:
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
    '''
    A puzzle game where you have to guess the graph!
    Totally not overcomplicated at all!
    Parameters
    ---------------
    game_state: GameState, the game state, I have nothing else to tell you
    parent    : Optional[QObject], the parent window, again, no elaboration is really needed
    '''
    TOLERANCE = 0.01  # Allowed error for match check
    class Mode(Enum):
        MODE_NORMAL = 0
        MODE_SKY_HIGH = 1
    SAFE_ENV = {
    "sin": np.sin, "cos": np.cos, "tan": np.tan,
    "abs": np.abs, "pi": np.pi,
    "sinh": np.sinh, "cosh": np.cosh, "tanh": np.tanh,
    "e": np.e, "sqrt": np.sqrt, "exp": np.exp, "ln": np.log,
    "arcsin": np.arcsin, "arccos": np.arccos, "arctan": np.arctan,
    "arcsinh": np.arcsinh, "arccosh": np.arccosh, "arctanh": np.arctanh,
    "erf": sci.erf, "gamma": sci.gamma
    }
    LINEAR_FUNCS = ["linear"]
    POLYNOMIAL_FUNCS = ["quadratic","cubic","quartic"]
    HYPERBOLAS = ["1/x","1/x^2","1/(x+a)^2"]
    TRIG_FUNCS = ["sin","cos","tan"]
    HYPERBOLIC_FUNCS = ["sinh","cosh","tanh"]
    OTHER_FUNCS = ["abs","sqrt","exp", "ln", "arcsin", "arccos", "arctan", "arcsinh", "arccosh", "arctanh", "erf", "gamma"]

    def __init__(self, game_state: GameState, parent: Optional[QObject]=None) -> GraphPuzzle:
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
        self.cursor = Cursor(self.ax, useblit=True, color="#00ff88", linewidth=1)
        self.coord_label = QLabel("x: 0.00 | y: 0.00")
        self.coord_label.setStyleSheet("""
            QLabel {
                color: #00ff88;
                background-color: #001100;
                border: 1px solid #00aa66;
                padding: 4px;
                font-family: Consolas;
            }
        """)
        
        layout.addWidget(self.coord_label)
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
        self.x_norm = np.linspace(-50, 50, 20000)
        self.player_line, = self.ax.plot([],[], linewidth=2, color="#00ff88")
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
        if self.state.mode == self.Mode.MODE_SKY_HIGH:
            self.sky_lbl.setText("Sky High Structuring | Max slope ≤ 1 | Reach y = 100 between x = 0 and 100")
        else:
            self.sky_lbl.hide()
        layout.addWidget(self.next_button)
    #Utility functions
    def _preprocess_for_eval(self, expr: str) -> str:
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
    def _break_asymptotes(self, y: np.ndarray[np.float64], threshold: int=10):
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
    # What is/isn't allowed
    def _eval_expr(self, expr: str, x: np.ndarray[np.float64]) -> Any:
        expr = self._preprocess_for_eval(expr)
        env = self.SAFE_ENV.copy()
        env["x"] = x
        return eval(expr, {"__builtins__": {}}, env)
    def _style_axes(self): 
        self.ax.set_facecolor("black") 
        self.ax.grid(True, color="#003322", linewidth=0.5) 
        for spine in self.ax.spines.values(): 
            spine.set_color("#006644") 
        self.ax.tick_params(colors="#00aa66") 
        if self.state.mode == self.Mode.MODE_SKY_HIGH:
            self.ax.set_xlim(0,100)
            self.ax.set_ylim(0,110)
        else:
            self.ax.set_xlim(-10,10) 
            self.ax.set_ylim(-10,10)
    def _generate_level_equation(self, level: int, bonus: bool=False) -> str:
      """
      Generates an equation according to the rules for levels 1-10.
      If bonus=True, derivative/integral mode (not implemented).
      """
      terms = []
  
      if level == 1:
          # Linear only
          return self._generate_linear()
      elif level == 2:
          # Quadratics–quartics
          return self._generate_polynomial()
      elif level == 3:
          # Hyperbolas, can chain but no addition
          return self._generate_hyperbola(chain=True)
      elif level == 4:
          # Trig & hyperbolic trig, addition allowed, no chaining
          for _ in range(random.randint(2,4)):
              terms.append(random.choice([self._generate_trig, self._generate_hyper_trig])(chained=False))
          return " + ".join(terms)
      elif level == 5:
          # Linear + trig/hyperbolic trig, addition + chaining allowed
          linear = self._generate_linear()
          trig_term = random.choice([self._generate_trig, self._generate_hyper_trig])(chained=True)
          return f"{linear} + {trig_term}"
      elif level == 6:
          # Trig/hyperbolic + powers + hyperbolas, chaining allowed, no linear or addition
          choices = [lambda: self._generate_trig(chained=True), lambda: self._generate_hyper_trig(chained=True), lambda: self._generate_hyperbola(chain=True)]
          return random.choice(choices)()
      elif level == 7:
          # Chaining of all prior content, no addition
          equation = ""
          while len(equation) < 20:
            choices = [lambda: self._generate_trig(chained=True),
                       lambda: self._generate_hyper_trig(chained=True)]
            equation =  random.choice(choices)()
          return equation
      elif level == 8:
          # Level 7 + other functions, chaining allowed
          equation = ""
          while len(equation) < 20:
            choices = [lambda: self._generate_other_func(chained=True)]
            equation =  random.choice(choices)()
          return equation
      elif level == 9:
          # Addition of functions, no chaining
          for _ in range(random.randint(4,8)):
              choices = [self._generate_linear, self._generate_polynomial,
                         lambda: self._generate_trig(chained=False),
                         lambda: self._generate_hyper_trig(chained=False),
                         self._generate_hyperbola, lambda: self._generate_other_func(chained=False)]
              terms.append(random.choice(choices)())
          return " + ".join(terms)
      elif level == 10:
          # Addition of chained + unchained functions
          for _ in range(random.randint(8,15)):
              choices = [self._generate_linear, self._generate_polynomial, self._generate_hyperbola,
                         lambda: self._generate_trig(chained=True),
                         lambda: self._generate_hyper_trig(chained=True),
                         lambda: self._generate_other_func(chained=True)]
              terms.append(random.choice(choices)())
          return " + ".join(terms)
      else:
          return self._generate_linear()  # fallback
    def _random_constant(self, low: int=-5, high: int=5, allow_float: bool=True) -> float:
        constant = 0
        while constant == 0:
          constant =  round(random.uniform(low, high), 1) if allow_float else random.randint(low, high)
        return constant    
    def _generate_linear(self) -> str:
        a = random.randint(-10,10)
        b = random.randint(-10,10)
        return f"{a}*x + {b}" 
    def _generate_polynomial(self) -> str:
        degree = random.randint(2,4)
        factors = [f"(x - {random.randint(-5,5)})" for _ in range(degree)]
        a = random.choice([-3,-2,-1,1,2,3])
        return f"{a}*{'*'.join(factors)}"
    def _generate_hyperbola(self, chain: bool=True) -> str:
        eq = "x"
        for _ in range(random.randint(1,2) if chain else 1):
            shift = random.choice([-1,1,2])
            power = random.choice([1,2])
            eq = f"1/({eq}+{shift})**{power}"
        return eq
    def _generate_trig(self, chained: bool=False) -> str:
        func = random.choice(self.TRIG_FUNCS)
        a = random.choice([-2,-1,1,2])
        freq = random.randint(1,3)
        shift = random.choice([-2,-1,1,2])
        inner = "x"
        if chained:
            inner = f"{random.choice([lambda: f'x**{random.randint(2,4)}', lambda: self._generate_hyperbola(chain=True), lambda: self._generate_trig(chained=True)])()}"  # can chain with simple expressions
        return f"{a}*{func}({freq}*{inner} + {shift})"
    def _generate_hyper_trig(self, chained: bool=False) -> str:
        func = random.choice(self.HYPERBOLIC_FUNCS)
        a = self._random_constant(-2,2)
        freq = self._random_constant(1,3)
        shift = self._random_constant(-2,2)
        inner = "x"
        if chained:
            inner = f"{random.choice([lambda: f'x**{random.randint(2,4)}',lambda: f'x{random.randint(-10,10)}', lambda: self._generate_trig(chained=True), lambda: self._generate_hyper_trig(chained=True), lambda: self._generate_hyperbola(chain=True)])()}"
        return f"{a}*{func}({freq}*{inner} + {shift})"
    def _generate_other_func(self, chained: bool=False) -> str:
        func = random.choice(self.OTHER_FUNCS)
        a = self._random_constant(-2,2)
        inside = f"x + {self._random_constant(-2,2)}"
        if chained:
            inside = f"{random.choice([lambda:self._generate_trig(chained=True), lambda:self._generate_hyper_trig(chained=True), lambda: f'x**{random.randint(2,10)}', lambda: self._generate_hyperbola(chain=True), lambda:self._generate_other_func(chained=True)])()}"
        return f"{a}*{func}({inside})"
    # Check if a majority of points line up
    def _check_match_numeric(self, target_expr: str, player_expr: str, x: np.ndarray[np.float64], tol: float=TOLERANCE) -> bool:
        try:
            y_target = np.array(self._eval_expr(target_expr, x), dtype=float)
            y_player = np.array(self._eval_expr(player_expr, x), dtype=float)
            y_target[~np.isfinite(y_target)] = np.nan
            y_player[~np.isfinite(y_player)] = np.nan
            error = np.nanmean(np.abs(y_target - y_player))
            return error < tol
        except Exception:
            return False
    #(15/100^0.4) * x^0.4 + 0.85x
    #Sky high structuring rule checks
    def _max_gradient_percentile(self, x: np.ndarray[np.float64], y: np.ndarray[np.float64], percentile: int=95, xmin: int=0, xmax: int=100) -> float:
        mask = (x >= xmin) & (x <= xmax) & np.isfinite(y)
        if np.count_nonzero(mask) < 2:
            return np.inf
    
        dy_dx = np.gradient(y[mask], x[mask])
        slopes = np.abs(dy_dx)
    
        return np.nanpercentile(slopes, percentile)
    def _reaches_height(self, x: np.ndarray[np.float64], y: np.ndarray[np.float64], target: int=100, xmin: int=0, xmax: int=100) -> bool:
        mask = (x >= xmin) & (x <= xmax) & np.isfinite(y)
        if not Any(mask):
            return False
        return np.nanmax(y[mask]) >= target
    def _is_trivial(self, x: np.ndarray[np.float64], y: np.ndarray[np.float64], tol: float=1e-3) -> bool:
        finite = np.isfinite(y)
        if np.count_nonzero(finite) < 3:
            return False
    
        dx = np.diff(x[finite])
        dy = np.diff(y[finite])
    
        slopes = dy / dx
        return np.all(np.abs(slopes - 1) < tol)
    def _sky_high_check(self, x: np.ndarray[np.float64], y: np.ndarray[np.float64], expr: str) -> tuple[bool, str]:
        if not Any(np.isfinite(y)):
            return False, "Graph is empty"
        
        if self._is_trivial_linear(x, y):
            return False, "Trivial linear solution (y = x) is not allowed"
        
        if self._max_gradient_percentile(x, y) > 1.01:
            return False, "Gradient exceeded maximum angle (approx 45°)"
    
        if not self._reaches_height(x, y):
            return False, "Did not reach y = 100"
        if len(expr) <= 12 or re.search(r"1\*", expr):
            return False, "Trivial solutions are not allowed"
        # Must touch origin
        idx = np.argmin(np.abs(x - 0))
        y_at_zero = y[idx]
        
        if not np.isfinite(y_at_zero) or abs(y_at_zero) > 1e-2:
            return False, "Graph must pass through the origin (0, 0)"
    
        return True, "Sky High Structuring complete, perhaps you are worthy of Esadrhium."
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
          sanitized_expr = self._preprocess_for_eval(expr) 
          x = self.x_sky if self.state.mode == self.Mode.MODE_SKY_HIGH else self.x_norm
          y_player = self._eval_expr(sanitized_expr, x)
          y_player = np.array(y_player, dtype=float)
          y_player[~np.isfinite(y_player)] = np.nan
          y_player = self._break_asymptotes(y_player)
          
          self.player_line.set_data(x, y_player)

          if self.state.mode == self.Mode.MODE_SKY_HIGH:
             success, reason = self._sky_high_check(x, y_player, expr)
             self.sky_lbl.setText(reason)
             if success:
                 self.on_success()
          elif self._check_match_numeric(self.target_equation, expr, self.x_norm): 
              self.on_success() 
          self.canvas.draw_idle() 
        except Exception: 
            pass
    def go_back(self):
      if self.parent():
          if self.state.mode == self.Mode.MODE_SKY_HIGH:
              self.state.mode = self.Mode.MODE_NORMAL
              self.parent().setCurrentWidget(self.parent().parent().menu)
          else:
              self.parent().setCurrentWidget(self.parent().parent().difficulty_select)
    def next_graph(self, skip: bool=False):
        """Generate next graph. If skip=True, no points are awarded"""
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
        if self.state.mode == self.Mode.MODE_SKY_HIGH:
            return
        # Generate new equation
        global equation
        equation = self._generate_level_equation(self.state.level)
        equation = self._preprocess_for_eval(equation)

        # Numeric evaluation
        self.target_equation = equation
        self.y_target = self._eval_expr(self.target_equation, self.x_norm)
        y_target = np.array(self.y_target, dtype=float)
        y_target[~np.isfinite(y_target)] = np.nan
        y_target = self._break_asymptotes(y_target)
        if not Any(np.isfinite(y_target)):
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
        self.skip_btn.setDisabled(self.state.mode == self.Mode.MODE_SKY_HIGH)
        self.canvas.draw_idle()

    def on_success(self):
        if self.state.mode != self.Mode.MODE_SKY_HIGH:
            self.state.mode = self.Mode.MODE_NORMAL
        self.solved = True
        self.input.setDisabled(True)
        self.player_line.set_color("#00ffaa")
        self.target_line.set_alpha(0.3)

        # Award points immediately)
        print(self.Mode.MODE_NORMAL == self.state.mode)
        if self.state.mode == self.Mode.MODE_NORMAL:
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
        if event.xdata is not None and event.ydata is not None:
            self.coord_label.setText(
                f"x: {event.xdata:.4f} | y: {event.ydata:.4f}"
            )
        else:
            self.coord_label.setText("Outside graph")
            return
    
        if self._press_event is None:
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
    def closeEvent(self, event: QCloseEvent):
        self.parentwin.close()
        event.accept()
class BadgesWindow(QDialog): 
 instances = weakref.WeakSet()
 def __init__(self, badge_data: dict, gradients: dict, stat_increment: dict, progress: int, parent: Optional[QObject]=None) -> BadgesWindow:
     super().__init__(parent)
     for instance in self.instances:
            instance.close()
     self.instances.clear()
     self.instances.add(self)
     self.gradients = gradients
     self.data = badge_data
     self.setMinimumSize(750,750)
     self.setMaximumSize(750,750)
     self.setStyleSheet(general_stylesheet)
     self.setWindowTitle("World Badges")
     self.labels_reference = {}
     self.increment = stat_increment
     self.progress = progress
     container_layout = QHBoxLayout(self)
     container = QWidget()
     scroll = QScrollArea()
     scroll.setWidgetResizable(True)
     scroll.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
     scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
     central_layout = QHBoxLayout(container)
     layout = QVBoxLayout()
     for cat in self.data.keys():
         if ((self.progress < 5 or self.progress >= 7) and cat == "Pre-existence") or (self.progress >= 5 and cat != "Pre-existence"):
           category_label = QLabel(cat)
           category_label.setStyleSheet("""QLabel {background-color: #1e1e1e; font-weight: bold; font-size: 20px;}""")
           layout.addWidget(category_label)
           for id in self.data[cat].keys():
               ref = self.data[cat][id]
               text = f"{ref['Display']}: {'Owned' if stat_increment["Badges"][id] else 'Not Owned'}"
               button = QPushButton()
               button.clicked.connect(lambda checked, c=cat, i=id: self.multi_edit(c, i))
               button.setStyleSheet("""QPushButton {background-color: #1e1e1e;
                                    border: none;}""")
               button.setFocusPolicy(Qt.NoFocus)
               gradient = copy.deepcopy(self.gradients[ref["Gradient"]])
               gradient["Colours"] = [darken(colour, 0.5) for colour in gradient["Colours"]] if not stat_increment["Badges"][id] else gradient["Colours"]
               label = GradientLabel(text, gradient["Colours"], gradient["Angle"], parent=button)
               gradient = None
               layout.addWidget(button)
               self.labels_reference[id] = label
     multi_layout = QVBoxLayout()
     self.multiplier_list = QListWidget()
     self.multiplier_list.setFixedWidth(150)
     self.multiplier_list.setStyleSheet(general_stylesheet)
     multiplier_header = QLabel("Stat Multipliers:")
     multiplier_header.setStyleSheet("""QLabel {background-color: #1e1e1e; font-weight: bold; font-size: 16px;}""")
     multi_layout.addWidget(multiplier_header, 1)
     multi_layout.addWidget(self.multiplier_list, 20)
     central_layout.addLayout(layout)
     container.setLayout(central_layout)
     scroll.setWidget(container)
     container_layout.addWidget(scroll, 4)
     container_layout.addLayout(multi_layout, 1)
     self.setLayout(container_layout)
 def multi_edit(self, category: str, badge: str):
     self.multiplier_list.clear()
     if self.data[category][badge]["Multis"]:
       for Stat, multi in self.data[category][badge]["Multis"].items():
           if Stat and multi:
             self.multiplier_list.addItem(f"{Stat} x{multi if not isinstance(multi, Mantissa) else multi.to_string()}")
     else:
         self.multiplier_list.addItem("Nothing")
 def update_badges(self):
    for id, lbl in self.labels_reference.items():
        name = lbl.text().split(":")[0]
        lbl.setText(f"{name}: {'Owned' if self.increment["Badges"][id] else 'Not Owned'}")        
class CollapsibleSection(QWidget):
    '''
    A Collapsible Widget
    It can collapse to save space...
    '''
    def __init__(self, title: str, build_callback: Callable) -> CollapsibleSection:
        super().__init__()
        self.built = False
        self.build_callback = build_callback

        self.layout = QVBoxLayout(self)

        self.button = QPushButton(title)
        self.button.setCheckable(True)
        self.button.setStyleSheet("text-align: left; font-weight: bold; font-size: 18px; border: none;")

        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setAlignment(Qt.AlignTop)
        self.content.setVisible(False)

        self.button.clicked.connect(self.toggle)

        self.layout.addWidget(self.button)
        self.layout.addWidget(self.content)

    def toggle(self):
        if not self.built:
            self.build_callback(self.content_layout)
            self.built = True

        self.content.setVisible(self.button.isChecked())
class HoldButton(Button):
    '''A Hold Button, probably could've been used for the cost buttons, but I'm far too lazy to change the logic
    Does NOT constantly trigger function, only triggers on release'''
    def __init__(self, text: str, hold_time: int, command: Callable, parent: Optional[QObject]=None, bg: str="black", text_color: str="white") -> HoldButton:
        super().__init__(text, parent, bg, text_color)
        self.time = hold_time
        self.cmd = command
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self._force_release)
        self.pressed.connect(self._on_press)
        self.released.connect(self._on_release)
    def _force_release(self):
        self.setDown(False)
        self.cmd()
    def _on_press(self):
        self.timer.start(self.time)
    def _on_release(self):
        if self.timer.isActive():
            self.timer.stop()
class Gluttony(HoldButton):
    '''Special variant for the Gluttony puzzle'''
    def __init__(self, texts: list[str], hold_time: int, parent: Optional[QObject]=None) -> Gluttony:
        self.txts = texts
        text = texts[0]
        self.increment = 0
        super().__init__(text, hold_time, parent)
    def _force_release(self):
        self.setDown(False)
        self.setText((lambda n=self.text()[::-1].split(" ", 2): f"{n[2][::-1]} {int(n[1][::-1])-1} HP")()) #Does this look overly complicated? This is what over optimisation gets you.
        if int(self.text()[::-1].split(" ",2)[1][::-1]) <= 0:
            self.increment += 1
            if self.increment >= len(self.txts):
                self.deleteLater()
                return
            self.setText(self.txts[self.increment])
    def _on_press(self):
        super()._on_press()
    def _on_release(self):
        super()._on_release()
class HoverButton(Button):
    '''For the Greed Puzzle, will most likely stay unused'''
    def __init__(self, text: str, function: Callable, bg: str="black", text_color: str="white") -> HoverButton:
        super().__init__(text, bg, text_color)
        self.func = function
    def enterEvent(self, event):
        super().enterEvent(event)
        self._on_hover()
    def _on_hover(self):
        self.func()
class Animation_Handler(QObject): 
    '''The text animation handler for my Cutscene class
    It used to just be called "Test", how informative'''
    def __init__(self, dialog: QDialog, text_list: list[str], timer: QTimer, end_function: Optional[Callable]=None) -> Animation_Handler: 
        super().__init__(dialog) 
        self.dialog = dialog 
        self.text_blocks = text_list  
        self.block_index = 0 
        self.char_index = 0 
        self.timer = timer 
        self._keys_pressed: set[Qt.Key] = set()
        self.func = end_function 
    def text_animator(self, label: QLabel): 
        if self.block_index < len(self.text_blocks): 
            current_block = self.text_blocks[self.block_index]
            
            if self.timer.interval() == 1000:
                label.setText("")
                if Qt.Key_C not in self._keys_pressed:
                  self.timer.setInterval(100)
                self.char_index = 0
                return

            if self.char_index < len(current_block): 
                label.setText(label.text() + current_block[self.char_index]) 
                self.char_index += 1 
            else: 
                if Qt.Key_C not in self._keys_pressed:
                  self.timer.setInterval(1000)
                self.block_index += 1
        else: 
            self.timer.stop() 
            self._on_end() 
    def _on_end(self): 
        if self.func: 
            self.func() 
        self.dialog.close() 
    def keyPressEvent(self, event: QKeyEvent):
       if event.isAutoRepeat():
            return
       if event.key() == Qt.Key_C:
           if self.timer.interval() > 10:
             self.timer.setInterval(10)
       self._keys_pressed.add(event.key())
    def keyReleaseEvent(self, event: QKeyEvent):
        if event.isAutoRepeat():
            return
        self._keys_pressed.discard(event.key())
class ScanlineOverlay(QWidget):
    def __init__(self, parent: Optional[QObject]=None) -> ScanlineOverlay:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        self.bar_y = 0  # Initial vertical position of the bar
        self.bar_height = 80  # Thickness of the rolling bar
        
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.update_position)
        self.anim_timer.start(16)

    def update_position(self):
        self.bar_y += 2.5  # Speed of the moving bar
        if self.bar_y > self.height():
            self.bar_y = -self.bar_height 
        self.update() 

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        bar_color = QColor(0, 255, 0, 25) 
        painter.fillRect(0, self.bar_y, self.width(), self.bar_height, bar_color)
class Cutscene(QDialog):
    '''Most inefficient cutscene creation ever?'''
    def __init__(self, text: list, text_color: str, bg: str, overlay: bool=False, parent: Optional[QObject]=None) -> Cutscene:
        super().__init__(parent, Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self.c_layout = QGridLayout(self)
        self.c_layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel("")
        self.label.setWordWrap(True)
        self.label.setStyleSheet(f"""QLabel{{ color: {text_color}; background-color: {bg}; font-weight: bold; font-size: 40px; padding: 50px}}""")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.overlay = ScanlineOverlay() if overlay else None
        self.c_layout.addWidget(self.label)
        if self.overlay:
            self.c_layout.addWidget(self.overlay, 0, 0)
            self.overlay.raise_()
        self.showFullScreen()
        self.timer = QTimer()
        animation = Animation_Handler(self, text, self.timer)
        self.setLayout(self.c_layout)
        self.timer.timeout.connect(lambda: animation.text_animator(self.label)) 
        self.timer.start(250) 
#Security validations and hashing, self explanatory
def validate_username(username: str) -> bool:
    return 3 <= len(username) <= 32 and username.isalnum()
def validate_password(pw: str) -> bool:
    return (len(pw) >= 8 and any(c.islower() for c in pw) and any(c.isupper() for c in pw) and any(c.isdigit() for c in pw) and any(not c.isalnum() for c in pw))
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())
class AuthWorker(QThread):
    '''The thread that deals with the authentication
    I'm admittedly way too lazy to write fully proper docstrings with parameter explanations for every single one of these classes'''
    finished = Signal(bool, str)  # success, message

    def __init__(self, mode: str, username: str, password: str, password2: Optional[str]=None, save_blob: dict=def_stat_increment) -> AuthWorker:
        super().__init__()
        self.mode = mode
        self.username = username
        self.password = password
        self.password2 = password2
        self.save_blob = save_blob

    def run(self):
        try:
            if self.mode == "register":
                if self.password != self.password2:
                    self.finished.emit(False, "Passwords do not match")
                    return

                hashed = hash_password(self.password)

                success = db.create_account(
                    self.username,
                    hashed,
                    self.save_blob
                )

                if success:
                    self.finished.emit(True, "Account created")
                else:
                    self.finished.emit(False, "Username already exists")

            elif self.mode == "login":
                row = db.get_account(self.username)

                if not row:
                    self.finished.emit(False, "Account not found")
                    return
                if check_password(self.password, row[0]['password_hash']):
                    self.finished.emit(True, "Login successful")
                else:
                    self.finished.emit(False, "Incorrect password")

        except Exception as e:
            self.finished.emit(False, f"Error: {e}")
class LoginWidget(QWidget):
    def __init__(self, parent: Optional[QObject]=None) -> LoginWidget:
        super().__init__(parent)
        layout = QVBoxLayout()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.status = QLabel("")
        self.login_btn = QPushButton("Login")
        register_alternative = QPushButton("Don't have an account? Create one instead!")
        self.login_btn.clicked.connect(parent.login)
        register_alternative.clicked.connect(parent.open_register)
        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.username)
        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.password)
        layout.addWidget(self.login_btn)
        layout.addWidget(register_alternative)
        layout.addWidget(self.status)
        self.setLayout(layout)
class RegisterWidget(QWidget):
    def __init__(self, parent: Optional[QObject]=None) -> RegisterWidget:
        super().__init__(parent)
        layout = QVBoxLayout()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password2 = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password2.setEchoMode(QLineEdit.Password)
        self.status = QLabel("")
        self.register_btn = QPushButton("Register")
        login_alternative = QPushButton("Already have an account? Login instead!")
        self.register_btn.clicked.connect(self.parent().register)
        login_alternative.clicked.connect(self.parent().open_login)
        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.username)
        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.password)
        layout.addWidget(QLabel("Repeat Password"))
        layout.addWidget(self.password2)
        layout.addWidget(self.register_btn)
        layout.addWidget(login_alternative)
        layout.addWidget(self.status)
        self.setLayout(layout)
class AuthWindow(QDialog):
    registered = Signal()
    
    def __init__(self, type: str, parent: Optional[QObject]=None) -> AuthWindow:
        super().__init__(parent)
        self.setWindowTitle("Registration")
        self.type = type
        self.central = QStackedWidget()
        self.setStyleSheet(cytherax_stylesheet)
        layout = QVBoxLayout()
        
        self.login_w = LoginWidget(self)
        self.register_w = RegisterWidget(self)
        
        self.central.addWidget(self.login_w)
        self.central.addWidget(self.register_w)
        
        title = QLabel("AIHA Corp. Registration Page")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        footnote = QLabel("Registration Page © AIHA Corp.")
        footnote.setFont(QFont("Consolas", 10))
        layout.addWidget(title)
        layout.addWidget(self.central)
        layout.addWidget(footnote)
        self.setLayout(layout)
        if type == "Register":
            self.central.setCurrentWidget(self.register_w)
        else:
            self.central.setCurrentWidget(self.login_w)
        self.worker = None

    def register(self):
        u = self.register_w.username.text().strip()
        p1 = self.register_w.password.text()
        p2 = self.register_w.password2.text()

        if not validate_username(u):
            self.register_w.status.setText("Invalid username")
            return

        if not validate_password(p1):
            self.register_w.status.setText("Weak password")
            return

        self.start_worker("register", u, p1, p2)
    def login(self):
        u = self.login_w.username.text().strip()
        p = self.login_w.password.text()

        self.start_worker("login", u, p)

    def start_worker(self, mode: str, username: str, password: str, password2: Optional[str]=None):
        self.worker = AuthWorker(mode, username, password, password2)
        self.worker.finished.connect(self.on_result)
        self.worker.start()

        self.central.currentWidget().status.setText("Working...")

    def on_result(self, success: bool, message: str):
        self.central.currentWidget().status.setText(message)

        if success:
            if not validate_session():
              create_session(self.central.currentWidget().username.text().strip())
              QTimer.singleShot(250, self, self.close)
    def open_register(self):
        self.central.setCurrentWidget(self.register_w)
    def open_login(self):
        self.central.setCurrentWidget(self.login_w)
    def closeEvent(self, event: QCloseEvent):
        if validate_session():
            self.registered.emit()
            event.accept()
        else:
            QMessageBox.warning(self, "Error 400", "Error: Window cannot be closed, session could not be found.")
            event.ignore()












'''
WARNING:
The segment below was heavily based on "outsourcing" through the use of Artificial Intelligence
Admittedly, the BossFight was never meant to make it into the main program, but here it is now
You may ignore the segment entirely if you wish, as despite the massive amount of code it uses it is only used in one ultraspecific location
'''











class PlayerPos:
    _instance_x: Optional[PlayerPos] = None
    _instance_y: Optional[PlayerPos] = None
 
    def __init__(self, axis: str) -> None:
        self._axis = axis  # "x" or "y"
 
    def __repr__(self) -> str:
        return f"PLAYER_{'X' if self._axis == 'x' else 'Y'}"
 
 
PLAYER_X: PlayerPos = PlayerPos("x")
PLAYER_Y: PlayerPos = PlayerPos("y")
 
# Type alias: any coordinate field can accept a plain float or a player pos.
Coord = Union[float, PlayerPos]

@dataclass
class BeamAttack:
    # axis-aligned
    orientation: str = "horizontal"
    position: Coord = 0.5

    # angled
    angle: Optional[float] = None
    origin_x: Coord = 0.5
    origin_y: Coord = 0.5

    # shared
    warning_ms: int = 1000
    duration_ms: int = 500
    thickness: int = 28
    delay_ms: int = 0
    color_warn: str = "#ffaa00"
    color_beam: str = "#ff3300"
    hitbox_shrink: int = 2
    track_player: bool = False
    inverse: bool = False

    # runtime state
    _snapped_origin_x: Optional[float] = field(default=None, init=False)
    _snapped_origin_y: Optional[float] = field(default=None, init=False)
    _snapped_position: Optional[float] = field(default=None, init=False)
    _phase: str = field(default="waiting", init=False)
    _phase_start: float = field(default=0.0, init=False)
    _fight_start: float = field(default=0.0, init=False)
    
@dataclass
class CircleAttack:
    x: Coord = 0.5
    y: Coord = 0.5

    # usual
    warning_ms: int = 1000
    duration_ms: int = 500
    radius: int = 28
    delay_ms: int = 0
    color_warn: str = "#ffaa00"
    color_beam: str = "#ff3300"
    hitbox_shrink: int = 2
    track_player: bool = False
    inverse: bool = False

    # runtime state
    _snapped_x: Optional[float] = field(default=None, init=False)
    _snapped_y: Optional[float] = field(default=None, init=False)
    _phase: str = field(default="waiting", init=False)
    _phase_start: float = field(default=0.0, init=False)
    _fight_start: float = field(default=0.0, init=False)

@dataclass
class ProjectileAttack:
    x: float = 0.5
    y: float = 0.5
    vx: float = -0.1
    vy: float = 0.1
    size: int = 20
    delay_ms: int = 0
    image_path: Optional[str] = "Program/Assets/Low quality projectile.png" #Hard coded because going back into every single projectile instance to set the path would be tedious
    color: str = "#e040fb"
    hitbox_shrink: int = 4
    track_player: bool = False
    inverse: bool = False

    # runtime state
    _active: bool = field(default=False, init=False)
    _done: bool = field(default=False, init=False)
    _px: float = field(default=0.0, init=False)
    _py: float = field(default=0.0, init=False)
    _pixmap: Optional[QPixmap] = field(default=None, init=False if not image_path else True)
    _fight_start: float = field(default=0.0, init=False)

@dataclass
class TextAttack:
    text: str = "..."
    x: Coord = 0.5
    y: Coord = 0.1
    duration_ms: int = 1500
    delay_ms: int = 0
    font_size: int = 32
    color: str = "#ffffff"

    # runtime state
    _active: bool = field(default=False, init=False) #I'm not going to write this on every line, but this essentially ensures that the unnecessary variables are not created on initialisation, they should not be defined on initialisastion as they are runtime states
    _done: bool = field(default=False, init=False)
    _start: float = field(default=0.0, init=False)
    _fight_start: float = field(default=0.0, init=False)
    _snapped_x: Optional[float] = field(default=None, init=False)
    _snapped_y: Optional[float] = field(default=None, init=False)
    
@dataclass
class ProjectileBurst:
    '''
    A warning marker followed by projectiles that all spawn from the given location,
    if PlayerPos was used as an arugment projectiles will come from the position the player was at when the warning first appeared.

    Created with random_projectiles()
    '''
    x: Coord = 0.5
    y: Coord = 0.5
    projectiles: list[ProjectileAttack] = field(default_factory=list)
    warning_ms: int = 600
    warning_color: str = "#ff4444"
    warning_font_size: int = 18
    delay_ms: int = 0
    spawn_delay_spread_ms: int = 0

    # runtime state
    _done: bool = field(default=False, init=False)
    _snapped_x: Optional[float] = field(default=None, init=False)
    _snapped_y: Optional[float] = field(default=None, init=False)
    _fight_start: float = field(default=0.0, init=False)
 
def rotating_beams(
    *, #Strictly keywords
    # geometry
    origin_x: float = 0.5,
    origin_y: float = 0.5,
    start_angle: float = 0.0,
    angle_between: float = 45.0,
    revolutions: float = 1.0,
    # timing
    delay_ms: int = 0,
    beam_delay_ms: int = 200,
    # BeamAttack defaults
    warning_ms: int = 1000,
    duration_ms: int = 500,
    thickness: int = 28,
    color_warn: str = "#ffaa00",
    color_beam: str = "#ff3300",
    hitbox_shrink: int = 6,
    track_player: bool= False,
    inverse: bool = False
) -> list[BeamAttack]:
    if angle_between <= 0:
        print("Angle between beams must be positive")
        return []
 
    total_degrees = 360.0 * revolutions
    raw_count = total_degrees / angle_between
    count = max(1, round(raw_count))
 
    beams: list[BeamAttack] = []
    for i in range(count):
        beams.append(BeamAttack(
            angle=start_angle + i * angle_between,
            origin_x=origin_x,
            origin_y=origin_y,
            delay_ms=delay_ms + i * beam_delay_ms,
            warning_ms=warning_ms,
            duration_ms=duration_ms,
            thickness=thickness,
            color_warn=color_warn,
            color_beam=color_beam,
            hitbox_shrink=hitbox_shrink,
            track_player=track_player,
            inverse=inverse
        ))
    return beams
def random_projectiles(
    *,
    x: Coord = 0.5,
    y: Coord = 0.5,
    amount: int = 10,
    delay_ms: int = 0,
    speed_min: float = 0.15,
    speed_max: float = 0.35,
    angle_min: float = 0.0,
    angle_max: float = 360.0,
    spawn_delay_spread_ms: int = 0,
    warning_ms: int = 600,
    warning_color: str = "#ff4444",
    warning_font_size: int = 18,
    size: int = 20,
    image_path: Optional[str] = "Program/Assets/Low quality projectile.png",
    color: str = "#e040fb",
    hitbox_shrink: int = 4,
) -> list:
    speed_min = max(speed_min, 0.05)
    speed_max = max(speed_max, speed_min)
    projectiles = []
    for i in range(amount):
        speed = random.uniform(speed_min, speed_max)
        angle_deg = random.uniform(angle_min, angle_max)
        angle_rad = math.radians(angle_deg)
        projectiles.append(ProjectileAttack(
            x=0.0, y=0.0,          # placeholder values to be overwritten
            vx=math.cos(angle_rad) * speed,
            vy=math.sin(angle_rad) * speed,
            size=size,
            delay_ms=i * spawn_delay_spread_ms,
            image_path=image_path,
            color=color,
            hitbox_shrink=hitbox_shrink,
        ))

    return [ProjectileBurst(
        x=x,
        y=y,
        projectiles=projectiles,
        warning_ms=warning_ms,
        warning_color=warning_color,
        warning_font_size=warning_font_size,
        delay_ms=delay_ms,
        spawn_delay_spread_ms=spawn_delay_spread_ms,
    )]

class BossFight(QDialog):
    """
    Fullscreen frameless PySide6 widget that runs a bullet-hell fight sequence.
 
    Parameters
    ----------
    attacks           : list of Attack Objects
    background_color  : any HEX colour string, transparency through these strings is not supported
    player_image_path : optional path to a player sprite image
    player_size       : player square side length in pixels
    player_speed      : player movement speed in pixels per second
    player_color      : fallback player colour when no image is given
    time_scale        : Speed up gameplay for debug purposes, obselete
    start_ms          : The better debug, starts from a given point in the fight
    end_ms            : Where the fight ends
    collisions_enabled: Disable collisions to test attack patterns for debugging
    end_function      : What happens when the player wins, called upon victory
    """
 
    TICK_MS = 16   # 60 fps
 
    def __init__(
        self,
        parent: QObject = None,
        attacks: list = None,
        background_color: str = "#000000",
        player_image_path: Optional[str] = "Program/Assets/The Culmination of Your Being.png",
        player_size: int = 20,
        player_speed: float = 450.0,
        player_color: str = "#00e5ff",
        time_scale: float = 1.0,
        start_ms: float = 0.0,
        end_ms: float = math.inf,
        collisions_enabled: bool=True,
        end_function: Optional[Callable]=None
    ):
        super().__init__(parent)
        self._time_scale=time_scale
        self._start_ms = start_ms
        self.end_ms = end_ms
        self.end_function = end_function
        self._end_func_called = False
        self.mm = self.parent().music_manager
        self.mm.offset = self._start_ms
        self.mm.path = f"{global_path_reference}/Program/Music/Bossfight Test"
        self.mm.music_list = os.listdir(self.mm.path)
        self.mm.stop()
        self.mm.stop_perm = True
        self.collisions_enabled = collisions_enabled
 
        self._bg_color = QColor(background_color)
        self._attacks: list = attacks or []
        self._player_size = player_size
        self._player_speed = player_speed
        self._player_color = QColor(player_color)
        self._player_image_path = player_image_path
 
        # Player position
        self._player_x: float = 0.0
        self._player_y: float = 0.0
        self._keys_pressed: set[Qt.Key] = set()
 
        self._alive: bool = True
        self._victory: bool = False
        self._fight_start: float = time.monotonic()
        self._last_tick: float = self._fight_start
 
        # Load player
        self._player_pixmap: Optional[QPixmap] = None
        if player_image_path:
            pm = QPixmap(player_image_path)
            if not pm.isNull():
                self._player_pixmap = pm.scaled(
                    player_size, player_size,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation,
                )
 
        # Preload projectile images
        now = self._fight_start
        for atk in self._attacks:
            atk._fight_start = now
            if isinstance(atk, ProjectileAttack) and atk.image_path:
                pm = QPixmap(atk.image_path)
                if not pm.isNull():
                    atk._pixmap = pm.scaled(
                        atk.size, atk.size,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation,
                    )
            if isinstance(atk, BeamAttack):
                atk._phase = "waiting"
            if isinstance(atk, CircleAttack):
                atk._phase = "waiting"
            if isinstance(atk, ProjectileBurst):
                for projectile in atk.projectiles:
                    if projectile.image_path:
                      pm = QPixmap(projectile.image_path)
                      if not pm.isNull():
                          projectile._pixmap = pm.scaled(
                              projectile.size, projectile.size,
                              Qt.KeepAspectRatio,
                              Qt.SmoothTransformation,
                          )
        
        self._reset()
        
        # Window setup
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.showFullScreen()
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()
 
        # Game loop timer
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(self.TICK_MS)
 
    
    def _reset(self):
        """Reset all attack and player states so the fight can start fresh."""
        now = time.monotonic()
        self.mm.play_random()
        self._fight_start = now - self._start_ms / 1000.0
        self._last_tick = now
        self._alive = True
        self._keys_pressed.clear()
 
        # Re-centre player
        cx = self.width() / 2.0
        cy = self.height() / 2.0
        self._player_x = cx - self._player_size / 2
        self._player_y = cy - self._player_size / 2
 
        #Reset every attack, mark any attack before start_ms as done
        for atk in self._attacks:
            atk._fight_start = now
            if isinstance(atk, BeamAttack):
                atk._phase_start = 0.0
                atk._snapped_origin_x = None
                atk._snapped_origin_y = None
                atk._snapped_position = None
                finished_by = atk.delay_ms + atk.warning_ms + atk.duration_ms
                if finished_by <= self._start_ms:
                    atk._phase = "done"
                else:
                    atk._phase = "waiting"
            elif isinstance(atk, CircleAttack):
                atk._phase_start = 0.0
                atk._snapped_x = None
                atk._snapped_y = None
                finished_by = atk.delay_ms + atk.warning_ms + atk.duration_ms
                if finished_by <= self._start_ms:
                    atk._phase = "done"
                else:
                    atk._phase = "waiting"
            elif isinstance(atk, ProjectileAttack):
                atk._px = 0.0
                atk._py = 0.0
                finished_by = atk.delay_ms  # projectiles go off screen and do not time out
                if finished_by <= self._start_ms:
                    # Ignore projectiles that wouldn't have spawned by this time, it is impossible to predict exact location without simulating the projectiles first
                    atk._active = False
                    atk._done = True
                else:
                    atk._active = False
                    atk._done = False
            elif isinstance(atk, TextAttack):
                atk._start = 0.0
                atk._snapped_x = None
                atk._snapped_y = None
                finished_by = atk.delay_ms + atk.duration_ms
                if finished_by <= self._start_ms:
                    atk._active = False
                    atk._done = True
                else:
                    atk._active = False
                    atk._done = False
            elif isinstance(atk, ProjectileBurst):
                 atk._snapped_x = None
                 atk._snapped_y = None
                 last_proj_delay = max((p.delay_ms for p in atk.projectiles), default=0)
                 finished_by = atk.delay_ms + atk.warning_ms + last_proj_delay
                 atk._done = finished_by <= self._start_ms
                 for proj in atk.projectiles:
                     proj._active = False
                     proj._done = atk._done
                     proj._px = 0.0
                     proj._py = 0.0
 
    def resizeEvent(self, event):
        # Centre player on first show
        cx = self.width() / 2.0
        cy = self.height() / 2.0
        self._player_x = cx - self._player_size / 2
        self._player_y = cy - self._player_size / 2
 
    def keyPressEvent(self, event: QKeyEvent):
       if event.key() == Qt.Key_Escape:
           self.close()
       if event.key() == Qt.Key_R and not self._alive:
           self._reset()
       if not event.isAutoRepeat():
           self._keys_pressed.add(event.key())
 
    def keyReleaseEvent(self, event: QKeyEvent):
        if not event.isAutoRepeat():
            self._keys_pressed.discard(event.key())

    def _tick(self):
        now = time.monotonic()
        dt = now - self._last_tick * self._time_scale
        self._last_tick = now
        elapsed_ms = (now - self._fight_start) * 1000.0 * self._time_scale
        if elapsed_ms >= self.end_ms and self._alive and not self._victory:
            self._victory = True #Funny story, I was wondering why this wasn't working, and then I realised I had put self._victory - True instead of = True
        
        if self._alive:
            self._move_player(dt)
 
        self._update_attacks(elapsed_ms, dt)
 
        if self._alive:
            self._check_collisions()
 
        self.update()  #repaint
 
    def _resolve(self, coord: Coord, axis: str) -> float:
        """
        Resolve coord to screen fraction to give player's current position
        """
        if not isinstance(coord, PlayerPos):
            return coord
        W, H = self.width(), self.height()
        if axis == "x":
            return (self._player_x + self._player_size / 2) / W if W else 0.0
        else:
            return (self._player_y + self._player_size / 2) / H if H else 0.0
 
    def _resolve_beam_origin(self, atk: BeamAttack) -> tuple[float, float]:
        """
        Return resolved origin points, if track_player=False return player's position when attack was first called
        """
        if not atk.track_player and atk._snapped_origin_x is not None:
            return atk._snapped_origin_x, atk._snapped_origin_y
        return self._resolve(atk.origin_x, "x"), self._resolve(atk.origin_y, "y")
    def _resolve_beam_position(self, atk: BeamAttack) -> float:
        """Resolve the position on axis"""
        if not atk.track_player and atk._snapped_position is not None:
            return atk._snapped_position
        axis = "y" if atk.orientation == "horizontal" else "x"
        return self._resolve(atk.position, axis)
    def _resolve_circle_coords(self, atk: CircleAttack, W, H) -> float:
        if not atk.track_player and atk._snapped_x is not None:
            return atk._snapped_x, atk._snapped_y
        return self._resolve(atk.x, "x") * W, self._resolve(atk.y, "y") * H
 
    def _move_player(self, dt: float):
        dx = dy = 0.0
        if Qt.Key_Left in self._keys_pressed or Qt.Key_A in self._keys_pressed:
            dx -= 1
        if Qt.Key_Right in self._keys_pressed or Qt.Key_D in self._keys_pressed:
            dx += 1
        if Qt.Key_Up in self._keys_pressed or Qt.Key_W in self._keys_pressed:
            dy -= 1
        if Qt.Key_Down in self._keys_pressed or Qt.Key_S in self._keys_pressed:
            dy += 1
 
        if dx != 0 and dy != 0:
            # Diagonal movement
            factor = 0.7071
            dx *= factor
            dy *= factor
 
        speed = self._player_speed
        self._player_x += dx * speed * dt
        self._player_y += dy * speed * dt

        s = self._player_size
        self._player_x = max(0.0, min(self.width() - s, self._player_x))
        self._player_y = max(0.0, min(self.height() - s, self._player_y))
 
    def _update_attacks(self, elapsed_ms: float, dt: float):
        W, H = self.width(), self.height()
 
        for atk in self._attacks:
 
            if isinstance(atk, BeamAttack):
                if atk._phase == "waiting":
                  if elapsed_ms >= atk.delay_ms:
                      atk._phase = "warn"
                      atk._phase_start = time.monotonic()
                      if not atk.track_player:
                          atk._snapped_origin_x = self._resolve(atk.origin_x, "x")
                          atk._snapped_origin_y = self._resolve(atk.origin_y, "y")
                          # Snapshot position using the correct axis for this orientation
                          axis = "y" if atk.orientation == "horizontal" else "x"
                          atk._snapped_position = self._resolve(atk.position, axis)
                elif atk._phase == "warn":
                    age_ms = (time.monotonic() - atk._phase_start) * 1000
                    if age_ms >= atk.warning_ms:
                        atk._phase = "active"
                        atk._phase_start = time.monotonic()
                elif atk._phase == "active":
                    age_ms = (time.monotonic() - atk._phase_start) * 1000
                    if age_ms >= atk.duration_ms:
                        atk._phase = "done"
 
            elif isinstance(atk, ProjectileAttack):
                if atk._done:
                    continue
                if not atk._active:
                    if elapsed_ms >= atk.delay_ms:
                        atk._active = True
                        atk._px = self._resolve(atk.x, "x") * W
                        atk._py = self._resolve(atk.y, "y") * H
                else:
                    atk._px += atk.vx * W * dt
                    atk._py += atk.vy * H * dt
                    # End attack when off screen
                    s = atk.size
                    if (atk._px + s < 0 or atk._px > W or
                            atk._py + s < 0 or atk._py > H):
                        atk._done = True
 
            elif isinstance(atk, TextAttack):
              if atk._done:
                  continue
              if not atk._active:
                  if elapsed_ms >= atk.delay_ms:
                      atk._active = True
                      atk._snapped_x = self._resolve(atk.x, "x")
                      atk._snapped_y = self._resolve(atk.y, "y")
                      atk._start = time.monotonic()
              else:
                  age_ms = (time.monotonic() - atk._start) * 1000
                  if age_ms >= atk.duration_ms:
                      atk._done = True
            elif isinstance(atk, CircleAttack):
                W = self.width()
                H = self.height()
                if atk._phase == "waiting":
                  if elapsed_ms >= atk.delay_ms:
                      atk._phase = "warn"
                      atk._phase_start = time.monotonic()
                      if not atk.track_player:
                          atk._snapped_x, atk._snapped_y = self._resolve_circle_coords(atk, W, H)
                elif atk._phase == "warn":
                    age_ms = (time.monotonic() - atk._phase_start) * 1000
                    if age_ms >= atk.warning_ms:
                        atk._phase = "active"
                        atk._phase_start = time.monotonic()
                elif atk._phase == "active":
                    age_ms = (time.monotonic() - atk._phase_start) * 1000
                    if age_ms >= atk.duration_ms:
                        atk._phase = "done"
            elif isinstance(atk, ProjectileBurst):
                  if atk._done:
                      continue
                  elapsed_since_fight = elapsed_ms
              
                  if atk._snapped_x is None:
                      # Not triggered yet
                      if elapsed_since_fight >= atk.delay_ms:
                          atk._snapped_x = self._resolve(atk.x, "x")
                          atk._snapped_y = self._resolve(atk.y, "y")
                  else:
                      # Triggered
                      age_ms = elapsed_since_fight - atk.delay_ms
                      all_done = True
                      for proj in atk.projectiles:
                          if proj._done:
                              continue
                          all_done = False
                          proj_trigger = atk.warning_ms + proj.delay_ms
                          if not proj._active and age_ms >= proj_trigger:
                              proj._active = True
                              proj._px = atk._snapped_x * W
                              proj._py = atk._snapped_y * H
                          if proj._active:
                              proj._px += proj.vx * W * dt
                              proj._py += proj.vy * H * dt
                              s = proj.size
                              if (proj._px + s < 0 or proj._px > W or
                                      proj._py + s < 0 or proj._py > H):
                                  proj._done = True
                      if all_done and age_ms > atk.warning_ms:
                          atk._done = True
 
    def _player_hitbox(self) -> QRectF:
        """Return a slightly inset or outset hitbox for player forgiveness."""
        margin = 4
        s = self._player_size
        return QRectF(
            self._player_x + margin,
            self._player_y + margin,
            s - margin * 2,
            s - margin * 2,
        )
 
    def _check_collisions(self):
        if not self.collisions_enabled:
          return
        phb = self._player_hitbox()
 
        for atk in self._attacks:
 
            if isinstance(atk, BeamAttack):
                if atk._phase != "active":
                    continue
                sk = atk.hitbox_shrink
                t = atk.thickness
 
                if atk.angle is not None:
                    W2, H2 = self.width(), self.height()
                    ox_frac, oy_frac = self._resolve_beam_origin(atk)
                    ox = ox_frac * W2
                    oy = oy_frac * H2
                    rad = math.radians(atk.angle)
                    # Unit direction vector along the beam
                    dx = math.cos(rad)
                    dy = math.sin(rad)
                    # Player hitbox centre
                    pcx = phb.x() + phb.width() / 2
                    pcy = phb.y() + phb.height() / 2
                    # Perpendicular distance = abs(cross product of (p-o) and d) i.e. math stuff
                    rx, ry = pcx - ox, pcy - oy
                    perp_dist = abs(rx * dy - ry * dx)
                    half_hit = t / 2 - sk
                    is_colliding = perp_dist < half_hit
                    is_colliding = not is_colliding if atk.inverse else is_colliding
                    if is_colliding:
                        self._alive = False
                else:
                    W2, H2 = self.width(), self.height()
                    pos = atk.position
                    pos = self._resolve_beam_position(atk)
                    if atk.orientation == "horizontal":
                        pos = self._resolve(pos, "y")
                        cy = pos * H2
                        beam_rect = QRectF(0, cy - t / 2 + sk, W2, t - sk * 2)
                    else:
                        pos = self._resolve(pos, "x")
                        cx = pos * W2
                        beam_rect = QRectF(cx - t / 2 + sk, 0, t - sk * 2, H2)
                    is_colliding = phb.intersects(beam_rect)
                    is_colliding = not is_colliding if atk.inverse else is_colliding
                    if is_colliding:
                        self._alive = False
            elif isinstance(atk, CircleAttack):
                if atk._phase != "active":
                    continue
                sk = atk.hitbox_shrink
                W2, H2 = self.width(), self.height()
                cx, cy = self._resolve_circle_coords(atk, W2, H2)
                r = atk.radius
                closest_x = max(phb.left(), min(cx, phb.right()))
                closest_y = max(phb.top(), min(cy, phb.bottom()))
                distance_x = cx - closest_x
                distance_y = cy - closest_y
                r = r - sk
                is_colliding = (distance_x ** 2 + distance_y ** 2) < (r ** 2) #For an accurate circle the equation x^2 + y^2 < r^2 is used to check if it is within the circle. This is another math thing
                is_colliding = not is_colliding if atk.inverse else is_colliding
                if is_colliding:
                  self._alive = False
            elif isinstance(atk, ProjectileAttack):
                if not atk._active or atk._done:
                    continue
                sk = atk.hitbox_shrink
                s = atk.size
                proj_rect = QRectF(
                    atk._px + sk, atk._py + sk,
                    s - sk * 2, s - sk * 2,
                )
                is_colliding = phb.intersects(proj_rect)
                is_colliding = not is_colliding if atk.inverse else is_colliding
                if is_colliding:
                    self._alive = False
            elif isinstance(atk, ProjectileBurst):
                if atk._snapped_x is None or atk._done:
                    continue
                for proj in atk.projectiles:
                    if not proj._active or proj._done:
                        continue
                    sk = proj.hitbox_shrink
                    s = proj.size
                    proj_rect = QRectF(proj._px + sk, proj._py + sk, s - sk*2, s - sk*2)
                    if phb.intersects(proj_rect):
                        self._alive = False
 
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        W, H = self.width(), self.height()
        # Background
        painter.fillRect(0, 0, W, H, self._bg_color)
 
        # Draw attacks
        for atk in self._attacks:
            if isinstance(atk, CircleAttack):
                self._draw_circle(painter, atk, W, H)
            elif isinstance(atk, BeamAttack):
                self._draw_beam(painter, atk, W, H)
            elif isinstance(atk, ProjectileAttack):
                self._draw_projectile(painter, atk)
            elif isinstance(atk, TextAttack):
                self._draw_text_attack(painter, atk, W, H)
            elif isinstance(atk, ProjectileBurst):
                self._draw_burst(painter, atk, W, H)
 
        # Draw player
        self._draw_player(painter)
 
        # Death overlay
        if not self._alive:
            self._draw_death_overlay(painter, W, H)
        elif self._victory: #Skips alive check as the death overlay only applies if the player is alive and would be executed first
            self._draw_victory_overlay(painter, W, H) #Victory
 
        painter.end()
 
 
    def _beam_half_length(self, W: int, H: int) -> float:
        '''Half-diagonal of the screen'''
        return math.hypot(W, H)
 
    def _draw_beam(self, painter: QPainter, atk: BeamAttack, W: int, H: int):
        if atk._phase == "waiting" or atk._phase == "done":
            return # If the attack shouldn't be on screen don't draw it
 
        if atk.angle is not None:
            self._draw_beam_angled(painter, atk, W, H)
        else:
            self._draw_beam_axis(painter, atk, W, H)
 
    def _draw_beam_axis(self, painter: QPainter, atk: BeamAttack, W: int, H: int):
        """Axis beam drawing"""
        t = atk.thickness
        pos = atk.position
        pos = self._resolve_beam_position(atk)
 
        if atk.orientation == "horizontal":
            cy = int(pos * H)
            rect = QRect(0, cy - t // 2, W, t)
        else:
            cx = int(pos * W)
            rect = QRect(cx - t // 2, 0, t, H)
 
        if atk._phase == "warn":
            age = (time.monotonic() - atk._phase_start) * 1000
            progress = min(age / atk.warning_ms, 1.0)
            alpha = int(80 + 120 * abs((progress * 6 % 2) - 1))
            color = QColor(atk.color_warn)
            color.setAlpha(alpha)
            painter.fillRect(rect, color)
 
            pen = QPen(QColor(atk.color_warn))
            pen.setWidth(2)
            pen.setStyle(Qt.DashLine)
            painter.setPen(pen)
            if atk.orientation == "horizontal":
                painter.drawLine(0, int(pos * H), W, int(pos * H))
            else:
                painter.drawLine(int(pos * W), 0, int(pos * W), H)
 
        elif atk._phase == "active":
            color = QColor(atk.color_beam)
            color.setAlpha(230)
            painter.fillRect(rect, color)
            core_rect = QRect(rect)
            shrink = t // 3
            if atk.orientation == "horizontal":
                core_rect.adjust(0, shrink, 0, -shrink)
            else:
                core_rect.adjust(shrink, 0, -shrink, 0)
            core_color = QColor("#000000")
            core_color.setAlpha(180)
            painter.fillRect(core_rect, core_color)
 
    def _draw_beam_angled(self, painter: QPainter, atk: BeamAttack, W: int, H: int):
        """
        Angled beam centred on (origin_x*W, origin_y*H [for accurate relative width and heights]), rotated by "angle"
        degrees clockwise from rightward horizontal.
        """
        ox_frac, oy_frac = self._resolve_beam_origin(atk)
        ox = ox_frac * W
        oy = oy_frac * H
        half_len = self._beam_half_length(W, H)
        t = atk.thickness
 
        painter.save()
        painter.translate(ox, oy)
        painter.rotate(atk.angle)  # Rotates clockwise ofc
 
        if atk._phase == "warn":
            age = (time.monotonic() - atk._phase_start) * 1000
            progress = min(age / atk.warning_ms, 1.0)
            alpha = int(80 + 120 * abs((progress * 6 % 2) - 1))
 
            # Warning fill
            color = QColor(atk.color_warn)
            color.setAlpha(alpha)
            painter.fillRect(
                QRect(int(-half_len), -t // 2, int(half_len * 2), t),
                color,
            )
            # Dashed centre line along the beam axis, not strictly necessaru
            pen = QPen(QColor(atk.color_warn))
            pen.setWidth(2)
            pen.setStyle(Qt.DashLine)
            painter.setPen(pen)
            painter.drawLine(int(-half_len), 0, int(half_len), 0)
 
        elif atk._phase == "active":
            # Outer band
            color = QColor(atk.color_beam)
            color.setAlpha(230)
            painter.fillRect(
                QRect(int(-half_len), -t // 2, int(half_len * 2), t),
                color,
            )
            #Core strip
            shrink = t // 3
            core_color = QColor("#000000")
            core_color.setAlpha(180)
            painter.fillRect(
                QRect(int(-half_len), -t // 2 + shrink, int(half_len * 2), t - shrink * 2),
                core_color,
            )
 
        painter.restore()
    def _draw_circle(self, painter: QPainter, atk: CircleAttack, W: int, H: int):
        '''"A beam rotated on the z-axis"
            It's just a circle'''
        if atk._phase == "waiting" or atk._phase == "done":
            return #Repeat from beam code
        cx, cy = self._resolve_circle_coords(atk, W, H)
        painter.save() #Save painter settings
        painter.setPen(Qt.NoPen)
        r = atk.radius
        if atk._phase == "warn":
            age = (time.monotonic() - atk._phase_start) * 1000
            progress = min(age / atk.warning_ms, 1.0)
            alpha = int(80 + 120 * abs((progress * 6 % 2) - 1))
 
            # Warning fill
            color = QColor(atk.color_warn)
            color.setAlpha(alpha)
            brush = QBrush(color)
            painter.setBrush(brush)
            painter.drawEllipse(QPointF(cx, cy), r, r)
        elif atk._phase == "active":
            # Outer band
            color = QColor(atk.color_beam)
            color.setAlpha(230)
            brush = QBrush(color)
            painter.setBrush(brush)
            painter.drawEllipse(QPointF(cx, cy), r, r)
            # Core
            shrink = r // 3
            core_color = QColor("#000000")
            core_color.setAlpha(180)
            brush.setColor(core_color)
            painter.setBrush(brush)
            painter.drawEllipse(QPointF(cx, cy), r- shrink, r - shrink)
        painter.restore() #Restore painter settings to before the code altered it
 
    def _draw_projectile(self, painter: QPainter, atk: ProjectileAttack):
        if not atk._active or atk._done:
            return
        s = atk.size
        x, y = int(atk._px), int(atk._py)
        if atk._pixmap:
            painter.drawPixmap(x, y, atk._pixmap)
        else:
            color = QColor(atk.color)
            painter.fillRect(QRect(x, y, s, s), color)
            #Outline for clarity if there is no image path
            pen = QPen(QColor("#ffffff"))
            pen.setWidth(1)
            pen.setStyle(Qt.SolidLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(QRect(x, y, s, s))
 
    def _draw_text_attack(self, painter: QPainter, atk: TextAttack, W: int, H: int):
        if not atk._active or atk._done:
            return
 
        age_ms = (time.monotonic() - atk._start) * 1000
        progress = age_ms / atk.duration_ms
 
        # Fade in for first 15%, fade out for last 20%, basic visuals
        if progress < 0.15:
            alpha = int(255 * (progress / 0.15))
        elif progress > 0.80:
            alpha = int(255 * (1.0 - (progress - 0.80) / 0.20))
        else:
            alpha = 255
 
        color = QColor(atk.color)
        color.setAlpha(alpha)
 
        font = QFont("Arial", atk.font_size, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QPen(color))
 
        cx = int((atk._snapped_x if atk._snapped_x is not None else atk.x) * W)
        cy = int((atk._snapped_y if atk._snapped_y is not None else atk.y) * H)
 
        fm = painter.fontMetrics()
        tw = fm.horizontalAdvance(atk.text)
        th = fm.height()
        painter.drawText(cx - tw // 2, cy + th // 3, atk.text)
    def _draw_burst(self, painter: QPainter, atk: ProjectileBurst, W: int, H: int):
        if atk._done:
            return #If it's finished return, of course
        # Draw warning dot while snapped position exists but warning is still active
        if atk._snapped_x is not None:
            elapsed_ms = (time.monotonic() - self._fight_start) * 1000.0 * self._time_scale
            age_ms = elapsed_ms - atk.delay_ms
            if age_ms < atk.warning_ms:
                progress = age_ms / atk.warning_ms
                if progress < 0.15:
                    alpha = int(255 * (progress / 0.15))
                elif progress > 0.80:
                    alpha = int(255 * (1.0 - (progress - 0.80) / 0.20))
                else:
                    alpha = 255
                color = QColor(atk.warning_color)
                color.setAlpha(alpha)
                font = QFont("Arial", atk.warning_font_size, QFont.Bold)
                painter.setFont(font)
                painter.setPen(QPen(color))
                cx = int(atk._snapped_x * W)
                cy = int(atk._snapped_y * H)
                fm = painter.fontMetrics()
                tw = fm.horizontalAdvance("●")
                th = fm.height()
                painter.drawText(cx - tw // 2, cy + th // 3, "●")
    
            # Draw active projectiles
            for proj in atk.projectiles:
                self._draw_projectile(painter, proj)
 
    def _draw_player(self, painter: QPainter):
        s = self._player_size
        x, y = int(self._player_x), int(self._player_y)
 
        if not self._alive:
            painter.setOpacity(0.35)
 
        if self._player_pixmap:
            painter.drawPixmap(x, y, self._player_pixmap)
        else:
            painter.fillRect(QRect(x, y, s, s), self._player_color)
            pen = QPen(QColor("#ffffff"))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(QRect(x, y, s, s))
 
        painter.setOpacity(1.0) #Reverting opacity change incase of player death
 
    def _draw_death_overlay(self, painter: QPainter, W: int, H: int):
        overlay = QColor(180, 0, 0, 100)
        painter.fillRect(0, 0, W, H, overlay)
 
        font = QFont("Arial", 52, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QPen(QColor("#ffffff")))
        msg = "YOU DIED"
        fm = painter.fontMetrics()
        tw = fm.horizontalAdvance(msg)
        painter.drawText(W // 2 - tw // 2, H // 2, msg)
 
        font2 = QFont("Arial", 20)
        painter.setFont(font2)
        sub = "Press R to restart or ESC to exit"
        fm2 = painter.fontMetrics()
        tw2 = fm2.horizontalAdvance(sub)
        painter.drawText(W // 2 - tw2 // 2, H // 2 + 50, sub)
    def _draw_victory_overlay(self, painter: QPainter, W: int, H: int):
        overlay = QColor(0, 180, 0, 100)
        painter.fillRect(0, 0, W, H, overlay)
 
        font = QFont("Arial", 52, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QPen(QColor("#ffffff")))
        msg = "YOU WON"
        fm = painter.fontMetrics()
        tw = fm.horizontalAdvance(msg)
        painter.drawText(W // 2 - tw // 2, H // 2, msg)
 
        font2 = QFont("Arial", 20)
        painter.setFont(font2)
        sub = "Somewhere something has changed. Pressed ESC to exit." if self.collisions_enabled else "Collisions were disabled"
        fm2 = painter.fontMetrics()
        tw2 = fm2.horizontalAdvance(sub)
        painter.drawText(W // 2 - tw2 // 2, H // 2 + 50, sub)
        if callable(self.end_function):
            if not self.end_func_called and self.collisions_enabled:
              self.end_func_called = True
              self.end_function()

attacks = [
        TextAttack(
            text="This, will be fun.",
            x=0.5, y=0.12,
            duration_ms=1800,
            delay_ms=0,
            font_size=38,
            color="#ff0000"),
        BeamAttack(origin_x=0.35, origin_y=0.67, angle=147, warning_ms=1000, duration_ms=1500, thickness=50, delay_ms=1500, color_warn="#ff5555"),
        ProjectileAttack(0, 0, 0.5, 0.4, 50, 1500),
        ProjectileAttack(1, 0.1, -0.5, 0.4, 50, 1500),
        *rotating_beams(
            origin_x=0,
            origin_y=1,
            start_angle=0.0,
            angle_between=7.0,
            revolutions=0.5,
            delay_ms=2500,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=0.5,
            origin_y=0.5,
            start_angle=0.0,
            angle_between=6,
            revolutions=2.5,
            delay_ms=4500,
            beam_delay_ms=100,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *random_projectiles(
            x=0.5, y=0.5,
            amount=220,
            delay_ms=20000,
            speed_min=0.15,
            speed_max=0.60,
            spawn_delay_spread_ms=80,
            warning_ms=700,
            warning_color="#ff6644",
            size=30,
            color="#ff6644",
        ),
        *rotating_beams(origin_x=PLAYER_X,
                        origin_y=PLAYER_Y,
                        start_angle=0,
                        angle_between=70,
                        revolutions=2.5,
                        delay_ms=4500,
                        beam_delay_ms=1100,
                        warning_ms=2000,
                        duration_ms=500,
                        hitbox_shrink=6,
                        thickness=20,
                        color_warn="#ff5555",
                        color_beam="#ff0000",),
        *rotating_beams(origin_x=PLAYER_X,
                        origin_y=PLAYER_Y,
                        start_angle=0,
                        angle_between=60,
                        revolutions=1.3,
                        delay_ms=20000,
                        beam_delay_ms=2500,
                        warning_ms=1000,
                        duration_ms=500,
                        hitbox_shrink=4,
                        thickness=35,
                        color_warn="#ff5555",
                        color_beam="#ff0000",),
        ProjectileAttack(1, 0.1, -0.5, 0.4, 50, 1500),
        *rotating_beams(
            origin_x=0,
            origin_y=1,
            start_angle=0.0,
            angle_between=7.0,
            revolutions=0.5,
            delay_ms=40000,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=0,
            start_angle=0.0,
            angle_between=7.0,
            revolutions=0.5,
            delay_ms=40000,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=1,
            start_angle=0.0,
            angle_between=7.0,
            revolutions=0.5,
            delay_ms=40000,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=0,
            origin_y=0,
            start_angle=0.0,
            angle_between=7.0,
            revolutions=0.5,
            delay_ms=40000,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *random_projectiles(
            x=0, y=0,
            amount=300,
            delay_ms=42000,
            speed_min=0.1,
            speed_max=0.40,
            spawn_delay_spread_ms=40,
            warning_ms=500,
            warning_color="#ff6644",
            size=10,
            color="#ff6644",
        ),
        *random_projectiles(
            x=1, y=1,
            amount=300,
            delay_ms=42000,
            speed_min=0.1,
            speed_max=0.40,
            spawn_delay_spread_ms=40,
            warning_ms=500,
            warning_color="#ff6644",
            size=10,
            color="#ff6644",
        ),
        TextAttack("Did you really expect it to be so easy?", 0.5, 0.1, 3000, 42000, 32, "#ff0000"),
        TextAttack("I should be insulted really...", 0.5, 0.1, 3000, 45000, 32, "#ff0000"),
        TextAttack("I'm surprised you've even lasted this long.", 0.5, 0.1, 3000, 48000, 32, "#ff0000"),
        TextAttack("But with the power your idiocy gave me...", 0.5, 0.1, 3000, 51000, 32, "#ff0000"),
        TextAttack("This is far from my limit.", 0.5, 0.1, 3000, 54000, 32, "#ff0000"),
        TextAttack("So let's make things a little more interesting.", 0.5, 0.1, 3000, 57000, 32, "#ff0000"),
        *[atk for i in range(6) for atk in rotating_beams(
            origin_x=PLAYER_X,
            origin_y=PLAYER_Y,
            start_angle=-30.0,
            angle_between=30.0,
            revolutions=0.25,
            delay_ms=(42000 + 3000 * i),
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        )],
        *[BeamAttack(position=(0.05 + 0.1*i), orientation="vertical", warning_ms=1000, duration_ms=500, thickness=50, delay_ms=60000+(50*i), color_warn="#ff5555") for i in range(10)],
        *[BeamAttack(position=(0.05 + 0.1*i), orientation="horizontal", warning_ms=1000, duration_ms=500, thickness=50, delay_ms=60000+(50*i), color_warn="#ff5555") for i in range(10)],
        BeamAttack(position=0.5,orientation="vertical",warning_ms=1625,duration_ms=2500,thickness=750,delay_ms=60000,color_warn="#ff5555"),
        BeamAttack(position=PLAYER_X,orientation="vertical",warning_ms=1000,duration_ms=500,thickness=100,delay_ms=69800,color_warn="#ff5555"),
        BeamAttack(position=PLAYER_Y,orientation="horizontal",warning_ms=750,duration_ms=500,thickness=100,delay_ms=70100,color_warn="#ff5555"),
        *rotating_beams(origin_x=PLAYER_X, origin_y=PLAYER_Y,
                        delay_ms=70400,
                        start_angle=0.0,
                        angle_between=21,
                        revolutions=0.6,
                        beam_delay_ms=0,
                        warning_ms=500,
                        duration_ms=1000,
                        thickness=50,
                        color_warn="#ff5555",
                        color_beam="#ff0000"),
        *[atk for i in range(19) for atk in random_projectiles(
            x=PLAYER_X, y=PLAYER_Y,
            amount=20,
            delay_ms=62500+(1000*i),
            speed_min=0.1,
            speed_max=0.2,
            spawn_delay_spread_ms=20,
            warning_ms=1000,
            warning_color="#ff6644",
            size=15,
            color="#ff6644",
        )],
        *[atk for i in range(19) for atk in rotating_beams(
            origin_x=PLAYER_X,
            origin_y=PLAYER_Y,
            start_angle=0.0,
            angle_between=25,
            revolutions=0.3,
            delay_ms=(62000 + 1000 * i),
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        )],
        *[atk for i in range(7) for atk in rotating_beams(
            origin_x=random.choice([0,1]),
            origin_y=random.choice([0,1]),
            start_angle=0.0,
            angle_between=7.0,
            revolutions=0.5,
            delay_ms=62000 + (3000*i),
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        )],
        BeamAttack(position=PLAYER_X,orientation="vertical",warning_ms=1000,duration_ms=500,thickness=100,delay_ms=79700,color_warn="#ff5555"),
        BeamAttack(position=PLAYER_Y,orientation="horizontal",warning_ms=750,duration_ms=500,thickness=100,delay_ms=80100,color_warn="#ff5555"),
        *rotating_beams(origin_x=PLAYER_X, origin_y=PLAYER_Y,
                        delay_ms=80500,
                        start_angle=0.0,
                        angle_between=21,
                        revolutions=0.6,
                        beam_delay_ms=0,
                        warning_ms=500,
                        duration_ms=500,
                        thickness=50,
                        color_warn="#ff5555",
                        color_beam="#ff0000"),
        *rotating_beams(
            origin_x=0,
            origin_y=1,
            start_angle=0.0,
            angle_between=7.0,
            revolutions=0.5,
            delay_ms=80500,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=0,
            start_angle=0.0,
            angle_between=7.0,
            revolutions=0.5,
            delay_ms=80700,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
            *rotating_beams(
                origin_x=0.5,
                origin_y=0.5,
                start_angle=0.0,
                angle_between=6,
                revolutions=2.7,
                delay_ms=82700,
                beam_delay_ms=100,
                warning_ms=1000,
                duration_ms=450,
                thickness=40,
                color_warn="#ff5555",
                color_beam="#ff0000",
            ),
            *rotating_beams(origin_x=PLAYER_X, origin_y=PLAYER_Y,
                            delay_ms=82700,
                            start_angle=0.0,
                            angle_between=7,
                            revolutions=3.2,
                            beam_delay_ms=100,
                            warning_ms=500,
                            duration_ms=500,
                            thickness=40,
                            color_warn="#ff5555",
                            color_beam="#ff0000"),
            *rotating_beams(origin_x=PLAYER_X, origin_y=PLAYER_Y,
                            delay_ms=83700,
                            start_angle=0.0,
                            angle_between=7,
                            revolutions=2.8,
                            beam_delay_ms=100,
                            warning_ms=500,
                            duration_ms=500,
                            thickness=40,
                            color_warn="#ff5555",
                            color_beam="#ff0000"),
            *[atk for i in range(18) for atk in random_projectiles(
                x=PLAYER_X, y=PLAYER_Y,
                amount=15,
                delay_ms=82700+(1000*i),
                speed_min=0.1,
                speed_max=0.15,
                spawn_delay_spread_ms=20,
                warning_ms=1000,
                warning_color="#ff6644",
                size=15,
                color="#ff6644",
            )],
        *rotating_beams(
            origin_x=0,
            origin_y=1,
            start_angle=0.0,
            angle_between=5.5,
            revolutions=0.5,
            delay_ms=100000,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=0,
            start_angle=0.0,
            angle_between=5.5,
            revolutions=0.5,
            delay_ms=100000,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=0,
            origin_y=0,
            start_angle=0.0,
            angle_between=5.5,
            revolutions=0.5,
            delay_ms=100000,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=1,
            start_angle=0.0,
            angle_between=5.5,
            revolutions=0.5,
            delay_ms=100000,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *random_projectiles(
            x=0, y=0,
            amount=300,
            delay_ms=102000,
            speed_min=0.1,
            speed_max=0.40,
            spawn_delay_spread_ms=40,
            warning_ms=500,
            warning_color="#ff6644",
            size=10,
            color="#ff6644",
        ),
        *random_projectiles(
            x=1, y=1,
            amount=300,
            delay_ms=102000,
            speed_min=0.1,
            speed_max=0.40,
            spawn_delay_spread_ms=40,
            warning_ms=500,
            warning_color="#ff6644",
            size=10,
            color="#ff6644",
        ),
        *random_projectiles(
            x=1, y=0,
            amount=450,
            delay_ms=102000,
            speed_min=0.1,
            speed_max=0.40,
            spawn_delay_spread_ms=40,
            warning_ms=500,
            warning_color="#ff6644",
            size=10,
            color="#ff6644",
        ),
        *random_projectiles(
            x=0, y=1,
            amount=450,
            delay_ms=102000,
            speed_min=0.1,
            speed_max=0.40,
            spawn_delay_spread_ms=40,
            warning_ms=500,
            warning_color="#ff6644",
            size=10,
            color="#ff6644",
        ),
        *[atk for i in range(9) for atk in rotating_beams(
            origin_x=PLAYER_X,
            origin_y=PLAYER_Y,
            start_angle=-20.0,
            angle_between=20.0,
            revolutions=0.35,
            delay_ms=(112000 + 1000 * i),
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=500,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        )],
       TextAttack("What?", 0.5, 0.1, 3000, 102000, 32, "#ff0000"),
       TextAttack("How are you still alive?", 0.5, 0.1, 3000, 105000, 32, "#ff0000"),
       TextAttack("I'm starting to run out of assets...", 0.5, 0.1, 3000, 108000, 32, "#ff0000"),
       TextAttack("Uh...", 0.5, 0.1, 3000, 111000, 32, "#ff0000"),
       TextAttack("Pretend you didn't hear that.", 0.5, 0.1, 3000, 114000, 32, "#ff0000"),
       TextAttack("This fight is never going to end, so just give up.", 0.5, 0.1, 3000, 117000, 32, "#ff0000"),
       TextAttack("Right?", 0.5, 0.1, 3000, 120000, 32, "#ff0000"),
        *rotating_beams(
            origin_x=0,
            origin_y=0,
            start_angle=0.0,
            angle_between=5.5,
            revolutions=0.5,
            delay_ms=120500,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=1,
            start_angle=0.0,
            angle_between=5.5,
            revolutions=0.5,
            delay_ms=120500,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=0,
            start_angle=0.0,
            angle_between=5.5,
            revolutions=0.5,
            delay_ms=120500,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=0,
            origin_y=1,
            start_angle=0.0,
            angle_between=5.5,
            revolutions=0.5,
            delay_ms=120500,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *[BeamAttack(position=PLAYER_X, orientation="vertical", warning_ms=1000, duration_ms=250, thickness=40, delay_ms=123000 + (500*i), color_warn="#ff5555", color_beam="#ff0000") for i in range(35)],
        *[BeamAttack(position=PLAYER_Y, orientation="horizontal", warning_ms=1000, duration_ms=250, thickness=40, delay_ms=123000 + (500*i), color_warn="#ff5555", color_beam="#ff0000") for i in range(35)],
        *random_projectiles(
            x=0.5, y=0.5,
            amount=200,
            delay_ms=122500,
            speed_min=0.1,
            speed_max=0.20,
            spawn_delay_spread_ms=80,
            warning_ms=2000,
            warning_color="#ff6644",
            size=10,
            color="#ff6644",
        ),
        *rotating_beams(
            origin_x=0,
            origin_y=0,
            start_angle=0.0,
            angle_between=7,
            revolutions=0.5,
            delay_ms=141000,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=1,
            start_angle=0.0,
            angle_between=7,
            revolutions=0.5,
            delay_ms=141000,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=0,
            start_angle=0.0,
            angle_between=7,
            revolutions=0.5,
            delay_ms=141000,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=0,
            origin_y=1,
            start_angle=0.0,
            angle_between=7,
            revolutions=0.5,
            delay_ms=141000,
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *random_projectiles(
            x=0, y=1,
            amount=120,
            delay_ms=143000,
            speed_min=0.1,
            speed_max=0.20,
            spawn_delay_spread_ms=100,
            warning_ms=1000,
            warning_color="#ff6644",
            size=125,
            color="#ff6644",
            hitbox_shrink=60
        ),
        *random_projectiles(
            x=0, y=0,
            amount=120,
            delay_ms=143000,
            speed_min=0.1,
            speed_max=0.20,
            spawn_delay_spread_ms=100,
            warning_ms=1000,
            warning_color="#ff6644",
            size=125,
            color="#ff6644",
            hitbox_shrink=60
        ),
        *random_projectiles(
            x=1, y=1,
            amount=120,
            delay_ms=143000,
            speed_min=0.1,
            speed_max=0.20,
            spawn_delay_spread_ms=100,
            warning_ms=1000,
            warning_color="#ff6644",
            size=125,
            color="#ff6644",
            hitbox_shrink=60
        ),
        *random_projectiles(
            x=1, y=0,
            amount=120,
            delay_ms=143000,
            speed_min=0.1,
            speed_max=0.20,
            spawn_delay_spread_ms=100,
            warning_ms=1000,
            warning_color="#ff6644",
            size=125,
            color="#ff6644",
            hitbox_shrink=30
        ),
        *rotating_beams(
            origin_x=PLAYER_X,
            origin_y=PLAYER_Y,
            start_angle=0.0,
            angle_between=21,
            revolutions=1,
            delay_ms=143000,
            beam_delay_ms=1000,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=0,
            origin_y=0,
            start_angle=0.0,
            angle_between=7,
            revolutions=0.5,
            delay_ms=161000,
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=1,
            start_angle=0.0,
            angle_between=7,
            revolutions=0.5,
            delay_ms=161000,
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=0,
            start_angle=0.0,
            angle_between=7,
            revolutions=0.5,
            delay_ms=161000,
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=0,
            origin_y=1,
            start_angle=0.0,
            angle_between=7,
            revolutions=0.5,
            delay_ms=161000,
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=0.5,
            origin_y=0.5,
            start_angle=0.0,
            angle_between=6,
            revolutions=2.8,
            delay_ms=163000,
            beam_delay_ms=100,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *[atk for i in range(12) for atk in rotating_beams(
            origin_x=random.choice([0,1]),
            origin_y=random.choice([0,1]),
            start_angle=0.0,
            angle_between=10,
            revolutions=0.5,
            delay_ms=163000+(1500*i),
            beam_delay_ms=30,
            warning_ms=1000,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        )],
        *[CircleAttack(x=PLAYER_X, y=PLAYER_Y,
                       warning_ms=500,
                       duration_ms=500,
                       delay_ms=172000 + (1000 * i),
                       radius=80,
                       color_warn="#ff5555",
                       color_beam="#ff0000") for i in range(9)],
        TextAttack("I... don't have any more projectiles...",  0.5, 0.1, 3000, 163000, 32, "#ff0000"),
        TextAttack("I need to be a bit more creative...",  0.5, 0.1, 3000, 166000, 32, "#ff0000"),
        TextAttack("What if, I rotated the beams on the z-axis?",  0.5, 0.1, 3000, 169000, 32, "#ff0000"),
        *rotating_beams(
            origin_x=0,
            origin_y=0,
            start_angle=0.0,
            angle_between=7,
            revolutions=0.5,
            delay_ms=181000,
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=1,
            start_angle=0.0,
            angle_between=7,
            revolutions=0.5,
            delay_ms=181000,
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=0,
            start_angle=0.0,
            angle_between=7,
            revolutions=0.5,
            delay_ms=181000,
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=0,
            origin_y=1,
            start_angle=0.0,
            angle_between=7,
            revolutions=0.5,
            delay_ms=181000,
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        CircleAttack(x=0.5, y=0.5,
                       warning_ms=1300,
                       duration_ms=38000,
                       delay_ms=181000,
                       radius=200,
                       color_warn="#ff5555",
                       color_beam="#ff0000",
                       hitbox_shrink=10),
       *rotating_beams(
                       origin_x=0.5,
                       origin_y=0.5,
                       start_angle=0.0,
                       angle_between=6,
                       revolutions=6.1,
                       delay_ms=182700,
                       beam_delay_ms=100,
                       warning_ms=1000,
                       duration_ms=450,
                       thickness=40,
                       color_warn="#ff5555",
                       color_beam="#ff0000",
                   ),
        *rotating_beams(origin_x=PLAYER_X, origin_y=PLAYER_Y,
                        delay_ms=182700,
                        start_angle=0.0,
                        angle_between=7,
                        revolutions=7.2,
                        beam_delay_ms=100,
                        warning_ms=500,
                        duration_ms=500,
                        thickness=40,
                        color_warn="#ff5555",
                        color_beam="#ff0000"),
        *rotating_beams(origin_x=PLAYER_X, origin_y=PLAYER_Y,
                        delay_ms=183700,
                        start_angle=0.0,
                        angle_between=7,
                        revolutions=6.8,
                        beam_delay_ms=100,
                        warning_ms=500,
                        duration_ms=500,
                        thickness=40,
                        color_warn="#ff5555",
                        color_beam="#ff0000"),
        *[CircleAttack(x=PLAYER_X, y=PLAYER_Y,
                       warning_ms=1000,
                       duration_ms=1000,
                       delay_ms=182700 + (500*i),
                       radius=100,
                       color_warn="#ff5555",
                       color_beam="#ff0000") for i in range(73)],
        *rotating_beams(origin_x=random.choice([0,1]), origin_y=random.choice([0,1]),
                        delay_ms=191200,
                        start_angle=0.0,
                        angle_between=7,
                        revolutions=0.5,
                        beam_delay_ms=30,
                        warning_ms=500,
                        duration_ms=500,
                        thickness=40,
                        color_warn="#ff5555",
                        color_beam="#ff0000"),
        *rotating_beams(origin_x=random.choice([0,1]), origin_y=random.choice([0,1]),
                        delay_ms=201700,
                        start_angle=0.0,
                        angle_between=7,
                        revolutions=0.5,
                        beam_delay_ms=30,
                        warning_ms=500,
                        duration_ms=500,
                        thickness=40,
                        color_warn="#ff5555",
                        color_beam="#ff0000"),
        *rotating_beams(origin_x=random.choice([0,1]), origin_y=random.choice([0,1]),
                        delay_ms=211700,
                        start_angle=0.0,
                        angle_between=7,
                        revolutions=0.5,
                        beam_delay_ms=30,
                        warning_ms=500,
                        duration_ms=500,
                        thickness=40,
                        color_warn="#ff5555",
                        color_beam="#ff0000"),
                *rotating_beams(
            origin_x=0,
            origin_y=0,
            start_angle=0.0,
            angle_between=5,
            revolutions=0.5,
            delay_ms=221000,
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=1,
            start_angle=0.0,
            angle_between=5,
            revolutions=0.5,
            delay_ms=221000,
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=1,
            origin_y=0,
            start_angle=0.0,
            angle_between=5,
            revolutions=0.5,
            delay_ms=221000,
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=0,
            origin_y=1,
            start_angle=0.0,
            angle_between=5,
            revolutions=0.5,
            delay_ms=221000,
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        TextAttack("It doesn't make any sense.",  0.5, 0.1, 3000, 222000, 32, "#ff0000"),
        TextAttack("You've survived everything I've thrown at you",  0.5, 0.1, 3000, 225000, 32, "#ff0000"),
        TextAttack("I guess I'll just have to use an attack that covers the entire fight.",  0.5, 0.1, 3000, 228000, 32, "#ff0000"),
        TextAttack("???",  0.5, 0.5, 3000, 230000, 32, "#00ff00"),
        CircleAttack(x=0.5, y=0.5,
                       warning_ms=100,
                       duration_ms=30000,
                       delay_ms=233000,
                       radius=200,
                       color_warn="#55ff55",
                       color_beam="#00ff00",
                       hitbox_shrink=-10,
                       inverse=True),
        TextAttack("What?",  0.5, 0.1, 3000, 234000, 32, "#ff0000"),
        TextAttack("Of course someone was helping you...",  0.5, 0.1, 3000, 237000, 32, "#ff0000"),
        TextAttack("I suppose I could use this to my advantage.",  0.5, 0.1, 3000, 240000, 32, "#ff0000"),
        *[atk for i in range(20) for atk in rotating_beams(
            origin_x=0.5,
            origin_y=0.5,
            start_angle=0.0,
            angle_between=30,
            revolutions=0.5,
            delay_ms=243000 + (1000*i),
            beam_delay_ms=30,
            warning_ms=500,
            duration_ms=400,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        )],
        *rotating_beams(
            origin_x=0.5,
            origin_y=0.5,
            start_angle=0.0,
            angle_between=10,
            revolutions=2.5,
            delay_ms=244000,
            beam_delay_ms=200,
            warning_ms=500,
            duration_ms=400,
            thickness=60,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=0.5,
            origin_y=0.5,
            start_angle=0.0,
            angle_between=20,
            revolutions=0.5,
            delay_ms=262000,
            beam_delay_ms=50,
            warning_ms=500,
            duration_ms=400,
            thickness=60,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        TextAttack("It'll be hard to make this work...",  0.5, 0.1, 3000, 245000, 32, "#ff0000"),
        TextAttack("He seems to be preventing me from creating impossible scenarios.",  0.5, 0.1, 3000, 248000, 32, "#ff0000"),
        TextAttack("Huh, looks like there were some projectiles left over after all",  0.5, 0.1, 3000, 251000, 32, "#ff0000"),
        TextAttack("Welp, here goes something.",  0.5, 0.1, 3000, 263000, 32, "#ff0000"),
        *[atk for i in range(18) for atk in random_projectiles(
                x=PLAYER_X, y=PLAYER_Y,
                amount=15,
                delay_ms=264000+(1000*i),
                speed_min=0.1,
                speed_max=0.15,
                spawn_delay_spread_ms=20,
                warning_ms=1000,
                warning_color="#ff6644",
                size=15,
                color="#ff6644",
            )],
        *rotating_beams(origin_x=PLAYER_X, origin_y=PLAYER_Y,
                        delay_ms=264000,
                        start_angle=0.0,
                        angle_between=7,
                        revolutions=3.5,
                        beam_delay_ms=100,
                        warning_ms=500,
                        duration_ms=500,
                        thickness=40,
                        color_warn="#ff5555",
                        color_beam="#ff0000"),
        *[CircleAttack(x=PLAYER_X, y=PLAYER_Y,
                       warning_ms=1000,
                       duration_ms=1000,
                       delay_ms=264000 + (500*i),
                       radius=100,
                       color_warn="#ff5555",
                       color_beam="#ff0000") for i in range(36)],
        *[BeamAttack(origin_x=PLAYER_X, origin_y=PLAYER_Y,
                     angle=random.uniform(10,80),
                     warning_ms=1000,
                     duration_ms=100,
                     delay_ms=264000 + (2000*i),
                     thickness=500,
                     color_warn="#55ff55",
                     color_beam="#00ff00",
                     inverse=True) for i in range(9)],
        *rotating_beams(
            origin_x=0.5,
            origin_y=0.5,
            start_angle=0.0,
            angle_between=10,
            revolutions=3,
            delay_ms=264000,
            beam_delay_ms=175,
            warning_ms=500,
            duration_ms=400,
            thickness=60,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *rotating_beams(
            origin_x=0.5,
            origin_y=0.5,
            start_angle=0.0,
            angle_between=6,
            revolutions=3,
            delay_ms=284000,
            beam_delay_ms=100,
            warning_ms=1000,
            duration_ms=450,
            thickness=40,
            color_warn="#ff5555",
            color_beam="#ff0000",
        ),
        *random_projectiles(
            x=0.5, y=0.5,
            amount=230,
            delay_ms=284000,
            speed_min=0.15,
            speed_max=0.60,
            spawn_delay_spread_ms=80,
            warning_ms=700,
            warning_color="#ff6644",
            size=30,
            color="#ff6644",
        ),
        *rotating_beams(origin_x=PLAYER_X,
                        origin_y=PLAYER_Y,
                        start_angle=0,
                        angle_between=70,
                        revolutions=3,
                        delay_ms=284000,
                        beam_delay_ms=1100,
                        warning_ms=2000,
                        duration_ms=500,
                        hitbox_shrink=6,
                        thickness=20,
                        color_warn="#ff5555",
                        color_beam="#ff0000",),
       CircleAttack(x=0.5, y=0.5,
                       warning_ms=1000,
                       duration_ms=18200,
                       delay_ms=284000,
                       radius=200,
                       color_warn="#ff5555",
                       color_beam="#ff0000",
                       hitbox_shrink=5,
                       inverse=False),
       TextAttack("I don't understand. You survived everything I could throw at you.",  0.5, 0.1, 3000, 304000, 32, "#ff0000"),
       TextAttack("There's no more assets for me to use...",  0.5, 0.1, 3000, 307000, 32, "#ff0000"),
       TextAttack("You actually, beat me?",  0.5, 0.1, 3000, 310000, 32, "#ff0000"),
       TextAttack("I suppose you're looking for some kind of reward...",  0.5, 0.1, 3000, 313000, 32, "#ff0000"),
       TextAttack('There was some kind of "stat" in the files...',  0.5, 0.1, 3000, 316000, 32, "#ff0000"),
       TextAttack("That wasn't meant to be obtainable...",  0.5, 0.1, 3000, 319000, 32, "#ff0000"),
       TextAttack("Fine, you can have 'DENIAL', I guess you deserve it.",  0.5, 0.1, 3000, 322000, 32, "#ff0000"),
       TextAttack("I've gotta run before someone notices I'm here.",  0.5, 0.1, 3000, 325000, 32, "#ff0000"),
       TextAttack("Maybe you aren't as much of an idiot as I thought.",  0.5, 0.1, 3000, 328000, 32, "#ff0000"),
       ]
if __name__ == "__main__":
    app = QApplication(sys.argv)
    #window = BolicalWorld(stat_data={"Stats": {"Graphite": 0, "Tesseract": 0, "Tetra": 0, "Master Tetra": 0}, "Keys": {"Bolical Points": 0, "Sky-High Structuring": False}})
    window = Cutscene([*["Blah"]*20], "green", "black")
    window.show()
    sys.exit(app.exec())
