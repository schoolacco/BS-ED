# Builtins/Must haves
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import json
import threading
import math
import os
import ctypes
import random
import sys
import warnings
from pathlib import Path
import colorama
import webbrowser
import re
from Module import Mantissa, find_key_path
from data import abs_stat_info
craftable_items = []
for key, value in abs_stat_info.items():
 for key, value in value.items():
     try:
         value["Recipe"]
         craftable_items.append(key)
     except:
      pass
class CraftingMenu(QDialog):
    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.items = items
        central = QWidget(self)
        self.outer_layout = QVBoxLayout(central)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background-color: #2f2f2f;")
        self.outer_layout.addWidget(self.scroll_area)
        # Content widget inside scroll area
        self.content = QWidget()
        self.content.setStyleSheet("background-color: #2f2f2f;")
        self.grid = QGridLayout(self.content)
        self.grid.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.content)
        # Store references to labels
        self.stat_labels = {}     # (category, stat_name) turns into QLabel
        self.current_row = 0
        self._populate_crafting()
    def _populate_crafting(self):
        col_count = 3
        row = 0
        col = 0
    
        for item in self.items:
            segment = self._create_crafting_segment(item)
            self.grid.addWidget(segment, row, col)
    
            col += 1
            if col >= col_count:
                col = 0
                row += 1
    def _create_crafting_segment(self, item_name):
      segment = QFrame()
      segment.setStyleSheet("""
          QFrame {
              background-color: #3a3a3a;
              border-radius: 8px;
              padding: 8px;
          }
      """)
      layout = QVBoxLayout(segment)
  
      # Title
      title = QLabel(item_name)
      title.setStyleSheet("font-weight: bold; font-size: 14px;")
      layout.addWidget(title)
  
      # Fetch recipe properly
      path = find_key_path(abs_stat_info, item_name)
      category, key = path[0], path[1]
      item_data = abs_stat_info[category][key]
      recipe = item_data["Recipe"]
  
      # Ingredients
      for ingredient, amount in recipe.items():
          if isinstance(amount, Mantissa):
              text = f"{amount.to_string()} {ingredient}"
          else:
              text = f"{amount} {ingredient}"
  
          layout.addWidget(QLabel(text))
      
      qty_layout = QHBoxLayout()

      qty_label = QLabel("Quantity:")
      quantity = QLineEdit()
      quantity.setPlaceholderText("Enter amount...")
      
      qty_layout.addWidget(qty_label)
      qty_layout.addWidget(quantity)
      
      layout.addLayout(qty_layout)

  
      # Craft button (placeholder)
      craft_btn = QPushButton("Craft")
      layout.addWidget(craft_btn)
  
      return segment

app =  QApplication(sys.argv)
root = CraftingMenu(craftable_items)
root.show()
app.exec()