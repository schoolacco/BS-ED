from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import simpleaudio as sa
import json
from pydub import AudioSegment
import time
import datetime
import threading
import math
import os
import random
import sys
import sqlalchemy
import werkzeug
from Module import Mantissa, tkinter_frames, Geode, GradientLabel
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
    def closeEvent(self, event: QCloseEvent):
      Save(stat_increment, upgrades)
      event.accept()
def_upgrades = {
    "cash_speed": {
      "name": "Cash Speed",
      "max_level": 22,
      "base_cost": 30,
      "cost_growth": 1.05,
      "effect": 1,
      "current_lvl": 0
    },
    "gem_speed": {
        "name": "Faster Gems",
        "max_level": 17,
        "base_cost": 60,
        "cost_growth": 1.2,
        "effect": 50,
        "current_lvl": 0
    },
    "cash_multi": {
        "name": "Cash Multiplier",
        "max_level": 10,
        "base_cost": 300,
        "cost_growth": 1.2,
        "effect": 0.2,
        "current_lvl": 0
    },
    "gem_timer_amount": {
        "name": "More Gems From Timer",
        "max_level": 36,
        "base_cost": 500,
        "cost_growth": 1.3,
        "effect": 10000,
        "current_lvl": 0
    },
    "lucky_draw": {
        "name": "Lucky Draw [random x100 Cash]",
        "max_level": 100,
        "base_cost": 15000,
        "cost_growth": 1.05,
        "effect": 0.01,
        "current_lvl": 0
    },
    "lucky_draw_multi": {
        "name": "Lucky Multiplier",
        "max_level": 30,
        "base_cost": 100000,
        "cost_growth": 1.2,
        "effect": 1,
        "current_lvl": 0
    },
    "geode_speed": {
        "name": "Geode Speed [min 0.25s]",
        "max_level": 25,
        "base_cost": 25000,
        "cost_growth": 1.2,
        "effect": 0.03,
        "current_lvl": 0
    },
    "geode_luck": {
        "name": "Geode Luck [max 2.5x]",
        "max_level": 15,
        "base_cost": 50000,
        "cost_growth": 1.25,
        "effect": 0.1,
        "current_lvl": 0
    },
    "crit_luck": {
        "name": "Critical Luck [max 2x]",
        "max_level": 20,
        "base_cost": 50000,
        "cost_growth": 1.15,
        "effect": 0.1,
        "current_lvl": 0
    }
}
upgrades = def_upgrades
MANTISSA_THRESHOLD = 1e300
luck = 1
crit_luck = 1
geode_speed= 1
bulk_roll= 1
music = ["Catswing.mp3", "Flamewall.mp3", "Ambrosia.mp3"]
def Geode_roll(btn, geode, luck=1, geode_speed=1, bulk_roll=1):
    global stat_increment
    local_crit = crit_luck + upgrades["crit_luck"]["effect"]*upgrades["crit_luck"]["current_lvl"]
    local_luck = luck + upgrades["geode_luck"]["effect"]*upgrades["geode_luck"]["current_lvl"]
    btn.setEnabled(False)
    stat_increment = geode.open(stat_increment, local_luck, bulk_roll, local_crit)
    QTimer.singleShot(int(geode_speed*1000), lambda: btn.setEnabled(True))
def load_check(key, req, unit, buttons):
    global stat_increment, container, scroll_area, content, layout
    amount = stat_increment[key][unit]["Value"]
    req = float_to_mantissa(req) if isinstance(amount, Mantissa) else req
    if amount >= req:
      container.deleteLater()  # remove old scroll area
      container, scroll_area, content = tkinter_frames.create_scrollable_area(root, buttons)
      layout.addWidget(container, 2, 1, 3, 3)
def float_to_mantissa(value: float) -> Mantissa:
      """Converts a float or int into a Mantissa representation."""
      if isinstance(value, Mantissa):
          return value
      if value == 0:
          return Mantissa(0, 0)
      exponent = int(math.floor(math.log10(abs(value))))
      mantissa = value / (10 ** exponent)
      return Mantissa(mantissa, exponent)
def upgrade_cost(info, level):
    base = info["base_cost"]
    growth = info["cost_growth"]
    return int(base * (growth ** level))
def serialize(obj):
    if isinstance(obj, Mantissa):
        return obj.to_dict()
    elif isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    else:
        return obj

# Recursive deserialization
def deserialize(obj):
    if isinstance(obj, dict):
        if obj.get("__mantissa__"):
            return Mantissa.from_dict(obj)
        return {k: deserialize(v) for k, v in obj.items()}
    else:
        return obj
def Load():
       '''Load your data from your savefile'''
       global upgrades
       if os.path.exists("savefile.json"): # If you have saved before
        with open("savefile.json", "r")  as file: # Read the file
          try:
            data = deserialize(json.load(file)) # Attempt to return backup data
            try:
              upgrades = data["Upgrades"]
            except:
                upgrades = def_upgrades
            try:
                del data["Upgrades"]
            except:
                pass
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
                      try:
                          del data["Upgrades"]
                      except:
                          pass
                      return data
                   except json.JSONDecodeError: # If corrupted
                      print("Backup file is also corrupted.")
                      return None
             else:
              print("Backup file does not exist.")
              return None
       else:
          print("You have never saved before.")
          return None # Return your empty collection
def Save(collection, upgrades):
        '''Saves your data to a json file, and makes the previous file a backup'''
        collection["Upgrades"] = upgrades
        try:
          if os.path.exists("savefile.json") and collection != {}: # If there is a savefile and your collection isn't empty
            with open("savefile.json", "r") as file: # Read the file
               data = json.load(file)
            with open("backup.json", "w") as file: # Write to the backup file and place the data
               json.dump(data, file)
          with open("savefile.json", "w") as file: # Insert data into main save file
            json.dump(serialize(collection), file)
        except json.JSONDecodeError: # If file is corrupted
           print("WARNING: Your back up file or main save file is CORRUPTED")
def calculate_multi(unit):
    """Calculates total multiplier for a given unit, supporting Mantissa instances."""
    global stat_increment, crit_luck
    local_crit = crit_luck + upgrades["crit_luck"]["effect"]*upgrades["crit_luck"]["current_lvl"]
    total = Mantissa(1, 0)  # Start as 1 in Mantissa form
    keys = list(stat_increment.keys())
    for key in keys:
      stat_list = list(stat_increment[key].keys())
      for item in stat_list:
          amount = stat_increment[key][item].get("Value", 0)
          multis = stat_increment[key][item].get("Multis")
          if multis is None:
            multis = {}
  
          multiplier = multis.get(unit)
          if multiplier is None:
              continue  # skip if this stat does not affect the unit
  
          if isinstance(multiplier, (int, float)):
              multiplier = float_to_mantissa(multiplier)
  
          amount_m = amount if isinstance(amount, Mantissa) else float_to_mantissa(amount)
          if amount_m.num == 0:
              continue
  
          total *= Mantissa(1, 0) + (multiplier * amount_m)
    # Ensure we don't return zero
    if total.num == 0:
        return Mantissa(1, 0)

    if total.exp < math.log(MANTISSA_THRESHOLD, 10):
        total = round(total.to_float(), 2)
        total = float_to_mantissa(total)
    total *= 2 if random.randint(1,500//local_crit) == 1 and not isinstance(total,Mantissa) else float_to_mantissa(2) if random.randint(1,500//local_crit) == 1 and isinstance(total, Mantissa) else 1 if not isinstance(total, Mantissa) else Mantissa(1,0)
    return total
def cash_increase():
    global stat_increment, cash_l

    # Base multiplier
    multiplier_value = stat_increment["Main"]["Multiplier"]["Value"]
    if isinstance(multiplier_value, (int, float)):
        multiplier_value = max(multiplier_value, 1)
        multiplier_m = float_to_mantissa(multiplier_value)
    else:
        multiplier_m = multiplier_value

    # Extra multipliers from other stats
    multi = calculate_multi("Cash")
    multi *= 1+(upgrades["cash_multi"]["current_lvl"]*upgrades["cash_multi"]["effect"]) if not isinstance(multi, Mantissa) else float_to_mantissa(1+(upgrades["cash_multi"]["current_lvl"]*upgrades["cash_multi"]["effect"]))
    # Compute approximate float multiplier
    approx_multiplier = multiplier_m.to_float() if hasattr(multiplier_m, "to_float") else float(multiplier_m)

    # Compute delay and speed ratio
    base_delay = 250
    base_delay /= upgrades["cash_speed"]["current_lvl"]
    if not isinstance(approx_multiplier, Mantissa):
      delay = max(1, int(math.ceil(base_delay / approx_multiplier)))
    else:
      delay = 1
    speed_ratio = base_delay / delay  # How many "ticks" worth of speed we have

    # Cap at 250× speed, convert overflow into extra cash
    if delay <= 1:
        # If we're at minimum delay, cash scales instead
        cash_scaling = approx_multiplier / (base_delay) if not isinstance(approx_multiplier, Mantissa) else approx_multiplier / float_to_mantissa(base_delay)
    else:
        cash_scaling = 1

    # Increment cash
    cash_scaling = float_to_mantissa(cash_scaling) if not isinstance(cash_scaling, Mantissa) else cash_scaling
    cash_increment = Mantissa(1, 0) * multi * cash_scaling
    cash_increment *= float_to_mantissa(1+upgrades["lucky_draw_multi"]["effect"]*upgrades["lucky_draw_multi"]["current_lvl"]) if random.random() <= upgrades["lucky_draw"]["effect"]*upgrades["lucky_draw"]["current_lvl"] else Mantissa(1,0)
    if isinstance(stat_increment["Main"]["Cash"]["Value"], Mantissa):
        stat_increment["Main"]["Cash"]["Value"] += cash_increment
    else:
        try:
          stat_increment['Main']["Cash"]["Value"] += cash_increment.to_float()
          stat_increment['Main']["Cash"]["Value"] = round(stat_increment["Main"]["Cash"]["Value"], 2)
        except TypeError:
          stat_increment['Main']["Cash"]["Value"] = float_to_mantissa(stat_increment['Main']["Cash"]["Value"])
          stat_increment["Main"]["Cash"]["Value"] += cash_increment
    # Update label
    val = stat_increment["Main"]["Cash"]["Value"]
    display_val = val.to_string() if hasattr(val, "to_string") else val
    cash_l.setText(f"Cash: {display_val}")
    timer = QTimer(root)
    timer.singleShot(delay, cash_increase)
    # Schedule next increment
def gem_increase():
    global stat_increment
    stat_increment["Main"]["Gems"]["Value"] += (1+upgrades["gem_timer_amount"]["current_lvl"]*upgrades["gem_timer_amount"]["effect"])
    if upgrades["gem_speed"]["current_lvl"] == 0:
        period = 60000
    else:
        period = 60000//(upgrades["gem_speed"]["effect"]*upgrades["gem_speed"]["current_lvl"])
    timer = QTimer(root)
    timer.singleShot(period, gem_increase)
def cost_button(key, unit, cost, unit_2, receive, key_2="Main"):
    global cash_l, multi_l, stat_increment

    value = stat_increment[key][unit]["Value"]

    if isinstance(value, Mantissa) and not isinstance(cost, Mantissa):
        cost = float_to_mantissa(cost)

    # Check if the player can afford it
    if value >= cost:
        # Deduct cost
        stat_increment[key][unit]["Value"] -= cost
        if key_2 == "Geode":
            keys = list(geode_list.keys())
            for key in keys:
                stat_list = list(geode_list[key].keys())
                if unit_2 in stat_list and stat_increment["Geode"].get(unit_2) == None:
                    stat_increment["Geode"][unit_2] = {"Value": receive, "Multis": geode_list[key][unit_2]["Multis"]}
        # Calculate the increment (reward)
        Multi = calculate_multi(unit_2)
        if isinstance(Multi, Mantissa):
             receive = float_to_mantissa(receive)
        increment = Multi*receive
        # Add the increment
        if not isinstance(stat_increment[key_2][unit_2]["Value"], Mantissa) and increment.exp < math.log(MANTISSA_THRESHOLD, 10):
            increment = increment.to_float()
        if isinstance(increment, Mantissa) and not isinstance(stat_increment[key_2][unit_2]["Value"], Mantissa):
          stat_increment[key_2][unit_2]["Value"] = float_to_mantissa(stat_increment[key_2][unit_2]["Value"])
        stat_increment[key_2][unit_2]["Value"] += increment
        # Update labels
        cash_val = stat_increment["Main"]["Cash"]["Value"]
        cash_text = cash_val.to_string() if isinstance(cash_val, Mantissa) else cash_val
        cash_l.setText(f"Cash: {cash_text}")

        multi_val = stat_increment["Main"]["Multiplier"]["Value"]
        multi_text = multi_val.to_string() if isinstance(multi_val, Mantissa) else multi_val
        multi_l.setText(f"Multiplier: {multi_text}")

        stat_increment["Extra"]["Buttons Pressed"]["Value"] += 1

def reset_button(key, cost, unit, reward, unit_2):
    global cash_l, multi_l, re_l, stat_increment

    current_value = stat_increment[key][unit]['Value']
    stat_list = list(stat_increment[key].keys())
    if isinstance(current_value, Mantissa) and not isinstance(cost, Mantissa):
        cost = float_to_mantissa(cost)
    if not isinstance(current_value, Mantissa) and isinstance(cost, Mantissa):
        current_value = float_to_mantissa(current_value)
    if current_value >= cost:
        # Reset all lower-tier stats before unit_2
        for i in range(stat_list.index(unit_2)):
            stat_increment[key][stat_list[i]]["Value"] = 0

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
            value = stat_increment[key][unit_2]["Value"]
            value= float_to_mantissa(value)
            value += reward_m
            value = value.to_float() if value.exp < math.log(MANTISSA_THRESHOLD, 10) else value
            stat_increment[key][unit_2]["Value"] = value
        r_text = stat_increment['Main']['Rebirths']['Value'] if not isinstance(stat_increment['Main']['Rebirths']['Value'], Mantissa) else stat_increment['Main']['Rebirths']['Value'].to_string()
        # Update labels
        cash_l.setText(f"Cash: {stat_increment['Main']['Cash']['Value']}")
        multi_l.setText(f"Multiplier: {stat_increment['Main']['Multiplier']['Value']}")
        re_l.setText(f"Rebirth: {r_text}")
        stat_increment["Extra"]["Buttons Pressed"]["Value"] += 1

def recovery_button_set(key, req, unit, Set, unit_2):
    global stat_increment
    amount = stat_increment[key][unit]["Value"]
    if isinstance(amount, Mantissa) and not isinstance(req, Mantissa):
        req = float_to_mantissa(req)
    if not isinstance(amount, Mantissa) and isinstance(req, Mantissa):
        amount = float_to_mantissa(amount)
    if amount >= req:
        if stat_increment[key][unit_2]["Value"] < Set:
          stat_increment[key][unit_2]["Value"] = Set
    else:
     pass
def recovery_button_fetch(key, req, unit, recovery, unit_2):
    global stat_increment
    amount = stat_increment[key][unit]["Value"]
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
          stat_increment[key][unit_2]["Value"] = float_to_mantissa(stat_increment[key][unit_2]["Value"])
      stat_increment[key][unit_2]["Value"] += amount
      c_msg = cash if not isinstance(cash, Mantissa) else cash.to_string()
      cash_l.setText(f"Cash: {c_msg}")
      multi = stat_increment['Main']['Multiplier']['Value']
      m_msg = multi if not isinstance(multi, Mantissa) else multi.to_string()
      multi_l.setText(f"Multiplier: {m_msg}")
      rebirths = stat_increment['Main']['Rebirths']['Value']
      re_msg = rebirths if not isinstance(rebirths, Mantissa) else rebirths.to_string()
      re_l.setText(f"Rebirths: {re_msg}")
    else:
     pass
app = QApplication(sys.argv)

root = Window()
root.setWindowTitle("BS:ED but bad")
cash_l = QLabel()
multi_l = QLabel()
re_l = QLabel()
stat_increment = {"Main": {"Cash": {"Value": 0, "Multis": None}, "Multiplier":  {"Value": 0, "Multis": None}, "Rebirths":  {"Value": 0, "Multis": {"Multiplier": 2}}, "Stone": {"Value": 0, "Multis": {"Cash": 1.5, "Rebirths": 2}}, "White Gems": {"Value": 0, "Multis": {"Multiplier": 1.5, "Stone": 1.8}}, "Crystal": {"Value": 0, "Multis": {"Cash": 2, "White Gems": 3}}, "Iron": {"Value": 0, "Multis": {"Rebirths": 1.5, "Crystal": 2}}, "Gold": {"Value": 0, "Multis": {"Cash": 2, "Stone": 2, "Iron": 2}}, "Quartz": {"Value": 0, "Multis": {"Multiplier": 10, "Rebirths": 2, "Stone": 5, "White Gems": 3, "Crystal": 2, "Gold": 2}}, "Jade": {"Value": 0, "Multis": {"Cash": 3, "Rebirths": 10, "Stone": 4, "Crystal": 4, "Quartz": 3}}, "Obsidian": {"Value": 0, "Multis": {"Rebirths": 15, "Stone": 15,"White Gems": 15, "Crystal": 10, "Iron": 10, "Gold": 7.5, "Jade": 5}}, "Ruby": {"Value": 0, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2}}, "Emerald": {"Value": 0, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2}}, "Sapphire": {"Value": 0, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2}}, "Diamond": {"Value": 0, "Multis": {"Emerald": 3, "Sapphire": 2}}, "Starlight": {"Value": 0, "Multis": {"Ruby": 6, "Sapphire": 3, "Diamond": 3}}, "Ion": {"Value": 0, "Multis": {"Jade": 4, "Ruby": 2, "Emerald": 10, "Sapphire": 1.4, "Diamond": 5, "Starlight": 5}}, "Uranium": {"Value": 0, "Multis": {"Crystal": 100, "Sapphire": 60, "Starlight": 5, "Ion": 2.2}}, "Bismuth": {"Value": 0, "Multis": {"Ruby": 50, "Emerald": 25, "Sapphire": 12, "Diamond": 3, "Ion": 2.5, "Uranium": 2}} , "Boracite": {"Value": 0, "Multis": {"Starlight": 5, "Uranium": 3, "Bismuth": 1.5}}, "Nissonite": {"Value": 0, "Multis": {"Obsidian": 5, "Bismuth": 2.75, "Boracite": 2.25}}, "Orpiment": {"Value": 0, "Multis": {"Cash": 23, "Multiplier": 22, "Rebirths": 21, "Stone": 20, "White Gems": 19, "Crystal": 18, "Iron": 17, "Gold": 16, "Quartz": 15, "Jade": 14, "Obsidian": 13, "Ruby": 12, "Emerald": 11, "Sapphire": 10, "Diamond": 9, "Starlight": 8, "Ion": 7, "Uranium": 6, "Bismuth": 5, "Boracite": 4, "Nissonite": 3}}, "Tetra": {"Value": 0, "Multis": {"Diamond": 1e4, "Boracite": 30, "Nissonite": 10, "Orpiment": 2.5}}, "Volt": {"Value": 0, "Multis": {"Uranium": 100, "Nissonite": 4, "Tetra": 2}}, "Aquamarine": {"Value": 0, "Multis": {"Obsidian": 1e6, "Ion": 500, "Uranium": 400, "Nissonite": 5, "Volt": 2.1}}, "Lollipop": {"Value": 0, "Multis": {"Emerald": 8152, "Sapphire": 4096, "Diamond": 2048, "Starlight": 1024, "Ion": 512, "Uranium": 256, "Bismuth": 128, "Boracite": 64, "Nissonite": 32, "Orpiment": 16, "Tetra": 8, "Volt": 4, "Aquamarine": 2}}, "C0RR8PT10N": {"Value": 0, "Multis": {"Cash": 6, "Multiplier": 6, "Rebirths": 6, "Stone": 6, "White Gems": 6, "Crystal": 6, "Iron": 6, "Gold": 6, "Quartz": 6, "Jade": 6, "Obsidian": 6, "Ruby": 6, "Emerald": 6, "Sapphire": 6, "Diamond": 6, "Starlight": 6, "Ion": 6, "Uranium": 6, "Bismuth": 6, "Boracite": 6, "Nissonite": 6, "Orpiment": 2.3, "Tetra": 6, "Volt": 6, "Aquamarine": 4, "Lollipop": 3}}, "Stargazed Metal": {"Value": 0, "Multis": {"Cash": 1e100, "Multiplier": 1e100, "Rebirths": 1e100, "Stone": 1e100, "White Gems": 1e100, "Crystal": 1e100, "Iron": 1e100, "Gold": 1e100, "Quartz": 1e100, "Jade": 1e100, "Obsidian": 7.5, "Ruby": 7.5, "Emerald": 7.5, "Aquamarine": 2.25, "Lollipop": 2.25, "C0RR8PT10N": 3}}, "Gyge": {"Value": 0, "Multis": {"Ruby": 1e25, "Emerald": 1e25, "Sapphire": 1e25, "Diamond": 1e25, "Starlight": 1e25, "Ion": 1e25, "Uranium": 1e25, "Bismuth": 1e25, "Boracite": 1e25, "Nissonite": 1e25, "Volt": 18, "Lollipop": 7, "C0RR8PT10N": 10, "Stargazed Metal": 2}}, "Auly Plate": {"Value": 0, "Multis": {"Cash": Mantissa(1,288290), "Orpiment": 1.61, "Tetra": 3.12, "Volt": 6.25, "Aquamarine": 12.5, "Lollipop": 18, "C0RR8PT10N": 50, "Stargazed Metal": 5, "Gyge": 2}}, "Shell Piece": {"Value": 0, "Multis": {"Cash": 1e75, "Multiplier": 1e75, "Rebirths": 1e75, "Stone": 1e75, "White Gems": 1e75, "Crystal": 1e75, "Iron": 1e75, "Gold": 1e75, "Quartz": 1e75, "Jade": 1e75, "Obsidian": 1e75, "Ruby": 1e75, "Emerald": 1e75, "Sapphire": 1e75, "Diamond": 1e75, "Starlight": 1e75, "Ion": 1e75, "Uranium": 1e75, "Bismuth": 1e75, "Boracite": 1e75, "Nissonite": 1e75, "Orpiment": 1e75, "Tetra": 100, "Volt": 100, "Aquamarine": 100, "Lollipop": 100, "C0RR8PT10N": 100, "Mint": 100, "Gems": 20, "Metal": 100, "Press": 100, "Microparticles": 100, "Star": 100, "Robot": 100, "Prototype": 100}}, "Singularity": {"Value": 0, "Multis": {"Cash": Mantissa(1,987654321), "Volt": 1200, "C0RR8PT10N": 150, "Gyge": 4, "Auly Plate": 2.5, "Gems": 75}}, "Capsuled Singularity": {"Value": 0, "Multis": {"Cash": Mantissa(1,303030303), "Ruby": Mantissa(1,266664), "Emerald": Mantissa(1,266664), "Sapphire": Mantissa(1,266664), "Diamond": Mantissa(1,266664), "Starlight": Mantissa(1,133337), "Ion": Mantissa(1,666666), "Uranium": Mantissa(1,333333), "Bismuth": Mantissa(1,12555), "Boracite": Mantissa(1,5555), "Nissonite": Mantissa(1,2222), "Orpiment": Mantissa(1,1000), "Tetra": Mantissa(1,500), "Volt": 1e150, "Aquamarine": 1e75, "Lollipop": 1e25, "C0RR8PT10N": 1e6, "Stargazed Metal": 2500, "Gyge": 500, "Auly Plate": 25, "Shell Piece": 2.5, "Prototype": 1240, "Gems": 300}}, "Gems": {"Value": 0, "Multis": None}}, "Extra": {"Buttons Pressed": {"Value": 0, "Multis": None}, "Geodes Opened": {"Value": 0, "Multis": None}}, "Geode": {}} # Gems technically aren't part of main progression, they're just placed here for temporary convenience
stat_list = list(stat_increment["Main"].keys())
geode_list = {"Stone Geode": {
        "Dezyp": {"Chance": 12000, "Multis": {"Cash": 15, "Rebirths": 20, "Stone": 2, "White Gems": 2}},
        "Podrillium": {"Chance": 1000000000, "Multis": {"Cash": Mantissa(1,3003), "Multiplier": Mantissa(1,3003), "Rebirths": Mantissa(1,3003), "Stone": Mantissa(1,3003), "White Gems": Mantissa(1,3003), "Crystal": Mantissa(1,303), "Iron": Mantissa(1,303), "Gold": Mantissa(1,303), "Jade": Mantissa(1,303), "Obsidian": 1e200, "Ruby": 1e200, "Emerald": 1e200, "Sapphire": 1e200, "Diamond": 1e100, "Starlight": 1e100, "Ion": 1e100, "Uranium": 1e100, "Bismuth": 1e50, "Boracite": 1e50, "Nissonte": 1e50, "Orpiment": 1e25, "Tetra": 1e20, "Volt": 1e15, "Aquamarine": 1e10, "Lollipop": 10000, "C0RR8PT10N": 10, "Stargazed Metal": 5, "Gyge": 4, "Auly Plate": 3, "Shell Piece": 2}} #Podrillium is real guys!!! Trust!!!
    },
    "White Gems Geode": {
        "Digenite": {"Chance": 100, "Multis": {"Cash": 4, "Stone": 6}},
        "Oneillite": {"Chance": 500, "Multis": {"Cash": 15, "Multiplier": 15, "Rebirths": 4, "Stone": 2, "White Gems": 1.25}},
        "Alum": {"Chance": 13000, "Multis": {"Stone": 12, "White Gems": 1.8, "Crystal": 1.14}},
        "Chaoite": {"Chance": 273000, "Multis": {"Cash": 6, "Multiplier": 6, "Rebirths": 6, "Stone": 6, "White Gems": 6, "Crystal": 6, "Iron": 6}},
    },
    "Crystal Geode": {
        "Amethyst": {"Chance": 333, "Multis": {"Stone": 6, "White Gems": 4, "Crystal": 3}},
        "Paradoxite": {"Chance": 65000, "Multis": {"Cash": 44, "Multipliers": 55, "Rebirths": 66, "Stone": 77, "White Gems": 88, "Crystal": 30, "Iron": 5}},
    },
    "Iron Geode": {
        "Silver": {"Chance": 142, "Multis": {"Multiplier": 10, "White Gems": 5, "Iron": 2}},
        "Platinum": {"Chance": 32000, "Multis": {"White Gems": 10, "Crystal": 20, "Iron": 15, "Gold": 3, "Quartz": 2}},
        "Mythril": {"Chance": 2000000, "Multis": {"Cash": 999, "Crystal": 5, "Iron": 10, "Gold": 50, "Quartz": 100}}
    },
    "Gold Geode": {
        "Yellow Beryl": {"Chance": 6666, "Multis": {"Crystal": 15, "Gold": 3}},
        "Opal": {"Chance": 51000, "Multis": {"Cash": 8, "Multiplier": 8, "Rebirths": 8, "Crystal": 8, "Gold": 8, "Jade": 8, "Ruby": 1.3, "Sapphire": 1.3, "Diamond": 1.3}},
        "Holeyum": {"Chance": 2750000, "Multis": {"Rebirths": 1000, "White Gems": 1000, "Crystal": 500, "Iron": 500, "Gold": 300}}
    },
    "Quartz Geode": {
        "Pink Quartz": {"Chance": 50, "Multis": {"Crystal": 10, "Quartz": 3}},
        "Cyan Quartz": {"Chance": 166, "Multis": {"Rebirths": 10, "Crystal": 10, "Quartz": 4}},
        "Black Quartz": {"Chance": 2500, "Multis": {"Stone": 10, "White Gems": 10, "Iron": 10, "Quartz": 5}},
        "Garnet": {"Chance": 23000, "Multis": {"Gold": 30, "Quartz": 15, "Jade": 10, "Obsidian": 5}},
        "Milky Quartz": {"Chance": 800000, "Multis": {"Cash": 10, "Multiplier": 10, "Rebirths": 10, "Stone": 100, "White Gems": 100, "Crystal": 10, "Iron": 100, "Gold": 10, "Quartz": 100, "Jade": 10, "Obsidian": 100}}
    },
    "Jade Geode": {
        "Jurite": {"Chance": 20, "Multis": {"Iron": 3, "Gold": 3, "Quartz": 3, "Jade": 3}},
        "Molybendum": {"Chance": 23000, "Multis": {"Stone": 1000, "White Gems": 1000, "Iron": 1000, "Quartz": 1000}},
        "Rbadam's Smokestackite": {"Chance": 100000, "Multis": {"Gold": 44,"Quartz": 33," Jade": 22, "Obsidian": 11, "Ruby": 1.1}}
    },
    "Emoji Geode": {
        ":3": {"Chance": 2, "Multis": {"Quartz": 2}},
        "O_O": {"Chance": 100, "Multis": {"Quartz": 5, "Jade": 2}},
        "^_^": {"Chance": 2000, "Multis": {"Multiplier": 1.1, "Rebirths": 2.2, "Stone": 3.3, "White Gems": 4.4, "Crystal": 5.5, "Iron": 6.6, "Gold": 7.7, "Quartz": 8.8}},
        "'-'": {"Chance": 12000, "Multis": {"Iron": 1.1, "Gold": 1.1, "Quartz": 1.1, "Jade": 1.1, "Obsidian": 1.1}},
        ":D": {"Chance": 35000, "Multis": {"Jade": 5, "Obsidian": 3, "Ruby": 2}},
        "OwO": {"Chance": 150000, "Multis": {"Gold": 5.5, "Emerald": 5.5}},
        "UwU": {"Chance": 1000000, "Multis": {"Gold": 6.5, "Quartz": 6.5, "Jade": 6.5, "Obsidian": 6.5, "Ruby": 5.4, "Emerald": 4.3, "Sapphire": 3.2, "Diamond": 2.1}}
    },
    "Obsidian Geode": {
        "Draconite": {"Chance": 100, "Multis": {"Crystal": 10, "Obsidian": 2}},
        "Burneite": {"Chance": 400, "Multis": {"Cash": 7, "Multiplier": 7, "Rebirths": 7, "Stone": 7, "White Gems": 7, "Crystal": 7, "Iron": 7, "Gold": 7, "Quartz": 7, "Jade": 7}},
        "Dragonglass": {"Chance": 6666, "Multis": {"Crystal": 25, "Quartz": 15, "Jade": 10, "Obsidian": 5}},
        "Hellyerite": {"Chance": 47000, "Multis": {"Obsidian": 10, "Ruby": 3}},
        "Palladium": {"Chance": 350000, "Multis": {"Cash": 6, "Multiplier": 6, "Rebirths": 6, "Stone": 6, "White Gems": 6, "Crystal": 6, "Iron": 6, "Gold": 6, "Jade": 6, "Obsidian": 6, "Ruby": 6, "Gems": 1.5}},
        "Osumillite": {"Chance": 4200000, "Multipliers": {"Cash": 6544, "Gold": 50, "Quartz": 40, "Jade": 30, "Obsidian": 20, "Ruby": 10}}
    },
    "Ruby Geode": {
        "Pascoite": {"Chance": 666, "Multis": {"Obsidian": 3, "Ruby": 2}},
        "Roselite": {"Chance": 3333, "Multis": {"Jade": 5, "Obsidian": 5, "Ruby": 3}},
        "Wulfenite": {"Chance": 50000, "Multis": {"Multiplier": 15, "Obsidian": 15, "Ruby": 8}}
    },
    "Emerald Geode": {
        "Olivine": {"Chance": 250, "Multis": {"Ruby": 3, "Emerald": 2}},
        "Heazlewoodite": {"Chance": 4000, "Multis": {"Obsidian": 5, "Ruby": 5, "Emerald": 3}},
        "Gaspeite": {"Chance": 35000, "Multis": {"Emerald": 15}},
        "Talc": {"Chance": 230000, "Multis": {"Cash": 15, "Jade": 15, "Emerald": 15}}
    },
    "Sapphire Geode": {
        "Lapis": {"Chance": 142, "Multis": {"Emerald": 3, "Sapphire": 2}},
        "Ringwoodite": {"Chance": 2000, "Multis": {"Ruby": 5, "Emerald": 5, "Sapphire": 3}},
        "Kyanite": {"Chance": 15000, "Multis": {"Sapphire": 15}},
        "Azurite": {"Chance": 85000, "Multis": {"Rebirths": 15, "Crystal": 15, "Quartz": 15 ,"Sapphire": 8}},
        "Cobalt": {"Chance": 3000000, "Multis": {"Cash": 20, "Multiplier": 20, "Rebirths": 20, "Crystal": 20, "Gold": 20, "Quartz": 20, "Jade": 20, "Ruby": 20, "Emerald": 20, "Sapphire": 20}}
    },
    "Diamond Geode": {
        "Spatial Dust": {"Chance": 20, "Multis": {"Ruby": 3, "Emerald": 3, "Sapphire": 3, "Diamond": 4, "Starlight": 2}},
        "Astrophyllite": {"Chance": 71000, "Multis": {"Gold": 80, "Jade": 30, "Obsidan": 12, "Ruby": 52, "Diamond": 20, "Starlight": 25}}
    },
    "Starlight Geode": {
        "Niter": {"Chance": 4000, "Multis": {"Starlight": 5}},
        "Yrnote": {"Chance": 80000, "Multis": {"Ruby": 10, "Emerald": 10, "Sapphire": 10, "Diamond": 20, "Starlight": 15}},
        "Sercense": {"Chance": 1400000, "Multis": {"Cash": 300, "Multiplier": 300, "Rebirths": 300, "Stone": 290, "White Gems": 280, "Crystal": 270, "Iron": 260, "Gold": 130, "Quartz": 120, "Jade": 110, "Obsidian": 100, "Ruby": 50, "Emerald": 40, "Sapphire": 30, "Diamond": 20, "Starlight": 10}}
    },
    "Ion Geode": {
        "Neuron": {"Chance": 20, "Multis": {"Starlight": 5, "Ion": 2}},
        "Antimatter": {"Chance": 45000, "Multis": {"Rebirths": 10, "Gold": 10, "Quartz": 10, "Sapphire": 10, "Diamond": 10, "Starlight": 10, "Ion": 10}}
    },
    "Uranium Geode": {
        "Acid": {"Chance": 20, "Multis": {"Uranium": 1.4, "Starlight": 2}},
        "Niflhemite": {"Chance": 100, "Multis": {"Multiplier": 3, "Rebirths": 3, "White Gems": 3, "Quartz": 3, "Obsidian": 3, "Ruby": 3, "Diamond": 3, "Uranium": 3}},
        "Reactivite": {"Chance": 27500, "Multis": {"Starlight": 12, "Ion": 8, "Uranium": 5}},
        "Plutonerite": {"Chance": 125000, "Multis": {"Diamond": 80, "Starlight": 40, "Ion": 20, "Uranium": 10}}
    }
}
stat_gradients = {
    "Gems": {"Colours": ["#f9fb7c", "#fefe01"], "Angle": 180},
    "Cash": {"Colours": ["#55c82f", "#4bb82c"], "Angle": 90},
    "Multiplier": {"Colours": ["#f79292", "#f66161"], "Angle": 90},
    "Rebirths": {"Colours": ["#a39afa", "#7b75e5"], "Angle": 90},
    "Stone": {"Colours": ["#a6a6a6", "8e8e8e"], "Angle": 90},
    "White Gems": {"Colours": ["#e3e3e3", "#d8d8d8"], "Angle": 90},
    "Crystal": {"Colours": ["#5432ae", "#5123bb"], "Angle": 90},
    "Iron": {"Colours": ["#3f3f15", "#3c3c16"], "Angle": 90},
    "Gold": {"Colours": ["#ffff7f", "#fffff8", "#ffff22", "#fffff3", "#fbfb01"], "Angle": 135},
    "Quartz": {"Colours": ["#88f7f9", "#50f9fc", "#caffff"], "Angle": 135},
    "Jade": {"Colours": ["#005500", "#0b9267", "#15807e"], "Angle": 135},
    "Obsidian": {"Colours": ["#000000", "#221313", "#000000"], "Angle": 135},
    "Ruby": {"Colours": ["#ff3c3c", "#f52c2c"], "Angle": 90},
    "Emerald": {"Colours": ["#a1ff73", "#b8f79b", "#abff82"], "Angle": 90},
    "Sapphire": {"Colours": ["#2829ff", "#4647f9"], "Angle": 90},
    "Diamond": {"Colours": ["#00aaff", "#ffffff", "#15b1ff", "#ffffff", "#87d7ff"], "Angle": 90},
    "Starlight": {"Colours": ["#ffff20", "#83ffed", "#ffffff", "#87d7ff"], "Angle": 90},
    "Ion": {"Colours": ["#a2a200", "#000609", "#00476b"], "Angle": 90},
    "Uranium": {"Colours": ["#4fff77", "#03ff05"], "Angle": 90},
    "Bismuth": {"Colours": ["#ffb9b7", "#90ff9a", "#aeccf8"], "Angle": 90},
    "Boracite": {"Colours": ["#00c0ff", "#ffffff", "#00c0ff"], "Angle": 90},
    "Nissonite": {"Colours": ["#aaffff", "#5556ff"], "Angle": 135},
    "Orpiment": {"Colours": ["#cf0000", "#f64100"], "Angle": 90},
    "Tetra": {"Colours": ["#2b747d", "#346ca6"], "Angle": 90},
    "Volt": {"Colours": ["#7d7900", "#fdf500", "#000000"], "Angle": 90},
    "Aquamarine": {"Colours": ["#283d8c", "#0cb668"], "Angle": 90},
    "Lollipop": {"Colours": ["#ffffff", "#ff6868"], "Angle": 90},
    "C0RR8PT10N": {"Colours": ["#7811c7", "#de4530"], "Angle": 180},
    "Stargazed Metal": {"Colours": ["#9c4fbe", "#6b0bf9"], "Angle": 180},
    "Gyge": {"Colours": ["#9c4fbe", "#33220f"], "Angle": 180},
    "Auly Plate": {"Colours": ["#80f2c1", "#ebfbab"], "Angle": 180},
    "Shell Piece": {"Colours": ["#2b2e2f", "#b5b8b8"], "Angle": 180},
    "Singularity": {"Colours": ["#ffffff","#ffffff","#6a6a6a","#000000","#6a6a6a","#ffffff","#6a6a6a","#000000","#6a6a6a","#ffffff","#6a6a6a","#000000","#6a6a6a","#ffffff","#ffffff"], "Angle": 100},
    "Capsuled Singularity": {"Colours": ["#323232", "#323232", "#323232", "#000000", "#9e9e9e", "#ffffff", "#9e9e9e", "#000000", "#323232", "#323232", "#323232"], "Angle": 135},
    "Buttons Pressed": {"Colours": ["#3e87a7", "#1b9fa2"], "Angle": 90},
    "Geodes Opened": {"Colours": ["#bc682d", "#d76d13"], "Angle": 90},
    "Dezyp": {"Colours": ["#333833", "#2e382d"], "Angle": 90},
    "Podrillium": {"Colours": ["#7DDAFF", "#D97652", "#952DD6", "#8BC389", "#EDDD53"], "Angle": 90},
    "Digenite": {"Colours": ["#525742", "#435359"], "Angle": 90},
    "Oneillite": {"Colours": ["#a7fbd7", "#abf7ff", "#b5fbde"], "Angle": 90},
    "Alum": {"Colours": ["#d0d7d7", "#a9aeab"], "Angle": 90},
    "Chaoite": {"Colours": ["#391515", "#291715"], "Angle": 180},
    "Amethyst": {"Colours": ["#5517ff", "#553eff"], "Angle": 90},
    "Paradoxite": {"Colours": ["#5500ff", "#55007f"], "Angle": 135},
    "Silver": {"Colours": ["#eaeaea", "#bfbfbf"], "Angle": 180},
    "Platinum": {"Colours": ["#7b7b7b", "#dbdbdb"], "Angle": 180},
    "Mythril": {"Colours": ["#202dc0", "#57d5f4"], "Angle": 180},
    "Yellow Beryl": {"Colours": ["#76bace", "#dbee35"], "Angle": 180},
    "Opal": {"Colours": ["#ddf490", "#298fff", "#fe00ff", "#acf807"], "Angle": 90},
    "Holeyum": {"Colours": ["#a8ffff", "#56ffff"], "Angle": 180},
    "Pink Quartz": {"Colours": ["#badeff", "#ee79ff"], "Angle": 180},
    "Cyan Quartz": {"Colours": ["#81ffff", "#2cffff"], "Angle": 180},
    "Black Quartz": {"Colours": ["#89cece", "#2c4242"], "Angle": 180},
    "Garnet": {"Colours": ["#e70101", "#b70000"], "Angle": 180},
    "Milky Quartz": {"Colours": ["#f1f1f1", "#272727"], "Angle": 180},
    "Jurite": {"Colours": ["#36aa7f", "#36aa7f"], "Angle": 90},
    "Molybendum": {"Colours": ["#959595", "#192732"], "Angle": 90},
    "Rbadam's Smokestackite": {"Colours": ["#0f0f0f","#173e1e" ,"#1a591b"], "Angle": 170},
    ":3": {"Colours": ["#000000", "#000000"], "Angle": 0},
    "O_O": {"Colours": ["#000000", "#000000"], "Angle": 0},
    "^_^": {"Colours": ["#000000", "#000000"], "Angle": 0},
    "'-'": {"Colours": ["#000000", "#000000"], "Angle": 0},
    ":D": {"Colours": ["#000000", "#000000"], "Angle": 0},
    "OwO": {"Colours": ["#000000", "#000000"], "Angle": 0},
    "UwU": {"Colours": ["#000000", "#000000"], "Angle": 0},
    "Draconite": {"Colours": ["#d943ff", "#740fff"], "Angle": 180},
    "Burneite": {"Colours": ["#f14769", "#b90f17"], "Angle": 180},
    "Dragonglass": {"Colours": ["#550095", "#5401f5"], "Angle": 180},
    "Hellyerite": {"Colours": ["#7bc700", "#f10a02"], "Angle": 180},
    "Palladium": {"Colours": ["#939d6c", "#00ffff"], "Angle": 90},
    "Osumillite": {"Colours": ["#074f0b", "#104d73", "#a40304"], "Angle": 0},
    "Pascoite": {"Colours": ["#f09465", "#ff6417"], "Angle": 180},
    "Roselite": {"Colours": ["#ff8738", "#ff5a31"], "Angle": 180},
    "Wulfenite": {"Colours": ["#ff5300", "#ff0100"], "Angle": 180},
    "Olivine": {"Colours": ["#55f169", "#55be1d"], "Angle": 180},
    "Heazlewoodite": {"Colours": ["#43ff9c", "#0fffe8"], "Angle": 180},
    "Gaspeite": {"Colours": ["#53ac7f", "#01fe7f"], "Angle": 180},
    "Talc": {"Colours": ["#a9fffd", "#56ff81"], "Angle": 180},
    "Lapis": {"Colours": ["#006bcf", "#000e89"], "Angle": 180},
    "Ringwoodite": {"Colours": ["#0ff0de", "#4cff8c"], "Angle": 180},
    "Kyanite": {"Colours": ["#0caaff", "#4caaff"], "Angle": 180},
    "Azurite": {"Colours": ["#5355fc", "#015581"], "Angle": 90},
    "Cobalt": {"Colours": ["#53fcff", "#0258ff"], "Angle": 180},
    "Spatial Dust": {"Colours": ["#baba96", "#46426d"], "Angle": 90},
    "Astrophyllite": {"Colours": ["#2b9cd6", "#5e17fe"], "Angle": 90},
    "Niter": {"Colours": ["#f60986", "#5ca3f9", "#f60986", "#5ca3f9"], "Angle": 180},
    "Yrnote": {"Colours": ["#ffad05", "#fffe7d"], "Angle": 180},
    "Sercense": {"Colours": ["#feabf8", "#fffe03"], "Angle": 180},
    "Neuron": {"Colours": ["#e2c7ff", "#c7e2ff"], "Angle": 90},
    "Antimatter": {"Colours": ["#4d06ff", "#191bff"], "Angle": 90},
    "Sphene": {"Colours": ["#1baaff", "#3baaff"], "Angle": 90},
    "Acid": {"Colours": ["#8ca758", "#7257a8"], "Angle": 90},
    "Niflhemite": {"Colours": ["#61006c", "#c20029"], "Angle": 90},
    "Reactivite": {"Colours": ["#8aff93", "#aeff71"], "Angle": 990},
    "Plutonerite": {"Colours": ["#ff6400", "#fffc00", "#ff5900"], "Angle": 135},
    "Badges": {"Colours":
    ["#b50202",
        "#b50202",
        "#9af119",
        "#ea5bda",
        "#a356ef",
        "#a356ef"],
        "Angle": 9},
    "Default": {"Colours": ["#ffffff", "#ffffff"], "Angle": 0}
}
root.setWindowTitle("BS:ED but bad")
root.setMinimumSize(QSize(100,100))
root.setWindowIcon(QIcon("Quant.png"))
layout = QGridLayout()
central = QWidget()
central.setLayout(layout)
temp = Load()
if temp != None:
   stat_increment = temp
cash = stat_increment['Main']['Cash']['Value']
c_msg = cash if not isinstance(cash, Mantissa) else cash.to_string()
cash_l.setText(f"Cash: {c_msg}")
multi = stat_increment['Main']['Multiplier']['Value']
m_msg = multi if not isinstance(multi, Mantissa) else multi.to_string()
multi_l.setText(f"Multiplier: {m_msg}")
rebirths = stat_increment['Main']['Rebirths']['Value']
re_msg = rebirths if not isinstance(rebirths, Mantissa) else rebirths.to_string()
re_l.setText(f"Rebirths: {re_msg}")
stone_geode = Geode({"Multiplier": {"Chance": 3},
                     "Rebirths": {"Chance": 10},
                     "Stone": {"Chance": 20},
                     #"Mint": 33,
                     "White Gems": {"Chance": 333},
                     "Dezyp": {"Chance": 12000, "Multis": {"Cash": 15, "Rebirths": 20, "Stone": 2, "White Gems": 2}},
                     "Podrillium": {"Chance": 1000000000, "Multis": {"Cash": Mantissa(1,3003), "Multiplier": Mantissa(1,3003), "Rebirths": Mantissa(1,3003), "Stone": Mantissa(1,3003), "White Gems": Mantissa(1,3003), "Crystal": Mantissa(1,303), "Iron": Mantissa(1,303), "Gold": Mantissa(1,303), "Jade": Mantissa(1,303), "Obsidian": 1e200, "Ruby": 1e200, "Emerald": 1e200, "Sapphire": 1e200, "Diamond": 1e100, "Starlight": 1e100, "Ion": 1e100, "Uranium": 1e100, "Bismuth": 1e50, "Boracite": 1e50, "Nissonte": 1e50, "Orpiment": 1e25, "Tetra": 1e20, "Volt": 1e15, "Aquamarine": 1e10, "Lollipop": 10000, "C0RR8PT10N": 10, "Stargazed Metal": 5, "Gyge": 4, "Auly Plate": 3, "Shell Piece": 2}}}, 1e6, "Stone") #Podrillium is real guys!!! Trust!!!
gems_geode = Geode({"Stone": {"Chance": 6},
                    "White Gems": {"Chance": 10},
                    "Crystal": {"Chance": 20},
                    "Gems": {"Chance": 20},
                    "Digenite": {"Chance": 100, "Multis": {"Cash": 4, "Stone": 6}},
                    "Oneillite": {"Chance": 500, "Multis": {"Cash": 15, "Multiplier": 15, "Rebirths": 4, "Stone": 2, "White Gems": 1.25}},
                    "Alum": {"Chance": 13000, "Multis": {"Stone": 12, "White Gems": 1.8, "Crystal": 1.14}},
                    "Chaoite": {"Chance": 273000, "Multis": {"Cash": 6, "Multiplier": 6, "Rebirths": 6, "Stone": 6, "White Gems": 6, "Crystal": 6, "Iron": 6}},
                    #"Starglass": {"Chance": 929221841},
                    "Shell Piece": {"Chance": 1650000000}}, 30, "White Gems")
crystal_geode = Geode({"White Gems": {"Chance": 4},
                       "Stone": {"Chance": 5},
                       "Crystal": {"Chance": 33},
                       "Amethyst": {"Chance": 333, "Multis": {"Stone": 6, "White Gems": 4, "Crystal": 3}},
                       "Iron": {"Chance": 1162},
                       "Paradoxite": {"Chance": 65000, "Multis": {"Cash": 44, "Multipliers": 55, "Rebirths": 66, "Stone": 77, "White Gems": 88, "Crystal": 30, "Iron": 5}}},
                       100, "Crystal")
iron_geode = Geode({"Iron": {"Chance": 5},
                    "Crystal": {"Chance": 10},
                    "White Gems": {"Chance": 20},
                    "Gems": {"Chance": 25},
                    #"Event Power": {"Chance": 33},
                    "Silver": {"Chance": 142, "Multis": {"Multiplier": 10, "White Gems": 5, "Iron": 2}},
                    "Platinum": {"Chance": 32000, "Multis": {"White Gems": 10, "Crystal": 20, "Iron": 15, "Gold": 3, "Quartz": 2}},
                    "Mythril": {"Chance": 2000000, "Multis": {"Cash": 999, "Crystal": 5, "Iron": 10, "Gold": 50, "Quartz": 100}}},
                    25, "Iron")
gold_geode = Geode({"Gold": {"Chance": 4},
                    "Iron": {"Chance": 6},
                    "Quartz": {"Chance": 33},
                    #"Mushroom": {"Chance": 100},
                    #"Pumpkin" {"Chance": 125},
                    "Yellow Beryl": {"Chance": 6666, "Multis": {"Crystal": 15, "Gold": 3}},
                    "Opal": {"Chance": 51000, "Multis": {"Cash": 8, "Multiplier": 8, "Rebirths": 8, "Crystal": 8, "Gold": 8, "Jade": 8, "Ruby": 1.3, "Sapphire": 1.3, "Diamond": 1.3}},
                    "Holeyum": {"Chance": 2750000, "Multis": {"Rebirths": 1000, "White Gems": 1000, "Crystal": 500, "Iron": 500, "Gold": 300}}},
                    60, "Gold")
quartz_geode = Geode({"Quartz": {"Chance": 5},
                      "Gold": {"Chance": 8},
                      "Jade": {"Chance": 16},
                      "Pink Quartz": {"Chance": 50, "Multis": {"Crystal": 10, "Quartz": 3}},
                      "Cyan Quartz": {"Chance": 166, "Multis": {"Rebirths": 10, "Crystal": 10, "Quartz": 4}},
                      "Black Quartz": {"Chance": 2500, "Multis": {"Stone": 10, "White Gems": 10, "Iron": 10, "Quartz": 5}},
                      "Garnet": {"Chance": 23000, "Multis": {"Gold": 30, "Quartz": 15, "Jade": 10, "Obsidian": 5}},
                      "Milky Quartz": {"Chance": 800000, "Multis": {"Cash": 10, "Multiplier": 10, "Rebirths": 10, "Stone": 100, "White Gems": 100, "Crystal": 10, "Iron": 100, "Gold": 10, "Quartz": 100, "Jade": 10, "Obsidian": 100}}},
                      30, "Quartz")
jade_geode = Geode({"Gold": {"Chance": 2},
                    "Quartz": {"Chance": 4},
                    "Jade": {"Chance": 10},
                    "Jurite": {"Chance": 20, "Multis": {"Iron": 3, "Gold": 3, "Quartz": 3, "Jade": 3}},
                    "Obsidian": {"Chance": 1000},
                    "Molybendum": {"Chance": 23000, "Multis": {"Stone": 1000, "White Gems": 1000, "Iron": 1000, "Quartz": 1000}},
                    "Rbadam's Smokestackite": {"Chance": 100000, "Multis": {"Gold": 44,"Quartz": 33," Jade": 22, "Obsidian": 11, "Ruby": 1.1}}},
                    500, "Jade")
emoji_geode = Geode({":3": {"Chance": 2, "Multis": {"Quartz": 2}},
                     "O_O": {"Chance": 100, "Multis": {"Quartz": 5, "Jade": 2}},
                     "^_^": {"Chance": 2000, "Multis": {"Multiplier": 1.1, "Rebirths": 2.2, "Stone": 3.3, "White Gems": 4.4, "Crystal": 5.5, "Iron": 6.6, "Gold": 7.7, "Quartz": 8.8}},
                     "'-'": {"Chance": 12000, "Multis": {"Iron": 1.1, "Gold": 1.1, "Quartz": 1.1, "Jade": 1.1, "Obsidian": 1.1}},
                     ":D": {"Chance": 35000, "Multis": {"Jade": 5, "Obsidian": 3, "Ruby": 2}},
                     "OwO": {"Chance": 150000, "Multis": {"Gold": 5.5, "Emerald": 5.5}},
                     "UwU": {"Chance": 1000000, "Multis": {"Gold": 6.5, "Quartz": 6.5, "Jade": 6.5, "Obsidian": 6.5, "Ruby": 5.4, "Emerald": 4.3, "Sapphire": 3.2, "Diamond": 2.1}}},
                     1000, "Gems")
obsidian_geode = Geode({"Obsidian": {"Chance": 5},
                        "Jade": {"Chance": 10},
                        "Ruby": {"Chance": 20},
                        "Draconite": {"Chance": 100, "Multis": {"Crystal": 10, "Obsidian": 2}},
                        "Burneite": {"Chance": 400, "Multis": {"Cash": 7, "Multiplier": 7, "Rebirths": 7, "Stone": 7, "White Gems": 7, "Crystal": 7, "Iron": 7, "Gold": 7, "Quartz": 7, "Jade": 7}},
                        "Dragonglass": {"Chance": 6666, "Multis": {"Crystal": 25, "Quartz": 15, "Jade": 10, "Obsidian": 5}},
                        "Hellyerite": {"Chance": 47000, "Multis": {"Obsidian": 10, "Ruby": 3}},
                        "Palladium": {"Chance": 350000, "Multis": {"Cash": 6, "Multiplier": 6, "Rebirths": 6, "Stone": 6, "White Gems": 6, "Crystal": 6, "Iron": 6, "Gold": 6, "Jade": 6, "Obsidian": 6, "Ruby": 6, "Gems": 1.5}},
                        "Osumillite": {"Chance": 4200000, "Multipliers": {"Cash": 6544, "Gold": 50, "Quartz": 40, "Jade": 30, "Obsidian": 20, "Ruby": 10}}},
                        1, "Obsidian")
ruby_geode = Geode({"Ruby": {"Chance": 5},
                    "Emerald": {"Chance": 10},
                    "Sapphire": {"Chance": 20},
                    "Pascoite": {"Chance": 666, "Multis": {"Obsidian": 3, "Ruby": 2}},
                    "Roselite": {"Chance": 3333, "Multis": {"Jade": 5, "Obsidian": 5, "Ruby": 3}},
                    "Wulfenite": {"Chance": 50000, "Multis": {"Multiplier": 15, "Obsidian": 15, "Ruby": 8}}},
                    100000, "Ruby")
emerald_geode = Geode({"Emerald": {"Chance": 5},
                       "Ruby": {"Chance": 10},
                       "Sapphire": {"Chance": 20},
                       "Olivine": {"Chance": 250, "Multis": {"Ruby": 3, "Emerald": 2}},
                       "Heazlewoodite": {"Chance": 4000, "Multis": {"Obsidian": 5, "Ruby": 5, "Emerald": 3}},
                       "Gaspeite": {"Chance": 35000, "Multis": {"Emerald": 15}},
                       "Talc": {"Chance": 230000, "Multis": {"Cash": 15, "Jade": 15, "Emerald": 15}}},
                        100000, "Emerald")
sapphire_geode = Geode({"Sapphire": {"Chance": 5},
                        "Emerald": {"Chance": 10},
                        "Ruby": {"Chance": 20},
                        "Lapis": {"Chance": 142, "Multis": {"Emerald": 3, "Sapphire": 2}},
                        "Ringwoodite": {"Chance": 2000, "Multis": {"Ruby": 5, "Emerald": 5, "Sapphire": 3}},
                        "Kyanite": {"Chance": 15000, "Multis": {"Sapphire": 15}},
                        "Azurite": {"Chance": 85000, "Multis": {"Rebirths": 15, "Crystal": 15, "Quartz": 15 ,"Sapphire": 8}},
                        "Cobalt": {"Chance": 3000000, "Multis": {"Cash": 20, "Multiplier": 20, "Rebirths": 20, "Crystal": 20, "Gold": 20, "Quartz": 20, "Jade": 20, "Ruby": 20, "Emerald": 20, "Sapphire": 20}}},
                        100000, "Sapphire")
diamond_geode = Geode({"Sapphire": {"Chance": 3},
                       "Emerald": {"Chance": 3},
                       "Ruby": {"Chance": 3},
                       "Spatial Dust": {"Chance": 20, "Multis": {"Ruby": 3, "Emerald": 3, "Sapphire": 3, "Diamond": 4, "Starlight": 2}},
                       "Starlight": {"Chance": 1666},
                       "Astrophyllite": {"Chance": 71000, "Multis": {"Gold": 80, "Jade": 30, "Obsidan": 12, "Ruby": 52, "Diamond": 20, "Starlight": 25}}},
                       2500, "Diamond")
starlight_geode = Geode({"Starlight": {"Chance": 5},
                         "Diamond": {"Chance": 10},
                         "Sapphire": {"Chance": 20},
                         "Ion": {"Chance": 333},
                         "Niter": {"Chance": 4000, "Multis": {"Starlight": 5}},
                         "Yrnote": {"Chance": 80000, "Multis": {"Ruby": 10, "Emerald": 10, "Sapphire": 10, "Diamond": 20, "Starlight": 15}},
                         "Sercense": {"Chance": 1400000, "Multis": {"Cash": 300, "Multiplier": 300, "Rebirths": 300, "Stone": 290, "White Gems": 280, "Crystal": 270, "Iron": 260, "Gold": 130, "Quartz": 120, "Jade": 110, "Obsidian": 100, "Ruby": 50, "Emerald": 40, "Sapphire": 30, "Diamond": 20, "Starlight": 10}}},
                         60, "Starlight")
ion_geode = Geode({"Diamond": {"Chance": 2},
                   "Starlight": {"Chance": 4},
                   "Ion": {"Chance": 10},
                   "Neuron": {"Chance": 20, "Multis": {"Starlight": 5, "Ion": 2}},
                   "Uranium": {"Chance": 4000},
                   "Antimatter": {"Chance": 45000, "Multis": {"Rebirths": 10, "Gold": 10, "Quartz": 10, "Sapphire": 10, "Diamond": 10, "Starlight": 10, "Ion": 10}}},
                   5, "Ion")
uranium_geode = Geode({"Sphene": {"Chance": 3, "Multis": {"Diamond": 5}},
                       "Uranium": {"Chance": 5},
                       "Acid": {"Chance": 20, "Multis": {"Uranium": 1.4, "Starlight": 2}},
                       "Niflhemite": {"Chance": 100, "Multis": {"Multiplier": 3, "Rebirths": 3, "White Gems": 3, "Quartz": 3, "Obsidian": 3, "Ruby": 3, "Diamond": 3, "Uranium": 3}},
                       "Bismuth": {"Chance": 666},
                       "Reactivite": {"Chance": 27500, "Multis": {"Starlight": 12, "Ion": 8, "Uranium": 5}},
                       "Plutonerite": {"Chance": 125000, "Multis": {"Diamond": 80, "Starlight": 40, "Ion": 20, "Uranium": 10}}},
                      12, "Uranium")
Spawn_Buttons = {
    "Multiplier": [
        ("12 Cash: 1 Multiplier", lambda: cost_button("Main","Cash",12,"Multiplier", 1)),
        ("50 Cash: 3 Multiplier", lambda: cost_button("Main","Cash",50,"Multiplier", 3)),
        ("100 Cash: 5 Multiplier", lambda: cost_button("Main","Cash",100,"Multiplier", 5)),
        ("500 Cash: 10 Multiplier", lambda: cost_button("Main","Cash",500,"Multiplier", 10)),
        ("10k Cash: 45 Multiplier", lambda: cost_button("Main","Cash",1e4,"Multiplier", 45)),
        ("75k Cash: 100 Multiplier", lambda: cost_button("Main","Cash",7.5e4,"Multiplier", 100)),
        ("1M Cash: 300 Multiplier", lambda: cost_button("Main","Cash",1e6,"Multiplier", 300)),
        ("30M Cash: 500 Multiplier", lambda: cost_button("Main","Cash",3e7,"Multiplier", 500)),
        ("100M Cash: 1k Multiplier", lambda: cost_button("Main","Cash",1e8,"Multiplier", 1e3)),
        ("1B Cash: 5k Multiplier", lambda: cost_button("Main","Cash",1e9,"Multiplier", 5e3)),
        ("5B Cash: 20k Multiplier", lambda: cost_button("Main","Cash",5e9,"Multiplier", 2e4)),
        ("30B Cash: 60k Multiplier", lambda: cost_button("Main","Cash",3e10,"Multiplier", 6e4)),
        ("200B Cash: 120k Multiplier", lambda: cost_button("Main","Cash",2e11,"Multiplier", 1.2e5)),
        ("700B Cash: 300k Multiplier", lambda: cost_button("Main","Cash",7e11,"Multiplier", 3e5)),
        ("3T Cash: 1M Multiplier", lambda: cost_button("Main","Cash",3e12,"Multiplier", 1e6)),
        ("10T Cash: 4M Multiplier", lambda: cost_button("Main","Cash",1e13,"Multiplier", 4e6)),
        ("50T Cash: 10M Multiplier", lambda: cost_button("Main","Cash",5e13,"Multiplier", 1e7)),
        ("120T Cash: 50M Multiplier", lambda: cost_button("Main","Cash",1.2e14,"Multiplier", 5e7)),
        ("400T Cash: 80M Multiplier", lambda: cost_button("Main","Cash",4e14,"Multiplier", 8e7)),
        ("1Qd Cash: 200M Multiplier", lambda: cost_button("Main","Cash",1e15,"Multiplier", 2e8)),
        ("5Qd Cash: 1B Multiplier", lambda: cost_button("Main","Cash",5e15,"Multiplier", 1e9)),
        ("25Qd Cash: 4B Multiplier", lambda: cost_button("Main","Cash",2.5e16,"Multiplier", 4e9)),
        ("100Qd Cash: 10B Multiplier", lambda: cost_button("Main","Cash",1e17,"Multiplier", 1e10))
    ],
    "Rebirths": [
        ("2k Multiplier: 1 Rebirths", lambda: reset_button("Main",2000,"Multiplier",1, "Rebirths")),
        ("15k Multiplier: 5 Rebirths", lambda: reset_button("Main",15000,"Multiplier",5, "Rebirths")),
        ("600k Multiplier: 23 Rebirths", lambda: reset_button("Main",6e5,"Multiplier",23, "Rebirths")),
        ("12M Multiplier: 69 Rebirths", lambda: reset_button("Main",1.2e7,"Multiplier",69, "Rebirths")),
        ("700M Multiplier: 272 Rebirths", lambda: reset_button("Main",7e8,"Multiplier",272, "Rebirths")),
        ("3B Multiplier: 1k Rebirths", lambda: reset_button("Main",3e9,"Multiplier",1000, "Rebirths")),
        ("15B Multiplier: 5k Rebirths", lambda: reset_button("Main",1.5e10,"Multiplier",5000, "Rebirths")),
        ("50B Multiplier: 20k Rebirths", lambda: reset_button("Main",5e10,"Multiplier",20000, "Rebirths")),
        ("600B Multiplier: 50k Rebirths", lambda: reset_button("Main",6e11,"Multiplier",5e4, "Rebirths")),
        ("1T Multiplier: 100k Rebirths", lambda: reset_button("Main",1e12,"Multiplier",1e5, "Rebirths")),
        ("75T Multiplier: 500k Rebirths", lambda: reset_button("Main",7.5e13,"Multiplier",5e5, "Rebirths")),
        ("400T Multiplier: 1M Rebirths", lambda: reset_button("Main",4e14,"Multiplier",1e6, "Rebirths")),
        ("2Qd Multiplier: 6M Rebirths", lambda: reset_button("Main",2e15,"Multiplier",6e6, "Rebirths")),
        ("15Qd Multiplier: 30M Rebirths", lambda: reset_button("Main",1.5e16,"Multiplier",3e7, "Rebirths")),
        ("50Qd Multiplier: 100M Rebirths", lambda: reset_button("Main",5e16,"Multiplier",1e8, "Rebirths")),
    ],
    "Stone": [
        ("30k Rebirths: 1 Stone", lambda: reset_button("Main",30000, "Rebirths", 1, "Stone")),
        ("30M Rebirths: 3 Stone", lambda: reset_button("Main",3e7, "Rebirths", 3, "Stone")),
        ("600M Rebirths: 6 Stone", lambda: reset_button("Main",6e8, "Rebirths", 6, "Stone")),
    ],
    "Recovery": [
       ("15 Stone: 15Qn Cash (Sets)", lambda: recovery_button_set("Main",15, "Stone", 5e19, "Cash")),
       ("7 Iron: 1e40 Cash (Sets)", lambda: recovery_button_set("Main",7, "Iron", 1e40, "Cash")),
       ("1 Gold: 6e41 Multiplier (Fetch)", lambda: recovery_button_fetch("Main",1, "Gold", 6e41, "Multiplier")),
       ("2 Gold: 1Sp Rebirths (Fetch)", lambda: recovery_button_fetch("Main",2, "Gold", 1e24, "Rebirths")),
       ("1 Obsidian: 25 Quartz (Sets)", lambda: recovery_button_set("Main",1, "Obsidian", 25, "Quartz")),
       ("2 Ion: 1 Sapphire (Fetch)", lambda: recovery_button_fetch("Main",2, "Ion", 1, "Sapphire")),
    ],
    "Geodes": [
       ("Stone Geode: 1M Stone", lambda btn: Geode_roll(btn, stone_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
       ("White Gems Geode: 30 White Gems", lambda btn: Geode_roll(btn, gems_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
       ("Jade Geode: 500 Jade", lambda btn: Geode_roll(btn, jade_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
       ("Uranium Geode: 12 Uranium", lambda btn: Geode_roll(btn, uranium_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
    ],
    "Area Teleports": [
       ("Caves (req: 10 Stone)", lambda: load_check("Main",10, "Stone", Cave_Buttons)),
       ("Crystal Beneaths (req: 300 White Gems)", lambda: load_check("Main",300, "White Gems", Crystal_Buttons)),
       ("Iron Shafts (req: 100 Crystal)", lambda: load_check("Main",100, "Crystal", Iron_Buttons)),
       ("Golden Quarry (req: 750 Iron)", lambda: load_check("Main",750,"Iron",Gold_Buttons)),
       ("Quartz Walkway (req: 75 Gold)", lambda: load_check("Main",75,"Gold", Quartz_Buttons)),
       ("Jade Forest (req: 450 Quartz)", lambda: load_check("Main",450,"Quartz", Jade_Buttons)),
       ("Obsidian Abyss (req: 80 Jade)", lambda: load_check("Main", 80, "Jade", Obsidian_Buttons)),
       ("Colour Temple (req: 5 Obsidian)", lambda: load_check("Main", 5, "Obsidian", Colour_Buttons)),
       ("Extraterrestrial Orbits (req: 50k Sapphire)", lambda: load_check("Main", 5e4, "Sapphire", ET_Buttons)),
       ("Empyrean Island (req: 100 Starlight)", lambda: load_check("Main", 100, "Starlight", Ion_Buttons)),
       ("Recover Hall (req: 0 Cash)", lambda: load_check("Main",0, "Cash", Recover_Hall_Buttons))
   ]
}
Cave_Buttons = {
    "Multiplier": [
        ("620Sp Cash: 1Qd Multiplier", lambda: cost_button("Main","Cash", 6.2e26, "Multiplier", 1e15)),
        ("3.5Oc Cash: 6Qd Multiplier", lambda: cost_button("Main","Cash", 3.5e27,"Multiplier", 6e15)),
        ("60Oc Cash: 50Qd Multiplier", lambda: cost_button("Main","Cash", 6e28, "Multiplier", 5e16)),
        ("450Oc Cash: 230Qd Multiplier", lambda: cost_button("Main","Cash", 4.5e29, "Multiplier", 2.3e17)),
        ("3No Cash: 1Qn Multiplier", lambda: cost_button("Main","Cash", 3e30,"Multiplier", 1e18)),
        ("100No Cash: 5Qn Multiplier", lambda: cost_button("Main","Cash",1e32,"Multiplier", 5e18)),
        ("800No Cash: 30Qn Multiplier", lambda: cost_button("Main","Cash",8e32,"Multiplier", 3e19)),
        ("8De Cash: 240Qn Multiplier", lambda: cost_button("Main","Cash",8e33,"Multiplier", 2.4e20)),
        ("90De Cash: 800Qn Multiplier", lambda: cost_button("Main","Cash",8e34,"Multiplier", 8e20)),
        ("500De Cash: 3Sx Multiplier", lambda: cost_button("Main","Cash",5e35,"Multiplier", 3e21)),
        ("1.2e36 Cash: 13Sx Multiplier", lambda: cost_button("Main","Cash",1.2e36,"Multiplier", 1.3e22)),
        ("4.2e37 Cash: 40Sx Multiplier", lambda: cost_button("Main","Cash",4.2e37,"Multiplier", 4e22)),
        ("3.25e38 Cash: 100Sx Multiplier", lambda: cost_button("Main","Cash",3.25e38,"Multiplier", 1e23)),
        ("1e39 Cash: 400Sx Multiplier", lambda: cost_button("Main","Cash",1e39,"Multiplier", 4e23)),
        ("3.5e40 Cash: 800Sx Multiplier", lambda: cost_button("Main","Cash",3.5e40,"Multiplier", 8e23)),
        ("5.05e41 Cash: 3Sp Multiplier", lambda: cost_button("Main","Cash",5.05e41,"Multiplier", 3e24)),
        ("2e42 Cash: 20Sp Multiplier", lambda: cost_button("Main","Cash",2e42,"Multiplier", 2e25)),
        ("7.5e43 Cash: 60Sp Multiplier", lambda: cost_button("Main","Cash", 7.5e43,"Multiplier", 6e25)),
        ("3.5e44 Cash: 200Sp Multiplier", lambda: cost_button("Main","Cash",3.5e44,"Multiplier", 2e26)),
        ("8.5e44 Cash: 500Sp Multiplier", lambda: cost_button("Main","Cash",8.5e44,"Multiplier", 5e26)),
        ("5e45 Cash: 1.2Oc Multiplier", lambda: cost_button("Main","Cash",5e45,"Multiplier", 1.2e27)),
        ("6.2e46 Cash: 3Oc Multiplier", lambda: cost_button("Main","Cash",6.2e46,"Multiplier", 3e27)),
    ],
    "Rebirths": [
        ("30Qn Multiplier: 1B Rebirths", lambda: reset_button("Main",3e19,"Multiplier",1e9, "Rebirths")),
        ("900Qn Multiplier: 10B Rebirths", lambda: reset_button("Main",9e20,"Multiplier",1e10, "Rebirths")),
        ("60Sx Multiplier: 80B Rebirths", lambda: reset_button("Main",6e22,"Multiplier",8e10, "Rebirths")),
        ("800Sx Multiplier: 150B Rebirths", lambda: reset_button("Main",8e23,"Multiplier",1.5e11, "Rebirths")),
        ("90Sp Multiplier: 500B Rebirths", lambda: reset_button("Main",9e25,"Multiplier",5e11, "Rebirths")),
        ("1Oc Multiplier: 10T Rebirths", lambda: reset_button("Main",1e27,"Multiplier",1e13, "Rebirths")),
        ("750Oc Multiplier: 70T Rebirths", lambda: reset_button("Main",7.5e29,"Multiplier",7e13, "Rebirths")),
        ("15No Multiplier: 300T Rebirths", lambda: reset_button("Main",1.5e31,"Multiplier",3e14, "Rebirths")),
        ("600No Multiplier: 2Qd Rebirths", lambda: reset_button("Main",6e32,"Multiplier",2e15, "Rebirths")),
        ("50De Multiplier: 15Qd Rebirths", lambda: reset_button("Main",5e34,"Multiplier",1.5e16, "Rebirths")),
        ("1e36 Multiplier: 200Qd Rebirths", lambda: reset_button("Main",1e36,"Multiplier",2e17, "Rebirths")),
        ("4e38 Multiplier: 1Qn Rebirths", lambda: reset_button("Main",4e38,"Multiplier",1e18, "Rebirths")),
        ("1.5e40 Multiplier: 40Qn Rebirths", lambda: reset_button("Main",1.5e40,"Multiplier", 4e19, "Rebirths")),
        ("1e42 Multiplier: 300Qn Rebirths", lambda: reset_button("Main",1e42,"Multiplier",3e20, "Rebirths")),
        ("1.5e45 Multiplier: 5Sx Rebirths", lambda: reset_button("Main",1.5e45,"Multiplier",5e21, "Rebirths")),
    ],
    "Stone": [
        ("250B Rebirths: 26 Stone", lambda: reset_button("Main",2.5e11, "Rebirths", 26, "Stone")),
        ("1Qd Rebirths: 120 Stone", lambda: reset_button("Main",1e15, "Rebirths", 120, "Stone")),
        ("700Qd Rebirths: 450 Stone", lambda: reset_button("Main",7e17, "Rebirths", 450, "Stone")),
        ("650Qn Rebirths: 5k Stone", lambda: reset_button("Main",6.5e20, "Rebirths", 5000, "Stone")),
        ("1Sp Rebirths: 15k Stone", lambda: reset_button("Main",1e15, "Rebirths", 15000, "Stone")),
        ("80Oc Rebirths: 32k Stone", lambda: reset_button("Main",8e19, "Rebirths", 32000, "Stone")),
        ("700Oc Rebirths: 85k Stone", lambda: reset_button("Main",7e20, "Rebirths", 85000, "Stone")),
        ("3No Rebirths: 300k Stone", lambda: reset_button("Main",3e21, "Rebirths", 3e5, "Stone")),
        ("24No Rebirths: 1M Stone", lambda: reset_button("Main",2.4e22, "Rebirths", 1e6, "Stone")),
    ],
    "White Gems": [
        ("5k Stone: 1 White Gems", lambda: reset_button("Main",5000, "Stone", 1, "White Gems")),
        ("60k Stone: 3 White Gems", lambda: reset_button("Main",60000, "Stone", 3, "White Gems")),
        ("500k Stone: 10 White Gems", lambda: reset_button("Main",500000, "Stone", 10, "White Gems")),
        ("10M Stone: 30 White Gems", lambda: reset_button("Main",1e7, "Stone", 30, "White Gems")),
        ("200M Stone: 86 White Gems", lambda: reset_button("Main",2e8, "Stone", 86, "White Gems")),
    ],
    "Gem Buttons": [
        ("50 White Gems: 1 Gems", lambda: cost_button("Main","White Gems", 50, "Gems", 1)),
        ("500 White Gems: 5 Gems", lambda: cost_button("Main","White Gems", 500, "Gems", 5)),
        ("3k White Gems: 10 Gems", lambda: cost_button("Main","White Gems", 3000, "Gems", 10)),
    ],
    "Recovery": [
       ("5 White Gems: 100k Rebirths (Fetch)", lambda: recovery_button_fetch("Main",5, "White Gems", 100000, "Rebirths")),
       ("50 Gems: 5T Multiplier (Fetch)", lambda: recovery_button_fetch("Main",50, "Gems", 5e12, "Multiplier")),
       ("3 Gold: 1M Stone (Fetch)", lambda: recovery_button_fetch("Main",3, "Gold", 1e6, "Stone")),
    ],
    "Area Teleports": [
       ("Crystal Beneaths (req: 300 White Gems)", lambda: load_check("Main",300, "White Gems", Crystal_Buttons)),
       ("Spawn (req: 0 Cash)", lambda: load_check("Main",0, "Cash", Spawn_Buttons)),
       ("Recover Hall (req: 0 Cash)", lambda: load_check("Main",0, "Cash", Recover_Hall_Buttons))
    ]
}
Recover_Hall_Buttons = {
    "Spawn": [
       ("15 Stone: 15Qn Cash (Sets)", lambda: recovery_button_set("Main",15, "Stone", 5e19, "Cash")),
       ("7 Iron: 1e40 Cash (Sets)", lambda: recovery_button_set("Main",7, "Iron", 1e40, "Cash")),
       ("1 Gold: 6e41 Multiplier (Fetch)", lambda: recovery_button_fetch("Main",1, "Gold", 6e41, "Multiplier")),
       ("2 Gold: 1Sp Rebirths (Fetch)", lambda: recovery_button_fetch("Main",2, "Gold", 1e24, "Rebirths")),
       ("1 Obsidian: 25 Quartz (Sets)", lambda: recovery_button_set("Main",1, "Obsidian", 25, "Quartz")),
       ("2 Ion: 1 Sapphire (Fetch)", lambda: recovery_button_fetch("Main",2, "Ion", 1, "Sapphire")),                
    ],
    "Caves": [
       ("5 White Gems: 100k Rebirths (Fetch)", lambda: recovery_button_fetch("Main",5, "White Gems", 100000, "Rebirths")),
       ("50 Gems: 5T Multiplier (Fetch)", lambda: recovery_button_fetch("Main",50, "Gems", 5e12, "Multiplier")),
    ],
    "Crystal Beneaths": [
       ("500 White Gems: 12Qn Multiplier (Fetch)", lambda: recovery_button_fetch("Main",500, "White Gems", 1.2e19, "Multiplier")),
       ("150B Stone: 3M Rebirths (Fetch)", lambda: recovery_button_fetch("Main",1.5e11, "Stone", 3e6, "Rebirths")),  
       ("3 Crystal: 200 Stone (Fetch)", lambda: recovery_button_fetch("Main",3, "Crystal", 200, "Stone")),
       ("5 Crystal: 200 White Gems (Sets)", lambda: recovery_button_set("Main",5, "Crystal", 200, "White Gems")),      
    ],
    "Iron Shafts": [
        ("1k Crystal: 500Qn Rebirths (Fetch)", lambda: recovery_button_fetch("Main",1000, "Crystal", 5e20, "Rebirths")),
        ("150B White Gems: 10k Stone (Fetch)", lambda: recovery_button_fetch("Main",1.5e14, "White Gems", 1e4, "Stone")),
        ("3 Iron: 10 White Gems (Fetch)", lambda: recovery_button_fetch("Main",3, "Iron", 10, "White Gems")),
        ("50k Gems: 70 Crystal", lambda: cost_button("Main","Gems", 5e4, "Crystal", 70)),
    ],
    "Gold Quarry": [
        ("3 Gold: 1M Stone (Fetch)", lambda: recovery_button_fetch("Main",3, "Gold", 1e6, "Stone")),
        ("4 Gold: 500 White Gems (Fetch)", lambda: recovery_button_fetch("Main",4, "Gold", 500, "White Gems")),
    ],
    "Quartz Walkway": [
        ("7k Gems: 1e45 Multiplier (Fetch)", lambda: recovery_button_fetch("Main",7000, "Gems", 1e45, "Multiplier")),
        ("1k Gold: 5M White Gems (Fetch)", lambda: recovery_button_fetch("Main",1000, "Gold", 5e6, "White Gems")),
        ("15 Quartz: 100 Iron (Fetch)", lambda: recovery_button_fetch("Main",15, "Quartz", 100, "Iron")),
        ("1 Quartz: 1B Crystal (Sets)", lambda: recovery_button_set("Main",1, "Quartz", 1e9, "Crystal")),
    ],
    "Jade Forest": [
        ("300 Quartz: 1e67 Rebirths (Fetch)", lambda: recovery_button_fetch("Main",300, "Quartz", 1e67, "Rebirths")),
        ("1M Gold: 1No Stone (Fetch)", lambda: recovery_button_fetch("Main",1e6, "Gold", 1e30, "Stone")),
        ("2 Jade: 15Sx Crystal (Fetch)", lambda: recovery_button_fetch("Main",2, "Jade", 1.5e22, "Crystal")),
        ("1 Jade: 10 Gold (Sets)", lambda: recovery_button_set("Main",1, "Jade", 10, "Gold")),
    ],
    "Obsidian Abyss": [
        ("1Qd Quartz: 1e303 Rebirths (Fetch)", lambda: recovery_button_fetch("Main",1e15, "Quartz", Mantissa(1,303), "Rebirths")),
        ("100 Jade: 5.2T White Gems (Fetch)", lambda: recovery_button_fetch("Main",100, "Jade", 5.2e12, "White Gems")),
        ("1M Jade: 1Qn Iron (Fetch)", lambda: recovery_button_fetch("Main",1e6, "Jade", 1e18, "Iron")),
        ("6 Obsidian: 5 Quartz (Fetch)", lambda: recovery_button_fetch("Main",6, "Obsidian", 5, "Quartz")),
        ("2 Obsidian: 3 Jade (Sets)", lambda: recovery_button_set("Main",2, "Obsidian", 3, "Jade")),
    ],
    "Colour Temple": [
        ("1 Ruby: 10 Quartz (Fetch)", lambda: recovery_button_fetch("Main",1, "Ruby", 10, "Quartz")),
        ("200 Ruby: 1Oc Gold (Fetch)", lambda: recovery_button_fetch("Main",200, "Ruby", 1e27, "Gold")),
        ("50 Emerald: 1e444 Rebirths (Fetch)", lambda: recovery_button_fetch("Main",50, "Emerald", Mantissa(1,444), "Rebirths")), 
        ("10 Obsidian: 500 Jade (Sets)", lambda: recovery_button_set("Main",10, "Obsidian", 500, "Jade")),
        ("1 Sapphire: 10 Ruby (Sets)", lambda: recovery_button_set("Main",1, "Sapphire", 10, "Ruby")),
    ],
    "Extraterrestrial Orbits": [
        ("1 Ruby: 50 Jade (Fetch)", lambda: recovery_button_fetch("Main",1, "Ruby", 50, "Jade")),
        ("1 Diamond: 5 Obsidian (Sets)", lambda: recovery_button_set("Main",1, "Diamond", 5, "Obsidian")),
        ("1 Starlight: 25 Obsidian (Sets)", lambda: recovery_button_set("Main",1, "Starlight", 25, "Obsidian")),
    ],
    "Empyrean Island": [
        ("10k Diamond: 1e650 Crystal (Sets)", lambda: recovery_button_set("Main",1e4, "Diamond", Mantissa(1,650), "Crystal")),
        ("500 Starlight: 15 Ruby (Fetch)", lambda: recovery_button_fetch("Main",500, "Starlight", 15, "Ruby")),
        ("400B Gems: 1 Diamond (Sets)", lambda: recovery_button_set("Main",4e11, "Gems", 1, "Diamond")),
        ("3 Ion: 1 Starlight (Sets)", lambda: recovery_button_set("Main",3, "Ion", 1, "Starlight")),
    ],
    "Uranium Wastelands": [
        ("100 Ion: 1e2000 Multiplier (Fetch)", lambda: recovery_button_fetch("Main",100, "Ion", Mantissa(1,2000), "Multiplier")),
        ("1T Gems: 1e45 Obsidian (Sets)", lambda: recovery_button_set("Main",1e12, "Gems", 1e45, "Obsidian")),
        ("1M Starlight: 1No Sapphire (Sets)", lambda: recovery_button_set("Main",1e6, "Starlight", 1e30, "Sapphire")),
        ("1 Uranium: 25 Diamond (Sets)", lambda: recovery_button_set("Main",1, "Uranium", 25, "Diamond")),
        ("3 Uranium: 1 Ion (Sets)", lambda: recovery_button_set("Main",3, "Uranium", 1, "Ion")),
    ],
    "Smooth Depths": [
        ("1 Bismuth: 800 Diamond (Fetch)", lambda: recovery_button_fetch("Main",1, "Bismuth", 600, "Diamond")),
    ],
    "Icy Palace": [
        ("3 Boracite: 200 Ion (Fetch)", lambda: recovery_button_fetch("Main",3, "Boracite", 200, "Ion")),
        ("1 Nissonite: 10 Bismuth (Sets)", lambda: recovery_button_set("Main",1, "Nissonite", 10, "Bismuth")),
    ],
    "Floating Purgatory": [
        ("666 Nissonite: 1k Uranium (Fetch)", lambda: recovery_button_fetch("Main",666, "Nissonite", 1000, "Uranium")),
        ("1 Orpiment: 60 Boracite (Sets)", lambda: recovery_button_set("Main",1, "Orpiment", 60, "Boracite")),
    ],
    "Tetratum": [
        ("10k Orpiment: 1k Bismuth (Fetch)", lambda: recovery_button_fetch("Main",1e4, "Orpiment", 1000, "Bismuth")),
        ("1 Tetra: 1k Boracite (Sets)", lambda: recovery_button_set("Main",1, "Tetra", 1000, "Boracite")),
        ("3 Tetra: 1 Orpiment (Sets)", lambda: recovery_button_set("Main",3, "Tetra", 1, "Orpiment")),
    ],
    "Voltiac Sector": [
        ("1Sp Nissonite: 1e33 Uranium (Fetch)", lambda: recovery_button_fetch("Main",1e24, "Nissonite", 1e33, "Uranium")),
        ("650 Tetra: 100 Nissonite (Fetch)", lambda: recovery_button_fetch("Main",650, "Tetra", 100, "Nissonite")),
        ("1 Volt: 100 Orpiment (Sets)", lambda: recovery_button_set("Main",1, "Volt", 100, "Orpiment")),
    ],
    "Abyssal Trenches": [
        ("1M Tetra: 10M Bismuth (Fetch)", lambda: recovery_button_fetch("Main",1e6, "Tetra", 1e7, "Bismuth")),
        ("500 Volt: 1 Orpiment (Fetch)", lambda: recovery_button_fetch("Main",500, "Volt", 1, "Orpiment")),
        ("1 Aquamarine: 1k Nissonite (Sets)", lambda: recovery_button_set("Main",1, "Aquamarine", 1000, "Nissonite")),
        ("1 Aquamarine: 30 Tetra (Sets)", lambda: recovery_button_set("Main",1, "Aquamarine", 30, "Tetra")),
    ],
    "Flourish Candylands": [
        ("1 Lollipop: 350 Volt (Sets)", lambda: recovery_button_set("Main",1, "Lollipop", 350, "Volt")),
        ("4 Lollipop: 100 Tetra (Fetch)", lambda: recovery_button_fetch("Main",4, "Lollipop", 100, "Tetra")),
    ],
    "Ω1": [

    ],
    "???3Δ8???": [
        ("1 Stargazed Metal: 1M Gold (Sets)", lambda: recovery_button_set("Main",1, "Stargazed Metal", 1e6, "Gold")),
        ("6 Stargazed Metal: 5 Obsidian (Fetch)", lambda: recovery_button_fetch("Main",6, "Stargazed Metal", 5, "Obsidian")),
        ("52 Stargazed Metal: 1k Diamond (Sets)", lambda: recovery_button_set("Main",52, "Stargazed Metal", 1000, "Diamond")),
        ("1 Gyge: 3 Emerald (Fetch)", lambda: recovery_button_fetch("Main",1, "Gyge", 3, "Emerald")),
        ("75 Gyge: 1M Uranium (Sets)", lambda: recovery_button_set("Main",75, "Gyge", 1e6, "Uranium")),
        ("3 Auly Plate: 50 Orpiment (Sets)", lambda: recovery_button_set("Main",3, "Auly Plate", 50, "Orpiment")),
    ],
    "Gem Buttons": [
        ("50 White Gems: 1 Gems", lambda: cost_button("Main","White Gems", 50, "Gems", 1)),
        ("15 Crystal: 3 Gems", lambda: cost_button("Main","Crystal", 15, "Gems", 3)),
        ("500 White Gems: 5 Gems", lambda: cost_button("Main","White Gems", 500, "Gems", 5)),
        ("3k White Gems: 10 Gems", lambda: cost_button("Main","White Gems", 3000, "Gems", 10)),
        ("100 Crystal: 12 Gems", lambda: cost_button("Main","Crystal", 100, "Gems", 12)),
        ("1 Iron: 20 Gems", lambda: cost_button("Main","Iron", 1, "Gems", 20)),
        ("1k Crystal: 21 Gems", lambda: cost_button("Main","Crystal", 1000, "Gems", 21)),
        ("3 Quartz: 70 Gems", lambda: cost_button("Main","Quartz", 3, "Gems", 70)),
        ("600k Iron: 100 Gems", lambda: cost_button("Main","Iron", 6e5, "Gems", 100)),
        ("10 Quartz: 200 Gems", lambda: cost_button("Main","Quartz", 10, "Gems", 200)),
        ("1e68 Rebirths: 400 Gems", lambda: cost_button("Main","Rebirths", 1e68, "Gems", 400)),
        ("600T Crystal: 500 Gems", lambda: cost_button("Main","Crystal", 6e14, "Gems", 500)),
        ("100De White Gems: 600 Gems", lambda: cost_button("Main","White Gems", 1e35, "Gems", 600)),
        ("1e172 Mutliplier: 750 Gems", lambda: cost_button("Main","Multiplier", 1e172, "Gems", 750)),
        ("1e47 Stone: 800 Gems", lambda: cost_button("Main","Stone", 1e47, "Gems", 800)),
        ("50 Quartz: 950 Gems", lambda: cost_button("Main","Quartz", 50, "Gems", 950)),
        ("10 Jade: 1k Gems", lambda: cost_button("Main","Jade", 10, "Gems", 1000)),
        ("250 Quartz: 2.2k Gems", lambda: cost_button("Main","Quartz", 250, "Gems", 2200)),
        ("150 Jade: 17.5k Gems", lambda: cost_button("Main","Jade", 150, "Gems", 17500)),
        ("25M Quartz: 50k Gems", lambda: cost_button("Main","Quartz", 2.5e7, "Gems", 5e4)),
        ("5e41 Sapphire: 250M Gems", lambda: cost_button("Main","Sapphire", 5e41, "Gems", 2.5e8)),
        ("1k Starlight: 800M Gems", lambda: cost_button("Main","Starlight", 1000, "Gems", 8e8)),
        ("7 Ion: 3B Gems", lambda: cost_button("Main","Ion", 7, "Gems", 3e9)),
        ("2 Volt: 1T Gems", lambda: cost_button("Main","Volt", 2, "Gems", 1e12)),
    ],
    "Area Teleports": [
        ("Spawn (req: 0 Cash)", lambda: load_check("Main",0, "Cash", Spawn_Buttons)),
        ("Caves (req: 10 Stone)", lambda: load_check("Main",10, "Stone", Cave_Buttons)),
        ("Crystal Beneaths (req: 300 White Gems)", lambda: load_check("Main",300, "White Gems", Crystal_Buttons)),
        ("Iron Shafts (req: 100 Crystal)", lambda: load_check("Main",100, "Crystal", Iron_Buttons)),
        ("Golden Quarry (req: 750 Iron)", lambda: load_check("Main",750,"Iron",Gold_Buttons)),
        ("Quartz Walkway (req: 75 Gold)", lambda: load_check("Main",75,"Gold", Quartz_Buttons)),
        ("Jade Forest (req: 450 Quartz)", lambda: load_check("Main",450,"Quartz", Jade_Buttons)),
        ("Obsidian Abyss (req: 80 Jade)", lambda: load_check("Main", 80, "Jade", Obsidian_Buttons)),
        ("Colour Temple (req: 5 Obsidian)", lambda: load_check("Main", 5, "Obsidian", Colour_Buttons)),
        ("Extraterrestrial Orbits (req: 50k Sapphire)", lambda: load_check("Main", 5e4, "Sapphire", ET_Buttons)),
        ("Empyrean Island (req: 100 Starlight)", lambda: load_check("Main", 100, "Starlight", Ion_Buttons)),
    ]
}
Crystal_Buttons = {
    "Multiplier": [
        ("8e71 Cash: 10Oc Multiplier", lambda: cost_button("Main","Cash",8e71,"Multiplier", 1e28)),
        ("1e74 Cash: 20Oc Multiplier", lambda: cost_button("Main","Cash",1e74,"Multiplier", 2e28)),
        ("7.5e74 Cash: 40Oc Multiplier", lambda: cost_button("Main","Cash",7.5e74,"Multiplier", 4e28)),
        ("5e76 Cash: 75Oc Multiplier", lambda: cost_button("Main","Cash",5e76,"Multiplier", 7.5e28)),
        ("1.8e77 Cash: 150Oc Multiplier", lambda: cost_button("Main","Cash",1.8e77,"Multiplier", 1.5e29)),
        ("7e77 Cash: 250Oc Multiplier", lambda: cost_button("Main","Cash",7e77,"Multiplier", 2.5e29)),
        ("3e78 Cash: 800Oc Multiplier", lambda: cost_button("Main","Cash",3e78,"Multiplier", 8e29)),
        ("4.6e79 Cash: 3No Multiplier", lambda: cost_button("Main","Cash",4.6e79,"Multiplier", 3e30)),
        ("1.85e80 Cash: 12No Multiplier", lambda: cost_button("Main","Cash",1.85e80,"Multiplier", 1.2e31)),
        ("7.25e80 Cash: 47No Multiplier", lambda: cost_button("Main","Cash",7.25e80,"Multiplier", 4.7e31)),
        ("4e81 Cash: 100No Multiplier", lambda: cost_button("Main","Cash",4e81,"Multiplier", 1e32)),
        ("6.5e82 Cash: 300No Multiplier", lambda: cost_button("Main","Cash",6.5e82,"Multiplier", 3e32)),
        ("4.44e83 Cash: 800No Multiplier", lambda: cost_button("Main","Cash",4.44e83,"Multiplier", 8e32)),
        ("1e84 Cash: 2De Multiplier", lambda: cost_button("Main","Cash",1e84,"Multiplier", 2e33)),
    ],
    "Rebirths": [
        ("8e62 Multiplier: 40Sx Rebirths", lambda: reset_button("Main",8e62,"Multiplier",4e22, "Rebirths")),
        ("2e64 Multiplier: 300Sx Rebirths", lambda: reset_button("Main",2e64,"Multiplier",3e23, "Rebirths")),
        ("7e65 Multiplier: 1Sp Rebirths", lambda: reset_button("Main",7e65,"Multiplier",1e24, "Rebirths")),
        ("8e66 Multiplier: 20Sp Rebirths", lambda: reset_button("Main",8e66,"Multiplier",2e25, "Rebirths")),
        ("1.6e68 Multiplier: 100Sp Rebirths", lambda: reset_button("Main",1.6e68,"Multiplier",1e26, "Rebirths")),
        ("9e68 Multiplier: 800Sp Rebirths", lambda: reset_button("Main",9e68,"Multiplier",8e26, "Rebirths")),
        ("1.5e70 Multiplier: 3Oc Rebirths", lambda: reset_button("Main",1.5e70,"Multiplier",3e27, "Rebirths")),
        ("7.5e71 Multiplier: 15Oc Rebirths", lambda: reset_button("Main",7.5e71,"Multiplier",1.5e28, "Rebirths")),
        ("2e73 Multiplier: 100Oc Rebirths", lambda: reset_button("Main",2e73,"Multiplier",1e29, "Rebirths")),
        ("6e74 Multiplier: 1No Rebirths", lambda: reset_button("Main",6e74,"Multiplier",1e30, "Rebirths")),
        ("4e75 Multiplier: 14No Rebirths", lambda: reset_button("Main",4e75,"Multiplier",1.4e31, "Rebirths")),
        ("2.6e77 Multiplier: 46No Rebirths", lambda: reset_button("Main",2.6e77,"Multiplier",4.6e31, "Rebirths")),
        ("2e78 Multiplier: 300No Rebirths", lambda: reset_button("Main",2e78,"Multiplier",3e32, "Rebirths")),
        ("7e79 Multiplier: 1De Rebirths", lambda: reset_button("Main",7e79,"Multiplier",1e33, "Rebirths")),
    ],
    "Stone": [
        ("3e40 Rebirths: 5M Stone", lambda: reset_button("Main",3e40,"Rebirths",5e6, "Stone")),
        ("5e41 Rebirths: 20M Stone", lambda: reset_button("Main",5e41,"Rebirths",2e7, "Stone")),
        ("3e42 Rebirths: 100M Stone", lambda: reset_button("Main",3e42,"Rebirths",1e8, "Stone")),
        ("8e43 Rebirths: 300M Stone", lambda: reset_button("Main",8e43,"Rebirths",3e8, "Stone")),
        ("4e44 Rebirths: 1B Stone", lambda: reset_button("Main",4e44, "Rebirths", 1e9,"Stone")),
        ("5e45 Rebirths: 20B Stone", lambda: reset_button("Main",5e45, "Rebirths",2e10,"Stone")),
        ("8e46 Rebirths: 100B Stone", lambda: reset_button("Main",8e46, "Rebirths",1e11,"Stone")),
        ("5e47 Rebirths: 400B Stone", lambda: reset_button("Main",5e47, "Rebirths",4e11,"Stone")),
        ("3e48 Rebirths: 3T Stone", lambda: reset_button("Main",3e48, "Rebirths",3e12,"Stone")),
        ("4e50 Rebirths: 10T Stone", lambda: reset_button("Main",4e50, "Rebirths",1e13,"Stone")),
        ("2e51 Rebirths: 40T Stone", lambda: reset_button("Main",2e51, "Rebirths",4e13,"Stone")),
        ("3e52 Rebirths: 100T Stone", lambda: reset_button("Main",3e52, "Rebirths", 1e14,"Stone")),
        ("7.5e53 Rebirths: 2Qd Stone", lambda: reset_button("Main",7.5e53, "Rebirths", 2e15,"Stone")),
        ("5e54 Rebirths: 10Qd Stone", lambda: reset_button("Main",5e54, "Rebirths",1e16,"Stone"))
    ],
    "White Gems": [
        ("100B Stone: 300 White Gems", lambda: reset_button("Main",1e11, "Stone", 300,"White Gems")),
        ("900B Stone: 1k White Gems", lambda: reset_button("Main",9e11, "Stone", 1000,"White Gems")),
        ("30T Stone: 5k White Gems", lambda: reset_button("Main",3e13, "Stone", 5000,"White Gems")),
        ("750T Stone: 12k White Gems", lambda: reset_button("Main",7.5e14, "Stone", 1.2e4,"White Gems")),
        ("2.8Qd Stone: 20k White Gems", lambda: reset_button("Main",2.8e15, "Stone", 2e4,"White Gems")),
        ("100Qd Stone: 120k White Gems", lambda: reset_button("Main",1e17, "Stone", 1.2e5,"White Gems")),
        ("4Qn Stone: 230k White Gems", lambda: reset_button("Main",4e18, "Stone", 2.3e5,"White Gems"))
    ],
    "Crystal": [
        ("10k White Gems: 1 Crystal", lambda: reset_button("Main",1e4, "White Gems", 1,"Crystal")),
        ("600k White Gems: 6 Crystal", lambda: reset_button("Main",6e5, "White Gems", 6,"Crystal")),
        ("2M White Gems: 20 Crystal", lambda: reset_button("Main",2e6, "White Gems", 20,"Crystal")),
        ("500M White Gems: 50 Crystal", lambda: reset_button("Main",5e8, "White Gems", 50,"Crystal")),
    ],
    "Gem Buttons": [
        ("15 Crystal: 3 Gems", lambda: cost_button("Main","Crystal",15, "Gems", 3)),
        ("100 Crystal: 12 Gems", lambda: cost_button("Main","Crystal",100, "Gems", 12)),
        ("1k Crystal: 21 Gems", lambda: cost_button("Main","Crystal",1000, "Gems", 21)),
    ],
    "Recovery": [
        ("3 Crystal: 200 Stone (Fetch)", lambda: recovery_button_fetch("Main",3, "Crystal", 200, "Stone")),
        ("500 White Gems: 12Qn Multiplier (Fetch)", lambda: recovery_button_fetch("Main",500, "White Gems", 1.2e19, "Multiplier")),
        ("4 Gold: 500 White Gems (Fetch)", lambda: recovery_button_fetch("Main",4, "Gold", 500, "White Gems")),
    ],
    "Geodes": [
        ("Crystal Geode: 100 Crystal", lambda btn: Geode_roll(btn, crystal_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll))
    ],
    "Area Teleports": [
       ("Iron Shafts (req: 100 Crystal)", lambda: load_check("Main",100, "Crystal", Iron_Buttons)),
       ("Spawn (req: 0 Cash)", lambda: load_check("Main",0, "Cash", Spawn_Buttons)),
       ("Recover Hall (req: 0 Cash)", lambda: load_check("Main",0, "Cash", Recover_Hall_Buttons))
    ]
}
Iron_Buttons = {
    "Mutliplier": [
        ("1e93 Cash: 8De Multiplier", lambda: cost_button("Main","Cash",1e93,"Multiplier", 8e33)),
        ("8e94 Cash: 17De Multiplier", lambda: cost_button("Main","Cash",8e94,"Multiplier", 1.7e34)),
        ("2e96 Cash: 40De Multiplier", lambda: cost_button("Main","Cash",2e96,"Multiplier", 4e34)),
        ("1e98 Cash: 200De Multiplier", lambda: cost_button("Main","Cash",1e98,"Multiplier", 2e35)),
        ("8e98 Cash: 500De Multiplier", lambda: cost_button("Main","Cash",8e98,"Multiplier", 5e35)),
        ("6e99 Cash: 1.2e36 Multiplier", lambda: cost_button("Main","Cash",6e99,"Multiplier", 1.2e36)),
        ("3e101 Cash: 3e36 Multiplier", lambda: cost_button("Main","Cash",3e101,"Multiplier", 3e36)),
        ("3e102 Cash: 4.5e37 Multiplier", lambda: cost_button("Main","Cash",3e102,"Multiplier", 4.5e37)),
        ("1e104 Cash: 7e37 Multiplier", lambda: cost_button("Main","Cash",1e104,"Multiplier", 7e37)),
        ("6e104 Cash: 1.2e38 Multiplier", lambda: cost_button("Main","Cash",6e104,"Multiplier", 1.2e38)),
        ("5e105 Cash: 4e38 Multiplier", lambda: cost_button("Main","Cash",5e105,"Multiplier", 4e38)),
        ("3.5e106 Cash: 7.5e38 Multiplier", lambda: cost_button("Main","Cash",3.5e106,"Multiplier", 7e38)),
        ("5e107 Cash: 2e39 Multiplier", lambda: cost_button("Main","Cash",5e107,"Multiplier", 2e39)),
        ("3e108 Cash: 4e40 Multiplier", lambda: cost_button("Main","Cash",3e108,"Multiplier", 4e40)),
        ("8e110 Cash: 6e40 Multiplier", lambda: cost_button("Main","Cash",8e110,"Multiplier", 6e40)),
    ],
    "Rebirths": [
        ("1e85 Multiplier: 50De Rebirths", lambda: reset_button("Main",1e85,"Multiplier",5e34, "Rebirths")),
        ("5e86 Multiplier: 200De Rebirths", lambda: reset_button("Main",5e87,"Multiplier",2e35, "Rebirths")),
        ("3e87 Multiplier: 500De Rebirths", lambda: reset_button("Main",3e87,"Multiplier",5e35, "Rebirths")),
        ("5e90 Multiplier: 800De Rebirths", lambda: reset_button("Main",5e90,"Multiplier",8e35, "Rebirths")),
        ("2e92 Multiplier: 3e36 Rebirths", lambda: reset_button("Main",2e92,"Multiplier",3e36, "Rebirths")),
        ("3e93 Multiplier: 1.5e37 Rebirths", lambda: reset_button("Main",3e93,"Multiplier",1.5e37, "Rebirths")),
        ("7e95 Multiplier: 8e37 Rebirths", lambda: reset_button("Main",7e95,"Multiplier",8e37, "Rebirths")),
        ("1.5e97 Multiplier: 2e38 Rebirths", lambda: reset_button("Main",1.5e97,"Multiplier",2e38, "Rebirths")),
        ("1e99 Multiplier: 7e38 Rebirths", lambda: reset_button("Main",1e99,"Multiplier",7e38, "Rebirths")),
        ("8e101 Multiplier: 3e39 Rebirths", lambda: reset_button("Main",8e101,"Multiplier",3e39, "Rebirths")),
        ("8e102 Multiplier: 1e40 Rebirths", lambda: reset_button("Main",8e102,"Multiplier",1e40, "Rebirths")),
        ("6e104 Multiplier: 6e40 Rebirths", lambda: reset_button("Main",6e104,"Multiplier",6e40, "Rebirths")),
        ("1.2e106 Multiplier: 4e41 Rebirths", lambda: reset_button("Main",1.2e106,"Multiplier",4e41, "Rebirths")),
    ],
    "Stone": [
        ("1e57 Rebirths: 50Qd Stone", lambda: reset_button("Main",1e57, "Rebirths", 5e16, "Stone")),
        ("5e59 Rebirths: 700Qd Stone", lambda: reset_button("Main",5e59, "Rebirths", 7e17, "Stone")),
        ("3e61 Rebirths: 10Qn Stone", lambda: reset_button("Main",3e61, "Rebirths", 1e19, "Stone")),
        ("7e62 Rebirths: 50Qn Stone", lambda: reset_button("Main",7e62, "Rebirths", 5e19, "Stone")),
        ("2.3e64 Rebirths: 300Qn Stone", lambda: reset_button("Main",2.3e64, "Rebirths", 3e20, "Stone")),
        ("4e65 Rebirths: 800Qn Stone", lambda: reset_button("Main",4e65, "Rebirths", 8e20, "Stone")),
        ("5e67 Rebirths: 3Sx Stone", lambda: reset_button("Main",5e67, "Rebirths", 3e21, "Stone")),
        ("8e68 Rebirths: 20Sx Stone", lambda: reset_button("Main",8e68, "Rebirths", 2e22, "Stone")),
        ("1e70 Rebirths: 100Sx Stone", lambda: reset_button("Main",1e70, "Rebirths", 1e23, "Stone")),
    ],
    "White Gems": [
        ("300Qn Stone: 500k White Gems", lambda: reset_button("Main",3e20, "Stone", 5e5,"White Gems")),
        ("10Sx Stone: 3M White Gems", lambda: reset_button("Main",1e22, "Stone", 3e6,"White Gems")),
        ("300Sx Stone: 10M White Gems", lambda: reset_button("Main",3e23, "Stone", 1e7,"White Gems")),
        ("5Sp Stone: 45M White Gems", lambda: reset_button("Main",5e24, "Stone", 4.5e7,"White Gems")),
        ("100Sp Stone: 160M White Gems", lambda: reset_button("Main",1e26, "Stone", 1.6e8,"White Gems")),
        ("800Sp Stone: 300M White Gems", lambda: reset_button("Main",8e26, "Stone", 3e8,"White Gems")),
        ("25Oc Stone: 750M White Gems", lambda: reset_button("Main",2.5e28, "Stone", 7.5e8,"White Gems")),
        ("800Oc Stone: 2.5B White Gems", lambda: reset_button("Main",8e29, "Stone", 2.5e9,"White Gems")),
    ],
    "Crystal": [
        ("10B White Gems: 125 Crystal", lambda: reset_button("Main",1e10, "White Gems", 125,"Crystal")),
        ("60B White Gems: 300 Crystal", lambda: reset_button("Main",6e10, "White Gems", 300,"Crystal")),
        ("300B White Gems: 750 Crystal", lambda: reset_button("Main",3e11, "White Gems", 750,"Crystal")),
        ("7T White Gems: 2k Crystal", lambda: reset_button("Main",7e12, "White Gems", 2e3,"Crystal")),
        ("80T White Gems: 5k Crystal", lambda: reset_button("Main",8e13, "White Gems", 5e3,"Crystal")),
        ("600T White Gems: 12k Crystal", lambda: reset_button("Main",6e14, "White Gems", 1.2e4,"Crystal")),
        ("50Qd White Gems: 30k Crystal", lambda: reset_button("Main",5e16, "White Gems", 3e4,"Crystal")),
        ("800Qd White Gems: 60k Crystal", lambda: reset_button("Main",8e17, "White Gems", 6e4,"Crystal")),
    ],
    "Iron": [
        ("4k Crystal: 1 Iron", lambda: reset_button("Main",4e3, "Crystal", 1,"Iron")),
        ("42k Crystal: 10 Iron", lambda: reset_button("Main",4.2e4, "Crystal", 10,"Iron")),
        ("1M Crystal: 47 Iron", lambda: reset_button("Main", 1e6, "Crystal", 47,"Iron")),
        ("120M Crystal: 300 Iron", lambda: reset_button("Main",1.2e8, "Crystal", 300,"Iron")),
    ],
    "Gem Buttons": [
        ("1 Iron: 20 Gems", lambda: cost_button("Main","Iron",1, "Gems", 20)),
    ],
    "Recovery": [
        ("1k Crystal: 500Qn Rebirths (Fetch)", lambda: recovery_button_fetch("Main",1000, "Crystal", 5e20, "Rebirths")),
        ("150B White Gems: 10k Stone (Fetch)", lambda: recovery_button_fetch("Main",1.5e14, "White Gems", 1e4, "Stone")),
        ("3 Iron: 10 White Gems (Fetch)", lambda: recovery_button_fetch("Main",3, "Iron", 10, "White Gems")),
        ("50k Gems: 70 Crystal", lambda: cost_button("Main","Gems", 5e4, "Crystal", 70)),
    ],
    "Geodes": [
        ("Iron Geode: 25 Iron", lambda btn: Geode_roll(btn, iron_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
    ],
    "Area Teleports": [
       ("Spawn (req: 0 Cash)", lambda: load_check("Main",0, "Cash", Spawn_Buttons)),
       ("Recover Hall (req: 0 Cash)", lambda: load_check("Main",0, "Cash", Recover_Hall_Buttons)),
       ("Golden Quarry (req: 750 Iron)", lambda: load_check("Main",750,"Iron",Gold_Buttons)),
    ]
}
Gold_Buttons = {
    "Multiplier": [
        ("1e121 Cash: 1.1e41 Multiplier", lambda: cost_button("Main","Cash",1e121,"Multiplier", 1.1e41)),
        ("2e122 Cash: 3.5e41 Multiplier", lambda: cost_button("Main","Cash",2e122,"Multiplier", 3.5e41)),
        ("5e123 Cash: 6e41 Multiplier", lambda: cost_button("Main","Cash",5e123,"Multiplier", 6e41)),
        ("7.5e124 Cash: 3e42 Multiplier", lambda: cost_button("Main","Cash",7.5e124,"Multiplier", 3e42)),
        ("6e125 Cash: 1e43 Multiplier", lambda: cost_button("Main","Cash",6e125,"Multiplier", 1e43)),
        ("7.5e126 Cash: 3e46 Multiplier", lambda: cost_button("Main","Cash",7.5e126,"Multiplier", 3e46)),
        ("2.5e131 Cash: 8e46 Multiplier", lambda: cost_button("Main","Cash",2.5e131,"Multiplier", 8e46)),
        ("8e131 Cash: 3e50 Multiplier", lambda: cost_button("Main","Cash",8e131,"Multiplier", 3e50)),
        ("9e132 Cash: 7.5e50 Multiplier", lambda: cost_button("Main","Cash",9e132,"Multiplier", 7.5e50)),
        ("8e133 Cash: 1e52 Multiplier", lambda: cost_button("Main","Cash",8e133,"Multiplier", 1e52)),
    ],
    "Rebirths": [
        ("1e114 Multiplier: 1e42 Rebirths", lambda: reset_button("Main",1e114,"Multiplier",1e42, "Rebirths")),
        ("5e115 Multiplier: 5e43 Rebirths", lambda: reset_button("Main",5e115,"Multiplier",5e43, "Rebirths")),
        ("3e116 Multiplier: 6e43 Rebirths", lambda: reset_button("Main",3e116,"Multiplier",6e43, "Rebirths")),
        ("8e117 Multiplier: 1e44 Rebirths", lambda: reset_button("Main",8e117,"Multiplier",1e44, "Rebirths")),
        ("7.6e118 Multiplier: 3.5e44 Rebirths", lambda: reset_button("Main",7.6e118,"Multiplier",3.5e44, "Rebirths")),
        ("7.6e124 Multiplier: 1e46 Rebirths", lambda: reset_button("Main",7.6e124,"Multiplier",1e46, "Rebirths")),
    ],
    "Stone": [
        ("1e75 Rebirths: 100Sx Stone", lambda: reset_button("Main",1e75, "Rebirths", 1e23, "Stone")),
        ("3e76 Rebirths: 500Sx Stone", lambda: reset_button("Main",3e76, "Rebirths", 5e23, "Stone")),
        ("4.5e77 Rebirths: 2Sp Stone", lambda: reset_button("Main",4.5e77, "Rebirths", 2e24, "Stone")),
        ("1.5e79 Rebirths: 10Sp Stone", lambda: reset_button("Main",1.5e79, "Rebirths", 1e25, "Stone")),
        ("8e79 Rebirths: 50Sp Stone", lambda: reset_button("Main",8e79, "Rebirths", 5e25, "Stone")),
        ("7.5e80 Rebirths: 200Sp Stone", lambda: reset_button("Main",7.5e80, "Rebirths", 2e26, "Stone")),
    ],
    "White Gems": [
        ("10De Stone: 30B White Gems", lambda: reset_button("Main",3e34, "Stone", 3e10,"White Gems")),
        ("90De Stone: 100B White Gems", lambda: reset_button("Main",9e34, "Stone", 1e11,"White Gems")),
        ("750De Stone: 500B White Gems", lambda: reset_button("Main",7.5e35, "Stone", 5e11,"White Gems")),
        ("8e36 Stone: 1.5T White Gems", lambda: reset_button("Main",8e36, "Stone", 1.5e12,"White Gems")),
        ("5e37 Stone: 15T White Gems", lambda: reset_button("Main",5e37, "Stone", 1.5e13,"White Gems")),
        ("3e38 Stone: 40T White Gems", lambda: reset_button("Main",3e38, "Stone", 4e13,"White Gems")),
        ("8e38 Stone: 100T White Gems", lambda: reset_button("Main",8e38, "Stone", 1e14,"White Gems")),
        ("5e39 Stone: 400T White Gems", lambda: reset_button("Main",5e39, "Stone", 4e14,"White Gems")),
    ],
    "Crystal": [
        ("500Qn White Gems: 300k Crystal", lambda: reset_button("Main",5e20, "White Gems", 3e5,"Crystal")),
        ("30Sx White Gems: 750k Crystal", lambda: reset_button("Main",3e22, "White Gems", 7.5e5,"Crystal")),
        ("200Sx White Gems: 10M Crystal", lambda: reset_button("Main", 2e23, "White Gems", 1e7,"Crystal")),
        ("10Sp White Gems: 50M Crystal", lambda: reset_button("Main",1e25, "White Gems", 5e7,"Crystal")),
        ("200Sp White Gems: 80M Crystal", lambda: reset_button("Main",2e26, "White Gems", 8e7,"Crystal")),
        ("750Sp White Gems: 250M Crystal", lambda: reset_button("Main",7.5e26, "White Gems", 2.5e8,"Crystal")),
        ("6Oc White Gems: 600M Crystal", lambda: reset_button("Main",6e27, "White Gems", 6e8,"Crystal")),
        ("250Oc White Gems: 2B Crystal", lambda: reset_button("Main",2.5e29, "White Gems", 2e9,"Crystal")),
        ("850Oc White Gems: 25B Crystal", lambda: reset_button("Main",8.5e29, "White Gems", 2.5e10,"Crystal")),
    ],
    "Iron": [
        ("750M Crystal: 720 Iron", lambda: reset_button("Main",7.5e8, "Crystal", 720,"Iron")),
        ("1.8B Crystal: 3k Iron", lambda: reset_button("Main",1.8e9, "Crystal", 3e3,"Iron")),
        ("11B Crystal: 7.5k Iron", lambda: reset_button("Main",1.1e10, "Crystal", 7.5e3,"Iron")),
        ("35B Crystal: 18k Iron", lambda: reset_button("Main",3.5e10, "Crystal", 1.8e4,"Iron")),
        ("100B Crystal: 45k Iron", lambda: reset_button("Main",1e11, "Crystal", 4.5e4,"Iron")),
        ("500B Crystal: 100k Iron", lambda: reset_button("Main",5e11, "Crystal", 1e5,"Iron")),
    ],
    "Gold": [
        ("45k Iron: 1 Gold", lambda: reset_button("Main",4.5e4, "Iron", 1,"Gold")),
        ("200k Iron: 5 Gold", lambda: reset_button("Main",2e5, "Iron", 5,"Gold")),
        ("500k Iron: 25 Gold", lambda: reset_button("Main",5e5, "Iron", 25,"Gold")),
    ],
    "Gem Buttons": [
        ("600k Iron: 100 Gems", lambda: cost_button("Main","Iron",6e5, "Gems", 100)),
        ("1e98 Rebirths: 400 Gems", lambda: cost_button("Main","Rebirths",1e98, "Gems", 400)),
        ("600T Crystal: 500 Gems", lambda: cost_button("Main","Crystal",6e14, "Gems", 500)),
        ("100De White Gems: 600 Gems", lambda: cost_button("Main","White Gems",1e35, "Gems", 600)),
        ("1e172 Multiplier: 750 Gems", lambda: cost_button("Main","Multiplier",1e172, "Gems", 750)),
        ("1e47 Stone: 800 Gems", lambda: cost_button("Main","Stone",1e47, "Gems", 800)),
    ],
    "Geodes": [
        ("Gold Geode: 60 Gold", lambda btn: Geode_roll(btn, gold_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
    ],
    "Area Teleports": [
       ("Spawn (req: 0 Cash)", lambda: load_check("Main",0, "Cash", Spawn_Buttons)),
       ("Recover Hall (req: 0 Cash)", lambda: load_check("Main",0, "Cash", Recover_Hall_Buttons))
    ]
}
Quartz_Buttons = {
    "Multiplier": [
        ("1e143 Cash: 3e54 Multiplier", lambda: cost_button("Main","Cash",1e143,"Multiplier", 3e54)),
        ("6e145 Cash: 1.5e55 Multiplier", lambda: cost_button("Main","Cash",6e145,"Multiplier", 1.5e55)),
        ("2e147 Cash: 4e55 Multiplier", lambda: cost_button("Main","Cash",2e147,"Multiplier", 4e55)),
        ("5e148 Cash: 1.2e56 Multiplier", lambda: cost_button("Main","Cash",5e148,"Multiplier", 1.2e56)),
        ("6e149 Cash: 2.3e56 Multiplier", lambda: cost_button("Main","Cash",6e149,"Multiplier", 2.3e56)),
        ("1.25e151 Cash: 6e56 Multiplier", lambda: cost_button("Main","Cash",1.25e151,"Multiplier", 6e56)),
        ("3e151 Cash: 3.5e58 Multiplier", lambda: cost_button("Main","Cash",3e151,"Multiplier", 3.5e58)),
        ("5.2e152 Cash: 6e58 Multiplier", lambda: cost_button("Main","Cash",5.2e152,"Multiplier", 6e58)),
        ("3e153 Cash: 1.25e59 Multiplier", lambda: cost_button("Main","Cash",3e153,"Multiplier", 1.25e59)),
        ("2e155 Cash: 3e59 Multiplier", lambda: cost_button("Main","Cash",2e155,"Multiplier", 3e59)),
        ("5e156 Cash: 1e60 Multiplier", lambda: cost_button("Main","Cash",5e156,"Multiplier", 1e60)),
    ],
    "Rebirths": [
        ("2.5e135 Multiplier: 1e51 Rebirths", lambda: reset_button("Main",2.5e135,"Multiplier",1e51, "Rebirths")),
        ("7.5e137 Multiplier: 7.5e52 Rebirths", lambda: reset_button("Main",7.5e137,"Multiplier",7.5e52, "Rebirths")),
        ("8e139 Multiplier: 3e53 Rebirths", lambda: reset_button("Main",8e139,"Multiplier",3e53, "Rebirths")),
        ("5e141 Multiplier: 7.5e53 Rebirths", lambda: reset_button("Main",5e141,"Multiplier",7.5e53, "Rebirths")),
        ("7.25e142 Multiplier: 1e55 Rebirths", lambda: reset_button("Main",7.25e142,"Multiplier",1e55, "Rebirths")),
        ("8e144 Multiplier: 5e55 Rebirths", lambda: reset_button("Main",8e144,"Multiplier",5e55, "Rebirths")),
        ("6e145 Multiplier: 1.2e56 Rebirths", lambda: reset_button("Main",6e145,"Multiplier",1.2e56, "Rebirths")),
        ("5e171 Multiplier: 1e59 Rebirths", lambda: reset_button("Main",5e171,"Multiplier",1e59, "Rebirths")),
        ("3e187 Multiplier: 1e62 Rebirths", lambda: reset_button("Main",3e187,"Multiplier",1e62, "Rebirths")),
        ("1e206 Multiplier: 1e65 Rebirths", lambda: reset_button("Main",1e206,"Multiplier",1e65, "Rebirths")),
    ],
    "Stone": [
        ("1e148 Rebirths: 1De Stone", lambda: reset_button("Main",1e148, "Rebirths", 1e33, "Stone")),
        ("1.5e154 Rebirths: 50De Stone", lambda: reset_button("Main",1.5e154, "Rebirths", 5e34, "Stone")),
        ("8.5e155 Rebirths: 2e37 Stone", lambda: reset_button("Main",8.5e155, "Rebirths", 2e37, "Stone")),
        ("3e159 Rebirths: 8e37 Stone", lambda: reset_button("Main",3e159, "Rebirths", 8e37, "Stone")),
        ("1.5e164 Rebirths: 6e38 Stone", lambda: reset_button("Main",1.5e164, "Rebirths", 6e38, "Stone")),
        ("1e166 Rebirths: 5e39 Stone", lambda: reset_button("Main",1e166, "Rebirths", 5e39, "Stone")),
        ("7.5e167 Rebirths: 6e40 Stone", lambda: reset_button("Main",7.5e167, "Rebirths", 6e40, "Stone")),
        ("6e169 Rebirths: 2.5e41 Stone", lambda: reset_button("Main",6e169, "Rebirths", 2.5e41, "Stone")),
    ],
    "White Gems": [
        ("1e60 Stone: 1Qd White Gems", lambda: reset_button("Main",1e60, "Stone", 1e15,"White Gems")),
        ("5e62 Stone: 25Qd White Gems", lambda: reset_button("Main",5e62, "Stone", 2.5e16,"White Gems")),
        ("2e64 Stone: 70Qd White Gems", lambda: reset_button("Main",2e64, "Stone", 7e16,"White Gems")),
        ("4.8e65 Stone: 160Qd White Gems", lambda: reset_button("Main",4.8e65, "Stone", 1.6e17,"White Gems")),
        ("6e67 Stone: 300Qd White Gems", lambda: reset_button("Main",6e67, "Stone", 3e17,"White Gems")),
        ("8e68 Stone: 650Qd White Gems", lambda: reset_button("Main",8e68, "Stone", 6.5e17,"White Gems")),
        ("3e70 Stone: 3Qn White Gems", lambda: reset_button("Main",3e70, "Stone", 3e18,"White Gems")),
        ("1.5e73 Stone: 45Qn White Gems", lambda: reset_button("Main",1.5e73, "Stone", 4.5e19,"White Gems")),
        ("8e74 Stone: 125Qn White Gems", lambda: reset_button("Main",8e74, "Stone", 1.25e20,"White Gems")),
        ("8e76 Stone: 600Qn White Gems", lambda: reset_button("Main",8e76, "Stone", 6e20,"White Gems")),
        ("9.5e77 Stone: 3Sx White Gems", lambda: reset_button("Main",9.5e77, "Stone", 3e21,"White Gems")),
    ],
    "Crystal": [
        ("3e37 White Gems: 1T Crystal", lambda: reset_button("Main",3e37, "White Gems", 1e12,"Crystal")),
        ("2e39 White Gems: 15T Crystal", lambda: reset_button("Main",2e39, "White Gems", 1.5e13,"Crystal")),
        ("4e44 White Gems: 75T Crystal", lambda: reset_button("Main",4e44, "White Gems", 7.5e13,"Crystal")),
        ("8e46 White Gems: 200T Crystal", lambda: reset_button("Main",8e46, "White Gems", 2e14,"Crystal")),
        ("5e51 White Gems: 750T Crystal", lambda: reset_button("Main",5e51, "White Gems", 7.5e14,"Crystal")),
        ("7.6e53 White Gems: 3Qd Crystal", lambda: reset_button("Main",7.6e53, "White Gems", 3e15,"Crystal")),
        ("2.5e55 White Gems: 50Qd Crystal", lambda: reset_button("Main",2.5e55, "White Gems", 5e16,"Crystal")),
        ("3.17e56 White Gems: 125Qd Crystal", lambda: reset_button("Main",3.17e56, "White Gems", 1.25e17,"Crystal")),
        ("4.2e58 White Gems: 417Qd Crystal", lambda: reset_button("Main",4.2e58, "White Gems", 4.17e17,"Crystal")),
        ("2.2e61 White Gems: 926Qd Crystal", lambda: reset_button("Main",2.2e61, "White Gems", 9.26e17,"Crystal")),
        ("7.23e62 White Gems: 11Qn Crystal", lambda: reset_button("Main",7.23e62, "White Gems", 1.1e19,"Crystal")),
        ("8.2e64 White Gems: 64Qn Crystal", lambda: reset_button("Main",8.2e64, "White Gems", 6.4e19,"Crystal")),
        ("9.22e65 White Gems: 265Qn Crystal", lambda: reset_button("Main",9.22e65, "White Gems", 2.65e20,"Crystal")),
    ],
    "Iron": [
        ("3Qd Crystal: 600k Iron", lambda: reset_button("Main",3e15, "Crystal", 6e5,"Iron")),
        ("600Qd Crystal: 5M Iron", lambda: reset_button("Main",6e17, "Crystal", 5e6,"Iron")),
        ("25Qn Crystal: 30M Iron", lambda: reset_button("Main",2.5e19, "Crystal", 3e7,"Iron")),
        ("500Qn Crystal: 100M Iron", lambda: reset_button("Main",5e20, "Crystal", 1e8,"Iron")),
        ("21Sx Crystal: 500M Iron", lambda: reset_button("Main",2.1e22, "Crystal", 5e8,"Iron")),
        ("450Sx Crystal: 3B Iron", lambda: reset_button("Main",4.5e23, "Crystal", 3e9,"Iron")),
        ("12Sp Crystal: 15B Iron", lambda: reset_button("Main",1.2e25, "Crystal", 1.5e10,"Iron")),
        ("210Sp Crystal: 40B Iron", lambda: reset_button("Main",2.1e26, "Crystal", 4e10,"Iron")),
        ("4Oc Crystal: 150B Iron", lambda: reset_button("Main",4e27, "Crystal", 1.5e11,"Iron")),
        ("300Oc Crystal: 300B Iron", lambda: reset_button("Main",3e29, "Crystal", 3e11,"Iron")),
        ("5No Crystal: 2T Iron", lambda: reset_button("Main",5e30, "Crystal", 2e12,"Iron")),
        ("250No Crystal: 36T Iron", lambda: reset_button("Main",2.5e32, "Crystal", 3.6e13,"Iron")),
    ],
    "Gold": [
        ("1M Iron: 75 Gold", lambda: reset_button("Main",1e6, "Iron", 75,"Gold")),
        ("50M Iron: 300 Gold", lambda: reset_button("Main",5e7, "Iron", 300,"Gold")),
        ("200M Iron: 800 Gold", lambda: reset_button("Main",2e8, "Iron", 800,"Gold")),
        ("1B Iron: 1.5k Gold", lambda: reset_button("Main",1e9, "Iron", 1500,"Gold")),
        ("45B Iron: 6k Gold", lambda: reset_button("Main",4.5e10, "Iron", 6000,"Gold")),
    ],
    "Quartz": [
        ("2.5k Gold: 1 Quartz", lambda: reset_button("Main",2.5e3, "Gold", 1,"Quartz")),
        ("7k Gold: 3 Quartz", lambda: reset_button("Main",7e3, "Gold", 3,"Quartz")),
        ("20k Gold: 10 Quartz", lambda: reset_button("Main",2e4, "Gold", 10,"Quartz")),
        ("55k Gold: 75 Quartz", lambda: reset_button("Main",5.5e4, "Gold", 75,"Quartz")),
    ],
    "Gem Buttons": [
        ("3 Quartz: 70 Gems", lambda: cost_button("Main","Quartz",3, "Gems", 75)),
        ("10 Quartz: 200 Gems", lambda: cost_button("Main","Quartz",10, "Gems", 200)),
        ("50 Quartz: 950 Gems", lambda: cost_button("Main","Quartz",50, "Gems", 950)),
        ("250 Quartz: 2200 Gems", lambda: cost_button("Main","Quartz",250, "Gems", 2200)),
    ],
    "Recovery": [
        ("7k Gems: 1e45 Multiplier (Fetch)", lambda: recovery_button_fetch("Main",7000, "Gems", 1e45, "Multiplier")),
        ("1k Gold: 5M White Gems (Fetch)", lambda: recovery_button_fetch("Main",1000, "Gold", 5e6, "White Gems")),
        ("15 Quartz: 100 Iron (Fetch)", lambda: recovery_button_fetch("Main",15, "Quartz", 100, "Iron")),
    ],
    "Geodes": [
        ("Quartz Geode: 30 Quartz", lambda btn: Geode_roll(btn, quartz_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
    ],
    "Area Teleports": [
       ("Spawn (req: 0 Cash)", lambda: load_check("Main",0, "Cash", Spawn_Buttons)),
       ("Recover Hall (req: 0 Cash)", lambda: load_check("Main",0, "Cash", Recover_Hall_Buttons))
    ]
}
Jade_Buttons = {
    "Multiplier": [
        ("1e301 Cash: 1e75 Multiplier", lambda: cost_button("Main","Cash",Mantissa(1,301),"Multiplier", 1e75)),
        ("5e308 Cash: 5e81 Multiplier", lambda: cost_button("Main","Cash",Mantissa(5,308),"Multiplier", 5e81)),
        ("1e316 Cash: 3e83 Multiplier", lambda: cost_button("Main","Cash",Mantissa(1,316),"Multiplier", 3e83)),
        ("4e320 Cash: 2.5e85 Multiplier", lambda: cost_button("Main","Cash",Mantissa(4,320),"Multiplier", 2.5e85)),
        ("3e322 Cash: 1.6e86 Multiplier", lambda: cost_button("Main","Cash",Mantissa(3,322),"Multiplier", 1.6e86)),
        ("2.2e323 Cash: 4.5e86 Multiplier", lambda: cost_button("Main","Cash",Mantissa(2.2,323),"Multiplier", 4.5e86)),
        ("1.6e325 Cash: 1e88 Multiplier", lambda: cost_button("Main","Cash",Mantissa(1.6,325),"Multiplier", 1e88)),
        ("3e326 Cash: 2.5e88 Multiplier", lambda: cost_button("Main","Cash",Mantissa(3,326),"Multiplier", 2.5e88)),
        ("8e326 Cash: 6.6e88 Multiplier", lambda: cost_button("Main","Cash",Mantissa(8,326),"Multiplier", 6.6e88)),
        ("1.2e328 Cash: 1.4e89 Multiplier", lambda: cost_button("Main","Cash",Mantissa(1.2,328),"Multiplier", 1.4e89)),
        ("7.2e328 Cash: 4.1e89 Multiplier", lambda: cost_button("Main","Cash",Mantissa(7.2,328),"Multiplier", 4.1e89)),
        ("2.8e329 Cash: 2e90 Multiplier", lambda: cost_button("Main","Cash",Mantissa(2.8,329),"Multiplier", 2e90)),
        ("7.5e329 Cash: 3.6e91 Multiplier", lambda: cost_button("Main","Cash",Mantissa(7.5,329),"Multiplier", 3.6e91)),
        ("1e331 Cash: 9e91 Multiplier", lambda: cost_button("Main","Cash",Mantissa(1,331),"Multiplier", 9e91)),
        ("8e331 Cash: 3.1e92 Multiplier", lambda: cost_button("Main","Cash",Mantissa(8,331),"Multiplier", 3.1e92)),
        ("4.5e332 Cash: 7.2e92 Multiplier", lambda: cost_button("Main","Cash",Mantissa(4.5,332),"Multiplier", 7.2e92)),
        ("1e333 Cash: 2e93 Multiplier", lambda: cost_button("Main","Cash",Mantissa(1,333),"Multiplier", 2e93)),
    ],
    "Rebirths": [
        ("1e269 Multiplier: 3e70 Rebirths", lambda: reset_button("Main",1e269,"Multiplier",3e70, "Rebirths")),
        ("3e285 Multiplier: 1.5e74 Rebirths", lambda: reset_button("Main",3e285,"Multiplier",1.5e74, "Rebirths")),
        ("1e295 Multiplier: 4e76 Rebirths", lambda: reset_button("Main",1e295,"Multiplier",4e76, "Rebirths")),
        ("4e299 Multiplier: 5e77 Rebirths", lambda: reset_button("Main",4e299,"Multiplier",5e77, "Rebirths")),
        ("5e301 Multiplier: 3e79 Rebirths", lambda: reset_button("Main",Mantissa(5,301),"Multiplier",3e79, "Rebirths")),
        ("2e305 Multiplier: 2e80 Rebirths", lambda: reset_button("Main",Mantissa(2,305),"Multiplier",2e80, "Rebirths")),
        ("1e307 Multiplier: 7e80 Rebirths", lambda: reset_button("Main",Mantissa(1,307),"Multiplier",7e80, "Rebirths")),
        ("6e308 Multiplier: 1e82 Rebirths", lambda: reset_button("Main",Mantissa(6,308),"Multiplier",1e82, "Rebirths")),
        ("4e310 Multiplier: 6e82 Rebirths", lambda: reset_button("Main",Mantissa(4,310),"Multiplier",6e82, "Rebirths")),
        ("2e311 Multiplier: 2e83 Rebirths", lambda: reset_button("Main",Mantissa(2,311),"Multiplier",2e83, "Rebirths")),
        ("1e312 Multiplier: 1e84 Rebirths", lambda: reset_button("Main",Mantissa(1,312),"Multiplier",1e84, "Rebirths")),
    ],
    "Stone": [
        ("1e181 Rebirths: 2e46 Stone", lambda: reset_button("Main",1e181, "Rebirths", 2e46, "Stone")),
        ("1.6e185 Rebirths: 5.3e46 Stone", lambda: reset_button("Main",1.6e185, "Rebirths", 5.3e46, "Stone")),
        ("6e188 Rebirths: 1.75e47 Stone", lambda: reset_button("Main",6e188, "Rebirths", 1.75e47, "Stone")),
        ("1.5e191 Rebirths: 5e47 Stone", lambda: reset_button("Main",1.5e191, "Rebirths", 5e47, "Stone")),
        ("9e191 Rebirths: 3e48 Stone", lambda: reset_button("Main",9e191, "Rebirths", 3e48, "Stone")),
        ("1e193 Rebirths: 2.4e49 Stone", lambda: reset_button("Main",1e193, "Rebirths", 2.4e49, "Stone")),
        ("1.75e194 Rebirths: 7.5e49 Stone", lambda: reset_button("Main",1.75e194, "Rebirths", 7.5e49, "Stone")),
        ("8.5e194 Rebirths: 3e50 Stone", lambda: reset_button("Main",8.5e194, "Rebirths", 3e50, "Stone")),
    ],
    "White Gems": [
        ("1e82 Stone: 15Sx White Gems", lambda: reset_button("Main",1e82, "Stone", 1.5e22,"White Gems")),
        ("2.5e83 Stone: 60Sx White Gems", lambda: reset_button("Main",2.5e83, "Stone", 6e22,"White Gems")),
        ("8e83 Stone: 300Sx White Gems", lambda: reset_button("Main",8e83, "Stone", 3e23,"White Gems")),
        ("5e85 Stone: 750Sx White Gems", lambda: reset_button("Main",5e85, "Stone", 7.5e23,"White Gems")),
        ("2.5e86 Stone: 25Sp White Gems", lambda: reset_button("Main",2.5e86, "Stone", 2.5e25,"White Gems")),
        ("7.7e86 Stone: 150Sp White Gems", lambda: reset_button("Main",7.7e86, "Stone", 1.5e26,"White Gems")),
        ("8e88 Stone: 500Sp White Gems", lambda: reset_button("Main",8e88, "Stone", 5e26,"White Gems")),
        ("3e89 Stone: 10Oc White Gems", lambda: reset_button("Main",3e89, "Stone", 1e28,"White Gems")),
        ("1e90 Stone: 75Oc White Gems", lambda: reset_button("Main",1e90, "Stone", 7.5e28,"White Gems")),
    ],
    "Crystal": [
        ("4.2e70 White Gems: 5Sx Crystal", lambda: reset_button("Main",4.2e70, "White Gems", 5e21,"Crystal")),
        ("3.5e71 White Gems: 30Sx Crystal", lambda: reset_button("Main",3.5e71, "White Gems", 3e22,"Crystal")),
        ("9e71 White Gems: 70Sx Crystal", lambda: reset_button("Main",9e71, "White Gems", 7e22,"Crystal")),
        ("3e73 White Gems: 400Sx Crystal", lambda: reset_button("Main",3e73, "White Gems", 4e23,"Crystal")),
        ("2e74 White Gems: 750Sx Crystal", lambda: reset_button("Main",2e74, "White Gems", 7.5e23,"Crystal")),
        ("6.5e74 White Gems: 15Sp Crystal", lambda: reset_button("Main",6.5e74, "White Gems", 1.5e25,"Crystal")),
        ("2.5e76 White Gems: 50Sp Crystal", lambda: reset_button("Main",2.5e76, "White Gems", 5e25,"Crystal")),
        ("3e77 White Gems: 120Sp Crystal", lambda: reset_button("Main",3e77, "White Gems", 1.2e26,"Crystal")),
        ("1e79 White Gems: 500Sp Crystal", lambda: reset_button("Main",1e79, "White Gems", 5e26,"Crystal")),
        ("2.5e80 White Gems: 30Oc Crystal", lambda: reset_button("Main",2.5e80, "White Gems", 3e28,"Crystal")),
    ],
    "Iron": [
        ("10De Crystal: 250T Iron", lambda: reset_button("Main",1e34, "Crystal", 2.5e14,"Iron")),
        ("200De Crystal: 725T Iron", lambda: reset_button("Main",2e35, "Crystal", 7.25e14,"Iron")),
        ("1e37 Crystal: 15Qd Iron", lambda: reset_button("Main",1e37, "Crystal", 1.5e16,"Iron")),
        ("1.75e38 Crystal: 40Qd Iron", lambda: reset_button("Main",1.75e38, "Crystal", 4e16,"Iron")),
        ("3e40 Crystal: 250Qd Iron", lambda: reset_button("Main",3e40, "Crystal", 2.5e17,"Iron")),
        ("1.5e41 Crystal: 800Qd Iron", lambda: reset_button("Main",1.5e41, "Crystal", 8e17,"Iron")),
        ("7.5e41 Crystal: 10Qn Iron", lambda: reset_button("Main",7.5e41, "Crystal", 1e19,"Iron")),
        ("3e43 Crystal: 60Qn Iron", lambda: reset_button("Main",3e43, "Crystal", 6e19,"Iron")),
        ("5e44 Crystal: 200Qn Iron", lambda: reset_button("Main",5e44, "Crystal", 2e20,"Iron")),
        ("2e46 Crystal: 800Qn Iron", lambda: reset_button("Main",2e46, "Crystal", 8e20,"Iron")),
        ("1.2e47 Crystal: 50Sx Iron", lambda: reset_button("Main",1.2e47, "Crystal", 5e22,"Iron")),
        ("6e47 Crystal: 120Sx Iron", lambda: reset_button("Main",6e47, "Crystal", 1.2e23,"Iron")),
        ("3e48 Crystal: 550Sx Iron", lambda: reset_button("Main",3e48, "Crystal", 5.5e23,"Iron")),
    ],
    "Gold": [
        ("300B Iron: 100k Gold", lambda: reset_button("Main",3e11, "Iron", 1e5,"Gold")),
        ("900T Iron: 500k Gold", lambda: reset_button("Main",9e14, "Iron", 5e5,"Gold")),
        ("10Qd Iron: 3M Gold", lambda: reset_button("Main",1e16, "Iron", 3e6,"Gold")),
        ("50Qn Iron: 20M Gold", lambda: reset_button("Main",5e19, "Iron", 2e7,"Gold")),
        ("300Sx Iron: 100M Gold", lambda: reset_button("Main",3e23, "Iron", 1e8,"Gold")),
        ("1Sp Iron: 750M Gold", lambda: reset_button("Main",1e24, "Iron", 7.5e8,"Gold")),
    ],
    "Quartz": [
        ("400k Gold: 200 Quartz", lambda: reset_button("Main",4e5, "Gold", 200,"Quartz")),
        ("15M Gold: 1k Quartz", lambda: reset_button("Main",1.5e7, "Gold", 1000,"Quartz")),
        ("250M Gold: 5k Quartz", lambda: reset_button("Main",2.5e8, "Gold", 5000,"Quartz")),
        ("5B Gold: 30k Quartz", lambda: reset_button("Main",5e9, "Gold", 3e4,"Quartz")),
    ],
    "Jade": [
        ("1k Quartz: 1 Jade", lambda: reset_button("Main",1000, "Quartz", 1,"Jade")),
        ("20k Quartz: 5 Jade", lambda: reset_button("Main",2e4, "Quartz", 5,"Jade")),
        ("500k Quartz: 24 Jade", lambda: reset_button("Main",5e5, "Quartz", 24,"Jade")),
    ],
    "Gem Buttons": [
        ("10 Jade: 1k Gems", lambda: cost_button("Main","Jade",10, "Gems", 1000)),
    ],
    "Recovery": [
        ("300 Quartz: 1e67 Rebirths (Fetch)", lambda: recovery_button_fetch("Main",300, "Quartz", 1e67, "Rebirths")),
        ("1M Gold: 1No Stone (Fetch)", lambda: recovery_button_fetch("Main",1e6, "Gold", 1e30, "Stone")),
        ("2 Jade: 15Sx Crystal (Fetch)", lambda: recovery_button_fetch("Main",2, "Jade", 1.5e22, "Crystal")),
    ],
    "Geodes": [
         ("Emoji Geode: 1k Gems", lambda btn: Geode_roll(btn, emoji_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
    ],
    "Area Teleports": [
       ("Spawn (req: 0 Cash)", lambda: load_check("Main",0, "Cash", Spawn_Buttons)),
       ("Recover Hall (req: 0 Cash)", lambda: load_check("Main",0, "Cash", Recover_Hall_Buttons))
    ]
}
Obsidian_Buttons = {
    "Multiplier": [
        ("1e360 Cash: 1e96 Multiplier", lambda: cost_button("Main","Cash",Mantissa(1,360),"Multiplier", 1e96)),
        ("1e378 Cash: 2e104 Multiplier", lambda: cost_button("Main","Cash",Mantissa(1,378),"Multiplier", 2e104)),
        ("1e399 Cash: 1.2e110 Multiplier", lambda: cost_button("Main","Cash",Mantissa(1,399),"Multiplier", 1.2e110)),
        ("1e432 Cash: 5e122 Multiplier", lambda: cost_button("Main","Cash",Mantissa(1,432),"Multiplier", 5e122)),
    ],
    "Rebirths": [
        ("3e324 Multiplier: 2e93 Rebirths", lambda: reset_button("Main",Mantissa(3,324),"Multiplier",2e93, "Rebirths")),
        ("1.5e340 Multiplier: 8e99 Rebirths", lambda: reset_button("Main",Mantissa(1.5,340),"Multiplier",8e99, "Rebirths")),
        ("5e365 Multiplier: 1e108 Rebirths", lambda: reset_button("Main",Mantissa(5,365),"Multiplier",1e108, "Rebirths")),
        ("2e398 Multiplier: 6e124 Rebirths", lambda: reset_button("Main",Mantissa(2,398),"Multiplier",6e124, "Rebirths")),
        ("4e412 Multiplier: 1e141 Rebirths", lambda: reset_button("Main",Mantissa(4,412),"Multiplier",1e141, "Rebirths")),
    ],
    "Stone": [
        ("6e213 Rebirths: 1e68 Stone", lambda: reset_button("Main",6e213, "Rebirths", 1e68, "Stone")),
        ("7e224 Rebirths: 2e76 Stone", lambda: reset_button("Main",7e224, "Rebirths", 2e76, "Stone")),
        ("2e245 Rebirths: 1.5e98 Stone", lambda: reset_button("Main",2e245, "Rebirths", 1.5e98, "Stone")),
        ("6.5e258 Rebirths: 5e106 Stone", lambda: reset_button("Main",6.5e258, "Rebirths", 5e106, "Stone")),
        ("2.1e265 Rebirths: 7e110 Stone", lambda: reset_button("Main",2.1e265, "Rebirths", 7e110, "Stone")),
        ("1e274 Rebirths: 3.5e117 Stone", lambda: reset_button("Main",1e274, "Rebirths", 3.5e117, "Stone")),
        ("8.2e292 Rebirths: 1e127 Stone", lambda: reset_button("Main",8.2e292, "Rebirths", 1e127, "Stone")),
    ],
    "White Gems": [
        ("1.5e110 Stone: 210No White Gems", lambda: reset_button("Main",1.5e110, "Stone", 2.1e32,"White Gems")),
        ("3.2e118 Stone: 52De White Gems", lambda: reset_button("Main",3.2e118, "Stone", 5.2e34,"White Gems")),
        ("5e126 Stone: 6e38 White Gems", lambda: reset_button("Main",5e126, "Stone", 6e38,"White Gems")),
        ("8.2e136 Stone: 2.5e42 White Gems", lambda: reset_button("Main",8.2e136, "Stone", 2.5e42,"White Gems")),
        ("5.1e140 Stone: 3.2e46 White Gems", lambda: reset_button("Main",5.1e140, "Stone", 3.2e46,"White Gems")),
        ("1.3e146 Stone: 7.5e51 White Gems", lambda: reset_button("Main",1.3e146, "Stone", 7.5e51,"White Gems")),
        ("5.2e152 Stone: 2.1e57 White Gems", lambda: reset_button("Main",5.2e152, "Stone", 2.1e57,"White Gems")),
        ("1.3e176 Stone: 1e60 White Gems", lambda: reset_button("Main",1.3e176, "Stone", 1e60,"White Gems")),
    ],
    "Crystal": [
        ("3.2e90 White Gems: 210Oc Crystal", lambda: reset_button("Main",3.2e90, "White Gems", 2.1e29,"Crystal")),
        ("3.2e90 White Gems: 210Oc Crystal", lambda: reset_button("Main",3.2e90, "White Gems", 2.1e29,"Crystal")),
        ("7.1e112 White Gems: 42No Crystal", lambda: reset_button("Main",7.1e112, "White Gems", 4.2e30,"Crystal")),
        ("4.2e123 White Gems: 6.2e36 Crystal", lambda: reset_button("Main",4.2e123, "White Gems", 6.2e36,"Crystal")),
        ("3.3e131 White Gems: 5.3e41 Crystal", lambda: reset_button("Main",3.3e131, "White Gems", 5.3e41,"Crystal")),
        ("7.2e139 White Gems: 9.1e48 Crystal", lambda: reset_button("Main",7.2e139, "White Gems", 9.1e48,"Crystal")),
        ("5.6e143 White Gems: 2e49 Crystal", lambda: reset_button("Main",5.6e143, "White Gems", 2e49,"Crystal")),
        ("6.2e150 White Gems: 1.5e57 Crystal", lambda: reset_button("Main",6.2e150, "White Gems", 1.5e57,"Crystal")),
        ("1e180 White Gems: 5e65 Crystal", lambda: reset_button("Main",1e180, "White Gems", 5e65,"Crystal")),
    ],
    "Iron": [
        ("3.2e51 Crystal: 120Sx Iron", lambda: reset_button("Main",3.2e51, "Crystal", 1.2e23,"Iron")),
        ("1.3e55 Crystal: 35Sp Iron", lambda: reset_button("Main",1.3e55, "Crystal", 3.5e25,"Iron")),
        ("7.2e60 Crystal: 16Oc Iron", lambda: reset_button("Main",7.2e60, "Crystal", 1.6e28,"Iron")),
        ("2.1e67 Crystal: 32No Iron", lambda: reset_button("Main",2.1e67, "Crystal", 3.2e31,"Iron")),
        ("1e74 Crystal: 500De Iron", lambda: reset_button("Main",1e74, "Crystal", 5e35,"Iron")),
    ],
    "Gold": [
        ("300Sp Iron: 2.1B Gold", lambda: reset_button("Main",3e26, "Iron", 2.1e9,"Gold")),
        ("6.2No Iron: 62B Gold", lambda: reset_button("Main",6.2e30, "Iron", 6.2e10,"Gold")),
        ("150De Iron: 210B Gold", lambda: reset_button("Main",1.5e35, "Iron", 2.1e11,"Gold")),
        ("6.2e38 Iron: 15T Gold", lambda: reset_button("Main",6.2e38, "Iron", 1.5e13,"Gold")),
    ],
    "Quartz": [
        ("230B Gold: 70k Quartz", lambda: reset_button("Main",2.3e11, "Gold", 7e4,"Quartz")),
        ("4.2T Gold: 230k Quartz", lambda: reset_button("Main",4.2e12, "Gold", 2.3e5,"Quartz")),
        ("84T Gold: 750k Quartz", lambda: reset_button("Main",8.4e13, "Gold", 7.5e5,"Quartz")),
        ("1.1Qd Gold: 3M Quartz", lambda: reset_button("Main",1.1e15, "Gold", 3e6,"Quartz")),
        ("750Qd Gold: 8M Quartz", lambda: reset_button("Main",7.5e17, "Gold", 8e6,"Quartz")),
        ("3.2Sx Gold: 300M Quartz", lambda: reset_button("Main",3.2e21, "Gold", 3e8,"Quartz")),
        ("710Sx Gold: 5B Quartz", lambda: reset_button("Main",7.1e23, "Gold", 5e9,"Quartz")),
    ],
    "Jade": [
        ("10M Quartz: 80 Jade", lambda: reset_button("Main",1e7, "Quartz", 80,"Jade")),
        ("200M Quartz: 300 Jade", lambda: reset_button("Main",2e8, "Quartz", 300,"Jade")),
        ("5B Quartz: 1k Jade", lambda: reset_button("Main",5e9, "Quartz", 1000,"Jade")),
        ("400B Quartz: 7.5k Jade", lambda: reset_button("Main",4e11, "Quartz", 7500,"Jade")),
        ("69T Quartz: 75.42k Jade", lambda: reset_button("Main",6.9e13, "Quartz", 7.542e4,"Jade")),
    ],
    "Obsidian": [
        ("75k Jade: 1 Obsidian", lambda: reset_button("Main",7.5e5, "Jade", 1,"Obsidian")),
    ],
    "Gem Buttons": [
        ("150 Jade: 17.5k Gems", lambda: cost_button("Main","Jade", 150, "Gems", 17500)),
        ("25M Quartz: 50k Gems", lambda: cost_button("Main","Quartz", 2.5e7, "Gems", 5e4)),
    ],
    "Recovery": [
        ("100 Jade: 5.2T White Gems (Fetch)", lambda: recovery_button_fetch("Main",100, "Jade", 5.2e12, "White Gems")),
    ],
    "Geodes": [
        ("Obsidian Geode: 1 Obsidian", lambda btn: Geode_roll(btn, obsidian_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
    ],
    "Area Teleports": [
       ("Spawn (req: 0 Cash)", lambda: load_check("Main",0, "Cash", Spawn_Buttons)),
       ("Recover Hall (req: 0 Cash)", lambda: load_check("Main",0, "Cash", Recover_Hall_Buttons))
    ]
}
Colour_Buttons = {
    "Multiplier": [
        ("3e955 Cash: 6e200 Multiplier", lambda: cost_button("Main","Cash",Mantissa(3,955),"Multiplier", 6e200)),
        ("7e1555 Cash: 1e500 Multiplier", lambda: cost_button("Main","Cash",Mantissa(7,1555),"Multiplier", Mantissa(1,500))),
        ("1e2062 Cash: 1e800 Multiplier", lambda: cost_button("Main","Cash",Mantissa(1,2062),"Multiplier", Mantissa(1,800))),
    ],
    "Rebirths": [
        ("6e751 Multiplier: 2e190 Rebirths", lambda: reset_button("Main",Mantissa(6,751),"Multiplier",2e190, "Rebirths")),
        ("3e1252 Multiplier: 9e300 Rebirths", lambda: reset_button("Main",Mantissa(3,1252),"Multiplier",Mantissa(9,300), "Rebirths")),
        ("1e1626 Multiplier: 5e450 Rebirths", lambda: reset_button("Main",Mantissa(1,1626),"Multiplier",Mantissa(5,450), "Rebirths")),
    ],
    "Stone": [
        ("5e451 Rebirths: 3e185 Stone", lambda: reset_button("Main",Mantissa(5,451), "Rebirths", 3e185, "Stone")),
        ("3e632 Rebirths: 1e255 Stone", lambda: reset_button("Main",Mantissa(3,632), "Rebirths", 1e255, "Stone")),
        ("6e952 Rebirths: 7e312 Stone", lambda: reset_button("Main",Mantissa(6,952), "Rebirths", Mantissa(7,312), "Stone")),
    ],
    "White Gems": [
        ("4e267 Stone: 5e80 White Gems", lambda: reset_button("Main",4e267, "Stone", 5e80,"White Gems")),
        ("1e527 Stone: 2e120 White Gems", lambda: reset_button("Main",Mantissa(1,527), "Stone", 2e120,"White Gems")),
        ("1e637 Stone: 6e135 White Gems", lambda: reset_button("Main",Mantissa(1,637), "Stone", 6e135,"White Gems")),
    ],
    "Crystal": [
        ("2e230 White Gems: 3e102 Crystal", lambda: reset_button("Main",2e230, "White Gems", 3e102,"Crystal")),
        ("5e310 White Gems: 4e141 Crystal", lambda: reset_button("Main",Mantissa(5,310), "White Gems", 4e141,"Crystal")),
        ("3e382 White Gems: 7e182 Crystal", lambda: reset_button("Main",Mantissa(3,382), "White Gems", 7e182,"Crystal")),
    ],
    "Iron": [
        ("3e300 Crystal: 2e62 Iron", lambda: reset_button("Main",Mantissa(3,300), "Crystal", 2e62,"Iron")),
        ("1e380 Crystal: 3e81 Iron", lambda: reset_button("Main",Mantissa(1,380), "Crystal", 3e81,"Iron")),
        ("5e462 Crystal: 1e102 Iron", lambda: reset_button("Main",Mantissa(5,462), "Crystal", 1e102,"Iron")),
    ],
    "Gold": [
        ("3e100 Iron: 3Qd Gold", lambda: reset_button("Main",3e100, "Iron", 3e15,"Gold")),
        ("1e140 Iron: 60Qd Gold", lambda: reset_button("Main",1e150, "Iron", 6e16,"Gold")),
        ("6e190 Iron: 4Qn Gold", lambda: reset_button("Main",6e190, "Iron", 4e18,"Gold")),
    ],
    "Quartz": [
        ("430Sp Gold: 23B Quartz", lambda: reset_button("Main",4.3e26, "Gold", 2.3e10,"Quartz")),
        ("72Oc Gold: 500B Quartz", lambda: reset_button("Main",7.2e28, "Gold", 5e11,"Quartz")),
        ("110No Gold: 30T Quartz", lambda: reset_button("Main",1.1e32, "Gold", 3e13,"Quartz")),
    ],
    "Jade": [
        ("15Qd Quartz: 100k Jade", lambda: reset_button("Main",1.5e16, "Quartz", 1e5,"Jade")),
        ("421Qd Quartz: 250k Jade", lambda: reset_button("Main",4.21e17, "Quartz", 2.5e5,"Jade")),
        ("6Qn Quartz: 825k Jade", lambda: reset_button("Main",6e18, "Quartz", 8.25e5,"Jade")),
    ],
    "Obsidian": [
        ("2M Jade: 3 Obsidian", lambda: reset_button("Main",2e6, "Jade", 3,"Obsidian")),
        ("10M Jade: 7 Obsidian", lambda: reset_button("Main",1e7, "Jade", 7,"Obsidian")),
    ],
    "Ruby": [
        ("60 Obsidian: 1 Ruby", lambda: reset_button("Main", 60, "Obsidian", 1, "Ruby"))
    ],
    "Emerald": [
        ("5 Ruby: 1 Emerald", lambda: cost_button("Main","Ruby",5, "Emerald", 1))
    ],
    "Sapphire": [
        ("5 Emerald: 1 Sapphire", lambda: cost_button("Main", "Emerald", 5, "Sapphire", 1)),
        ("100k Emerald: 4 Sapphire", lambda: cost_button("Main", "Emerald", 100000, "Sapphire", 4)),
    ],
    "Discount": [
        ("1Qn Starlight: 1 Neuron", lambda: cost_button("Main", "Starlight", 1e12, "Neuron", 1, "Geode")),
        ("15 Yrnote: 1 Antimatter", lambda: cost_button("Geode", "Yrnote", 15, "Antimatter", 1, "Geode")),
        ("100k Ion: 0.1 Uranium", lambda: cost_button("Main", "Ion", 1e5, "Uranium", 0.1)),
        ("1e3030 Stone: 1 Dezyp", lambda: cost_button("Main", "Stone", Mantissa(1,3030), "Dezyp", 1, "Geode")),
        ("10M Dezyp: 1 Podrillium", lambda: cost_button("Geode", "Dezyp", 1e7, "Podrillium", 1, "Geode")),
    ],
    "Geodes": [
        ("Ruby Geode: 100k Ruby", lambda btn: Geode_roll(btn, ruby_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
        ("Emerald Geode: 100k Emerald", lambda btn: Geode_roll(btn, emerald_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
        ("Sapphire Geode: 100k Sapphire", lambda btn: Geode_roll(btn, sapphire_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
    ],
    "Area Teleports": [
       ("Spawn (req: 0 Cash)", lambda: load_check("Main",0, "Cash", Spawn_Buttons)),
       ("Recover Hall (req: 0 Cash)", lambda: load_check("Main",0, "Cash", Recover_Hall_Buttons))
    ]
}
ET_Buttons = {
    "Ruby": [
        ("50Sx Obsidian: 3 Ruby", lambda: reset_button("Main", 5e22, "Obsidian", 3, "Ruby")),
        ("600Sp Obsidian: 10 Ruby", lambda: reset_button("Main", 6e26, "Obsidian", 10, "Ruby")),
        ("20No Obsidian: 40 Ruby", lambda: reset_button("Main", 2e31, "Obsidian", 40, "Ruby")),
    ],
    "Emerald": [
        ("3Qn Ruby: 5 Emerald", lambda: cost_button("Main","Ruby",3e18, "Emerald", 5)),
        ("400Qn Ruby: 14 Emerald", lambda: cost_button("Main","Ruby",4e20, "Emerald", 14)),
        ("10Sx Ruby: 40 Emerald", lambda: cost_button("Main","Ruby",1e22, "Emerald", 40)),
    ],
    "Sapphire": [
        ("2B Emerald: 10 Sapphire", lambda: cost_button("Main", "Emerald", 2e9, "Sapphire", 10)),
        ("50B Emerald: 30 Sapphire", lambda: cost_button("Main", "Emerald", 5e10, "Sapphire", 30)),
        ("400T Emerald: 100 Sapphire", lambda: cost_button("Main", "Emerald", 4e14, "Sapphire", 100)),
    ],
    "Diamond": [
        ("500k Sapphire: 1 Diamond", lambda: reset_button("Main", 5e5, "Sapphire", 1, "Diamond")),
        ("3M Sapphire: 3 Diamond", lambda: reset_button("Main", 3e6, "Sapphire", 3, "Diamond")),
        ("15M Sapphire: 10 Diamond", lambda: reset_button("Main", 1.5e7, "Sapphire", 10, "Diamond")),
    ],
    "Starlight": [
        ("5 Diamond: 1 Starlight", lambda: reset_button("Main", 5, "Diamond", 1, "Starlight")),
        ("30 Diamond: 4 Starlight", lambda: reset_button("Main", 30, "Diamond", 4, "Starlight")), 
        ("86 Diamond: 10 Starlight", lambda: reset_button("Main", 86, "Diamond", 10, "Starlight")),
    ],
    "Recovery": [
        ("1 Ruby: 50 Jade (Fetch)", lambda: recovery_button_fetch("Main",1, "Ruby", 50, "Jade")),
    ],
    "Geodes": [
        ("Diamond Geode: 2.5k Diamond", lambda btn: Geode_roll(btn, diamond_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
        ("Starlight Geode: 60 Starlight", lambda btn: Geode_roll(btn, starlight_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
        ("Ion Geode: 5 Ion", lambda btn: Geode_roll(btn, ion_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
    ],
    "Area Teleports": [
       ("Spawn (req: 0 Cash)", lambda: load_check("Main",0, "Cash", Spawn_Buttons)),
       ("Recover Hall (req: 0 Cash)", lambda: load_check("Main",0, "Cash", Recover_Hall_Buttons))
    ]
}
Ion_Buttons = {
    "Diamond": [
        ("50M Sapphire: 30 Diamond", lambda: reset_button("Main", 5e7, "Sapphire", 30, "Diamond")),
        ("80M Sapphire: 70 Diamond", lambda: reset_button("Main", 8e7, "Sapphire", 70, "Diamond")),
        ("525B Sapphire: 130 Diamond", lambda: reset_button("Main", 5.25e11, "Sapphire", 130, "Diamond")),
        ("20T Sapphire: 3220 Diamond", lambda: reset_button("Main", 2e13, "Sapphire", 30, "Diamond")),
        ("400Qd Sapphire: 750 Diamond", lambda: reset_button("Main", 4e17, "Sapphire", 750, "Diamond")),
    ],
    "Starlight": [
        ("375 Diamond: 25 Starlight", lambda: reset_button("Main", 375, "Diamond", 25, "Starlight")),
        ("900 Diamond: 40 Starlight", lambda: reset_button("Main", 900, "Diamond", 40, "Starlight")),
        ("5.5k Diamond: 100 Starlight", lambda: reset_button("Main", 5500, "Diamond", 100, "Starlight")),
    ],
    "Ion": [
        ("150 Starlight: 1 Ion", lambda: reset_button("Main", 150, "Starlight", 1, "Ion")),
    ],
    "Area Teleports": [
       ("Spawn (req: 0 Cash)", lambda: load_check("Main",0, "Cash", Spawn_Buttons)),
       ("Recover Hall (req: 0 Cash)", lambda: load_check("Main",0, "Cash", Recover_Hall_Buttons))
    ]
}
def open_stat_menu(parent, stat_increment):
    """
    PySide6 version of the Tkinter stat menu.
    Creates a scrollable window with live updating and dynamic row creation.
    """

    class StatMenu(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)

            self.setWindowTitle("Stats Menu")
            self.setStyleSheet("background-color: #212121; color: white;")
            self.resize(400, 500)

            # --- Scroll Area Setup ---
            outer_layout = QVBoxLayout(self)

            self.scroll_area = QScrollArea()
            self.scroll_area.setWidgetResizable(True)
            self.scroll_area.setStyleSheet("background-color: #2f2f2f;")

            outer_layout.addWidget(self.scroll_area)

            # Content widget inside scroll area
            self.content = QWidget()
            self.content.setStyleSheet("background-color: #2f2f2f;")
            self.grid = QGridLayout(self.content)
            self.grid.setAlignment(Qt.AlignTop)
            self.scroll_area.setWidget(self.content)

            # Store references to labels
            self.stat_labels = {}     # (category, stat_name) → QLabel
            self.current_row = 0

            # --- Header ---
            self._add_header()

            # --- Initial Population ---
            self._populate_initial_stats(stat_increment)

            # Timer for updating
            self.timer = QTimer()
            self.timer.timeout.connect(lambda: self.update_stats(stat_increment))
            self.timer.start(25)

        # -------------------------------------------------------

        def _add_header(self):
            header1 = QLabel("Stat")
            header1.setStyleSheet("font-weight: bold; font-size: 14px;")
            self.grid.addWidget(header1, self.current_row, 0)

            header2 = QLabel("Value")
            header2.setStyleSheet("font-weight: bold; font-size: 14px;")
            self.grid.addWidget(header2, self.current_row, 1)

            self.current_row += 1

        # -------------------------------------------------------

        def _populate_initial_stats(self, stat_increment):
            for category, stats in stat_increment.items():

                # Category label
                cat = QLabel(category)
                cat.setStyleSheet("font-weight: bold; font-size: 12px; margin-top: 8px;")
                self.grid.addWidget(cat, self.current_row, 0, 1, 2)
                self.current_row += 1
                if category == "Geode":
                    # master list with desired order
                    geode_ordered_stats = []
                    for geode_type, ordered_list in geode_list.items():
                        for stat_name in list(ordered_list.keys()):
                            if stat_name in stats:
                                geode_ordered_stats.append((stat_name, stats[stat_name]))
                    # add any new/unknown geode stats at the end
                    for stat_name, stat_data in stats.items():
                        if stat_name not in [name for name, _ in geode_ordered_stats]:
                            geode_ordered_stats.append((stat_name, stat_data))
                    stat_items = geode_ordered_stats
                else:
                    # Normal categories: keep existing order
                    stat_items = stats.items()
                for stat_name, stat_data in stat_items:
                    self._add_new_stat_row(category, stat_name, stat_data)

        # -------------------------------------------------------

        def _add_new_stat_row(self, category, stat_name, stat_data):

            # Stat name
            if stat_name in list(stat_gradients.keys()):
                gradient = stat_gradients[stat_name]["Colours"]
                angle = stat_gradients[stat_name]["Angle"]
            else:
                gradient = stat_gradients["Default"]["Colours"]
                angle = stat_gradients["Default"]["Angle"]
            name_label = GradientLabel(stat_name, gradient, angle)
            self.grid.addWidget(name_label, self.current_row, 0)

            # Value formatting
            value = stat_data.get("Value", 0)

            if isinstance(value, Mantissa):
                text = value.to_string()
            elif isinstance(value, (int, float)):
                text = str(round(value, 6))
            else:
                text = str(value)

            value_label = QLabel(text)
            self.grid.addWidget(value_label, self.current_row, 1, alignment=Qt.AlignRight)

            # Store for later updates
            self.stat_labels[(category, stat_name)] = value_label

            self.current_row += 1

        # -------------------------------------------------------

        def update_stats(self, stat_increment):

            # Update values of existing stats
            for (category, stat_name), label in list(self.stat_labels.items()):
                try:
                    value = stat_increment[category][stat_name]["Value"]

                    if isinstance(value, Mantissa):
                        text = value.to_string()
                    elif isinstance(value, (int, float)):
                        text = str(round(value, 6))
                    else:
                        text = str(value)

                    label.setText(text)

                except KeyError:
                    label.setText("N/A")

            # Detect new stats dynamically
            for category, stats in stat_increment.items():
                if category == "Geode":
                    # Ordered insertion for geode stats
                    geode_ordered_stats = []
                    for geode_type, ordered_list in geode_list.items():
                        for stat_name in list(ordered_list.keys()):
                            if stat_name in stats:
                                geode_ordered_stats.append((stat_name, stats[stat_name]))
                    # Include unknown/new geode stats at the end
                    for stat_name, stat_data in stats.items():
                        if stat_name not in [name for name, _ in geode_ordered_stats]:
                            geode_ordered_stats.append((stat_name, stat_data))
                    stat_items = geode_ordered_stats
                else:
                    stat_items = stats.items()
                for stat_name, stat_data in stat_items:
                    if (category, stat_name) not in self.stat_labels:
                        self._add_new_stat_row(category, stat_name, stat_data)

    # ----------------------------
    # Create and show the dialog
    # ----------------------------
    win = StatMenu(parent)
    win.show()
    return win
def open_boosts_menu():
  class UpgradeMenu(QWidget):
      def __init__(self, save_data):
          super().__init__()
  
          self.save_data = save_data
  
          self.setWindowTitle("Boosts")
          self.setWindowIcon(QIcon("Quant.png"))
          self.setMinimumSize(400, 500)
          self.setStyleSheet("background-color: #212121; color: white; padding: 1px; border: 1px solid white")
          # Scroll setup
          scroll = QScrollArea()
          scroll.setWidgetResizable(True)
          scroll.setStyleSheet("background-color: #2f2f2f;")
  
          container = QWidget()
          self.layout = QVBoxLayout(container)
  
          # Generate upgrade rows
          for upgrade_id, info in upgrades.items():
              self.add_upgrade_row(upgrade_id, info)
  
          scroll.setWidget(container)
  
          # Main layout
          outer = QVBoxLayout(self)
          outer.addWidget(scroll)
  
      def add_upgrade_row(self, upgrade_id, info):
          level = self.save_data[upgrade_id].get("current_lvl", 0)
          cost = upgrade_cost(info, level)
  
          row = QFrame()
          row_layout = QHBoxLayout(row)
  
          name_label = QLabel(f"{info['name']}")
          level_label = QLabel(f"Level: {level}/{info['max_level']}" if level < info['max_level'] else f"Level: MAX ({level}/{info['max_level']})")
          cost_label = QLabel(f"Cost: {cost} gems" if level < info['max_level'] else "Cost: MAX")
  
          buy_btn = QPushButton("Buy")
  
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
  
      def buy_upgrade(self, upgrade_id, info, level_label, cost_label, buy_button):
          level = self.save_data[upgrade_id].get("current_lvl", 0)
  
          # Maxed?
          if level >= info["max_level"]:
              return
  
          cost = upgrade_cost(info, level)
  
          # Check if player has enough gems
          if stat_increment["Main"]["Gems"]["Value"] < cost:
              return  # or display a popup
  
          # Apply purchase
          stat_increment["Main"]["Gems"]["Value"] -= cost
          level += 1
          self.save_data[upgrade_id]["current_lvl"] = level
  
          # Update UI
          level_label.setText(f"Level: {level}/{info['max_level']}")
          if level >= info["max_level"]:
              buy_button.setDisabled(True)
          else:
              cost_label.setText(f"Cost: {upgrade_cost(info, level)} gems")
  win = UpgradeMenu(upgrades)
  win.show()
  return win
stat_menu = QPushButton("Open Stat Menu")
stat_menu.clicked.connect(lambda: open_stat_menu(root, stat_increment))
boosts_menu = QPushButton("Boosts")
boosts_menu.clicked.connect(lambda: open_boosts_menu())
stylesheet = open("general.qss", "r")
stat_menu.setStyleSheet(stylesheet.read())
boosts_menu.setStyleSheet('''QPushButton {
                    background-color: #2f2f2f;
                    color: white;
                    padding: 6px;
                    border: 1px solid white;
                }
QPushButton:hover {
                    background-color: #222;
                }''') # It didn't seem to be working when I didn't do this >:(
layout.addWidget(stat_menu, 2, 0, 1, 1)
layout.addWidget(boosts_menu, 3, 0, 1, 1)
layout.addWidget(cash_l, 0, 1, 1, 1)
layout.addWidget(multi_l, 0, 2, 1, 1)
layout.addWidget(re_l, 0, 3, 1, 1)
root.setCentralWidget(central)
container, scroll_area, content = tkinter_frames.create_scrollable_area(root, Spawn_Buttons)
layout.addWidget(container, 2, 1, 3, 3)
layout.setColumnStretch(1, 1) # How to make things have the correct size 101
layout.setColumnStretch(2, 1)
layout.setColumnStretch(3, 1)

layout.setRowStretch(2, 1)
layout.setRowStretch(3, 1)
layout.setRowStretch(4, 1)
def play_music():
    '''This constantly loops background music'''
    i = 0
    while True:
      song = AudioSegment.from_mp3(music[i%len(music)])
      playback = sa.play_buffer( #Copy and paste
            song.raw_data,
            num_channels=song.channels,
            bytes_per_sample=song.sample_width,
            sample_rate=song.frame_rate
        )
      i += 1
      playback.wait_done() # This waits until the song is finished before continuing
stat_increment = Load()
# Run in a thread
threading.Thread(target=play_music, daemon=True).start()
cash_increase()
gem_increase()
root.show()

app.exec()