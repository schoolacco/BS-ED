from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from Module import GradientLabel, Mantissa, RotatedLabel
from bsed import cythrex_data, stat_gradients, abs_stat_info, def_stat_increment
import os
import os.path
import random
def build_cythrex_index(stat_info, meta_data):
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

    return index



CYTHREX_INDEX = build_cythrex_index(abs_stat_info, cythrex_data)

def resolve_search(query: str, index: dict):
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

        name_match = any(word in key for word in words)
        tag_match = any(
            word in tag
            for word in words
            for tag in entry["tags"]
        )

        if name_match or tag_match:
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
class BootScreen(QWidget):
    finished = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: black;")

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
class CY47Window(QWidget):
    def __init__(self, stat_info, meta_data):
        super().__init__()
        self.setWindowTitle("CY-47 :: SYSTEM INTERFACE")
        self.resize(1000, 650)
        self.stat_info = stat_info
        self.meta_data = meta_data
        self.stat_list = list(def_stat_increment.keys())
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
        self.stat_name = GradientLabel(stat, stat_gradients.get(stat, stat_gradients["Default"])["Colours"], stat_gradients.get(stat, stat_gradients["Default"])["Angle"], stroke_color=stat_gradients.get(stat, stat_gradients["Default"]).get("S_Colour", None), stroke_width=stat_gradients.get(stat, stat_gradients["Default"]).get("S_Width", None))
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
        image = stat_gradients.get(stat, stat_gradients["Default"]).get("File", None)
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
    
        self.page_container.addLayout(layout)
        self.current_page = layout

    
    def on_search(self):
      query = self.search.text().strip()
  
      if not query:
          self.show_default_page()
          return
  
      results = resolve_search(query, CYTHREX_INDEX)
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
if __name__ == '__main__':
    app = QApplication([])

    boot = BootScreen()
    boot.show()

    def start_main():
        app.main_window = CY47Window(abs_stat_info, cythrex_data)
        app.main_window.show()

    boot.finished.connect(start_main)

    app.exec()

