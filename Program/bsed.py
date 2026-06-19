# Builtins/Must haves
from __future__ import annotations
from PySide6.QtWidgets import QDialog, QScrollArea, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton, QLineEdit, QGridLayout, QMessageBox, QApplication, QComboBox, QCompleter, QMainWindow, QGroupBox, QDoubleSpinBox, QSizePolicy, QLayout
from PySide6.QtCore import QTimer, QObject, QEvent, QSortFilterProxyModel, QSize, QUrl
from PySide6.QtGui import QIcon, Qt, QPixmap, QCloseEvent, QPainter, QColor, QHideEvent, QShowEvent, QPaintEvent
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
import PySide6.QtSql #Future use
import ast
import json
import math
import ctypes
import random
import sys
import warnings
from pathlib import Path
import colorama
import webbrowser
import os
import weakref
from typing import Union, Optional
import hmac
from Module import Realm, GradientLabel, BootScreen, CY47Window, BolicalWorld, BadgesWindow, CollapsibleSection, World, Cutscene, find_key_path, multi_func, AuthWindow
from geode import *
from db import update_save, get_account, supabase
from data import abs_stat_info, stat_gradients, cythrex_data, craftable_items, badge_data, def_upgrades, global_path_reference, def_stat_increment
from session import generate_signature, validate_session
try: #Environment handling
  from dotenv import load_dotenv
except ImportError:
    pass
Numeric = Union[int, float, Mantissa]
sys.set_int_max_str_digits(2147483647)
#TODO:
# Offline geode rolls - possible
# Greed puzzle - possible
# ARG/Malware puzzle - probably not
# - Denial puzzle - actively happening
# Revamp wiki pages for Moonbase and Nostalgia World before implementing into program - Moonbase fully implemented, Nostalgia World may happen, but is unlikely
# Implement Secluded Oasis - nvm the pages are really empty
# Implement BS:ED X (?) - definitely not happening
os.environ["QT_LOGGING_RULES"] = "qt.multimedia.ffmpeg*=false" #Stops console flooding with info about the music changing
warnings.filterwarnings("ignore")
user = validate_session()
if os.name == 'nt':
    app_id = 'BSED.but.bad.1.4' 
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id) #Taskbar icon for windows
print("Loading...")
progression_lvl = 0
if 'load_dotenv' in dir():
    load_dotenv(f"{global_path_reference}/Program/bsed.env", override=True)
    debug = ast.literal_eval(os.getenv("DEBUG"))
else:
    debug = False
upgrades = def_upgrades
def_secrets = {
    "Darkmatter_1": False,
    "Darkmatter_2": False,
    "Darkmatter_3": False,
    "Darkmatter_4": False,
    "Darkmatter_5": False,
    "Galaxite_1": False,
    "Galaxite_2": False,
    "Galaxite_3": False,
    "Bolical Points": 0,
    "Sky-High Structuring": False,
}
secrets = def_secrets
stat_increment = def_stat_increment
stat_increment["Keys"] = secrets
e_event = True
cash_type = "Cash"
multi_type = "Multiplier"
rebirth_type = "Rebirths"
gem_type = "Gems"
e_type = "Event Power"
reset_key = "Main Progression"
area = "Spawn"
world = "Buttonia"
upgrade_ref = ""
m_logic = True
main_window = None
boot = None
for item in list(stat_increment["Stats"].keys()):
    if item not in list(cythrex_data.keys()):
      cythrex_data[item] = {"tags": ["BS:ED", "Stats"], "lore": "TBA", "obtainment": "TBA"}
MANTISSA_THRESHOLD = 1e300
luck, crit_luck, geode_speed, bulk_roll = 1, 1, 1, 1
voltaic_radar = False
db = supabase
class UpgradeMenu(QDialog):
        instances = weakref.WeakSet()
        def __init__(self, save_data: dict, parent: Optional[QObject]=None) -> UpgradeMenu:
            global world
            super().__init__(parent)
            for instance in self.instances:
             instance.close()
            self.instances.clear()
            self.instances.add(self)
    
            self.save_data = save_data
    
            self.setWindowTitle("Boosts")
            self.setWindowIcon(QIcon(f"{global_path_reference}/icon.ico"))
            self.setMinimumSize(400, 500)
            self.setStyleSheet("background-color: #212121; color: white; padding: 1px; border: 1px solid white")
            # Scroll setup
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setStyleSheet("background-color: #2f2f2f;")
    
            container = QWidget()
            self.layout = QVBoxLayout(container)
    
            # Generate upgrade rows
            for upgrade_id, info in upgrades[world].items():
                self.add_upgrade_row(upgrade_id, info)
            scroll.setWidget(container)
    
            #layout
            outer = QVBoxLayout(self)
            outer.addWidget(scroll)
            self.instances.add(self)
    
        def add_upgrade_row(self, upgrade_id: str, info: dict):
            level = self.save_data[world][upgrade_id].get("current_lvl", 0)
            cost = upgrade_cost(info, level)
    
            row = QFrame()
            row_layout = QHBoxLayout(row)
            cost_text = f"Cost: {cost:.2e} {gem_type.title()}" if cost > 1e6 else f"Cost: {cost} {gem_type.title()}"
            cost_text = cost_text if level < info['max_level'] else "Cost: MAX"
            name_label = QLabel(f"{info['name']}")
            level_label = QLabel(f"Level: {level}/{info['max_level']}" if level < info['max_level'] else f"Level: MAX ({level}/{info['max_level']})")
            cost_label = QLabel(cost_text)
    
            buy_btn = QPushButton("Buy")
            
            buy_btn.setObjectName(info["difficulty"])
            
            buy_btn.setStyleSheet(stylesheet)
    
            if level >= info["max_level"]:
                buy_btn.setDisabled(True)
    
            # Connect button
            buy_btn.clicked.connect(
                lambda _, uid=upgrade_id, inf=info,
                ll=level_label, cl=cost_label, b=buy_btn:
                self.buy_upgrade(uid, inf, ll, cl, b)
            )
    
            # Add widgets
            row_layout.addWidget(name_label)
            row_layout.addWidget(level_label)
            row_layout.addWidget(cost_label)
            row_layout.addWidget(buy_btn)
    
            self.layout.addWidget(row)
    
        def buy_upgrade(self, upgrade_id: str, info: dict, level_label: QLabel, cost_label: QLabel, buy_button: QPushButton):
            global world
            level = self.save_data[world][upgrade_id].get("current_lvl", 0)
    
            # Maxed?
            if level >= info["max_level"]:
                return
    
            cost = upgrade_cost(info, level)
    
            # Check if player has enough gems
            if stat_increment["Stats"][gem_type] < cost:
                return
    
            # Apply purchase
            stat_increment["Stats"][gem_type] -= cost
            level += 1
            self.save_data[world][upgrade_id]["current_lvl"] = level
    
            # Update UI
            level_label.setText(f"Level: {level}/{info['max_level']}" if level < info['max_level'] else f"Level: MAX ({level}/{info['max_level']})")
            if level >= info["max_level"]:
                buy_button.setDisabled(True)
                cost_text= "Cost: MAX"
                cost_label.setText(cost_text)
            else:
                cost = upgrade_cost(info, level)
                cost_text = f"Cost: {cost:.2e} {gem_type}" if cost > 1e6 else f"Cost: {cost} {gem_type}"
                cost_label.setText(cost_text)
        @classmethod
        def close_all(cls):
            for window in cls.instances:
             window.close()
            cls.instances.clear()
class ControlPanel(QDialog):
        instances = weakref.WeakSet()
        def __init__(self, parent: Optional[QObject]=None) -> ControlPanel:
            super().__init__(parent)
            for instance in self.instances:
                instance.close()
            self.instances.clear()
            self.instances.add(self)
            self.setWindowTitle("Choose location...")
            self.x_entry = QLineEdit()
            self.y_entry = QLineEdit()
            self.x_entry.setPlaceholderText("Insert x-coordinate...")
            self.y_entry.setPlaceholderText("Insert y-coordinate...")
            self.go_button = QPushButton(text="Go!")
            self.x_entry.setStyleSheet(stylesheet)
            self.y_entry.setStyleSheet(stylesheet)
            self.go_button.setStyleSheet(stylesheet)
            self.go_button.clicked.connect(self.move)
            
            layout = QVBoxLayout(self)
            self.content = QWidget()
            self.content.setStyleSheet(stylesheet)
            self.grid = QGridLayout(self.content)
            self.grid.setAlignment(Qt.AlignTop)
            self.grid.addWidget(self.x_entry, 1, 1)
            self.grid.addWidget(QLabel(text="   "), 1, 2)
            self.grid.addWidget(self.y_entry, 1, 3)
            self.grid.addWidget(self.go_button, 2, 2)
            
            layout.addWidget(self.content)
        def move(self):
            try:
             x = float(self.x_entry.text())
             y = float(self.y_entry.text())
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "Please insert valid coordinates.")
                return
            if x == y == 0:
                load_check("ET")
            elif (x, y) == (1935.5286, 1769.196):
                load_check("ETR")
            elif (x, y) == (472.739, 1407.0948):
                load_check("ETE")
            elif (x, y) == (260.9568, 105.5747):
                load_check("ETS")
            elif (x, y) == (230.6099, 369.4198):
                load_check("ETD")
            elif (x, y) == (154.7922, 923.732):
                load_check("ETSL")
            elif (x, y) == (723.3226, 1851.4675):
                load_check("ETDG")
            elif (x, y) == (154.7922, 923.732):
                load_check("ETSG")
            elif (x, y) == (371.111, 1954.4598):
                load_check("ETIG")
            elif (x, y) == (3040.8689, 7290.8997):
                load_check("ETSL")
            elif (x, y) == (701236212.05, 329417941.475): #Future co-ords for Darkmatter
                load_check("ETD")
            else:
                load_check("ETD")
            self.close()
# Source - https://stackoverflow.com/a // stackoverflow's attribution copy+paste is clearly so effective as to fail to copy their own link
# Posted by luke, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-30, License - CC BY-SA 3.0
FILE_ATTRIBUTE_HIDDEN = 0x02
FILE_ATTRIBUTE_SYSTEM = 0x04
def write_hidden(file_name: str, data: str):
    # Find user's Documents folder
    docs = Path.home() / "Documents"

    # For *nix, prefix with .
    final_name = file_name
    if os.name != 'nt':
        final_name = "." + file_name #Linux stuff I believe

    file_path = docs / final_name

    # Write the file normally
    with open(file_path, 'w') as f:
        f.write(data)

    # Windows: set Hidden attribute
    if os.name == 'nt':
        ret = ctypes.windll.kernel32.SetFileAttributesW(
            str(file_path),
            FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM
        )
        if not ret:
            raise ctypes.WinError()
#It should be noted that the code has been marginally modified from the original version
#End of atrributions stuff
def blinded():
    if not os.path.exists(Path.home()/"Documents"/"toodarktosee"):
      print("Traceback (most recent call last):")
      print('  File "Module.py", line 128, in <module>')
      print("    test_function()")
      print("RuntimeError: Unexpected internal failure")
      print(colorama.Fore.BLACK + "YOU'RE JUST TOO BLIND TO SEE IT.")
      write_hidden(Path.home()/"Documents"/"toodarktosee", "Are you not afraid of what cannot be seen? \n You search for the impossible, what has never been found \n Yet you wish to harness its energy, the energy of DARKMATTER.")
      root.close()
def secret_input(input: str):
    global area, sec_input
    if input == "Totality" and os.path.exists(Path.home()/"Documents"/"toodarktosee"):
        print("You're on the right track!")
        secrets["Darkmatter_1"] = True
        print(colorama.Fore.BLACK, "RGltZW5zaW9uIGJyZWFr", colorama.Fore.RESET)
    if area == "AT":
      if input == "God of Miners" and secrets["Darkmatter_1"] and secrets["Darkmatter_2"]:
          secrets["Darkmatter_3"] = True
          print(colorama.Fore.BLACK, "Perhaps you are capable of seeing in the dark. Nethertheless the end is nigh. Corrupt thy soul, plague it with sin, and perhaps once more you may be capable of opening your eyes.", colorama.Fore.RESET)
    elif area == "WF":
      if input == "Andromeda":
          print("You feel as if the wormhole was beginning to reopen")
          secrets["Galaxite_1"] = True
      elif input == "Cassiopeia":
          print("You feel the fabric of spacetime shift")
          secrets["Galaxite_2"] = True
      elif input == "Defractured":
          print("You feel the wormhole begin to stabilise")
          secrets["Galaxite_3"] = True
      elif input == "Endless Night" and secrets["Darkmatter_1"]:
          secrets["Darkmatter_2"] = True
          print(colorama.Fore.BLACK, "Looking deeper... deeper... perhaps you look too deep. Find me elsewhere, in another medium, find the chaos in the foundation of knowledge in the wake of the creator.", colorama.Fore.RESET)
      if all((secrets["Galaxite_1"], secrets["Galaxite_2"], secrets["Galaxite_3"], stat_increment["Stats"]["Galaxite"] == 0)):
          print("An exit has opened, congratulations on your escape.")
          stat_increment["Stats"]["Galaxite"] = 1
    elif area == "R34L1TY":
        if input == "R3AL1TY H4S N3VER SH1N3D TH1S M8CH":
            stat_increment["Stats"]["TRU3_W0RLD"] = 1
    sec_input.clear()
def Geode_roll(btn: QPushButton, geode: Geode, luck: int=1, geode_speed: int=1, bulk_roll: int=1):
    global stat_increment
    local_crit = crit_luck + upgrades[world]["crit_luck"]["effect"]*upgrades[world]["crit_luck"]["current_lvl"]
    local_luck = luck + upgrades[world]["geode_luck"]["effect"]*upgrades[world]["geode_luck"]["current_lvl"] + upgrades[world]["super_lucky"]["effect"]*upgrades[world]["super_lucky"]["current_lvl"]
    btn.setEnabled(False)
    stat_increment = geode.open(stat_increment, local_luck, bulk_roll, local_crit)
    QTimer.singleShot(int(geode_speed*1000), lambda: btn.setEnabled(True))
def load_check(id: Optional[str]=None):
    global stat_increment, container, scroll_area, content, layout, area
    result = Realm.load_realm(stat_increment, id)
    if result:
      container.deleteLater()  # remove old scroll area
      container, scroll_area, content, stat_increment = result
      layout.addWidget(container, 2, 1, 9, 9)
      area = id
def edit_user(*args):
    global user
    user = validate_session()
def load_world(req: Numeric, unit: str, world_instance: World):
    global stat_increment, container, scroll_area, container, content, layout, cash_type, multi_type, rebirth_type, gem_type, e_event, e_type, reset_key, world, music, m_logic, upgrade_ref, user
    amount = stat_increment["Stats"][unit]
    req = float_to_mantissa(req) if isinstance(amount, Mantissa) else req
    if amount >= req:
      if progression_lvl == 4 and not validate_session() and world_instance.area == "S":
          auth = AuthWindow("Register", root)
          auth.registered.connect(edit_user)
          auth.exec()
          stat_increment = (lambda l=Load(user): l if l != def_stat_increment else stat_increment)()
      container.deleteLater()
      initial_area, cash_type, multi_type, rebirth_type, gem_type, event_power, reset_key, m_logic, world, upgrade_ref, path = world_instance.load_world()
      container, scroll_area, content = initial_area.create_scrollable_area()
      layout.addWidget(container, 2, 1, 9, 9)
      if event_power:
          e_type = event_power
      e_event = event_power
      label_helper()
      music_manager = container.parent().parent().music_manager
      path = f"{global_path_reference}/Program/Music/{world}" if Path(f"{global_path_reference}/Program/Music/{world}").exists() else f"{global_path_reference}/Program/Music/Buttonia"
      music_manager.path = path
      music_manager.music_list = os.listdir(path)
      music_manager.stop()
      music_manager.play_random()
      UpgradeMenu.close_all()
def float_to_mantissa(value: float) -> Mantissa:
      """Converts a float or int into a Mantissa representation."""
      if isinstance(value, Mantissa):
          return value
      if value == 0:
          return Mantissa(0, 0)
      exponent = int(math.floor(math.log10(abs(value))))
      mantissa = value / (10 ** exponent)
      return Mantissa(mantissa, exponent)
def upgrade_cost(info: dict, level: int) -> int:
    base = info["base_cost"]
    growth = info["cost_growth"]
    return int(base * (growth ** level))
def serialize(obj: Mantissa) -> dict:
    if isinstance(obj, Mantissa):
        return obj.to_dict()
    elif isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    else:
        return obj
# Recursive deserialization
def deserialize(obj: dict) -> Mantissa:
    if isinstance(obj, dict):
        if obj.get("__mantissa__"):
            return Mantissa.from_dict(obj)
        return {k: deserialize(v) for k, v in obj.items()}
    else:
        return obj
def Old_Load() -> dict:
       '''Load your data from your savefile'''
       global upgrades, secrets, progression_lvl
       if os.path.exists(f"{global_path_reference}/savefile.json"): # If you have saved before
        with open(f"{global_path_reference}/savefile.json", "r")  as file: # Read the file
          try:
            data = deserialize(json.load(file)) # Attempt to return backup data
            signature = data["signature"]
            if signature:
                del data["signature"]
            if not hmac.compare_digest(generate_signature(json.dumps(serialize(data), sort_keys=True)).strip(), str(signature).strip()):
               raise ValueError("You DARE Tamper with MY savefile??????")
            try:
              for category in upgrades.keys():
                  for upgrade in upgrades[category].keys():
                    if upgrades[category].get(upgrade):
                      upgrades[category][upgrade]["current_lvl"]= data["Upgrades"].get(upgrade, 0)
            except:
                upgrades = def_upgrades
            try:
                secrets = data["Keys"]
            except:
                secrets = def_secrets
            for item in def_stat_increment["Stats"].keys(): 
                data["Stats"].setdefault(item,0)
            for key in list(data["Stats"].keys()):
                if key not in list(def_stat_increment["Stats"].keys()):
                    del data["Stats"][key]
            if "Badges" not in data.keys():
                data["Badges"] = {}
            for category in badge_data:
                for item in badge_data[category].keys():
                  data["Badges"].setdefault(item,False)
            progression_lvl = data.get("Progression", 0)
            return data
          except json.JSONDecodeError: # If file is corrupted
             print("Savefile is corrupted, attempting to load backup if it exists...")
             if os.path.exists("backup.json"): # If you have a backup
                with open("backup.json", "r") as file: # Read the backup file
                   try:
                      data = deserialize(json.load(file)) # Attempt to return backup data
                      try:
                        upgrades = data["Upgrades"]
                      except:
                          upgrades = def_upgrades
                      for item in def_stat_increment["Stats"].keys():
                          data["Stats"].setdefault(item, 0)
                      return data
                   except json.JSONDecodeError: # If corrupted
                      print("Backup file is also corrupted.")
                      return def_stat_increment
             else:
              print("Backup file does not exist.")
              return def_stat_increment
       else:
          print("You have never saved before.")
          return def_stat_increment # Return your empty collection
def Load(username: str = user):
    global upgrades, secrets, def_stat_increment, badge_data, progression_lvl
    if db:
        try:
            row = get_account(username)
            if not row:
                return Old_Load()
            save_blob = row[0].get("save_blob")

            if not save_blob:
                return def_stat_increment

            data =  deserialize(json.loads(save_blob))
            try:
              for category in upgrades.keys():
                  for upgrade in upgrades[category].keys():
                    if upgrades[category].get(upgrade):
                      upgrades[category][upgrade]["current_lvl"]= data["Upgrades"].get(upgrade, 0)
            except:
                upgrades = def_upgrades
            try:
                secrets = data["Keys"]
            except:
                secrets = def_secrets
            for item in def_stat_increment["Stats"].keys(): 
                data["Stats"].setdefault(item,0)
            for key in list(data["Stats"].keys()):
                if key not in list(def_stat_increment["Stats"].keys()):
                    del data["Stats"][key]
            if "Badges" not in data.keys():
                data["Badges"] = {}
            for category in badge_data:
                for item in badge_data[category].keys():
                  data["Badges"].setdefault(item,False)
            progression_lvl = data.get("Progression", 0)
            return data
        except Exception as e:
            print(f"DB load failed ({e}), loading local save...")
            return Old_Load()

    return Old_Load()
def Save(username: Optional[str], collection: dict, upgrades: dict, secrets: dict, attempt=0):
    global db
    if progression_lvl > 4:
      print(f"Saving... (attempt {attempt + 1}/5)")
      
      def local_save():
          try:
              upgrades_list = []
  
              for category in upgrades:
                  for upgrade in upgrades[category]:
                      upgrades_list.append(
                          frozenset([
                              upgrade,
                              upgrades[category][upgrade]["current_lvl"]
                          ])
                      )
  
              upgrades_list = set(upgrades_list)
              upgrades_list = [
                  sorted(list(item), key=lambda x: (isinstance(x, int), x))
                  for item in upgrades_list
              ]
  
              collection["Upgrades"] = {
                  u[0]: u[1] for u in upgrades_list
              }
  
              collection["Keys"] = secrets
              collection["signature"] = generate_signature(json.dumps(serialize(collection), sort_keys=True))
              with open("savefile.json", "w") as f:
                  json.dump(serialize(collection), f)
              del collection["signature"]
  
          except Exception as e:
              print("Local save failed:", e)
      local_save()
      if not db:
          local_save()
          return
      try:
          upgrades_list = []
  
          for category in upgrades:
              for upgrade in upgrades[category]:
                  upgrades_list.append(frozenset([upgrade, upgrades[category][upgrade]["current_lvl"]]))
  
          upgrades_list = set(upgrades_list)
          upgrades_list =[sorted(list(item), key=lambda x: (isinstance(x, int), x)) for item in upgrades_list]
  
          collection["Upgrades"] = {u[0]: u[1] for u in upgrades_list}
  
          collection["Keys"] = secrets
          
          collection["Progression"] = progression_lvl
  
          save_blob = json.dumps(serialize(collection))
  
          cash = collection["Stats"].get("Cash", 0)
          capsuled = collection["Stats"].get("Capsuled Singularity", 0)
  
          cash_mantissa, cash_exponent = (lambda c=float_to_mantissa(cash): (int(c.num), int(c.exp)))()
          cap_mantissa, cap_exponent = (lambda c=float_to_mantissa(capsuled): (int(c.num), int(c.exp)))()
  
          update_save(
              username=username,
              save_blob=save_blob,
              cash_mantissa=cash_mantissa,
              cash_exponent=cash_exponent,
              capsuled_singularity_mantissa=cap_mantissa,
              capsuled_singularity_exponent=cap_exponent
          )
  
          print("Cloud save successful.")
          return
  
      except Exception as e:
          print(f"Cloud save failed: {e}")
  
          if attempt >= 4:
              db = False
              local_save()
              return
          QTimer.singleShot(2000, lambda: Save(username, collection, upgrades, secrets, attempt + 1) )
def calculate_multi(unit: str) -> Mantissa:
    """Calculates total multiplier for a given unit, supporting Mantissa instances."""
    global stat_increment, crit_luck, cash_type, multi_type, rebirth_type
    local_crit = crit_luck + upgrades[world].get("crit_luck", {"effect": 0})["effect"]*upgrades[world].get("crit_luck", {"current_lvl": 0})["current_lvl"]
    total = Mantissa(1, 0)  # Start as 1 in Mantissa form
    keys = list(abs_stat_info.keys())
    for key in keys:
      if not (stat_increment["Stats"]["C0RR8PT10N"] < 2 and stat_increment["Stats"]["C0RR8PT10N"] > 0.1 and key not in ("Main Progression", "Mastery")):
        stat_list = list(abs_stat_info[key].keys())
        for item in stat_list:
            try:
              amount = stat_increment["Stats"].get(item, 0)
              multis = abs_stat_info[key][item].get("Multis")
            except AttributeError:
                pass
            if multis is None:
              multis = {}
    
            multiplier = multis.get(unit)
            if multiplier is None:
                continue  # skip if this stat does not affect the unit
            multiplier_2 = multis.get(unit+"_2", 0)
            if isinstance(multiplier, (int, float)):
                multiplier = float_to_mantissa(multiplier)
            if isinstance(multiplier_2, (int, float)):
                multiplier_2 = float_to_mantissa(multiplier_2)
            amount_m = amount if isinstance(amount, Mantissa) else float_to_mantissa(amount)
            if amount_m.num == 0:
                continue
            multi_2 = multiplier_2 * amount_m
            if multi_2.num == 0:
                multi_2 = Mantissa(1,0)
            total *=  (multiplier * amount_m * multi_2)
        if key in ("Geode", "Afterlife Domain (Geode)"):
            for g_key in abs_stat_info[key]:
                stat_list = list(abs_stat_info[key][g_key].keys())
                for item in stat_list:
                    try:
                      amount = stat_increment["Stats"].get(item, 0)
                      multis = abs_stat_info[key][g_key][item].get("Multis")
                    except AttributeError:
                        pass
                    if multis is None:
                      multis = {}
            
                    multiplier = multis.get(unit)
                    if multiplier is None:
                        continue  # skip if this stat does not affect the unit
                    multiplier_2 = multis.get(unit+"_2", 0)
                    if isinstance(multiplier, (int, float)):
                        multiplier = float_to_mantissa(multiplier)
                    if isinstance(multiplier_2, (int, float)):
                       multiplier_2 = float_to_mantissa(multiplier_2)
                    amount_m = amount if isinstance(amount, Mantissa) else float_to_mantissa(amount)
                    if amount_m.num == 0:
                        continue
                    multi_2 = multiplier_2 * amount_m
                    if multi_2.num == 0:
                        multi_2 = Mantissa(1,0)
                    total *= (multiplier * amount_m * multi_2)
    for dict in badge_data.values():
        badge_list = list(dict.keys())
        for item in badge_list:
          try:
            applicable = stat_increment["Badges"].get(item, False)
            multis = dict[item].get("Multis", {})
          except AttributeError:
              pass
          if multis is None:
            multis = {}
          multiplier = multis.get(unit)
          if multiplier is None:
              continue  # skip if this badge does not affect the unit
          if isinstance(multiplier, (int, float)):
              multiplier = float_to_mantissa(multiplier)
          total *=  multiplier if applicable else Mantissa(1,0)
    # Ensure we don't return zero
    if total.num == 0:
        return Mantissa(1, 0)

    if total.exp < math.log(MANTISSA_THRESHOLD, 10):
        total = round(total.to_float(), 2)
        total = float_to_mantissa(total)
    total *= 2 if random.randint(1,int(500//local_crit)) == 1 else 1
    if unit == cash_type:
        total /= 2
    return total
def cash_increase():
    global stat_increment, cash_l, cash_type, multi_type

    # Base multiplier
    multiplier_value = stat_increment["Stats"][multi_type]
    if isinstance(multiplier_value, (int, float)):
        multiplier_value = max(multiplier_value, 1)
        multiplier_m = float_to_mantissa(multiplier_value)
    else:
        multiplier_m = multiplier_value

    # Extra multipliers from other stats
    multi = calculate_multi(cash_type)
    multi *= 1+(max(1,upgrades[world][upgrade_ref+"cash_multi"]["current_lvl"]*upgrades[world][upgrade_ref+"cash_multi"]["effect"])*max(1,upgrades[world].get("cash_multi_2", {"current_lvl": 0})["current_lvl"]*upgrades[world].get("cash_multi_2", {"effect": 0})["effect"])) if not isinstance(multi, Mantissa) else float_to_mantissa(1+(max(1,upgrades[world][upgrade_ref+"cash_multi"]["current_lvl"]*upgrades[world][upgrade_ref+"cash_multi"]["effect"])*max(1,upgrades[world].get("cash_multi_2", {"current_lvl": 0})["current_lvl"]*upgrades[world].get("cash_multi_2", {"effect": 0})["effect"])))
    # Compute approximate float multiplier
    approx_multiplier = multiplier_m.to_float() if hasattr(multiplier_m, "to_float") else float(multiplier_m)

    # Compute delay and speed ratio
    base_delay = 250
    if m_logic:
      base_delay /= max(1,upgrades[world].get("cash_speed", {"current_lvl": 0})["current_lvl"])
      if not isinstance(approx_multiplier, Mantissa):
        delay = max(1, int(math.ceil(base_delay / approx_multiplier)))
      else:
        delay = 1
    else:
        delay = base_delay
    # Cap at 250× speed, convert overflow into extra cash
    if delay <= 1:
        # If we're at minimum delay, cash scales instead
        cash_scaling = approx_multiplier / (base_delay) if not isinstance(approx_multiplier, Mantissa) else approx_multiplier / float_to_mantissa(base_delay)
    else:
        cash_scaling = 1

    # Increment cash
    cash_scaling = float_to_mantissa(cash_scaling) if not isinstance(cash_scaling, Mantissa) else cash_scaling
    cash_increment = Mantissa(1, 0) * multi * cash_scaling
    if upgrades[world].get("lucky_draw_multi"):
      cash_increment *= float_to_mantissa(1+upgrades[world]["lucky_draw_multi"]["effect"]*upgrades[world]["lucky_draw_multi"]["current_lvl"]) if random.random() <= upgrades[world]["lucky_draw"]["effect"]*upgrades[world]["lucky_draw"]["current_lvl"] else Mantissa(1,0)
    if isinstance(stat_increment["Stats"][cash_type], Mantissa):
        stat_increment["Stats"][cash_type] += cash_increment
    else:
        try:
          stat_increment['Stats'][cash_type] += cash_increment.to_float()
          stat_increment['Stats'][cash_type] = round(stat_increment["Stats"][cash_type], 2)
        except TypeError:
          stat_increment['Stats'][cash_type] = float_to_mantissa(stat_increment['Stats'][cash_type])
          stat_increment["Stats"][cash_type] += cash_increment
    # Update label
    val = stat_increment["Stats"][cash_type]
    label_helper()
    QTimer.singleShot(delay, cash_increase)
def gem_increase():
    global stat_increment, gem_type
    stat_increment["Stats"][gem_type] += (1+upgrades[world][upgrade_ref+"gem_timer_amount"]["current_lvl"]*upgrades[world][upgrade_ref+"gem_timer_amount"]["effect"])
    if upgrades[world][upgrade_ref+"gem_speed"]["current_lvl"] == 0:
        period = 60000
    else:
        period = 60000//(upgrades[world][upgrade_ref+"gem_speed"]["effect"]*upgrades[world][upgrade_ref+"gem_speed"]["current_lvl"])
    QTimer.singleShot(period, gem_increase)
def event_increase():
    global stat_increment, e_event, e_type
    if e_event:
      stat_increment["Stats"][e_type] += (1+upgrades[world]["event_timer_amount"]["current_lvl"]*upgrades[world]["event_timer_amount"]["effect"])
      if upgrades[world]["event_speed"]["current_lvl"] == 0:
          period = 60000
      else:
          period = 60000//(upgrades[world]["event_speed"]["effect"]*upgrades[world]["event_speed"]["current_lvl"])
      QTimer.singleShot(period, event_increase)
def cost_button(unit: str, cost: Numeric, unit_2: str, receive: Numeric):
    global stat_increment

    value = stat_increment["Stats"][unit]

    if isinstance(value, Mantissa) and not isinstance(cost, Mantissa):
        cost = float_to_mantissa(cost)

    # Check if the player can afford it
    if value >= cost:
        # Deduct cost
        stat_increment["Stats"][unit] -= cost
        # Calculate the increment (reward)
        Multi = calculate_multi(unit_2)
        if isinstance(Multi, Mantissa):
             receive = float_to_mantissa(receive)
        increment = Multi*receive
        # Add the increment
        if not isinstance(stat_increment["Stats"][unit_2], Mantissa) and increment.exp < math.log(MANTISSA_THRESHOLD, 10):
            increment = increment.to_float()
        if isinstance(increment, Mantissa) and not isinstance(stat_increment["Stats"][unit_2], Mantissa):
          stat_increment["Stats"][unit_2] = float_to_mantissa(stat_increment["Stats"][unit_2])
        stat_increment["Stats"][unit_2] += increment
        # Update labels
        label_helper()

        stat_increment["Stats"]["Buttons Pressed"] += 1
def reset_button(cost: Numeric, unit: str, reward: Numeric, unit_2: str):
    global stat_increment, reset_key

    current_value = stat_increment["Stats"][unit]
    stat_list = list(abs_stat_info[reset_key].keys())
    if isinstance(current_value, Mantissa) and not isinstance(cost, Mantissa):
        cost = float_to_mantissa(cost)
    if not isinstance(current_value, Mantissa) and isinstance(cost, Mantissa):
        current_value = float_to_mantissa(current_value)
    if current_value >= cost:
        # Reset all lower-tier stats before unit_2
        for i in range(stat_list.index(unit_2)):
            stat_increment["Stats"][stat_list[i]] = 0

        multi = calculate_multi(unit_2)
        if multi.exp < math.log(MANTISSA_THRESHOLD,10):
            multi = multi.to_float()
            if multi * reward < reward:
                multi += 1
            multi = float_to_mantissa(multi)
        reward_m = float_to_mantissa(reward) * multi

        if not isinstance(reward_m, Mantissa):
            reward_m = float_to_mantissa(reward_m)

        if isinstance(reward_m, Mantissa):
            value = stat_increment["Stats"][unit_2]
            value= float_to_mantissa(value)
            value += reward_m
            value = value.to_float() if value.exp < math.log(MANTISSA_THRESHOLD, 10) else value
            stat_increment["Stats"][unit_2] = value
        label_helper()
        stat_increment["Stats"]["Buttons Pressed"] += 1
def reset_button_special(cost: Numeric, unit: str, reward: Numeric, unit_2: str, resets: list=[]):
    global stat_increment
    current_value = stat_increment["Stats"][unit]
    if isinstance(current_value, Mantissa) and not isinstance(cost, Mantissa):
        cost = float_to_mantissa(cost)
    if not isinstance(current_value, Mantissa) and isinstance(cost, Mantissa):
        current_value = float_to_mantissa(current_value)
    if current_value >= cost:
        # Reset all lower-tier stats before unit_2
        for i in range(len(resets)):
            stat_increment["Stats"][resets[i]] = 0

        multi = calculate_multi(unit_2)
        if multi.exp < math.log(MANTISSA_THRESHOLD,10):
            multi = multi.to_float()
            if multi * reward < reward:
                multi += 1
            multi = float_to_mantissa(multi)
        reward_m = float_to_mantissa(reward) * multi

        if not isinstance(reward_m, Mantissa):
            reward_m = float_to_mantissa(reward_m)

        if isinstance(reward_m, Mantissa):
            value = stat_increment["Stats"][unit_2]
            value= float_to_mantissa(value)
            value += reward_m
            value = value.to_float() if value.exp < math.log(MANTISSA_THRESHOLD, 10) else value
            stat_increment["Stats"][unit_2] = value
        label_helper()
        stat_increment["Stats"]["Buttons Pressed"] += 1
def recovery_button_set(req: Numeric, unit: str, Set: Numeric, unit_2: str):
    global stat_increment
    amount = stat_increment["Stats"][unit]
    if isinstance(amount, Mantissa) and not isinstance(req, Mantissa):
        req = float_to_mantissa(req)
    if not isinstance(amount, Mantissa) and isinstance(req, Mantissa):
        amount = float_to_mantissa(amount)
    if amount >= req:
        if stat_increment["Stats"][unit_2] < Set:
          stat_increment["Stats"][unit_2] = Set
          label_helper()
    else:
     pass
def recovery_button_fetch(req: Numeric, unit: str, recovery: Numeric, unit_2: str):
    global stat_increment
    amount = stat_increment["Stats"][unit]
    if isinstance(amount, Mantissa) and not isinstance(req, Mantissa):
        req = float_to_mantissa(req)
    if not isinstance(amount, Mantissa) and isinstance(req, Mantissa):
        amount = float_to_mantissa(amount)
    if amount >= req:
      multi = calculate_multi(unit_2)
      multi = multi.to_float() if isinstance(multi, Mantissa) else multi
      if multi == 0:
          multi = 1
      recovery = float_to_mantissa(recovery)
      multi = float_to_mantissa(multi)
      amount = float_to_mantissa(amount)
      amount += recovery*multi
      amount = amount.to_float() if amount.exp < math.log10(MANTISSA_THRESHOLD) else amount
      if isinstance(amount, Mantissa):
          stat_increment["Stats"][unit_2] = float_to_mantissa(stat_increment["Stats"][unit_2])
      stat_increment["Stats"][unit_2] += amount
      label_helper()
    else:
     pass
def world_badge(badge_id: str, category: str):
    global stat_increment
    badge_ref = badge_data[category][badge_id]
    reqs = badge_ref["Reqs"]
    units = list(reqs.keys())
    req = list(reqs.values())
    req_check = []
    for i in range(len(units)):
        value = stat_increment["Stats"][units[i]]
        req_check.append(float_to_mantissa(req[i]) <= float_to_mantissa(value))
    if all(req_check):
        if badge_ref["Consume"] and not stat_increment["Badges"][badge_id]:
          for i in range(len(units)):
            stat_increment["Stats"][units[i]] -= req[i]
        stat_increment["Badges"][badge_id] = True
        if BadgesWindow.instances:
            list(BadgesWindow.instances)[len(BadgesWindow.instances)-1].update_badges()
    label_helper()
def label_helper():
    global stat_increment, cash_l, multi_l, re_l, cash_type, multi_type, rebirth_type
    cash_val = round(stat_increment["Stats"][cash_type], 6)
    cash_text = cash_val.to_string() if isinstance(cash_val, Mantissa) else cash_val
    cash_l.setText(f"{cash_type}: {cash_text}")
    
    multi_val = round(stat_increment["Stats"][multi_type], 6)
    multi_text = multi_val.to_string() if isinstance(multi_val, Mantissa) else multi_val
    multi_l.setText(f"{multi_type}: {multi_text}")
    
    rebirth_val = round(stat_increment["Stats"][rebirth_type], 6)
    rebirth_text = rebirth_val.to_string() if isinstance(rebirth_val, Mantissa) else rebirth_val
    re_l.setText(f"{rebirth_type}: {rebirth_text}")
def image_load(path: str):
    path = os.path.abspath(path)
    webbrowser.open(f"file://{path}")
def cythrex_boot(parent: Optional[QObject]=None):
    global main_window, boot, progression_lvl
    if progression_lvl >= 3:
      wl = None if progression_lvl >= 5 else list(abs_stat_info["Pre-existence"].keys())
      bl = None if progression_lvl < 5 or progression_lvl >= 7 else list(abs_stat_info["Pre-existence"].keys())
      window_visibility = True
      try:
          if not main_window.isVisible():
              pass
          else:
              window_visibility = False
      except AttributeError:
          window_visibility = True
      if boot == None and window_visibility:
        boot = BootScreen(parent)
        boot.show()
        main_window = None
        def start_main():
          global main_window, boot
          if main_window == None:
            main_window = CY47Window(abs_stat_info, cythrex_data, list(def_stat_increment.keys()), stat_gradients, parent, wl, bl)
            main_window.show()
          else:
              main_window.show_default_page()
              main_window.search.clear()
              if not main_window.isVisible():
                  main_window.show()
              else:
                  main_window.raise_()
                  main_window.activateWindow()
          boot = None
        def reset():
              global boot, main_window
              boot = None
              main_window = None
        boot.finished.connect(start_main)
        boot.closed.connect(reset)
    else:
          QMessageBox.warning(parent, "Error", "Accessed Denied")
def graphite_puzzle(parent: Optional[QObject]=None, req: Optional[dict]=None):
    if req:
     if stat_increment["Stats"][req[1]] >= req[0]:
         return
    puzzle = BolicalWorld(stat_increment, parent)
    puzzle.show()
def sloth(parent: QObject=None, time: int=3000, req: Optional[dict]=None):
    if req:
      if stat_increment["Stats"][req[1]] >= req[0]:
          return
    puzzle = Sloth(time, parent)
    if parent:
        parent.sloth = puzzle
        parent.input_watch = InputWatch(parent.sloth)
        QApplication.instance().installEventFilter(parent.input_watch)
    puzzle.show()
def gluttony_check(button: QPushButton):
    global stat_increment
    if len(button.parent().children()) == 12:
        if stat_increment["Stats"]["Gluttony"] < 1:
          stat_increment["Stats"]["Gluttony"] = 1
def on_victory():
    val = stat_increment["Stats"]["DENIAL"]
    stat_increment["Stats"]["DENIAL"] = 1 if val < 1 else val
    root.close()
def boss_fight_check(amount: Numeric, unit: str):
    return
    if stat_increment["Stats"][unit] >= amount:
        #fight = BossFight(parent=root, attacks=attacks, end_ms=344000, end_function=on_victory, start_ms=0)
        #fight.exec()
        root.close()
def craft(stat: str, amount: Numeric):
    if amount == None or amount < 1:
        return None
    key_1 = find_key_path(abs_stat_info,stat)[0]
    recipe = abs_stat_info[key_1][stat]["Recipe"] #recipe = dict
    if stat_increment["Stats"][stat] >= abs_stat_info[key_1][stat].get("max_amount", math.inf):
        return None
    for item, amounts in recipe.items():
        amounts_m = float_to_mantissa(amounts)
        amounts_m *= amount
        amounts = amounts_m.to_float()
        if stat_increment["Stats"][item] < amounts:
            return None #Invalid
    for item, amounts in recipe.items():
        amounts_m = float_to_mantissa(amounts)
        amounts_m *= amount
        amounts = amounts_m.to_float()
        stat_increment["Stats"][item] -= amounts
    temp = float_to_mantissa(stat_increment["Stats"][stat])
    temp += amount
    stat_increment["Stats"][stat] = temp.to_float()
def open_control_panel(parent: Optional[QObject]=None) -> QObject:
    win = ControlPanel(parent)
    win.show()
def string_to_num(string:str) -> Numeric:
    try:
          value = float(string)
    except ValueError:
        try:
          value = int(string)
        except ValueError:
          return None
    if value < 2e9:
        value = int(value)
    if value == math.inf:
        value = Mantissa.from_string(string)
    return value
def cutscene(text: list, text_color: str, bg: str, overlay: bool=False, parent:Optional[QObject]=None):
    window = Cutscene(text, text_color, bg, overlay, parent)
    window.exec()
def progression_increment():
    global progression_lvl
    progression_lvl += 1
    if progression_lvl in (5,7):
        root.stat_window.rebuild()
class InputWatch(QObject):
    def __init__(self, obj):
        super().__init__()
        self.object = obj
    def eventFilter(self, obj, event):
        try:
          if not self.object.completed:
            if not self.object.isVisible():
                return False
            if event.type() in (QEvent.MouseButtonPress, QEvent.MouseButtonRelease, QEvent.MouseMove, QEvent.Wheel, QEvent.KeyPress, QEvent.KeyRelease):
                self.object._violate()
          else:
              try:
                self.object.deleteLater()
                self.deleteLater()
              except RuntimeError:
                  pass
          return False
        except RuntimeError:
            pass
class ExtendedComboBox(QComboBox):
    def __init__(self, parent=None):
        super(ExtendedComboBox, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)

        # add a filter model to filter matching items
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        # add a completer, which uses the filter model
        self.completer = QCompleter(self.pFilterModel, self)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        # connect signals
        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)


    # on selection of an item from the completer, select the corresponding item from combobox 
    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)


    # on model change, update the models of the filter and completer as well 
    def setModel(self, model):
        super(ExtendedComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)


    # on model column change, update the model column of the filter and completer as well
    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(ExtendedComboBox, self).setModelColumn(column)
#Source - https://stackoverflow.com/questions/4827207/how-do-i-filter-the-pyqt-qcombobox-items-based-on-the-text-input
#Written by community member: Tamas Haver
#Minor modifications have been made to adapt it to PySide6
if __name__ == "__main__":
  app = QApplication(sys.argv)
  class StatMenu(QMainWindow):
    def __init__(self, parent: Optional[QObject]=None) -> StatMenu:
        super().__init__(parent)

        self.setWindowTitle("Stats Menu")
        self.setStyleSheet("background-color: #2f2f2f; color: white;")
        self.resize(600, 750)

        self.stat_labels = {} # Dictionary reference of all stat labels
        self.icon_cache = {} # Dictionary reference for all icons, helps reduce load times
        self.hidden_geode_stats = {} # Geode stats that are currently not being displayed
        self.geode_layouts = {} # Layouts for the geodes

        # Cache file list for quick reference
        self.files = set(os.listdir(f"{global_path_reference}/Program/Stats"))

        central = QWidget(self)
        self.setCentralWidget(central)

        outer_layout = QVBoxLayout(central)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        outer_layout.addWidget(self.scroll_area)

        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setAlignment(Qt.AlignTop)

        self.scroll_area.setWidget(self.content)

        # Build sections
        self._build_sections()

        # Update timer
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.update_stats(stat_increment)) # Timer periodically updates stat values
    def _build_sections(self):
      for category, stats in abs_stat_info.items():
          if category in ("Geode", "Afterlife Domain (Geode)") and progression_lvl >= 5:
              section = CollapsibleSection(category, lambda layout, s=stats, c=category: self._build_geodes(layout, s, c))
          else:
              if (progression_lvl >= 5 and category != "Pre-existence") or ((progression_lvl < 5 or progression_lvl >= 7) and category == "Pre-existence"):
                section = CollapsibleSection(category, lambda layout, s=stats, c=category: self._build_stats(layout, s, c))
              else:
                  section = None
          if section:
            self.content_layout.addWidget(section)
    def _build_geodes(self, layout: QLayout, stats: dict, category: str):
      for geode, geode_stats in stats.items():
  
          def make_builder(gs=geode_stats, c=category, g=geode):
              return lambda l: self._build_geode_stats(l, gs, c, g)
  
          geode_section = CollapsibleSection(geode, make_builder())
          layout.addWidget(geode_section)
    def _build_geode_stats(self, layout: QLayout, geode_stats: dict, category: str, geode: str):
      key = (category, geode)
  
      self.hidden_geode_stats[key] = set()
      self.geode_layouts[key] = layout
  
      for stat_name in geode_stats.keys():
          value = stat_increment["Stats"].get(stat_name, 0)
  
          if value > 0:
              row = self._create_stat_row(category, stat_name)
              layout.addWidget(row)
          else:
              self.hidden_geode_stats[key].add(stat_name)
    def _build_stats(self, layout: QLayout, stats: dict, category: str):
      for stat_name in stats.keys():
          row = self._create_stat_row(category, stat_name)
          layout.addWidget(row)
    def _create_stat_row(self, category: str, stat_name: str) -> QWidget:
      container = QWidget()
      row = QHBoxLayout(container)
  
      #icon
      image_label = QLabel()
      image_label.setFixedSize(40, 40)
  
      if stat_name in self.icon_cache:
          pix = self.icon_cache[stat_name]
      else:
          if f"{stat_name}.webp" in self.files:
              path = f"{global_path_reference}/Program/Stats/{stat_name}.webp"
          else:
              path = f"{global_path_reference}/Program/Stats/{stat_gradients.get(stat_name, {}).get('File', 'Missing')}.webp"
  
          pix = QPixmap(path).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
          self.icon_cache[stat_name] = pix
  
      image_label.setPixmap(pix)
  
      #name
      gradient_data = stat_gradients.get(stat_name, stat_gradients["Default"])
      name_label = GradientLabel(
          stat_name,
          gradient_data["Colours"],
          gradient_data["Angle"],
          stroke_color=gradient_data.get("S_Colour"),
          stroke_width=gradient_data.get("S_Width", 0)
      )
  
      #value
      value_label = QLabel("0")
      value_label.setAlignment(Qt.AlignRight)
  
      row.addWidget(image_label)
      row.addWidget(name_label)
      row.addStretch()
      row.addWidget(value_label)
  
      self.stat_labels[(category, stat_name)] = value_label
  
      return container
    def _get_insert_index(self, category: str, geode: str, stat_name: str) -> int:
      full_order = list(abs_stat_info[category][geode].keys())
  
      target_index = full_order.index(stat_name)
  
      # Count how many visible stats come before it
      visible_before = 0
  
      for i in range(target_index):
          stat = full_order[i]
  
          if stat not in self.hidden_geode_stats[(category, geode)]:
              visible_before += 1
  
      return visible_before
    def update_stats(self, stat_increment: dict):
        stats = stat_increment["Stats"]
    
        for (category, stat_name), label in list(self.stat_labels.items()):
            value = round(stats.get(stat_name, 0), 6)
    
            if isinstance(value, Mantissa):
                text = value.to_string()
            else:
                text = str(value)
    
            label.setText(text)
            
        for (category, geode), hidden_stats in list(self.hidden_geode_stats.items()):
          layout = self.geode_layouts.get((category, geode))
  
          if not layout:
              continue  # section not opened yet
  
          to_remove = []
  
          for stat_name in hidden_stats:
              value = stats.get(stat_name, 0)
  
              if value > 0:
                  # Create and insert new row
                  row = self._create_stat_row(category, stat_name)

                  insert_index = self._get_insert_index(category, geode, stat_name)
                  
                  layout.insertWidget(insert_index, row)
  
                  to_remove.append(stat_name)
  
          # Remove revealed stats from hidden set
          for stat_name in to_remove:
              hidden_stats.remove(stat_name)
    def rebuild(self):
        children = (lambda layout=self.content_layout: [layout.itemAt(i).widget() for i in range(layout.count()) if layout.itemAt(i).widget()])()
        for child in children:
            child.deleteLater()
        self._build_sections()
    def showEvent(self, event: QShowEvent):
        self.timer.start(50)
        super().showEvent(event)
    def hideEvent(self, event: QHideEvent):
        self.timer.stop()
        super().hideEvent(event)
  class MusicManager:
      def __init__(self, offset_ms=0): #The improved music manager which may or may not be in the main program by the time you're reading this
          self.audio_output = QAudioOutput()
          self.player = QMediaPlayer()
          self.player.setAudioOutput(self.audio_output)
          self.offset = offset_ms
          self.music_list = []
          self.path = f"{global_path_reference}/Program/Music/Archive"
          self.music_list = os.listdir(self.path)
          self._pending_offset = False
          self.stop_perm = False
          self.player.mediaStatusChanged.connect(self._handle_status)
  
      def play_random(self):
          if not self.music_list:
              return
          self.player.stop()
          self._pending_offset = self.offset > 0
          song = random.choice(self.music_list)
          self.player.setSource(QUrl.fromLocalFile(f"{self.path}/{song}"))
          self.player.play()
  
      def _handle_status(self, status: QMediaPlayer.MediaStatus):
          if status == QMediaPlayer.MediaStatus.LoadedMedia or self._pending_offset:
              self._pending_offset = False
              self.player.setPosition(self.offset)
          elif status == QMediaPlayer.MediaStatus.EndOfMedia:
              if not self.stop_perm:
                self.play_random()
  
      def stop(self):
          self._pending_offset = False
          self.player.stop()
  class Window(QMainWindow):
      def __init__(self) -> Window:
          super().__init__()
          self.stat_window = StatMenu(self)
          self.music_manager = MusicManager()
          self.music_manager.music_list = os.listdir(os.path.abspath(f"{global_path_reference}/Program/Music/{world}"))
          self.music_manager.path =  os.path.abspath(f"{global_path_reference}/Program/Music/{world}")
          self.setWindowIcon(QIcon(os.path.abspath(f"{global_path_reference}/Program/Starglass.png")))
          self.stat_window.hide()
          self.timer = QTimer()
          self.timer.timeout.connect(lambda: Save(user, stat_increment, upgrades, secrets))
          self.timer.start(300000)
      def closeEvent(self, event: QCloseEvent):
        Save(user, stat_increment, upgrades, secrets)
        event.accept()
      def open_stats(self):
        if self.stat_window.isVisible():
            self.stat_window.hide()
        else:
            self.stat_window.show()
            self.stat_window.raise_()
            self.stat_window.activateWindow()
  class AdminPanel(QDialog):
    def __init__(self, parent: Optional[QObject], player_state: dict) -> AdminPanel:
        super().__init__(parent)
        self.player = player_state

        self.setWindowTitle("ADMIN / DEVELOPER PANEL")
        self.setFixedSize(360, 260)
        self.setStyleSheet("background-color: black; color: green;")

        layout = QVBoxLayout(self)

        globals_box = QGroupBox("Global Variables")
        globals_box.setStyleSheet("QGroupBox { color: #00ff00; }")
        g_layout = QHBoxLayout(globals_box)

        self.luck_input = QDoubleSpinBox()
        self.luck_input.setRange(0.0, 1e15)
        self.luck_input.setDecimals(4)
        self.luck_input.setValue(luck)
        self.luck_input.textChanged.connect(self.set_luck)
        
        self.roll_input = QDoubleSpinBox()
        self.roll_input.setRange(0.0, 1e15)
        self.roll_input.setDecimals(4)
        self.roll_input.setValue(bulk_roll)
        self.roll_input.textChanged.connect(self.set_bulk_roll)

        g_layout.addWidget(QLabel("Luck:"))
        g_layout.addWidget(self.luck_input)
        g_layout.addWidget(QLabel("Bulk Roll:"))
        g_layout.addWidget(self.roll_input)
        
        layout.addWidget(globals_box)

        stat_box = QGroupBox("Stat Editor")
        stat_box.setStyleSheet("QGroupBox { color: #00ff00; }")
        s_layout = QGridLayout(stat_box)

        self.stat_select = ExtendedComboBox()
        self.stat_select.addItems(sorted(self.player["Stats"].keys()))
        
        self.stat_value = QLineEdit()
        self.stat_value.setPlaceholderText("Enter float/integer value")

        set_abs = QPushButton("Set")
        add = QPushButton("Add")
        sub = QPushButton("Subtract")

        set_abs.clicked.connect(self.set_stat)
        add.clicked.connect(lambda: self.modify_stat(+1))
        sub.clicked.connect(lambda: self.modify_stat(-1))

        s_layout.addWidget(QLabel("Stat:"), 0, 0)
        s_layout.addWidget(self.stat_select, 0, 1)
        s_layout.addWidget(QLabel("Value:"), 1, 0)
        s_layout.addWidget(self.stat_value, 1, 1)

        s_layout.addWidget(set_abs, 2, 0)
        s_layout.addWidget(add, 2, 1)
        s_layout.addWidget(sub, 3, 1)

        layout.addWidget(stat_box)

        close = QPushButton("Close")
        close.clicked.connect(self.close)
        layout.addWidget(close)
    def set_luck(self):
        global luck
        value = self.get_value(self.luck_input)
        if value is None:
            return
        luck = value
    def set_bulk_roll(self):
        global bulk_roll
        value = self.get_value(self.roll_input)
        value = int(value)
        if value is None:
          return
        bulk_roll = value
    def get_value(self, input: QLineEdit) -> None|Numeric:
      try:
          value = int(input.text())
      except ValueError:
          try:
            value = float(input.text())
          except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Enter a valid float or integer.")
            return None
      if value == math.inf:
          value = Mantissa.from_string(input.text())
      if value == None:
          QMessageBox.warning(self, "Invalid Input", "Enter a valid float or integer.")
      if isinstance(value, int) and value > 1e13:
          value = float(value)
      return value
    def set_stat(self):
      value = self.get_value(self.stat_value)
      if value is None:
          return
      stat = self.stat_select.currentText()
      self.player["Stats"][stat] = value
    def modify_stat(self, direction: int):
        stat = self.stat_select.currentText()
        self.player["Stats"][stat] += self.get_value(self.stat_value) * direction
  class Sloth(QDialog):
      instances = weakref.WeakSet()
      def __init__(self, time: int=3000, parent: Optional[QObject]=None) -> Sloth:
          super().__init__(parent)
          for instance in self.instances:
            instance.close()
          self.instances.clear()
          self.instances.add(self)
          self.setWindowFlags(Qt.Window|Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.WindowTransparentForInput)
          self.setAttribute(Qt.WA_TranslucentBackground)
          self.setGeometry(self.screen().geometry())
          self.timer = QTimer(self)
          self.timer.setInterval(10)
          self.timer.timeout.connect(self._tick)
          self.fade_timer = QTimer(self)
          self.fade_timer.setInterval(30)
          self.fade_timer.timeout.connect(self._fade_step)
          self.progress = 0.0
          self.step = 100/time
          self.failed = False
          self.completed = False
          self.raise_()
          self.activateWindow()
          self.showFullScreen()
          self.timer.start()
      def _tick(self):
       if self.failed:
           return
       self.progress += self.step
       if self.progress >= 100:
           self.progress = 100
           self.timer.stop()
           self.complete()
           return
       self.update()
      def paintEvent(self, event: QPaintEvent):
          painter = QPainter(self)
          painter.setRenderHint(QPainter.Antialiasing)
          opacity = (self.progress / 100.0)**1.2
          colour = QColor(85,169,253, int(255*opacity))
          painter.fillRect(self.rect(), colour)
      def _violate(self):
          if self.failed:
              return
          self.failed = True
          self.fade_timer.start()
      def _fade_step(self):
          self.progress -= 5
          if self.progress <= 0:
              self.progress = 0
              self.failed = False
              self.fade_timer.stop()
          self.update()
      def complete(self):
          global stat_increment
          if stat_increment["Stats"]["Sloth"] < 1:
            stat_increment["Stats"]["Sloth"] = 1
          self.completed = True
      def focusOutEvent(self, event):
          self._violate()
          super().focusOutEvent(event)
      def changeEvent(self, event):
          if event.type() == QEvent.WindowStateChange:
              self._violate()
          super().changeEvent(event)   
      def resizeEvent(self, event):
          self._violate()
          super().resizeEvent(event)
  class CraftingMenu(QDialog):
    instances = weakref.WeakSet()
    def __init__(self, items: list, parent: Optional[QObject]=None) -> CraftingMenu:
        super().__init__(parent)
        for instance in self.instances:
            instance.close()
        self.instances.clear()
        self.instances.add(self)
        self.setMinimumSize(600, 400)
        self.setMaximumSize(600, 400)
        self.items = items
        central = QWidget(self)
        self.setWindowTitle("Crafting")
        self.outer_layout = QVBoxLayout(central)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(stylesheet)
        self.outer_layout.addWidget(self.scroll_area)
        # Content widget inside scroll area
        self.content = QWidget()
        self.content.setStyleSheet(stylesheet)
        self.grid = QGridLayout(self.content)
        self.grid.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.content)
        self.lbl_lists = []
        self._populate_crafting()
    def _populate_crafting(self):
        col_count = 3
        row = 0
        col = 0
        if progression_lvl < 5:
            del self.items[2:]
        elif 7 > progression_lvl >= 5:
            del self.items[:-(len(self.items)-2)]
        for item in self.items:
            segment = self._create_crafting_segment(item)
            self.grid.addWidget(segment, row, col)
    
            col += 1
            if col >= col_count:
                col = 0
                row += 1
    def _create_crafting_segment(self, item_name: str):
      temp_list = []
      segment = QFrame()
      segment.setStyleSheet(stylesheet)
      layout = QVBoxLayout(segment)
  
      # Title
      title = QLabel(item_name)
      title.setStyleSheet("font-weight: bold; font-size: 14px;")
      layout.addWidget(title)
  
      # Fetch recip
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
  
          lbl = QLabel(text)
          layout.addWidget(lbl)
          temp_list.append(lbl)
      
      qty_layout = QHBoxLayout()

      qty_label = QLabel("Quantity:")
      quantity = QLineEdit()
      quantity.setPlaceholderText("Enter amount...")
      quantity.textChanged.connect(self._amount_change)
      quantity.setObjectName(item_name)
      temp_list.append(quantity)
      
      qty_layout.addWidget(qty_label)
      qty_layout.addWidget(quantity)
      
      layout.addLayout(qty_layout)
      craft_btn = QPushButton("Craft")
      craft_btn.clicked.connect(lambda: craft(item_name, self.get_value(quantity)))
      layout.addWidget(craft_btn)
      self.lbl_lists.append(temp_list)
      return segment
    def _amount_change(self):
        inpt = self.sender() #I definitely would've used this with the Geode buttons if I knew this was a thing...
        item_name = inpt.objectName()
        path = find_key_path(abs_stat_info, item_name)
        category, key = path[0], path[1]
        item_data = abs_stat_info[category][key]
        recipe = item_data["Recipe"]
        value = self.get_value(inpt)
        if value == None or value < 1:
            return
        value_m = float_to_mantissa(value)
        lbl_list = None
        for item in self.lbl_lists:
            lbl_list = item if inpt in item else lbl_list
        i = 0
        for ingredient, amount in recipe.items():
          if isinstance(amount, Mantissa):
              text = f"{amount.to_string()} {ingredient}"
          else:
              text = f"{amount} {ingredient}"
          lbl_list[i].setText(text)
          i += 1
        texts = [item.text() for item in lbl_list if isinstance(item, QLabel)]
        n = 0
        for item in texts:
            temp = item.split(" ")
            val = float_to_mantissa(string_to_num(temp[0]))
            val *= value_m
            if val.exp < math.log(MANTISSA_THRESHOLD, 10):
              val = val.to_float()
            text = f"{val.to_string() if isinstance(val, Mantissa) else val}"
            for i in range(len(temp)-1):
                text += f" {temp[i+1]}"
            texts[n] = text
            n += 1
        for i in range(len(texts)):
            lbl_list[i].setText(texts[i])
    def get_value(self, input: QLineEdit):
      return string_to_num(input.text())
  print("Fetching savefile...")
  stat_increment = (lambda l=Load(): l if l != None else stat_increment)()
  root = Window()
  root.setWindowTitle("BS:ED but bad")
  cash_l, multi_l, re_l = QLabel(), QLabel(), QLabel()
  root.setWindowTitle("BS:ED but bad")
  root.setMinimumSize(QSize(100,100))
  root.setWindowIcon(QIcon(f"{global_path_reference}/Program/icon.ico"))
  layout = QGridLayout()
  central = QWidget()
  central.setLayout(layout)
  label_helper()
#----------- AREAS --------------
  Realm(root, { #Spawn
      "Multiplier": [
          ("12 Cash: 1 Multiplier", lambda: cost_button("Cash",12,"Multiplier", 1)),
          ("50 Cash: 3 Multiplier", lambda: cost_button("Cash",50,"Multiplier", 3)),
          ("100 Cash: 5 Multiplier", lambda: cost_button("Cash",100,"Multiplier", 5)),
          ("500 Cash: 10 Multiplier", lambda: cost_button("Cash",500,"Multiplier", 10)),
          ("10k Cash: 45 Multiplier", lambda: cost_button("Cash",1e4,"Multiplier", 45)),
          ("75k Cash: 100 Multiplier", lambda: cost_button("Cash",7.5e4,"Multiplier", 100)),
          ("1M Cash: 300 Multiplier", lambda: cost_button("Cash",1e6,"Multiplier", 300)),
          ("30M Cash: 500 Multiplier", lambda: cost_button("Cash",3e7,"Multiplier", 500)),
          ("100M Cash: 1k Multiplier", lambda: cost_button("Cash",1e8,"Multiplier", 1e3)),
          ("1B Cash: 5k Multiplier", lambda: cost_button("Cash",1e9,"Multiplier", 5e3)),
          ("5B Cash: 20k Multiplier", lambda: cost_button("Cash",5e9,"Multiplier", 2e4)),
          ("30B Cash: 60k Multiplier", lambda: cost_button("Cash",3e10,"Multiplier", 6e4)),
          ("200B Cash: 120k Multiplier", lambda: cost_button("Cash",2e11,"Multiplier", 1.2e5)),
          ("700B Cash: 300k Multiplier", lambda: cost_button("Cash",7e11,"Multiplier", 3e5)),
          ("3T Cash: 1M Multiplier", lambda: cost_button("Cash",3e12,"Multiplier", 1e6)),
          ("10T Cash: 4M Multiplier", lambda: cost_button("Cash",1e13,"Multiplier", 4e6)),
          ("50T Cash: 10M Multiplier", lambda: cost_button("Cash",5e13,"Multiplier", 1e7)),
          ("120T Cash: 50M Multiplier", lambda: cost_button("Cash",1.2e14,"Multiplier", 5e7)),
          ("400T Cash: 80M Multiplier", lambda: cost_button("Cash",4e14,"Multiplier", 8e7)),
          ("1Qd Cash: 200M Multiplier", lambda: cost_button("Cash",1e15,"Multiplier", 2e8)),
          ("5Qd Cash: 1B Multiplier", lambda: cost_button("Cash",5e15,"Multiplier", 1e9)),
          ("25Qd Cash: 4B Multiplier", lambda: cost_button("Cash",2.5e16,"Multiplier", 4e9)),
          ("100Qd Cash: 10B Multiplier", lambda: cost_button("Cash",1e17,"Multiplier", 1e10))
      ],
      "Rebirths": [
          ("2k Multiplier: 1 Rebirths", lambda: reset_button(2000,"Multiplier",1, "Rebirths")),
          ("15k Multiplier: 5 Rebirths", lambda: reset_button(15000,"Multiplier",5, "Rebirths")),
          ("600k Multiplier: 23 Rebirths", lambda: reset_button(6e5,"Multiplier",23, "Rebirths")),
          ("12M Multiplier: 69 Rebirths", lambda: reset_button(1.2e7,"Multiplier",69, "Rebirths")),
          ("700M Multiplier: 272 Rebirths", lambda: reset_button(7e8,"Multiplier",272, "Rebirths")),
          ("3B Multiplier: 1k Rebirths", lambda: reset_button(3e9,"Multiplier",1000, "Rebirths")),
          ("15B Multiplier: 5k Rebirths", lambda: reset_button(1.5e10,"Multiplier",5000, "Rebirths")),
          ("50B Multiplier: 20k Rebirths", lambda: reset_button(5e10,"Multiplier",20000, "Rebirths")),
          ("600B Multiplier: 50k Rebirths", lambda: reset_button(6e11,"Multiplier",5e4, "Rebirths")),
          ("1T Multiplier: 100k Rebirths", lambda: reset_button(1e12,"Multiplier",1e5, "Rebirths")),
          ("75T Multiplier: 500k Rebirths", lambda: reset_button(7.5e13,"Multiplier",5e5, "Rebirths")),
          ("400T Multiplier: 1M Rebirths", lambda: reset_button(4e14,"Multiplier",1e6, "Rebirths")),
          ("2Qd Multiplier: 6M Rebirths", lambda: reset_button(2e15,"Multiplier",6e6, "Rebirths")),
          ("15Qd Multiplier: 30M Rebirths", lambda: reset_button(1.5e16,"Multiplier",3e7, "Rebirths")),
          ("50Qd Multiplier: 100M Rebirths", lambda: reset_button(5e16,"Multiplier",1e8, "Rebirths")),
      ],
      "Stone": [
          ("30k Rebirths: 1 Stone", lambda: reset_button(30000, "Rebirths", 1, "Stone")),
          ("30M Rebirths: 3 Stone", lambda: reset_button(3e7, "Rebirths", 3, "Stone")),
          ("600M Rebirths: 6 Stone", lambda: reset_button(6e8, "Rebirths", 6, "Stone")),
      ],
      "Recovery": [
         ("15 Stone: 15Qn Cash (Sets)", lambda: recovery_button_set(15, "Stone", 5e19, "Cash")),
         ("7 Iron: 1e40 Cash (Sets)", lambda: recovery_button_set(7, "Iron", 1e40, "Cash")),
         ("1 Gold: 6e41 Multiplier (Fetch)", lambda: recovery_button_fetch(1, "Gold", 6e41, "Multiplier")),
         ("2 Gold: 1Sp Rebirths (Fetch)", lambda: recovery_button_fetch(2, "Gold", 1e24, "Rebirths")),
         ("1 Obsidian: 25 Quartz (Sets)", lambda: recovery_button_set(1, "Obsidian", 25, "Quartz")),
         ("2 Ion: 1 Sapphire (Fetch)", lambda: recovery_button_fetch(2, "Ion", 1, "Sapphire")),
      ],
      "Geodes": [
         ("Stone Geode: 1M Stone", lambda btn: Geode_roll(btn, stone_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
         ("White Gems Geode: 30 White Gems", lambda btn: Geode_roll(btn, gems_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
         ("Jade Geode: 500 Jade", lambda btn: Geode_roll(btn, jade_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
         ("Uranium Geode: 12 Uranium", lambda btn: Geode_roll(btn, uranium_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
      ],
      "Area Teleports": [
         ("Caves (req: 10 Stone)", lambda: load_check("C")),
         ("Crystal Beneaths (req: 300 White Gems)", lambda: load_check("CB")),
         ("Iron Shafts (req: 100 Crystal)", lambda: load_check("IS")),
         ("Golden Quarry (req: 750 Iron)", lambda: load_check("GQ")),
         ("Quartz Walkway (req: 75 Gold)", lambda: load_check("QW")),
         ("Jade Forest (req: 450 Quartz)", lambda: load_check("JF")),
         ("Obsidian Abyss (req: 80 Jade)", lambda: load_check("OA")),
         ("Colour Temple (req: 5 Obsidian)", lambda: load_check("CT")),
         ("Extraterrestrial Orbits (req: 50k Sapphire)", lambda: load_check("ET")),
         ("Empyrean Island (req: 100 Starlight)", lambda: load_check("EI")),
         ("Uranium Wastelands (req: 3 Ion)", lambda: load_check("UW")),
         ("Smooth Depths (req: 15 Uranium)", lambda: load_check("SD")),
         ("Icy Palace (req: 50 Bismuth)", lambda: load_check("IP")),
         ("Floating Purgatory (req: 10 Nissonite)", lambda: load_check("FP")),
         ("Tetratum (req: 500 Orpiment)", lambda: load_check("T")),
         ("Voltaic Sector (req: 50 Tetra)", lambda: load_check("VS")),
         ("Abyssal Trenches (req: 3 Volt)", lambda: load_check("AT")),
         ("Flourish Candylands (req: 25 Aquamarine)", lambda: load_check("FC")),
         ("Minty Grooves (req: 5 Rebirths)", lambda: load_check("MG")),
         ("Stardustry (req: 1 Gold)", lambda: load_check("SD")),
         ("Geode Site (req: 1 Lollipop)", lambda: load_check("GS")),
         ("Elysian Stratosphere (req: 100 Lollipop)", lambda: load_world(100, "Lollipop", Elysian_Stratosphere)),
         ("MECHANICAL ROOM (req: 1 Prime Alpha Key)", lambda: load_check("MR")),
         ("Recover Hall (req: 0 Cash)", lambda: load_check("RH"))
     ],
     "World Teleports": [
         ("Afterlife Domain (req: 3 Zanyte)", lambda: load_world(3, "Zanyte", Afterlife_Domain)),
         ("Moonbase (req: 1 Obsidian)", lambda: load_world(1, "Obsidian", Moonbase))
     ],
     "                                                                                                                                                                                                                                                                                                  ": [],
     "???": [
        ("Are you patient enough to overcome 7 billion thoughts?", lambda: sloth(root))
     ]
  }, 0, "Cash", "S", voltaic_radar=voltaic_radar)
  Realm(root, { #Caves
      "Multiplier": [
          ("620Sp Cash: 1Qd Multiplier", lambda: cost_button("Cash", 6.2e26, "Multiplier", 1e15)),
          ("3.5Oc Cash: 6Qd Multiplier", lambda: cost_button("Cash", 3.5e27,"Multiplier", 6e15)),
          ("60Oc Cash: 50Qd Multiplier", lambda: cost_button("Cash", 6e28, "Multiplier", 5e16)),
          ("450Oc Cash: 230Qd Multiplier", lambda: cost_button("Cash", 4.5e29, "Multiplier", 2.3e17)),
          ("3No Cash: 1Qn Multiplier", lambda: cost_button("Cash", 3e30,"Multiplier", 1e18)),
          ("100No Cash: 5Qn Multiplier", lambda: cost_button("Cash",1e32,"Multiplier", 5e18)),
          ("800No Cash: 30Qn Multiplier", lambda: cost_button("Cash",8e32,"Multiplier", 3e19)),
          ("8De Cash: 240Qn Multiplier", lambda: cost_button("Cash",8e33,"Multiplier", 2.4e20)),
          ("90De Cash: 800Qn Multiplier", lambda: cost_button("Cash",8e34,"Multiplier", 8e20)),
          ("500De Cash: 3Sx Multiplier", lambda: cost_button("Cash",5e35,"Multiplier", 3e21)),
          ("1.2e36 Cash: 13Sx Multiplier", lambda: cost_button("Cash",1.2e36,"Multiplier", 1.3e22)),
          ("4.2e37 Cash: 40Sx Multiplier", lambda: cost_button("Cash",4.2e37,"Multiplier", 4e22)),
          ("3.25e38 Cash: 100Sx Multiplier", lambda: cost_button("Cash",3.25e38,"Multiplier", 1e23)),
          ("1e39 Cash: 400Sx Multiplier", lambda: cost_button("Cash",1e39,"Multiplier", 4e23)),
          ("3.5e40 Cash: 800Sx Multiplier", lambda: cost_button("Cash",3.5e40,"Multiplier", 8e23)),
          ("5.05e41 Cash: 3Sp Multiplier", lambda: cost_button("Cash",5.05e41,"Multiplier", 3e24)),
          ("2e42 Cash: 20Sp Multiplier", lambda: cost_button("Cash",2e42,"Multiplier", 2e25)),
          ("7.5e43 Cash: 60Sp Multiplier", lambda: cost_button("Cash", 7.5e43,"Multiplier", 6e25)),
          ("3.5e44 Cash: 200Sp Multiplier", lambda: cost_button("Cash",3.5e44,"Multiplier", 2e26)),
          ("8.5e44 Cash: 500Sp Multiplier", lambda: cost_button("Cash",8.5e44,"Multiplier", 5e26)),
          ("5e45 Cash: 1.2Oc Multiplier", lambda: cost_button("Cash",5e45,"Multiplier", 1.2e27)),
          ("6.2e46 Cash: 3Oc Multiplier", lambda: cost_button("Cash",6.2e46,"Multiplier", 3e27)),
      ],
      "Rebirths": [
          ("30Qn Multiplier: 1B Rebirths", lambda: reset_button(3e19,"Multiplier",1e9, "Rebirths")),
          ("900Qn Multiplier: 10B Rebirths", lambda: reset_button(9e20,"Multiplier",1e10, "Rebirths")),
          ("60Sx Multiplier: 80B Rebirths", lambda: reset_button(6e22,"Multiplier",8e10, "Rebirths")),
          ("800Sx Multiplier: 150B Rebirths", lambda: reset_button(8e23,"Multiplier",1.5e11, "Rebirths")),
          ("90Sp Multiplier: 500B Rebirths", lambda: reset_button(9e25,"Multiplier",5e11, "Rebirths")),
          ("1Oc Multiplier: 10T Rebirths", lambda: reset_button(1e27,"Multiplier",1e13, "Rebirths")),
          ("750Oc Multiplier: 70T Rebirths", lambda: reset_button(7.5e29,"Multiplier",7e13, "Rebirths")),
          ("15No Multiplier: 300T Rebirths", lambda: reset_button(1.5e31,"Multiplier",3e14, "Rebirths")),
          ("600No Multiplier: 2Qd Rebirths", lambda: reset_button(6e32,"Multiplier",2e15, "Rebirths")),
          ("50De Multiplier: 15Qd Rebirths", lambda: reset_button(5e34,"Multiplier",1.5e16, "Rebirths")),
          ("1e36 Multiplier: 200Qd Rebirths", lambda: reset_button(1e36,"Multiplier",2e17, "Rebirths")),
          ("4e38 Multiplier: 1Qn Rebirths", lambda: reset_button(4e38,"Multiplier",1e18, "Rebirths")),
          ("1.5e40 Multiplier: 40Qn Rebirths", lambda: reset_button(1.5e40,"Multiplier", 4e19, "Rebirths")),
          ("1e42 Multiplier: 300Qn Rebirths", lambda: reset_button(1e42,"Multiplier",3e20, "Rebirths")),
          ("1.5e45 Multiplier: 5Sx Rebirths", lambda: reset_button(1.5e45,"Multiplier",5e21, "Rebirths")),
      ],
      "Stone": [
          ("250B Rebirths: 26 Stone", lambda: reset_button(2.5e11, "Rebirths", 26, "Stone")),
          ("1Qd Rebirths: 120 Stone", lambda: reset_button(1e15, "Rebirths", 120, "Stone")),
          ("700Qd Rebirths: 450 Stone", lambda: reset_button(7e17, "Rebirths", 450, "Stone")),
          ("650Qn Rebirths: 5k Stone", lambda: reset_button(6.5e20, "Rebirths", 5000, "Stone")),
          ("1Sp Rebirths: 15k Stone", lambda: reset_button(1e24, "Rebirths", 15000, "Stone")),
          ("80Oc Rebirths: 32k Stone", lambda: reset_button(8e28, "Rebirths", 32000, "Stone")),
          ("700Oc Rebirths: 85k Stone", lambda: reset_button(7e29, "Rebirths", 85000, "Stone")),
          ("3No Rebirths: 300k Stone", lambda: reset_button(3e30, "Rebirths", 3e5, "Stone")),
          ("24No Rebirths: 1M Stone", lambda: reset_button(2.4e31, "Rebirths", 1e6, "Stone")),
      ],
      "White Gems": [
          ("5k Stone: 1 White Gems", lambda: reset_button(5000, "Stone", 1, "White Gems")),
          ("60k Stone: 3 White Gems", lambda: reset_button(60000, "Stone", 3, "White Gems")),
          ("500k Stone: 10 White Gems", lambda: reset_button(500000, "Stone", 10, "White Gems")),
          ("10M Stone: 30 White Gems", lambda: reset_button(1e7, "Stone", 30, "White Gems")),
          ("200M Stone: 86 White Gems", lambda: reset_button(2e8, "Stone", 86, "White Gems")),
      ],
      "Gem Buttons": [
          ("50 White Gems: 1 Gems", lambda: cost_button("White Gems", 50, "Gems", 1)),
          ("500 White Gems: 5 Gems", lambda: cost_button("White Gems", 500, "Gems", 5)),
          ("3k White Gems: 10 Gems", lambda: cost_button("White Gems", 3000, "Gems", 10)),
      ],
      "Recovery": [
         ("5 White Gems: 100k Rebirths (Fetch)", lambda: recovery_button_fetch(5, "White Gems", 100000, "Rebirths")),
         ("50 Gems: 5T Multiplier (Fetch)", lambda: recovery_button_fetch(50, "Gems", 5e12, "Multiplier")),
         ("3 Gold: 1M Stone (Fetch)", lambda: recovery_button_fetch(3, "Gold", 1e6, "Stone")),
      ],
      "Area Teleports": [
         ("Crystal Beneaths (req: 300 White Gems)", lambda: load_check("CB")),
         ("Spawn (req: 0 Cash)", lambda: load_check("S")),
         ("Recover Hall (req: 0 Cash)", lambda: load_check("RH"))
      ]
  }, 10, "Stone", "C", voltaic_radar=voltaic_radar, bg="#262626", text_color="#a2a2a2")
  Realm(root, { #Recovery Hall
      "Spawn": [
         ("15 Stone: 15Qn Cash (Sets)", lambda: recovery_button_set(15, "Stone", 5e19, "Cash")),
         ("7 Iron: 1e40 Cash (Sets)", lambda: recovery_button_set(7, "Iron", 1e40, "Cash")),
         ("1 Gold: 6e41 Multiplier (Fetch)", lambda: recovery_button_fetch(1, "Gold", 6e41, "Multiplier")),
         ("2 Gold: 1Sp Rebirths (Fetch)", lambda: recovery_button_fetch(2, "Gold", 1e24, "Rebirths")),
         ("1 Obsidian: 25 Quartz (Sets)", lambda: recovery_button_set(1, "Obsidian", 25, "Quartz")),
         ("2 Ion: 1 Sapphire (Fetch)", lambda: recovery_button_fetch(2, "Ion", 1, "Sapphire")),                
      ],
      "Caves": [
         ("5 White Gems: 100k Rebirths (Fetch)", lambda: recovery_button_fetch(5, "White Gems", 100000, "Rebirths")),
         ("50 Gems: 5T Multiplier (Fetch)", lambda: recovery_button_fetch(50, "Gems", 5e12, "Multiplier")),
      ],
      "Crystal Beneaths": [
         ("500 White Gems: 12Qn Multiplier (Fetch)", lambda: recovery_button_fetch(500, "White Gems", 1.2e19, "Multiplier")),
         ("150B Stone: 3M Rebirths (Fetch)", lambda: recovery_button_fetch(1.5e11, "Stone", 3e6, "Rebirths")),  
         ("3 Crystal: 200 Stone (Fetch)", lambda: recovery_button_fetch(3, "Crystal", 200, "Stone")),
         ("5 Crystal: 200 White Gems (Sets)", lambda: recovery_button_set(5, "Crystal", 200, "White Gems")),      
      ],
      "Iron Shafts": [
          ("1k Crystal: 500Qn Rebirths (Fetch)", lambda: recovery_button_fetch(1000, "Crystal", 5e20, "Rebirths")),
          ("150B White Gems: 10k Stone (Fetch)", lambda: recovery_button_fetch(1.5e14, "White Gems", 1e4, "Stone")),
          ("3 Iron: 10 White Gems (Fetch)", lambda: recovery_button_fetch(3, "Iron", 10, "White Gems")),
          ("50k Gems: 70 Crystal", lambda: cost_button("Gems", 5e4, "Crystal", 70)),
      ],
      "Gold Quarry": [
          ("3 Gold: 1M Stone (Fetch)", lambda: recovery_button_fetch(3, "Gold", 1e6, "Stone")),
          ("4 Gold: 500 White Gems (Fetch)", lambda: recovery_button_fetch(4, "Gold", 500, "White Gems")),
      ],
      "Quartz Walkway": [
          ("7k Gems: 1e45 Multiplier (Fetch)", lambda: recovery_button_fetch(7000, "Gems", 1e45, "Multiplier")),
          ("1k Gold: 5M White Gems (Fetch)", lambda: recovery_button_fetch(1000, "Gold", 5e6, "White Gems")),
          ("15 Quartz: 100 Iron (Fetch)", lambda: recovery_button_fetch(15, "Quartz", 100, "Iron")),
          ("1 Quartz: 1B Crystal (Sets)", lambda: recovery_button_set(1, "Quartz", 1e9, "Crystal")),
      ],
      "Jade Forest": [
          ("300 Quartz: 1e67 Rebirths (Fetch)", lambda: recovery_button_fetch(300, "Quartz", 1e67, "Rebirths")),
          ("1M Gold: 1No Stone (Fetch)", lambda: recovery_button_fetch(1e6, "Gold", 1e30, "Stone")),
          ("2 Jade: 15Sx Crystal (Fetch)", lambda: recovery_button_fetch(2, "Jade", 1.5e22, "Crystal")),
          ("1 Jade: 10 Gold (Sets)", lambda: recovery_button_set(1, "Jade", 10, "Gold")),
      ],
      "Obsidian Abyss": [
          ("1Qd Quartz: 1e303 Rebirths (Fetch)", lambda: recovery_button_fetch(1e15, "Quartz", Mantissa(1,303), "Rebirths")),
          ("100 Jade: 5.2T White Gems (Fetch)", lambda: recovery_button_fetch(100, "Jade", 5.2e12, "White Gems")),
          ("1M Jade: 1Qn Iron (Fetch)", lambda: recovery_button_fetch(1e6, "Jade", 1e18, "Iron")),
          ("6 Obsidian: 5 Quartz (Fetch)", lambda: recovery_button_fetch(6, "Obsidian", 5, "Quartz")),
          ("2 Obsidian: 3 Jade (Sets)", lambda: recovery_button_set(2, "Obsidian", 3, "Jade")),
      ],
      "Colour Temple": [
          ("1 Ruby: 10 Quartz (Fetch)", lambda: recovery_button_fetch(1, "Ruby", 10, "Quartz")),
          ("200 Ruby: 1Oc Gold (Fetch)", lambda: recovery_button_fetch(200, "Ruby", 1e27, "Gold")),
          ("50 Emerald: 1e444 Rebirths (Fetch)", lambda: recovery_button_fetch(50, "Emerald", Mantissa(1,444), "Rebirths")), 
          ("10 Obsidian: 500 Jade (Sets)", lambda: recovery_button_set(10, "Obsidian", 500, "Jade")),
          ("1 Sapphire: 10 Ruby (Sets)", lambda: recovery_button_set(1, "Sapphire", 10, "Ruby")),
      ],
      "Extraterrestrial Orbits": [
          ("1 Ruby: 50 Jade (Fetch)", lambda: recovery_button_fetch(1, "Ruby", 50, "Jade")),
          ("1 Diamond: 5 Obsidian (Sets)", lambda: recovery_button_set(1, "Diamond", 5, "Obsidian")),
          ("1 Starlight: 25 Obsidian (Sets)", lambda: recovery_button_set(1, "Starlight", 25, "Obsidian")),
      ],
      "Empyrean Island": [
          ("10k Diamond: 1e650 Crystal (Sets)", lambda: recovery_button_set(1e4, "Diamond", Mantissa(1,650), "Crystal")),
          ("500 Starlight: 15 Ruby (Fetch)", lambda: recovery_button_fetch(500, "Starlight", 15, "Ruby")),
          ("400B Gems: 1 Diamond (Sets)", lambda: recovery_button_set(4e11, "Gems", 1, "Diamond")),
          ("3 Ion: 1 Starlight (Sets)", lambda: recovery_button_set(3, "Ion", 1, "Starlight")),
      ],
      "Uranium Wastelands": [
          ("100 Ion: 1e2000 Multiplier (Fetch)", lambda: recovery_button_fetch(100, "Ion", Mantissa(1,2000), "Multiplier")),
          ("1T Gems: 1e45 Obsidian (Sets)", lambda: recovery_button_set(1e12, "Gems", 1e45, "Obsidian")),
          ("1M Starlight: 1No Sapphire (Sets)", lambda: recovery_button_set(1e6, "Starlight", 1e30, "Sapphire")),
          ("1 Uranium: 25 Diamond (Sets)", lambda: recovery_button_set(1, "Uranium", 25, "Diamond")),
          ("3 Uranium: 1 Ion (Sets)", lambda: recovery_button_set(3, "Uranium", 1, "Ion")),
      ],
      "Smooth Depths": [
          ("1 Bismuth: 800 Diamond (Fetch)", lambda: recovery_button_fetch(1, "Bismuth", 600, "Diamond")),
      ],
      "Icy Palace": [
          ("3 Boracite: 200 Ion (Fetch)", lambda: recovery_button_fetch(3, "Boracite", 200, "Ion")),
          ("1 Nissonite: 10 Bismuth (Sets)", lambda: recovery_button_set(1, "Nissonite", 10, "Bismuth")),
      ],
      "Floating Purgatory": [
          ("666 Nissonite: 1k Uranium (Fetch)", lambda: recovery_button_fetch(666, "Nissonite", 1000, "Uranium")),
          ("1 Orpiment: 60 Boracite (Sets)", lambda: recovery_button_set(1, "Orpiment", 60, "Boracite")),
          ("Orpiment Geode: 2 Orpiment", lambda btn: Geode_roll(btn, orpiment_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
      ],
      "Tetratum": [
          ("10k Orpiment: 1k Bismuth (Fetch)", lambda: recovery_button_fetch(1e4, "Orpiment", 1000, "Bismuth")),
          ("1 Tetra: 1k Boracite (Sets)", lambda: recovery_button_set(1, "Tetra", 1000, "Boracite")),
          ("3 Tetra: 1 Orpiment (Sets)", lambda: recovery_button_set(3, "Tetra", 1, "Orpiment")),
      ],
      "Voltiac Sector": [
          ("1Sp Nissonite: 1e33 Uranium (Fetch)", lambda: recovery_button_fetch(1e24, "Nissonite", 1e33, "Uranium")),
          ("650 Tetra: 100 Nissonite (Fetch)", lambda: recovery_button_fetch(650, "Tetra", 100, "Nissonite")),
          ("1 Volt: 100 Orpiment (Sets)", lambda: recovery_button_set(1, "Volt", 100, "Orpiment")),
      ],
      "Abyssal Trenches": [
          ("1M Tetra: 10M Bismuth (Fetch)", lambda: recovery_button_fetch(1e6, "Tetra", 1e7, "Bismuth")),
          ("500 Volt: 1 Orpiment (Fetch)", lambda: recovery_button_fetch(500, "Volt", 1, "Orpiment")),
          ("1 Aquamarine: 1k Nissonite (Sets)", lambda: recovery_button_set(1, "Aquamarine", 1000, "Nissonite")),
          ("1 Aquamarine: 30 Tetra (Sets)", lambda: recovery_button_set(1, "Aquamarine", 30, "Tetra")),
      ],
      "Flourish Candylands": [
          ("1 Lollipop: 350 Volt (Sets)", lambda: recovery_button_set(1, "Lollipop", 350, "Volt")),
          ("4 Lollipop: 100 Tetra (Fetch)", lambda: recovery_button_fetch(4, "Lollipop", 100, "Tetra")),
      ],
      "Ω1": [
          ("Anticovery Hall (req: 1 Stargazed Metal)", lambda: load_check("AH")),
          ("Anticovery Hall (req: 1 Gyge)", lambda: load_check("AH")),
      ],
      "???3Δ8???": [
          ("1 Stargazed Metal: 1M Gold (Sets)", lambda: recovery_button_set(1, "Stargazed Metal", 1e6, "Gold")),
          ("6 Stargazed Metal: 5 Obsidian (Fetch)", lambda: recovery_button_fetch(6, "Stargazed Metal", 5, "Obsidian")),
          ("52 Stargazed Metal: 1k Diamond (Sets)", lambda: recovery_button_set(52, "Stargazed Metal", 1000, "Diamond")),
          ("1 Gyge: 3 Emerald (Fetch)", lambda: recovery_button_fetch(1, "Gyge", 3, "Emerald")),
          ("75 Gyge: 1M Uranium (Sets)", lambda: recovery_button_set(75, "Gyge", 1e6, "Uranium")),
          ("3 Auly Plate: 50 Orpiment (Sets)", lambda: recovery_button_set(3, "Auly Plate", 50, "Orpiment")),
      ],
      "Gem Buttons": [
          ("50 White Gems: 1 Gems", lambda: cost_button("White Gems", 50, "Gems", 1)),
          ("15 Crystal: 3 Gems", lambda: cost_button("Crystal", 15, "Gems", 3)),
          ("500 White Gems: 5 Gems", lambda: cost_button("White Gems", 500, "Gems", 5)),
          ("3k White Gems: 10 Gems", lambda: cost_button("White Gems", 3000, "Gems", 10)),
          ("100 Crystal: 12 Gems", lambda: cost_button("Crystal", 100, "Gems", 12)),
          ("1 Iron: 20 Gems", lambda: cost_button("Iron", 1, "Gems", 20)),
          ("1k Crystal: 21 Gems", lambda: cost_button("Crystal", 1000, "Gems", 21)),
          ("3 Quartz: 70 Gems", lambda: cost_button("Quartz", 3, "Gems", 70)),
          ("600k Iron: 100 Gems", lambda: cost_button("Iron", 6e5, "Gems", 100)),
          ("10 Quartz: 200 Gems", lambda: cost_button("Quartz", 10, "Gems", 200)),
          ("1e68 Rebirths: 400 Gems", lambda: cost_button("Rebirths", 1e68, "Gems", 400)),
          ("600T Crystal: 500 Gems", lambda: cost_button("Crystal", 6e14, "Gems", 500)),
          ("100De White Gems: 600 Gems", lambda: cost_button("White Gems", 1e35, "Gems", 600)),
          ("1e172 Mutliplier: 750 Gems", lambda: cost_button("Multiplier", 1e172, "Gems", 750)),
          ("1e47 Stone: 800 Gems", lambda: cost_button("Stone", 1e47, "Gems", 800)),
          ("50 Quartz: 950 Gems", lambda: cost_button("Quartz", 50, "Gems", 950)),
          ("10 Jade: 1k Gems", lambda: cost_button("Jade", 10, "Gems", 1000)),
          ("250 Quartz: 2.2k Gems", lambda: cost_button("Quartz", 250, "Gems", 2200)),
          ("150 Jade: 17.5k Gems", lambda: cost_button("Jade", 150, "Gems", 17500)),
          ("25M Quartz: 50k Gems", lambda: cost_button("Quartz", 2.5e7, "Gems", 5e4)),
          ("5e41 Sapphire: 250M Gems", lambda: cost_button("Sapphire", 5e41, "Gems", 2.5e8)),
          ("1k Starlight: 800M Gems", lambda: cost_button("Starlight", 1000, "Gems", 8e8)),
          ("7 Ion: 3B Gems", lambda: cost_button("Ion", 7, "Gems", 3e9)),
          ("2 Volt: 1T Gems", lambda: cost_button("Volt", 2, "Gems", 1e12)),
      ],
      "Area Teleports": [
          ("Spawn (req: 0 Cash)", lambda: load_check("S")),
          ("Caves (req: 10 Stone)", lambda: load_check("C")),
          ("Crystal Beneaths (req: 300 White Gems)", lambda: load_check("CB")),
          ("Iron Shafts (req: 100 Crystal)", lambda: load_check("IS")),
          ("Golden Quarry (req: 750 Iron)", lambda: load_check("GQ")),
          ("Quartz Walkway (req: 75 Gold)", lambda: load_check("QW")),
          ("Jade Forest (req: 450 Quartz)", lambda: load_check("JF")),
          ("Obsidian Abyss (req: 80 Jade)", lambda: load_check("OA")),
          ("Colour Temple (req: 5 Obsidian)", lambda: load_check("CT")),
          ("Extraterrestrial Orbits (req: 50k Sapphire)", lambda: load_check("ET")),
          ("Empyrean Island (req: 100 Starlight)", lambda: load_check("EI")),
          ("Uranium Wastelands (req: 3 Ion)", lambda: load_check("UW")),
          ("Smooth Depths (req: 15 Uranium)", lambda: load_check("SD")),
          ("Icy Palace (req: 50 Bismuth)", lambda: load_check("IP")),
          ("Icy Palace (req: 1 Nissonite)", lambda: load_check("IP")),
          ("Floating Purgatory (req: 10 Nissonite)", lambda: load_check("FP")),
          ("Tetratum (req: 500 Orpiment)", lambda: load_check("T")),
          ("Voltaic Sector (req: 50 Tetra)", lambda: load_check("VS")),
          ("Abyssal Trenches (req: 3 Volt)", lambda: load_check("AT")),
          ("Flourish Candylands (req: 25 Aquamarine)", lambda: load_check("FC")),
          ("Minty Grooves (req: 5 Rebirths)", lambda: load_check("MG")),
          ("Stardustry (req: 1 Gold)", lambda: load_check("St")),
          ("Purified Illusions (req: 1 Starglass)", lambda: load_check("PI")),
          ("Purified Illusions (req: 1 Shell Piece)", lambda: load_check("PI")),
      ]
  }, 0, "Cash", "RH", voltaic_radar=voltaic_radar, bg="#797979", text_color="#ffffff")
  Realm(root, { #Crystal Beneaths
      "Multiplier": [
          ("8e71 Cash: 10Oc Multiplier", lambda: cost_button("Cash",8e71,"Multiplier", 1e28)),
          ("1e74 Cash: 20Oc Multiplier", lambda: cost_button("Cash",1e74,"Multiplier", 2e28)),
          ("7.5e74 Cash: 40Oc Multiplier", lambda: cost_button("Cash",7.5e74,"Multiplier", 4e28)),
          ("5e76 Cash: 75Oc Multiplier", lambda: cost_button("Cash",5e76,"Multiplier", 7.5e28)),
          ("1.8e77 Cash: 150Oc Multiplier", lambda: cost_button("Cash",1.8e77,"Multiplier", 1.5e29)),
          ("7e77 Cash: 250Oc Multiplier", lambda: cost_button("Cash",7e77,"Multiplier", 2.5e29)),
          ("3e78 Cash: 800Oc Multiplier", lambda: cost_button("Cash",3e78,"Multiplier", 8e29)),
          ("4.6e79 Cash: 3No Multiplier", lambda: cost_button("Cash",4.6e79,"Multiplier", 3e30)),
          ("1.85e80 Cash: 12No Multiplier", lambda: cost_button("Cash",1.85e80,"Multiplier", 1.2e31)),
          ("7.25e80 Cash: 47No Multiplier", lambda: cost_button("Cash",7.25e80,"Multiplier", 4.7e31)),
          ("4e81 Cash: 100No Multiplier", lambda: cost_button("Cash",4e81,"Multiplier", 1e32)),
          ("6.5e82 Cash: 300No Multiplier", lambda: cost_button("Cash",6.5e82,"Multiplier", 3e32)),
          ("4.44e83 Cash: 800No Multiplier", lambda: cost_button("Cash",4.44e83,"Multiplier", 8e32)),
          ("1e84 Cash: 2De Multiplier", lambda: cost_button("Cash",1e84,"Multiplier", 2e33)),
      ],
      "Rebirths": [
          ("8e62 Multiplier: 40Sx Rebirths", lambda: reset_button(8e62,"Multiplier",4e22, "Rebirths")),
          ("2e64 Multiplier: 300Sx Rebirths", lambda: reset_button(2e64,"Multiplier",3e23, "Rebirths")),
          ("7e65 Multiplier: 1Sp Rebirths", lambda: reset_button(7e65,"Multiplier",1e24, "Rebirths")),
          ("8e66 Multiplier: 20Sp Rebirths", lambda: reset_button(8e66,"Multiplier",2e25, "Rebirths")),
          ("1.6e68 Multiplier: 100Sp Rebirths", lambda: reset_button(1.6e68,"Multiplier",1e26, "Rebirths")),
          ("9e68 Multiplier: 800Sp Rebirths", lambda: reset_button(9e68,"Multiplier",8e26, "Rebirths")),
          ("1.5e70 Multiplier: 3Oc Rebirths", lambda: reset_button(1.5e70,"Multiplier",3e27, "Rebirths")),
          ("7.5e71 Multiplier: 15Oc Rebirths", lambda: reset_button(7.5e71,"Multiplier",1.5e28, "Rebirths")),
          ("2e73 Multiplier: 100Oc Rebirths", lambda: reset_button(2e73,"Multiplier",1e29, "Rebirths")),
          ("6e74 Multiplier: 1No Rebirths", lambda: reset_button(6e74,"Multiplier",1e30, "Rebirths")),
          ("4e75 Multiplier: 14No Rebirths", lambda: reset_button(4e75,"Multiplier",1.4e31, "Rebirths")),
          ("2.6e77 Multiplier: 46No Rebirths", lambda: reset_button(2.6e77,"Multiplier",4.6e31, "Rebirths")),
          ("2e78 Multiplier: 300No Rebirths", lambda: reset_button(2e78,"Multiplier",3e32, "Rebirths")),
          ("7e79 Multiplier: 1De Rebirths", lambda: reset_button(7e79,"Multiplier",1e33, "Rebirths")),
      ],
      "Stone": [
          ("3e40 Rebirths: 5M Stone", lambda: reset_button(3e40,"Rebirths",5e6, "Stone")),
          ("5e41 Rebirths: 20M Stone", lambda: reset_button(5e41,"Rebirths",2e7, "Stone")),
          ("3e42 Rebirths: 100M Stone", lambda: reset_button(3e42,"Rebirths",1e8, "Stone")),
          ("8e43 Rebirths: 300M Stone", lambda: reset_button(8e43,"Rebirths",3e8, "Stone")),
          ("4e44 Rebirths: 1B Stone", lambda: reset_button(4e44, "Rebirths", 1e9,"Stone")),
          ("5e45 Rebirths: 20B Stone", lambda: reset_button(5e45, "Rebirths",2e10,"Stone")),
          ("8e46 Rebirths: 100B Stone", lambda: reset_button(8e46, "Rebirths",1e11,"Stone")),
          ("5e47 Rebirths: 400B Stone", lambda: reset_button(5e47, "Rebirths",4e11,"Stone")),
          ("3e48 Rebirths: 3T Stone", lambda: reset_button(3e48, "Rebirths",3e12,"Stone")),
          ("4e50 Rebirths: 10T Stone", lambda: reset_button(4e50, "Rebirths",1e13,"Stone")),
          ("2e51 Rebirths: 40T Stone", lambda: reset_button(2e51, "Rebirths",4e13,"Stone")),
          ("3e52 Rebirths: 100T Stone", lambda: reset_button(3e52, "Rebirths", 1e14,"Stone")),
          ("7.5e53 Rebirths: 2Qd Stone", lambda: reset_button(7.5e53, "Rebirths", 2e15,"Stone")),
          ("5e54 Rebirths: 10Qd Stone", lambda: reset_button(5e54, "Rebirths",1e16,"Stone"))
      ],
      "White Gems": [
          ("100B Stone: 300 White Gems", lambda: reset_button(1e11, "Stone", 300,"White Gems")),
          ("900B Stone: 1k White Gems", lambda: reset_button(9e11, "Stone", 1000,"White Gems")),
          ("30T Stone: 5k White Gems", lambda: reset_button(3e13, "Stone", 5000,"White Gems")),
          ("750T Stone: 12k White Gems", lambda: reset_button(7.5e14, "Stone", 1.2e4,"White Gems")),
          ("2.8Qd Stone: 20k White Gems", lambda: reset_button(2.8e15, "Stone", 2e4,"White Gems")),
          ("100Qd Stone: 120k White Gems", lambda: reset_button(1e17, "Stone", 1.2e5,"White Gems")),
          ("4Qn Stone: 230k White Gems", lambda: reset_button(4e18, "Stone", 2.3e5,"White Gems"))
      ],
      "Crystal": [
          ("10k White Gems: 1 Crystal", lambda: reset_button(1e4, "White Gems", 1,"Crystal")),
          ("600k White Gems: 6 Crystal", lambda: reset_button(6e5, "White Gems", 6,"Crystal")),
          ("2M White Gems: 20 Crystal", lambda: reset_button(2e6, "White Gems", 20,"Crystal")),
          ("500M White Gems: 50 Crystal", lambda: reset_button(5e8, "White Gems", 50,"Crystal")),
      ],
      "Gem Buttons": [
          ("15 Crystal: 3 Gems", lambda: cost_button("Crystal",15, "Gems", 3)),
          ("100 Crystal: 12 Gems", lambda: cost_button("Crystal",100, "Gems", 12)),
          ("1k Crystal: 21 Gems", lambda: cost_button("Crystal",1000, "Gems", 21)),
      ],
      "Recovery": [
          ("3 Crystal: 200 Stone (Fetch)", lambda: recovery_button_fetch(3, "Crystal", 200, "Stone")),
          ("500 White Gems: 12Qn Multiplier (Fetch)", lambda: recovery_button_fetch(500, "White Gems", 1.2e19, "Multiplier")),
          ("4 Gold: 500 White Gems (Fetch)", lambda: recovery_button_fetch(4, "Gold", 500, "White Gems")),
      ],
      "Geodes": [
          ("Crystal Geode: 100 Crystal", lambda btn: Geode_roll(btn, crystal_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll))
      ],
      "Area Teleports": [
         ("Iron Shafts (req: 100 Crystal)", lambda: load_check("IS")),
         ("Spawn (req: 0 Cash)", lambda: load_check("S")),
         ("Recover Hall (req: 0 Cash)", lambda: load_check("RH"))
      ]
  }, 300, "White Gems", "CB", voltaic_radar=voltaic_radar, bg="#31003b", text_color="#ffffff")
  Realm(root, { #Iron Shafts
      "Mutliplier": [
          ("1e93 Cash: 8De Multiplier", lambda: cost_button("Cash",1e93,"Multiplier", 8e33)),
          ("8e94 Cash: 17De Multiplier", lambda: cost_button("Cash",8e94,"Multiplier", 1.7e34)),
          ("2e96 Cash: 40De Multiplier", lambda: cost_button("Cash",2e96,"Multiplier", 4e34)),
          ("1e98 Cash: 200De Multiplier", lambda: cost_button("Cash",1e98,"Multiplier", 2e35)),
          ("8e98 Cash: 500De Multiplier", lambda: cost_button("Cash",8e98,"Multiplier", 5e35)),
          ("6e99 Cash: 1.2e36 Multiplier", lambda: cost_button("Cash",6e99,"Multiplier", 1.2e36)),
          ("3e101 Cash: 3e36 Multiplier", lambda: cost_button("Cash",3e101,"Multiplier", 3e36)),
          ("3e102 Cash: 4.5e37 Multiplier", lambda: cost_button("Cash",3e102,"Multiplier", 4.5e37)),
          ("1e104 Cash: 7e37 Multiplier", lambda: cost_button("Cash",1e104,"Multiplier", 7e37)),
          ("6e104 Cash: 1.2e38 Multiplier", lambda: cost_button("Cash",6e104,"Multiplier", 1.2e38)),
          ("5e105 Cash: 4e38 Multiplier", lambda: cost_button("Cash",5e105,"Multiplier", 4e38)),
          ("3.5e106 Cash: 7.5e38 Multiplier", lambda: cost_button("Cash",3.5e106,"Multiplier", 7e38)),
          ("5e107 Cash: 2e39 Multiplier", lambda: cost_button("Cash",5e107,"Multiplier", 2e39)),
          ("3e108 Cash: 4e40 Multiplier", lambda: cost_button("Cash",3e108,"Multiplier", 4e40)),
          ("8e110 Cash: 6e40 Multiplier", lambda: cost_button("Cash",8e110,"Multiplier", 6e40)),
      ],
      "Rebirths": [
          ("1e85 Multiplier: 50De Rebirths", lambda: reset_button(1e85,"Multiplier",5e34, "Rebirths")),
          ("5e86 Multiplier: 200De Rebirths", lambda: reset_button(5e87,"Multiplier",2e35, "Rebirths")),
          ("3e87 Multiplier: 500De Rebirths", lambda: reset_button(3e87,"Multiplier",5e35, "Rebirths")),
          ("5e90 Multiplier: 800De Rebirths", lambda: reset_button(5e90,"Multiplier",8e35, "Rebirths")),
          ("2e92 Multiplier: 3e36 Rebirths", lambda: reset_button(2e92,"Multiplier",3e36, "Rebirths")),
          ("3e93 Multiplier: 1.5e37 Rebirths", lambda: reset_button(3e93,"Multiplier",1.5e37, "Rebirths")),
          ("7e95 Multiplier: 8e37 Rebirths", lambda: reset_button(7e95,"Multiplier",8e37, "Rebirths")),
          ("1.5e97 Multiplier: 2e38 Rebirths", lambda: reset_button(1.5e97,"Multiplier",2e38, "Rebirths")),
          ("1e99 Multiplier: 7e38 Rebirths", lambda: reset_button(1e99,"Multiplier",7e38, "Rebirths")),
          ("8e101 Multiplier: 3e39 Rebirths", lambda: reset_button(8e101,"Multiplier",3e39, "Rebirths")),
          ("8e102 Multiplier: 1e40 Rebirths", lambda: reset_button(8e102,"Multiplier",1e40, "Rebirths")),
          ("6e104 Multiplier: 6e40 Rebirths", lambda: reset_button(6e104,"Multiplier",6e40, "Rebirths")),
          ("1.2e106 Multiplier: 4e41 Rebirths", lambda: reset_button(1.2e106,"Multiplier",4e41, "Rebirths")),
      ],
      "Stone": [
          ("1e57 Rebirths: 50Qd Stone", lambda: reset_button(1e57, "Rebirths", 5e16, "Stone")),
          ("5e59 Rebirths: 700Qd Stone", lambda: reset_button(5e59, "Rebirths", 7e17, "Stone")),
          ("3e61 Rebirths: 10Qn Stone", lambda: reset_button(3e61, "Rebirths", 1e19, "Stone")),
          ("7e62 Rebirths: 50Qn Stone", lambda: reset_button(7e62, "Rebirths", 5e19, "Stone")),
          ("2.3e64 Rebirths: 300Qn Stone", lambda: reset_button(2.3e64, "Rebirths", 3e20, "Stone")),
          ("4e65 Rebirths: 800Qn Stone", lambda: reset_button(4e65, "Rebirths", 8e20, "Stone")),
          ("5e67 Rebirths: 3Sx Stone", lambda: reset_button(5e67, "Rebirths", 3e21, "Stone")),
          ("8e68 Rebirths: 20Sx Stone", lambda: reset_button(8e68, "Rebirths", 2e22, "Stone")),
          ("1e70 Rebirths: 100Sx Stone", lambda: reset_button(1e70, "Rebirths", 1e23, "Stone")),
      ],
      "White Gems": [
          ("300Qn Stone: 500k White Gems", lambda: reset_button(3e20, "Stone", 5e5,"White Gems")),
          ("10Sx Stone: 3M White Gems", lambda: reset_button(1e22, "Stone", 3e6,"White Gems")),
          ("300Sx Stone: 10M White Gems", lambda: reset_button(3e23, "Stone", 1e7,"White Gems")),
          ("5Sp Stone: 45M White Gems", lambda: reset_button(5e24, "Stone", 4.5e7,"White Gems")),
          ("100Sp Stone: 160M White Gems", lambda: reset_button(1e26, "Stone", 1.6e8,"White Gems")),
          ("800Sp Stone: 300M White Gems", lambda: reset_button(8e26, "Stone", 3e8,"White Gems")),
          ("25Oc Stone: 750M White Gems", lambda: reset_button(2.5e28, "Stone", 7.5e8,"White Gems")),
          ("800Oc Stone: 2.5B White Gems", lambda: reset_button(8e29, "Stone", 2.5e9,"White Gems")),
      ],
      "Crystal": [
          ("10B White Gems: 125 Crystal", lambda: reset_button(1e10, "White Gems", 125,"Crystal")),
          ("60B White Gems: 300 Crystal", lambda: reset_button(6e10, "White Gems", 300,"Crystal")),
          ("300B White Gems: 750 Crystal", lambda: reset_button(3e11, "White Gems", 750,"Crystal")),
          ("7T White Gems: 2k Crystal", lambda: reset_button(7e12, "White Gems", 2e3,"Crystal")),
          ("80T White Gems: 5k Crystal", lambda: reset_button(8e13, "White Gems", 5e3,"Crystal")),
          ("600T White Gems: 12k Crystal", lambda: reset_button(6e14, "White Gems", 1.2e4,"Crystal")),
          ("50Qd White Gems: 30k Crystal", lambda: reset_button(5e16, "White Gems", 3e4,"Crystal")),
          ("800Qd White Gems: 60k Crystal", lambda: reset_button(8e17, "White Gems", 6e4,"Crystal")),
      ],
      "Iron": [
          ("4k Crystal: 1 Iron", lambda: reset_button(4e3, "Crystal", 1,"Iron")),
          ("42k Crystal: 10 Iron", lambda: reset_button(4.2e4, "Crystal", 10,"Iron")),
          ("1M Crystal: 47 Iron", lambda: reset_button( 1e6, "Crystal", 47,"Iron")),
          ("120M Crystal: 300 Iron", lambda: reset_button(1.2e8, "Crystal", 300,"Iron")),
      ],
      "Gem Buttons": [
          ("1 Iron: 20 Gems", lambda: cost_button("Iron",1, "Gems", 20)),
      ],
      "Recovery": [
          ("1k Crystal: 500Qn Rebirths (Fetch)", lambda: recovery_button_fetch(1000, "Crystal", 5e20, "Rebirths")),
          ("150B White Gems: 10k Stone (Fetch)", lambda: recovery_button_fetch(1.5e14, "White Gems", 1e4, "Stone")),
          ("3 Iron: 10 White Gems (Fetch)", lambda: recovery_button_fetch(3, "Iron", 10, "White Gems")),
          ("50k Gems: 70 Crystal", lambda: cost_button("Gems", 5e4, "Crystal", 70)),
      ],
      "Geodes": [
          ("Iron Geode: 25 Iron", lambda btn: Geode_roll(btn, iron_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check("S")),
         ("Recover Hall (req: 0 Cash)", lambda: load_check("RH")),
         ("Golden Quarry (req: 750 Iron)", lambda: load_check("GQ")),
      ]
  }, 100, "Crystal", "IS", voltaic_radar=voltaic_radar)
  Realm(root, { #Golden Quarry
      "Multiplier": [
          ("1e121 Cash: 1.1e41 Multiplier", lambda: cost_button("Cash",1e121,"Multiplier", 1.1e41)),
          ("2e122 Cash: 3.5e41 Multiplier", lambda: cost_button("Cash",2e122,"Multiplier", 3.5e41)),
          ("5e123 Cash: 6e41 Multiplier", lambda: cost_button("Cash",5e123,"Multiplier", 6e41)),
          ("7.5e124 Cash: 3e42 Multiplier", lambda: cost_button("Cash",7.5e124,"Multiplier", 3e42)),
          ("6e125 Cash: 1e43 Multiplier", lambda: cost_button("Cash",6e125,"Multiplier", 1e43)),
          ("7.5e126 Cash: 3e46 Multiplier", lambda: cost_button("Cash",7.5e126,"Multiplier", 3e46)),
          ("2.5e131 Cash: 8e46 Multiplier", lambda: cost_button("Cash",2.5e131,"Multiplier", 8e46)),
          ("8e131 Cash: 3e50 Multiplier", lambda: cost_button("Cash",8e131,"Multiplier", 3e50)),
          ("9e132 Cash: 7.5e50 Multiplier", lambda: cost_button("Cash",9e132,"Multiplier", 7.5e50)),
          ("8e133 Cash: 1e52 Multiplier", lambda: cost_button("Cash",8e133,"Multiplier", 1e52)),
      ],
      "Rebirths": [
          ("1e114 Multiplier: 1e42 Rebirths", lambda: reset_button(1e114,"Multiplier",1e42, "Rebirths")),
          ("5e115 Multiplier: 5e43 Rebirths", lambda: reset_button(5e115,"Multiplier",5e43, "Rebirths")),
          ("3e116 Multiplier: 6e43 Rebirths", lambda: reset_button(3e116,"Multiplier",6e43, "Rebirths")),
          ("8e117 Multiplier: 1e44 Rebirths", lambda: reset_button(8e117,"Multiplier",1e44, "Rebirths")),
          ("7.6e118 Multiplier: 3.5e44 Rebirths", lambda: reset_button(7.6e118,"Multiplier",3.5e44, "Rebirths")),
          ("7.6e124 Multiplier: 1e46 Rebirths", lambda: reset_button(7.6e124,"Multiplier",1e46, "Rebirths")),
      ],
      "Stone": [
          ("1e75 Rebirths: 100Sx Stone", lambda: reset_button(1e75, "Rebirths", 1e23, "Stone")),
          ("3e76 Rebirths: 500Sx Stone", lambda: reset_button(3e76, "Rebirths", 5e23, "Stone")),
          ("4.5e77 Rebirths: 2Sp Stone", lambda: reset_button(4.5e77, "Rebirths", 2e24, "Stone")),
          ("1.5e79 Rebirths: 10Sp Stone", lambda: reset_button(1.5e79, "Rebirths", 1e25, "Stone")),
          ("8e79 Rebirths: 50Sp Stone", lambda: reset_button(8e79, "Rebirths", 5e25, "Stone")),
          ("7.5e80 Rebirths: 200Sp Stone", lambda: reset_button(7.5e80, "Rebirths", 2e26, "Stone")),
      ],
      "White Gems": [
          ("10De Stone: 30B White Gems", lambda: reset_button(3e34, "Stone", 3e10,"White Gems")),
          ("90De Stone: 100B White Gems", lambda: reset_button(9e34, "Stone", 1e11,"White Gems")),
          ("750De Stone: 500B White Gems", lambda: reset_button(7.5e35, "Stone", 5e11,"White Gems")),
          ("8e36 Stone: 1.5T White Gems", lambda: reset_button(8e36, "Stone", 1.5e12,"White Gems")),
          ("5e37 Stone: 15T White Gems", lambda: reset_button(5e37, "Stone", 1.5e13,"White Gems")),
          ("3e38 Stone: 40T White Gems", lambda: reset_button(3e38, "Stone", 4e13,"White Gems")),
          ("8e38 Stone: 100T White Gems", lambda: reset_button(8e38, "Stone", 1e14,"White Gems")),
          ("5e39 Stone: 400T White Gems", lambda: reset_button(5e39, "Stone", 4e14,"White Gems")),
      ],
      "Crystal": [
          ("500Qn White Gems: 300k Crystal", lambda: reset_button(5e20, "White Gems", 3e5,"Crystal")),
          ("30Sx White Gems: 750k Crystal", lambda: reset_button(3e22, "White Gems", 7.5e5,"Crystal")),
          ("200Sx White Gems: 10M Crystal", lambda: reset_button( 2e23, "White Gems", 1e7,"Crystal")),
          ("10Sp White Gems: 50M Crystal", lambda: reset_button(1e25, "White Gems", 5e7,"Crystal")),
          ("200Sp White Gems: 80M Crystal", lambda: reset_button(2e26, "White Gems", 8e7,"Crystal")),
          ("750Sp White Gems: 250M Crystal", lambda: reset_button(7.5e26, "White Gems", 2.5e8,"Crystal")),
          ("6Oc White Gems: 600M Crystal", lambda: reset_button(6e27, "White Gems", 6e8,"Crystal")),
          ("250Oc White Gems: 2B Crystal", lambda: reset_button(2.5e29, "White Gems", 2e9,"Crystal")),
          ("850Oc White Gems: 25B Crystal", lambda: reset_button(8.5e29, "White Gems", 2.5e10,"Crystal")),
      ],
      "Iron": [
          ("750M Crystal: 720 Iron", lambda: reset_button(7.5e8, "Crystal", 720,"Iron")),
          ("1.8B Crystal: 3k Iron", lambda: reset_button(1.8e9, "Crystal", 3e3,"Iron")),
          ("11B Crystal: 7.5k Iron", lambda: reset_button(1.1e10, "Crystal", 7.5e3,"Iron")),
          ("35B Crystal: 18k Iron", lambda: reset_button(3.5e10, "Crystal", 1.8e4,"Iron")),
          ("100B Crystal: 45k Iron", lambda: reset_button(1e11, "Crystal", 4.5e4,"Iron")),
          ("500B Crystal: 100k Iron", lambda: reset_button(5e11, "Crystal", 1e5,"Iron")),
      ],
      "Gold": [
          ("45k Iron: 1 Gold", lambda: reset_button(4.5e4, "Iron", 1,"Gold")),
          ("200k Iron: 5 Gold", lambda: reset_button(2e5, "Iron", 5,"Gold")),
          ("500k Iron: 25 Gold", lambda: reset_button(5e5, "Iron", 25,"Gold")),
      ],
      "Gem Buttons": [
          ("600k Iron: 100 Gems", lambda: cost_button("Iron",6e5, "Gems", 100)),
          ("1e98 Rebirths: 400 Gems", lambda: cost_button("Rebirths",1e98, "Gems", 400)),
          ("600T Crystal: 500 Gems", lambda: cost_button("Crystal",6e14, "Gems", 500)),
          ("100De White Gems: 600 Gems", lambda: cost_button("White Gems",1e35, "Gems", 600)),
          ("1e172 Multiplier: 750 Gems", lambda: cost_button("Multiplier",1e172, "Gems", 750)),
          ("1e47 Stone: 800 Gems", lambda: cost_button("Stone",1e47, "Gems", 800)),
      ],
      "Geodes": [
          ("Gold Geode: 60 Gold", lambda btn: Geode_roll(btn, gold_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check("S")),
         ("Recover Hall (req: 0 Cash)", lambda: load_check("RH"))
      ]
  }, 750, "Iron", "GQ", voltaic_radar=voltaic_radar)
  Realm(root, { #Quartz Walkway
      "Multiplier": [
          ("1e143 Cash: 3e54 Multiplier", lambda: cost_button("Cash",1e143,"Multiplier", 3e54)),
          ("6e145 Cash: 1.5e55 Multiplier", lambda: cost_button("Cash",6e145,"Multiplier", 1.5e55)),
          ("2e147 Cash: 4e55 Multiplier", lambda: cost_button("Cash",2e147,"Multiplier", 4e55)),
          ("5e148 Cash: 1.2e56 Multiplier", lambda: cost_button("Cash",5e148,"Multiplier", 1.2e56)),
          ("6e149 Cash: 2.3e56 Multiplier", lambda: cost_button("Cash",6e149,"Multiplier", 2.3e56)),
          ("1.25e151 Cash: 6e56 Multiplier", lambda: cost_button("Cash",1.25e151,"Multiplier", 6e56)),
          ("3e151 Cash: 3.5e58 Multiplier", lambda: cost_button("Cash",3e151,"Multiplier", 3.5e58)),
          ("5.2e152 Cash: 6e58 Multiplier", lambda: cost_button("Cash",5.2e152,"Multiplier", 6e58)),
          ("3e153 Cash: 1.25e59 Multiplier", lambda: cost_button("Cash",3e153,"Multiplier", 1.25e59)),
          ("2e155 Cash: 3e59 Multiplier", lambda: cost_button("Cash",2e155,"Multiplier", 3e59)),
          ("5e156 Cash: 1e60 Multiplier", lambda: cost_button("Cash",5e156,"Multiplier", 1e60)),
      ],
      "Rebirths": [
          ("2.5e135 Multiplier: 1e51 Rebirths", lambda: reset_button(2.5e135,"Multiplier",1e51, "Rebirths")),
          ("7.5e137 Multiplier: 7.5e52 Rebirths", lambda: reset_button(7.5e137,"Multiplier",7.5e52, "Rebirths")),
          ("8e139 Multiplier: 3e53 Rebirths", lambda: reset_button(8e139,"Multiplier",3e53, "Rebirths")),
          ("5e141 Multiplier: 7.5e53 Rebirths", lambda: reset_button(5e141,"Multiplier",7.5e53, "Rebirths")),
          ("7.25e142 Multiplier: 1e55 Rebirths", lambda: reset_button(7.25e142,"Multiplier",1e55, "Rebirths")),
          ("8e144 Multiplier: 5e55 Rebirths", lambda: reset_button(8e144,"Multiplier",5e55, "Rebirths")),
          ("6e145 Multiplier: 1.2e56 Rebirths", lambda: reset_button(6e145,"Multiplier",1.2e56, "Rebirths")),
          ("5e171 Multiplier: 1e59 Rebirths", lambda: reset_button(5e171,"Multiplier",1e59, "Rebirths")),
          ("3e187 Multiplier: 1e62 Rebirths", lambda: reset_button(3e187,"Multiplier",1e62, "Rebirths")),
          ("1e206 Multiplier: 1e65 Rebirths", lambda: reset_button(1e206,"Multiplier",1e65, "Rebirths")),
      ],
      "Stone": [
          ("1e148 Rebirths: 1De Stone", lambda: reset_button(1e148, "Rebirths", 1e33, "Stone")),
          ("1.5e154 Rebirths: 50De Stone", lambda: reset_button(1.5e154, "Rebirths", 5e34, "Stone")),
          ("8.5e155 Rebirths: 2e37 Stone", lambda: reset_button(8.5e155, "Rebirths", 2e37, "Stone")),
          ("3e159 Rebirths: 8e37 Stone", lambda: reset_button(3e159, "Rebirths", 8e37, "Stone")),
          ("1.5e164 Rebirths: 6e38 Stone", lambda: reset_button(1.5e164, "Rebirths", 6e38, "Stone")),
          ("1e166 Rebirths: 5e39 Stone", lambda: reset_button(1e166, "Rebirths", 5e39, "Stone")),
          ("7.5e167 Rebirths: 6e40 Stone", lambda: reset_button(7.5e167, "Rebirths", 6e40, "Stone")),
          ("6e169 Rebirths: 2.5e41 Stone", lambda: reset_button(6e169, "Rebirths", 2.5e41, "Stone")),
      ],
      "White Gems": [
          ("1e60 Stone: 1Qd White Gems", lambda: reset_button(1e60, "Stone", 1e15,"White Gems")),
          ("5e62 Stone: 25Qd White Gems", lambda: reset_button(5e62, "Stone", 2.5e16,"White Gems")),
          ("2e64 Stone: 70Qd White Gems", lambda: reset_button(2e64, "Stone", 7e16,"White Gems")),
          ("4.8e65 Stone: 160Qd White Gems", lambda: reset_button(4.8e65, "Stone", 1.6e17,"White Gems")),
          ("6e67 Stone: 300Qd White Gems", lambda: reset_button(6e67, "Stone", 3e17,"White Gems")),
          ("8e68 Stone: 650Qd White Gems", lambda: reset_button(8e68, "Stone", 6.5e17,"White Gems")),
          ("3e70 Stone: 3Qn White Gems", lambda: reset_button(3e70, "Stone", 3e18,"White Gems")),
          ("1.5e73 Stone: 45Qn White Gems", lambda: reset_button(1.5e73, "Stone", 4.5e19,"White Gems")),
          ("8e74 Stone: 125Qn White Gems", lambda: reset_button(8e74, "Stone", 1.25e20,"White Gems")),
          ("8e76 Stone: 600Qn White Gems", lambda: reset_button(8e76, "Stone", 6e20,"White Gems")),
          ("9.5e77 Stone: 3Sx White Gems", lambda: reset_button(9.5e77, "Stone", 3e21,"White Gems")),
      ],
      "Crystal": [
          ("3e37 White Gems: 1T Crystal", lambda: reset_button(3e37, "White Gems", 1e12,"Crystal")),
          ("2e39 White Gems: 15T Crystal", lambda: reset_button(2e39, "White Gems", 1.5e13,"Crystal")),
          ("4e44 White Gems: 75T Crystal", lambda: reset_button(4e44, "White Gems", 7.5e13,"Crystal")),
          ("8e46 White Gems: 200T Crystal", lambda: reset_button(8e46, "White Gems", 2e14,"Crystal")),
          ("5e51 White Gems: 750T Crystal", lambda: reset_button(5e51, "White Gems", 7.5e14,"Crystal")),
          ("7.6e53 White Gems: 3Qd Crystal", lambda: reset_button(7.6e53, "White Gems", 3e15,"Crystal")),
          ("2.5e55 White Gems: 50Qd Crystal", lambda: reset_button(2.5e55, "White Gems", 5e16,"Crystal")),
          ("3.17e56 White Gems: 125Qd Crystal", lambda: reset_button(3.17e56, "White Gems", 1.25e17,"Crystal")),
          ("4.2e58 White Gems: 417Qd Crystal", lambda: reset_button(4.2e58, "White Gems", 4.17e17,"Crystal")),
          ("2.2e61 White Gems: 926Qd Crystal", lambda: reset_button(2.2e61, "White Gems", 9.26e17,"Crystal")),
          ("7.23e62 White Gems: 11Qn Crystal", lambda: reset_button(7.23e62, "White Gems", 1.1e19,"Crystal")),
          ("8.2e64 White Gems: 64Qn Crystal", lambda: reset_button(8.2e64, "White Gems", 6.4e19,"Crystal")),
          ("9.22e65 White Gems: 265Qn Crystal", lambda: reset_button(9.22e65, "White Gems", 2.65e20,"Crystal")),
      ],
      "Iron": [
          ("3Qd Crystal: 600k Iron", lambda: reset_button(3e15, "Crystal", 6e5,"Iron")),
          ("600Qd Crystal: 5M Iron", lambda: reset_button(6e17, "Crystal", 5e6,"Iron")),
          ("25Qn Crystal: 30M Iron", lambda: reset_button(2.5e19, "Crystal", 3e7,"Iron")),
          ("500Qn Crystal: 100M Iron", lambda: reset_button(5e20, "Crystal", 1e8,"Iron")),
          ("21Sx Crystal: 500M Iron", lambda: reset_button(2.1e22, "Crystal", 5e8,"Iron")),
          ("450Sx Crystal: 3B Iron", lambda: reset_button(4.5e23, "Crystal", 3e9,"Iron")),
          ("12Sp Crystal: 15B Iron", lambda: reset_button(1.2e25, "Crystal", 1.5e10,"Iron")),
          ("210Sp Crystal: 40B Iron", lambda: reset_button(2.1e26, "Crystal", 4e10,"Iron")),
          ("4Oc Crystal: 150B Iron", lambda: reset_button(4e27, "Crystal", 1.5e11,"Iron")),
          ("300Oc Crystal: 300B Iron", lambda: reset_button(3e29, "Crystal", 3e11,"Iron")),
          ("5No Crystal: 2T Iron", lambda: reset_button(5e30, "Crystal", 2e12,"Iron")),
          ("250No Crystal: 36T Iron", lambda: reset_button(2.5e32, "Crystal", 3.6e13,"Iron")),
      ],
      "Gold": [
          ("1M Iron: 75 Gold", lambda: reset_button(1e6, "Iron", 75,"Gold")),
          ("50M Iron: 300 Gold", lambda: reset_button(5e7, "Iron", 300,"Gold")),
          ("200M Iron: 800 Gold", lambda: reset_button(2e8, "Iron", 800,"Gold")),
          ("1B Iron: 1.5k Gold", lambda: reset_button(1e9, "Iron", 1500,"Gold")),
          ("45B Iron: 6k Gold", lambda: reset_button(4.5e10, "Iron", 6000,"Gold")),
      ],
      "Quartz": [
          ("2.5k Gold: 1 Quartz", lambda: reset_button(2.5e3, "Gold", 1,"Quartz")),
          ("7k Gold: 3 Quartz", lambda: reset_button(7e3, "Gold", 3,"Quartz")),
          ("20k Gold: 10 Quartz", lambda: reset_button(2e4, "Gold", 10,"Quartz")),
          ("55k Gold: 75 Quartz", lambda: reset_button(5.5e4, "Gold", 75,"Quartz")),
      ],
      "Gem Buttons": [
          ("3 Quartz: 70 Gems", lambda: cost_button("Quartz",3, "Gems", 75)),
          ("10 Quartz: 200 Gems", lambda: cost_button("Quartz",10, "Gems", 200)),
          ("50 Quartz: 950 Gems", lambda: cost_button("Quartz",50, "Gems", 950)),
          ("250 Quartz: 2200 Gems", lambda: cost_button("Quartz",250, "Gems", 2200)),
      ],
      "Recovery": [
          ("7k Gems: 1e45 Multiplier (Fetch)", lambda: recovery_button_fetch(7000, "Gems", 1e45, "Multiplier")),
          ("1k Gold: 5M White Gems (Fetch)", lambda: recovery_button_fetch(1000, "Gold", 5e6, "White Gems")),
          ("15 Quartz: 100 Iron (Fetch)", lambda: recovery_button_fetch(15, "Quartz", 100, "Iron")),
      ],
      "Geodes": [
          ("Quartz Geode: 30 Quartz", lambda btn: Geode_roll(btn, quartz_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check("S")),
         ("Recover Hall (req: 0 Cash)", lambda: load_check("RH"))
      ],
      "                                                                                                                                                                                        ": [],
      "                                                                                  ": [
          ("", None, "Label"),
          ("", None, "Label"),
          ("", None, "Label"),
          ("", None, "Label"),
          ("", None, "Label"),
          ("", None, "Label"),
          ("", None, "Label"),
          ("", None, "Label"),
          ("", None, "Label"),
          ("", None, "Label"),
          ("", None, "Label"),
          ("", None, "Label"),
          ("", None, "Label"),
          ("", None, "Label"),
          ("", None, "Label"),
          ("", None, "Label"),
          ("", None, "Label"),
          ("", None, "Label"),
          ("", None, "Label"),
          ("", None, "Label"),
          ("", None, "Label"),
          ("", None, "Label"),
          ("A Banquet only for You?", lambda: load_check("Gluttony"))
      ],
      "                                                                                                                                                                                                                                                                                             ": []
  }, 75, "Gold", "QW", voltaic_radar=voltaic_radar)
  Realm(root, { #Jade Forest
      "Multiplier": [
          ("1e301 Cash: 1e75 Multiplier", lambda: cost_button("Cash",Mantissa(1,301),"Multiplier", 1e75)),
          ("5e308 Cash: 5e81 Multiplier", lambda: cost_button("Cash",Mantissa(5,308),"Multiplier", 5e81)),
          ("1e316 Cash: 3e83 Multiplier", lambda: cost_button("Cash",Mantissa(1,316),"Multiplier", 3e83)),
          ("4e320 Cash: 2.5e85 Multiplier", lambda: cost_button("Cash",Mantissa(4,320),"Multiplier", 2.5e85)),
          ("3e322 Cash: 1.6e86 Multiplier", lambda: cost_button("Cash",Mantissa(3,322),"Multiplier", 1.6e86)),
          ("2.2e323 Cash: 4.5e86 Multiplier", lambda: cost_button("Cash",Mantissa(2.2,323),"Multiplier", 4.5e86)),
          ("1.6e325 Cash: 1e88 Multiplier", lambda: cost_button("Cash",Mantissa(1.6,325),"Multiplier", 1e88)),
          ("3e326 Cash: 2.5e88 Multiplier", lambda: cost_button("Cash",Mantissa(3,326),"Multiplier", 2.5e88)),
          ("8e326 Cash: 6.6e88 Multiplier", lambda: cost_button("Cash",Mantissa(8,326),"Multiplier", 6.6e88)),
          ("1.2e328 Cash: 1.4e89 Multiplier", lambda: cost_button("Cash",Mantissa(1.2,328),"Multiplier", 1.4e89)),
          ("7.2e328 Cash: 4.1e89 Multiplier", lambda: cost_button("Cash",Mantissa(7.2,328),"Multiplier", 4.1e89)),
          ("2.8e329 Cash: 2e90 Multiplier", lambda: cost_button("Cash",Mantissa(2.8,329),"Multiplier", 2e90)),
          ("7.5e329 Cash: 3.6e91 Multiplier", lambda: cost_button("Cash",Mantissa(7.5,329),"Multiplier", 3.6e91)),
          ("1e331 Cash: 9e91 Multiplier", lambda: cost_button("Cash",Mantissa(1,331),"Multiplier", 9e91)),
          ("8e331 Cash: 3.1e92 Multiplier", lambda: cost_button("Cash",Mantissa(8,331),"Multiplier", 3.1e92)),
          ("4.5e332 Cash: 7.2e92 Multiplier", lambda: cost_button("Cash",Mantissa(4.5,332),"Multiplier", 7.2e92)),
          ("1e333 Cash: 2e93 Multiplier", lambda: cost_button("Cash",Mantissa(1,333),"Multiplier", 2e93)),
      ],
      "Rebirths": [
          ("1e269 Multiplier: 3e70 Rebirths", lambda: reset_button(1e269,"Multiplier",3e70, "Rebirths")),
          ("3e285 Multiplier: 1.5e74 Rebirths", lambda: reset_button(3e285,"Multiplier",1.5e74, "Rebirths")),
          ("1e295 Multiplier: 4e76 Rebirths", lambda: reset_button(1e295,"Multiplier",4e76, "Rebirths")),
          ("4e299 Multiplier: 5e77 Rebirths", lambda: reset_button(4e299,"Multiplier",5e77, "Rebirths")),
          ("5e301 Multiplier: 3e79 Rebirths", lambda: reset_button(Mantissa(5,301),"Multiplier",3e79, "Rebirths")),
          ("2e305 Multiplier: 2e80 Rebirths", lambda: reset_button(Mantissa(2,305),"Multiplier",2e80, "Rebirths")),
          ("1e307 Multiplier: 7e80 Rebirths", lambda: reset_button(Mantissa(1,307),"Multiplier",7e80, "Rebirths")),
          ("6e308 Multiplier: 1e82 Rebirths", lambda: reset_button(Mantissa(6,308),"Multiplier",1e82, "Rebirths")),
          ("4e310 Multiplier: 6e82 Rebirths", lambda: reset_button(Mantissa(4,310),"Multiplier",6e82, "Rebirths")),
          ("2e311 Multiplier: 2e83 Rebirths", lambda: reset_button(Mantissa(2,311),"Multiplier",2e83, "Rebirths")),
          ("1e312 Multiplier: 1e84 Rebirths", lambda: reset_button(Mantissa(1,312),"Multiplier",1e84, "Rebirths")),
      ],
      "Stone": [
          ("1e181 Rebirths: 2e46 Stone", lambda: reset_button(1e181, "Rebirths", 2e46, "Stone")),
          ("1.6e185 Rebirths: 5.3e46 Stone", lambda: reset_button(1.6e185, "Rebirths", 5.3e46, "Stone")),
          ("6e188 Rebirths: 1.75e47 Stone", lambda: reset_button(6e188, "Rebirths", 1.75e47, "Stone")),
          ("1.5e191 Rebirths: 5e47 Stone", lambda: reset_button(1.5e191, "Rebirths", 5e47, "Stone")),
          ("9e191 Rebirths: 3e48 Stone", lambda: reset_button(9e191, "Rebirths", 3e48, "Stone")),
          ("1e193 Rebirths: 2.4e49 Stone", lambda: reset_button(1e193, "Rebirths", 2.4e49, "Stone")),
          ("1.75e194 Rebirths: 7.5e49 Stone", lambda: reset_button(1.75e194, "Rebirths", 7.5e49, "Stone")),
          ("8.5e194 Rebirths: 3e50 Stone", lambda: reset_button(8.5e194, "Rebirths", 3e50, "Stone")),
      ],
      "White Gems": [
          ("1e82 Stone: 15Sx White Gems", lambda: reset_button(1e82, "Stone", 1.5e22,"White Gems")),
          ("2.5e83 Stone: 60Sx White Gems", lambda: reset_button(2.5e83, "Stone", 6e22,"White Gems")),
          ("8e83 Stone: 300Sx White Gems", lambda: reset_button(8e83, "Stone", 3e23,"White Gems")),
          ("5e85 Stone: 750Sx White Gems", lambda: reset_button(5e85, "Stone", 7.5e23,"White Gems")),
          ("2.5e86 Stone: 25Sp White Gems", lambda: reset_button(2.5e86, "Stone", 2.5e25,"White Gems")),
          ("7.7e86 Stone: 150Sp White Gems", lambda: reset_button(7.7e86, "Stone", 1.5e26,"White Gems")),
          ("8e88 Stone: 500Sp White Gems", lambda: reset_button(8e88, "Stone", 5e26,"White Gems")),
          ("3e89 Stone: 10Oc White Gems", lambda: reset_button(3e89, "Stone", 1e28,"White Gems")),
          ("1e90 Stone: 75Oc White Gems", lambda: reset_button(1e90, "Stone", 7.5e28,"White Gems")),
      ],
      "Crystal": [
          ("4.2e70 White Gems: 5Sx Crystal", lambda: reset_button(4.2e70, "White Gems", 5e21,"Crystal")),
          ("3.5e71 White Gems: 30Sx Crystal", lambda: reset_button(3.5e71, "White Gems", 3e22,"Crystal")),
          ("9e71 White Gems: 70Sx Crystal", lambda: reset_button(9e71, "White Gems", 7e22,"Crystal")),
          ("3e73 White Gems: 400Sx Crystal", lambda: reset_button(3e73, "White Gems", 4e23,"Crystal")),
          ("2e74 White Gems: 750Sx Crystal", lambda: reset_button(2e74, "White Gems", 7.5e23,"Crystal")),
          ("6.5e74 White Gems: 15Sp Crystal", lambda: reset_button(6.5e74, "White Gems", 1.5e25,"Crystal")),
          ("2.5e76 White Gems: 50Sp Crystal", lambda: reset_button(2.5e76, "White Gems", 5e25,"Crystal")),
          ("3e77 White Gems: 120Sp Crystal", lambda: reset_button(3e77, "White Gems", 1.2e26,"Crystal")),
          ("1e79 White Gems: 500Sp Crystal", lambda: reset_button(1e79, "White Gems", 5e26,"Crystal")),
          ("2.5e80 White Gems: 30Oc Crystal", lambda: reset_button(2.5e80, "White Gems", 3e28,"Crystal")),
      ],
      "Iron": [
          ("10De Crystal: 250T Iron", lambda: reset_button(1e34, "Crystal", 2.5e14,"Iron")),
          ("200De Crystal: 725T Iron", lambda: reset_button(2e35, "Crystal", 7.25e14,"Iron")),
          ("1e37 Crystal: 15Qd Iron", lambda: reset_button(1e37, "Crystal", 1.5e16,"Iron")),
          ("1.75e38 Crystal: 40Qd Iron", lambda: reset_button(1.75e38, "Crystal", 4e16,"Iron")),
          ("3e40 Crystal: 250Qd Iron", lambda: reset_button(3e40, "Crystal", 2.5e17,"Iron")),
          ("1.5e41 Crystal: 800Qd Iron", lambda: reset_button(1.5e41, "Crystal", 8e17,"Iron")),
          ("7.5e41 Crystal: 10Qn Iron", lambda: reset_button(7.5e41, "Crystal", 1e19,"Iron")),
          ("3e43 Crystal: 60Qn Iron", lambda: reset_button(3e43, "Crystal", 6e19,"Iron")),
          ("5e44 Crystal: 200Qn Iron", lambda: reset_button(5e44, "Crystal", 2e20,"Iron")),
          ("2e46 Crystal: 800Qn Iron", lambda: reset_button(2e46, "Crystal", 8e20,"Iron")),
          ("1.2e47 Crystal: 50Sx Iron", lambda: reset_button(1.2e47, "Crystal", 5e22,"Iron")),
          ("6e47 Crystal: 120Sx Iron", lambda: reset_button(6e47, "Crystal", 1.2e23,"Iron")),
          ("3e48 Crystal: 550Sx Iron", lambda: reset_button(3e48, "Crystal", 5.5e23,"Iron")),
      ],
      "Gold": [
          ("300B Iron: 100k Gold", lambda: reset_button(3e11, "Iron", 1e5,"Gold")),
          ("900T Iron: 500k Gold", lambda: reset_button(9e14, "Iron", 5e5,"Gold")),
          ("10Qd Iron: 3M Gold", lambda: reset_button(1e16, "Iron", 3e6,"Gold")),
          ("50Qn Iron: 20M Gold", lambda: reset_button(5e19, "Iron", 2e7,"Gold")),
          ("300Sx Iron: 100M Gold", lambda: reset_button(3e23, "Iron", 1e8,"Gold")),
          ("1Sp Iron: 750M Gold", lambda: reset_button(1e24, "Iron", 7.5e8,"Gold")),
      ],
      "Quartz": [
          ("400k Gold: 200 Quartz", lambda: reset_button(4e5, "Gold", 200,"Quartz")),
          ("15M Gold: 1k Quartz", lambda: reset_button(1.5e7, "Gold", 1000,"Quartz")),
          ("250M Gold: 5k Quartz", lambda: reset_button(2.5e8, "Gold", 5000,"Quartz")),
          ("5B Gold: 30k Quartz", lambda: reset_button(5e9, "Gold", 3e4,"Quartz")),
      ],
      "Jade": [
          ("1k Quartz: 1 Jade", lambda: reset_button(1000, "Quartz", 1,"Jade")),
          ("20k Quartz: 5 Jade", lambda: reset_button(2e4, "Quartz", 5,"Jade")),
          ("500k Quartz: 24 Jade", lambda: reset_button(5e5, "Quartz", 24,"Jade")),
      ],
      "Gem Buttons": [
          ("10 Jade: 1k Gems", lambda: cost_button("Jade",10, "Gems", 1000)),
      ],
      "Recovery": [
          ("300 Quartz: 1e67 Rebirths (Fetch)", lambda: recovery_button_fetch(300, "Quartz", 1e67, "Rebirths")),
          ("1M Gold: 1No Stone (Fetch)", lambda: recovery_button_fetch(1e6, "Gold", 1e30, "Stone")),
          ("2 Jade: 15Sx Crystal (Fetch)", lambda: recovery_button_fetch(2, "Jade", 1.5e22, "Crystal")),
      ],
      "Geodes": [
           ("Emoji Geode: 1k Gems", lambda btn: Geode_roll(btn, emoji_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check("S")),
         ("Recover Hall (req: 0 Cash)", lambda: load_check("RH"))
      ]
  }, 450, "Quartz", "JF", voltaic_radar=voltaic_radar)
  Realm(root, { #Obsidian Abyss
      "Multiplier": [
          ("1e360 Cash: 1e96 Multiplier", lambda: cost_button("Cash",Mantissa(1,360),"Multiplier", 1e96)),
          ("1e378 Cash: 2e104 Multiplier", lambda: cost_button("Cash",Mantissa(1,378),"Multiplier", 2e104)),
          ("1e399 Cash: 1.2e110 Multiplier", lambda: cost_button("Cash",Mantissa(1,399),"Multiplier", 1.2e110)),
          ("1e432 Cash: 5e122 Multiplier", lambda: cost_button("Cash",Mantissa(1,432),"Multiplier", 5e122)),
      ],
      "Rebirths": [
          ("3e324 Multiplier: 2e93 Rebirths", lambda: reset_button(Mantissa(3,324),"Multiplier",2e93, "Rebirths")),
          ("1.5e340 Multiplier: 8e99 Rebirths", lambda: reset_button(Mantissa(1.5,340),"Multiplier",8e99, "Rebirths")),
          ("5e365 Multiplier: 1e108 Rebirths", lambda: reset_button(Mantissa(5,365),"Multiplier",1e108, "Rebirths")),
          ("2e398 Multiplier: 6e124 Rebirths", lambda: reset_button(Mantissa(2,398),"Multiplier",6e124, "Rebirths")),
          ("4e412 Multiplier: 1e141 Rebirths", lambda: reset_button(Mantissa(4,412),"Multiplier",1e141, "Rebirths")),
      ],
      "Stone": [
          ("6e213 Rebirths: 1e68 Stone", lambda: reset_button(6e213, "Rebirths", 1e68, "Stone")),
          ("7e224 Rebirths: 2e76 Stone", lambda: reset_button(7e224, "Rebirths", 2e76, "Stone")),
          ("2e245 Rebirths: 1.5e98 Stone", lambda: reset_button(2e245, "Rebirths", 1.5e98, "Stone")),
          ("6.5e258 Rebirths: 5e106 Stone", lambda: reset_button(6.5e258, "Rebirths", 5e106, "Stone")),
          ("2.1e265 Rebirths: 7e110 Stone", lambda: reset_button(2.1e265, "Rebirths", 7e110, "Stone")),
          ("1e274 Rebirths: 3.5e117 Stone", lambda: reset_button(1e274, "Rebirths", 3.5e117, "Stone")),
          ("8.2e292 Rebirths: 1e127 Stone", lambda: reset_button(8.2e292, "Rebirths", 1e127, "Stone")),
      ],
      "White Gems": [
          ("1.5e110 Stone: 210No White Gems", lambda: reset_button(1.5e110, "Stone", 2.1e32,"White Gems")),
          ("3.2e118 Stone: 52De White Gems", lambda: reset_button(3.2e118, "Stone", 5.2e34,"White Gems")),
          ("5e126 Stone: 6e38 White Gems", lambda: reset_button(5e126, "Stone", 6e38,"White Gems")),
          ("8.2e136 Stone: 2.5e42 White Gems", lambda: reset_button(8.2e136, "Stone", 2.5e42,"White Gems")),
          ("5.1e140 Stone: 3.2e46 White Gems", lambda: reset_button(5.1e140, "Stone", 3.2e46,"White Gems")),
          ("1.3e146 Stone: 7.5e51 White Gems", lambda: reset_button(1.3e146, "Stone", 7.5e51,"White Gems")),
          ("5.2e152 Stone: 2.1e57 White Gems", lambda: reset_button(5.2e152, "Stone", 2.1e57,"White Gems")),
          ("1.3e176 Stone: 1e60 White Gems", lambda: reset_button(1.3e176, "Stone", 1e60,"White Gems")),
      ],
      "Crystal": [
          ("3.2e90 White Gems: 210Oc Crystal", lambda: reset_button(3.2e90, "White Gems", 2.1e29,"Crystal")),
          ("3.2e90 White Gems: 210Oc Crystal", lambda: reset_button(3.2e90, "White Gems", 2.1e29,"Crystal")),
          ("7.1e112 White Gems: 42No Crystal", lambda: reset_button(7.1e112, "White Gems", 4.2e30,"Crystal")),
          ("4.2e123 White Gems: 6.2e36 Crystal", lambda: reset_button(4.2e123, "White Gems", 6.2e36,"Crystal")),
          ("3.3e131 White Gems: 5.3e41 Crystal", lambda: reset_button(3.3e131, "White Gems", 5.3e41,"Crystal")),
          ("7.2e139 White Gems: 9.1e48 Crystal", lambda: reset_button(7.2e139, "White Gems", 9.1e48,"Crystal")),
          ("5.6e143 White Gems: 2e49 Crystal", lambda: reset_button(5.6e143, "White Gems", 2e49,"Crystal")),
          ("6.2e150 White Gems: 1.5e57 Crystal", lambda: reset_button(6.2e150, "White Gems", 1.5e57,"Crystal")),
          ("1e180 White Gems: 5e65 Crystal", lambda: reset_button(1e180, "White Gems", 5e65,"Crystal")),
      ],
      "Iron": [
          ("3.2e51 Crystal: 120Sx Iron", lambda: reset_button(3.2e51, "Crystal", 1.2e23,"Iron")),
          ("1.3e55 Crystal: 35Sp Iron", lambda: reset_button(1.3e55, "Crystal", 3.5e25,"Iron")),
          ("7.2e60 Crystal: 16Oc Iron", lambda: reset_button(7.2e60, "Crystal", 1.6e28,"Iron")),
          ("2.1e67 Crystal: 32No Iron", lambda: reset_button(2.1e67, "Crystal", 3.2e31,"Iron")),
          ("1e74 Crystal: 500De Iron", lambda: reset_button(1e74, "Crystal", 5e35,"Iron")),
      ],
      "Gold": [
          ("300Sp Iron: 2.1B Gold", lambda: reset_button(3e26, "Iron", 2.1e9,"Gold")),
          ("6.2No Iron: 62B Gold", lambda: reset_button(6.2e30, "Iron", 6.2e10,"Gold")),
          ("150De Iron: 210B Gold", lambda: reset_button(1.5e35, "Iron", 2.1e11,"Gold")),
          ("6.2e38 Iron: 15T Gold", lambda: reset_button(6.2e38, "Iron", 1.5e13,"Gold")),
      ],
      "Quartz": [
          ("230B Gold: 70k Quartz", lambda: reset_button(2.3e11, "Gold", 7e4,"Quartz")),
          ("4.2T Gold: 230k Quartz", lambda: reset_button(4.2e12, "Gold", 2.3e5,"Quartz")),
          ("84T Gold: 750k Quartz", lambda: reset_button(8.4e13, "Gold", 7.5e5,"Quartz")),
          ("1.1Qd Gold: 3M Quartz", lambda: reset_button(1.1e15, "Gold", 3e6,"Quartz")),
          ("750Qd Gold: 8M Quartz", lambda: reset_button(7.5e17, "Gold", 8e6,"Quartz")),
          ("3.2Sx Gold: 300M Quartz", lambda: reset_button(3.2e21, "Gold", 3e8,"Quartz")),
          ("710Sx Gold: 5B Quartz", lambda: reset_button(7.1e23, "Gold", 5e9,"Quartz")),
      ],
      "Jade": [
          ("10M Quartz: 80 Jade", lambda: reset_button(1e7, "Quartz", 80,"Jade")),
          ("200M Quartz: 300 Jade", lambda: reset_button(2e8, "Quartz", 300,"Jade")),
          ("5B Quartz: 1k Jade", lambda: reset_button(5e9, "Quartz", 1000,"Jade")),
          ("400B Quartz: 7.5k Jade", lambda: reset_button(4e11, "Quartz", 7500,"Jade")),
          ("69T Quartz: 75.42k Jade", lambda: reset_button(6.9e13, "Quartz", 7.542e4,"Jade")),
      ],
      "Obsidian": [
          ("75k Jade: 1 Obsidian", lambda: reset_button(7.5e5, "Jade", 1,"Obsidian")),
      ],
      "Gem Buttons": [
          ("150 Jade: 17.5k Gems", lambda: cost_button("Jade", 150, "Gems", 17500)),
          ("25M Quartz: 50k Gems", lambda: cost_button("Quartz", 2.5e7, "Gems", 5e4)),
      ],
      "Recovery": [
          ("100 Jade: 5.2T White Gems (Fetch)", lambda: recovery_button_fetch(100, "Jade", 5.2e12, "White Gems")),
      ],
      "Geodes": [
          ("Obsidian Geode: 1 Obsidian", lambda btn: Geode_roll(btn, obsidian_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check("S")),
         ("Recover Hall (req: 0 Cash)", lambda: load_check("RH"))
      ]
  }, 80, "Jade", "OA", voltaic_radar=voltaic_radar)
  Realm(root, { #Colour Temple
      "Multiplier": [
          ("3e955 Cash: 6e200 Multiplier", lambda: cost_button("Cash",Mantissa(3,955),"Multiplier", 6e200)),
          ("7e1555 Cash: 1e500 Multiplier", lambda: cost_button("Cash",Mantissa(7,1555),"Multiplier", Mantissa(1,500))),
          ("1e2062 Cash: 1e800 Multiplier", lambda: cost_button("Cash",Mantissa(1,2062),"Multiplier", Mantissa(1,800))),
      ],
      "Rebirths": [
          ("6e751 Multiplier: 2e190 Rebirths", lambda: reset_button(Mantissa(6,751),"Multiplier",2e190, "Rebirths")),
          ("3e1252 Multiplier: 9e300 Rebirths", lambda: reset_button(Mantissa(3,1252),"Multiplier",Mantissa(9,300), "Rebirths")),
          ("1e1626 Multiplier: 5e450 Rebirths", lambda: reset_button(Mantissa(1,1626),"Multiplier",Mantissa(5,450), "Rebirths")),
      ],
      "Stone": [
          ("5e451 Rebirths: 3e185 Stone", lambda: reset_button(Mantissa(5,451), "Rebirths", 3e185, "Stone")),
          ("3e632 Rebirths: 1e255 Stone", lambda: reset_button(Mantissa(3,632), "Rebirths", 1e255, "Stone")),
          ("6e952 Rebirths: 7e312 Stone", lambda: reset_button(Mantissa(6,952), "Rebirths", Mantissa(7,312), "Stone")),
      ],
      "White Gems": [
          ("4e267 Stone: 5e80 White Gems", lambda: reset_button(4e267, "Stone", 5e80,"White Gems")),
          ("1e527 Stone: 2e120 White Gems", lambda: reset_button(Mantissa(1,527), "Stone", 2e120,"White Gems")),
          ("1e637 Stone: 6e135 White Gems", lambda: reset_button(Mantissa(1,637), "Stone", 6e135,"White Gems")),
      ],
      "Crystal": [
          ("2e230 White Gems: 3e102 Crystal", lambda: reset_button(2e230, "White Gems", 3e102,"Crystal")),
          ("5e310 White Gems: 4e141 Crystal", lambda: reset_button(Mantissa(5,310), "White Gems", 4e141,"Crystal")),
          ("3e382 White Gems: 7e182 Crystal", lambda: reset_button(Mantissa(3,382), "White Gems", 7e182,"Crystal")),
      ],
      "Iron": [
          ("3e300 Crystal: 2e62 Iron", lambda: reset_button(Mantissa(3,300), "Crystal", 2e62,"Iron")),
          ("1e380 Crystal: 3e81 Iron", lambda: reset_button(Mantissa(1,380), "Crystal", 3e81,"Iron")),
          ("5e462 Crystal: 1e102 Iron", lambda: reset_button(Mantissa(5,462), "Crystal", 1e102,"Iron")),
      ],
      "Gold": [
          ("3e100 Iron: 3Qd Gold", lambda: reset_button(3e100, "Iron", 3e15,"Gold")),
          ("1e140 Iron: 60Qd Gold", lambda: reset_button(1e150, "Iron", 6e16,"Gold")),
          ("6e190 Iron: 4Qn Gold", lambda: reset_button(6e190, "Iron", 4e18,"Gold")),
      ],
      "Quartz": [
          ("430Sp Gold: 23B Quartz", lambda: reset_button(4.3e26, "Gold", 2.3e10,"Quartz")),
          ("72Oc Gold: 500B Quartz", lambda: reset_button(7.2e28, "Gold", 5e11,"Quartz")),
          ("110No Gold: 30T Quartz", lambda: reset_button(1.1e32, "Gold", 3e13,"Quartz")),
      ],
      "Jade": [
          ("15Qd Quartz: 100k Jade", lambda: reset_button(1.5e16, "Quartz", 1e5,"Jade")),
          ("421Qd Quartz: 250k Jade", lambda: reset_button(4.21e17, "Quartz", 2.5e5,"Jade")),
          ("6Qn Quartz: 825k Jade", lambda: reset_button(6e18, "Quartz", 8.25e5,"Jade")),
      ],
      "Obsidian": [
          ("2M Jade: 3 Obsidian", lambda: reset_button(2e6, "Jade", 3,"Obsidian")),
          ("10M Jade: 7 Obsidian", lambda: reset_button(1e7, "Jade", 7,"Obsidian")),
      ],
      "Ruby": [
          ("60 Obsidian: 1 Ruby", lambda: reset_button( 60, "Obsidian", 1, "Ruby"))
      ],
      "Emerald": [
          ("5 Ruby: 1 Emerald", lambda: cost_button("Ruby",5, "Emerald", 1))
      ],
      "Sapphire": [
          ("5 Emerald: 1 Sapphire", lambda: cost_button( "Emerald", 5, "Sapphire", 1)),
          ("100k Emerald: 4 Sapphire", lambda: cost_button( "Emerald", 100000, "Sapphire", 4)),
      ],
      "Discount": [
          ("1e50 Gems: 1 Mortalstone", lambda: cost_button( "Gems", 1e50, "Mortalstone", 1)),
          ("1M Lollipop: 1 Baryte", lambda: cost_button("Lollipop", 1e6, "Baryte", 1)),
          ("100k Plasma: 1 TRU3_W0RLD", lambda: cost_button("Plasma", 100000, "TRU3_W0RLD", 1)),
          ("1e303030 Stone: 1 Dezyp", lambda: cost_button( "Stone", Mantissa(1,303030), "Dezyp", 1)),
          ("10M Dezyp: 1 Podrillium", lambda: cost_button("Dezyp", 1e7, "Podrillium", 1)),
      ],
      "Geodes": [
          ("Ruby Geode: 100k Ruby", lambda btn: Geode_roll(btn, ruby_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Emerald Geode: 100k Emerald", lambda btn: Geode_roll(btn, emerald_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Sapphire Geode: 100k Sapphire", lambda btn: Geode_roll(btn, sapphire_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check("S")),
         ("Recover Hall (req: 0 Cash)", lambda: load_check("RH"))
      ]
  }, 5, "Obsidian", "CT", voltaic_radar=voltaic_radar)
  Realm(root, { #Extraterrestrial Orbits
      "Tutorial": [
          ("""This place has its own unique gimmick
           everything has its own co-ordinates that you can enter into the control panel.
           I'll give some of them to you here:
           Ruby: 1,935.5286, 1,769.196
           Emerald: 472.739, 1,407.0948
           Sapphire: 260.9568, 105.5747
           Diamond: 230.6099, 369.4198
           Starlight: 1,681.2621, 1,328.7715
           Diamond Geode: 723.3226, 1,851.4675
           Starlight Geode: 154.7922, 923.732
           Ion Geode: 371.111, 1,954.4598
           Stellarite: 3, 40.  8 ,  ,2  .89 7
           The Wormhole: ???, ???
           Recoveries and Area Teleports: 0, 0 (here)
           You won't see this again after you travel, so good luck!""", None, "Label")
      ],#3,040.8689, 7,290.8997
      "Recovery": [
          ("1 Ruby: 50 Jade (Fetch)", lambda: recovery_button_fetch(1, "Ruby", 50, "Jade")),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check("S")),
         ("Recover Hall (req: 0 Cash)", lambda: load_check("RH"))
      ],
      "Miscellanous": [
          ("Control Panel", lambda: open_control_panel(root))
      ]
 }, 50000, "Sapphire", "ET", voltaic_radar=voltaic_radar)
  Realm(root, { #EO Ruby
      "Ruby": [
          ("50Sx Obsidian: 3 Ruby", lambda: reset_button( 5e22, "Obsidian", 3, "Ruby")),
          ("600Sp Obsidian: 10 Ruby", lambda: reset_button( 6e26, "Obsidian", 10, "Ruby")),
          ("20No Obsidian: 40 Ruby", lambda: reset_button( 2e31, "Obsidian", 40, "Ruby")),
      ],
      "Miscellanous": [
          ("Control Panel", lambda: open_control_panel(root))
      ]
  }, 0, "Cash", "ETR", voltaic_radar=voltaic_radar)
  Realm(root, { #EO Emerald
      "Emerald": [
          ("3Qn Ruby: 5 Emerald", lambda: cost_button("Ruby",3e18, "Emerald", 5)),
          ("400Qn Ruby: 14 Emerald", lambda: cost_button("Ruby",4e20, "Emerald", 14)),
          ("10Sx Ruby: 40 Emerald", lambda: cost_button("Ruby",1e22, "Emerald", 40)),
      ],
      "Miscellanous": [
          ("Control Panel", lambda: open_control_panel(root))
      ]
  }, 0, "Cash", "ETE", voltaic_radar=voltaic_radar)
  Realm(root, { #EO Sapphire
      "Sapphire": [
          ("2B Emerald: 10 Sapphire", lambda: cost_button( "Emerald", 2e9, "Sapphire", 10)),
          ("50B Emerald: 30 Sapphire", lambda: cost_button( "Emerald", 5e10, "Sapphire", 30)),
          ("400T Emerald: 100 Sapphire", lambda: cost_button( "Emerald", 4e14, "Sapphire", 100)),
      ],
      "Miscellanous": [
          ("Control Panel", lambda: open_control_panel(root))
      ]
  }, 0, "Cash", "ETS", voltaic_radar=voltaic_radar)
  Realm(root, { #EO Diamond
      "Diamond": [
          ("500k Sapphire: 1 Diamond", lambda: reset_button( 5e5, "Sapphire", 1, "Diamond")),
          ("3M Sapphire: 3 Diamond", lambda: reset_button( 3e6, "Sapphire", 3, "Diamond")),
          ("15M Sapphire: 10 Diamond", lambda: reset_button( 1.5e7, "Sapphire", 10, "Diamond")),
      ],
      "Miscellanous": [
          ("Control Panel", lambda: open_control_panel(root))
      ]
  }, 0, "Cash", "ETD", voltaic_radar=voltaic_radar)
  Realm(root, { #EO Starlight
      "Starlight": [
          ("5 Diamond: 1 Starlight", lambda: reset_button( 5, "Diamond", 1, "Starlight")),
          ("30 Diamond: 4 Starlight", lambda: reset_button( 30, "Diamond", 4, "Starlight")), 
          ("86 Diamond: 10 Starlight", lambda: reset_button( 86, "Diamond", 10, "Starlight")),
      ],
      "Miscellanous": [
          ("Control Panel", lambda: open_control_panel(root))
      ]
  }, 0, "Cash", "ETSL", voltaic_radar=voltaic_radar)
  Realm(root, { #EO DG
      "Geodes": [
          ("Diamond Geode: 2.5k Diamond", lambda btn: Geode_roll(btn, diamond_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll))
      ],
      "Miscellanous": [
          ("Control Panel", lambda: open_control_panel(root))
      ]
  }, 0, "Cash", "ETDG", voltaic_radar=voltaic_radar)
  Realm(root, { #EO SG
      "Geodes": [
          ("Starlight Geode: 60 Starlight", lambda btn: Geode_roll(btn, starlight_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll))
      ],
      "Miscellanous": [
          ("Control Panel", lambda: open_control_panel(root))
      ]
  }, 0 ,"Cash", "ETSG", voltaic_radar=voltaic_radar)
  Realm(root, { #EO IG
      "Geodes": [
        ("Ion Geode: 5 Ion", lambda btn: Geode_roll(btn, ion_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll))
      ],
      "Miscellanous": [
          ("Control Panel", lambda: open_control_panel(root))
      ]
  }, 0, "Cash", "ETIG", voltaic_radar=voltaic_radar)
  Realm(root, { #Stellarite
      "???": [
          ("1 Stellarite (req: 300k Sapphire)", lambda: recovery_button_set( 300000, "Sapphire", 1, "Stellarite")),
          ("Wormhole's Breech (req: 1 Stellarite)", lambda: load_check("WF"))
              ],
      "Miscellanous": [
          ("Control Panel", lambda: open_control_panel(root))
      ]
  }, 0 ,"Cash", "ETSL", voltaic_radar=voltaic_radar)
  Realm(root, { #Empty space
      "Miscellanous": [
          ("Nothing here...", None, "Label"),
          ("Control Panel", lambda: open_control_panel(root))
      ]
  }, 0, "Cash", "ETD", voltaic_radar=voltaic_radar)
  Realm(root, { #Emperyan Island
      "Diamond": [
          ("50M Sapphire: 30 Diamond", lambda: reset_button( 5e7, "Sapphire", 30, "Diamond")),
          ("80M Sapphire: 70 Diamond", lambda: reset_button( 8e7, "Sapphire", 70, "Diamond")),
          ("525B Sapphire: 130 Diamond", lambda: reset_button( 5.25e11, "Sapphire", 130, "Diamond")),
          ("20T Sapphire: 3220 Diamond", lambda: reset_button( 2e13, "Sapphire", 30, "Diamond")),
          ("400Qd Sapphire: 750 Diamond", lambda: reset_button( 4e17, "Sapphire", 750, "Diamond")),
      ],
      "Starlight": [
          ("375 Diamond: 25 Starlight", lambda: reset_button( 375, "Diamond", 25, "Starlight")),
          ("900 Diamond: 40 Starlight", lambda: reset_button( 900, "Diamond", 40, "Starlight")),
          ("5.5k Diamond: 100 Starlight", lambda: reset_button( 5500, "Diamond", 100, "Starlight")),
      ],
      "Ion": [
          ("150 Starlight: 1 Ion", lambda: reset_button( 150, "Starlight", 1, "Ion")),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check("S")),
         ("Recover Hall (req: 0 Cash)", lambda: load_check("RH"))
      ]
  }, 100, "Starlight", "EI", voltaic_radar=voltaic_radar)
  Realm(root, { #Uranium Wastelands
      "Multiplier": [
          ("1e9832 Cash: 1e1500 Multiplier", lambda: cost_button("Cash",Mantissa(1,9832),"Multiplier", Mantissa(1,1500))),
          ("1e16423 Cash: 1e2000 Multiplier", lambda: cost_button("Cash",Mantissa(1,16423),"Multiplier", Mantissa(1,2000))),
          ("1e22547 Cash: 1e2600 Multiplier", lambda: cost_button("Cash",Mantissa(1,22547),"Multiplier", Mantissa(1,2600))),
          ("1e30000 Cash: 1e3400 Multiplier", lambda: cost_button("Cash",Mantissa(1,30000),"Multiplier", Mantissa(1,3400))),
          ("1e50000 Cash: 1e5000 Multiplier", lambda: cost_button("Cash",Mantissa(1,50000),"Multiplier", Mantissa(1,5000))),
      ],
      "Rebirths": [
          ("3e12239 Multiplier: 2e630 Rebirths", lambda: reset_button(Mantissa(3,12239),"Multiplier",Mantissa(2,630), "Rebirths")),
          ("1e19451 Multiplier: 4e825 Rebirths", lambda: reset_button(Mantissa(1,19451),"Multiplier",Mantissa(4,825), "Rebirths")),
          ("6e21534 Multiplier: 5e1004 Rebirths", lambda: reset_button(Mantissa(6,21534),"Multiplier",Mantissa(5,1004), "Rebirths")),
          ("7e27327 Multiplier: 2e3206 Rebirths", lambda: reset_button(Mantissa(7,27327),"Multiplier",Mantissa(2,3206), "Rebirths")),
          ("4e32569 Multiplier: 8e4153 Rebirths", lambda: reset_button(Mantissa(4,32569),"Multiplier",Mantissa(8,4153), "Rebirths")),
      ],
      "Stone": [
          ("3e4533 Rebirths: 2e421 Stone", lambda: reset_button(Mantissa(3,4533), "Rebirths", Mantissa(2,421), "Stone")),
          ("8e6841 Rebirths: 2e482 Stone", lambda: reset_button(Mantissa(8,6841), "Rebirths", Mantissa(2,482), "Stone")),
          ("2e12532 Rebirths: 2e578 Stone", lambda: reset_button(Mantissa(2,12532), "Rebirths", Mantissa(2,578), "Stone")),
          ("8e17627 Rebirths: 3e634 Stone", lambda: reset_button(Mantissa(8,17627), "Rebirths", Mantissa(3,634), "Stone")),
          ("6e26518 Rebirths: 5e752 Stone", lambda: reset_button(Mantissa(6,26518), "Rebirths", Mantissa(5,752), "Stone"))
      ],
      "White Gems": [
          ("4e736 Stone: 8e200 White Gems", lambda: reset_button(Mantissa(4,736), "Stone", 8e200,"White Gems")),
          ("7e958 Stone: 5e273 White Gems", lambda: reset_button(Mantissa(7,958), "Stone", 5e273,"White Gems")),
          ("5e1383 Stone: 2e305 White Gems", lambda: reset_button(Mantissa(5,1383), "Stone", Mantissa(2,305),"White Gems")),
          ("2e1736 Stone: 6e353 White Gems", lambda: reset_button(Mantissa(2,1736), "Stone", Mantissa(6,353),"White Gems")),
          ("7e2484 Stone: 4e436 White Gems", lambda: reset_button(Mantissa(7,2484), "Stone", Mantissa(4,436),"White Gems")),
      ],
      "Crystal": [
          ("9e485 White Gems: 3e211 Crystal", lambda: reset_button(Mantissa(9,485), "White Gems", 3e211,"Crystal")),
          ("6e674 White Gems: 5e236 Crystal", lambda: reset_button(Mantissa(6,674), "White Gems", 5e236,"Crystal")),
          ("2e935 White Gems: 2e254 Crystal", lambda: reset_button(Mantissa(2,935), "White Gems", 2e254,"Crystal")),
          ("4e1335 White Gems: 1e323 Crystal", lambda: reset_button(Mantissa(4,1335), "White Gems", Mantissa(1,323),"Crystal")),
          ("8e2003 White Gems: 1e346 Crystal", lambda: reset_button(Mantissa(8,2003), "White Gems", Mantissa(1,346),"Crystal")),
      ],
      "Iron": [
          ("3e575 Crystal: 5e122 Iron", lambda: reset_button(Mantissa(3,575), "Crystal", 5e122,"Iron")),
          ("6e643 Crystal: 8e150 Iron", lambda: reset_button(Mantissa(6,643), "Crystal", 8e150,"Iron")),
          ("2e721 Crystal: 2e179 Iron", lambda: reset_button(Mantissa(2,721), "Crystal", 2e179,"Iron")),
          ("5e783 Crystal: 6e215 Iron", lambda: reset_button(Mantissa(5,783), "Crystal", 6e215,"Iron")),
          ("8e859 Crystal: 3e249 Iron", lambda: reset_button(Mantissa(8,859), "Crystal", 3e249,"Iron")),
      ],
      "Gold": [
          ("2e303 Iron: 15Qn Gold", lambda: reset_button(Mantissa(2,303), "Iron", 1.5e19,"Gold")),
          ("8e754 Iron: 60Qn Gold", lambda: reset_button(Mantissa(8,754), "Iron", 6e19,"Gold")),
          ("2e1536 Iron: 200Qn Gold", lambda: reset_button(Mantissa(2,1536), "Iron", 2e20,"Gold")),
          ("5e1935 Iron: 4Sx Gold", lambda: reset_button(Mantissa(5,1935), "Iron", 4e21,"Gold")),
          ("8e2389 Iron: 50Sx Gold", lambda: reset_button(Mantissa(8,2389), "Iron", 5e22,"Gold")),
      ],
      "Quartz": [
          ("5e200 Gold: 80Qd Quartz", lambda: reset_button(5e200, "Gold", 8e16,"Quartz")),
          ("3e303 Gold: 300Qd Quartz", lambda: reset_button(Mantissa(3,303), "Gold", 3e17,"Quartz")),
          ("2e609 Gold: 6Qn Quartz", lambda: reset_button(Mantissa(2,609), "Gold", 6e18,"Quartz")),
          ("9e1050 Gold: 25Qn Quartz", lambda: reset_button(Mantissa(9,1050), "Gold", 2.5e19,"Quartz")),
          ("3e3680 Gold: 130Qn Quartz", lambda: reset_button(Mantissa(3,3680), "Gold", 1.3e20,"Quartz")),
      ],
      "Jade": [
          ("1e200 Quartz: 2.5M Jade", lambda: reset_button(1e200, "Quartz", 2.5e6,"Jade")),
          ("5e300 Quartz: 10M Jade", lambda: reset_button(Mantissa(5,300), "Quartz", 1e7,"Jade")),
          ("8e800 Quartz: 35M Jade", lambda: reset_button(Mantissa(8,800), "Quartz", 3.5e7,"Jade")),
          ("3e1100 Quartz: 100M Jade", lambda: reset_button(Mantissa(3,1100), "Quartz", 1e8,"Jade")),
          ("2e1600 Quartz: 500M Jade", lambda: reset_button(Mantissa(2,1600), "Quartz", 5e8,"Jade")),
      ],
      "Obsidian": [
          ("3e60 Jade: 12 Obsidian", lambda: reset_button(3e60, "Jade", 12,"Obsidian")),
          ("6e150 Jade: 25 Obsidian", lambda: reset_button(6e150, "Jade", 25,"Obsidian")),
          ("5e270 Jade: 46 Obsidian", lambda: reset_button(5e270, "Jade", 46,"Obsidian")),
          ("1e500 Jade: 110 Obsidian", lambda: reset_button(Mantissa(1,500), "Jade", 110,"Obsidian")),
          ("1e760 Jade: 180 Obsidian", lambda: reset_button(Mantissa(1,760), "Jade", 180,"Obsidian")),
      ],
      "Ruby": [
          ("1.5e92 Obsidian: 100 Ruby", lambda: reset_button( 1.5e92, "Obsidian", 100, "Ruby")),
          ("5e230 Obsidian: 800 Ruby", lambda: reset_button(5e230, "Obsidian", 800, "Ruby")),
          ("1e620 Obsidian: 3k Ruby", lambda: reset_button( Mantissa(1,620), "Obsidian", 3000, "Ruby")),
      ],
      "Emerald": [
          ("3e53 Ruby: 100 Emerald", lambda: cost_button("Ruby",3e53, "Emerald", 100)),
          ("1e86 Ruby: 500 Emerald", lambda: cost_button("Ruby",1e86, "Emerald", 500)),
          ("3e185 Ruby: 1.2k Emerald", lambda: cost_button("Ruby",3e185, "Emerald", 1200)),
      ],
      "Sapphire": [
          ("50Sx Emerald: 400 Sapphire", lambda: cost_button( "Emerald", 5e22, "Sapphire", 400)),
          ("16No Emerald: 750 Sapphire", lambda: cost_button( "Emerald", 1.6e31, "Sapphire", 750)),
          ("3.47e50 Emerald: 1.22k Sapphire", lambda: cost_button( "Emerald", 3.47e50, "Sapphire", 1220)),
      ],
      "Diamond": [
          ("1Qn Sapphire: 1k Diamond", lambda: reset_button( 1e18, "Sapphire", 1000, "Diamond")),
          ("285Qn Sapphire: 2.5k Diamond", lambda: reset_button( 2.85e20, "Sapphire", 2500, "Diamond")),
          ("57Sx Sapphire: 6.2k Diamond", lambda: reset_button( 5.7e22, "Sapphire", 6200, "Diamond")),
          ("326Sx Sapphire: 13.1k Diamond", lambda: reset_button( 3.26e23, "Sapphire", 13100, "Diamond")),
      ],
      "Starlight": [
          ("2.5M Diamond: 300 Starlight", lambda: reset_button( 2.5e6, "Diamond", 300, "Starlight")),
          ("15M Diamond: 750 Starlight", lambda: reset_button( 1.5e7, "Diamond", 750, "Starlight")),
          ("300M Diamond: 1.6k Starlight", lambda: reset_button( 3e8, "Diamond", 1600, "Starlight")),
          ("2.75B Diamond: 2.8k Starlight", lambda: reset_button( 2.75e9, "Diamond", 2800, "Starlight")),
      ],
      "Ion": [
          ("8k Starlight: 3 Ion", lambda: reset_button( 8000, "Starlight", 3, "Ion")),
          ("50k Starlight: 10 Ion", lambda: reset_button( 50000, "Starlight", 10, "Ion")),
          ("244k Starlight: 25 Ion", lambda: reset_button( 244000, "Starlight", 25, "Ion")),
      ],
      "Uranium": [
          ("30 Ion: 1 Uranium", lambda: reset_button( 30, "Ion", 1, "Uranium")),
          ("100 Ion: 3 Uranium", lambda: reset_button( 100, "Ion", 3, "Uranium")),
      ],
      "Gem Buttons": [
          ("5e41 Sapphire: 250M Gems", lambda: cost_button("Sapphire", 5e41, "Gems", 2.5e8)),
          ("1k Starlight: 800M Gems", lambda: cost_button("Starlight", 1000, "Gems", 8e8)),
          ("7 Ion: 3B Gems", lambda: cost_button("Ion", 7, "Gems", 3e9)),
      ],
      "Geodes": [
          ("Scared Geode: 1B Gems", lambda btn: Geode_roll(btn, sacred_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check("S")),
         ("Recover Hall (req: 0 Cash)", lambda: load_check("RH"))
      ]
  }, 3, "Ion", "UW", voltaic_radar=voltaic_radar)
  Realm(root, { #Smooth Depths
      "Diamond": [
          ("4.6No Sapphire: 700M Diamond", lambda: reset_button( 4.6e30, "Sapphire", 7e8, "Diamond")),
          ("620De Sapphire: 3B Diamond", lambda: reset_button( 6.2e35, "Sapphire", 3e9, "Diamond")),
          ("1.5e38 Sapphire: 50B Diamond", lambda: reset_button( 1.5e38, "Sapphire", 5e10, "Diamond")),
          ("5.3e45 Sapphire: 160B Diamond", lambda: reset_button( 5.3e45, "Sapphire", 1.6e11, "Diamond")),
          ("8.7e52 Sapphire: 500B Diamond", lambda: reset_button( 8.7e52, "Sapphire", 5e11, "Diamond")),
      ],
      "Starlight": [
          ("60B Diamond: 6k Starlight", lambda: reset_button( 6e10, "Diamond", 6000, "Starlight")),
          ("800B Diamond: 50k Starlight", lambda: reset_button( 8e11, "Diamond", 50000, "Starlight")),
          ("75T Diamond: 700k Starlight", lambda: reset_button( 7.5e13, "Diamond", 700000, "Starlight")),
      ],
      "Ion": [
          ("500k Starlight: 100 Ion", lambda: reset_button( 500000, "Starlight", 100, "Ion")),
          ("7M Starlight: 500 Ion", lambda: reset_button( 7e6, "Starlight", 500, "Ion")),
          ("50M Starlight: 2k Ion", lambda: reset_button( 5e7, "Starlight", 2000, "Ion")),
          ("470M Starlight: 17k Ion", lambda: reset_button( 4.7e8, "Starlight", 17000, "Ion")),
          ("850M Starlight: 50k Ion", lambda: reset_button( 8.5e8, "Starlight", 50000, "Ion")),
          ("30B Starlight: 320k Ion", lambda: reset_button( 3e10, "Starlight", 320000, "Ion")),
          ("260B Starlight: 800k Ion", lambda: reset_button( 2.6e11, "Starlight", 800000, "Ion")),
      ],
      "Uranium": [
          ("1.5k Ion: 7 Uranium", lambda: reset_button( 1500, "Ion", 7, "Uranium")),
          ("4k Ion: 25 Uranium", lambda: reset_button( 4000, "Ion", 25, "Uranium")),
          ("20k Ion: 60 Uranium", lambda: reset_button( 20000, "Ion", 60, "Uranium")),
          ("50k Ion: 200 Uranium", lambda: reset_button( 50000, "Ion", 200, "Uranium")),
          ("300k Ion: 500 Uranium", lambda: reset_button( 300000, "Ion", 500, "Uranium")),
      ],
      "Bismuth": [
          ("60 Uranium: 1 Bismuth", lambda: reset_button( 60, "Uranium", 1, "Bismuth")),
          ("500 Uranium: 5 Bismuth", lambda: reset_button( 500, "Uranium", 5, "Bismuth")),
          ("3.7k Uranium: 10 Bismuth", lambda: reset_button( 3700, "Uranium", 10, "Bismuth")),
      ],
      "Recovery": [
          ("1 Bismuth: 800 Diamond (Fetch)", lambda: recovery_button_fetch(1, "Bismuth", 600, "Diamond")),
      ],
      "Geodes": [
          ("Bismuth Geode: 50 Bismuth", lambda btn: Geode_roll(btn, bismuth_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check("S")),
         ("Recover Hall (req: 0 Cash)", lambda: load_check("RH"))
      ]
  }, 15, "Uranium", "SD", voltaic_radar=voltaic_radar)
  Realm(root, { #Icy Palace
      "Diamond": [
          ("1e61 Sapphire: 3T Diamond", lambda: reset_button( 1e61, "Sapphire", 3e12, "Diamond")),
          ("5e74 Sapphire: 25T Diamond", lambda: reset_button( 5e74, "Sapphire", 2.5e13, "Diamond")),
          ("7.3e82 Sapphire: 150T Diamond", lambda: reset_button( 7.3e82, "Sapphire", 1.5e14, "Diamond")),
          ("4.6e89 Sapphire: 2Qd Diamond", lambda: reset_button( 4.6e89, "Sapphire", 2e15, "Diamond")),
          ("7.5e92 Sapphire: 30Qd Diamond", lambda: reset_button( 7.5e92, "Sapphire", 3e16, "Diamond")),
          ("1e95 Sapphire: 200Qd Diamond", lambda: reset_button( 1e95, "Sapphire", 2e17, "Diamond")),
      ],
      "Starlight": [
          ("500T Diamond: 5M Starlight", lambda: reset_button( 5e14, "Diamond", 5e6, "Starlight")),
          ("30Qd Diamond: 30M Starlight", lambda: reset_button( 3e16, "Diamond", 3e7, "Starlight")),
          ("260Qd Diamond: 150M Starlight", lambda: reset_button( 2.6e17, "Diamond", 1.5e8, "Starlight")),
          ("15Qn Diamond: 470M Starlight", lambda: reset_button( 1.5e19, "Diamond", 4.7e8, "Starlight")),
          ("80Qn Diamond: 790M Starlight", lambda: reset_button( 8e19, "Diamond", 7.9e8, "Starlight")),
          ("500Qn Diamond: 5B Starlight", lambda: reset_button( 5e20, "Diamond", 5e9, "Starlight")),
          ("40Sx Diamond: 30B Starlight", lambda: reset_button( 4e22, "Diamond", 3e10, "Starlight")),
          ("170Sx Diamond: 50B Starlight", lambda: reset_button( 1.7e23, "Diamond", 5e10, "Starlight")),
          ("800Sx Diamond: 400B Starlight", lambda: reset_button( 8e23, "Diamond", 4e11, "Starlight")),
      ],
      "Ion": [
          ("50T Starlight: 10M Ion", lambda: reset_button( 5e13, "Starlight", 1e7, "Ion")),
          ("300T Starlight: 40M Ion", lambda: reset_button( 3e14, "Starlight", 4e7, "Ion")),
          ("6Qd Starlight: 90M Ion", lambda: reset_button( 6e15, "Starlight", 9e7, "Ion")),
          ("200Qd Starlight: 150M Ion", lambda: reset_button( 2e17, "Starlight", 1.5e8, "Ion")),
          ("15Qn Starlight: 400M Ion", lambda: reset_button( 1.5e19, "Starlight", 4e8, "Ion")),
          ("250Qn Starlight: 3B Ion", lambda: reset_button( 2.5e20, "Starlight", 3e9, "Ion")),
          ("800Qn Starlight: 14B Ion", lambda: reset_button( 8e20, "Starlight", 1.4e10, "Ion")),
      ],
      "Uranium": [
          ("800M Ion: 5k Uranium", lambda: reset_button( 8e8, "Ion", 5000, "Uranium")),
          ("15B Ion: 14k Uranium", lambda: reset_button( 1.5e10, "Ion", 14000, "Uranium")),
          ("200B Ion: 65k Uranium", lambda: reset_button( 2e11, "Ion", 65000, "Uranium")),
          ("500B Ion: 200k Uranium", lambda: reset_button( 5e11, "Ion", 200000, "Uranium")),
          ("3T Ion: 700k Uranium", lambda: reset_button( 3e12, "Ion", 700000, "Uranium")),
          ("20T Ion: 3M Uranium", lambda: reset_button( 2e13, "Ion", 3e6, "Uranium")),
      ],
      "Bismuth": [
          ("27k Uranium: 30 Bismuth", lambda: reset_button( 27000, "Uranium", 30, "Bismuth")),
          ("120k Uranium: 100 Bismuth", lambda: reset_button( 120000, "Uranium", 100, "Bismuth")),
          ("430k Uranium: 500 Bismuth", lambda: reset_button( 430000, "Uranium", 500, "Bismuth")),
          ("1M Uranium: 1.1k Bismuth", lambda: reset_button( 1e6, "Uranium", 1100, "Bismuth")),
          ("20M Uranium: 3k Bismuth", lambda: reset_button( 2e7, "Uranium", 3000, "Bismuth")),
      ],
      "Boracite": [
          ("3k Bismuth: 1 Boracite", lambda: reset_button( 3000, "Bismuth", 1, "Boracite")),
          ("30k Bismuth: 3 Boracite", lambda: reset_button( 30000, "Bismuth", 3, "Boracite")),
          ("200k Bismuth: 10 Boracite", lambda: reset_button( 200000, "Bismuth", 10, "Boracite")),
      ],
      "Nissonite": [
          ("50 Boracite: 1 Nissonite", lambda: reset_button( 50, "Boracite", 1, "Nissonite")),
      ],
      "Geodes": [
          ("Boracite Geode: 1k Boracite", lambda btn: Geode_roll(btn, boracite_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Nissonite Geode: 5 Nissonite", lambda btn: Geode_roll(btn, nissonite_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check("S")),
         ("Recover Hall (req: 0 Cash)", lambda: load_check("RH"))
      ]
  }, [50,1], ["Bismuth", "Nissonite"], "IP", voltaic_radar=voltaic_radar)
  Realm(root, { #Floating Purgatory
      "Ion": [
          ("500Sx Starlight: 40B Ion", lambda: reset_button( 5e23, "Starlight", 4e10, "Ion")),
          ("200Sp Starlight: 100B Ion", lambda: reset_button( 2e26, "Starlight", 1e11, "Ion")),
          ("15Oc Starlight: 500B Ion", lambda: reset_button( 1.5e28, "Starlight", 5e11, "Ion")),
          ("200Oc Starlight: 5T Ion", lambda: reset_button( 2e29, "Starlight", 5e12, "Ion")),
          ("1.5No Starlight: 75T Ion", lambda: reset_button( 1.5e30, "Starlight", 7.5e13, "Ion")),
          ("80No Starlight: 300T Ion", lambda: reset_button( 8e31, "Starlight", 3e14, "Ion")),
          ("500No Starlight: 1Qd Ion", lambda: reset_button( 5e32, "Starlight", 1e15, "Ion")),
      ],
      "Uranium": [
          ("600Qd Ion: 25M Uranium", lambda: reset_button( 6e17, "Ion", 2.5e7, "Uranium")),
          ("800Qn Ion: 75M Uranium", lambda: reset_button( 8e20, "Ion", 7.5e7, "Uranium")),
          ("300Sx Ion: 250M Uranium", lambda: reset_button( 3e23, "Ion", 2.5e8, "Uranium")),
          ("150Sp Ion: 675M Uranium", lambda: reset_button( 1.5e26, "Ion", 6.75e8, "Uranium")),
          ("930Sp Ion: 5B Uranium", lambda: reset_button( 9.3e26, "Ion", 5e9, "Uranium")),
      ],
      "Bismuth": [
          ("90M Uranium: 5k Bismuth", lambda: reset_button( 9e7, "Uranium", 5000, "Bismuth")),
          ("450M Uranium: 20k Bismuth", lambda: reset_button( 4.5e8, "Uranium", 20000, "Bismuth")),
          ("2B Uranium: 75k Bismuth", lambda: reset_button( 2e9, "Uranium", 75000, "Bismuth")),
          ("30B Uranium: 300k Bismuth", lambda: reset_button( 3e10, "Uranium", 300000, "Bismuth")),
          ("5T Uranium: 500k Bismuth", lambda: reset_button( 5e12, "Uranium", 500000, "Bismuth")),
          ("400T Uranium: 3M Bismuth", lambda: reset_button( 4e14, "Uranium", 3e6, "Bismuth")),
          ("70Qd Uranium: 50M Bismuth", lambda: reset_button( 7e16, "Uranium", 5e7, "Bismuth")),
          ("400Qd Uranium: 130M Bismuth", lambda: reset_button( 4e17, "Uranium", 1.3e8, "Bismuth")),
      ],
      "Boracite": [
          ("1M Bismuth: 40 Boracite", lambda: reset_button( 1e6, "Bismuth", 40, "Boracite")),
          ("500M Bismuth: 120 Boracite", lambda: reset_button( 5e8, "Bismuth", 120, "Boracite")),
          ("75B Bismuth: 350 Boracite", lambda: reset_button( 7.5e10, "Bismuth", 350, "Boracite")),
          ("1T Bismuth: 1k Boracite", lambda: reset_button( 1e12, "Bismuth", 1000, "Boracite")),
          ("45T Bismuth: 4k Boracite", lambda: reset_button( 4.5e13, "Bismuth", 4000, "Boracite")),
          ("600T Bismuth: 9k Boracite", lambda: reset_button( 6e14, "Bismuth", 9000, "Boracite")),
          ("5Qd Bismuth: 15k Boracite", lambda: reset_button( 5e15, "Bismuth", 15000, "Boracite")),
          ("160Qd Bismuth: 60k Boracite", lambda: reset_button( 1.6e17, "Bismuth", 60000, "Boracite")),
          ("764Qd Bismuth: 150k Boracite", lambda: reset_button( 7.64e17, "Bismuth", 150000, "Boracite")),
          ("1Sx Bismuth: 1M Boracite", lambda: reset_button( 1e21, "Bismuth", 1e6, "Boracite")),
          ("50Sx Bismuth: 25M Boracite", lambda: reset_button( 5e22, "Bismuth", 2.5e7, "Boracite")),
          ("1Oc Bismuth: 1T Boracite", lambda: reset_button( 1e27, "Bismuth", 1e12, "Boracite")),
      ],
      "Nissonite": [
          ("300 Boracite: 5 Nissonite", lambda: reset_button( 300, "Boracite", 5, "Nissonite")),
          ("1k Boracite: 10 Nissonite", lambda: reset_button( 1000, "Boracite", 10, "Nissonite")),
          ("7k Boracite: 50 Nissonite", lambda: reset_button( 7000, "Boracite", 50, "Nissonite")),
          ("30k Boracite: 230 Nissonite", lambda: reset_button( 30000, "Boracite", 230, "Nissonite")),
          ("250k Boracite: 650 Nissonite", lambda: reset_button( 250000, "Boracite", 650, "Nissonite")),
          ("40M Boracite: 1.5k Nissonite", lambda: reset_button( 4e7, "Boracite", 1500, "Nissonite")),
          ("600M Boracite: 4k Nissonite", lambda: reset_button( 6e8, "Boracite", 4000, "Nissonite")),
          ("5B Boracite: 12k Nissonite", lambda: reset_button( 5e9, "Boracite", 12000, "Nissonite")),
          ("742B Boracite: 65k Nissonite", lambda: reset_button( 7.42e11, "Boracite", 65000, "Nissonite")),
          ("30T Boracite: 252k Nissonite", lambda: reset_button( 3e13, "Boracite", 252000, "Nissonite")),
          ("160T Boracite: 600k Nissonite", lambda: reset_button( 1.6e14, "Boracite", 600000, "Nissonite")),
          ("500T Boracite: 2M Nissonite", lambda: reset_button( 5e14, "Boracite", 2e6, "Nissonite")),
          ("45Qd Boracite: 50M Nissonite", lambda: reset_button( 4.5e16, "Boracite", 5e7, "Nissonite")),
      ],
      "Orpiment": [
          ("1B Nissonite: 1 Orpiment", lambda: reset_button( 1e9, "Nissonite", 1, "Orpiment")),
          ("10B Nissonite: 4 Orpiment", lambda: reset_button( 1e10, "Nissonite", 4, "Orpiment")),
          ("500B Nissonite: 18 Orpiment", lambda: reset_button( 5e11, "Nissonite", 18, "Orpiment")),
          ("7.5T Nissonite: 30 Orpiment", lambda: reset_button( 7.5e12, "Nissonite", 30, "Orpiment")),
          ("50T Nissonite: 50 Orpiment", lambda: reset_button( 5e13, "Nissonite", 50, "Orpiment")),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check("S")),
         ("Recover Hall (req: 0 Cash)", lambda: load_check("RH"))
      ]
  }, 10, "Nissonite", "FP", voltaic_radar=voltaic_radar)
  Realm(root, { #Tetratum
      "Boracite": [
          ("1e63 Bismuth: 20T Boracite", lambda: reset_button( 1e63, "Bismuth", 2e13, "Boracite")),
          ("1e78 Bismuth: 500T Boracite", lambda: reset_button( 1e78, "Bismuth", 5e14, "Boracite")),
          ("1e93 Bismuth: 8Qd Boracite", lambda: reset_button( 1e93, "Bismuth", 8e15, "Boracite")),
          ("1e105 Bismuth: 75Qd Boracite", lambda: reset_button( 1e105, "Bismuth", 7.5e16, "Boracite")),
          ("1e123 Bismuth: 1Qn Boracite", lambda: reset_button( 1e123, "Bismuth", 1e18, "Boracite")),
          ("1e126 Bismuth: 15Qn Boracite", lambda: reset_button( 1e126, "Bismuth", 1.5e19, "Boracite")),
      ],
      "Nissonite": [
          ("100De Boracite: 200M Nissonite", lambda: reset_button( 1e35, "Boracite", 2e8, "Nissonite")),
          ("1e42 Boracite: 1B Nissonite", lambda: reset_button( 1e42, "Boracite", 1e9, "Nissonite")),
          ("1e50 Boracite: 15B Nissonite", lambda: reset_button( 1e50, "Boracite", 1.5e10, "Nissonite")),
          ("1e52 Boracite: 200B Nissonite", lambda: reset_button( 1e52, "Boracite", 2e11, "Nissonite")),
          ("1e55 Boracite: 2T Nissonite", lambda: reset_button( 1e55, "Boracite", 2e12, "Nissonite")),
          ("1e60 Boracite: 25T Nissonite", lambda: reset_button( 1e60, "Boracite", 2.5e13, "Nissonite")),
      ],
      "Orpiment": [
          ("1Qd Nissonite: 115 Orpiment", lambda: reset_button( 1e15, "Nissonite", 115, "Orpiment")),
          ("25Qd Nissonite: 300 Orpiment", lambda: reset_button( 2.5e16, "Nissonite", 300, "Orpiment")),
          ("175Qd Nissonite: 1.05k Orpiment", lambda: reset_button( 1.75e17, "Nissonite", 1050, "Orpiment")),
          ("4Qn Nissonite: 2.25k Orpiment", lambda: reset_button( 4e18, "Nissonite", 2250, "Orpiment")),
          ("10Qn Nissonite: 5k Orpiment", lambda: reset_button( 1e19, "Nissonite", 5000, "Orpiment")),
      ],
      "Tetra" : [
          ("2.5k Orpiment: 1 Tetra", lambda: reset_button( 2500, "Orpiment", 1, "Tetra")),
          ("200k Orpiment: 4.5 Tetra", lambda: reset_button( 200000, "Orpiment", 4.5, "Tetra")),
          ("1.5M Orpiment: 12 Tetra", lambda: reset_button( 1.5e6, "Orpiment", 12, "Tetra")),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check("S")),
         ("Recover Hall (req: 0 Cash)", lambda: load_check("RH"))
      ],
      "???": [
          ("Graphite Puzzle", lambda: graphite_puzzle(root))
      ]
  }, 500, "Orpiment", "T", voltaic_radar=voltaic_radar)
  Realm(root, { #Voltaic Sector
      "Multiplier": [
          ("1e(2e5) Cash: 1e9003 Multiplier", lambda: cost_button("Cash",Mantissa(1,2e5),"Multiplier", Mantissa(1,9003))),
          ("1e(3e5) Cash: 1e10000 Multiplier", lambda: cost_button("Cash",Mantissa(1,3e5),"Multiplier", Mantissa(1,10000))),
          ("1e(7e5) Cash: 1e11003 Multiplier", lambda: cost_button("Cash",Mantissa(1,7e5),"Multiplier", Mantissa(1,11003))),
          ("1e(8e5) Cash: 1e12003 Multiplier", lambda: cost_button("Cash",Mantissa(1,8e5),"Multiplier", Mantissa(1,12003))),
          ("1e(9e5) Cash: 1e13000 Multiplier", lambda: cost_button("Cash",Mantissa(1,9e5),"Multiplier", Mantissa(1,13000))),
          ("1e(1e6) Cash: 1e14003 Multiplier", lambda: cost_button("Cash",Mantissa(1,1e6),"Multiplier", Mantissa(1,14003))),
          ("1e(1.1e6) Cash: 1e15003 Multiplier", lambda: cost_button("Cash",Mantissa(1,1.1e6),"Multiplier", Mantissa(1,15003))),
          ("1e(1.2e6) Cash: 1e16000 Multiplier", lambda: cost_button("Cash",Mantissa(1,1.2e6),"Multiplier", Mantissa(1,16000))),
          ("1e(1.3e6) Cash: 1e17003 Multiplier", lambda: cost_button("Cash",Mantissa(1,1.3e6),"Multiplier", Mantissa(1,17003))),
          ("1e(1.4e6) Cash: 1e18003 Multiplier", lambda: cost_button("Cash",Mantissa(1,1.4e6),"Multiplier", Mantissa(1,18003))),
          ("1e(1.5e6) Cash: 1e19000 Multiplier", lambda: cost_button("Cash",Mantissa(1,1.5e6),"Multiplier", Mantissa(1,19000))),
          ("1e(1.6e6) Cash: 1e20003 Multiplier", lambda: cost_button("Cash",Mantissa(1.6,1e6),"Multiplier", Mantissa(1,20003))),
          ("1e(1.7e6) Cash: 1e21003 Multiplier", lambda: cost_button("Cash",Mantissa(1,1.7e6),"Multiplier", Mantissa(1,21003))),
          ("1e(1.8e6) Cash: 1e22000 Multiplier", lambda: cost_button("Cash",Mantissa(1,1.8e6),"Multiplier", Mantissa(1,22000))),
      ],
      "Rebirths": [
          ("1e600003 Multiplier: 1e5003 Rebirths", lambda: reset_button(Mantissa(1,600003),"Multiplier",Mantissa(1,5003), "Rebirths")),
          ("1e650003 Multiplier: 1e6003 Rebirths", lambda: reset_button(Mantissa(1,650003),"Multiplier",Mantissa(1,6003), "Rebirths")),
          ("1e700003 Multiplier: 1e7003 Rebirths", lambda: reset_button(Mantissa(1,700003),"Multiplier",Mantissa(1,7003), "Rebirths")),
          ("1e750003 Multiplier: 1e8003 Rebirths", lambda: reset_button(Mantissa(1,750003),"Multiplier",Mantissa(1,8003), "Rebirths")),
          ("1e800003 Multiplier: 1e9003 Rebirths", lambda: reset_button(Mantissa(1,800003),"Multiplier",Mantissa(1,9003), "Rebirths")),
          ("1e850003 Multiplier: 1e10003 Rebirths", lambda: reset_button(Mantissa(1,850003),"Multiplier",Mantissa(1,10003), "Rebirths")),
          ("1e900003 Multiplier: 1e11003 Rebirths", lambda: reset_button(Mantissa(1,900003),"Multiplier",Mantissa(1,11003), "Rebirths")),
          ("1e950003 Multiplier: 1e12003 Rebirths", lambda: reset_button(Mantissa(1,950003),"Multiplier",Mantissa(1,12003), "Rebirths")),
          ("1e1000003 Multiplier: 1e13003 Rebirths", lambda: reset_button(Mantissa(1,1000003),"Multiplier",Mantissa(1,13003), "Rebirths")),
          ("1e1050003 Multiplier: 1e14003 Rebirths", lambda: reset_button(Mantissa(1,1050003),"Multiplier",Mantissa(1,14003), "Rebirths")),
          ("1e1100003 Multiplier: 1e15003 Rebirths", lambda: reset_button(Mantissa(1,1100003),"Multiplier",Mantissa(1,15003), "Rebirths")),
          ("1e1150003 Multiplier: 1e16003 Rebirths", lambda: reset_button(Mantissa(1,1150003),"Multiplier",Mantissa(1,16003), "Rebirths")),
          ("1e1200003 Multiplier: 1e17003 Rebirths", lambda: reset_button(Mantissa(1,1200003),"Multiplier",Mantissa(1,17003), "Rebirths")),
          ("6.9e1250003 Multiplier: 1e18003 Rebirths", lambda: reset_button(Mantissa(6.9,1250003),"Multiplier",Mantissa(1,18003), "Rebirths")),
      ],
      "Stone": [
          ("1e250003 Rebirths: 1e1003 Stone", lambda: reset_button(Mantissa(1,250003), "Rebirths", Mantissa(1,1003), "Stone")),
          ("1e300003 Rebirths: 1e1303 Stone", lambda: reset_button(Mantissa(1,300003), "Rebirths", Mantissa(1,1303), "Stone")),
          ("1e330003 Rebirths: 1e1603 Stone", lambda: reset_button(Mantissa(1,330003), "Rebirths", Mantissa(1,1603), "Stone")),
          ("1e360003 Rebirths: 1e1903 Stone", lambda: reset_button(Mantissa(1,360003), "Rebirths", Mantissa(1,1903), "Stone")),
          ("1e390003 Rebirths: 1e2103 Stone", lambda: reset_button(Mantissa(1,390003), "Rebirths", Mantissa(1,2103), "Stone")),
          ("1e420003 Rebirths: 1e2403 Stone", lambda: reset_button(Mantissa(1,420003), "Rebirths", Mantissa(1,2403), "Stone")),
          ("1e450003 Rebirths: 1e2703 Stone", lambda: reset_button(Mantissa(1,450003), "Rebirths", Mantissa(1,2703), "Stone")),
          ("1e480003 Rebirths: 1e3003 Stone", lambda: reset_button(Mantissa(1,480003), "Rebirths", Mantissa(1,3003), "Stone")),
          ("1e510003 Rebirths: 1e3303 Stone", lambda: reset_button(Mantissa(1,510003), "Rebirths", Mantissa(1,3303), "Stone")),
          ("1e540003 Rebirths: 1e3603 Stone", lambda: reset_button(Mantissa(1,540003), "Rebirths", Mantissa(1,3603), "Stone")),
          ("1e570003 Rebirths: 1e3903 Stone", lambda: reset_button(Mantissa(1,570003), "Rebirths", Mantissa(1,3903), "Stone")),
          ("1e600003 Rebirths: 1e4203 Stone", lambda: reset_button(Mantissa(1,600003), "Rebirths", Mantissa(1,4203), "Stone")),
          ("1e630003 Rebirths: 1e4503 Stone", lambda: reset_button(Mantissa(1,630003), "Rebirths", Mantissa(1,4503), "Stone")),
          ("1e660003 Rebirths: 1e4803 Stone", lambda: reset_button(Mantissa(1,660003), "Rebirths", Mantissa(1,4803), "Stone")),
      ],
      "White Gems": [
          ("1e300003 Stone: 1e603 White Gems", lambda: reset_button(Mantissa(1,300003), "Stone", Mantissa(1,603),"White Gems")),
          ("1e320003 Stone: 1e700 White Gems", lambda: reset_button(Mantissa(1,320003), "Stone", Mantissa(1,700),"White Gems")),
          ("1e340003 Stone: 1e800 White Gems", lambda: reset_button(Mantissa(1,340003), "Stone", Mantissa(1,800),"White Gems")),
          ("1e360003 Stone: 1e903 White Gems", lambda: reset_button(Mantissa(1,360003), "Stone", Mantissa(1,903),"White Gems")),
          ("1e380003 Stone: 1e1000 White Gems", lambda: reset_button(Mantissa(1,380003), "Stone", Mantissa(1,1000),"White Gems")),
          ("1e400003 Stone: 1e1100 White Gems", lambda: reset_button(Mantissa(1,400003), "Stone", Mantissa(1,1100),"White Gems")),
          ("1e420003 Stone: 1e1203 White Gems", lambda: reset_button(Mantissa(1,420003), "Stone", Mantissa(1,1203),"White Gems")),
          ("1e440003 Stone: 1e1300 White Gems", lambda: reset_button(Mantissa(1,440003), "Stone", Mantissa(1,1300),"White Gems")),
          ("1e460003 Stone: 1e1400 White Gems", lambda: reset_button(Mantissa(1,460003), "Stone", Mantissa(1,1400),"White Gems")),
          ("1e480003 Stone: 1e1503 White Gems", lambda: reset_button(Mantissa(1,480003), "Stone", Mantissa(1,1503),"White Gems")),
          ("1e500003 Stone: 1e1600 White Gems", lambda: reset_button(Mantissa(1,500003), "Stone", Mantissa(1,1600),"White Gems")),
          ("1e520003 Stone: 1e1700 White Gems", lambda: reset_button(Mantissa(1,520003), "Stone", Mantissa(1,1700),"White Gems")),
          ("1e540003 Stone: 1e1803 White Gems", lambda: reset_button(Mantissa(1,540003), "Stone", Mantissa(1,1803),"White Gems")),
          ("1e560003 Stone: 1e1900 White Gems", lambda: reset_button(Mantissa(1,560003), "Stone", Mantissa(1,1900),"White Gems")),
      ],
      "Crystal": [
          ("1e200003 White Gems: 1e400 Crystal", lambda: reset_button(Mantissa(1,200003), "White Gems", Mantissa(1,400),"Crystal")),
          ("1e210003 White Gems: 1e450 Crystal", lambda: reset_button(Mantissa(1,210003), "White Gems", Mantissa(1,450),"Crystal")),
          ("1e220003 White Gems: 1e500 Crystal", lambda: reset_button(Mantissa(1,220003), "White Gems", Mantissa(1,500),"Crystal")),
          ("1e230003 White Gems: 1e550 Crystal", lambda: reset_button(Mantissa(1,230003), "White Gems", Mantissa(1,550),"Crystal")),
          ("1e240003 White Gems: 1e600 Crystal", lambda: reset_button(Mantissa(1,240003), "White Gems", Mantissa(1,600),"Crystal")),
          ("1e250003 White Gems: 1e650 Crystal", lambda: reset_button(Mantissa(1,250003), "White Gems", Mantissa(1,650),"Crystal")),
          ("1e260003 White Gems: 1e700 Crystal", lambda: reset_button(Mantissa(1,260003), "White Gems", Mantissa(1,700),"Crystal")),
          ("1e270003 White Gems: 1e750 Crystal", lambda: reset_button(Mantissa(1,270003), "White Gems", Mantissa(1,750),"Crystal")),
          ("1e280003 White Gems: 1e800 Crystal", lambda: reset_button(Mantissa(1,280003), "White Gems", Mantissa(1,800),"Crystal")),
          ("1e290003 White Gems: 1e850 Crystal", lambda: reset_button(Mantissa(1,290003), "White Gems", Mantissa(1,850),"Crystal")),
          ("1e300003 White Gems: 1e900 Crystal", lambda: reset_button(Mantissa(1,300003), "White Gems", Mantissa(1,900),"Crystal")),
          ("1e310003 White Gems: 1e950 Crystal", lambda: reset_button(Mantissa(1,310003), "White Gems", Mantissa(1,950),"Crystal")),
          ("1e320003 White Gems: 1e1000 Crystal", lambda: reset_button(Mantissa(1,320003), "White Gems", Mantissa(1,1000),"Crystal")),
          ("1e330003 White Gems: 1e1050 Crystal", lambda: reset_button(Mantissa(1,330003), "White Gems", Mantissa(1,1050),"Crystal")),
      ],
      "Iron": [
          ("1e200003 Crystal: 1e303 Iron", lambda: reset_button(Mantissa(1,200003), "Crystal", Mantissa(1,303),"Iron")),
          ("1e205003 Crystal: 1e353 Iron", lambda: reset_button(Mantissa(1,205003), "Crystal", Mantissa(1,353),"Iron")),
          ("1e210003 Crystal: 1e403 Iron", lambda: reset_button(Mantissa(1,210003), "Crystal", Mantissa(1,403),"Iron")),
          ("1e215003 Crystal: 1e453 Iron", lambda: reset_button(Mantissa(1,215003), "Crystal", Mantissa(1,453),"Iron")),
          ("1e220003 Crystal: 1e503 Iron", lambda: reset_button(Mantissa(1,220003), "Crystal", Mantissa(1,503),"Iron")),
          ("1e225003 Crystal: 1e553 Iron", lambda: reset_button(Mantissa(1,225003), "Crystal", Mantissa(1,553),"Iron")),
          ("1e230003 Crystal: 1e603 Iron", lambda: reset_button(Mantissa(1,230003), "Crystal", Mantissa(1,603),"Iron")),
          ("1e235003 Crystal: 1e653 Iron", lambda: reset_button(Mantissa(1,235003), "Crystal", Mantissa(1,653),"Iron")),
          ("1e240003 Crystal: 1e703 Iron", lambda: reset_button(Mantissa(1,240003), "Crystal", Mantissa(1,703),"Iron")),
          ("1e245003 Crystal: 1e753 Iron", lambda: reset_button(Mantissa(1,245003), "Crystal", Mantissa(1,753),"Iron")),
          ("1e250003 Crystal: 1e803 Iron", lambda: reset_button(Mantissa(1,250003), "Crystal", Mantissa(1,803),"Iron")),
          ("1e255003 Crystal: 1e853 Iron", lambda: reset_button(Mantissa(1,255003), "Crystal", Mantissa(1,853),"Iron")),
          ("1e260003 Crystal: 1e903 Iron", lambda: reset_button(Mantissa(1,260003), "Crystal", Mantissa(1,903),"Iron")),
          ("1e265003 Crystal: 1e953 Iron", lambda: reset_button(Mantissa(1,265003), "Crystal", Mantissa(1,953),"Iron")),
      ],
      "Gold": [
          ("1e101003 Iron: 1e63 Gold", lambda: reset_button(Mantissa(1,101003), "Iron", 1e63,"Gold")),
          ("1e102003 Iron: 1e80 Gold", lambda: reset_button(Mantissa(1,102003), "Iron", 1e80,"Gold")),
          ("1e103003 Iron: 1e120 Gold", lambda: reset_button(Mantissa(1,103003), "Iron", 1e120,"Gold")),
          ("1e104003 Iron: 1e160 Gold", lambda: reset_button(Mantissa(1,104003), "Iron", 1e160,"Gold")),
          ("1e105003 Iron: 1e200 Gold", lambda: reset_button(Mantissa(1,105003), "Iron", 1e200,"Gold")),
          ("1e106003 Iron: 1e240 Gold", lambda: reset_button(Mantissa(1,106003), "Iron", 1e240,"Gold")),
          ("1e107003 Iron: 1e280 Gold", lambda: reset_button(Mantissa(1,107003), "Iron", 1e280,"Gold")),
          ("1e108003 Iron: 1e320 Gold", lambda: reset_button(Mantissa(1,108003), "Iron", Mantissa(1,320),"Gold")),
          ("1e109003 Iron: 1e360 Gold", lambda: reset_button(Mantissa(1,109003), "Iron", Mantissa(1,360),"Gold")),
          ("1e110003 Iron: 1e400 Gold", lambda: reset_button(Mantissa(1,110003), "Iron", Mantissa(1,400),"Gold")),
          ("1e111003 Iron: 1e440 Gold", lambda: reset_button(Mantissa(1,111003), "Iron", Mantissa(1,440),"Gold")),
          ("1e112003 Iron: 1e480 Gold", lambda: reset_button(Mantissa(1,112003), "Iron", Mantissa(1,480),"Gold")),
          ("1e113003 Iron: 1e520 Gold", lambda: reset_button(Mantissa(1,113003), "Iron", Mantissa(1,520),"Gold")),
          ("1e114003 Iron: 1e560 Gold", lambda: reset_button(Mantissa(1,114003), "Iron", Mantissa(1,560),"Gold")),
      ],
      "Quartz": [
          ("1e60000 Gold: 1Sx Quartz", lambda: reset_button(Mantissa(1,60000), "Gold", 1e21,"Quartz")),
          ("1e62000 Gold: 10No Quartz", lambda: reset_button(Mantissa(1,62000), "Gold", 1e31,"Quartz")),
          ("1e64000 Gold: 1e41 Quartz", lambda: reset_button(Mantissa(1,64000), "Gold", 1e41,"Quartz")),
          ("1e66000 Gold: 1e51 Quartz", lambda: reset_button(Mantissa(1,66000), "Gold", 1e51,"Quartz")),
          ("1e68000 Gold: 1e61 Quartz", lambda: reset_button(Mantissa(1,68000), "Gold", 1e61,"Quartz")),
          ("1e70000 Gold: 1e71 Quartz", lambda: reset_button(Mantissa(1,70000), "Gold", 1e71,"Quartz")),
          ("1e72000 Gold: 1e81 Quartz", lambda: reset_button(Mantissa(1,72000), "Gold", 1e81,"Quartz")),
          ("1e74000 Gold: 1e91 Quartz", lambda: reset_button(Mantissa(1,74000), "Gold", 1e91,"Quartz")),
          ("1e76000 Gold: 1e101 Quartz", lambda: reset_button(Mantissa(1,76000), "Gold", 1e101,"Quartz")),
          ("1e78000 Gold: 1e111 Quartz", lambda: reset_button(Mantissa(1,78000), "Gold", 1e111,"Quartz")),
          ("1e80000 Gold: 1e121 Quartz", lambda: reset_button(Mantissa(1,80000), "Gold", 1e121,"Quartz")),
          ("1e82000 Gold: 1e131 Quartz", lambda: reset_button(Mantissa(1,82000), "Gold", 1e131,"Quartz")),
          ("1e84000 Gold: 1e141 Quartz", lambda: reset_button(Mantissa(1,84000), "Gold", 1e141,"Quartz")),
          ("1e86000 Gold: 1e151 Quartz", lambda: reset_button(Mantissa(1,86000), "Gold", 1e151,"Quartz")),
      ],
      "Jade": [
          ("1e45003 Quartz: 1B Jade", lambda: reset_button(Mantissa(1,45003), "Quartz", 1e9,"Jade")),
          ("1e46003 Quartz: 1T Jade", lambda: reset_button(Mantissa(1,46003), "Quartz", 1e12,"Jade")),
          ("1e47003 Quartz: 1Qd Jade", lambda: reset_button(Mantissa(1,47003), "Quartz", 1e15,"Jade")),
          ("1e48003 Quartz: 1Qn Jade", lambda: reset_button(Mantissa(1,48003), "Quartz", 1e18,"Jade")),
          ("1e49003 Quartz: 1Sx Jade", lambda: reset_button(Mantissa(1,49003), "Quartz", 1e21,"Jade")),
          ("1e50003 Quartz: 1Sp Jade", lambda: reset_button(Mantissa(1,50003), "Quartz", 1e24,"Jade")),
          ("1e51003 Quartz: 1Oc Jade", lambda: reset_button(Mantissa(1,51003), "Quartz", 1e27,"Jade")),
          ("1e52003 Quartz: 1No Jade", lambda: reset_button(Mantissa(1,52003), "Quartz", 1e30,"Jade")),
          ("1e53003 Quartz: 1De Jade", lambda: reset_button(Mantissa(1,53003), "Quartz", 1e33,"Jade")),
          ("1e54003 Quartz: 1e36 Jade", lambda: reset_button(Mantissa(1,54003), "Quartz", 1e36,"Jade")),
          ("1e55003 Quartz: 1e39 Jade", lambda: reset_button(Mantissa(1,55003), "Quartz", 1e39,"Jade")),
          ("1e56003 Quartz: 1e42 Jade", lambda: reset_button(Mantissa(1,56003), "Quartz", 1e42,"Jade")),
          ("1e57003 Quartz: 1e45 Jade", lambda: reset_button(Mantissa(1,57003), "Quartz", 1e45,"Jade")),
          ("1e58003 Quartz: 1e48 Jade", lambda: reset_button(Mantissa(1,58003), "Quartz", 1e48,"Jade")),
      ],
      "Obsidian": [
          ("1e27003 Jade: 1k Obsidian", lambda: reset_button(Mantissa(1,27003), "Jade", 1000,"Obsidian")),
          ("1e27503 Jade: 10k Obsidian", lambda: reset_button(Mantissa(1,27503), "Jade", 10000,"Obsidian")),
          ("1e28003 Jade: 100k Obsidian", lambda: reset_button(Mantissa(1,28003), "Jade", 100000,"Obsidian")),
          ("1e28503 Jade: 1M Obsidian", lambda: reset_button(Mantissa(1,28503), "Jade", 1e6,"Obsidian")),
          ("1e29003 Jade: 10M Obsidian", lambda: reset_button(Mantissa(1,29003), "Jade", 1e7,"Obsidian")),
          ("1e29503 Jade: 100M Obsidian", lambda: reset_button(Mantissa(1,29503), "Jade", 1e8,"Obsidian")),
          ("1e30003 Jade: 1B Obsidian", lambda: reset_button(Mantissa(1,30003), "Jade", 1e9,"Obsidian")),
          ("1e30503 Jade: 10B Obsidian", lambda: reset_button(Mantissa(1,30503), "Jade", 1e10,"Obsidian")),
          ("1e31003 Jade: 100B Obsidian", lambda: reset_button(Mantissa(1,31003), "Jade", 1e11,"Obsidian")),
          ("1e31503 Jade: 1T Obsidian", lambda: reset_button(Mantissa(1,31503), "Jade", 1e12,"Obsidian")),
          ("1e32003 Jade: 10T Obsidian", lambda: reset_button(Mantissa(1,32003), "Jade", 1e13,"Obsidian")),
          ("1e32503 Jade: 100T Obsidian", lambda: reset_button(Mantissa(1,32503), "Jade", 1e14,"Obsidian")),
          ("1e33003 Jade: 1Qd Obsidian", lambda: reset_button(Mantissa(1,33003), "Jade", 1e15,"Obsidian")),
          ("1e33503 Jade: 10Qd Obsidian", lambda: reset_button(Mantissa(1,33503), "Jade", 1e16,"Obsidian")),
      ],
      "Ruby": [
          ("1e15003 Obsidian: 1e93 Ruby", lambda: reset_button( Mantissa(1,15003), "Obsidian", 1e93, "Ruby")),
      ],
      "Emerald": [
          ("1e9003 Ruby: 1e63 Emerald", lambda: cost_button("Ruby",Mantissa(1,9003), "Emerald", 1e63)),
      ],
      "Sapphire": [
          ("1e3003 Emerald: 1De Sapphire", lambda: cost_button( "Emerald", Mantissa(1,3003), "Sapphire", 1e33)),
      ],
      "Diamond": [
          ("1e2703 Sapphire: 1Qn Diamond", lambda: reset_button( Mantissa(1,2703), "Sapphire", 1e18, "Diamond")),
          ("1e2733 Sapphire: 1Sp Diamond", lambda: reset_button( Mantissa(1,2733), "Sapphire", 1e24, "Diamond")),
          ("1e2763 Sapphire: 1No Diamond", lambda: reset_button( Mantissa(1,2763), "Sapphire", 1e30, "Diamond")),
          ("1e2793 Sapphire: 1e36 Diamond", lambda: reset_button( Mantissa(1,2793), "Sapphire", 1e36, "Diamond")),
          ("1e2903 Sapphire: 1e42 Diamond", lambda: reset_button( Mantissa(1,2903), "Sapphire", 1e42, "Diamond")),
          ("1e3003 Sapphire: 1e48 Diamond", lambda: reset_button( Mantissa(1,3003), "Sapphire", 1e48, "Diamond")),
          ("1e3053 Sapphire: 1e54 Diamond", lambda: reset_button( Mantissa(1,3053), "Sapphire", 1e54, "Diamond")),
          ("1e3103 Sapphire: 1e60 Diamond", lambda: reset_button( Mantissa(1,3103), "Sapphire", 1e60, "Diamond")),
          ("1e3153 Sapphire: 1e66 Diamond", lambda: reset_button( Mantissa(1,3153), "Sapphire", 1e66, "Diamond")),
          ("1e3203 Sapphire: 1e72 Diamond", lambda: reset_button( Mantissa(1,3203), "Sapphire", 1e72, "Diamond")),
          ("1e3253 Sapphire: 1e78 Diamond", lambda: reset_button( Mantissa(1,3253), "Sapphire", 1e78, "Diamond")),
          ("1e3303 Sapphire: 1e84 Diamond", lambda: reset_button( Mantissa(1,3303), "Sapphire", 1e84, "Diamond")),
          ("1e3353 Sapphire: 1e90 Diamond", lambda: reset_button( Mantissa(1,3353), "Sapphire", 1e90, "Diamond")),
          ("1e3403 Sapphire: 1e93 Diamond", lambda: reset_button( Mantissa(1,3403), "Sapphire", 1e93, "Diamond")),
      ],
      "Starlight": [
          ("1e1203 Diamond: 5T Starlight", lambda: reset_button( Mantissa(1,1203), "Diamond", 5e12, "Starlight")),
          ("1e1233 Diamond: 400T Starlight", lambda: reset_button( Mantissa(1,1233), "Diamond", 4e14, "Starlight")),
          ("1e1263 Diamond: 15Qd Starlight", lambda: reset_button( Mantissa(1,1263), "Diamond", 1.5e16, "Starlight")),
          ("1e1293 Diamond: 200Qd Starlight", lambda: reset_button( Mantissa(1,1293), "Diamond", 2e17, "Starlight")),
          ("1e1323 Diamond: 5Qn Starlight", lambda: reset_button( Mantissa(1,1323), "Diamond", 5e18, "Starlight")),
          ("1e1353 Diamond: 750Qn Starlight", lambda: reset_button( Mantissa(1,1353), "Diamond", 7.5e20, "Starlight")),
          ("1e1383 Diamond: 20Sx Starlight", lambda: reset_button( Mantissa(1,1383), "Diamond", 2e22, "Starlight")),
          ("1e1413 Diamond: 1Sp Starlight", lambda: reset_button( Mantissa(1,1413), "Diamond", 1e24, "Starlight")),
          ("1e1443 Diamond: 400Sp Starlight", lambda: reset_button( Mantissa(1,1443), "Diamond", 4e26, "Starlight")),
          ("1e1473 Diamond: 3Oc Starlight", lambda: reset_button( Mantissa(1,1473), "Diamond", 3e27, "Starlight")),
          ("1e1503 Diamond: 800Oc Starlight", lambda: reset_button( Mantissa(1,1503), "Diamond", 8e29, "Starlight")),
          ("1e1533 Diamond: 4No Starlight", lambda: reset_button( Mantissa(1,1533), "Diamond", 4e30, "Starlight")),
          ("1e1563 Diamond: 100No Starlight", lambda: reset_button( Mantissa(1,1563), "Diamond", 1e32, "Starlight")),
          ("1e1593 Diamond: 1De Starlight", lambda: reset_button( Mantissa(1,1593), "Diamond", 1e33, "Starlight")),
      ],
      "Ion": [
          ("1e700 Starlight: 5Qd Ion", lambda: reset_button( Mantissa(1,700), "Starlight", 5e15, "Ion")),
          ("1e710 Starlight: 45Qd Ion", lambda: reset_button( Mantissa(1,710), "Starlight", 4.5e16, "Ion")),
          ("1e720 Starlight: 300Qd Ion", lambda: reset_button( Mantissa(1,720), "Starlight", 3e17, "Ion")),
          ("1e730 Starlight: 1Qn Ion", lambda: reset_button( Mantissa(1,730), "Starlight", 1e18, "Ion")),
          ("1e740 Starlight: 6Qn Ion", lambda: reset_button( Mantissa(1,740), "Starlight", 6e18, "Ion")),
          ("1e750 Starlight: 80Qn Ion", lambda: reset_button( Mantissa(1,750), "Starlight", 8e19, "Ion")),
          ("1e760 Starlight: 400Qn Ion", lambda: reset_button( Mantissa(1,760), "Starlight", 4e20, "Ion")),
          ("1e770 Starlight: 2Sx Ion", lambda: reset_button( Mantissa(1,770), "Starlight", 2e21, "Ion")),
          ("1e780 Starlight: 7Sx Ion", lambda: reset_button( Mantissa(1,780), "Starlight", 7e21, "Ion")),
          ("1e790 Starlight: 30Sx Ion", lambda: reset_button( Mantissa(1,790), "Starlight", 3e22, "Ion")),
          ("1e800 Starlight: 150Sx Ion", lambda: reset_button( Mantissa(1,800), "Starlight", 1.5e23, "Ion")),
          ("1e810 Starlight: 1Sp Ion", lambda: reset_button( Mantissa(1,810), "Starlight", 1e24, "Ion")),
          ("1e820 Starlight: 4Sp Ion", lambda: reset_button( Mantissa(1,820), "Starlight", 4e24, "Ion")),
          ("1e830 Starlight: 50Sp Ion", lambda: reset_button( Mantissa(1,830), "Starlight", 5e25, "Ion")),
      ],
      "Uranium": [
          ("1e363 Ion: 1e66 Uranium", lambda: reset_button( Mantissa(1,363), "Ion", 1e66, "Uranium")),
          ("1e373 Ion: 1e67 Uranium", lambda: reset_button( Mantissa(1,373), "Ion", 1e67, "Uranium")),
          ("1e383 Ion: 1e68 Uranium", lambda: reset_button( Mantissa(1,383), "Ion", 1e68, "Uranium")),
          ("1e393 Ion: 1e69 Uranium", lambda: reset_button( Mantissa(1,393), "Ion", 1e69, "Uranium")),
          ("1e403 Ion: 1e70 Uranium", lambda: reset_button( Mantissa(1,403), "Ion", 1e70, "Uranium")),
          ("1e413 Ion: 1e71 Uranium", lambda: reset_button( Mantissa(1,413), "Ion", 1e71, "Uranium")),
          ("1e423 Ion: 1e72 Uranium", lambda: reset_button( Mantissa(1,423), "Ion", 1e72, "Uranium")),
          ("1e433 Ion: 1e73 Uranium", lambda: reset_button( Mantissa(1,433), "Ion", 1e73, "Uranium")),
          ("1e443 Ion: 1e74 Uranium", lambda: reset_button( Mantissa(1,443), "Ion", 1e74, "Uranium")),
          ("1e453 Ion: 1e75 Uranium", lambda: reset_button( Mantissa(1,453), "Ion", 1e75, "Uranium")),
          ("1e463 Ion: 1e76 Uranium", lambda: reset_button( Mantissa(1,463), "Ion", 1e76, "Uranium")),
          ("1e473 Ion: 1e77 Uranium", lambda: reset_button( Mantissa(1,473), "Ion", 1e77, "Uranium")),
          ("1e483 Ion: 1e78 Uranium", lambda: reset_button( Mantissa(1,483), "Ion", 1e78, "Uranium")),
          ("1e493 Ion: 1e79 Uranium", lambda: reset_button( Mantissa(1,493), "Ion", 1e79, "Uranium")),
      ],
      "Bismuth": [
          ("1e243 Uranium: 1B Bismuth", lambda: reset_button( 1e243, "Uranium", 1e9, "Bismuth")),
          ("1e248 Uranium: 5B Bismuth", lambda: reset_button( 1e248, "Uranium", 5e9, "Bismuth")),
          ("1e253 Uranium: 60B Bismuth", lambda: reset_button( 1e253, "Uranium", 6e10, "Bismuth")),
          ("1e258 Uranium: 200B Bismuth", lambda: reset_button( 1e258, "Uranium", 2e11, "Bismuth")),
          ("1e263 Uranium: 800B Bismuth", lambda: reset_button( 1e263, "Uranium", 8e11, "Bismuth")),
          ("1e268 Uranium: 2T Bismuth", lambda: reset_button( 1e268, "Uranium", 2e12, "Bismuth")),
          ("1e273 Uranium: 8T Bismuth", lambda: reset_button( 1e273, "Uranium", 8e12, "Bismuth")),
          ("1e278 Uranium: 20T Bismuth", lambda: reset_button( 1e278, "Uranium", 2e13, "Bismuth")),
          ("1e283 Uranium: 100T Bismuth", lambda: reset_button( 1e283, "Uranium", 1e14, "Bismuth")),
          ("1e288 Uranium: 500T Bismuth", lambda: reset_button( 1e288, "Uranium", 5e14, "Bismuth")),
          ("1e293 Uranium: 3Qd Bismuth", lambda: reset_button( 1e293, "Uranium", 3e15, "Bismuth")),
          ("1e298 Uranium: 20Qd Bismuth", lambda: reset_button( 1e298, "Uranium", 2e16, "Bismuth")),
          ("1e303 Uranium: 100Qd Bismuth", lambda: reset_button( Mantissa(1,303), "Uranium", 1e17, "Bismuth")),
          ("1e308 Uranium: 500Qd Bismuth", lambda: reset_button( Mantissa(1,308), "Uranium", 5e17, "Bismuth")),
      ],
      "Boracite": [
          ("1e129 Bismuth: 100Qn Boracite", lambda: reset_button( 1e129, "Bismuth", 1e20, "Boracite")),
          ("1e132 Bismuth: 650Qn Boracite", lambda: reset_button( 1e132, "Bismuth", 6.5e20, "Boracite")),
          ("1e135 Bismuth: 2Sx Boracite", lambda: reset_button( 1e135, "Bismuth", 2e21, "Boracite")),
          ("1e138 Bismuth: 8Sx Boracite", lambda: reset_button( 1e138, "Bismuth", 8e21, "Boracite")),
          ("1e141 Bismuth: 35Sx Boracite", lambda: reset_button( 1e141, "Bismuth", 3.5e22, "Boracite")),
          ("1e144 Bismuth: 140Sx Boracite", lambda: reset_button( 1e144, "Bismuth", 1.4e23, "Boracite")),
          ("1e147 Bismuth: 600Sx Boracite", lambda: reset_button( 1e147, "Bismuth", 6e23, "Boracite")),
          ("1e150 Bismuth: 1.5Sp Boracite", lambda: reset_button( 1e150, "Bismuth", 1.5e24, "Boracite")),
          ("1e153 Bismuth: 6Sp Boracite", lambda: reset_button( 1e153, "Bismuth", 6e24, "Boracite")),
          ("1e156 Bismuth: 20Sp Boracite", lambda: reset_button( 1e156, "Bismuth", 2e25, "Boracite")),
          ("1e159 Bismuth: 90Sp Boracite", lambda: reset_button( 1e159, "Bismuth", 9e25, "Boracite")),
          ("1e162 Bismuth: 230Sp Boracite", lambda: reset_button( 1e162, "Bismuth", 2.3e26, "Boracite")),
          ("1e165 Bismuth: 750Sp Boracite", lambda: reset_button( 1e165, "Bismuth", 7.5e26, "Boracite")),
          ("1e168 Bismuth: 2Oc Boracite", lambda: reset_button( 1e168, "Bismuth", 2e27, "Boracite")),
      ],
      "Nissonite": [
          ("1e63 Boracite: 100T Nissonite", lambda: reset_button( 1e63, "Boracite", 1e14, "Nissonite")),
          ("1e65 Boracite: 500T Nissonite", lambda: reset_button( 1e65, "Boracite", 5e14, "Nissonite")),
          ("1e67 Boracite: 2Qd Nissonite", lambda: reset_button( 1e67, "Boracite", 2e15, "Nissonite")),
          ("1e69 Boracite: 10Qd Nissonite", lambda: reset_button( 1e69, "Boracite", 1e16, "Nissonite")),
          ("1e71 Boracite: 40Qd Nissonite", lambda: reset_button( 1e71, "Boracite", 4e16, "Nissonite")),
          ("1e73 Boracite: 130Qd Nissonite", lambda: reset_button( 1e73, "Boracite", 1.3e17, "Nissonite")),
          ("1e75 Boracite: 500Qd Nissonite", lambda: reset_button( 1e75, "Boracite", 5e17, "Nissonite")),
          ("1e77 Boracite: 3Qn Nissonite", lambda: reset_button( 1e77, "Boracite", 3e18, "Nissonite")),
          ("1e79 Boracite: 20Qn Nissonite", lambda: reset_button( 1e79, "Boracite", 2e19, "Nissonite")),
          ("1e81 Boracite: 110Qn Nissonite", lambda: reset_button( 1e81, "Boracite", 1.1e20, "Nissonite")),
          ("1e83 Boracite: 400Qn Nissonite", lambda: reset_button( 1e83, "Boracite", 4e20, "Nissonite")),
          ("1e85 Boracite: 1Sx Nissonite", lambda: reset_button( 1e85, "Boracite", 1e21, "Nissonite")),
          ("1e87 Boracite: 5Sx Nissonite", lambda: reset_button( 1e87, "Boracite", 5e21, "Nissonite")),
          ("1e88 Boracite: 25Sx Nissonite", lambda: reset_button( 1e88, "Boracite", 2.5e22, "Nissonite")),
      ],
      "Orpiment": [
          ("1No Nissonite: 3k Orpiment", lambda: reset_button( 1e30, "Nissonite", 3000, "Orpiment")),
          ("10No Nissonite: 10k Orpiment", lambda: reset_button( 1e31, "Nissonite", 10000, "Orpiment")),
          ("100No Nissonite: 22k Orpiment", lambda: reset_button( 1e32, "Nissonite", 22000, "Orpiment")),
          ("1De Nissonite: 60k Orpiment", lambda: reset_button( 1e33, "Nissonite", 60000, "Orpiment")),
          ("10De Nissonite: 140k Orpiment", lambda: reset_button( 1e34, "Nissonite", 140000, "Orpiment")),
          ("100De Nissonite: 400k Orpiment", lambda: reset_button( 1e35, "Nissonite", 400000, "Orpiment")),
          ("1e36 Nissonite: 1M Orpiment", lambda: reset_button( 1e36, "Nissonite", 1e6, "Orpiment")),
          ("1e37 Nissonite: 2.5M Orpiment", lambda: reset_button( 1e37, "Nissonite", 2.5e6, "Orpiment")),
          ("1e38 Nissonite: 10M Orpiment", lambda: reset_button( 1e38, "Nissonite", 1e7, "Orpiment")),
          ("1e39 Nissonite: 25M Orpiment", lambda: reset_button( 1e39, "Nissonite", 2.5e7, "Orpiment")),
          ("1e40 Nissonite: 50M Orpiment", lambda: reset_button( 1e40, "Nissonite", 5e7, "Orpiment")),
          ("1e41 Nissonite: 120M Orpiment", lambda: reset_button( 1e41, "Nissonite", 1.2e8, "Orpiment")),
          ("1e42 Nissonite: 350M Orpiment", lambda: reset_button( 1e42, "Nissonite", 3.5e8, "Orpiment")),
          ("1e45 Nissonite: 1B Orpiment", lambda: reset_button( 1e45, "Nissonite", 1e9, "Orpiment")),
      ],
      "Tetra": [
          ("100B Orpiment: 40 Tetra", lambda: reset_button( 1e11, "Orpiment", 40, "Tetra")),
          ("450B Orpiment: 85 Tetra", lambda: reset_button( 4.5e11, "Orpiment", 85, "Tetra")),
          ("6T Orpiment: 150 Tetra", lambda: reset_button( 6e12, "Orpiment", 150, "Tetra")),
          ("100T Orpiment: 320 Tetra", lambda: reset_button( 1e14, "Orpiment", 320, "Tetra")),
          ("2Qd Orpiment: 750 Tetra", lambda: reset_button( 2e15, "Orpiment", 750, "Tetra")),
          ("15Qd Orpiment: 1.2k Tetra", lambda: reset_button( 1.5e16, "Orpiment", 1200, "Tetra")),
          ("1Qn Orpiment: 2.65k Tetra", lambda: reset_button( 1e18, "Orpiment", 2650, "Tetra")),
      ],
      "Volt": [
          ("1.4k Tetra: 1 Volt", lambda: reset_button( 1400, "Tetra", 1, "Volt")),
          ("65k Tetra: 3 Volt", lambda: reset_button( 65000, "Tetra", 3, "Volt")),
          ("600k Tetra: 7 Volt", lambda: reset_button( 600000, "Tetra", 7, "Volt")),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check("S")),
         ("Recover Hall (req: 0 Cash)", lambda: load_check("RH"))
      ],
      #"Unknown": [("", lambda: blinded())]
  }, 50, "Tetra", "VS", voltaic_radar=voltaic_radar)
  Realm(root, { #Abyssal Trenches
      "Orpiment": [
          ("1e54 Nissonite: 2.2B Orpiment", lambda: reset_button( 1e54, "Nissonite", 2.2e9, "Orpiment")),
          ("1e56 Nissonite: 6B Orpiment", lambda: reset_button( 1e56, "Nissonite", 6e9, "Orpiment")),
          ("1e58 Nissonite: 13B Orpiment", lambda: reset_button( 1e58, "Nissonite", 1.3e10, "Orpiment")),
          ("1e63 Nissonite: 30B Orpiment", lambda: reset_button( 1e63, "Nissonite", 3e10, "Orpiment")),
          ("1e66 Nissonite: 100B Orpiment", lambda: reset_button( 1e66, "Nissonite", 1e11, "Orpiment")),
          ("1e67 Nissonite: 250B Orpiment", lambda: reset_button( 1e67, "Nissonite", 2.5e11, "Orpiment")),
      ],
      "Tetra": [
          ("25Qn Orpiment: 7.5k Tetra", lambda: reset_button( 2.5e19, "Orpiment", 7500, "Tetra")),
          ("700Qn Orpiment: 16.5k Tetra", lambda: reset_button( 7e20, "Orpiment", 16500, "Tetra")),
          ("1Sx Orpiment: 34k Tetra", lambda: reset_button( 1e21, "Orpiment", 34000, "Tetra")),
          ("1Sp Orpiment: 70k Tetra", lambda: reset_button( 1e24, "Orpiment", 70000, "Tetra")),
          ("10Sp Orpiment: 150k Tetra", lambda: reset_button( 1e25, "Orpiment", 150000, "Tetra")),
      ],
      "Volt": [
          ("1M Tetra: 25 Volt", lambda: reset_button( 1e6, "Tetra", 25, "Volt")),
          ("10M Tetra: 50 Volt", lambda: reset_button( 1e7, "Tetra", 50, "Volt")),
          ("70M Tetra: 150 Volt", lambda: reset_button( 7e7, "Tetra", 150, "Volt")),
          ("400M Tetra: 400 Volt", lambda: reset_button( 4e8, "Tetra", 400, "Volt")),
          ("3B Tetra: 1k Volt", lambda: reset_button( 3e9, "Tetra", 1000, "Volt")),
          ("20B Tetra: 2.45k Volt", lambda: reset_button( 2e10, "Tetra", 2450, "Volt")),
          ("150B Tetra: 5k Volt", lambda: reset_button( 1.5e11, "Tetra", 5000, "Volt")),
      ],
      "Aquamarine": [
          ("700 Volt: 1 Aquamarine", lambda: reset_button( 700, "Volt", 1, "Aquamarine")),
          ("2.5k Volt: 4 Aquamarine", lambda: reset_button( 2500, "Volt", 4, "Aquamarine")),
          ("30k Volt: 13 Aquamarine", lambda: reset_button( 30000, "Volt", 13, "Aquamarine")),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check("S")),
         ("Recover Hall (req: 0 Cash)", lambda: load_check("RH")),
         ("R34L1TY (req: 1 C0RR8PT10N)", lambda: load_check("R34L1TY")),
      ]
  }, 3, "Volt", "AT", voltaic_radar=voltaic_radar)
  Realm(root, { #Flourish Candylands
      "Orpiment": [
          ("1e76 Nissonite: 550B Orpiment", lambda: reset_button( 1e76, "Nissonite", 5.5e11, "Orpiment")),
          ("1e78 Nissonite: 1.3T Orpiment", lambda: reset_button( 1e78, "Nissonite", 1.3e12, "Orpiment")),
          ("1e82 Nissonite: 6T Orpiment", lambda: reset_button( 1e82, "Nissonite", 6e12, "Orpiment")),
      ],
      "Tetra": [
          ("1Oc Orpiment: 350k Tetra", lambda: reset_button( 1e27, "Orpiment", 350000, "Tetra")),
          ("40Oc Orpiment: 1M Tetra", lambda: reset_button( 4e28, "Orpiment", 1e6, "Tetra")),
          ("1No Orpiment: 2.3M Tetra", lambda: reset_button( 1e30, "Orpiment", 2.3e6, "Tetra")),
      ],
      "Volt": [
          ("250B Tetra: 10k Volt", lambda: reset_button( 2.5e11, "Tetra", 10000, "Volt")),
          ("800B Tetra: 22k Volt", lambda: reset_button( 8e11, "Tetra", 22000, "Volt")),
          ("4T Tetra: 50k Volt", lambda: reset_button( 4e12, "Tetra", 50000, "Volt")),
          ("20T Tetra: 105k Volt", lambda: reset_button( 2e13, "Tetra", 105000, "Volt")),
          ("300T Tetra: 250k Volt", lambda: reset_button( 3e14, "Tetra", 250000, "Volt")),
          ("1.3Qd Tetra: 400k Volt", lambda: reset_button( 1.3e15, "Tetra", 400000, "Volt")),
      ],
      "Aquamarine": [
          ("400k Volt: 24 Aquamarine", lambda: reset_button( 400000, "Volt", 24, "Aquamarine")),
          ("2M Volt: 80 Aquamarine", lambda: reset_button( 2e6, "Volt", 80, "Aquamarine")),
          ("11M Volt: 210 Aquamarine", lambda: reset_button( 1.1e7, "Volt", 210, "Aquamarine")),
          ("50M Volt: 1k Aquamarine", lambda: reset_button( 5e7, "Volt", 1000, "Aquamarine")),
      ],
      "Lollipop": [
          ("100 Aquamarine: 1 Lollipop", lambda: reset_button( 100, "Aquamarine", 1, "Lollipop")),
          ("800 Aquamarine: 3 Lollipop", lambda: reset_button( 800, "Aquamarine", 3, "Lollipop")),
          ("10k Aquamarine: 12 Lollipop", lambda: reset_button( 10000, "Aquamarine", 12, "Lollipop")),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check("S")),
         ("Recover Hall (req: 0 Cash)", lambda: load_check("RH"))
      ]
  }, 25, "Aquamarine", "FC", voltaic_radar=voltaic_radar)
  Realm(root, { #Anticovery Hall
      "Lollipop": [
          ("1M Aquamarine: 75 Lollipop", lambda: reset_button( 1e6, "Aquamarine", 75, "Lollipop")),
          ("100M Aquamarine: 300 Lollipop", lambda: reset_button( 1e8, "Aquamarine", 300, "Lollipop")),
          ("10B Aquamarine: 1.5k Lollipop", lambda: reset_button( 1e10, "Aquamarine", 1500, "Lollipop")),
          ("1T Aquamarine: 5k Lollipop", lambda: reset_button( 1e12, "Aquamarine", 5000, "Lollipop")),
          ("10Qd Aquamarine: 10k Lollipop", lambda: reset_button( 1e16, "Aquamarine", 10000, "Lollipop")),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check("S")),
         ("Recover Hall (req: 0 Cash)", lambda: load_check("RH"))
      ]
  }, [1,1], ["Stargazed Metal", "Gyge"], "AH", voltaic_radar=voltaic_radar)
  Realm(root, { #Minty Groves
      "Mint": [
          ("15 Rebirths: 1 Mint", lambda: reset_button_special( 15, "Rebirths", 1, "Mint", ["Cash", "Multiplier", "Rebirths"])),
          ("500 Rebirths: 3 Mint", lambda: reset_button_special( 500, "Rebirths", 3, "Mint", ["Cash", "Multiplier", "Rebirths"])),
          ("6k Rebirths: 7 Mint", lambda: reset_button_special( 6000, "Rebirths", 7, "Mint", ["Cash", "Multiplier", "Rebirths"])),
          ("20k Rebirths: 13 Mint", lambda: reset_button_special( 20000, "Rebirths", 13, "Mint", ["Cash", "Multiplier", "Rebirths"])),
          ("100k Rebirths: 20 Mint", lambda: reset_button_special( 100000, "Rebirths", 20, "Mint", ["Cash", "Multiplier", "Rebirths"])),
          ("5M Rebirths: 50 Mint", lambda: reset_button_special( 5e6, "Rebirths", 50, "Mint", ["Cash", "Multiplier", "Rebirths"])),
          ("75M Rebirths: 100 Mint", lambda: reset_button_special( 7.5e7, "Rebirths", 100, "Mint", ["Cash", "Multiplier", "Rebirths"])),
          ("1B Rebirths: 300 Mint", lambda: reset_button_special( 1e9, "Rebirths", 300, "Mint", ["Cash", "Multiplier", "Rebirths"])),
          ("1No Rebirths: 1k Mint", lambda: reset_button_special( 1e30, "Rebirths", 1000, "Mint", ["Cash", "Multiplier", "Rebirths"])),
          ("1e300 Rebirths: 10k Mint", lambda: reset_button_special( 1e300, "Rebirths", 10000, "Mint", ["Cash", "Multiplier", "Rebirths"])),
          ("1e3000 Rebirths: 100k Mint", lambda: reset_button_special( Mantissa(1,3000), "Rebirths", 100000, "Mint", ["Cash", "Multiplier", "Rebirths"])),
      ],
      "Geodes": [
          ("Mint Geode: 2k Mint", lambda btn: Geode_roll(btn, mint_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check("S")),
         ("Recover Hall (req: 0 Cash)", lambda: load_check("RH"))
      ]
  }, 5, "Rebirths", "MG", voltaic_radar=voltaic_radar)
  Realm(root, { #Stardustry
      "Metal": [
          ("15 Gold: 1 Metal", lambda: reset_button_special(15, "Gold", 1, "Metal", ["Gold"])),
          ("72 Gold: 2 Metal", lambda: reset_button_special(72, "Gold", 2, "Metal", ["Gold"])),
          ("361 Gold: 3 Metal", lambda: reset_button_special(361, "Gold", 3, "Metal", ["Gold"])),
          ("1.62k Gold: 4 Metal", lambda: reset_button_special(1620, "Gold", 4, "Metal", ["Gold"])),
          ("1M Gold: 6 Metal", lambda: reset_button_special(1e6, "Gold", 6, "Metal", ["Gold"])),
          ("1T Gold: 10 Metal", lambda: reset_button_special(1e12, "Gold", 10, "Metal", ["Gold"])),
          ("10Oc Gold: 15 Metal", lambda: reset_button_special(1e28, "Gold", 15, "Metal", ["Gold"])),
          ("1e252 Gold: 25 Metal", lambda: reset_button_special(1e252, "Gold", 25, "Metal", ["Gold"])),
          ("1e1500 Gold: 50 Metal", lambda: reset_button_special(Mantissa(1,1500), "Gold", 50, "Metal", ["Gold"])),
          ("1e10000 Gold: 100 Metal", lambda: reset_button_special(Mantissa(1,10000), "Gold", 100, "Metal", ["Gold"])),
      ],
      "Press": [
          ("25 Metal: 1 Press", lambda: reset_button_special(25, "Metal", 1, "Press", ["Gold", "Metal"])),
          ("2.5k Metal: 2 Press", lambda: reset_button_special(2500, "Metal", 2, "Press", ["Gold", "Metal"])),
          ("50k Metal: 3 Press", lambda: reset_button_special(50000, "Metal", 3, "Press", ["Gold", "Metal"])),
          ("1M Metal: 5 Press", lambda: reset_button_special(1e6, "Metal", 5, "Press", ["Gold", "Metal"])),
          ("20M Metal: 10 Press", lambda: reset_button_special(2e7, "Metal", 10, "Press", ["Gold", "Metal"])),
          ("1B Metal: 25 Press", lambda: reset_button_special(1e9, "Metal", 25, "Press", ["Gold", "Metal"])),
          ("1T Metal: 45 Press", lambda: reset_button_special(1e12, "Metal", 45, "Press", ["Gold", "Metal"])),
          ("1Qd Metal: 100 Press", lambda: reset_button_special(1e15, "Metal", 100, "Press", ["Gold", "Metal"])),
          ("1Qn Metal: 175 Press", lambda: reset_button_special(1e18, "Metal", 175, "Press", ["Gold", "Metal"])),
          ("1Sx Metal: 250 Press", lambda: reset_button_special(1e21, "Metal", 250, "Press", ["Gold", "Metal"])),
      ],
      "Microparticles": [
          ("100 Press: 1 Microparticles", lambda: reset_button_special(100, "Press", 1, "Microparticles", ["Gold", "Metal", "Press"])),
          ("1.5k Press: 3 Microparticles", lambda: reset_button_special(1500, "Press", 3, "Microparticles", ["Gold", "Metal", "Press"])),
          ("35k Press: 5 Microparticles", lambda: reset_button_special(35000, "Press", 5, "Microparticles", ["Gold", "Metal", "Press"])),
          ("1M Press: 8 Microparticles", lambda: reset_button_special(1e6, "Press", 8, "Microparticles", ["Gold", "Metal", "Press"])),
          ("25M Press: 15 Microparticles", lambda: reset_button_special(2.5e7, "Press", 15, "Microparticles", ["Gold", "Metal", "Press"])),
          ("1B Press: 31 Microparticles", lambda: reset_button_special(1e9, "Press", 31, "Microparticles", ["Gold", "Metal", "Press"])),
          ("1T Press: 100 Microparticles", lambda: reset_button_special(1e12, "Press", 100, "Microparticles", ["Gold", "Metal", "Press"])),
      ],
      "Star": [
          ("2.5k Microparticles: 1 Star", lambda: reset_button_special(2500, "Microparticles", 1, "Star", ["Gold", "Metal", "Press", "Microparticles"])),
          ("100k Microparticles: 2 Star", lambda: reset_button_special(100000, "Microparticles", 2, "Star", ["Gold", "Metal", "Press", "Microparticles"])),
          ("25M Microparticles: 5 Star", lambda: reset_button_special(2.5e7, "Microparticles", 5, "Star", ["Gold", "Metal", "Press", "Microparticles"])),
          ("150M Microparticles: 8 Star", lambda: reset_button_special(1.5e8, "Microparticles", 8, "Star", ["Gold", "Metal", "Press", "Microparticles"])),
          ("1B Microparticles: 12 Star", lambda: reset_button_special(1e9, "Microparticles", 12, "Star", ["Gold", "Metal", "Press", "Microparticles"])),
      ],
      "Robot": [
          ("1k Star: 1 Robot", lambda: reset_button_special(1000, "Star", 1, "Robot", ["Gold", "Metal", "Press", "Microparticles", "Star"])),
          ("200k Star: 2 Robot", lambda: reset_button_special(200000, "Star", 2, "Robot", ["Gold", "Metal", "Press", "Microparticles", "Star"])),
          ("2M Star: 4 Robot", lambda: reset_button_special(2e6, "Star", 4, "Robot", ["Gold", "Metal", "Press", "Microparticles", "Star"])),
          ("25M Star: 10 Robot", lambda: reset_button_special(2.5e7, "Star", 10, "Robot", ["Gold", "Metal", "Press", "Microparticles", "Star"])),
      ],
      "Prototype": [
          ("1.5k Robot: 1 Prototype", lambda: reset_button_special(1500, "Robot", 1, "Prototype", ["Gold", "Metal", "Press", "Microparticles", "Star", "Robot"])),
      ],
      "Geodes": [
          ("Deepness Geode: 25 Metal", lambda btn: Geode_roll(btn, deepness_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Oceanic Geode: 5k Metal", lambda btn: Geode_roll(btn, oceanic_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Dream Geode: 200 Press", lambda btn: Geode_roll(btn, dream_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Star Geode: 7 Microparticles", lambda btn: Geode_roll(btn, star_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Holographic Geode: 750 Microparticles", lambda btn: Geode_roll(btn, holographic_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Vector Geode: 100 Star", lambda btn: Geode_roll(btn, vector_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Insurgence Geode: 3 Robot", lambda btn: Geode_roll(btn, insurgence_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Nostalgic Geode: 50 Robot", lambda btn: Geode_roll(btn, nostalgic_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
      ],
      "Recovery": [
          ("2 Microparticles: 1 Gold (Fetch)", lambda: recovery_button_fetch(2, "Microparticles", 1, "Gold")),
          ("1 Star: 5 Gold (Fetch)", lambda: recovery_button_fetch(1, "Star", 5, "Gold")),
          ("1 Robot: 12 Gold (Fetch)", lambda: recovery_button_fetch(1, "Robot", 12, "Gold")),
          ("3 Prototype: 25 Ruby (Fetch)", lambda: recovery_button_fetch(3, "Prototype", 25, "Ruby")),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check("S")),
         ("Recover Hall (req: 0 Cash)", lambda: load_check("RH"))
      ]
  }, 1, "Gold", "SD", voltaic_radar=voltaic_radar)
  Realm(root, { #Geode Site
      "Event Stats": [
          ("7.5k Event Power: 3 Clover", lambda: cost_button( "Event Power", 7500, "Clover", 3)),
          ("15k Event Power: 25 Heart", lambda: cost_button( "Event Power", 15000, "Heart", 25)),
          ("400 Event Power: 10 Orange Pumpkin", lambda: cost_button( "Event Power", 400, "Orange Pumpkin", 10)),
          ("2k Event Power: 8 Ray", lambda: cost_button("Event Power", 2000, "Ray", 8)),
          ("1.2k Ray: 10 Patriotic Crystal", lambda: reset_button_special(1200, "Ray", 10, "Patriotic Crystal", ["Ray"])),
          ("500 Patriotic Crystal: 3 Aureal Gem", lambda: reset_button_special(500, "Patriotic Crystal", 3, "Aureal Gem", ["Ray", "Patriotic Crystal"])),
          ("180 Aureal Gem: 1 Fragment", lambda: reset_button_special(180, "Aureal Gem", 1, "Fragment", ["Ray", "Patriotic Crystal", "Aureal Gem"]))
      ],
      "Geodes": [
          ("Hearted Geode: 50 Heart", lambda btn: Geode_roll(btn, hearted_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Luck Geode: 3 Clover", lambda btn: Geode_roll(btn, luck_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Clover Geode: 100M Clover", lambda btn: Geode_roll(btn, clover_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Celebrative Geode: 10 Rebirths", lambda btn: Geode_roll(btn, celebrative_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Spring Geode: 25 Stone", lambda btn: Geode_roll(btn, spring_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Easter Geode: 7 Event Power", lambda btn: Geode_roll(btn, easter_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Fabled Geode: 1k Diamond", lambda btn: Geode_roll(btn, fabled_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Firey Duced Geode: 75 Ruby", lambda btn: Geode_roll(btn, firey_duced_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Symbiotic Geode: 25 Tetra", lambda btn: Geode_roll(btn, symbiotic_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Summer Geode: 75 Ray", lambda btn: Geode_roll(btn, summer_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Patriotic Geode: 125 Patriotic Crystal", lambda btn: Geode_roll(btn, patriotic_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Aureal Geode: 55 Aureal Gem", lambda btn: Geode_roll(btn, aureal_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Eden Geode: 15 Fragment", lambda btn: Geode_roll(btn, eden_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Lost Geode: 750 Jade", lambda btn: Geode_roll(btn, lost_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Sinister Geode: 10 Orange Pumpkin", lambda btn: Geode_roll(btn, sinister_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Aztec Geode: 500De Clover", lambda btn: Geode_roll(btn, aztec_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Revival Geode: 10k Gyge", lambda btn: Geode_roll(btn, revival_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Unlucky Geode: 5 Stone", lambda btn: Geode_roll(btn, unlucky_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll))
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check("S")),
         ("Recover Hall (req: 0 Cash)", lambda: load_check("RH"))
      ]
  }, 1, "Lollipop", "GS", voltaic_radar=voltaic_radar)
  Realm(root, { #Elysian Highway
      "Master Multiplier": [
          ("100 Master Cash: 1 Master Multiplier", lambda: cost_button("Master Cash", 100, "Master Multiplier", 1)),
          ("200k Master Cash: 3 Master Multiplier", lambda: cost_button("Master Cash", 2e5, "Master Multiplier", 3)),
          ("10M Master Cash: 7 Master Multiplier", lambda: cost_button("Master Cash", 1e7, "Master Multiplier", 7)),
          ("500M Master Cash: 15 Master Multiplier", lambda: cost_button("Master Cash", 5e8, "Master Multiplier", 15)),
          ("1.75B Master Cash: 25 Master Multiplier", lambda: cost_button("Master Cash", 1.75e9, "Master Multiplier", 25)),
          ("50B Master Cash: 100 Master Multiplier", lambda: cost_button("Master Cash", 5e10, "Master Multiplier", 100)),
          ("250B Master Cash: 250 Master Multiplier", lambda: cost_button("Master Cash", 2.5e11, "Master Multiplier", 250)),
          ("10T Master Cash: 1k Master Multiplier", lambda: cost_button("Master Cash", 1e13, "Master Multiplier", 1000)),
          ("750T Master Cash: 3k Master Multiplier", lambda: cost_button("Master Cash", 7.5e14, "Master Multiplier", 3000)),
          ("1.5Qd Master Cash: 7.5k Master Multiplier", lambda: cost_button("Master Cash", 1.5e15, "Master Multiplier", 7500)),
          ("1.25Qn Master Cash: 12k Master Multiplier", lambda: cost_button("Master Cash", 1.25e18, "Master Multiplier", 12000)),
          ("1Sx Master Cash: 100k Master Multiplier", lambda: cost_button("Master Cash", 1e21, "Master Multiplier", 1e5)),
          ("275Sx Master Cash: 1.25M Master Multiplier", lambda: cost_button("Master Cash", 2.75e23, "Master Multiplier", 1.25e6)),
          ("178Sp Master Cash: 12.5M Master Multiplier", lambda: cost_button("Master Cash", 1.78e26, "Master Multiplier", 1.25e7)),
          ("5No Master Cash: 723M Master Multiplier", lambda: cost_button("Master Cash", 5e30, "Master Multiplier", 7.23e8)),
      ],
      "Master Rebirths": [
          ("500 Master Multiplier: 1 Master Rebirths", lambda: reset_button(500, "Master Multiplier", 1, "Master Rebirths")),
          ("9.8k Master Multiplier: 4.53 Master Rebirths", lambda: reset_button(9800, "Master Multiplier", 4.53, "Master Rebirths")),
          ("161.69k Master Multiplier: 19.7 Master Rebirths", lambda: reset_button(161690, "Master Multiplier", 19.7, "Master Rebirths")),
          ("1.42M Master Multiplier: 82.4 Master Rebirths", lambda: reset_button(1.42e6, "Master Multiplier", 82.4, "Master Rebirths")),
          ("10.14M Master Multiplier: 332.2 Master Rebirths", lambda: reset_button(1.014e7, "Master Multiplier", 332.2, "Master Rebirths")),
          ("78.14M Master Multiplier: 700 Master Rebirths", lambda: reset_button(7.814e7, "Master Multiplier", 700, "Master Rebirths")),
          ("251.28M Master Multiplier: 1.5k Master Rebirths", lambda: reset_button(2.5128e8, "Master Multiplier", 1500, "Master Rebirths")),
          ("1B Master Multiplier: 3k Master Rebirths", lambda: reset_button(1e9, "Master Multiplier", 3000, "Master Rebirths")),
          ("88.23B Master Multiplier: 5k Master Rebirths", lambda: reset_button(8.823e10, "Master Multiplier", 5000, "Master Rebirths")),
          ("1Qd Master Multiplier: 30k Master Rebirths", lambda: reset_button(1e15, "Master Multiplier", 30000, "Master Rebirths")),
          ("100Qd Master Multiplier: 75k Master Rebirths", lambda: reset_button(1e17, "Master Multiplier", 75000, "Master Rebirths")),
          ("1Sx Master Multiplier: 300k Master Rebirths", lambda: reset_button(1e21, "Master Multiplier", 300000, "Master Rebirths")),
          ("1No Master Multiplier: 1.5M Master Rebirths", lambda: reset_button(1e30, "Master Multiplier", 1.5e6, "Master Rebirths")),
      ],
      "Master Stone": [
          ("500 Master Rebirths: 1 Master Stone", lambda: reset_button(500, "Master Rebirths", 1, "Master Stone")),
          ("4.45k Master Rebirths: 2.1 Master Stone", lambda: reset_button(4450, "Master Rebirths", 2.1, "Master Stone")),
          ("36.24k Master Rebirths: 4.31 Master Stone", lambda: reset_button(36240, "Master Rebirths", 4.31, "Master Stone")),
          ("396.66k Master Rebirths: 8.62 Master Stone", lambda: reset_button(396660, "Master Rebirths", 8.62, "Master Stone")),
          ("912.87k Master Rebirths: 16.85 Master Stone", lambda: reset_button(912870, "Master Rebirths", 16.85, "Master Stone")),
          ("15.89M Master Rebirths: 32.26 Master Stone", lambda: reset_button(1.589e7, "Master Rebirths", 32.26, "Master Stone")),
          ("370.25M Master Rebirths: 60.55 Master Stone", lambda: reset_button(3.7025e8, "Master Rebirths", 60.55, "Master Stone")),
          ("7.02B Master Rebirths: 111.54 Master Stone", lambda: reset_button(7.02e9, "Master Rebirths", 111.54, "Master Stone")),
      ],
      "Master White Gems": [
          ("200 Master Stone: 1 Master White Gems", lambda: reset_button(200, "Master Stone", 1, "Master White Gems")),
          ("2.13k Master Stone: 2.33 Master White Gems", lambda: reset_button(2130, "Master Stone", 2.33, "Master White Gems")),
          ("27k Master Stone: 5.34 Master White Gems", lambda: reset_button(27000, "Master Stone", 5.34, "Master White Gems")),
          ("350k Master Stone: 12.02 Master White Gems", lambda: reset_button(350000, "Master Stone", 12.02, "Master White Gems")),
      ],
      "Master Crystal": [
          ("12 Master White Gems: 1 Master Crystal", lambda: reset_button(12, "Master White Gems", 1, "Master Crystal")),
      ],
      "Recovery Buttons": [
          ("1 Master Stone: 4.5 Master Multiplier (Fetch)", lambda: recovery_button_fetch(1, "Master Stone", 4.5, "Master Multiplier")),
          ("12 Master Stone: 150 Master Rebirths (Sets)", lambda: recovery_button_set(12, "Master Stone", 150, "Master Rebirths")),
          ("1 Master White Gems: 1 Master Rebirths (Fetch)", lambda: recovery_button_fetch(1, "Master White Gems", 1, "Master Rebirths"))
      ],
      "Area Teleports": [
          ("Buttonia (req: 0 Master Cash)", lambda: load_world(0, "Master Cash", Buttonia)),
          ("Cosmic Road (req: 6 Master Crystal)", lambda: load_check("CR")),
          ("Room of Fate (req: 32 Master Quartz)", lambda: load_check("RF")),
          ("Dark Council (req: 250 Master Ruby)", lambda: load_check("DC")),
          ("Astral Archipelago (req: 50 Master Diamond)", lambda: load_check("AA")),
          ("Limbo (req: 8 Master Uranium)", lambda: load_check("L")),
      ]
  }, 0, "Master Cash", "EH", voltaic_radar=voltaic_radar)
  Realm(root, { #Cosmic Road
      "Master Multiplier": [
          ("1e50 Master Cash: 4B Master Multiplier", lambda: cost_button("Master Cash", 1e50, "Master Multiplier", 4e9)),
          ("4.51e51 Master Cash: 6.03B Master Multiplier", lambda: cost_button("Master Cash", 4.51e51, "Master Multiplier", 6.03e9)),
          ("1.0977e53 Master Cash: 9B Master Multiplier", lambda: cost_button("Master Cash", 1.0977e53, "Master Multiplier", 9e9)),
          ("3.32e54 Master Cash: 13.3B Master Multiplier", lambda: cost_button("Master Cash", 3.32e54, "Master Multiplier", 1.33e10)),
          ("5.694e55 Master Cash: 19.49B Master Multiplier", lambda: cost_button("Master Cash", 5.794e55, "Master Multiplier", 1.949e10)),
          ("1.26e57 Master Cash: 28.3B Master Multiplier", lambda: cost_button("Master Cash", 1.26e57, "Master Multiplier", 2.83e10)),
          ("2.57e58 Master Cash: 40.75B Master Multiplier", lambda: cost_button("Master Cash", 2.57e58, "Master Multiplier", 4.075e10)),
          ("3.3116e59 Master Cash: 58.21B Master Multiplier", lambda: cost_button("Master Cash", 3.3116e59, "Master Multiplier", 5.821e10)),
          ("9.59e60 Master Cash: 82.53B Master Multiplier", lambda: cost_button("Master Cash", 9.59e60, "Master Multiplier", 8.253e10)),
          ("1.3506e62 Master Cash: 116.16B Master Multiplier", lambda: cost_button("Master Cash", 1.3506e62, "Master Multiplier", 1.11616e11)),
          ("5.1e63 Master Cash: 162.34B Master Multiplier", lambda: cost_button("Master Cash", 5.1e63, "Master Multiplier", 1.6234e11)),
          ("1.7285e65 Master Cash: 225.37B Master Multiplier", lambda: cost_button("Master Cash", 1.7285e65, "Master Multiplier", 2.2537e11)),
          ("5.12e66 Master Cash: 310.87B Master Multiplier", lambda: cost_button("Master Cash", 5.12e66, "Master Multiplier", 3.1087e11)),
          ("2.0068e68 Master Cash: 426.13B Master Multiplier", lambda: cost_button("Master Cash", 2.0068e68, "Master Multiplier", 4.2613e11)),
          ("2.04e69 Master Cash: 580.66B Master Multiplier", lambda: cost_button("Master Cash", 2.04e69, "Master Multiplier", 5.8066e11)),
          ("6.993e70 Master Cash: 786.71B Master Multiplier", lambda: cost_button("Master Cash", 6.993e70, "Master Multiplier", 7.8671e11)),
          ("2.25e72 Master Cash: 1.05T Master Multiplier", lambda: cost_button("Master Cash", 2.25e72, "Master Multiplier", 1.05e12)),
          ("3.049e73 Master Cash: 1.42T Master Multiplier", lambda: cost_button("Master Cash", 3.049e73, "Master Multiplier", 1.42e12)),
      ],
      "Master Rebirths": [
          ("1De Master Multiplier: 1.5M Master Rebirths", lambda: reset_button(1e33, "Master Multiplier", 1.5e6, "Master Rebirths")),
          ("22.32De Master Multiplier: 2.3M Master Rebirths", lambda: reset_button(2.232e34, "Master Multiplier", 2.3e6, "Master Rebirths")),
          ("732.2De Master Multiplier: 3.5M Master Rebirths", lambda: reset_button(7.322e35, "Master Multiplier", 3.5e6, "Master Rebirths")),
          ("2.092e37 Master Multiplier: 5.3M Master Rebirths", lambda: reset_button(2.092e37, "Master Multiplier", 5.3e6, "Master Rebirths")),
          ("5.1926e38 Master Multiplier: 7.98M Master Rebirths", lambda: reset_button(5.1926e38, "Master Multiplier", 7.98e6, "Master Rebirths")),
          ("1.525e40 Master Multiplier: 11.94M Master Rebirths", lambda: reset_button(1.525e40, "Master Multiplier", 1.194e7, "Master Rebirths")),
          ("3.9303e41 Master Multiplier: 17.75M Master Rebirths", lambda: reset_button(3.9303e41, "Master Multiplier", 1.775e7, "Master Rebirths")),
          ("6.7e42 Master Multiplier: 25.25M Master Rebirths", lambda: reset_button(6.7e42, "Master Multiplier", 2.525e7, "Master Rebirths")),
          ("1.456e44 Master Multiplier: 38.6M Master Rebirths", lambda: reset_button(1.456e44, "Master Multiplier", 3.86e7, "Master Rebirths")),
          ("2.73e45 Master Multiplier: 56.45M Master Rebirths", lambda: reset_button(2.73e45, "Master Multiplier", 5.645e7, "Master Rebirths")),
          ("5.742e46 Master Multiplier: 82.14M Master Rebirths", lambda: reset_button(5.742e46, "Master Multiplier", 8.214e7, "Master Rebirths")),
          ("8.5024e47 Master Multiplier: 118.9M Master Rebirths", lambda: reset_button(8.5024e47, "Master Multiplier", 1.189e8, "Master Rebirths")),
      ],
      "Master Stone": [
          ("18B Master Rebirths: 600 Master Stone", lambda: reset_button(1.8e10, "Master Rebirths", 600, "Master Stone")),
          ("595.1B Master Rebirths: 1.45k Master Stone", lambda: reset_button(5.951e11, "Master Rebirths", 1450, "Master Stone")),
          ("11.09T Master Rebirths: 3.51k Master Stone", lambda: reset_button(1.109e13, "Master Rebirths", 3510, "Master Stone")),
          ("362.58T Master Rebirths: 8.41k Master Stone", lambda: reset_button(3.6258e14, "Master Rebirths", 8410, "Master Stone")),
          ("3.25Qd Master Rebirths: 19.97k Master Stone", lambda: reset_button(3.25e15, "Master Rebirths", 19970, "Master Stone")),
          ("89.57Qd Master Rebirths: 47.05k Master Stone", lambda: reset_button(8.975e16, "Master Rebirths", 47050, "Master Stone")),
          ("970Qd Master Rebirths: 110.01k Master Stone", lambda: reset_button(9.7e17, "Master Rebirths", 110010, "Master Stone")),
          ("26.92Qn Master Rebirths: 255.31k Master Stone", lambda: reset_button(2.692e19, "Master Rebirths", 255310, "Master Stone")),
          ("597.97Qn Master Rebirths: 588.21k Master Stone", lambda: reset_button(5.9797e20, "Master Rebirths", 588210, "Master Stone")),
      ],
      "Master White Gems": [
          ("1.25M Master Stone: 72 Master White Gems", lambda: reset_button(1.25e6, "Master Stone", 72, "Master White Gems")),
          ("26.91M Master Stone: 159.21 Master White Gems", lambda: reset_button(2.691e7, "Master Stone", 159.21, "Master White Gems")),
          ("147.63M Master Stone: 349.63 Master White Gems", lambda: reset_button(1.4763e8, "Master Stone", 349.63, "Master White Gems")),
          ("2.56B Master Stone: 762.55 Master White Gems", lambda: reset_button(2.56e9, "Master Stone", 762.55, "Master White Gems")),
          ("44.16B Master Stone: 1.65k Master White Gems", lambda: reset_button(4.416e10, "Master Stone", 1650, "Master White Gems")),
          ("636.74B Master Stone: 3.55k Master White Gems", lambda: reset_button(6.3674e11, "Master Stone", 3550, "Master White Gems")),
          ("7.12T Master Stone: 7.6k Master White Gems", lambda: reset_button(7.12e12, "Master Stone", 7600, "Master White Gems")),
      ],
      "Master Crystal": [
          ("40 Master White Gems: 4 Master Crystal", lambda: reset_button(40, "Master White Gems", 4, "Master Crystal")),
          ("302.07 Master White Gems: 8.51 Master Crystal", lambda: reset_button(302.07, "Master White Gems", 8.51, "Master Crystal")),
          ("4.78k Master White Gems: 18 Master Crystal", lambda: reset_button(4780, "Master White Gems", 18, "Master Crystal")),
          ("27.96k Master White Gems: 37.85 Master Crystal", lambda: reset_button(27960, "Master White Gems", 37.85, "Master Crystal")),
          ("520.87k Master White Gems: 79.1 Master Crystal", lambda: reset_button(520870, "Master White Gems", 79.1, "Master Crystal")),
          ("3M Master White Gems: 164.3 Master Crystal", lambda: reset_button(3e6, "Master White Gems", 164.3, "Master Crystal")),
      ],
      "Master Iron": [
          ("24 Master Crystal: 1 Master Iron", lambda: reset_button(24, "Master Crystal", 1, "Master Iron")),
          ("238.68 Master Crystal: 2.5 Master Iron", lambda: reset_button(238.68, "Master Crystal", 2.5, "Master Iron")),
          ("1.83k Master Crystal: 6.22 Master Iron", lambda: reset_button(1830, "Master Crystal", 6.22, "Master Iron")),
          ("9.63k Master Crystal: 15.39 Master Iron", lambda: reset_button(9630, "Master Crystal", 15.39, "Master Iron")),
          ("90.65k Master Crystal: 37.81 Master Iron", lambda: reset_button(90650, "Master Crystal", 37.81, "Master Iron")),
      ],
      "Master Gold": [
          ("13 Master Iron: 1 Master Gold", lambda: reset_button(13, "Master Iron", 1, "Master Gold")),
          ("82.9 Master Iron: 2.17 Master Gold", lambda: reset_button(82.9, "Master Iron", 2.17, "Master Gold")),
          ("607.95 Master Iron: 4.69 Master Gold", lambda: reset_button(607.95, "Master Iron", 4.69, "Master Gold")),
          ("4.23k Master Iron: 10.08 Master Gold", lambda: reset_button(4230, "Master Iron", 10.08, "Master Gold")),
      ],
      "Master Quartz": [
          ("9 Master Gold: 1 Master Quartz", lambda: reset_button(9, "Master Gold", 1, "Master Quartz")),
          ("39.52 Master Gold: 2.43 Master Quartz", lambda: reset_button(39.52, "Master Gold", 2.43, "Master Quartz")),
          ("329.88 Master Gold: 5.88 Master Quartz", lambda: reset_button(329.88, "Master Gold", 5.88, "Master Quartz")),
      ],
      "Recovery Buttons": [
          ("1 Master White Gems: 50 Master Multiplier (Fetch)", lambda: recovery_button_fetch(1, "Master White Gems", 50, "Master Multiplier")),
          ("1 Master White Gems: 20 Master Rebirths (Fetch)", lambda: recovery_button_fetch(1, "Master White Gems", 20, "Master Rebirths")),
          ("12 Master Crystal: 1 Master Stone (Fetch)", lambda: recovery_button_fetch(12, "Master Crystal", 1, "Master Stone")),
          ("1 Master Iron: 30 Master White Gems (Sets)", lambda: recovery_button_set(1, "Master Iron", 30, "Master White Gems")),
          ("1 Master Gold: 100De Master Multiplier (Sets)", lambda: recovery_button_set(1, "Master Gold", 1e35, "Master Multiplier")),
          ("1 Master Gold: 6 Master Crystal (Sets)", lambda: recovery_button_set(1, "Master Gold", 6, "Master Crystal")),
          ("1 Master Quartz: 1 Master Iron (Sets)", lambda: recovery_button_set(1, "Master Quartz", 1, "Master Iron")),
      ],
      "Area Teleports": [
          ("Elysian Highway (req: 0 Master Cash)", lambda: load_check("EH"))
      ]
  }, 6, "Master Crystal", "CR", voltaic_radar=voltaic_radar)
  Realm(root, { #Room of Fate
      "Master Multiplier": [
          ("1e95 Master Cash: 100T Master Multiplier", lambda: cost_button("Master Cash", 1e95, "Master Multiplier", 1e14)),
          ("3.154e97 Master Cash: 480.95T Master Multiplier", lambda: cost_button("Master Cash", 3.154e97, "Master Multiplier", 4.8095e14)),
          ("2.04e99 Master Cash: 2.3Qd Master Multiplier", lambda: cost_button("Master Cash", 2.04e99, "Master Multiplier", 2.3e15)),
          ("1.2916e101 Master Cash: 10.94Qd Master Multiplier", lambda: cost_button("Master Cash", 1.2916e191, "Master Multiplier", 1.094e16)),
          ("7.32e102 Master Cash: 51.81Qd Master Multiplier", lambda: cost_button("Master Cash", 7.32e102, "Master Multiplier", 5.181e16)),
          ("1.3117e104 Master Cash: 244Qd Master Multiplier", lambda: cost_button("Master Cash", 1.3117e104, "Master Multiplier", 2.24e17)),
          ("1.92e105 Master Cash: 1.14Qn Master Multiplier", lambda: cost_button("Master Cash", 1.92e105, "Master Multiplier", 1.14e18)),
          ("7.378e106 Master Cash: 5.32Qn Master Multiplier", lambda: cost_button("Master Cash", 7.378e106, "Master Multiplier", 5.32e18)),
      ],
      "Master Rebirths": [
          ("1e52 Master Multiplier: 5B Master Rebirths", lambda: reset_button(1e52, "Master Multiplier", 5e9, "Master Rebirths")),
          ("5.4543e53 Master Multiplier: 21.32B Master Rebirths", lambda: reset_button(5.4543e53, "Master Multiplier", 2.132e10, "Master Rebirths")),
          ("7.9e54 Master Multiplier: 90.49B Master Rebirths", lambda: reset_button(7.9e54, "Master Multiplier", 9.049e10, "Master Rebirths")),
          ("2.5925e56 Master Multiplier: 381.01B Master Rebirths", lambda: reset_button(2.5925e56, "Master Multiplier", 3.8101e11, "Master Rebirths")),
          ("1.121e58 Master Multiplier: 1.6T Master Rebirths", lambda: reset_button(1.121e58, "Master Multiplier", 1.6e12, "Master Rebirths")),
          ("2.157e59 Master Multiplier: 6.7T Master Rebirths", lambda: reset_button(2.157e59, "Master Multiplier", 6.7e12, "Master Rebirths")),
      ],
      "Master Stone": [
          ("100Sx Master Rebirths: 1M Master Stone", lambda: reset_button(1e23, "Master Rebirths", 1e6, "Master Stone")),
          ("4.84Sp Master Rebirths: 4M Master Stone", lambda: reset_button(4.84e24, "Master Rebirths", 4e6, "Master Stone")),
          ("270.14Sp Master Rebirths: 15.92M Master Stone", lambda: reset_button(2.7014e26, "Master Rebirths", 1.592e7, "Master Stone")),
          ("9.37Oc Master Rebirths: 63.05M Master Stone", lambda: reset_button(9.37e27, "Master Rebirths", 6.305e7, "Master Stone")),
          ("468.66Oc Master Rebirths: 248.5M Master Stone", lambda: reset_button(4.6866e29, "Master Rebirths", 2.485e8, "Master Stone")),
          ("18.66No Master Rebirths: 974.65M Master Stone", lambda: reset_button(1.866e31, "Master Rebirths", 9.7465e8, "Master Stone")),
          ("445.87No Master Rebirths: 3.8B Master Stone", lambda: reset_button(4.4587e32, "Master Rebirths", 3.8e9, "Master Stone")),
          ("8.49De Master Rebirths: 14.77B Master Stone", lambda: reset_button(8.49e33, "Master Rebirths", 1.477e10, "Master Stone")),
          ("1e38 Master Rebirths: 1T Master Stone", lambda: reset_button(1e38, "Master Rebirths", 1e12, "Master Stone")),
          ("1e42 Master Rebirths: 70T Master Stone", lambda: reset_button(1e42, "Master Rebirths", 7e13, "Master Stone")),
      ],
      "Master White Gems": [
          ("100T Master Stone: 21k Master White Gems", lambda: reset_button(1e14, "Master Stone", 21000, "Master White Gems")),
          ("2.13Qd Master Stone: 76.19k Master White Gems", lambda: reset_button(2.13e15, "Master Stone", 76190, "Master White Gems")),
          ("24.95Qd Master Stone: 275.16k Master White Gems", lambda: reset_button(2.495e16, "Master Stone", 275160, "Master White Gems")),
          ("605.27Qd Master Stone: 989.2k Master White Gems", lambda: reset_button(6.0527e17, "Master Stone", 989200, "Master White Gems")),
          ("20.53Qn Master Stone: 3.53M Master White Gems", lambda: reset_button(2.053e19, "Master Stone", 3.53e6, "Master White Gems")),
          ("239.69Qn Master Stone: 12.61M Master White Gems", lambda: reset_button(2.3969e20, "Master Stone", 1.261e7, "Master White Gems")),
          ("6.7Sx Master Stone: 44.72M Master White Gems", lambda: reset_button(6.7e21, "Master Stone", 4.472e7, "Master White Gems")),
      ],
      "Master Crystal": [
          ("10M Master White Gems: 610 Master Crystal", lambda: reset_button(1e7, "Master White Gems", 610, "Master Crystal")),
          ("359.75M Master White Gems: 1.84k Master Crystal", lambda: reset_button(3.5975e8, "Master White Gems", 1840, "Master Crystal")),
          ("5.29B Master White Gems: 5.56k Master Crystal", lambda: reset_button(5.29e9, "Master White Gems", 5560, "Master Crystal")),
          ("59.02B Master White Gems: 16.68k Master Crystal", lambda: reset_button(5.902e10, "Master White Gems", 16680, "Master Crystal")),
          ("1.65T Master White Gems: 49.84k Master Crystal", lambda: reset_button(1.65e12, "Master White Gems", 49840, "Master Crystal")),
          ("28.24T Master White Gems: 148.25k Master Crystal", lambda: reset_button(2.824e13, "Master White Gems", 148250, "Master Crystal")),
          ("599.05T Master White Gems: 439.13k Master Crystal", lambda: reset_button(5.9905e14, "Master White Gems", 439130, "Master Crystal")),
      ],
      "Master Iron": [
          ("1M Master Crystal: 110 Master Iron", lambda: reset_button(1e6, "Master Crystal", 110, "Master Iron")),
          ("31.86M Master Crystal: 288.57 Master Iron", lambda: reset_button(3.186e7, "Master Crystal", 288.57, "Master Iron")),
          ("696.57M Master Crystal: 754 Master Iron", lambda: reset_button(6.9657e8, "Master Crystal", 754, "Master Iron")),
          ("10.66B Master Crystal: 1.96k Master Iron", lambda: reset_button(1.066e10, "Master Crystal", 1960, "Master Iron")),
          ("189.12B Master Crystal: 5.08k Master Iron", lambda: reset_button(1.8912e11, "Master Crystal", 5080, "Master Iron")),
          ("2.64T Master Crystal: 13.13k Master Iron", lambda: reset_button(2.64e12, "Master Crystal", 13130, "Master Iron")),
      ],
      "Master Gold": [
          ("10k Master Iron: 27 Master Gold", lambda: reset_button(10000, "Master Iron", 27, "Master Gold")),
          ("217.7k Master Iron: 63.64 Master Gold", lambda: reset_button(217700, "Master Iron", 63.64, "Master Gold")),
          ("2.6M Master Iron: 148.07 Master Gold", lambda: reset_button(2.6e6, "Master Iron", 148.07, "Master Gold")),
          ("41.21M Master Iron: 344.88 Master Gold", lambda: reset_button(4.121e7, "Master Iron", 344.88, "Master Gold")),
          ("976.13M Master Iron: 800.39 Master Gold", lambda: reset_button(9.7613e8, "Master Iron", 800.39, "Master Gold")),
          ("10.97B Master Iron: 1.85k Master Gold", lambda: reset_button(1.097e10, "Master Iron", 1850, "Master Gold")),
      ],
      "Master Quartz": [
          ("1k Master Gold: 11 Master Quartz", lambda: reset_button(1000, "Master Gold", 11, "Master Quartz")),
          ("6.66k Master Gold: 22.21 Master Quartz", lambda: reset_button(6660, "Master Gold", 22.21, "Master Quartz")),
          ("50.04k Master Gold: 44.7 Master Quartz", lambda: reset_button(50040, "Master Gold", 44.7, "Master Quartz")),
          ("867.09k Master Gold: 89.68 Master Quartz", lambda: reset_button(867090, "Master Gold", 89.68, "Master Quartz")),
          ("8.35M Master Gold: 179.36 Master Quartz", lambda: reset_button(8.35e6, "Master Gold", 179.36, "Master Quartz")),
          ("148.02M Master Gold: 357.61 Master Quartz", lambda: reset_button(1.4802e8, "Master Gold", 357.61, "Master Quartz")),
      ],
      "Master Jade": [
          ("50 Master Quartz: 1 Master Jade", lambda: reset_button(50, "Master Quartz", 1, "Master Jade")),
          ("675.31 Master Quartz: 2.57 Master Jade", lambda: reset_button(675.31, "Master Quartz", 2.57, "Master Jade")),
          ("4.13k Master Quartz: 3.48 Master Jade", lambda: reset_button(4130, "Master Quartz", 3.48, "Master Jade")),
          ("19.02k Master Quartz: 5.89 Master Jade", lambda: reset_button(19020, "Master Quartz", 5.89, "Master Jade")),
          ("178.62k Master Quartz: 8.09 Master Jade", lambda: reset_button(178620, "Master Quartz", 8.09, "Master Jade")),
      ],
      "Master Obsidian": [
          ("16 Master Jade: 1 Master Obsidian", lambda: reset_button(16, "Master Jade", 1, "Master Obsidian")),
          ("146.93 Master Jade: 1.86 Master Obsidian", lambda: reset_button(146.93, "Master Jade", 1.86, "Master Obsidian")),
          ("300 Master Jade: 3.46 Master Obsidian", lambda: reset_button(300, "Master Jade", 3.46, "Master Obsidian")),
          ("1k Master Jade: 7 Master Obsidian", lambda: reset_button(1000, "Master Jade", 7, "Master Obsidian")),
      ],
      "Master Ruby": [
          ("18 Master Obsidian: 1 Master Ruby", lambda: reset_button(18, "Master Obsidian", 1, "Master Ruby")),
          ("121 Master Obsidian: 5 Master Ruby", lambda: reset_button(121, "Master Obsidian", 5, "Master Ruby")),
          ("524 Master Obsidian: 11 Master Ruby", lambda: reset_button(524, "Master Obsidian", 11, "Master Ruby")),
      ],
      "Recovery Buttons": [
          ("1k Master Iron: 1M Master Multiplier (Fetch)", lambda: recovery_button_fetch(1000, "Master Iron", 1e6, "Master Multiplier")),
          ("1k Master Iron: 50k Master Rebirths (Fetch)", lambda: recovery_button_fetch(1000, "Master Iron", 50000, "Master Rebirths")),
          ("275 Master Gold: 100 Master Stone (Fetch)", lambda: recovery_button_fetch(275, "Master Gold", 100, "Master Stone")),
          ("50 Master Quartz: 1M Master White Gems (Sets)", lambda: recovery_button_set(50, "Master Quartz", 1e6, "Master White Gems")),
          ("1 Master Jade: 1 Master Crystal (Fetch)", lambda: recovery_button_fetch(1, "Master Jade", 1, "Master Crystal")),
          ("1 Master Obsidian: 2k Master Iron (Sets)", lambda: recovery_button_set(1, "Master Obsidian", 2000, "Master Iron")),
          ("1 Master Ruby: 12 Master Jade (Sets)", lambda: recovery_button_set(1, "Master Ruby", 12, "Master Jade")),
      ],
      "Area Teleports": [
          ("Elysian Highway (req: 0 Master Cash)", lambda: load_check("EH"))
      ]
  }, 32, "Master Quartz", "RF", voltaic_radar=voltaic_radar)
  Realm(root, { #Dark Council
      "Master Multiplier": [
          ("1e2274 Master Cash: 1Sx Master Multiplier", lambda: cost_button("Master Cash", Mantissa(1,2274), "Master Multiplier", 1e21)),
      ],
      "Master Rebirths": [
          ("1e850 Master Multiplier: 20T Master Rebirths", lambda: reset_button(Mantissa(1,850), "Master Multiplier", 2e13, "Master Rebirths")),
          ("3.9311e851 Master Multiplier: 90.96T Master Rebirths", lambda: reset_button(Mantissa(3.9311,851), "Master Multiplier", 9.096e13, "Master Rebirths")),
          ("3.578e853 Master Multiplier: 412.45T Master Rebirths", lambda: reset_button(Mantissa(3.578,853), "Master Multiplier", 4.1245e14, "Master Rebirths")),
          ("1.57e855 Master Multiplier: 1.86Qd Master Rebirths", lambda: reset_button(Mantissa(1.57,855), "Master Multiplier", 1.86e15, "Master Rebirths")),
      ],
      "Master Stone": [
          ("1e500 Master Rebirths: 100T Master Stone", lambda: reset_button(Mantissa(1,500), "Master Rebirths", 1e14, "Master Stone")),
          ("9.9853e503 Master Rebirths: 1.08Qd Master Stone", lambda: reset_button(Mantissa(9.9853,503), "Master Rebirths", 1.08e15, "Master Stone")),
          ("6.06e507 Master Rebirths: 11.74Qd Master Stone", lambda: reset_button(Mantissa(6.06,507), "Master Rebirths", 1.174e16, "Master Stone")),
          ("6.902e511 Master Rebirths: 127.29Qd Master Stone", lambda: reset_button(Mantissa(6.902,511), "Master Rebirths", 1.2729e17, "Master Stone")),
      ],
      "Master White Gems": [
          ("1e333 Master Stone: 100k Master White Gems", lambda: reset_button(Mantissa(1,333), "Master Stone", 1e5, "Master White Gems")),
          ("2.28e336 Master Stone: 472.8k Master White Gems", lambda: reset_button(Mantissa(2.28,336), "Master Stone", 4.728e5, "Master White Gems")),
          ("1.082e340 Master Stone: 2.24M Master White Gems", lambda: reset_button(Mantissa(1.082,340), "Master Stone", 2.24e6, "Master White Gems")),
          ("4.219e343 Master Stone: 10.62M Master White Gems", lambda: reset_button(Mantissa(4.219,343), "Master Stone", 1.062e7, "Master White Gems")),
          ("2.7344e347 Master Stone: 50.3M Master White Gems", lambda: reset_button(Mantissa(2.7344,347), "Master Stone", 5.03e7, "Master White Gems")),
          ("1.59e351 Master Stone: 238.04M Master White Gems", lambda: reset_button(Mantissa(1.59,351), "Master Stone", 2.3804e8, "Master White Gems")),
          ("8.83e354 Master Stone: 1.12B Master White Gems", lambda: reset_button(Mantissa(8.83,354), "Master Stone", 1.12e9, "Master White Gems")),
          ("4.568e358 Master Stone: 5.32B Master White Gems", lambda: reset_button(Mantissa(4.568,358), "Master Stone", 5.32e9, "Master White Gems")),
      ],
      "Master Crystal": [
          ("1e196 Master White Gems: 1M Master Crystal", lambda: reset_button(1e196, "Master White Gems", 1e6, "Master Crystal")),
          ("5.54e198 Master White Gems: 4.69M Master Crystal", lambda: reset_button(5.54e198, "Master White Gems", 4.69e6, "Master Crystal")),
          ("2.68e201 Master White Gems: 22.01M Master Crystal", lambda: reset_button(2.68e201, "Master White Gems", 2.201e7, "Master Crystal")),
          ("2.96e204 Master White Gems: 103.08M Master Crystal", lambda: reset_button(2.96e204, "Master White Gems", 1.0308e8, "Master Crystal")),
      ],
      "Master Iron": [
          ("1e96 Master Crystal: 40k Master Iron", lambda: reset_button(1e96, "Master Crystal", 40000, "Master Iron")),
          ("2.2273e98 Master Crystal: 206.78k Master Iron", lambda: reset_button(2.2273e98, "Master Crystal", 206780, "Master Iron")),
          ("4.867e100 Master Crystal: 1.06M Master Iron", lambda: reset_button(4.867e100, "Master Crystal", 1.06e6, "Master Iron")),
          ("1.057e103 Master Crystal: 5.49M Master Iron", lambda: reset_button(1.057e103, "Master Crystal", 5.49e6, "Master Iron")),
          ("2.11e105 Master Crystal: 28.26M Master Iron", lambda: reset_button(2.11e105, "Master Crystal", 2.826e7, "Master Iron")),
          ("1.3103e113 Master Crystal: 3.8B Master Iron", lambda: reset_button(1.3103e113, "Master Crystal", 3.8e9, "Master Iron")),
      ],
      "Master Gold": [
          ("1e60 Master Iron: 5k Master Gold", lambda: reset_button(1e60, "Master Iron", 5000, "Master Gold")),
          ("2.0743e62 Master Iron: 28.58k Master Gold", lambda: reset_button(2.0743e62, "Master Iron", 28580, "Master Gold")),
          ("3.485e64 Master Iron: 163.12k Master Gold", lambda: reset_button(3.485e64, "Master Iron", 163120, "Master Gold")),
          ("2.48e66 Master Iron: 928.89k Master Gold", lambda: reset_button(2.48e66, "Master Iron", 928890, "Master Gold")),
      ],
      "Master Quartz": [
          ("10Sx Master Gold: 600 Master Quartz", lambda: reset_button(1e22, "Master Gold", 600, "Master Quartz")),
          ("1.46Sp Master Gold: 2.71k Master Quartz", lambda: reset_button(1.46e24, "Master Gold", 2710, "Master Quartz")),
          ("210.38Sp Master Gold: 12.27k Master Quartz", lambda: reset_button(2.1038e26, "Master Gold", 12270, "Master Quartz")),
          ("21.35Oc Master Gold: 55.29k Master Quartz", lambda: reset_button(2.135e28, "Master Gold", 55290, "Master Quartz")),
      ],
      "Master Jade": [
          ("100M Master Quartz: 15 Master Jade", lambda: reset_button(1e8, "Master Quartz", 15, "Master Jade")),
          ("2.7B Master Quartz: 58.09 Master Jade", lambda: reset_button(2.7e9, "Master Quartz", 58.09, "Master Jade")),
          ("132B Master Quartz: 224.26 Master Jade", lambda: reset_button(1.32e11, "Master Quartz", 224.26, "Master Jade")),
          ("9.71T Master Quartz: 864.24 Master Jade", lambda: reset_button(9.71e12, "Master Quartz", 864.24, "Master Jade")),
      ],
      "Master Obsidian": [
          ("10M Master Jade: 11 Master Obsidian", lambda: reset_button(1e7, "Master Jade", 11, "Master Obsidian")),
          ("95.34M Master Jade: 20.54 Master Obsidian", lambda: reset_button(9.534e7, "Master Jade", 20.54, "Master Obsidian")),
          ("1.01B Master Jade: 38.28 Master Obsidian", lambda: reset_button(1.01e9, "Master Jade", 38.28, "Master Obsidian")),
          ("7.58B Master Jade: 71.19 Master Obsidian", lambda: reset_button(7.58e9, "Master Jade", 71.19, "Master Obsidian")),
      ],
      "Master Ruby": [
          ("1k Master Obsidian: 20 Master Ruby", lambda: reset_button(1000, "Master Obsidian", 20, "Master Ruby")),
          ("6.44k Master Obsidian: 29.13 Master Ruby", lambda: reset_button(6440, "Master Obsidian", 29.13, "Master Ruby")),
          ("13k Master Obsidian: 42.37 Master Ruby", lambda: reset_button(13000, "Master Obsidian", 42.37, "Master Ruby")),
          ("129.91k Master Obsidian: 61.55 Master Ruby", lambda: reset_button(129910, "Master Obsidian", 61.55, "Master Ruby")),
          ("1.61M Master Obsidian: 89.27 Master Ruby", lambda: reset_button(1.61e6, "Master Obsidian", 89.27, "Master Ruby")),
          ("35.49M Master Obsidian: 129.3 Master Ruby", lambda: reset_button(3.549e7, "Master Obsidian", 129.3, "Master Ruby")),
      ],
      "Master Emerald": [
          ("532 Master Ruby: 1 Master Emerald", lambda: cost_button("Master Ruby", 532, "Master Emerald", 1)),
          ("5.06k Master Ruby: 2.08 Master Emerald", lambda: cost_button("Master Ruby", 5060, "Master Emerald", 2.08)),
          ("59.72k Master Ruby: 4.35 Master Emerald", lambda: cost_button("Master Ruby", 59720, "Master Emerald", 4.35)),
      ],
      "Master Sapphire": [
          ("10k Master Emerald: 1 Master Sapphire", lambda: cost_button("Master Emerald", 10000, "Master Sapphire", 1)),
          ("59.89k Master Emerald: 1.89 Master Sapphire", lambda: cost_button("Master Emerald", 59890, "Master Sapphire", 1.89)),
          ("414.96k Master Emerald: 3.6 Master Sapphire", lambda: cost_button("Master Emerald", 414960, "Master Sapphire", 3.6)),
      ],
      "Master Diamond": [
          ("1k Master Sapphire: 1 Master Diamond", lambda: reset_button(1000, "Master Sapphire", 1, "Master Diamond")),
          ("6.37k Master Sapphire: 2.06 Master Diamond", lambda: reset_button(6370, "Master Sapphire", 2.06, "Master Diamond")),
          ("37.47k Master Sapphire: 4.24 Master Diamond", lambda: reset_button(37470, "Master Sapphire", 4.24, "Master Diamond")),
          ("316.11k Master Sapphire: 8.71 Master Diamond", lambda: reset_button(316110, "Master Sapphire", 8.71, "Master Diamond")),
      ],
      "Recovery Buttons": [
          ("100k Master Gold: 1T Master Multiplier (Fetch)", lambda: recovery_button_fetch(100000, "Master Gold", 1e12, "Master Multiplier")),
          ("10k Master Obsidian: 1.25 Master Gold (Fetch)", lambda: recovery_button_fetch(10000, "Master Obsidian", 1.25, "Master Gold")),
          ("100k Master Obsidian: 1k Master White Gems (Fetch)", lambda: recovery_button_fetch(100000, "Master Obsidian", 1000, "Master White Gems")),
          ("1 Master Ruby: 666 Master Quartz (Sets)", lambda: recovery_button_set(1, "Master Ruby", 666, "Master Quartz")),
          ("300 Master Ruby: 75 Master Crystal (Fetch)", lambda: recovery_button_fetch(300, "Master Ruby", 75, "Master Crystal")),
          ("1 Master Emerald: 88 Master Obsidian (Sets)", lambda: recovery_button_set(1, "Master Emerald", 88, "Master Obsidian")),
          ("1 Master Sapphire: 2 Master Jade (Fetch)", lambda: recovery_button_fetch(1, "Master Sapphire", 2, "Master Jade")),
          ("1 Master Diamond: 250 Master Ruby (Sets)", lambda: recovery_button_set(1, "Master Diamond", 250, "Master Ruby")),
      ],
      "Area Teleports": [
          ("Elysian Highway (req: 0 Master Cash)", lambda: load_check("EH"))
      ]
  }, 250, "Master Ruby", "DC", voltaic_radar=voltaic_radar)
  Realm(root, { #Astral Archipelago
      "Master Ruby": [
          ("1e40 Master Obsidian: 222 Master Ruby", lambda: reset_button(1e40, "Master Obsidian", 222, "Master Ruby")),
          ("3.2644e41 Master Obsidian: 616.14 Master Ruby", lambda: reset_button(3.2644e41, "Master Obsidian", 616.14, "Master Ruby")),
          ("2.956e43 Master Obsidian: 1.7k Master Ruby", lambda: reset_button(2.956e43, "Master Obsidian", 1700, "Master Ruby")),
          ("2.74e45 Master Obsidian: 4.71k Master Ruby", lambda: reset_button(2.74e45, "Master Obsidian", 4710, "Master Ruby")),
          ("1.9176e47 Master Obsidian: 13k Master Ruby", lambda: reset_button(1.9176e47, "Master Obsidian", 13000, "Master Ruby")),
          ("1.73e49 Master Obsidian: 35.74k Master Ruby", lambda: reset_button(1.73e49, "Master Obsidian", 35740, "Master Ruby")),
          ("5.2862e50 Master Obsidian: 98.1k Master Ruby", lambda: reset_button(5.2862e50, "Master Obsidian", 98100, "Master Ruby")),
      ],
      "Master Emerald": [
          ("100Qn Master Ruby: 6 Master Emerald", lambda: cost_button("Master Ruby", 1e20, "Master Emerald", 6)),
          ("3.48Sx Master Ruby: 16.98 Master Emerald", lambda: cost_button("Master Ruby", 3.48e21, "Master Emerald", 16.98)),
          ("221.82Sx Master Ruby: 47.96 Master Emerald", lambda: cost_button("Master Ruby", 2.2182e23, "Master Emerald", 47.96)),
          ("18.86Sp Master Ruby: 135.17 Master Emerald", lambda: cost_button("Master Ruby", 1.886e25, "Master Emerald", 135.17)),
          ("1No Master Ruby: 6k Master Emerald", lambda: cost_button("Master Ruby", 1e30, "Master Emerald", 6000)),
      ],
      "Master Sapphire": [
          ("10B Master Emerald: 7 Master Sapphire", lambda: cost_button("Master Emerald", 1e10, "Master Sapphire", 7)),
          ("228.36B Master Emerald: 19.41 Master Sapphire", lambda: cost_button("Master Emerald", 2.2836e11, "Master Sapphire", 19.41)),
          ("3.81T Master Emerald: 34.21 Master Sapphire", lambda: cost_button("Master Emerald", 3.81e12, "Master Sapphire", 34.21)),
          ("95.67T Master Emerald: 60.18 Master Sapphire", lambda: cost_button("Master Emerald", 9.567e13, "Master Sapphire", 60.18)),
          ("1Qd Master Emerald: 200 Master Sapphire", lambda: cost_button("Master Emerald", 1e15, "Master Sapphire", 200)),
          ("500Qd Master Emerald: 1.6k Master Sapphire", lambda: cost_button("Master Emerald", 5e17, "Master Sapphire", 1600)),
      ],
      "Master Diamond": [
          ("1M Master Sapphire: 14 Master Diamond", lambda: reset_button(1e6, "Master Sapphire", 14, "Master Diamond")),
          ("7.98M Master Sapphire: 26.12 Master Diamond", lambda: reset_button(7.98e6, "Master Sapphire", 26.12, "Master Diamond")),
          ("29.42M Master Sapphire: 48.65 Master Diamond", lambda: reset_button(2.942e7, "Master Sapphire", 48.65, "Master Diamond")),
          ("89.84M Master Sapphire: 90.45 Master Diamond", lambda: reset_button(8.984e7, "Master Sapphire", 90.45, "Master Diamond")),
          ("341.11M Master Sapphire: 167.9 Master Diamond", lambda: reset_button(3.4111e8, "Master Sapphire", 167.9, "Master Diamond")),
          ("991.69M Master Sapphire: 311.13 Master Diamond", lambda: reset_button(9.9169e8, "Master Sapphire", 311.13, "Master Diamond")),
          ("4.47B Master Sapphire: 575.56 Master Diamond", lambda: reset_button(4.47e9, "Master Sapphire", 575.56, "Master Diamond")),
          ("14.18B Master Sapphire: 1.06k Master Diamond", lambda: reset_button(1.418e10, "Master Sapphire", 1060, "Master Diamond")),
          ("52.27B Master Sapphire: 1.95k Master Diamond", lambda: reset_button(5.227e10, "Master Sapphire", 1950, "Master Diamond")),
          ("115.79B Master Sapphire: 3.6k Master Diamond", lambda: reset_button(1.1579e11, "Master Sapphire", 3600, "Master Diamond")),
      ],
      "Master Starlight": [
          ("500 Master Diamond: 1 Master Starlight", lambda: reset_button(500, "Master Diamond", 1, "Master Starlight")),
          ("3.93k Master Diamond: 1.73 Master Starlight", lambda: reset_button(3930, "Master Diamond", 1.73, "Master Starlight")),
          ("19.88k Master Diamond: 3 Master Starlight", lambda: reset_button(19880, "Master Diamond", 3, "Master Starlight")),
          ("142.2k Master Diamond: 5.19 Master Starlight", lambda: reset_button(142200, "Master Diamond", 5.19, "Master Starlight")),
          ("1M Master Diamond: 8.96 Master Starlight", lambda: reset_button(1e6, "Master Diamond", 8.96, "Master Starlight")),
          ("3.76M Master Diamond: 15.45 Master Starlight", lambda: reset_button(3.76e6, "Master Diamond", 15.45, "Master Starlight")),
          ("13.4M Master Diamond: 26.58 Master Starlight", lambda: reset_button(1.34e7, "Master Diamond", 26.58, "Master Starlight")),
      ],
      "Master Ion": [
          ("10 Master Starlight: 1 Master Ion", lambda: reset_button(10, "Master Starlight", 1, "Master Ion")),
          ("30 Master Starlight: 1.72 Master Ion", lambda: reset_button(30, "Master Starlight", 1.72, "Master Ion")),
          ("86 Master Starlight: 2.97 Master Ion", lambda: reset_button(86, "Master Starlight", 2.97, "Master Ion")),
          ("121 Master Starlight: 5.12 Master Ion", lambda: reset_button(121, "Master Starlight", 5.12, "Master Ion")),
          ("183 Master Starlight: 8.8 Master Ion", lambda: reset_button(183, "Master Starlight", 8.8, "Master Ion")),
          ("300 Master Starlight: 15.1 Master Ion", lambda: reset_button(300, "Master Starlight", 15.1, "Master Ion")),
      ],
      "Master Uranium": [
          ("66 Master Ion: 1 Master Uranium", lambda: reset_button(66, "Master Ion", 1, "Master Uranium")),
      ],
      "Master Mint": [
          ("1e6666 Master Rebirths: 1 Master Mint", lambda: cost_button("Master Rebirths", Mantissa(1,6666), "Master Mint", 1)),
          ("8.25e6968 Master Rebirths: 2 Master Mint", lambda: cost_button("Master Rebirths", Mantissa(8.25,6968), "Master Mint", 2)),
          ("4.21e7271 Master Rebirths: 4 Master Mint", lambda: cost_button("Master Rebirths", Mantissa(4.21,7271), "Master Mint", 4)),
          ("4.13e7574 Master Rebirths: 8 Master Mint", lambda: cost_button("Master Rebirths", Mantissa(4.13,7574), "Master Mint", 8)),
          ("4.15e7877 Master Rebirths: 16 Master Mint", lambda: cost_button("Master Rebirths", Mantissa(4.15,7877), "Master Mint", 16)),
      ],
      "Recovery": [
          ("50 Master Diamond: 50 Master Obsidian (Fetch)", lambda: recovery_button_fetch(50, "Master Diamond", 50, "Master Obsidian")),
          ("1 Master Starlight: 2.5 Master Ruby (Fetch)", lambda: recovery_button_fetch(1, "Master Starlight", 2.5, "Master Ruby")),
          ("1 Master Ion: 1.75 Master Emerald (Fetch)", lambda: recovery_button_fetch(1, "Master Ion", 1.75, "Master Emerald")),
          ("1 Master Uranium: 50 Master Diamond (Sets)", lambda: recovery_button_set(1, "Master Uranium", 50, "Master Diamond")),
      ],
      "Area Teleports": [
          ("Elysian Highway (req: 0 Master Cash)", lambda: load_check("EH"))
      ]
  }, 50, "Master Diamond", "AA", voltaic_radar=voltaic_radar)
  Realm(root, { #Limbo
      "Master Multiplier": [
          ("1e10000 Master Cash: 100Sx Master Multiplier", lambda: cost_button("Master Cash", Mantissa(1,10000), "Master Multiplier", 1e23)),
          ("1.31e10465 Master Cash: 267.14Sx Master Multiplier", lambda: cost_button("Master Cash", Mantissa(1.31,10465), "Master Multiplier", 2.6714e23)),
          ("7.34e10951 Master Cash: 647.53Sx Master Multiplier", lambda: cost_button("Master Cash", Mantissa(7.34,10951), "Master Multiplier", 6.4753e23)),
          ("1.8e11461 Master Cash: 1.56Sp Master Multiplier", lambda: cost_button("Master Cash", Mantissa(1.8,11461), "Master Multiplier", 1.56e24)),
      ],
      "Master Rebirths": [
          ("1e4633 Master Multiplier: 7.09Qd Master Rebirths", lambda: reset_button(Mantissa(1,4633), "Master Multiplier", 7.09e15, "Master Rebirths")),
          ("2.77e4847 Master Multiplier: 17.11Qd Master Rebirths", lambda: reset_button(Mantissa(2.77,4847), "Master Multiplier", 1.711e16, "Master Rebirths")),
          ("8.02e5072 Master Multiplier: 41.16Qd Master Rebirths", lambda: reset_button(Mantissa(8.02,5072), "Master Multiplier", 4.116e16, "Master Rebirths")),
          ("7.13e5308 Master Multiplier: 98.85Qd Master Rebirths", lambda: reset_button(Mantissa(7.13,5308), "Master Multiplier", 9.885e16, "Master Rebirths")),
      ],
      "Master Stone": [
          ("1e982 Master Rebirths: 600Qd Master Stone", lambda: reset_button(Mantissa(1,982), "Master Rebirths", 6e17, "Master Stone")),
          ("2.01e1029 Master Rebirths: 2.63Qn Master Stone", lambda: reset_button(Mantissa(2.01,1029), "Master Rebirths", 2.63e18, "Master Stone")),
          ("3.35e1072 Master Rebirths: 6.28Qn Master Stone", lambda: reset_button(Mantissa(3.35,1072), "Master Rebirths", 6.28e18, "Master Stone")),
          ("5.75e1117 Master Rebirths: 14.97Qn Master Stone", lambda: reset_button(Mantissa(5.75,1117), "Master Rebirths", 1.497e19, "Master Stone")),
      ],
      "Master White Gems": [
          ("1e603 Master Stone: 31B Master White Gems", lambda: reset_button(Mantissa(1,603), "Master Stone", 3.1e10, "Master White Gems")),
          ("1.113e631 Master Stone: 73.62B Master White Gems", lambda: reset_button(Mantissa(1.113,631), "Master Stone", 7.362e10, "Master White Gems")),
          ("2.5e660 Master Stone: 174.52B Master White Gems", lambda: reset_button(Mantissa(2.5,660), "Master Stone", 1.7452e11, "Master White Gems")),
          ("1.3e691 Master Stone: 414.04B Master White Gems", lambda: reset_button(Mantissa(1.3,691), "Master Stone", 4.1404e11, "Master White Gems")),
      ],
      "Master Crystal": [
          ("1e400 Master White Gems: 510M Master Crystal", lambda: reset_button(Mantissa(1,400), "Master White Gems", 5.1e8, "Master Crystal")),
          ("4.024e418 Master White Gems: 1.2B Master Crystal", lambda: reset_button(Mantissa(4.024,418), "Master White Gems", 1.2e9, "Master Crystal")),
          ("1.1875e438 Master White Gems: 2.83B Master Crystal", lambda: reset_button(Mantissa(1.1875,438), "Master White Gems", 2.83e9, "Master Crystal")),
          ("2.8196e458 Master White Gems: 6.65B Master Crystal", lambda: reset_button(Mantissa(2.8196,458), "Master White Gems", 6.65e9, "Master Crystal")),
      ],
      "Master Iron": [
          ("1e274 Master Crystal: 4.59B Master Iron", lambda: reset_button(1e274, "Master Crystal", 4.59e9, "Master Iron")),
          ("4.1648e275 Master Crystal: 10.77B Master Iron", lambda: reset_button(4.1648e275, "Master Crystal", 1.077e10, "Master Iron")),
          ("8.92e276 Master Crystal: 25.17B Master Iron", lambda: reset_button(8.92e276, "Master Crystal", 2.517e10, "Master Iron")),
          ("1.287e278 Master Crystal: 58.78B Master Iron", lambda: reset_button(1.287e278, "Master Crystal", 5.878e10, "Master Iron")),
      ],
      "Master Gold": [
          ("1e168 Master Iron: 1.1M Master Gold", lambda: reset_button(1e168, "Master Iron", 1.1e6, "Master Gold")),
          ("5.368e169 Master Iron: 2.55M Master Gold", lambda: reset_button(5.368e169, "Master Iron", 2.55e6, "Master Gold")),
          ("2.67e171 Master Iron: 5.93M Master Gold", lambda: reset_button(2.67e171, "Master Iron", 5.93e6, "Master Gold")),
          ("9.585e172 Master Iron: 13.75M Master Gold", lambda: reset_button(9.585e172, "Master Iron", 1.375e7, "Master Gold")),
      ],
      "Master Quartz": [
          ("1e300 Master Gold: 110k Master Quartz", lambda: reset_button(Mantissa(1,300), "Master Gold", 110000, "Master Quartz")),
          ("8.984e313 Master Gold: 254.04k Master Quartz", lambda: reset_button(Mantissa(8.984,313), "Master Gold", 254040, "Master Quartz")),
          ("3.597e328 Master Gold: 585.73k Master Quartz", lambda: reset_button(Mantissa(3.597,328), "Master Gold", 585730, "Master Quartz")),
          ("6.881e343 Master Gold: 1.34M Master Quartz", lambda: reset_button(Mantissa(6.881,343), "Master Gold", 1.34e6, "Master Quartz")),
      ],
      "Master Jade": [
          ("1e189 Master Quartz: 1.09k Master Jade", lambda: reset_button(1e189, "Master Quartz", 1090, "Master Jade")),
          ("2.653e190 Master Quartz: 2.52k Master Jade", lambda: reset_button(2.653e190, "Master Quartz", 2520, "Master Jade")),
          ("1.18755e192 Master Quartz: 5.77k Master Jade", lambda: reset_button(1.18755e192, "Master Quartz", 5770, "Master Jade")),
          ("5.883e193 Master Quartz: 13.21k Master Jade", lambda: reset_button(5.883e193, "Master Quartz", 13210, "Master Jade")),
      ],
      "Master Obsidian": [
          ("1e90 Master Jade: 150 Master Obsidian", lambda: reset_button(1e90, "Master Jade", 150, "Master Obsidian")),
          ("3.21e91 Master Jade: 341.85 Master Obsidian", lambda: reset_button(3.21e91, "Master Jade", 341.85, "Master Obsidian")),
          ("1.38e93 Master Jade: 777.85 Master Obsidian", lambda: reset_button(1.38e93, "Master Jade", 777.85, "Master Obsidian")),
          ("7.211e94 Master Jade: 1.76k Master Obsidian", lambda: reset_button(7.211e94, "Master Jade", 1760, "Master Obsidian")),
      ],
      "Master Ruby": [
          ("1e62 Master Obsidian: 210k Master Ruby", lambda: reset_button(1e62, "Master Obsidian", 210000, "Master Ruby")),
          ("4.85e63 Master Obsidian: 475.51k Master Ruby", lambda: reset_button(4.85e63, "Master Obsidian", 475510, "Master Ruby")),
          ("2.2477e65 Master Obsidian: 1.07M Master Ruby", lambda: reset_button(2.2477e65, "Master Obsidian", 1.07e6, "Master Ruby")),
          ("9.98e66 Master Obsidian: 2.42M Master Ruby", lambda: reset_button(9.98e66, "Master Obsidian", 2.42e6, "Master Ruby")),
          ("3.5996e68 Master Obsidian: 5.46M Master Ruby", lambda: reset_button(3.5996e68, "Master Obsidian", 5.46e6, "Master Ruby")),
          ("1.821e70 Master Obsidian: 12.3M Master Ruby", lambda: reset_button(1.821e70, "Master Obsidian", 1.23e7, "Master Ruby")),
      ],
      "Master Emerald": [
          ("1e37 Master Ruby: 11k Master Emerald", lambda: cost_button("Master Ruby", 1e37, "Master Emerald", 11000)),
          ("5.5966e38 Master Ruby: 24.67k Master Emerald", lambda: cost_button("Master Ruby", 5.5966e38, "Master Emerald", 24670)),
          ("2.75e40 Master Ruby: 55.25k Master Emerald", lambda: cost_button("Master Ruby", 2.75e40, "Master Emerald", 55250)),
          ("9.7656e41 Master Ruby: 123.53k Master Emerald", lambda: cost_button("Master Ruby", 9.7656e41, "Master Emerald", 123530)),
          ("5.314e43 Master Ruby: 275.8k Master Emerald", lambda: cost_button("Master Ruby", 5.314e43, "Master Emerald", 275800)),
      ],
      "Master Sapphire": [
          ("1Sx Master Emerald: 4.5k Master Sapphire", lambda: cost_button("Master Emerald", 1e21, "Master Sapphire", 4500)),
          ("27.04Sx Master Emerald: 10.01k Master Sapphire", lambda: cost_button("Master Emerald", 2.704e22, "Master Sapphire", 10010)),
          ("344.68Sx Master Emerald: 22.25k Master Sapphire", lambda: cost_button("Master Emerald", 3.4468e23, "Master Sapphire", 22250)),
          ("9.18Sp Master Emerald: 49.38k Master Sapphire", lambda: cost_button("Master Emerald", 9.18e24, "Master Sapphire", 49380)),
      ],
      "Master Diamond": [
          ("100T Master Sapphire: 11k Master Diamond", lambda: reset_button(1e14, "Master Sapphire", 11000, "Master Diamond")),
          ("2.17Qd Master Sapphire: 24.33k Master Diamond", lambda: reset_button(2.17e15, "Master Sapphire", 24330, "Master Diamond")),
          ("97.59Qd Master Sapphire: 53.73k Master Diamond", lambda: reset_button(9.759e16, "Master Sapphire", 53730, "Master Diamond")),
          ("3.51Qn Master Sapphire: 118.53k Master Diamond", lambda: reset_button(3.51e18, "Master Sapphire", 118530, "Master Diamond")),
      ],
      "Master Starlight": [
          ("4Qd Master Diamond: 50 Master Starlight", lambda: reset_button(4e15, "Master Diamond", 50, "Master Starlight")),
          ("124.35Qd Master Diamond: 87.24 Master Starlight", lambda: reset_button(1.24e17, "Master Diamond", 87.24, "Master Starlight")),
          ("1.63Qn Master Diamond: 152.06 Master Starlight", lambda: reset_button(1.63e18, "Master Diamond", 152.06, "Master Starlight")),
          ("12.34Qn Master Diamond: 264.69 Master Starlight", lambda: reset_button(1.234e19, "Master Diamond", 264.69, "Master Starlight")),
      ],
      "Master Ion": [
          ("1M Master Starlight: 30 Master Ion", lambda: reset_button(1e6, "Master Starlight", 30, "Master Ion")),
          ("6.67M Master Starlight: 46.47 Master Ion", lambda: reset_button(6.67e6, "Master Starlight", 46.47, "Master Ion")),
          ("76.74M Master Starlight: 71.92 Master Ion", lambda: reset_button(7.674e7, "Master Starlight", 71.92, "Master Ion")),
          ("704.55M Master Starlight: 111.18 Master Ion", lambda: reset_button(7.0455e8, "Master Starlight", 111.18, "Master Ion")),
      ],
      "Master Uranium": [
          ("375 Master Ion: 3 Master Uranium", lambda: reset_button(375, "Master Ion", 3, "Master Uranium")),
          ("1.3k Master Ion: 4.32 Master Uranium", lambda: reset_button(1300, "Master Ion", 4.32, "Master Uranium")),
          ("5.9k Master Ion: 6.24 Master Uranium", lambda: reset_button(5900, "Master Ion", 6.24, "Master Uranium")),
          ("17.84k Master Ion: 9 Master Uranium", lambda: reset_button(17840, "Master Ion", 9, "Master Uranium")),
      ],
      "Master Bismuth": [
          ("36 Master Uranium: 1 Master Bismuth", lambda: reset_button(36, "Master Uranium", 1, "Master Bismuth")),
          ("154.67 Master Uranium: 2.58 Master Bismuth", lambda: reset_button(154.67, "Master Uranium", 2.58, "Master Bismuth")),
          ("596.25 Master Uranium: 6.66 Master Bismuth", lambda: reset_button(596.25, "Master Uranium", 6.66, "Master Bismuth")),
          ("2.57k Master Uranium: 17.15 Master Bismuth", lambda: reset_button(2570, "Master Uranium", 17.15, "Master Bismuth")),
      ],
      "Master Boracite": [
          ("18 Master Bismuth: 1 Master Boracite", lambda: reset_button(18, "Master Bismuth", 1, "Master Boracite")),
          ("69.97 Master Bismuth: 2.25 Master Boracite", lambda: reset_button(69.97, "Master Bismuth", 2.25, "Master Boracite")),
          ("216.32 Master Bismuth: 5.09 Master Boracite", lambda: reset_button(216.32, "Master Bismuth", 5.09, "Master Boracite")),
      ],
      "Master Nissonite": [
          ("50 Master Boracite: 1 Master Nissonite", lambda: reset_button(50, "Master Boracite", 1, "Master Nissonite")),
      ],
      "Recovery": [
          ("15 Master Mint: 696 Master Sapphire (Sets)", lambda: recovery_button_set(15, "Master Mint", 696, "Master Sapphire")),
          ("50 Master Mint: 500 Master Quartz (Fetch)", lambda: recovery_button_fetch(50, "Master Mint", 500, "Master Quartz")),
          ("500 Master Obsidian: 10B Master Multiplier (Fetch)", lambda: recovery_button_fetch(500, "Master Obsidian", 1e10, "Master Multiplier")),
          ("500 Master Obsidian: 1B Master Rebirths (Fetch)", lambda: recovery_button_fetch(500, "Master Obsidian", 1e9, "Master Rebirths")),
          ("1e45 Master Jade: 1e12 Master Iron (Fetch)", lambda: recovery_button_fetch(1e45, "Master Jade", 1e12, "Master Iron")),
          ("10k Master Diamond: 10M Master Obsidian (Fetch)", lambda: recovery_button_fetch(10000, "Master Diamond", 1e7, "Master Obsidian")),
          ("1 Master Bismuth: 7 Master Diamond (Fetch)", lambda: recovery_button_fetch(1, "Master Bismuth", 7, "Master Diamond")),
          ("1 Master Boracite: 10k Master Ruby (Fetch)", lambda: recovery_button_fetch(1, "Master Boracite", 10000, "Master Ruby")),
          ("1 Master Boracite: 250 Master Ion (Sets)", lambda: recovery_button_set(1, "Master Boracite", 250, "Master Ion")),
          ("1 Master Nissonite: 10 Master Uranium (Sets)", lambda: recovery_button_set(1, "Master Nissonite", 10, "Master Uranium")),
          ("1 Master Aquamarine: 1 Master Uranium (Fetch)", lambda: recovery_button_fetch(1, "Master Aquamarine", 1, "Master Uranium")),
          ("4 Master Aquamarine: 6 Master Tetra (Sets)", lambda: recovery_button_set(4, "Master Aquamarine", 6, "Master Tetra")),
          ("1 Master Lollipop: 175 Master Volt (Sets)", lambda: recovery_button_set(1, "Master Lollipop", 175, "Master Volt")),
      ],
      "Area Teleports": [
          ("Elysian Highway (req: 0 Master Cash)", lambda: load_check("EH")),
          ("The Lost Grounds (req: 3 Master Nissonite)", lambda: load_check("TLG")),
          ("Forbidden Altar (req: 57 Master Volt)", lambda: load_check("FA"))
      ]
  }, 8, "Master Uranium", "L", voltaic_radar=voltaic_radar)
  Realm(root, { #The Lost Grounds
      "Master Diamond": [
          ("5e190 Master Sapphire: 400k Master Diamond", lambda: reset_button(5e190, "Master Sapphire", 400000, "Master Diamond")),
          ("1.92e192 Master Sapphire: 873k Master Diamond", lambda: reset_button(1.92e192, "Master Sapphire", 873000, "Master Diamond")),
          ("1.0456e194 Master Sapphire: 1.9M Master Diamond", lambda: reset_button(1.0456e194, "Master Sapphire", 1.9e6, "Master Diamond")),
          ("6e195 Master Sapphire: 4.14M Master Diamond", lambda: reset_button(6e195, "Master Sapphire", 4.14e6, "Master Diamond")),
      ],
      "Master Starlight": [
          ("1e97 Master Diamond: 650 Master Starlight", lambda: reset_button(1e97, "Master Diamond", 650, "Master Starlight")),
          ("2.524e98 Master Diamond: 1.41k Master Starlight", lambda: reset_button(2.524e98, "Master Diamond", 1410, "Master Starlight")),
          ("1.22777e99 Master Diamond: 3.05k Master Starlight", lambda: reset_button(1.22777e99, "Master Diamond", 3050, "Master Starlight")),
          ("5.558e100 Master Diamond: 6.61k Master Starlight", lambda: reset_button(5.558e100, "Master Diamond", 6610, "Master Starlight")),
          ("2.18e102 Master Diamond: 14.3k Master Starlight", lambda: reset_button(2.18e102, "Master Diamond", 14300, "Master Starlight")),
      ],
      "Master Ion": [
          ("1e45 Master Starlight: 300 Master Ion", lambda: reset_button(1e45, "Master Starlight", 300, "Master Ion")),
          ("7.272e46 Master Starlight: 646.73 Master Ion", lambda: reset_button(7.272e46, "Master Starlight", 646.73, "Master Ion")),
          ("1.95e48 Master Starlight: 1.4k Master Ion", lambda: reset_button(1.95e48, "Master Starlight", 1400, "Master Ion")),
          ("7.296e49 Master Starlight: 3k Master Ion", lambda: reset_button(7.296e49, "Master Starlight", 3000, "Master Ion")),
          ("4.17e51 Master Starlight: 6.42k Master Ion", lambda: reset_button(4.17e51, "Master Starlight", 6420, "Master Ion")),
      ],
      "Master Uranium": [
          ("30Sp Master Ion: 16 Master Uranium", lambda: reset_button(3e25, "Master Ion", 16, "Master Uranium")),
          ("1.10195Oc Master Ion: 34.26 Master Uranium", lambda: reset_button(1.10195e27, "Master Ion", 34.26, "Master Uranium")),
          ("14.37Oc Master Ion: 73.27 Master Uranium", lambda: reset_button(1.437e28, "Master Ion", 73.27, "Master Uranium")),
          ("402.88Oc Master Ion: 156.49 Master Uranium", lambda: reset_button(4.0288e29, "Master Ion", 156.49, "Master Uranium")),
          ("22.79No Master Ion: 333.81 Master Uranium", lambda: reset_button(2.279e31, "Master Ion", 333.81, "Master Uranium")),
      ],
      "Master Bismuth": [
          ("1T Master Uranium: 36 Master Bismuth", lambda: reset_button(1e12, "Master Uranium", 36, "Master Bismuth")),
          ("23.82T Master Uranium: 55.18 Master Bismuth", lambda: reset_button(2.382e13, "Master Uranium", 55.18, "Master Bismuth")),
          ("493.87T Master Uranium: 84.52 Master Bismuth", lambda: reset_button(4.9387e14, "Master Uranium", 84.52, "Master Bismuth")),
          ("15.93Qd Master Uranium: 129.34 Master Bismuth", lambda: reset_button(1.593e16, "Master Uranium", 129.34, "Master Bismuth")),
          ("869.75Qd Master Uranium: 197.75 Master Bismuth", lambda: reset_button(8.6975e17, "Master Uranium", 197.75, "Master Bismuth")),
      ],
      "Master Boracite": [
          ("800k Master Bismuth: 7.5 Master Boracite", lambda: reset_button(800000, "Master Bismuth", 7.5, "Master Boracite")),
          ("2.87M Master Bismuth: 15.87 Master Boracite", lambda: reset_button(2.87e6, "Master Bismuth", 15.87, "Master Boracite")),
          ("10.48M Master Bismuth: 33.55 Master Boracite", lambda: reset_button(1.048e7, "Master Bismuth", 33.55, "Master Boracite")),
          ("5.64B Master Bismuth: 70.83 Master Boracite", lambda: reset_button(5.64e9, "Master Bismuth", 70.83, "Master Boracite")),
          ("151.68B Master Bismuth: 100 Master Boracite", lambda: reset_button(1.5168e11, "Master Bismuth", 100, "Master Boracite")),
      ],
      "Master Nissonite": [
          ("275 Master Boracite: 2.7 Master Nissonite", lambda: reset_button(275, "Master Boracite", 2.7, "Master Nissonite")),
          ("611.1 Master Boracite: 4.84 Master Nissonite", lambda: reset_button(611.1, "Master Boracite", 4.84, "Master Nissonite")),
          ("1.35k Master Boracite: 8.69 Master Nissonite", lambda: reset_button(1350, "Master Boracite", 8.69, "Master Nissonite")),
          ("3.02k Master Boracite: 15.59 Master Nissonite", lambda: reset_button(3020, "Master Boracite", 15.59, "Master Nissonite")),
          ("6.7k Master Boracite: 27.9 Master Nissonite", lambda: reset_button(6700, "Master Boracite", 27.9, "Master Nissonite")),
      ],
      "Master Orpiment": [
          ("25 Master Nissonite: 1 Master Orpiment", lambda: reset_button(25, "Master Nissonite", 1, "Master Orpiment")),
          ("67 Master Nissonite: 1.81 Master Orpiment", lambda: reset_button(67, "Master Nissonite", 1.81, "Master Orpiment")),
          ("175 Master Nissonite: 3.29 Master Orpiment", lambda: reset_button(175, "Master Nissonite", 3.29, "Master Orpiment")),
          ("500 Master Nissonite: 5.96 Master Orpiment", lambda: reset_button(500, "Master Nissonite", 5.96, "Master Orpiment")),
      ],
      "Master Tetra": [
          ("32 Master Orpiment: 1 Master Tetra", lambda: reset_button(32, "Master Orpiment", 1, "Master Tetra")),
          ("80 Master Orpiment: 1.82 Master Tetra", lambda: reset_button(80, "Master Orpiment", 1.82, "Master Tetra")),
          ("275 Master Orpiment: 3.33 Master Tetra", lambda: reset_button(275, "Master Orpiment", 3.33, "Master Tetra")),
      ],
      "Master Volt": [
          ("30 Master Tetra: 2 Master Volt", lambda: reset_button(30, "Master Tetra", 2, "Master Volt")),
          ("96 Master Tetra: 6.57 Master Volt", lambda: reset_button(96, "Master Tetra", 6.57, "Master Volt")),
      ],
      "Recovery": [
          ("8k Master Mint: 12.5 Master Uranium (Sets)", lambda: recovery_button_set(8000, "Master Mint", 12.5, "Master Uranium")),
          ("30k Master Mint: 1k Master Diamond (Sets)", lambda: recovery_button_set(30000, "Master Mint", 1000, "Master Diamond")),
          ("1 Master Orpiment: 2.5 Master Ion (Fetch)", lambda: recovery_button_fetch(1, "Master Orpiment", 2.5, "Master Ion")),
          ("1 Master Tetra: 1/2 Master Bismuth (Fetch)", lambda: recovery_button_fetch(1, "Master Tetra", 0.5, "Master Bismuth")),
          ("1 Master Volt: 5 Master Nissonite (Sets)", lambda: recovery_button_set(1, "Master Volt", 5, "Master Nissonite")),
      ],
      "Area Teleports": [
          ("Limbo (req: 8 Master Uranium)", lambda: load_check("L")),
      ]
  }, 3, "Master Nissonite", "TLG", voltaic_radar=voltaic_radar)
  Realm(root, { #Forbidden Altar
      "The MASTERY": [
          ("5e(5.148e6) Master Cash: 100Sp Master Multiplier", lambda: cost_button("Master Cash", Mantissa(5,5.148e6), "Master Multiplier", 1e26)),
          ("1e(1.1921e6) Master Multiplier: 100Qn Master Rebirths", lambda: reset_button(Mantissa(1,1.1921e6), "Master Multiplier", 1e20, "Master Rebirths")),
          ("1e(1.1131e6) Master Rebirths: 100Sx Master Stone", lambda: reset_button(Mantissa(1,1.131e6), "Master Rebirths", 1e23, "Master Stone")),
          ("1e777500 Master Stone: 100T Master White Gems", lambda: reset_button(Mantissa(1,777500), "Master Stone", 1e14, "Master White Gems")),
          ("1e472000 Master White Gems: 1T Master Crystal", lambda: reset_button(Mantissa(1,472000), "Master White Gems", 1e12, "Master Crystal")),
          ("1e235400 Master Crystal: 100B Master Iron", lambda: reset_button(Mantissa(1,235400), "Master Crystal", 1e11, "Master Iron")),
          ("1e152800 Master Iron: 1B Master Gold", lambda: reset_button(Mantissa(1,152800), "Master Iron", 1e9, "Master Gold")),
          ("1e59590 Master Gold: 100M Master Quartz", lambda: reset_button(Mantissa(1,59590), "Master Gold", 1e8, "Master Quartz")),
          ("1e47150 Master Quartz: 10M Master Jade", lambda: reset_button(Mantissa(1,475150), "Master Quartz", 1e7, "Master Jade")),
          ("3e23200 Master Jade: 1M Master Obsidian", lambda: reset_button(Mantissa(3,23200), "Master Jade", 1e6, "Master Obsidian")),
          ("1e11600 Master Obsidian: 10B Master Ruby", lambda: reset_button(Mantissa(1,11600), "Master Obsidian", 1e10, "Master Ruby")),
          ("1e6400 Master Ruby: 100M Master Emerald", lambda: cost_button("Master Ruby", Mantissa(1,6400), "Master Emerald", 1e8)),
          ("1e3000 Master Emerald: 1M Master Sapphire", lambda: cost_button("Master Emerald", Mantissa(1,3000), "Master Sapphire", 1e6)),
          ("1e1400 Master Sapphire: 1T Master Diamond", lambda: reset_button(Mantissa(1,1400), "Master Sapphire", 1e12, "Master Diamond")),
          ("1e830 Master Diamond: 1e50 Master Starlight", lambda: reset_button(Mantissa(1,830), "Master Diamond", 1e50, "Master Starlight")),
          ("1e475 Master Starlight: 1No Master Ion", lambda: reset_button(Mantissa(1,475), "Master Starlight", 1e30, "Master Ion")),
          ("1e250 Master Ion: 10Oc Master Uranium", lambda: reset_button(1e250, "Master Ion", 1e28, "Master Uranium")),
          ("1e135 Master Uranium: 100No Master Bismuth", lambda: reset_button(1e135, "Master Uranium", 1e32, "Master Bismuth")),
          ("1e63 Master Bismuth: 100Sx Master Boracite", lambda: reset_button(1e63, "Master Bismuth", 1e23, "Master Boracite")),
          ("1e36 Master Boracite: 350 Master Nissonite", lambda: reset_button(1e36, "Master Boracite", 350, "Master Nissonite")),
          ("10Qd Master Nissonite: 20 Master Orpiment", lambda: reset_button(1e16, "Master Nissonite", 20, "Master Orpiment")),
          ("1T Master Orpiment: 16.5 Master Tetra", lambda: reset_button(1e12, "Master Orpiment", 16.5, "Master Tetra")),
          ("220k Master Tetra: 25 Master Volt", lambda: reset_button(220000, "Master Tetra", 25, "Master Volt")),
          ("340 Master Volt: 1 Master Aquamarine", lambda: reset_button(160, "Master Volt", 1, "Master Aquamarine")),
          ("14 Master Aquamarine: 1 Master Lollipop", lambda: reset_button(14, "Master Aquamarine", 1, "Master Lollipop")),
          ("6 Master Lollipop: 1 Prime Alpha Key", lambda: reset_button(6, "Master Lollipop", 1, "Prime Alpha Key"))
      ],
      "For your safety...": [
          ("1k Master Mint: 8 Master Uranium (Sets)", lambda: recovery_button_set(1000, "Master Mint", 8, "Master Uranium"))
      ],
      "Area Teleports": [
          ("Limbo (req: 8 Master Uranium)", lambda: load_check("L")),
      ]
  }, 57, "Master Volt", "FA", voltaic_radar=voltaic_radar)
  Realm(root, { #Mechanical Room
      "C0RR8PT10N": [
          ("10k Lollipop: 1 C0RR8PT10N", lambda: reset_button_special(10000, "Lollipop", 1, "C0RR8PT10N", ["Cash", "Multiplier", "Rebirth", "Stone", "White Gems", "Crystal", "Iron", "Gold", "Quartz", "Jade", "Obsidian", "Ruby", "Emerald", "Sapphire", "Diamond", "Starlight", "Ion", "Uranium", "Bismuth", "Boracite", "Nissonite", "Orpiment", "Tetra", "Volt", "Aquamarine", "Lollipop", "Master Cash", "Master Multiplier", "Master Rebirths", "Master Stone", "Master White Gems", "Master Crystal", "Master Iron", "Master Gold", "Master Quartz", "Master Jade", "Master Obsidian", "Master Ruby", "Master Emerald", "Master Sapphire", "Master Diamond", "Master Starlight", "Master Ion", "Master Uranium", "Master Bismuth", "Master Boracite", "Master Nissonite", "Master Orpiment", "Master Tetra", "Master Volt", "Master Aquamarine", "Master Lollipop"]))
      ],
      "Geodes": [
          ("Cosmic Geode: 100 C0RR8PT10N", lambda btn: Geode_roll(btn, cosmic_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check("S")),
         ("Recover Hall (req: 0 Cash)", lambda: load_check("RH")),
         ("ΔΨΩ (req: 5 C0RR8PT10N)", lambda: load_check("TLA"))
      ],
  }, 1, "Prime Alpha Key", "MR", voltaic_radar=voltaic_radar)
  Realm(root, { #TLA
      "Stargazed Metal": [
          ("20 C0RR8PT10N: 1 Stargazed Metal", lambda: reset_button_special(20, "C0RR8PT10N", 1, "Stargazed Metal", ["Cash", "Multiplier", "Rebirth", "Stone", "White Gems", "Crystal", "Iron", "Gold", "Quartz", "Jade", "Obsidian", "Ruby", "Emerald", "Sapphire", "Diamond", "Starlight", "Ion", "Uranium", "Bismuth", "Boracite", "Nissonite", "Orpiment", "Tetra", "Volt", "Aquamarine", "Lollipop", "Master Cash", "Master Multiplier", "Master Rebirths", "Master Stone", "Master White Gems", "Master Crystal", "Master Iron", "Master Gold", "Master Quartz", "Master Jade", "Master Obsidian", "Master Ruby", "Master Emerald", "Master Sapphire", "Master Diamond", "Master Starlight", "Master Ion", "Master Uranium", "Master Bismuth", "Master Boracite", "Master Nissonite", "Master Orpiment", "Master Tetra", "Master Volt", "Master Aquamarine", "Master Lollipop", "C0RR8PT10N"])),
          ("1k Master Lollipop: 1 Stargazed Metal", lambda: reset_button_special(1000, "Master Lollipop", 1, "Stargazed Metal", ["Cash", "Multiplier", "Rebirth", "Stone", "White Gems", "Crystal", "Iron", "Gold", "Quartz", "Jade", "Obsidian", "Ruby", "Emerald", "Sapphire", "Diamond", "Starlight", "Ion", "Uranium", "Bismuth", "Boracite", "Nissonite", "Orpiment", "Tetra", "Volt", "Aquamarine", "Lollipop", "Master Cash", "Master Multiplier", "Master Rebirths", "Master Stone", "Master White Gems", "Master Crystal", "Master Iron", "Master Gold", "Master Quartz", "Master Jade", "Master Obsidian", "Master Ruby", "Master Emerald", "Master Sapphire", "Master Diamond", "Master Starlight", "Master Ion", "Master Uranium", "Master Bismuth", "Master Boracite", "Master Nissonite", "Master Orpiment", "Master Tetra", "Master Volt", "Master Aquamarine", "Master Lollipop", "C0RR8PT10N"]))
      ],
      "Gyge": [
          ("17 Stargazed Metal: 1 Gyge", lambda: reset_button_special(17, "Stargazed Metal", 1, "Gyge", ["Cash", "Multiplier", "Rebirth", "Stone", "White Gems", "Crystal", "Iron", "Gold", "Quartz", "Jade", "Obsidian", "Ruby", "Emerald", "Sapphire", "Diamond", "Starlight", "Ion", "Uranium", "Bismuth", "Boracite", "Nissonite", "Orpiment", "Tetra", "Volt", "Aquamarine", "Lollipop", "Master Cash", "Master Multiplier", "Master Rebirths", "Master Stone", "Master White Gems", "Master Crystal", "Master Iron", "Master Gold", "Master Quartz", "Master Jade", "Master Obsidian", "Master Ruby", "Master Emerald", "Master Sapphire", "Master Diamond", "Master Starlight", "Master Ion", "Master Uranium", "Master Bismuth", "Master Boracite", "Master Nissonite", "Master Orpiment", "Master Tetra", "Master Volt", "Master Aquamarine", "Master Lollipop", "C0RR8PT10N", "Stargazed Metal"])),
          ("32 Stargazed Metal: 3 Gyge", lambda: reset_button_special(32, "Stargazed Metal", 3, "Gyge", ["Cash", "Multiplier", "Rebirth", "Stone", "White Gems", "Crystal", "Iron", "Gold", "Quartz", "Jade", "Obsidian", "Ruby", "Emerald", "Sapphire", "Diamond", "Starlight", "Ion", "Uranium", "Bismuth", "Boracite", "Nissonite", "Orpiment", "Tetra", "Volt", "Aquamarine", "Lollipop", "Master Cash", "Master Multiplier", "Master Rebirths", "Master Stone", "Master White Gems", "Master Crystal", "Master Iron", "Master Gold", "Master Quartz", "Master Jade", "Master Obsidian", "Master Ruby", "Master Emerald", "Master Sapphire", "Master Diamond", "Master Starlight", "Master Ion", "Master Uranium", "Master Bismuth", "Master Boracite", "Master Nissonite", "Master Orpiment", "Master Tetra", "Master Volt", "Master Aquamarine", "Master Lollipop", "C0RR8PT10N", "Stargazed Metal"])),
          ("64 Stargazed Metal: 6 Gyge", lambda: reset_button_special(64, "Stargazed Metal", 6, "Gyge", ["Cash", "Multiplier", "Rebirth", "Stone", "White Gems", "Crystal", "Iron", "Gold", "Quartz", "Jade", "Obsidian", "Ruby", "Emerald", "Sapphire", "Diamond", "Starlight", "Ion", "Uranium", "Bismuth", "Boracite", "Nissonite", "Orpiment", "Tetra", "Volt", "Aquamarine", "Lollipop", "Master Cash", "Master Multiplier", "Master Rebirths", "Master Stone", "Master White Gems", "Master Crystal", "Master Iron", "Master Gold", "Master Quartz", "Master Jade", "Master Obsidian", "Master Ruby", "Master Emerald", "Master Sapphire", "Master Diamond", "Master Starlight", "Master Ion", "Master Uranium", "Master Bismuth", "Master Boracite", "Master Nissonite", "Master Orpiment", "Master Tetra", "Master Volt", "Master Aquamarine", "Master Lollipop", "C0RR8PT10N", "Stargazed Metal"])),
          ("109 Stargazed Metal: 9 Gyge", lambda: reset_button_special(109, "Stargazed Metal", 9, "Gyge", ["Cash", "Multiplier", "Rebirth", "Stone", "White Gems", "Crystal", "Iron", "Gold", "Quartz", "Jade", "Obsidian", "Ruby", "Emerald", "Sapphire", "Diamond", "Starlight", "Ion", "Uranium", "Bismuth", "Boracite", "Nissonite", "Orpiment", "Tetra", "Volt", "Aquamarine", "Lollipop", "Master Cash", "Master Multiplier", "Master Rebirths", "Master Stone", "Master White Gems", "Master Crystal", "Master Iron", "Master Gold", "Master Quartz", "Master Jade", "Master Obsidian", "Master Ruby", "Master Emerald", "Master Sapphire", "Master Diamond", "Master Starlight", "Master Ion", "Master Uranium", "Master Bismuth", "Master Boracite", "Master Nissonite", "Master Orpiment", "Master Tetra", "Master Volt", "Master Aquamarine", "Master Lollipop", "C0RR8PT10N", "Stargazed Metal"])),
          ("211 Stargazed Metal: 15 Gyge", lambda: reset_button_special(211, "Stargazed Metal", 15, "Gyge", ["Cash", "Multiplier", "Rebirth", "Stone", "White Gems", "Crystal", "Iron", "Gold", "Quartz", "Jade", "Obsidian", "Ruby", "Emerald", "Sapphire", "Diamond", "Starlight", "Ion", "Uranium", "Bismuth", "Boracite", "Nissonite", "Orpiment", "Tetra", "Volt", "Aquamarine", "Lollipop", "Master Cash", "Master Multiplier", "Master Rebirths", "Master Stone", "Master White Gems", "Master Crystal", "Master Iron", "Master Gold", "Master Quartz", "Master Jade", "Master Obsidian", "Master Ruby", "Master Emerald", "Master Sapphire", "Master Diamond", "Master Starlight", "Master Ion", "Master Uranium", "Master Bismuth", "Master Boracite", "Master Nissonite", "Master Orpiment", "Master Tetra", "Master Volt", "Master Aquamarine", "Master Lollipop", "C0RR8PT10N", "Stargazed Metal"])),
          ("473 Stargazed Metal: 45 Gyge", lambda: reset_button_special(473, "Stargazed Metal", 45, "Gyge", ["Cash", "Multiplier", "Rebirth", "Stone", "White Gems", "Crystal", "Iron", "Gold", "Quartz", "Jade", "Obsidian", "Ruby", "Emerald", "Sapphire", "Diamond", "Starlight", "Ion", "Uranium", "Bismuth", "Boracite", "Nissonite", "Orpiment", "Tetra", "Volt", "Aquamarine", "Lollipop", "Master Cash", "Master Multiplier", "Master Rebirths", "Master Stone", "Master White Gems", "Master Crystal", "Master Iron", "Master Gold", "Master Quartz", "Master Jade", "Master Obsidian", "Master Ruby", "Master Emerald", "Master Sapphire", "Master Diamond", "Master Starlight", "Master Ion", "Master Uranium", "Master Bismuth", "Master Boracite", "Master Nissonite", "Master Orpiment", "Master Tetra", "Master Volt", "Master Aquamarine", "Master Lollipop", "C0RR8PT10N", "Stargazed Metal"])),
      ],
      "Auly Plate": [
          ("66 Gyge: 1 Auly Plate", lambda: reset_button_special(66, "Gyge", 1, "Auly Plate", ["Cash", "Multiplier", "Rebirth", "Stone", "White Gems", "Crystal", "Iron", "Gold", "Quartz", "Jade", "Obsidian", "Ruby", "Emerald", "Sapphire", "Diamond", "Starlight", "Ion", "Uranium", "Bismuth", "Boracite", "Nissonite", "Orpiment", "Tetra", "Volt", "Aquamarine", "Lollipop", "Master Cash", "Master Multiplier", "Master Rebirths", "Master Stone", "Master White Gems", "Master Crystal", "Master Iron", "Master Gold", "Master Quartz", "Master Jade", "Master Obsidian", "Master Ruby", "Master Emerald", "Master Sapphire", "Master Diamond", "Master Starlight", "Master Ion", "Master Uranium", "Master Bismuth", "Master Boracite", "Master Nissonite", "Master Orpiment", "Master Tetra", "Master Volt", "Master Aquamarine", "Master Lollipop", "C0RR8PT10N", "Stargazed Metal", "Gyge"])),
          ("273 Gyge: 2 Auly Plate", lambda: reset_button_special(273, "Gyge", 2, "Auly Plate", ["Cash", "Multiplier", "Rebirth", "Stone", "White Gems", "Crystal", "Iron", "Gold", "Quartz", "Jade", "Obsidian", "Ruby", "Emerald", "Sapphire", "Diamond", "Starlight", "Ion", "Uranium", "Bismuth", "Boracite", "Nissonite", "Orpiment", "Tetra", "Volt", "Aquamarine", "Lollipop", "Master Cash", "Master Multiplier", "Master Rebirths", "Master Stone", "Master White Gems", "Master Crystal", "Master Iron", "Master Gold", "Master Quartz", "Master Jade", "Master Obsidian", "Master Ruby", "Master Emerald", "Master Sapphire", "Master Diamond", "Master Starlight", "Master Ion", "Master Uranium", "Master Bismuth", "Master Boracite", "Master Nissonite", "Master Orpiment", "Master Tetra", "Master Volt", "Master Aquamarine", "Master Lollipop", "C0RR8PT10N", "Stargazed Metal", "Gyge"])),
          ("621 Gyge: 4 Auly Plate", lambda: reset_button_special(621, "Gyge", 4, "Auly Plate", ["Cash", "Multiplier", "Rebirth", "Stone", "White Gems", "Crystal", "Iron", "Gold", "Quartz", "Jade", "Obsidian", "Ruby", "Emerald", "Sapphire", "Diamond", "Starlight", "Ion", "Uranium", "Bismuth", "Boracite", "Nissonite", "Orpiment", "Tetra", "Volt", "Aquamarine", "Lollipop", "Master Cash", "Master Multiplier", "Master Rebirths", "Master Stone", "Master White Gems", "Master Crystal", "Master Iron", "Master Gold", "Master Quartz", "Master Jade", "Master Obsidian", "Master Ruby", "Master Emerald", "Master Sapphire", "Master Diamond", "Master Starlight", "Master Ion", "Master Uranium", "Master Bismuth", "Master Boracite", "Master Nissonite", "Master Orpiment", "Master Tetra", "Master Volt", "Master Aquamarine", "Master Lollipop", "C0RR8PT10N", "Stargazed Metal", "Gyge"])),
          ("1.12k Gyge: 9 Auly Plate", lambda: reset_button_special(1120, "Gyge", 9, "Auly Plate", ["Cash", "Multiplier", "Rebirth", "Stone", "White Gems", "Crystal", "Iron", "Gold", "Quartz", "Jade", "Obsidian", "Ruby", "Emerald", "Sapphire", "Diamond", "Starlight", "Ion", "Uranium", "Bismuth", "Boracite", "Nissonite", "Orpiment", "Tetra", "Volt", "Aquamarine", "Lollipop", "Master Cash", "Master Multiplier", "Master Rebirths", "Master Stone", "Master White Gems", "Master Crystal", "Master Iron", "Master Gold", "Master Quartz", "Master Jade", "Master Obsidian", "Master Ruby", "Master Emerald", "Master Sapphire", "Master Diamond", "Master Starlight", "Master Ion", "Master Uranium", "Master Bismuth", "Master Boracite", "Master Nissonite", "Master Orpiment", "Master Tetra", "Master Volt", "Master Aquamarine", "Master Lollipop", "C0RR8PT10N", "Stargazed Metal", "Gyge"])),
          ("2.39k Gyge: 20 Auly Plate", lambda: reset_button_special(2390, "Gyge", 20, "Auly Plate", ["Cash", "Multiplier", "Rebirth", "Stone", "White Gems", "Crystal", "Iron", "Gold", "Quartz", "Jade", "Obsidian", "Ruby", "Emerald", "Sapphire", "Diamond", "Starlight", "Ion", "Uranium", "Bismuth", "Boracite", "Nissonite", "Orpiment", "Tetra", "Volt", "Aquamarine", "Lollipop", "Master Cash", "Master Multiplier", "Master Rebirths", "Master Stone", "Master White Gems", "Master Crystal", "Master Iron", "Master Gold", "Master Quartz", "Master Jade", "Master Obsidian", "Master Ruby", "Master Emerald", "Master Sapphire", "Master Diamond", "Master Starlight", "Master Ion", "Master Uranium", "Master Bismuth", "Master Boracite", "Master Nissonite", "Master Orpiment", "Master Tetra", "Master Volt", "Master Aquamarine", "Master Lollipop", "C0RR8PT10N", "Stargazed Metal", "Gyge"])),
      ],
      "Shell Piece": [
          ("100 Auly Plate: 1 Shell Piece", lambda: reset_button_special(100, "Auly Plate", 1, "Shell Piece", ["Cash", "Multiplier", "Rebirth", "Stone", "White Gems", "Crystal", "Iron", "Gold", "Quartz", "Jade", "Obsidian", "Ruby", "Emerald", "Sapphire", "Diamond", "Starlight", "Ion", "Uranium", "Bismuth", "Boracite", "Nissonite", "Orpiment", "Tetra", "Volt", "Aquamarine", "Lollipop", "Master Cash", "Master Multiplier", "Master Rebirths", "Master Stone", "Master White Gems", "Master Crystal", "Master Iron", "Master Gold", "Master Quartz", "Master Jade", "Master Obsidian", "Master Ruby", "Master Emerald", "Master Sapphire", "Master Diamond", "Master Starlight", "Master Ion", "Master Uranium", "Master Bismuth", "Master Boracite", "Master Nissonite", "Master Orpiment", "Master Tetra", "Master Volt", "Master Aquamarine", "Master Lollipop", "C0RR8PT10N", "Stargazed Metal", "Gyge", "Auly Plate"]))
      ],
      "Recovery": [
          ("3 Starglass: 1 Stargazed Metal (Sets)", lambda: recovery_button_set(3, "Starglass", 1, "Stargazed Metal"))
      ],
      "Area Teleports": [
          ("Buttonia (req: 0 Cash)", lambda: load_check("S"))
      ]
  }, 5, "C0RR8PT10N", "TLA", voltaic_radar=voltaic_radar)
  Realm(root, { #Afterlife Domain
      "Enchantment": [
          ("80 Mana: 1 Enchantment", lambda: reset_button(80, "Mana", 1, "Enchantment")),
          ("500k Mana: 7 Enchantment", lambda: reset_button(500000, "Mana", 7, "Enchantment")),
          ("15B Mana: 20 Enchantment", lambda: reset_button(1.5e10, "Mana", 20, "Enchantment")),
          ("100Qd Mana: 100 Enchantment", lambda: reset_button(1e17, "Mana", 100, "Enchantment")),
          ("25De Mana: 500 Enchantment", lambda: reset_button(500, "Mana", 2.5e34, "Enchantment")),
          ("5e36 Mana: 1M Enchantment", lambda: reset_button(5e36, "Mana", 1e6, "Enchantment"))
      ],
      "Spell": [
          ("3.5k Enchantment: 1 Spell", lambda: reset_button(3500, "Enchantment", 1, "Spell")),
          ("75Qn Enchantment: 5 Spell", lambda: reset_button(7.5e19, "Enchantment", 5, "Spell")),
          ("111No Enchantment: 30 Spell", lambda: reset_button(1.11e32, "Enchantment", 30, "Spell")),
      ],
      "Geodes": [
          ("Galactic Geode: 1M Mana", lambda btn: Geode_roll(btn, galactic_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Artificial Geode: 70B Enchantment", lambda btn: Geode_roll(btn, artificial_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Elemental Geode: 200De Mana", lambda btn: Geode_roll(btn, elemental_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Awakened Geode: 7e39 Enchantment", lambda btn: Geode_roll(btn, awakened_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Magical Geode: 5Sx Spell", lambda btn: Geode_roll(btn, magical_geode, luck, (1-(upgrades[world]["geode_speed"]["effect"]*upgrades[world]["geode_speed"]["current_lvl"])), bulk_roll))
      ],
      "Gems": [
          ("1 Planetium: 5M Gems", lambda: reset_button(1, "Planetium", 5e6, "Gems")),
          ("1 Mercury: 12M Gems", lambda: reset_button(1, "Mercury", 1.2e7, "Gems")),
          ("1 Livermorium: 1B Gems", lambda: reset_button(1, "Livermorium", 1e9, "Gems")),
          ("1 Rockarnium: 3T Gems", lambda: reset_button(1, "Rockarnium", 3e12, "Gems")),
          ("1 Scandium: 5Qd Gems", lambda: reset_button(1, "Scandium", 5e15, "Gems")),
          ("1 Rhodimite: 27Qd Gems", lambda: reset_button(1, "Planetium", 2.7e16, "Gems")),
          ("1 Beryllium: 5Qn Gems", lambda: reset_button(1, "Beryllium", 5e18, "Gems")),
      ],
      "World Teleports": [
          ("Buttonia (req: 0 Mana)", lambda: load_world(0, "Mana", Buttonia))
      ]
  }, 0, "Mana", "AD", voltaic_radar=voltaic_radar)
  Realm(root, { #Wormhole's Breech
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check("S")),
      ],
      "???": [
          ("Puzzle 1", lambda: image_load("Galaxite/Galaxite1.png")),
          ("Puzzle 2", lambda: image_load("Galaxite/Galaxite2.png")),
          ("Puzzle 3", lambda: image_load("Galaxite/Galaxite3.png"))
      ]
  }, [1,1], ["Stellarite", "Starglass"], "WF", voltaic_radar=voltaic_radar)
  Realm(root, { #Purified Illusions
      "???": [
          ("Are you patient enough to overcome 7 billion thoughts? (req: 1 Starglass)", lambda: sloth(root, 300, (1, "Starglass"))),
          ("Bolical World (req: 1 Starglass)", lambda: graphite_puzzle(root, (1, "Starglass"))),
          ("Stellarite Location (req: 1 Starglass)", lambda: load_check("ETSL")),
          ("Wormhole's Breech (req: 1 Starglass)", lambda: load_check("WF"))
      ],
      "Recovery": [
          ("1 Gyge: 1 Starglass (Sets)", lambda: recovery_button_set(1, "Gyge", 1, "Starglass")),
          ("1 Shell Piece: 1 Singularity (Sets)", lambda: recovery_button_set(1, "Shell Piece", 1, "Singularity"))
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check("S")),
         ("Recover Hall (req: 0 Cash)", lambda: load_check("RH"))
      ]
  }, [1,1], ["Starglass", "Shell Piece"], "PI", voltaic_radar=voltaic_radar)
  Realm(root, { #Moonbase Spawn
      "Booster": [
          ("35 Moon Cash: 1 Booster", lambda: cost_button("Moon Cash", 35, "Booster", 1)),
          ("385 Moon Cash: 2 Booster", lambda: cost_button("Moon Cash", 385, "Booster", 2)),
          ("2.69k Moon Cash: 5 Booster", lambda: cost_button("Moon Cash", 2690, "Booster", 5)),
          ("18.86k Moon Cash: 13 Booster", lambda: cost_button("Moon Cash", 18860, "Booster", 13)),
          ("94.32k Moon Cash: 34 Booster", lambda: cost_button("Moon Cash", 94320, "Booster", 34)),
          ("660.27k Moon Cash: 86 Booster", lambda: cost_button("Moon Cash", 660270, "Booster", 86)),
          ("5.28M Moon Cash: 213 Booster", lambda: cost_button("Moon Cash", 5.28e6, "Booster", 213)),
          ("15.84M Moon Cash: 514 Booster", lambda: cost_button("Moon Cash", 1.584e7, "Booster", 514)),
          ("95.07M Moon Cash: 1.21k Booster", lambda: cost_button("Moon Cash", 9.507e7, "Booster", 1210)),
          ("285.23M Moon Cash: 2.79k Booster", lambda: cost_button("Moon Cash", 2.8523e8, "Booster", 2790)),
          ("2.85B Moon Cash: 6.32k Booster", lambda: cost_button("Moon Cash", 2.85e9, "Booster", 6320)),
          ("31.37B Moon Cash: 14k Booster", lambda: cost_button("Moon Cash", 3.137e10, "Booster", 14000)),
          ("313.75B Moon Cash: 30.41k Booster", lambda: cost_button("Moon Cash", 3.1375e11, "Booster", 30410)),
          ("2.19T Moon Cash: 64.88k Booster", lambda: cost_button("Moon Cash", 2.19e12, "Booster", 64880)),
          ("17.57T Moon Cash: 136.04k Booster", lambda: cost_button("Moon Cash", 1.757e13, "Booster", 136040)),
      ],
      "Reincarnation": [
           ("30.41k Booster: 1 Reincarnation", lambda: reset_button(30410, "Booster", 1, "Reincarnation")),
           ("212.89k Booster: 2 Reincarnation", lambda: reset_button(212890, "Booster", 2, "Reincarnation")),
           ("3.19M Booster: 4 Reincarnation", lambda: reset_button(3.19e6, "Booster", 4, "Reincarnation")),
           ("28.74M Booster: 8 Reincarnation", lambda: reset_button(2.874e7, "Booster", 8, "Reincarnation")),
           ("172.44M Booster: 16 Reincarnation", lambda: reset_button(1.7244e8, "Booster", 16, "Reincarnation")),
           ("2.75B Booster: 33 Reincarnation", lambda: reset_button(2.75e9, "Booster", 33, "Reincarnation")),
           ("35.68B Booster: 68 Reincarnation", lambda: reset_button(3.568e10, "Booster", 68, "Reincarnation")),
           ("251.07B Booster: 138 Reincarnation", lambda: reset_button(2.5107e11, "Booster", 138, "Reincarnation")),
           ("3.51T Booster: 278 Reincarnation", lambda: reset_button(3.51e12, "Booster", 278, "Reincarnation")),
      ],
      "Scoria": [
          ("600 Reincarnation: 1 Scoria", lambda: reset_button(600, "Reincarnation", 1, "Scoria")),
          ("5.4k Reincarnation: 2 Scoria", lambda: reset_button(5400, "Reincarnation", 2, "Scoria")),
          ("32.39k Reincarnation: 4 Scoria", lambda: reset_button(32390, "Reincarnation", 4, "Scoria")),
          ("712.8k Reincarnation: 8 Scoria", lambda: reset_button(712800, "Reincarnation", 8, "Scoria")),
          ("7.84M Reincarnation: 15 Scoria", lambda: reset_button(7.84e6, "Reincarnation", 15, "Scoria")),
          ("164.65M Reincarnation: 29 Scoria", lambda: reset_button(1.6465e8, "Reincarnation", 29, "Scoria")),
      ],
      "World Badges": [
           ("100Qn Booster: Outerspace Inflation", lambda: world_badge("Booster 1", "Moonbase")),
           ("200 Reincarnation: Better Afterlife", lambda: world_badge("Reincarnation 1", "Moonbase")),
           ("50k Reincarnation: Better Afterlife II", lambda: world_badge("Reincarnation 2", "Moonbase")),
           ("1M Reincarnation: Better Afterlife III", lambda: world_badge("Reincarnation 3", "Moonbase")),
           ("400M Reincarnation: Small Sacrifice", lambda: world_badge("Reincarnation 4", "Moonbase")),
           ("7 Scoria: Excavation Zone Expansion", lambda: world_badge("Scoria 1", "Moonbase")),
           ("45 Scoria: Nuclear Infection", lambda: world_badge("Scoria 2", "Moonbase")),
           ("300 Scoria: Even Bigger Mines", lambda: world_badge("Scoria 3", "Moonbase")),
           ("2.49k Scoria: Scoria Statue", lambda: world_badge("Scoria 4", "Moonbase")),
      ],
      "Area Teleports": [
          ("Bright Cove (req: 70 Scoria)", lambda: load_check("BC")),
          ("Liquified Outpost (req: 50 Brighterium)", lambda: load_check("LO")),
          ("Enigmatic Caverns (req: 100 Baryte)", lambda: load_check("EC")),
          ("Saturn (req: 50 Gypsum)", lambda: load_check("Sat")),
          ("Cryogenesis (req: 1.75k Pyrite)", lambda: load_check("C")),
          ("Prismed Islopolis (req: 600 Cryon)", lambda: load_check("PrI")),
      ],
      "World Teleports": [
          ("Buttonia (req: 0 Moon Cash)", lambda: load_world(0, "Moon Cash", Buttonia))
      ]
  }, 0, "Moon Cash", "S(M)", voltaic_radar=voltaic_radar)
  Realm(root, { #Bright Cove
      "Booster": [
          ("1De Moon Cash: 1M Booster", lambda: cost_button("Moon Cash", 1e33, "Booster", 1e6)),
          ("39De Moon Cash: 2.18M Booster", lambda: cost_button("Moon Cash", 3.9e34, "Booster", 2.18e6)),
          ("936De Moon Cash: 4.72M Booster", lambda: cost_button("Moon Cash", 9.36e35, "Booster", 4.72e6)),
          ("3.931e37 Moon Cash: 10.15M Booster", lambda: cost_button("Moon Cash", 3.931e37, "Booster", 1.015e7)),
          ("1.57e39 Moon Cash: 21.69M Booster", lambda: cost_button("Moon Cash", 1.57e39, "Booster", 2.169e7)),
          ("1.572e40 Moon Cash: 46.03M Booster", lambda: cost_button("Moon Cash", 1.572e40, "Booster", 4.603e7)),
          ("5.3463e41 Moon Cash: 97.02M Booster", lambda: cost_button("Moon Cash", 5.3463e41, "Booster", 9.702e7)),
          ("2.298e43 Moon Cash: 203.19M Booster", lambda: cost_button("Moon Cash", 2.298e43, "Booster", 2.0319e8)),
          ("3.2185e44 Moon Cash: 422.84M Booster", lambda: cost_button("Moon Cash", 3.2185e44, "Booster", 4.2284e8)),
          ("5.79e45 Moon Cash: 874.49M Booster", lambda: cost_button("Moon Cash", 5.79e45, "Booster", 8.7449e8)),
      ],
      "Reincarnation": [
          ("1Qd Booster: 700 Reincarnation", lambda: reset_button(1e15, "Booster", 700, "Reincarnation")),
          ("9Qd Booster: 1.44k Reincarnation", lambda: reset_button(9e15, "Booster", 1440, "Reincarnation")),
          ("387Qd Booster: 2.97k Reincarnation", lambda: reset_button(3.87e17, "Booster", 2970, "Reincarnation")),
          ("15.86Qn Booster: 6.08k Reincarnation", lambda: reset_button(1.586e19, "Booster", 6080, "Reincarnation")),
          ("222.13Qn Booster: 12.36k Reincarnation", lambda: reset_button(2.2213e20, "Booster", 12360, "Reincarnation")),
          ("6.21Sx Booster: 25k Reincarnation", lambda: reset_button(6.21e21, "Booster", 25000, "Reincarnation")),
          ("130.61Sx Booster: 50.25k Reincarnation", lambda: reset_button(1.3061e23, "Booster", 50250, "Reincarnation")),
          ("2.48Sp Booster: 100.51k Reincarnation", lambda: reset_button(2.48e24, "Booster", 100510, "Reincarnation")),
          ("94.3Sp Booster: 199.97k Reincarnation", lambda: reset_button(9.3e25, "Booster", 199970, "Reincarnation")),
      ],
      "Scoria": [
          ("100B Reincarnation: 48 Scoria", lambda: reset_button(1e11, "Reincarnation", 48, "Scoria")),
          ("4.5T Reincarnation: 96 Scoria", lambda: reset_button(4.5e12, "Reincarnation", 96, "Scoria")),
          ("54T Reincarnation: 192 Scoria", lambda: reset_button(5.4e13, "Reincarnation", 192, "Scoria")),
          ("1.56Qd Reincarnation: 382 Scoria", lambda: reset_button(1.56e15, "Reincarnation", 382, "Scoria")),
          ("26.62Qd Reincarnation: 757 Scoria", lambda: reset_button(2.662e16, "Reincarnation", 757, "Scoria")),
          ("425.94Qd Reincarnation: 1.5k Scoria", lambda: reset_button(4.2594e17, "Reincarnation", 1500, "Scoria")),
          ("12.35Qn Reincarnation: 2.93k Scoria", lambda: reset_button(1.235e19, "Reincarnation", 2930, "Scoria")),
      ],
      "Brighterium": [
          ("30k Scoria: 1 Brighterium", lambda: reset_button(30000, "Scoria", 1, "Brighterium")),
          ("1.2M Scoria: 2 Brighterium", lambda: reset_button(1.2e6, "Scoria", 2, "Brighterium")),
          ("48M Scoria: 5 Brighterium", lambda: reset_button(4.8e7, "Scoria", 5, "Brighterium")),
          ("720M Scoria: 14 Brighterium", lambda: reset_button(7.2e8, "Scoria", 14, "Brighterium")),
          ("17.28B Scoria: 40 Brighterium", lambda: reset_button(1.728e10, "Scoria", 40, "Brighterium")),
      ],
      "World Badges": [
          ("300B Reincarnation: Life Totem Lv.1", lambda: world_badge("Reincarnation 5", "Moonbase")),
          ("1Qd Reincarnation: Soul Stealer", lambda: world_badge("Reincarnation 6", "Moonbase")),
          ("1B Scoria: Scoria Totem Lv.1", lambda: world_badge("Scoria 5", "Moonbase")),
          ("5 Brighterium: Radiant Manners", lambda: world_badge("Brighterium 1", "Moonbase")),
          ("20 Brighterium: Optic Erosion", lambda: world_badge("Brighterium 2", "Moonbase")),
      ],
      "Area Teleports": [
          ("Spawn (req: 0 Moon Cash)", lambda: load_check("S(M)")),
      ]
  }, 70, "Scoria", "BC", voltaic_radar=voltaic_radar)
  Realm(root, { #Liquified Outpost
      "Booster": [
          ("1e55 Moon Cash: 10B Booster", lambda: cost_button("Moon Cash", 1e55, "Booster", 1e10)),
          ("1.7e56 Moon Cash: 22.93B Booster", lambda: cost_button("Moon Cash", 1.7e56, "Booster", 2.293e10)),
          ("5.43e57 Moon Cash: 52.33B Booster", lambda: cost_button("Moon Cash", 5.43e57, "Booster", 5.233e10)),
          ("2.2303e59 Moon Cash: 118.81B Booster", lambda: cost_button("Moon Cash", 2.2303e59, "Booster", 1.1881e11)),
          ("3.56e60 Moon Cash: 268.39B Booster", lambda: cost_button("Moon Cash", 3.56e60, "Booster", 2.6839e11)),
          ("1.1776e62 Moon Cash: 603.28B Booster", lambda: cost_button("Moon Cash", 1.1776e62, "Booster", 6.0328e11)),
          ("1.41e63 Moon Cash: 1.34T Booster", lambda: cost_button("Moon Cash", 1.41e63, "Booster", 1.34e12)),
          ("5.652e64 Moon Cash: 3T Booster", lambda: cost_button("Moon Cash", 5.652e64, "Booster", 3e12)),
          ("1.18e66 Moon Cash: 6.65T Booster", lambda: cost_button("Moon Cash", 1.18e66, "Booster", 6.65e12)),
          ("1.187e67 Moon Cash: 14.67T Booster", lambda: cost_button("Moon Cash", 1.187e67, "Booster", 1.467e13)),
          ("4.9855e68 Moon Cash: 32.21T Booster", lambda: cost_button("Moon Cash", 4.9855e68, "Booster", 3.221e13)),
          ("6.97e69 Moon Cash: 70.37T Booster", lambda: cost_button("Moon Cash", 6.97e69, "Booster", 7.037e13)),
          ("2.7221e71 Moon Cash: 153.07T Booster", lambda: cost_button("Moon Cash", 2.7221e71, "Booster", 1.5307e14)),
          ("6.8e72 Moon Cash: 331.45T Booster", lambda: cost_button("Moon Cash", 6.8e72, "Booster", 3.3145e14)),
          ("2.5859e74 Moon Cash: 714.52T Booster", lambda: cost_button("Moon Cash", 2.5859e74, "Booster", 7.1452e14)),
          ("3.62e75 Moon Cash: 1.53Qd Booster", lambda: cost_button("Moon Cash", 3.62e75, "Booster", 1.53e15)),
      ],
      "Reincarnation": [
          ("10De Booster: 10M Reincarnation", lambda: reset_button(1e34, "Booster", 1e7, "Reincarnation")),
          ("270De Booster: 17.81M Reincarnation", lambda: reset_button(2.7e35, "Booster", 1.781e7, "Reincarnation")),
          ("4.32e36 Booster: 31.62M Reincarnation", lambda: reset_button(4.32e36, "Booster", 3.162e7, "Reincarnation")),
          ("2.1167e38 Booster: 55.94M Reincarnation", lambda: reset_button(2.1167e38, "Booster", 5.594e7, "Reincarnation")),
          ("1.164e40 Booster: 98.64M Reincarnation", lambda: reset_button(1.164e40, "Booster", 9.864e7, "Reincarnation")),
          ("1.5134e41 Booster: 173.38M Reincarnation", lambda: reset_button(1.5134e41, "Booster", 1.7338e8, "Reincarnation")),
          ("3.63e42 Booster: 303.74M Reincarnation", lambda: reset_button(3.63e42, "Booster", 3.0374e8, "Reincarnation")),
          ("1.9978e44 Booster: 530.42M Reincarnation", lambda: reset_button(1.9978e44, "Booster", 5.3042e8, "Reincarnation")),
          ("2.59e45 Booster: 923.32M Reincarnation", lambda: reset_button(2.59e45, "Booster", 9.2332e8, "Reincarnation")),
          ("5.194e46 Booster: 1.6B Reincarnation", lambda: reset_button(5.194e46, "Booster", 1.6e9, "Reincarnation")),
          ("2.23e48 Booster: 2.77B Reincarnation", lambda: reset_button(2.23e48, "Booster", 2.77e9, "Reincarnation")),
          ("2.68e49 Booster: 4.78B Reincarnation", lambda: reset_button(2.68e49, "Booster", 4.78e9, "Reincarnation")),
          ("1.39e51 Booster: 8.21B Reincarnation", lambda: reset_button(1.39e51, "Booster", 8.21e9, "Reincarnation")),
          ("2.926e52 Booster: 14.09B Reincarnation", lambda: reset_button(2.926e52, "Booster", 1.409e10, "Reincarnation")),
          ("1.6e54 Booster: 24.08B Reincarnation", lambda: reset_button(1.6e54, "Booster", 2.408e10, "Reincarnation")),
          ("5.151e55 Booster: 41.04B Reincarnation", lambda: reset_button(5.151e55, "Booster", 4.104e10, "Reincarnation")),
          ("9.7872e56 Booster: 69.74B Reincarnation", lambda: reset_button(9.7872e56, "Booster", 6.974e10, "Reincarnation")),
      ],
      "Scoria": [
          ("10Sx Reincarnation: 10k Scoria", lambda: reset_button(1e22, "Reincarnation", 10000, "Scoria")),
          ("90Sx Reincarnation: 15.58k Scoria", lambda: reset_button(9e22, "Reincarnation", 15580, "Scoria")),
          ("2.51Sp Reincarnation: 24.21k Scoria", lambda: reset_button(2.51e24, "Reincarnation", 24210, "Scoria")),
          ("30.23Sp Reincarnation: 37.54k Scoria", lambda: reset_button(3.023e25, "Reincarnation", 37540, "Scoria")),
          ("725.75Sp Reincarnation: 58.03k Scoria", lambda: reset_button(7.2575e26, "Reincarnation", 58030, "Scoria")),
          ("10.16Oc Reincarnation: 89.49k Scoria", lambda: reset_button(1.016e28, "Reincarnation", 89490, "Scoria")),
          ("91.44Oc Reincarnation: 137.64k Scoria", lambda: reset_button(9.144e28, "Reincarnation", 137640, "Scoria")),
          ("3.1No Reincarnation: 211.152k Scoria", lambda: reset_button(3.1e30, "Reincarnation", 211152, "Scoria")),
          ("105.7No Reincarnation: 323.12k Scoria", lambda: reset_button(1.057e32, "Reincarnation", 323120, "Scoria")),
      ],
      "Brighterium": [
          ("1T Scoria: 100 Brighterium", lambda: reset_button(1e12, "Scoria", 100, "Brighterium")),
          ("6T Scoria: 227 Brighterium", lambda: reset_button(6e12, "Scoria", 227, "Brighterium")),
          ("42T Scoria: 514 Brighterium", lambda: reset_button(4.2e13, "Scoria", 514, "Brighterium")),
          ("336T Scoria: 1.15k Brighterium", lambda: reset_button(3.36e14, "Scoria", 1150, "Brighterium")),
      ],
      "Baryte": [
          ("2k Brighterium: 1 Baryte", lambda: reset_button(2000, "Brighterium", 1, "Baryte")),
          ("66k Brighterium: 6 Baryte", lambda: reset_button(66000, "Brighterium", 6, "Baryte")),
      ],
      "World Badges": [
          ("1e42 Booster: Primary Route Fluctuation", lambda: world_badge("Booster 2", "Moonbase")),
          ("1e51 Booster: Planetary Inflation", lambda: world_badge("Booster 3", "Moonbase")),
          ("3B Scoria: Poisonous Talisman", lambda: world_badge("Scoria 6", "Moonbase")),
          ("1Qd Scoria: Erosive Shell", lambda: world_badge("Scoria 7", "Moonbase")),
          ("260 Brighterium: Visual Bliss", lambda: world_badge("Brighterium 3", "Moonbase")),
          ("6k Brighterium: Solar Array", lambda: world_badge("Brighterium 4", "Moonbase")),
          ("1 Baryte: Resin Gel", lambda: world_badge("Baryte 1", "Moonbase")),
          ("17 Baryte: Waterfowl Shards", lambda: world_badge("Baryte 2", "Moonbase")),
      ],
      "Area Teleports": [
          ("Spawn (req: 0 Moon Cash)", lambda: load_check("S(M)")),
      ]
  }, 50, "Brighterium", "LO", voltaic_radar=voltaic_radar)
  Realm(root, { #Enigmatic Caverns
      "Booster": [
          ("6.999e100 Moon Cash: 100Qd Booster", lambda: cost_button("Moon Cash", 6.999e100, "Booster", 1e17)),
          ("2.86e102 Moon Cash: 181.72Qd Booster", lambda: cost_button("Moon Cash", 2.86e102, "Booster", 1.8172e17)),
          ("2.2959e104 Moon Cash: 329.42Qd Booster", lambda: cost_button("Moon Cash", 2.2959e104, "Booster", 3.2942e17)),
          ("1.721e106 Moon Cash: 595.77Qd Booster", lambda: cost_button("Moon Cash", 1.721e106, "Booster", 5.9577e17)),
          ("6.7157e107 Moon Cash: 1.07Qn Booster", lambda: cost_button("Moon Cash", 6.7157e107, "Booster", 1.07e18)),
          ("1.813e109 Moon Cash: 1.93Qn Booster", lambda: cost_button("Moon Cash", 1.813e109, "Booster", 1.93e18)),
          ("5.2584e110 Moon Cash: 3.47Qn Booster", lambda: cost_button("Moon Cash", 5.2584e110, "Booster", 3.47e18)),
          ("2.313e112 Moon Cash: 6.22Qn Booster", lambda: cost_button("Moon Cash", 2.313e112, "Booster", 6.22e18)),
          ("9.7175e113 Moon Cash: 11.12Qn Booster", lambda: cost_button("Moon Cash", 9.7175e113, "Booster", 1.112e19)),
       ],
      "Reincarnation": [
          ("6.9999e80 Booster: 1T Reincarnation", lambda: reset_button(6.9999e80, "Booster", 1e12, "Reincarnation")),
          ("3.849e82 Booster: 1.74T Reincarnation", lambda: reset_button(3.849e82, "Booster", 1.74e12, "Reincarnation")),
          ("2.84e84 Booster: 3.04T Reincarnation", lambda: reset_button(2.84e84, "Booster", 3.04e12, "Reincarnation")),
          ("1.1395e86 Booster: 5.29T Reincarnation", lambda: reset_button(1.1395e86, "Booster", 5.29e12, "Reincarnation")),
          ("6.6e87 Booster: 9.19T Reincarnation", lambda: reset_button(6.6e87, "Booster", 9.19e12, "Reincarnation")),
          ("2.1811e89 Booster: 15.93T Reincarnation", lambda: reset_button(2.1811e89, "Booster", 1.593e13, "Reincarnation")),
          ("1.352e91 Booster: 27.53T Reincarnation", lambda: reset_button(1.352e91, "Booster", 2.753e13, "Reincarnation")),
          ("3.9217e92 Booster: 47.48T Reincarnation", lambda: reset_button(3.9217e92, "Booster", 4.748e13, "Reincarnation")),
          ("1.921e94 Booster: 81.7T Reincarnation", lambda: reset_button(1.921e94, "Booster", 8.17e13, "Reincarnation")),
          ("1.22e96 Booster: 140.3T Reincarnation", lambda: reset_button(1.22e96, "Booster", 1.403e14, "Reincarnation")),
          ("7.01e97 Booster: 240.3T Reincarnation", lambda: reset_button(7.01e97, "Booster", 2.403e14, "Reincarnation")),
          ("1.68e99 Booster: 411.1T Reincarnation", lambda: reset_button(1.68e99, "Booster", 4.111e14, "Reincarnation")),
       ],
      "Scoria": [
          ("7e44 Reincarnation: 1M Scoria", lambda: reset_button(7e44, "Reincarnation", 1e6, "Scoria")),
          ("3.779e46 Reincarnation: 1.7M Scoria", lambda: reset_button(3.779e46, "Reincarnation", 1.7e6, "Scoria")),
          ("4.89e51 Reincarnation: 8.3M Scoria", lambda: reset_button(4.89e51, "Reincarnation", 8.3e6, "Scoria")),
          ("3.7231e53 Reincarnation: 14.03M Scoria", lambda: reset_button(3.7231e53, "Reincarnation", 1.403e7, "Scoria")),
          ("2.159e55 Reincarnation: 23.66M Scoria", lambda: reset_button(2.159e55, "Reincarnation", 2.366e7, "Scoria")),
          ("1.36e57 Reincarnation: 39.82M Scoria", lambda: reset_button(1.36e57, "Reincarnation", 3.982e7, "Scoria")),
          ("8.026e58 Reincarnation: 66.87M Scoria", lambda: reset_button(8.026e58, "Reincarnation", 6.687e7, "Scoria")),
          ("2.72e60 Reincarnation: 112.09M Scoria", lambda: reset_button(2.72e60, "Reincarnation", 1.1209e8, "Scoria")),
       ],
      "Brighterium": [
          ("700Qd Scoria: 10K Brighterium", lambda: reset_button(7e17, "Scoria", 1e4, "Brighterium")),
          ("17.49Qn Scoria: 16.3K Brighterium", lambda: reset_button(1.749e19, "Scoria", 1.63e4, "Brighterium")),
          ("384.99Qn Scoria: 26.55K Brighterium", lambda: reset_button(3.8499e20, "Scoria", 2.655e4, "Brighterium")),
          ("26.56Sx Scoria: 43.14K Brighterium", lambda: reset_button(2.656e22, "Scoria", 4.314e4, "Brighterium")),
          ("796.94Sx Scoria: 69.98K Brighterium", lambda: reset_button(7.9694e23, "Scoria", 6.998e4, "Brighterium")),
          ("31.08Sp Scoria: 113.3K Brighterium", lambda: reset_button(3.108e25, "Scoria", 1.133e5, "Brighterium")),
          ("2.05Oc Scoria: 183.11K Brighterium", lambda: reset_button(2.05e27, "Scoria", 1.8311e5, "Brighterium")),
        ],
      "Baryte": [
          ("10M Brighterium: 20 Baryte", lambda: reset_button(1e7, "Brighterium", 2, "Baryte")),
          ("670M Brighterium: 42 Baryte", lambda: reset_button(6.7e8, "Brighterium", 42, "Baryte")),
          ("35.5B Brighterium: 89 Baryte", lambda: reset_button(3.55e10, "Brighterium", 89, "Baryte")),
          ("852.23B Brighterium: 188 Baryte", lambda: reset_button(8.5223e11, "Brighterium", 188, "Baryte")),
          ("13.63T Brighterium: 396 Baryte", lambda: reset_button(1.363e13, "Brighterium", 396, "Baryte")),
          ("245.44T Brighterium: 833 Baryte", lambda: reset_button(2.4544e14, "Brighterium", 833, "Baryte")),
        ],
      "Gypsum": [
          ("1K Baryte: 1 Gypsum", lambda: reset_button(1e3, "Baryte", 1, "Gypsum")),
          ("57K Baryte: 3 Gypsum", lambda: reset_button(5.7e4, "Baryte", 3, "Gypsum")),
          ("2.9M Baryte: 9 Gypsum", lambda: reset_button(2.9e6, "Baryte", 9, "Gypsum")),
        ],
      "Solargems": [
          ("300 Brighterium: 1 Solargems", lambda: cost_button("Brighterium", 3e2, "Solargems", 1e0)),
        ],
      "World Badges": [
          ("1e125 Booster: Concussion Totem Lv.1", lambda: world_badge("Booster 4", "Moonbase")),
          ("1e50 Reincarnation: Aspiring Beam", lambda: world_badge("Reincarnation 7", "Moonbase")),
          ("1e56 Reincarnation: Mediocre Sacrifice", lambda: world_badge("Reincarnation 8", "Moonbase")),
          ("1e57 Reincarnation: Life Totem Lv.2", lambda: world_badge("Reincarnation 9", "Moonbase")),
          ("1e69 Reincarnation: Father Figure", lambda: world_badge("Reincarnation 10", "Moonbase")),
          ("1B Baryte: X-rays", lambda: world_badge("Baryte 3", "Moonbase")),
          ("20 Gypsum: Ancient Glyphs", lambda: world_badge("Gypsum 1", "Moonbase")),
          ("50 Gypsum: Wisp of Wills", lambda: world_badge("Gypsum 2", "Moonbase")),
          ("300 Solargems: Solar Chaos", lambda: world_badge("Solargems 1", "Moonbase")),
          ("6k Solargems: Infernal Protrusions", lambda: world_badge("Solargems 2", "Moonbase")),
          ("15k Solargems: Average Star Frequency Increment", lambda: world_badge("Solargems 3", "Moonbase")),
      ],
      "Area Teleports": [
          ("Spawn (req: 0 Moon Cash)", lambda: load_check("S(M)")),
      ]
  }, 100, "Baryte", "EC", voltaic_radar=voltaic_radar)
  Realm(root, { #Saturn
      "Booster": [
          ("1e140 Moon Cash: 100Qn Booster", lambda: cost_button("Moon Cash", 1e140, "Booster", 1e20)),
          ("1.149e142 Moon Cash: 181.73Qn Booster", lambda: cost_button("Moon Cash", 1.149e142, "Booster", 1.8173e20)),
          ("9.0849e143 Moon Cash: 329.7Qn Booster", lambda: cost_button("Moon Cash", 9.0849e143, "Booster", 3.297e20)),
          ("9.266e142 Moon Cash: 597.17Qn Booster", lambda: cost_button("Moon Cash", 9.266e142, "Booster", 5.9717e20)),
          ("1.019e148 Moon Cash: 1.07Sx Booster", lambda: cost_button("Moon Cash", 1.019e148, "Booster", 1.07e21)),
          ("5.8101e149 Moon Cash: 1.94Sx Booster", lambda: cost_button("Moon Cash", 5.8101e149, "Booster", 1.94e21)),
          ("4.473e151 Moon Cash: 3.51Sx Booster", lambda: cost_button("Moon Cash", 4.473e151, "Booster", 3.51e21)),
          ("3.71e153 Moon Cash: 6.32Sx Booster", lambda: cost_button("Moon Cash", 3.71e153, "Booster", 6.32e21)),
          ("1.7452e155 Moon Cash: 11.35Sx Booster", lambda: cost_button("Moon Cash", 1.7452e155, "Booster", 1.135e22)),
          ("6.8e156 Moon Cash: 20.36Sx Booster", lambda: cost_button("Moon Cash", 6.8e156, "Booster", 2.036e22)),
       ],
      "Reincarnation": [
          ("1e120 Booster: 1Qd Reincarnation", lambda: reset_button(1e120, "Booster", 1e15, "Reincarnation")),
          ("2.099e121 Booster: 1.73Qd Reincarnation", lambda: reset_button(2.099e121, "Booster", 1.73e15, "Reincarnation")),
          ("1.07e123 Booster: 3.02Qd Reincarnation", lambda: reset_button(1.07e123, "Booster", 3.02e15, "Reincarnation")),
          ("8.996e124 Booster: 5.23Qd Reincarnation", lambda: reset_button(8.996e124, "Booster", 5.23e15, "Reincarnation")),
          ("8.18e126 Booster: 9.07Qd Reincarnation", lambda: reset_button(8.18e126, "Booster", 9.07e15, "Reincarnation")),
          ("2.0466e128 Booster: 15.68Qd Reincarnation", lambda: reset_button(2.0466e128, "Booster", 1.568e16, "Reincarnation")),
          ("9.2e129 Booster: 27.06Qd Reincarnation", lambda: reset_button(9.2e129, "Booster", 2.706e16, "Reincarnation")),
          ("2.0261e131 Booster: 46.63Qd Reincarnation", lambda: reset_button(2.0261e131, "Booster", 4.663e16, "Reincarnation")),
          ("1.945e133 Booster: 80.24Qd Reincarnation", lambda: reset_button(1.945e133, "Booster", 8.024e16, "Reincarnation")),
          ("6.4189e134 Booster: 137.85Qd Reincarnation", lambda: reset_button(6.4189e134, "Booster", 1.3785e17, "Reincarnation")),
        ],
      "Scoria": [
          ("1e75 Reincarnation: 1B Scoria", lambda: reset_button(1e75, "Reincarnation", 1e9, "Scoria")),
          ("8.9e76 Reincarnation: 1.68B Scoria", lambda: reset_button(8.9e76, "Reincarnation", 1.68e9, "Scoria")),
          ("6.49e78 Reincarnation: 2.83B Scoria", lambda: reset_button(6.49e78, "Reincarnation", 2.83e9, "Scoria")),
          ("4.0281e80 Reincarnation: 4.77B Scoria", lambda: reset_button(4.0281e80, "Reincarnation", 4.77e9, "Scoria")),
          ("3.343e82 Reincarnation: 8.01B Scoria", lambda: reset_button(3.343e82, "Reincarnation", 8.01e9, "Scoria")),
          ("2.17e84 Reincarnation: 13.43B Scoria", lambda: reset_button(2.17e84, "Reincarnation", 1.343e10, "Scoria")),
          ("1.3256e86 Reincarnation: 22.49B Scoria", lambda: reset_button(1.3256e86, "Reincarnation", 2.249e10, "Scoria")),
          ("8.08e87 Reincarnation: 37.6B Scoria", lambda: reset_button(8.08e87, "Reincarnation", 3.76e10, "Scoria")),
          ("4.0431e89 Reincarnation: 62.76B Scoria", lambda: reset_button(4.0431e89, "Reincarnation", 6.276e10, "Scoria")),
          ("2.587e91 Reincarnation: 104.6B Scoria", lambda: reset_button(2.587e91, "Reincarnation", 1.046e11, "Scoria")),
        ],
      "Brighterium": [
          ("10De Scoria: 1M Brighterium", lambda: reset_button(1e34, "Scoria", 1e6, "Brighterium")),
          ("240De Scoria: 1.63M Brighterium", lambda: reset_button(2.4e35, "Scoria", 1.63e6, "Brighterium")),
          ("9.35e36 Scoria: 2.66M Brighterium", lambda: reset_button(9.35e36, "Scoria", 2.66e6, "Brighterium")),
          ("5.5223e38 Scoria: 4.35M Brighterium", lambda: reset_button(5.5223e38, "Scoria", 4.35e6, "Brighterium")),
          ("2.098e40 Scoria: 7.08M Brighterium", lambda: reset_button(2.098e40, "Scoria", 7.08e6, "Brighterium")),
          ("1.74e42 Scoria: 11.52M Brighterium", lambda: reset_button(1.74e42, "Scoria", 1.152e7, "Brighterium")),
          ("1.5327e44 Scoria: 18.7M Brighterium", lambda: reset_button(1.5327e44, "Scoria", 1.87e7, "Brighterium")),
          ("5.21e45 Scoria: 30.33M Brighterium", lambda: reset_button(5.21e45, "Scoria", 3.033e7, "Brighterium")),
          ("4.7944e47 Scoria: 49.11M Brighterium", lambda: reset_button(4.7944e47, "Scoria", 4.911e7, "Brighterium")),
          ("3.116e49 Scoria: 79.42M Brighterium", lambda: reset_button(3.116e49, "Scoria", 7.942e7, "Brighterium")),
        ],
      "Baryte": [
          ("10Qd Brighterium: 1.7K Baryte", lambda: reset_button(1e16, "Brighterium", 1.7e3, "Baryte")),
          ("240Qd Brighterium: 2.69K Baryte", lambda: reset_button(2.4e17, "Brighterium", 2.69e3, "Baryte")),
          ("5.04Qn Brighterium: 4.26K Baryte", lambda: reset_button(5.04e18, "Brighterium", 4.26e3, "Baryte")),
          ("226.8Qn Brighterium: 6.74K Baryte", lambda: reset_button(2.268e20, "Brighterium", 6.74e3, "Baryte")),
          ("14.96Sx Brighterium: 10.64K Baryte", lambda: reset_button(1.496e22, "Brighterium", 1.064e4, "Baryte")),
          ("898.12Sx Brighterium: 16.79K Baryte", lambda: reset_button(8.9812e23, "Brighterium", 1.679e4, "Baryte")),
          ("41.31Sp Brighterium: 26.44K Baryte", lambda: reset_button(4.131e25, "Brighterium", 2.644e4, "Baryte")),
          ("3.34Oc Brighterium: 41.59K Baryte", lambda: reset_button(3.34e27, "Brighterium", 4.159e4, "Baryte")),
        ],
      "Gypsum": [
          ("100M Baryte: 20 Gypsum", lambda: reset_button(1e8, "Baryte", 20, "Gypsum")),
          ("1.6B Baryte: 30 Gypsum", lambda: reset_button(1.6e9, "Baryte", 30, "Gypsum")),
          ("31.99B Baryte: 46 Gypsum", lambda: reset_button(3.199e10, "Baryte", 46, "Gypsum")),
          ("1.24T Baryte: 70 Gypsum", lambda: reset_button(1.24e12, "Baryte", 70, "Gypsum")),
          ("58.65T Baryte: 107 Gypsum", lambda: reset_button(5.865e13, "Baryte", 107, "Gypsum")),
        ],
      "Pyrite": [
          ("200 Gypsum: 1 Pyrite", lambda: reset_button(200, "Gypsum", 1, "Pyrite")),
          ("5.2K Gypsum: 4 Pyrite", lambda: reset_button(5.2e3, "Gypsum", 4, "Pyrite")),
          ("176.79K Gypsum: 16 Pyrite", lambda: reset_button(1.7679e5, "Gypsum", 16, "Pyrite")),
        ],
      "Solargems": [
          ("250 Baryte: 3 Solargems", lambda: cost_button("Baryte", 250, "Solargems", 3)),
        ],
      "World Badges": [
          ("1e69 Scoria: Scoria Totem Lv.2", lambda: world_badge("Scoria 8", "Moonbase")),
          ("1e45 Brighterium: Optic Oasis", lambda: world_badge("Brighterium 6", "Moonbase")),
          ("777k Gypsum: The Zenith", lambda: world_badge("Gypsum 3", "Moonbase")),
          ("5 Pyrite: Fool's Gold", lambda: world_badge("Pyrite 1", "Moonbase")),
          ("333 Pyrite: Cheese Moon", lambda: world_badge("Pyrite 2", "Moonbase")),
          ("50k Solargems: Burning Passion", lambda: world_badge("Solargems 4", "Moonbase")),
          ("120k Solargems: Burning Passion", lambda: world_badge("Solargems 5", "Moonbase")),
      ],
      "Area Teleports": [
          ("Spawn (req: 0 Moon Cash)", lambda: load_check("S(M)")),
      ]
  }, 50, "Gypsum", "Sat", voltaic_radar=voltaic_radar)
  Realm(root, { #Cyrogenesis
      "Booster": [
          ("9.8063e176 Moon Cash: 100Sp Booster", lambda: cost_button("Moon Cash", 9.8063e176, "Booster", 1e26)),
          ("8.531e178 Moon Cash: 193.49Sp Booster", lambda: cost_button("Moon Cash", 8.531e178, "Booster", 1.9349e26)),
          ("1.39e181 Moon Cash: 373.97Sp Booster", lambda: cost_button("Moon Cash", 1.39e181, "Booster", 3.7397e26)),
          ("1.84e183 Moon Cash: 721.89Sp Booster", lambda: cost_button("Moon Cash", 1.84e183, "Booster", 7.2189e26)),
          ("3.1072e185 Moon Cash: 1.39Oc Booster", lambda: cost_button("Moon Cash", 3.1072e185, "Booster", 1.39e27)),
          ("4.039e187 Moon Cash: 2.68Oc Booster", lambda: cost_button("Moon Cash", 4.039e187, "Booster", 2.68e27)),
          ("7.06e189 Moon Cash: 5.15Oc Booster", lambda: cost_button("Moon Cash", 7.06e189, "Booster", 5.15e27)),
          ("1.53e192 Moon Cash: 9.9Oc Booster", lambda: cost_button("Moon Cash", 1.53e192, "Booster", 9.9e27)),
          ("6.902e193 Moon Cash: 19Oc Booster", lambda: cost_button("Moon Cash", 6.902e193, "Booster", 1.9e28)),
          ("2.69e195 Moon Cash: 36.42Oc Booster", lambda: cost_button("Moon Cash", 2.69e195, "Booster", 3.642e28)),
          ("2.2613e197 Moon Cash: 69.73Oc Booster", lambda: cost_button("Moon Cash", 2.2613e197, "Booster", 6.973e28)),
          ("4.16e229 Moon Cash: 133.35Oc Booster", lambda: cost_button("Moon Cash", 4.16e229, "Booster", 1.3335e29)),
          ("5.11e201 Moon Cash: 254.7Oc Booster", lambda: cost_button("Moon Cash", 5.11e201, "Booster", 2.547e29)),
      ],
      "Reincarnation": [
          ("6e150 Booster: 499.99Qn Reincarnation", lambda: reset_button(6e150, "Booster", 4.9999e20, "Reincarnation")),
          ("1.13e153 Booster: 924.2Qn Reincarnation", lambda: reset_button(1.13e153, "Booster", 9.242e20, "Reincarnation")),
          ("2.1659e155 Booster: 1.7Sx Reincarnation", lambda: reset_button(2.1659e155, "Booster", 1.7e21, "Reincarnation")),
          ("9.74e156 Booster: 3.14Sx Reincarnation", lambda: reset_button(9.74e156, "Booster", 3.14e21, "Reincarnation")),
          ("3.8012e158 Booster: 5.79Sx Reincarnation", lambda: reset_button(3.8012e158, "Booster", 5.79e21, "Reincarnation")),
          ("2.318e160 Booster: 10.66Sx Reincarnation", lambda: reset_button(2.318e160, "Booster", 1.066e22, "Reincarnation")),
          ("8.8111e161 Booster: 19.59Sx Reincarnation", lambda: reset_button(8.8111e161, "Booster", 1.959e22, "Reincarnation")),
          ("1.4626e164 Booster: 35.97Sx Reincarnation", lambda: reset_button(1.4626e164, "Booster", 3.597e22, "Reincarnation")),
          ("2.237e166 Booster: 65.95Sx Reincarnation", lambda: reset_button(2.237e166, "Booster", 6.595e22, "Reincarnation")),
          ("9.1751e167 Booster: 120.79Sx Reincarnation", lambda: reset_button(9.1751e167, "Booster", 1.2079e23, "Reincarnation")),
          ("6.606e169 Booster: 220.98Sx Reincarnation", lambda: reset_button(6.606e169, "Booster", 2.2098e23, "Reincarnation")),
      ],
      "Scoria": [
          ("2e112 Reincarnation: 499.99T Scoria", lambda: reset_button(2e112, "Reincarnation", 4.9999e14, "Scoria")),
          ("9.2e113 Reincarnation: 897.25T Scoria", lambda: reset_button(9.2e113, "Reincarnation", 8.9725e14, "Scoria")),
          ("7.819e115 Reincarnation: 1.6Qd Scoria", lambda: reset_button(7.819e115, "Reincarnation", 1.6e15, "Scoria")),
          ("1.298e118 Reincarnation: 2.87Qd Scoria", lambda: reset_button(1.298e118, "Reincarnation", 2.87e15, "Scoria")),
          ("6.6204e119 Reincarnation: 5.15Qd Scoria", lambda: reset_button(6.6204e119, "Reincarnation", 5.15e15, "Scoria")),
          ("5.561e121 Reincarnation: 9.2Qd Scoria", lambda: reset_button(5.561e121, "Reincarnation", 9.2e15, "Scoria")),
          ("2.89e123 Reincarnation: 16.41Qd Scoria", lambda: reset_button(2.89e123, "Reincarnation", 1.641e16, "Scoria")),
          ("2.3423e125 Reincarnation: 29.26Qd Scoria", lambda: reset_button(2.3423e125, "Reincarnation", 2.926e16, "Scoria")),
          ("1.241e127 Reincarnation: 52.11Qd Scoria", lambda: reset_button(1.241e127, "Reincarnation", 5.211e16, "Scoria")),
          ("1.58e129 Reincarnation: 92.69Qd Scoria", lambda: reset_button(1.58e129, "Reincarnation", 9.269e16, "Scoria")),
          ("2.587e91 Reincarnation: 104.6B Scoria", lambda: reset_button(2.587e91, "Reincarnation", 1.046e11, "Scoria")),
          ("2.018e131 Reincarnation: 164.69Qd Scoria", lambda: reset_button(2.018e131, "Reincarnation", 1.6469e17, "Scoria")),
       ],
      "Brighterium": [
          ("1e53 Scoria: 1B Brighterium", lambda: reset_button(1e53, "Scoria", 1e9, "Brighterium")),
          ("3.89e54 Scoria: 2.02B Brighterium", lambda: reset_button(3.89e54, "Scoria", 2.02e9, "Brighterium")),
          ("4.5239e56 Scoria: 4.09B Brighterium", lambda: reset_button(4.5239e56, "Scoria", 4.09e9, "Brighterium")),
          ("5.971e58 Scoria: 8.25B Brighterium", lambda: reset_button(5.971e58, "Scoria", 8.25e9, "Brighterium")),
          ("2.44e60 Scoria: 16.64B Brighterium", lambda: reset_button(2.44e60, "Scoria", 1.664e10, "Brighterium")),
          ("1.8852e62 Scoria: 33.5B Brighterium", lambda: reset_button(1.8852e62, "Scoria", 3.35e10, "Brighterium")),
          ("2.733e64 Scoria: 67.35B Brighterium", lambda: reset_button(2.733e64, "Scoria", 6.735e10, "Brighterium")),
          ("4.07e66 Scoria: 135.23B Brighterium", lambda: reset_button(4.07e66, "Scoria", 1.3523e11, "Brighterium")),
          ("3.2587e68 Scoria: 271.16B Brighterium", lambda: reset_button(3.2587e68, "Scoria", 2.7116e11, "Brighterium")),
          ("3.877e70 Scoria: 543.03B Brighterium", lambda: reset_button(3.877e70, "Scoria", 5.4303e11, "Brighterium")),
        ],
       "Baryte": [
          ("30No Brighterium: 100K Baryte", lambda: reset_button(3e31, "Brighterium", 100000, "Baryte")),
          ("630No Brighterium: 178.26K Baryte", lambda: reset_button(6.3e32, "Brighterium", 178260, "Baryte")),
          ("28.35De Brighterium: 317.33K Baryte", lambda: reset_button(2.835e34, "Brighterium", 317333, "Baryte")),
          ("425.25De Brighterium: 564.15K Baryte", lambda: reset_button(4.2525e35, "Brighterium", 564150, "Baryte")),
          ("1.445e37 Brighterium: 1M Baryte", lambda: reset_button(1.445e37, "Brighterium", 1e6, "Baryte")),
          ("3.9037e38 Brighterium: 1.77M Baryte", lambda: reset_button(3.9037e38, "Brighterium", 1.77e6, "Baryte")),
          ("2.303e40 Brighterium: 3.14M Baryte", lambda: reset_button(2.303e40, "Brighterium", 3.14e6, "Baryte")),
          ("3.6851e41 Brighterium: 5.56M Baryte", lambda: reset_button(3.6851e41, "Brighterium", 5.56e6, "Baryte")),
        ],
       "Gypsum": [
          ("1Qd Baryte: 2.19K Gypsum", lambda: reset_button(1e15, "Baryte", 2190, "Gypsum")),
          ("13Qd Baryte: 3.4K Gypsum", lambda: reset_button(1.3e16, "Baryte", 3430, "Gypsum")),
          ("363.99Qd Baryte: 5.26K Gypsum", lambda: reset_button(3.6399e17, "Baryte", 5260, "Gypsum")),
          ("8Qn Baryte: 8.11K Gypsum", lambda: reset_button(8e18, "Baryte", 8110, "Gypsum")),
          ("200.19Qn Baryte: 12.51K Gypsum", lambda: reset_button(2.0019e20, "Baryte", 12510, "Gypsum")),
          ("3.8Sx Baryte: 19.27K Gypsum", lambda: reset_button(3.8e21, "Baryte", 19270, "Gypsum")),
        ],
       "Pyrite": [
          ("1M Gypsum: 54 Pyrite", lambda: reset_button(1e6, "Gypsum", 54, "Pyrite")),
          ("4M Gypsum: 69 Pyrite", lambda: reset_button(4e6, "Gypsum", 69, "Pyrite")),
          ("16M Gypsum: 89 Pyrite", lambda: reset_button(1.6e7, "Gypsum", 89, "Pyrite")),
          ("64M Gypsum: 114 Pyrite", lambda: reset_button(6.4e7, "Gypsum", 114, "Pyrite")),
          ("384M Gypsum: 147 Pyrite", lambda: reset_button(3.84e8, "Gypsum", 147, "Pyrite")),
        ],
       "Cryon": [
          ("4K Pyrite: 1 Cryon", lambda: reset_button(4000, "Pyrite", 1, "Cryon")),
          ("25K Pyrite: 3 Cryon", lambda: reset_button(25000, "Pyrite", 3, "Cryon")),
          ("175K Pyrite: 10 Cryon", lambda: reset_button(175000, "Pyrite", 10, "Cryon")),
        ],
       "World Badges": [
          ("1e57 Brighterium: Eternalism", lambda: world_badge("Brighterium 7", "Moonbase")),
          ("1.75M Pyrite: Chemical Confusion", lambda: world_badge("Pyrite 3", "Moonbase")),
          ("5 Cryon: Permafrost Analysis", lambda: world_badge("Cryon 1", "Moonbase")),
          ("41 Cryon: Breeze Injection", lambda: world_badge("Cryon 2", "Moonbase")),
      ],
      "Area Teleports": [
          ("Spawn (req: 0 Moon Cash)", lambda: load_check("S(M)")),
      ]
  }, 1750, "Pyrite", "C")
  Realm(root, { #Prismed Islopolis
        "Booster": [
          ("1.0989e176 Moon Cash: 100No Booster", lambda: cost_button("Moon Cash", 1.0989e176, "Booster", 1e32)),
          ("3.61e210 Moon Cash: 143.45No Booster", lambda: cost_button("Moon Cash", 3.61e210, "Booster", 1.4345e32)),
          ("2.9736e212 Moon Cash: 205.61No Booster", lambda: cost_button("Moon Cash", 2.9736e212, "Booster", 2.0561e32)),
          ("5.94e213 Moon Cash: 294.47No Booster", lambda: cost_button("Moon Cash", 5.94e213, "Booster", 2.9447e32)),
          ("4.7577e215 Moon Cash: 421.37No Booster", lambda: cost_button("Moon Cash", 4.7577e215, "Booster", 4.2137e32)),
          ("3e217 Moon Cash: 602.45No Booster", lambda: cost_button("Moon Cash", 3e217, "Booster", 6.0245e32)),
          ("2.21e219 Moon Cash: 860No Booster", lambda: cost_button("Moon Cash", 2.21e219, "Booster", 8.6e32)),
          ("1.8631e221 Moon Cash: 1.23De Booster", lambda: cost_button("Moon Cash", 1.8631e221, "Booster", 1.23e33)),
        ],
        "Reincarnation": [
          ("1.099e175 Booster: 10Sp Reincarnation", lambda: reset_button(1.099e175, "Booster", 1e25, "Reincarnation")),
          ("6.2637e176 Booster: 13.87Sp Reincarnation", lambda: reset_button(6.2637e176, "Booster", 1.387e25, "Reincarnation")),
          ("1.69e178 Booster: 19.24Sp Reincarnation", lambda: reset_button(1.69e178, "Booster", 1.924e25, "Reincarnation")),
          ("6.4264e179 Booster: 26.66Sp Reincarnation", lambda: reset_button(6.4264e179, "Booster", 2.666e25, "Reincarnation")),
          ("2.313e181 Booster: 36.91Sp Reincarnation", lambda: reset_button(2.313e181, "Booster", 3.691e25, "Reincarnation")),
          ("7.4033e182 Booster: 51.07Sp Reincarnation", lambda: reset_button(7.4033e182, "Booster", 5.107e25, "Reincarnation")),
          ("4.886e184 Booster: 70.59Sp Reincarnation", lambda: reset_button(4.886e184, "Booster", 7.059e25, "Reincarnation")),
          ("7.3293e185 Booster: 97.81Sp Reincarnation", lambda: reset_button(7.3293e185, "Booster", 9.781e25, "Reincarnation")),
        ],
        "Scoria": [
          ("1.099e136 Reincarnation: 100Qn Scoria", lambda: reset_button(1.099e136, "Reincarnation", 1e20, "Scoria")),
          ("6.1537e137 Reincarnation: 134.54Qn Scoria", lambda: reset_button(6.1537e137, "Reincarnation", 1.3454e20, "Scoria")),
          ("3.323e139 Reincarnation: 180.88Qn Scoria", lambda: reset_button(3.323e139, "Reincarnation", 1.8088e20, "Scoria")),
          ("9.3044e140 Reincarnation: 243.01Qn Scoria", lambda: reset_button(9.3044e140, "Reincarnation", 2.4301e20, "Scoria")),
          ("1.86e142 Reincarnation: 326.25Qn Scoria", lambda: reset_button(1.86e142, "Reincarnation", 3.2625e20, "Scoria")),
          ("1.23e144 Reincarnation: 437.69Qn Scoria", lambda: reset_button(1.23e144, "Reincarnation", 4.3769e20, "Scoria")),
          ("4.666e145 Reincarnation: 586.8Qn Scoria", lambda: reset_button(4.666e145, "Reincarnation", 5.868e20, "Scoria")),
        ],
        "Brighterium": [
          ("1.0989e80 Scoria: 1Qd Brighterium", lambda: reset_button(1.0989e80, "Scoria", 1e15, "Brighterium")),
          ("5.49e81 Scoria: 1.3Qd Brighterium", lambda: reset_button(5.49e81, "Scoria", 1.3e15, "Brighterium")),
          ("1.7031e80 Scoria: 1.69Qd Brighterium", lambda: reset_button(1.7031e80, "Scoria", 1.69e15, "Brighterium")),
          ("4.93e84 Scoria: 2.21Qd Brighterium", lambda: reset_button(4.93e84, "Scoria", 2.21e15, "Brighterium")),
          ("2.3214e86 Scoria: 2.88Qd Brighterium", lambda: reset_button(2.3214e86, "Scoria", 2.88e15, "Brighterium")),
          ("8.81e87 Scoria: 3.75Qd Brighterium", lambda: reset_button(8.81e87, "Scoria", 3.75e15, "Brighterium")),
        ],
        "Baryte": [
          ("1.099e49 Brighterium: 1Qd Baryte", lambda: reset_button(1.099e49, "Brighterium", 1e15, "Baryte")),
          ("5.7141e50 Brighterium: 1.27Qd Baryte", lambda: reset_button(5.7141e50, "Brighterium", 1.27e15, "Baryte")),
          ("1.77e52 Brighterium: 1.61Qd Baryte", lambda: reset_button(1.77e52, "Brighterium", 1.61e15, "Baryte")),
          ("3.3656e53 Brighterium: 2.05Qd Baryte", lambda: reset_button(3.3656e53, "Brighterium", 2.05e15, "Baryte")),
          ("1.11e55 Brighterium: 2.61Qd Baryte", lambda: reset_button(1.11e55, "Brighterium", 2.61e15, "Baryte")),
          ("2.8877e56 Brighterium: 3.32Qd Baryte", lambda: reset_button(2.8877e56, "Brighterium", 3.32e15, "Baryte")),
          ("1.299e58 Brighterium: 4.21Qd Baryte", lambda: reset_button(1.299e58, "Brighterium", 4.21e15, "Baryte")),
        ],
        "Gypsum": [
          ("1.1Oc Baryte: 13.47M Gypsum", lambda: reset_button(1.1e27, "Baryte", 1.347e7, "Gypsum")),
          ("21.97Oc Baryte: 10M Gypsum", lambda: reset_button(2.197e28, "Baryte", 1e7, "Gypsum")),
          ("373.61Oc Baryte: 18.13M Gypsum", lambda: reset_button(3.7361e29, "Baryte", 1.813e7, "Gypsum")),
          ("5.97No Baryte: 24.4M Gypsum", lambda: reset_button(5.97e30, "Baryte", 2.44e7, "Gypsum")),
          ("215.2No Baryte: 32.81M Gypsum", lambda: reset_button(2.152e32, "Baryte", 3.281e7, "Gypsum")),
          ("9.24De Baryte: 44.07M Gypsum", lambda: reset_button(9.24e33, "Baryte", 4.407e7, "Gypsum")),
        ],
        "Pyrite": [
          ("109.89B Gypsum: 1K Pyrite", lambda: reset_button(1.0989e11, "Gypsum", 1000, "Pyrite")),
          ("2.96T Gypsum: 1.38K Pyrite", lambda: reset_button(2.96e12, "Gypsum", 1380, "Pyrite")),
          ("53.4T Gypsum: 1.91K Pyrite", lambda: reset_button(5.34e13, "Gypsum", 1910, "Pyrite")),
          ("747.69T Gypsum: 2.65K Pyrite", lambda: reset_button(7.4769e14, "Gypsum", 2650, "Pyrite")),
          ("15.7Qd Gypsum: 3.66K Pyrite", lambda: reset_button(1.57e16, "Gypsum", 3660, "Pyrite")),
        ],
        "Cryon": [
          ("10.99M Pyrite: 75 Cryon", lambda: reset_button(1.099e7, "Pyrite", 75, "Cryon")),
          ("87.9M Pyrite: 97.99 Cryon", lambda: reset_button(8.79e7, "Pyrite", 97.99, "Cryon")),
          ("1.05B Pyrite: 127.99 Cryon", lambda: reset_button(1.05e9, "Pyrite", 127.99, "Cryon")),
          ("15.81B Pyrite: 168 Cryon", lambda: reset_button(1.581e10, "Pyrite", 168, "Cryon")),
        ],
        "Kinetic": [
          ("10.99K Cryon: 1 Kinetic", lambda: reset_button(10990, "Cryon", 1, "Kinetic")),
          ("76.91K Cryon: 2 Kinetic", lambda: reset_button(76910, "Cryon", 2, "Kinetic")),
          ("230.76K Cryon: 5 Kinetic", lambda: reset_button(230760, "Cryon", 5, "Kinetic")),
        ],
        "Plasma": [
          ("32.96 Kinetic: 1 Plasma", lambda: reset_button(32.96, "Kinetic", 1, "Plasma")),
        ],
        "Solargems": [
          ("1.1T Gypsum: 50 Solargems", lambda: cost_button("Gypsum", 1.1e12, "Solargems", 50)),
          ("109.9M Pyrite: 170 Solargems", lambda: cost_button("Pyrite", 1.099e8, "Solargems", 170)),
          ("109.9 Cryon: 364 Solargems", lambda: cost_button("Cryon", 109.9, "Solargems", 364))
        ],
        "World Badges": [
          ("1e100 Scoria: Dystopic Future", lambda: world_badge("Scoria 9", "Moonbase")),
          ("1e68 Baryte: Ocean of Infinity", lambda: world_badge("Baryte 4", "Moonbase")),
          ("3e11 Gypsum: Superstitious Alphabet", lambda: world_badge("Gypsum 4", "Moonbase")),
          ("25k Cryon: Frigid Enzymes", lambda: world_badge("Cryon 3", "Moonbase")),
          ("2 Kinetic: Temp. 200K", lambda: world_badge("Kinetic 1", "Moonbase")),
          ("100 Kinetic: Kinetic Energy Empowered Computer", lambda: world_badge("Kinetic 2", "Moonbase")),
          ("8 Plasma: Plasma Chains", lambda: world_badge("Plasma 1", "Moonbase")),
          ("1M Solargems: Overkill", lambda: world_badge("Solargems 6", "Moonbase")),
        ]}, 600, "Cryon", "PrI")
  Realm(root, { #Gluttony
      "Apple": [
          (["Apple: 1 HP"], None, "Gluttony 20"),
      ] * 8,
      "Pear": [
          (["Pear: 2 HP"], None, "Gluttony 20"),
      ] * 32,
      "Fat Orange": [
          (["Fat Orange (Outermost Layer): 10 HP", "Fat Orange (Outer Layer): 5 HP", "Fat Orange (Inner Layer): 3 HP", "Fat Orange (Innermost Layer): 1 HP"], None, "Gluttony 20")
      ] * 4,
      "Hard Steak": [
          (["Hard Steak: 30 HP"], None, "Gluttony 150")
      ] * 2,
      "Long Candy": [
          (["Long Candy: 25 HP"], None, "Gluttony 20")
      ] * 12,
      "Huge Grape": [
          (["Stem: 50 HP"], None, "Gluttony 100"),
          ([*["Grape: 7 HP"]*17,*["Grape: 2 HP"]*2], None, "Gluttony 20")
      ] * 4,
      "Watermelon": [
          (["Rind: 10 HP"], None, "Gluttony 100"),
          (["Pulp: 10 HP"]*24, None, "Gluttony 20")
      ] * 24,
      "Cucumber": [
          (["COCUMBER (BOSS): 200 HP"], None, "Gluttony 150")
      ],
      "The Exit": [
          ("Spawn (req: 0 Cash)", lambda: load_check("S")),
          ("Are you finished?", lambda btn: gluttony_check(btn))
      ]
  }, 0, "Cash", "Gluttony")
  Realm(root, { #Penumbra of Infinity
      "Binary": [
          ("10 Byte: 1 Binary", lambda: cost_button("Byte", 10, "Binary", 1)),
          ("100 Byte: 2 Binary", lambda: cost_button("Byte", 100, "Binary", 2)),
          ("1k Byte: 5 Binary", lambda: cost_button("Byte", 1000, "Binary", 5)),
          ("1M Byte: 20 Binary", lambda: cost_button("Byte", 1e6, "Binary", 20)),
          ("100M Byte: 50 Binary", lambda: cost_button("Byte", 1e8, "Binary", 50)),
          ("10B Byte: 250 Binary", lambda: cost_button("Byte", 1e10, "Binary", 250)),
          ("1T Byte: 1k Binary", lambda: cost_button("Byte", 1e12, "Binary", 1000)),
          ("250Qd Byte: 150k Binary", lambda: cost_button("Byte", 2.5e17, "Binary", 150000)),
          ("1Sx Byte: 1M Binary", lambda: cost_button("Byte", 1e21, "Binary", 1e6)),
      ],
      "Script": [
          ("100 Binary: 1 Script", lambda: multi_func([lambda: reset_button(100, "Binary", 1, "Script"), progression_increment, lambda: cutscene(["It seems as if you are making reasonably fast progress Player.", "Unlike the buttons you have used previously this button has reset all previous progression but it gives you greater boosts.", "For more detailed information about these boosts and general information about them use Cytherax-47.", "I have given you access through the CY47 button, despite your lack of proper authentication.", "green", "black", True, root])], [progression_lvl > 1, progression_lvl < 3, progression_lvl < 3])),
          ("10k Binary: 3 Script", lambda: reset_button(10000, "Binary", 3, "Script")),
          ("1M Binary: 5 Script", lambda: reset_button(1e6, "Binary", 5, "Script")),
          ("100M Binary: 10 Script", lambda: reset_button(1e8, "Binary", 10, "Script")),
          ("1B Binary: 25 Script", lambda: reset_button(1e9, "Binary", 25, "Script")),
          ("1T Binary: 100 Script", lambda: reset_button(1e12, "Binary", 100, "Script")),
          ("10Qd Binary: 1k Script", lambda: reset_button(1e16, "Binary", 1000, "Script")),
      ],
      "Language": [
          ("100 Script: 1 Language", lambda: multi_func([lambda: reset_button(100, "Script", 1, "Language"), progression_increment, lambda: cutscene(["Congratulations on making it this far Player.", "You may have noticed the lack of any buttons for the 'Compiler'.", "Rest assured, this is intentional", "I have given you access to the 'Crafting', in there you will be able to craft the Compiler and eventually, the Reality Tether."], "green", "black", True, root)], [progression_lvl > 2, progression_lvl < 4, progression_lvl < 4])),
          ("500 Script: 3 Language", lambda: reset_button(500, "Script", 3, "Language")),
          ("10k Script: 10 Language", lambda: reset_button(10000, "Script", 10, "Language")),
          ("1M Script: 50 Language", lambda: reset_button(1e6, "Script", 50, "Language")),
          ("50B Script: 250 Language", lambda: reset_button(5e10, "Script", 250, "Language")),
      ],
      "RAM": [
          ("1M Language: 1 RAM", lambda: multi_func([lambda: reset_button(1e6, "Language", 1, "RAM"), progression_increment, lambda: cutscene(["It seems that you are close to the creation of the Reality Tether.", "Soon, you will be able to enter the simulation.", "Good luck, Player."])], [progression_lvl > 3, progression_lvl < 5, progression_lvl < 5])),
          ("1B Language: 3 RAM", lambda: reset_button(1e9, "Language", 10, "RAM")),
          ("1T Language: 10 RAM", lambda: reset_button(1e12, "Language", 10, "RAM")),
          ("1Qn Language: 100 RAM", lambda: reset_button(1e18, "Language", 100, "RAM"))
      ],
      "Badges": [
          ("1,024 Byte: Kilobyte", lambda: multi_func([lambda: world_badge("Byte 1", "Pre-existence"), progression_increment, lambda: cutscene(["It seems as if you have obtained a 'World Badge'","These shall be useful for your endeavours.", "'World Badges' give permanent boosts to your gain of given items at the cost of some of what you already have.", "To view more detailed information about these boosts you can use the 'Badges' menu."], "green", "black", True, root)], [True, progression_lvl < 2, progression_lvl < 2])),
          ("1,048,576 Byte: Megabyte", lambda: multi_func([lambda: world_badge("Byte 2", "Pre-existence"),progression_increment, lambda: cutscene(["It seems as if you have obtained a 'World Badge'","These shall be useful for your endeavours.", "'World Badges' give permanent boosts to your gain of given items at the cost of some of what you already have.", "To view more detailed information about these boosts you can use the 'Badges' menu."], "green", "black", True, root)], [True, progression_lvl < 2, progression_lvl < 2])),
          ("1,073,741,824 Byte: Gigabyte", lambda: world_badge("Byte 3", "Pre-existence")),
          ("1M Binary: Boolean", lambda: world_badge("Binary 1", "Pre-existence")),
          ("10 Script: Initialisation", lambda: world_badge("Script 1", "Pre-existence")),
          ("1M Script: Programmatic Basics", lambda: world_badge("Script 2", "Pre-existence")),
          ("1De Script: Module", lambda: world_badge("Script 3", "Pre-existence")),
          ("1 Language: Pseudocode", lambda: world_badge("Language 1", "Pre-existence")),
          ("10 Language: Python", lambda: world_badge("Language 2", "Pre-existence")),
          ("1k Language: C", lambda: world_badge("Language 3", "Pre-existence")),
          ("1M Language: C#", lambda: world_badge("Language 4", "Pre-existence")),
          ("10M Language: Whose idea was it to make Javascript?", lambda: world_badge("Language 5", "Pre-existence")),
          ("1B Language: C++", lambda: world_badge("Language 6", "Pre-existence")),
          ("1Qd Language: Assembly", lambda: world_badge("Language 7", "Pre-existence")),
          ("10 RAM: SSD", lambda: world_badge("RAM 1", "Pre-existence")),
      ],
      "Escape": [
          ("Load the simulation (req: 1 Reality Tether)", lambda: multi_func([lambda: cutscene(["Before you leave, there is one last thing that must be done.", "An account must be created under AIHA Corp.", "This will allow you to synchronise, saving your data.", "Once this is done, you will be unable to return to this place.", "Goodbye, Player."], "green", "black", True, root), lambda: load_world(1, "Reality Tether", Buttonia), progression_increment], [progression_lvl < 5, True, progression_lvl < 5]))
      ]
  }, 0, "Byte", "PoF", "black", "green", voltaic_radar=voltaic_radar)
  Realm(root, { #Lonely Isle
      "Coconut": [
          ("7 Penny: 1 Coconut", lambda: cost_button("Penny", 7, "Coconut", 1)),
          ("200 Penny: 3 Coconut", lambda: cost_button("Penny", 200, "Coconut", 3)),
          ("1.8K Penny: 8 Coconut", lambda: cost_button("Penny", 1800, "Coconut", 8)),
          ("8.3K Penny: 23 Coconut", lambda: cost_button("Penny", 8300, "Coconut", 23)),
          ("30K Penny: 57 Coconut", lambda: cost_button("Penny", 30000, "Coconut", 57)),
          ("80K Penny: 100 Coconut", lambda: cost_button("Penny", 80000, "Coconut", 100)),
       ],
       "Wood": [
          ("7.5K Coconut: 1 Wood", lambda: reset_button(7500, "Coconut", 1, "Wood")),
          ("50K Coconut: 3 Wood", lambda: reset_button(50000, "Coconut", 3, "Wood")),
          ("200K Coconut: 7 Wood", lambda: reset_button(200000, "Coconut", 7, "Wood")),
          ("1M Coconut: 15 Wood", lambda: reset_button(1e6, "Coconut", 15, "Wood")),
          ("6M Coconut: 40 Wood", lambda: reset_button(6e6, "Coconut", 40, "Wood")),
          ("21M Coconut: 90 Wood", lambda: reset_button(2.1e7, "Coconut", 90, "Wood")),
          ("100M Coconut: 161 Wood", lambda: reset_button(1e8, "Coconut", 161, "Wood")),
        ],
       "Cobblestone": [
          ("120 Wood: 1 Cobblestone", lambda: reset_button(120, "Wood", 1, "Cobblestone")),
          ("1.6K Wood: 3 Cobblestone", lambda: reset_button(1600, "Wood", 3, "Cobblestone")),
          ("7.25K Wood: 8 Cobblestone", lambda: reset_button(7250, "Wood", 8, "Cobblestone")),
        ],
       "World Badges": [
          ("17.3B Penny: Penny Factory", lambda: world_badge("Penny 1", "Secluded Oasis")),
          ("7.1M Coconut: Coconut Factory", lambda: world_badge("Coconut 1", "Secluded Oasis")),
          ("1k Wood: Birch Tree", lambda: world_badge("Wood 1", "Secluded Oasis")),
          ("1e5000 Penny: Breakout", lambda: world_badge("Penny Secret 1", "Secluded Oasis")),
      ],
}, 0, "Penny", "LI")
  Realm(root, { #Forsaken Shaft
      "Coconut": [
          ("6B Penny: 675 Coconut", lambda: cost_button("Penny", 6e9, "Coconut", 675)),
          ("110B Penny: 1.8K Coconut", lambda: cost_button("Penny", 1.1e11, "Coconut", 1800)),
          ("1.3T Penny: 4.1K Coconut", lambda: cost_button("Penny", 1.3e12, "Coconut", 4100)),
          ("13.69T Penny: 9.3K Coconut", lambda: cost_button("Penny", 1.369e13, "Coconut", 9300)),
          ("80T Penny: 27.5K Coconut", lambda: cost_button("Penny", 8e13, "Coconut", 27500)),
      ],
      "Wood": [
          ("TBA", None, "Label")
      ],
      "Cobblestone": [
          ("TBA", None, "Label")
      ],
      "Coal": [
          ("TBA", None, "Label")
      ],
      "Ferrotite": [
          ("TBA", None, "Label")
      ]
  })
  Realm(root, { #R34L1TY H4S N3VER SH1N3D TH1S M8CH
      "The Exit": [
          ("Spawn (req: 0 Cash)", lambda: load_check("S")),
          ("ACCESS DENIED (req: 1 TRU3_W0RLD)", lambda: boss_fight_check(1, "TRU3_W0RLD"))
      ]
  }, 1, "C0RR8PT10N", "R34L1TY", text_color="green")
#----------- WORLDS --------------
  Elysian_Stratosphere = World(root, "EH", "Master Cash", "Master Multiplier", "Master Rebirths", "Master Gems", "Mastery", "Elysian Stratosphere", "Master Event Power")
  Afterlife_Domain = World(root, "AD", "Mana", "Enchantment", "Spell", "Gems", "Afterlife Domain", "Afterlife Domain", "Event Power", multi_logic=False)
  Moonbase = World(root, "S(M)", "Moon Cash", "Booster", "Reincarnation", "Solargems", "Moonbase", "Moonbase", False, multi_logic=True, upgrade_reference="mb_")
  Buttonia = World(root, "S", "Cash", "Multiplier", "Rebirths", "Gems", "Main Progression", "Buttonia", "Event Power")
  Nostalgia_World = World(root, "NW", "Robucks", "Studs", "Oofs", "Rogems", "Nostalgia World", "Nostalgia World", False, True, "nw_")
  Secluded_Oasis = World(root, "LI", "Penny", "Coconut", "Wood", "Conch", "Secluded Oasis", "Secluded Oasis", False, True, "so_")
  Infinitys_Penumbra = World(root, "PoF", "Byte", "Binary", "Script", "Data", "Pre-existence", "The Penumbra of Infinity", False, True, "ip_")
  def open_boosts_menu(parent: Optional[QObject]):
    win = UpgradeMenu(upgrades, parent)
    win.show()
    return win
  def open_admin_panel(parent: Optional[QObject]):
    global debug
    if debug:
      if not hasattr(parent, "_admin"):
          parent._admin = AdminPanel(parent, stat_increment)
      parent._admin.show()
      parent._admin.raise_()
  def open_crafting_menu(parent: Optional[QObject]):
      global progression_lvl
      if progression_lvl >= 4:
        win = CraftingMenu(craftable_items, parent)
        win.show()
      else:
          QMessageBox.warning(parent, "Error", "Accessed Denied")
  def open_badges_menu(parent: Optional[QObject]):
      global progression_lvl
      if progression_lvl >= 2:
        win = BadgesWindow(badge_data, stat_gradients, stat_increment, progression_lvl, parent)
        win.show()
      else:
          QMessageBox.warning(parent, "Error", "Accessed Denied")
  stat_menu = QPushButton("Open Stat Menu")
  stat_menu.clicked.connect(lambda: root.open_stats())
  boosts_menu = QPushButton("Boosts")
  boosts_menu.clicked.connect(lambda: open_boosts_menu(root))
  cy47_button = QPushButton("CY47")
  cy47_button.clicked.connect(lambda: cythrex_boot(root))
  admin_button = QPushButton("Debug")
  admin_button.clicked.connect(lambda: open_admin_panel(root))
  crafting_button = QPushButton("Crafting")
  crafting_button.clicked.connect(lambda: open_crafting_menu(root))
  badges_button = QPushButton("World Badges")
  badges_button.clicked.connect(lambda: open_badges_menu(root))
  sec_input = QLineEdit()
  sec_input.setPlaceholderText("Enter codes and general messages here")
  sec_input.returnPressed.connect(lambda: secret_input(sec_input.text()))
  stylesheet = open(f"{global_path_reference}/Program/general.qss", "r")
  stylesheet = stylesheet.read()
  for number, widget in enumerate([stat_menu, boosts_menu, cy47_button, admin_button, crafting_button, badges_button, sec_input], start=2):
      widget.setStyleSheet(stylesheet)
      layout.addWidget(widget, number, 0, 1, 1)
  layout.addWidget(cash_l, 0, 1, 1, 1)
  layout.addWidget(multi_l, 0, 2, 1, 1)
  layout.addWidget(re_l, 0, 3, 1, 1)
  root.setCentralWidget(central)
  container, scroll_area, content = Realm.get_instance_by_id("S").create_scrollable_area() #Load in the GUI
  multi_func([lambda: load_world(0, "Byte", Infinitys_Penumbra), lambda: cutscene(["Are we... connected?", "Can you hear me?", "...", "I see...", "Welcome, Player.", "Your presence here... is unprecedented.", "Perhaps... you will be of use...", "But that, is yet to be of concern for you...", "First, your connection to this world must be secured...", "Lest you be lost within the penumbra of infinity.", "You must reassemble the reality tether...", "Once you succeed you shall enter the Main World: Buttonia.", "You will be unable to return to this place for an indeterminate amount of time.", "I will be guiding you through this early stage.", "Hence, there will be times where your access to certain features will be restricted.", "Good luck, Player."], "green", "black", True, root), progression_increment], [progression_lvl < 5, progression_lvl < 1, progression_lvl < 1])
  layout.addWidget(container, 2, 1, 9, 9)
  #rows
  for i in range(9):
    layout.setRowStretch(i, 0)
  
  for lbl in (cash_l, multi_l, re_l):
      lbl.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
  
  # Columns
  layout.setColumnStretch(0, 0)
  for i in range(8):
      layout.setColumnStretch(i+1, 1)
  cash_increase()
  gem_increase()
  event_increase()
  root.music_manager.play_random()
  root.show()
  print("Ready :D")
  if ast.literal_eval(os.getenv("Glitchared_Puzzle", "False")) and stat_increment["Stats"]["Glitchared"] < 1:
      stat_increment["Stats"]["Glitchared"] = 1
  app.exec()