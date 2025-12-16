from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from Module import GradientLabel, Mantissa
from bsed import cythrex_data, stat_gradients, abs_stat_info
import os
import os.path

def build_cythrex_index(stat_info, meta_data):
    index = {}

    for name, meta in meta_data.items():
        index[name.lower()] = {
            "name": name,
            "tags": [t.lower() for t in meta.get("tags", [])],
        }

    return index


CYTHREX_INDEX = build_cythrex_index(abs_stat_info, cythrex_data)

def resolve_search(query: str, index: dict):
      query = query.strip().lower()
      if not query:
          return []
  
      words = query.split()
      results = []
      seen = set()
  
      # 1. Exact name match
      if query in index:
          results.append(index[query]["name"])
          seen.add(query)
  
      # 2. Tag-based search
      for key, entry in index.items():
          if key in seen:
              continue
  
          if any(word in entry["tags"] for word in words):
              results.append(entry["name"])
              seen.add(key)
  
      return results

def find_key_path(nested_dict, target_key_name, current_path=None):
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
class CY47Window(QWidget):
    def __init__(self, stat_info, meta_data):
        super().__init__()
        self.setWindowTitle("CY-47 :: SYSTEM INTERFACE")
        self.resize(1000, 650)
        self.stat_info = stat_info
        self.meta_data = meta_data
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
        self.stat_name = GradientLabel(stat, stat_gradients[stat]["Colours"], stat_gradients[stat]["Angle"])
        self.stat_name.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.stat_name.setAlignment(Qt.AlignCenter)

        self.right_panel.addWidget(self.stat_name)

        # Image + info row
        mid_row = QHBoxLayout()

        # Left text
        left_info = QVBoxLayout()
        self.stat_type = QLabel(f"Type: {find_key_path(self.stat_info, stat)[0]}")
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
        image = self.meta_data[stat].get("image", None)
        if image == None:
          files = [f for f in os.listdir("Stats") if os.path.isfile(os.path.join("Stats", f))]
          if f"{stat}.webp" in files:
            self.image.setPixmap(QPixmap(f"Stats/{stat}.webp"). scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
          else:
            self.image.setPixmap(QPixmap(f"Stats/Missing.webp"). scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.image.setPixmap(QPixmap(f"Stats/{image}.webp"). scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
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

        self.obtainment_label = QLabel(self.meta_data[stat]["obtainment"])
        self.obtainment_label.setStyleSheet('''QLabel {
            color: green;
            background-color: black;
            }''')

        self.obtainment_layout.addWidget(self.obtainment_label)

        self.right_panel.addWidget(self.obtainment)
        
        self.left_panel = QVBoxLayout()
        
        # Left: multipliers
        self.multiplier_list = QListWidget()
        self.multiplier_list.setFixedWidth(260)
        if self.stat_info[find_key_path(self.stat_info, stat)[0]][stat]["Multis"]:
          for Stat, multi in self.stat_info[find_key_path(self.stat_info, stat)[0]][stat]["Multis"].items():
              if Stat and multi:
                self.multiplier_list.addItem(f"{Stat} x{multi if not isinstance(multi, Mantissa) else multi.to_string()}")
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
    
        self.root.addLayout(layout)
        self.current_page = layout

    
    def on_search(self):
      query = self.search.text().strip()
  
      if not query:
          self.show_default_page()
          return
  
      results = resolve_search(query, CYTHREX_INDEX)
  
      if results:
          if len(results) == 1:
              self.generate_content(results[0])
          else:
              self.show_results_page(results)
      else:
          self.show_no_results_page(query)

    def show_results_page(self, results):
      self.clear_page()
  
      layout = QVBoxLayout()
  
      header = QLabel(f"Search Results ({len(results)})")
      header.setFont(QFont("Segoe UI", 16, QFont.Bold))
      header.setStyleSheet("color: green;")
      layout.addWidget(header)
  
      list_widget = QListWidget()
      list_widget.setStyleSheet("color: green; background-color: black;")
  
      for name in results:
          item = QListWidgetItem(name)
          list_widget.addItem(item)
  
      # --- CLICK / ENTER BEHAVIOR ---
      list_widget.itemActivated.connect(
          lambda item: self.generate_content(item.text())
      )
  
      layout.addWidget(list_widget)
  
      self.page_container.addLayout(layout)
      self.current_page = layout
if __name__ == '__main__':
    app = QApplication([])
    win = CY47Window(abs_stat_info, cythrex_data)
    win.show()
    app.exec()
