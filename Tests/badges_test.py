from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
import sys
from Module import GradientLabel, Mantissa
from data import stat_gradients
badge_data = {"Category": {"Badge 1": {"Owned": False, "Display": "Example Badge", "Gradient": "Badges" , "Reqs": {"Cash": 100}, "Consume": True, "Multis": None}, "Badge 1.1": {"Owned": True, "Display": "Tester's Glory", "Gradient": "Testium", "Reqs": {"Testium": 1}, "Consume": False, "Multis": {"Testium": 5}}}, "Category 2": {"Badge 2": {"Owned": True, "Display": "Another Badge", "Gradient": "Totality", "Multis": {"Totality": 3}}, "Badge 2.3": {"Owned": True, "Display": "Another Badge", "Gradient": "Totality", "Multis": {"Totality": 3}}, "Badge 2.2": {"Owned": True, "Display": "Another Badge", "Gradient": "Totality", "Multis": {"Totality": 3}}, "Badge 2.1": {"Owned": True, "Display": "Another Badge", "Gradient": "Totality", "Multis": {"Totality": 3}}, "Badge 2.4": {"Owned": True, "Display": "Another Badge", "Gradient": "Totality", "Multis": {"Totality": 3}}, "Badge 2.5": {"Owned": True, "Display": "Another Badge", "Gradient": "Totality", "Multis": {"Totality": 3}}, "Badge 2.6": {"Owned": True, "Display": "Another Badge", "Gradient": "Totality", "Multis": {"Totality": 3}}, "Badge 2.6": {"Owned": True, "Display": "Another Badge", "Gradient": "Totality", "Multis": {"Totality": 3}}, "Badge 2.7": {"Owned": True, "Display": "Another Badge", "Gradient": "Totality", "Multis": {"Totality": 3}}, "Badge 2.8": {"Owned": True, "Display": "Another Badge", "Gradient": "Totality", "Multis": {"Totality": 3}}, "Badge 2.9": {"Owned": True, "Display": "Another Badge", "Gradient": "Totality", "Multis": {"Totality": 3}}, "Badge 2.10": {"Owned": True, "Display": "Another Badge", "Gradient": "Totality", "Multis": {"Totality": 3}}, "Badge 2.11": {"Owned": True, "Display": "Another Badge", "Gradient": "Totality", "Multis": {"Totality": 3}}, "Badge 2.12": {"Owned": True, "Display": "Another Badge", "Gradient": "Totality", "Multis": {"Totality": 3}}, "Badge 2.13": {"Owned": True, "Display": "Another Badge", "Gradient": "Totality", "Multis": {"Totality": 3}}}}
app = QApplication(sys.argv)
class BadgesWindow(QDialog):
 def __init__(self, badge_data, parent=None):
     super().__init__(parent)
     self.data = badge_data
     self.setMinimumSize(500,500)
     self.setMaximumSize(500,500)
     self.setStyleSheet("background-color: black")
     self.setWindowTitle("World Badges")
     container_layout = QVBoxLayout(self)
     container = QWidget()
     scroll = QScrollArea()
     scroll.setWidgetResizable(True)
     scroll.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
     scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
     central_layout = QHBoxLayout(container)
     layout = QVBoxLayout()
     for cat in self.data.keys():
         category_label = QLabel(cat)
         category_label.setStyleSheet("font-weight: bold; font-size: 24px; margin-top: 8px;")
         layout.addWidget(category_label)
         for id in self.data[cat].keys():
             ref = self.data[cat][id]
             text = f"{ref['Display']}: {'Owned' if ref['Owned'] else 'Not Owned'}"
             button = QPushButton()
             button.clicked.connect(lambda checked, c=cat, i=id: self.multi_edit(c, i))
             button.setStyleSheet("background-color: black")
             button.setFocusPolicy(Qt.NoFocus)
             GradientLabel(text, stat_gradients[ref["Gradient"]]["Colours"], stat_gradients[ref["Gradient"]]["Angle"], parent=button)
             layout.addWidget(button)
     multi_layout = QVBoxLayout()
     self.multiplier_list = QListWidget()
     self.multiplier_list.setFixedWidth(150)
     self.multiplier_list.setStyleSheet('''QListWidget {
         background-color: black;
         }''')
     multiplier_header = QLabel("Stat Multipliers:")
     multiplier_header.setStyleSheet('''QLabel {
         background-color: black;
         }''')
     multi_layout.addWidget(multiplier_header, 1)
     multi_layout.addWidget(self.multiplier_list, 20)
     central_layout.addLayout(layout, 4)
     central_layout.addLayout(multi_layout, 1)
     container.setLayout(central_layout)
     scroll.setWidget(container)
     container_layout.addWidget(scroll)
     self.setLayout(container_layout)
 def multi_edit(self, category, badge):
     self.multiplier_list.clear()
     if self.data[category][badge]["Multis"]:
       for Stat, multi in self.data[category][badge]["Multis"].items():
           if Stat and multi:
             self.multiplier_list.addItem(f"{Stat} x{multi if not isinstance(multi, Mantissa) else multi.to_string()}")
     else:
         self.multiplier_list.addItem("Nothing")
root = BadgesWindow(badge_data)
root.show()
app.exec()