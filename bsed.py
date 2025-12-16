# Builtins/Must haves
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import json
import time
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
from Module import Mantissa, tkinter_frames, Geode, GradientLabel
try: #Unused imports
  import sqlalchemy
  import werkzeug
  import datetime
except ImportError:
    pass
try: #Audio imports
  from pydub import AudioSegment
  import simpleaudio as sa
except ImportError:
    print("The following Modules: pydub, simpleaudio have not been imported due to their excessive requirements for install. The program does not necessitate their presence for functionality however music shall not be played without them")

warnings.filterwarnings("ignore")
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
    def closeEvent(self, event: QCloseEvent):
      Save(stat_increment, upgrades, secrets)
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
    },
    "event_timer_amount": {
        "name": "More Event Power From Timer",
        "max_level": 800,
        "base_cost": 600000,
        "cost_growth": 1.01,
        "effect": 1000,
        "current_lvl": 0
    },
    "event_speed": {
        "name": "Faster Event Power From Timer",
        "max_level": 88,
        "base_cost": 250000,
        "cost_growth": 1.2,
        "effect": 5,
        "current_lvl": 0
    },
    "cash_multi_2": {
        "name": "More Cash Multiplier",
        "max_level": 1000,
        "base_cost": 5e7,
        "cost_growth": 1.01,
        "effect": 0.5,
        "current_lvl": 0
    },
    "super_lucky": {
        "name": "Super Lucky",
        "max_level": 6,
        "base_cost": 6e26,
        "cost_growth": 10,
        "effect": 0.5,
        "current_lvl": 0
    },
    "geode_express": {
        "name": "Geode Express",
        "max_level": 1,
        "base_cost": 1e57,
        "cost_growth": 1,
        "effect": 0.1,
        "current_lvl": 0
    },
    "offline_roll": {
        "name": "Offline Geodes",
        "max_level": 1,
        "base_cost": 1e63,
        "cost_growth": 1,
        "current_lvl": 0
    }
}
upgrades = def_upgrades
def_secrets = {
    "Darkmatter_1": False,
    "Darkmatter_2": False,
    "Darkmatter_3": False,
    "Darkmatter_4": False,
    "Darkmatter_5": False,
    "Galaxite_1": False,
    "Galaxite_2": False,
    "Galaxite_3": False
}
secrets = def_secrets
abs_stat_info = {
    "Main Progression": {
     "Cash":  {"Multis": None}, 
     "Multiplier":  {"Multis": None}, 
     "Rebirths":  {"Multis": {"Multiplier": 2}}, 
     "Stone": {"Multis": {"Cash": 1.5, "Rebirths": 2}}, 
     "White Gems": {"Multis": {"Multiplier": 1.5, "Stone": 1.8}}, 
     "Crystal": {"Multis": {"Cash": 2, "White Gems": 3}}, 
     "Iron": {"Multis": {"Rebirths": 1.5, "Crystal": 2}}, 
     "Gold": {"Multis": {"Cash": 2, "Stone": 2, "Iron": 2}}, 
     "Quartz": {"Multis": {"Multiplier": 10, "Rebirths": 2, "Stone": 5, "White Gems": 3, "Crystal": 2, "Gold": 2}}, 
     "Jade": {"Multis": {"Cash": 3, "Rebirths": 10, "Stone": 4, "Crystal": 4, "Quartz": 3}}, 
     "Obsidian": {"Multis": {"Rebirths": 15, "Stone": 15,"White Gems": 15, "Crystal": 10, "Iron": 10, "Gold": 7.5, "Jade": 5}}, 
     "Ruby": {"Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2}}, 
     "Emerald": {"Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2}}, 
     "Sapphire": {"Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2}}, 
     "Diamond": {"Multis": {"Emerald": 3, "Sapphire": 2}}, 
     "Starlight": {"Multis": {"Ruby": 6, "Sapphire": 3, "Diamond": 3}}, 
     "Ion": {"Multis": {"Jade": 4, "Ruby": 2, "Emerald": 10, "Sapphire": 1.4, "Diamond": 5, "Starlight": 5}}, 
     "Uranium": {"Multis": {"Crystal": 100, "Sapphire": 60, "Starlight": 5, "Ion": 2.2}}, 
     "Bismuth": {"Multis": {"Ruby": 50, "Emerald": 25, "Sapphire": 12, "Diamond": 3, "Ion": 2.5, "Uranium": 2}} , 
     "Boracite": {"Multis": {"Starlight": 5, "Uranium": 3, "Bismuth": 1.5}}, 
     "Nissonite": {"Multis": {"Obsidian": 5, "Bismuth": 2.75, "Boracite": 2.25}}, 
     "Orpiment": {"Multis": {"Cash": 23, "Multiplier": 22, "Rebirths": 21, "Stone": 20, "White Gems": 19, "Crystal": 18, "Iron": 17, "Gold": 16, "Quartz": 15, "Jade": 14, "Obsidian": 13, "Ruby": 12, "Emerald": 11, "Sapphire": 10, "Diamond": 9, "Starlight": 8, "Ion": 7, "Uranium": 6, "Bismuth": 5, "Boracite": 4, "Nissonite": 3}}, 
     "Tetra": {"Multis": {"Diamond": 1e4, "Boracite": 30, "Nissonite": 10, "Orpiment": 2.5}}, 
     "Volt": {"Multis": {"Uranium": 100, "Nissonite": 4, "Tetra": 2}}, 
     "Aquamarine": {"Multis": {"Obsidian": 1e6, "Ion": 500, "Uranium": 400, "Nissonite": 5, "Volt": 2.1}}, 
     "Lollipop": {"Multis": {"Emerald": 8152, "Sapphire": 4096, "Diamond": 2048, "Starlight": 1024, "Ion": 512, "Uranium": 256, "Bismuth": 128, "Boracite": 64, "Nissonite": 32, "Orpiment": 16, "Tetra": 8, "Volt": 4, "Aquamarine": 2}}, 
     "C0RR8PT10N": {"Multis": {"Cash": 6, "Multiplier": 6, "Rebirths": 6, "Stone": 6, "White Gems": 6, "Crystal": 6, "Iron": 6, "Gold": 6, "Quartz": 6, "Jade": 6, "Obsidian": 6, "Ruby": 6, "Emerald": 6, "Sapphire": 6, "Diamond": 6, "Starlight": 6, "Ion": 6, "Uranium": 6, "Bismuth": 6, "Boracite": 6, "Nissonite": 6, "Orpiment": 2.3, "Tetra": 6, "Volt": 6, "Aquamarine": 4, "Lollipop": 3}}, 
     "Stargazed Metal": {"Multis": {"Cash": 1e100, "Multiplier": 1e100, "Rebirths": 1e100, "Stone": 1e100, "White Gems": 1e100, "Crystal": 1e100, "Iron": 1e100, "Gold": 1e100, "Quartz": 1e100, "Jade": 1e100, "Obsidian": 7.5, "Ruby": 7.5, "Emerald": 7.5, "Aquamarine": 2.25, "Lollipop": 2.25, "C0RR8PT10N": 3}}, 
     "Gyge": {"Multis": {"Ruby": 1e25, "Emerald": 1e25, "Sapphire": 1e25, "Diamond": 1e25, "Starlight": 1e25, "Ion": 1e25, "Uranium": 1e25, "Bismuth": 1e25, "Boracite": 1e25, "Nissonite": 1e25, "Volt": 18, "Lollipop": 7, "C0RR8PT10N": 10, "Stargazed Metal": 2}}, 
     "Auly Plate": {"Multis": {"Cash": Mantissa(1,288290), "Orpiment": 1.61, "Tetra": 3.12, "Volt": 6.25, "Aquamarine": 12.5, "Lollipop": 18, "C0RR8PT10N": 50, "Stargazed Metal": 5, "Gyge": 2}}, 
     "Shell Piece": {"Multis": {"Cash": 1e75, "Multiplier": 1e75, "Rebirths": 1e75, "Stone": 1e75, "White Gems": 1e75, "Crystal": 1e75, "Iron": 1e75, "Gold": 1e75, "Quartz": 1e75, "Jade": 1e75, "Obsidian": 1e75, "Ruby": 1e75, "Emerald": 1e75, "Sapphire": 1e75, "Diamond": 1e75, "Starlight": 1e75, "Ion": 1e75, "Uranium": 1e75, "Bismuth": 1e75, "Boracite": 1e75, "Nissonite": 1e75, "Orpiment": 1e75, "Tetra": 100, "Volt": 100, "Aquamarine": 100, "Lollipop": 100, "C0RR8PT10N": 100, "Mint": 100, "Gems": 20, "Metal": 100, "Press": 100, "Microparticles": 100, "Star": 100, "Robot": 100, "Prototype": 100}}, 
     "Singularity": {"Multis": {"Cash": Mantissa(1,987654321), "Volt": 1200, "C0RR8PT10N": 150, "Gyge": 4, "Auly Plate": 2.5, "Gems": 75}}, 
     "Capsuled Singularity": {"Multis": {"Cash": Mantissa(1,303030303), "Ruby": Mantissa(1,266664), "Emerald": Mantissa(1,266664), "Sapphire": Mantissa(1,266664), "Diamond": Mantissa(1,266664), "Starlight": Mantissa(1,133337), "Ion": Mantissa(1,666666), "Uranium": Mantissa(1,333333), "Bismuth": Mantissa(1,12555), "Boracite": Mantissa(1,5555), "Nissonite": Mantissa(1,2222), "Orpiment": Mantissa(1,1000), "Tetra": Mantissa(1,500), "Volt": 1e150, "Aquamarine": 1e75, "Lollipop": 1e25, "C0RR8PT10N": 1e6, "Stargazed Metal": 2500, "Gyge": 500, "Auly Plate": 25, "Shell Piece": 2.5, "Prototype": 1240, "Gems": 300}}, 
     "Gems": {"Multis": None}, 
     "Event Power": {"Multis": None},
     "Mint": {"Multis": {"Multiplier": 1.5, "Rebirths": 1.3}}},
    "Mastery": {
        "Master Cash": {"Multis": {"Cash": 2}},
        "Master Multiplier": {"Multis": {"Multiplier": 2}},
        "Master Rebirths": {"Multis": {"Rebirths": 2, "Master Multiplier": 2}},
        "Master Stone": {"Multis": {"Stone": 2, "Master Cash": 1, "Master Rebirths": 1.75}},
        "Master White Gems": {"Multis": {"White Gems": 2, "Master Multiplier": 1.5, "Master Stone": 2}},
        "Master Crystal": {"Multis": {"Crystal": 2, "Master Cash": 1.5, "Master Multiplier": 1.5, "Master Rebirths": 1.5, "Master Stone": 1.5, "Master White Gems": 1.5}},
        "Master Iron": {"Multis": {"Iron": 2, "Master Cash": 2, "Master White Gems": 1.75, "Master Crystal": 2.5}},
        "Master Gold": {"Multis": {"Gold": 2, "Master Cash": 2, "Master Rebirths": 3, "Master White Gems": 2, "Master Iron": 2}},
        "Master Quartz": {"Multis": {"Quartz": 2, "Master Cash": 5, "Master Multiplier": 5, "Master Rebirths": 5, "Master Stone": 4, "Master Crystal": 2.2, "Master Iron": 1.8, "Master Gold": 3}},
        "Master Jade": {"Multis": {"Jade": 2, "Master Cash": 10, "Master Multiplier": 10, "Master Crystal": 5, "Master Iron": 4, "Master Quartz": 2}},
        "Master Obsidian": {"Multis": {"Obsidian": 2, "Master Stone": 5, "Master White Gems": 5, "Master Iron": 5, "Master Quartz": 3, "Master Jade": 2}},
        "Master Ruby": {"Multis": {"Ruby": 2, "Master Cash": 2.25, "Master Multiplier": 2.25, "Master Rebirths": 2.25, "Master Stone": 2.25, "Master White Gems": 2.25, "Master Crystal": 2.25, "Master Iron": 2.25, "Master Gold": 2.25, "Master Quartz": 2.25, "Master Jade": 2.25, "Master Obsidian": 2.25}},
        "Master Emerald": {"Multis": {"Emerald": 2, "Master Cash": 2, "Master Multiplier": 2, "Master Rebirths": 2, "Master Stone": 2, "Master White Gems": 2, "Master Crystal": 2, "Master Iron": 2, "Master Gold": 2, "Master Quartz": 2, "Master Jade": 2, "Master Obsidian": 2, "Master Ruby": 2}},
        "Master Sapphire": {"Multis": {"Sapphire": 2, "Master Cash": 1.75, "Master Multiplier": 1.75, "Master Rebirths": 1.75, "Master Stone": 1.75, "Master White Gems": 1.75, "Master Crystal": 1.75, "Master Iron": 1.75, "Master Gold": 1.75, "Master Quartz": 1.75, "Master Jade": 1.75, "Master Obsidian": 1.75, "Master Ruby": 1.75, "Master Emerald": 1.75}},
        "Master Diamond": {"Multis": {"Diamond": 2, "Master Cash": 6, "Master Multiplier": 6, "Master White Gems": 6, "Master Crystal": 6, "Master Gold": 6, "Master Quartz": 6, "Master Ruby": 3.33, "Master Emerald": 3.33, "Master Sapphire": 3.33}},
        "Master Starlight": {"Multis": {"Starlight": 2, "Master Cash": 66, "Master Multiplier": 66, "Master Rebirths": 66, "Master Stone": 15, "Master White Gems": 15, "Master Crystal": 15, "Master Iron": 15, "Master Gold": 15, "Master Quartz": 15, "Master Jade": 15, "Master Ruby": 6, "Master Ruby": 6, "Master Sapphire": 2.7, "Master Diamond": 2.5}},
        "Master Ion": {"Multis": {"Ion": 2, "Master Obsidian": 2, "Master Ruby": 3, "Master Emerald": 3.5, "Master Sapphire": 3, "Master Diamond": 2, "Master Starlight": 5}},
        "Master Uranium": {"Multis": {"Uranium": 2, "Master Quartz": 10, "Master Jade": 9, "Master Obsidian": 8, "Master Ruby": 7, "Master Emerald": 6, "Master Sapphire": 5, "Master Diamond": 4, "Master Starlight": 3, "Master Ion": 2}},
        "Master Bismuth": {"Multis": {"Bismuth": 2, "Master Cash": 150, "Master Multiplier": 150, "Master Rebirths": 150, "Master Diamond": 7, "Master Ion": 5, "Master Uranium": 3}},
        "Master Boracite": {"Multis": {"Boracite": 2, "Master Sapphire": 7, "Master Diamond": 6, "Master Starlight": 5, "Master Ion": 4, "Master Uranium": 3, "Master Bismuth": 2}},
        "Master Nissonite": {"Multis": {"Nissonite": 2, "Master Cash": 4, "Master Multiplier": 4, "Master Rebirths": 4, "Master Stone": 4, "Master White Gems": 4, "Master Crystal": 4, "Master Iron": 4, "Master Gold": 4, "Master Quartz": 4, "Master Jade": 4, "Master Obsidian": 4, "Master Ruby": 4, "Master Emerald": 4, "Master Sapphire": 4, "Master Diamond": 4, "Master Starlight": 4, "Master Ion": 4, "Master Uranium": 4, "Master Bismuth": 3, "Master Boracite": 2}},
        "Master Orpiment": {"Multis": {"Opriment": 2, "Master Cash": 1e10, "Master Multiplier": 1e10, "Master Rebirths": 1e10, "Master Obsidian": 100, "Master Diamond": 10, "Master Uranium": 3, "Master Bismuth": 2, "Master Boracite": 3, "Master Nissonite": 2}},
        "Master Tetra": {"Multis": {"Tetra": 2, "Master Multiplier": 2.5, "Master Stone": 2.5, "Master Crystal": 2.5, "Master Gold": 2.5, "Master Jade": 2.5, "Master Ruby": 2.5, "Master Sapphire": 2.5, "Master Starlight": 2.5, "Master Uranium": 2.5, "Master Boracite": 2.5, "Master Orpiment": 2.5}},
        "Master Volt": {"Multis": {"Volt": 2, "Master Cash": 25, "Master Multiplier": 24, "Master Rebirths": 23, "Master Stone": 22, "Master White Gems": 21, "Master Crystal": 20, "Master Iron": 19, "Master Gold": 18, "Master Quartz": 17, "Master Jade": 16, "Master Obsidian": 15, "Master Ruby": 14, "Master Emerald": 13, "Master Sapphire": 12, "Master Diamond": 11, "Master Starlight": 10, "Master Ion": 9, "Master Uranium": 8, "Master Bismuth": 7, "Master Boracite": 6, "Master Nissonite": 5, "Master Orpiment": 4, "Master Tetra": 3}},
        "Master Aquamarine": {"Multis": {"Aquamarine": 2, "Master Obsidian": 25, "Master Emerald": 6, "Master Sapphire": 12, "Master Diamond": 16, "Master Ion": 7, "Master Bismuth": 15, "Master Nissonite": 10, "Master Volt": 2}},
        "Master Lollipop": {"Multis": {"Lollipop": 2, "Master Gold": 500, "Master Quartz": 400, "Master Jade": 300, "Master Obsidian": 200, "Master Ruby": 100, "Master Starlight": 50, "Master Ion": 40, "Master Uranium": 20, "Master Bismuth": 10, "Master Orpiment": 5, "Master Tetra": 4, "Master Volt": 3, "Master Aquamarine": 2}},
        "Prime Alpha Key": {"Multis": {"Master Cash": 2, "Master Multiplier": 2, "Master Rebirths": 2, "Master Stone": 2, "Master White Gems": 2, "Master Crystal": 2, "Master Iron": 2, "Master Gold": 2, "Master Quartz": 2, "Master Jade": 2, "Master Obsidian": 2, "Master Ruby": 2, "Master Emerald": 2, "Master Sapphire": 2, "Master Diamond": 2, "Master Starlight": 2, "Master Ion": 2, "Master Uranium": 2, "Master Bismuth": 2, "Master Boracite": 2, "Master Nissonite": 2, "Master Orpiment": 2, "Master Tetra": 2, "Master Volt": 2, "Master Aquamarine": 2, "Master Lollipop": 2, "Master Mint": 2, "Master Gems": 2, "Master Event Power": 2}},
        "Master Mint": {"Multis": {"Mint": 2, "Master Rebirths": 100}},
        "Master Gems": {"Multis": {"Gems": 2}},
        "Master Event Power": {"Multis": {"Event Power": 2}}
    },
    "Extra": {
        "Buttons Pressed": {"Multis": None}, 
        "Geodes Opened": {"Multis": None}},
    "Exclusive": {
        "Testium": {"Multis": {"Cash": 26, "Multiplier": 25, "Rebirths": 24, "Stone": 23, "White Gems": 22, "Crystal": 21, "Iron": 20, "Gold": 19, "Quartz": 18, "Jade": 17, "Obsidian": 16, "Ruby": 15, "Emerald": 14, "Sapphire": 13, "Diamond": 12, "Starlight": 11, "Ion": 10, "Uranium": 9, "Bismuth": 8, "Boracite": 7, "Nissonite": 6, "Orpiment": 5, "Tetra": 4, "Volt": 3, "Aquamarine": 2, "Lollipop": 1}},
        "Alpha Point": {"Multis": {"Cash": 1.1, "Multiplier": 1.1, "Rebirths": 1.1}}},
    "Event": {
      "Leaf": {"Multis": None },
      "Acorn": {"Multis": { "Cash": 1.5, "Leaf": 2 } },
      "Chestnut": {"Multis": { "Multiplier": 2.2, "Acorn": 2 } },
      "Pine": {
        "Multis": { "White Gems": 3.6, "Acorn": 1.5, "Chestnut": 2.5 }
      },
      "Mushroom": {"Multis": { "Gold": 5, "Pine": 4, "Leaf": 2 } },
      "Wicked Branch": {
        "Multis": { "Jade": 15, "Chestnut": 2.5, "Mushroom": 3 }
      },
      "Candy": {"Multis": None },
      "Pumpkin": {"Multis": { "Rebirths": 1.5, "Candy": 1.25 } },
      "Bat": {
        "Multis": { "White Gems": 3, "Crystal": 2, "Pumpkins": 1.5 }
      },
      "Bone": {"Multis": {"Iron": 5, "Quartz": 2, "Candy": 2, "Bat": 2 }},
      "Clover": {"Multis": {"Cash": 1.1}},
      "Heart": {"Multis": {"Flower": 2, "Love": 1.35}},
      "Orange Pumpkin": {"Multis": {"White Gems": 1.75}},
      "Ray": {"Multis": {"Stone": 2, "White Gems": 1.1, "Sand": 1.5}},
      "Patriotic Crystal": {"Multis": {"Crystal": 2, "Ray": 2}},
      "Aureal Gem": {"Multis": {"Gold": 2.5, "Quartz": 1.8, "Sand": 3, "Patriotic Crystal": 2}},
      "Fragment": {"Multis": {"Cash": 10, "Multiplier": 10, "Rebirths": 10, "Stone": 10, "White Gems": 10, "Crystal": 10, "Iron": 10, "Gold": 10, "Quartz": 10, "Jade": 10, "Ruby": 2, "Diamond": 1.2, "Sand": 5, "Ray": 3, "Patriotic Crystal": 2.5, "Aureal Gem": 2}}
    },
    "Secret": {
        "Graphite": {"Multis": { "Orpiment": 4, "Tetra": 2 } },
        "Stellarite": {"Multis": { "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2.5 }},
        "Galaxite": {"Multis": {"Obsidian": 2.75,"Ruby": 5,"Emerald": 5,"Sapphire": 5,"Diamond": 2,"Starlight": 2}},
        "Starglass": {"Multis": {"Cash": Mantissa(1,303), "Multiplier": Mantissa(1,303), "Rebirths": Mantissa(1,303)}},
        "Darkmatter": {"Multis": {"Obsidian": Mantissa(1,303), "Tetra": 1000000.0, "Volt": 10000, "Aquamarine": 100,  "Lollipop": 10,  "C0RR8PT10N": 1.2}}
    },
    "Geode": {"Stone Geode": {
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
          "Sphene": {"Chance": 3, "Multis": {"Diamond": 5}},
          "Acid": {"Chance": 20, "Multis": {"Uranium": 1.4, "Starlight": 2}},
          "Niflhemite": {"Chance": 100, "Multis": {"Multiplier": 3, "Rebirths": 3, "White Gems": 3, "Quartz": 3, "Obsidian": 3, "Ruby": 3, "Diamond": 3, "Uranium": 3}},
          "Reactivite": {"Chance": 27500, "Multis": {"Starlight": 12, "Ion": 8, "Uranium": 5}},
          "Plutonerite": {"Chance": 125000, "Multis": {"Diamond": 80, "Starlight": 40, "Ion": 20, "Uranium": 10}}
      },
      "Sacred Geode": {
          "Grail": {"Chance": 2, "Multis": {"Starlight": 2, "Ion": 2, "Uranium": 2}},
          "Box": {"Chance": 3500000, "Multis": {"Obsidian": 3, "Ruby": 3, "Emerald": 3, "Sapphire": 3, "Bismuth": 3, "Boracite": 3}}
      },
      "Bismuth Geode": {
          "Lead": {"Chance": 2, "Multis": {"Iron": 10000, "Obsidian": 5, "Ruby": 5, "Emerald": 5, "Sapphire": 5, "Diamond": 5}},
          "Pseudomalachite": {"Chance": 10, "Multis": {"Diamond": 6, "Uranium": 2, "Bismuth": 1.15}},
          "Osmium": {"Chance": 1428, "Multis": {"Bismuth": 5}},
          "Yhed": {"Chance": 45000, "Multis": {"Cash": 80000, "Rebirths": 80000, "White Gems": 80000, "Iron": 80000, "Quartz": 800, "Obsidian": 800, "Emerald": 8, "Diamond": 8, "Ion": 8, "Bismuth": 8}},
          "Hexaferrum": {"Chance": 300000, "Multis": {"Ruby": 3000, "Emerald": 2000, "Sapphire": 1000, "Diamond": 160, "Uranium": 40, "Bismuth": 15, "Boracite": 3}}
      },
      "Boracite Geode": {
          "Spectrolite": {"Chance": 4000, "Multis": {"Starlight": 5, "Ion": 5, "Bismuth": 5, "Boracite": 3}},
          "Hectam": {"Chance": 25000, "Multis": {"Crystal": 100, "Quartz": 100, "Jade": 100, "Ruby": 100, "Emerald": 100, "Diamond": 100, "Boracite": 10}}
      },
      "Nissonite Geode": {
          "Frostone": {"Chance": 1250, "Multis": {"Rebirths": 15, "Crystal": 15, "Quartz": 15, "Sapphire": 15, "Diamond": 15, "Boracite": 15, "Nissonite": 4, "Mint": 1.04}},
          "Neptunian": {"Chance": 6666, "Multis": {"Cash": 2, "Multiplier": 3, "Rebirths": 30, "Ion": 1.5, "Uranium": 2, "Bismuth": 3, "Boracite": 30, "Nissonite": 10}},
          "Clouminance": {"Chance": 19000, "Multis": {"Diamond": 100, "Starlight": 100, "Ion": 100, "Boracite": 100, "Nissonite": 20}},
          "Galarium": {"Chance": 600000, "Multis": {"Diamond": 300, "Starlight": 300, "Nissonite": 45}},
          "Unova": {"Chance": 5000000, "Multis": {"Cash": 1111, "Multiplier": 1111, "Rebirths": 1111, "Stone": 1111, "White Gems": 1111, "Crystal": 1111, "Iron": 1111, "Gold": 1111, "Quartz": 1111, "Jade": 1111, "Obsidian": 1111, "Ruby": 1111, "Emerald": 1111, "Sapphire": 1111, "Diamond": 1111, "Starlight": 1111, "Ion": 1111, "Uranium": 1111, "Bismuth": 1111, "Boracite": 1111, "Nissonite": 111, "Orpiment": 7, "Mint": 11.1, "Gems": 1.1}}
      },
      "Orpiment Geode": {
          "Borax": {"Chance": 3, "Multis": {"Boracite": 20}},
          "Axiom": {"Chance": 10, "Multis": {"Boracite": 15, "Nissonite": 10}},
          "Vergemite": {"Chance": 33, "Multis": {"Bismuth": 25, "Orpiment": 1.01}},
          "Zanyte": {"Chance": 13000, "Multis": {"Iron": 10, "Gold": 10, "Quartz": 10, "Jade": 10, "Obsidian": 10, "Ruby": 10, "Emerald": 10, "Sapphire": 10, "Diamond": 10, "Starlight": 10, "Ion": 10, "Uranium": 10, "Bismuth": 10, "Boracite": 10, "Nissonite": 10, "Orpiment": 4}},
          "Secretum": {"Chance": 100000, "Multis": {"Orpiment": 12}},
          "Mortalstone": {"Chance": 750000, "Multis": {"Cash": 999, "Multiplier": 999, "Rebirths": 999, "Stone": 999, "White Gems": 999, "Crystal": 999, "Iron": 999, "Gold": 999, "Quartz": 999, "Jade": 999, "Obsidian": 999, "Ruby": 999, "Emerald": 999, "Sapphire": 999, "Diamond": 999, "Starlight": 999, "Ion": 999, "Uranium": 999, "Bismuth": 999, "Boracite": 100, "Nissonite": 100, "Orpiment": 15, "Gems": 10}}
      },
      "Mint Geode": {
          "Uzik": {"Chance": 69420, "Multis": {"Jade": 10, "Mint": 5}},
          "Omet": {"Chance": 133371, "Multis": {"Cash": 100000, "Mint": 20}}
      },
      "Hearted Geode": {
          "Sweet": {"Chance": 2, "Multis": {"Cash": 3, "Multiplier": 2, "Flower": 2.5, "Love": 1.5}},
          "Ichor Flower": {"Chance": 8, "Multis": {"Cash": 5, "Rebirths": 3, "Stone": 1.5, "Heart": 2}},
          "Halved Heart": {"Chance": 20, "Multis": {"White Gems": 2, "Love": 5, "Heart": 3}},
          "Rainbow": {"Chance": 100, "Multis": {"Cash": 3, "Multiplier": 3, "Rebirths": 3, "Crystal": 3, "Flower": 7, "Heart": 4}},
          "Unicorn": {"Chance": 333, "Multis": {"Cash": 7, "Multiplier": 7, "Rebirths": 7, "Stone": 7, "White Gems": 7, "Crystal": 7, "Flower": 7, "Heart": 7}},
          "Rose": {"Chance": 4000, "Multis": {"Gold": 5, "Quartz": 3, "Flower": 50, "Love": 20, "Heart": 10}},
          "Wickedite": {"Chance": 17500, "Multis": {"Stone": 10, "White Gems": 10, "Crystal": 10, "Iron": 10, "Gold": 10, "Quartz": 10, "Jade": 10, "Obsidian": 10, "Heart": 1/1.4}},
          "Heartium": {"Chance": 280000, "Multis": {"Multiplier": 100, "Stone": 100, "Crystal": 100, "Jade": 10, "Ruby": 5, "Sapphire": 3, "Flower": 50, "Love": 50, "Heart": 50}},
          "Eternal Rose": {"Chance": 1250000, "Multis": {"Cash": 1000, "Multiplier": 1000, "Stone": 1000, "White Gems": 1000, "Crystal": 1000, "Iron": 1000, "Gold": 1000, "Quartz": 1000, "Jade": 1000, "Obsidian": 1000, "Ruby": 100, "Emerald": 100, "Sapphire": 100, "Nissonite": 4, "Flower": 1000, "Love": 1000, "Heart": 1000}}
      },
      "Luck Geode": {
          "Lucky Clover": {"Chance": 4, "Multis": {"Cash": 2, "Clover": 1.05}},
          "Golden Clover": {"Chance": 20, "Multis": {"Cash": 1.8, "Multiplier": 1.75, "Clover": 1.15}},
          "Diamond Clover": {"Chance": 100, "Multis": {"Multiplier": 2, "Rebirths": 3.5, "Clover": 1.25}},
          "Leprechaun's Hat": {"Chance": 200, "Multis": {"Rebirths": 3, "Stone": 1.8, "Clover": 1.32}},
          "Supreme Clover": {"Chance": 12000, "Multis": {"Crystal": 3, "Quartz": 4.5, "Clover": 1.75}},
          "Cloverite": {"Chance": 35000, "Multis": {"Stone": 10, "Gold": 5, "Jade": 3, "Emerald": 1.25, "Clover": 2.5}},
          "Ace": {"Chance": 1600000, "Multis": {"Cash": 6, "Multiplier": 6, "Rebirths": 6, "Stone": 6, "Crystal": 6, "Quartz": 6, "Ruby": 6, "Emerald": 6, "Sapphire": 6, "Diamond": 6, "Clover": 12.5}},
          "777": {"Chance": 7777777, "Multis": {"Cash": 777, "Multiplier": 777, "Rebirths": 777, "Stone": 77, "White Gems": 77, "Crystal": 77, "Iron": 77, "Gold": 77, "Quartz": 77, "Jade": 77, "Obsidian": 77, "Ruby": 77, "Emerald": 77, "Sapphire": 77, "Clover": 77.7}}
      },
      "Clover Geode": {
          "Holy Clover": {"Chance": 3, "Multis": {"Quartz": 2, "Ruby": 1.5, "Clover": 1.45}},
          "Red Clover": {"Chance": 6, "Multis": {"Multiplier": 3, "White Gems": 1.15, "Obsidian": 3, "Ruby": 3, "Clover": 1.55}},
          "Death Clover": {"Chance": 20, "Multis": {"Stone": 5, "White Gems": 5, "Iron": 5, "Obsidian": 5, "Clover": 1.65}},
          "Oblivion Clover": {"Chance": 40, "Multis": {"Obsidian": 6, "Sapphire": 6, "Clover": 1.8}},
          "Giant Clover": {"Chance": 285, "Multis": {"Cash": 15, "Multiplier": 15, "Rebirths": 15, "Stone": 15, "Crystal": 15, "Clover": 2}},
          "Albino Clover": {"Chance": 1000, "Multis": {"Stone": 8, "White Gems": 8, "Iron": 8, "Ruby": 8, "Clover": 2.5}},
          "Tripetaled": {"Chance": 15000, "Multis": {"Cash": 3, "Multiplier": 3, "Rebirths": 3, "Stone": 3, "White Gems": 3, "Crystal": 3, "Iron": 3, "Gold": 3, "Quartz": 3, "Jade": 3, "Obsidian": 3, "Ruby": 3, "Emerald": 3, "Sapphire": 3, "Diamond": 3, "Clover": 3}},
          "Oddium": {"Chance": 55000, "Multis": {"Stone": 30, "Iron": 30, "Obsidian": 30, "Ruby": 30, "Emerald": 30, "Clover": 5}},
          "Dualpetaled": {"Chance": 120000, "Multis": {"Cash": 10, "Multiplier": 10, "Rebirths": 10, "Stone": 10, "White Gems": 10, "Crystal": 10, "Iron": 10, "Gold": 10, "Quartz": 10, "Jade": 10, "Clover": 10}},
          "Core Clover": {"Chance": 1000001, "Multis": {"Cash": 100, "Rebirths": 100, "White Gems": 100, "Gold": 100, "Jade": 100, "Ruby": 100, "Mint": 10, "Clover": 25}},
          "Luckant": {"Chance": 4500000, "Multis": {"Cash": 666, "Multiplier": 666, "Rebirths": 666, "Stone": 666, "White Gems": 66, "Iron": 666, "Gold": 66, "Quartz": 66, "Jade": 66, "Obsidian": 66, "Ruby": 66, "Emerald": 66, "Sapphire": 66, "Starlight": 6, "Ion": 6, "Uranium": 6, "Bismuth": 1.6}},
          "Jackpotium": {"Chance": 8000000, "Multis": {"Cash": 1e5, "Multiplier": 1e5, "Rebirths": 1e5, "Stone": 1e5, "White Gems": 1e5, "Crystal": 1e5, "Nissonite": 1000, "Orpiment": 8, "Clover": 1000}},
          "Reality": {"Chance": 50000000, "Multis": {"Cash": 1e9, "Multiplier": 1e9, "Rebirths": 1e9, "Stone": 1e9, "White Gems": 1e9, "Crystal": 1e9, "Iron": 1e9, "Gold": 1e9, "Quartz": 1e9, "Jade": 1e9, "Obsidian": 1e9, "Ruby": 1e9, "Emerald": 1e9, "Sapphire": 1e9, "Diamond": 1e9, "Starlight": 1e9, "Ion": 1e9, "Uranium": 1e5, "Bismuth": 1e5, "Boracite": 1e5, "Nissonite": 1e5, "Orpiment": 10, "Mint": 1e9, "Clover": 1e9}}
      },
      "Celebrative Geode": {
          "Goldenium": {"Chance": 2, "Multis": {"Cash": 1.5, "Multiplier": 1.2}},
          "Lightroom": {"Chance": 5, "Multis": {"Obsidian": 1.75}},
          "Dazzlium": {"Chance": 11, "Multis": {"Cash": 2, "Multiplier": 1.7, "Rebirths": 1.7}},
          "Juled": {"Chance": 50, "Multis": {"Rebirths": 2, "Stone": 1.8}},
          "Tempested": {"Chance": 400, "Multis": {"Rebirths": 3, "Crystal": 1.5}},
          "Cyclone": {"Chance": 13000, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2}},
          "Koanite": {"Chance": 21000, "Multis": {"Crystal": 5, "Quartz": 3}},
          "Torbdenum": {"Chance": 45000, "Multis": {"Gold": 12, "Jade": 10, "Obsidian": 5}},
          "Darnite": {"Chance": 100000, "Multis": {"Cash": 1000, "Ruby": 2, "Emerald": 2, "Sapphire": 2}},
          "Wubium": {"Chance": 500000, "Multis": {"Rebirths": 653, "Crystal": 25, "Obsidian": 8, "Diamond": 3}},
          "Woofern": {"Chance": 1150000, "Multis": {"Cash": 27, "Multiplier": 27, "Rebirths": 27, "Stone": 27, "White Gems": 27, "Crystal": 27, "Iron": 27, "Gold": 27, "Quartz": 27, "Jade": 27, "Obsidian": 27, "Ion": 10, "Bismuth": 2}},
          "Acastar": {"Chance": 4750000, "Multis": {"Rebirths": 100, "Quartz": 100, "Sapphire": 100, "Diamond": 100, "Starlight": 100, "Ion": 100}},
          "Zincton": {"Chance": 9000000, "Multis": {"Cash": 5, "Multiplier": 5, "Rebirths": 5, "Stone": 5, "White Gems": 5, "Crystal": 5, "Iron": 5, "Gold": 5, "Quartz": 5, "Jade": 5, "Orpiment": 3.5}},
          "Prismatum": {"Chance": 17500000, "Multis": {"Iron": 20, "Gold": 20, "Quartz": 20, "Jade": 20, "Obsidian": 20, "Ruby": 20, "Emerald": 20, "Sapphire": 20, "Diamond": 20, "Starlight": 20, "Ion": 20, "Uranium": 20, "Bismuth": 20, "Boracite": 20, "Nissonite": 20, "Orpiment": 8.5}}
    },
    "Spring Geode": {"Vine": {"Chance": 4, "Multis": {"Cash": 10, "Rebirths": 5}},
          "Dew": {"Chance": 6, "Multis": {"Cash": 25, "Multiplier": 30, "Stone": 20}},
          "Daisy": {"Chance": 12, "Multis": {"Cash": 100, "Stone": 25, "White Gems": 10}},
          "Tulip": {"Chance": 33, "Multis": {"Multiplier": 20, "Crystal": 10}},
          "Aster": {"Chance": 10000, "Multis": {"Stone": 1000, "Gold": 250, "Quartz": 100}},
          "Honeysuckle": {"Chance": 27500, "Multis": {"Rebirths": 2500, "Iron": 50, "Jade": 25}},
          "Trollius": {"Chance": 75000, "Multis": {"Stone": 1000, "Crystal": 250, "Gold": 200, "Jade": 100}},
          "Nymphea": {"Chance": 255000, "Multis": {"White Gems": 2500, "Quartz": 150, "Obsidian": 5}},
          "Sunflower": {"Chance": 800000, "Multis": {"Stone": 200, "Gold": 1000, "Ruby": 5}},
          "Yarrow": {"Chance": 3000000, "Multis": {"Cash": 1e6, "Ruby": 200, "Emerald": 200, "Sapphire": 200}},
          "Windflower": {"Chance": 5000000, "Multis": {"Multiplier": 10000, "Iron": 250, "Obsidian": 50, "Diamond": 15}},
          "Bachelor's Button": {"Chance": 12500000, "Multis": {"Rebirths": 1e5, "Gold": 500, "Emerald": 35, "Starlight": 5}}
     },
     "Easter Geode": {"Egg": {"Chance": 4, "Multis": {"Cash": 2}},
           "Tainted Egg": {"Chance": 5, "Multis": {"Cash": 10, "Multiplier": 10}},
           "Spotted Egg": {"Chance": 8, "Multis": {"Rebirths": 10}},
           "Equinox Egg": {"Chance": 20, "Multis": {"Stone": 10}},
           "Sugar Egg": {"Chance": 15000, "Multis": {"Multiplier": 100, "White Gems": 15, "Crystal": 10}},
           "Time Egg": {"Chance": 50500, "Multis": {"Quartz": 25, "Obsidian": 1.1}},
           "Malicious Egg": {"Chance": 125000, "Multis": {"Rebirths": 10000, "Iron": 1000, "Jade": 20}},
           "Stained Glass Egg": {"Chance": 6000000, "Multis": {"Stone": 3, "White Gems": 3, "Crystal": 3, "Iron": 3, "Gold": 3, "Quartz": 3, "Jade": 3, "Obsidian": 3, "Ruby": 3}},
           "Space Egg": {"Chance": 6000000, "Multis": {"White Gems": 42, "Crystal": 42, "Obsidian": 10, "Ruby": 2}},
           "Gravitational Egg": {"Chance": 6000000, "Multis": {"Cash": 4, "Multiplier": 4, "Rebirths": 4, "Stone": 4, "White Gems": 4, "Crystal": 4, "Iron": 4, "Gold": 4, "Quartz": 4, "Jade": 4, "Obsidian": 4}},
           "EGG9000": {"Chance": 6000000, "Multis": {"Stone": 9000, "White Gems": 9000, "Crystal": 9000, "Iron": 9000, "Gold": 9000, "Quartz": 900, "Jade": 90, "Obsidian": 9}},
           "Dust Devil Egg": {"Chance": 6000000, "Multis": {"Multiplier": 3e6, "White Gems": 300, "Quartz": 35, "Obsidian": 3, "Ruby": 2.5}},
           "Black Iron Fabergé": {"Chance": 25000000, "Multis": {"Iron": 1e12, "Obsidian": 1e6, "Uranium": 1.25}},
           "Gilded Fabergé": {"Chance": 25000000, "Multis": {"Cash": 1e12, "Stone": 1000, "Crystal": 500, "Emerald": 100, "Sapphire": 5}},
           "Royal Fabergé": {"Chance": 25000000, "Multis": {"Cash": 1e9, "Gold": 1e6, "Diamond": 5, "Uranium": 1.5}},
           "Easter Basket": {"Chance": 100000000, "Multis": {"Cash": 100, "Multiplier": 100, "Rebirths": 100, "Stone": 100, "White Gems": 100, "Crystal": 100, "Iron": 100, "Gold": 100, "Quartz": 100, "Jade": 100, "Obsidian": 100, "Ruby": 100, "Emerald": 100, "Sapphire": 100, "Diamond": 100, "Starlight": 100, "Ion": 100, "Uranium": 100, "Bismuth": 100, "Boracite": 25, "Nissonite": 10, "Orpiment": 5, "Orpiment_2": 5, "Tetra": 10000, "Volt": 100, "Aquamarine": 15, "Lollipop": 5, "Stargazed Metal": 15, "Gyge": 5, "Auly Plate": 2}},
           "Egg of Destiny": {"Chance": 1000000000000, "Multis": {"Cash": Mantissa(1,303), "Multiplier": Mantissa(1,303), "Rebirths": Mantissa(1,303), "Stone": Mantissa(1,303), "White Gems": Mantissa(1,303), "Crystal": Mantissa(1,303), "Iron": Mantissa(1,303), "Gold": Mantissa(1,303), "Quartz": Mantissa(1,303), "Jade": Mantissa(1,303), "Obsidian": Mantissa(1,303), "Ruby": Mantissa(1,303), "Emerald": Mantissa(1,303), "Sapphire": Mantissa(1,303), "Diamond": Mantissa(1,303), "Starlight": Mantissa(1,303), "Ion": Mantissa(1,303), "Uranium": Mantissa(1,303), "Bismuth": Mantissa(1,303), "Boracite": Mantissa(1,303), "Nissonite": Mantissa(1,303), "Orpiment": Mantissa(1,303), "Tetra": Mantissa(1,303), "Volt": Mantissa(1,303), "Aquamarine": Mantissa(1,303), "Lollipop": Mantissa(1,303), "C0RR8PT10N": Mantissa(1,303), "Stargazed Metal": 1e100, "Gyge": 1e50, "Auly Plate": 1e25, "Shell Piece": 100000, "Prime Alpha Key": 1000}}
    },
    "Fabled Geode": {"Shinestone": {"Chance": 5, "Multis": {"Cash": 1e12, "Rebirths": 1e9}},
           "Yen": {"Chance": 5, "Multis": {"Cash": 2, "Multiplier": 2}},
           "Ascension": {"Chance": 5, "Multis": {"Rebirths": 800, "Stone": 400, "White Gems": 200, "Crystal": 100, "Iron": 50, "Gold": 25}},
           "Translucid Gem": {"Chance": 10, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2}},
           "Luminant Crystal": {"Chance": 10, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2}},
           "Exotic Metal": {"Chance": 20, "Multis": {"Cash": 2, 'Multiplier': 2, "Rebirths": 2, "Stone": 2, "Crystal": 2}},
           "Polyhedral Gold": {"Chance": 20, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "Crystal": 2, "Iron": 2}},
           "Luxurious Quartz": {"Chance": 33, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "Crystal": 2, "Iron": 2, "Gold": 2}},
           "Scarlet Jade": {"Chance": 33, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2}},
           "Reflected Obsidian": {"Chance": 100, "Multis": {"Cash": 2, "Multiplier": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2}},
           "Chromio": {"Chance": 100, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2}},
           "Clusterized Diamond": {"Chance": 200, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2}},
           "Cosmodryal": {"Chance": 200, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2}},
           "Augmented Ion": {"Chance": 1000, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2, "Starlight": 2}},
           "Symmetrite": {"Chance": 1000, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2, "Ion": 2}},
           "Levigated Bismuth": {"Chance": 2000, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2, "Ion": 2, "Uranium": 2}},
           "Niflhemic Boracite": {"Chance": 4000, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2, "Ion": 2, "Uranium": 2, "Bismuth": 2}},
           "Encored Nissonite": {"Chance": 4000, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2, "Ion": 2, "Uranium": 2, "Bismuth": 2, "Boracite": 2}},
           "Ethereal Orpiment": {"Chance": 12500, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2, "Ion": 2, "Uranium": 2, "Bismuth": 2, "Boracite": 2, "Nissonite": 2}},
           "Charged Tetra": {"Chance": 30000, "Multis": {"Cash": 1.5, "Multiplier": 1.5, "Rebirths": 1.5, "Stone": 1.5, "White Gems": 1.5, "Crystal": 1.5, "Iron": 1.5, "Gold": 1.5, "Quartz": 1.5, "Jade": 1.5, "Obsidian": 1.5, "Ruby": 1.5, "Emerald": 1.5, "Sapphire": 1.5, "Diamond": 1.5, "Ion": 1.5, "Uranium": 1.5, "Bismuth": 1.5, "Boracite": 1.5, "Nissonite": 1.5, "Orpiment": 1.5}},
           "Overclocked Volt": {"Chance": 75000, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2, "Ion": 2, "Uranium": 2, "Bismuth": 2, "Boracite": 2, "Nissonite": 2, "Orpiment": 2}},
           "Agate": {"Chance": 125000, "Multis": {"Jade": 1e9, "Diamond": 1e9, "Ion": 1e5}},
           "Bustamite": {"Chance": 175000, "Multis": {"Iron": 1e9, "Sapphire": 1000, "Starlight": 20000}},
           "Polycrase": {"Chance": 262000, "Multis": {"Cash": 1e15, "Stone": 1e12, "Quartz": 1e9, "Ruby": 1e6}},
           "Stolzite": {"Chance": 363000, "Multis": {"Gold": 1e12, "Emerald": 1e9, "Uranium": 100}},
           "Zeunerite": {"Chance": 532000, "Multis": {"Jade": 1e12, "Emerald": 1e9, "Starlight": 1000, "Boracite": 100}},
           "Phosphophyllite": {"Chance": 750000, "Multis": {"Sapphire": 1e9, "Diamond": 2e6, "Ion": 1000, "Uranium": 400}},
           "Haxonite": {"Chance": 958000, "Multis": {"Ruby": 1e6, "Emerald": 1e15, "Starlight": 1e12, "Boracite": 600}},
           "Glaucodot": {"Chance": 987000, "Multis": {"Diamond": 1000, "Starlight": 1000, "Ion": 1000, "Uranium": 1000, "Bismuth": 1e6}},
           "Dyscrasite": {"Chance": 1525000, "Multis": {"Sapphire": 1e7, "Ion": 10000, "Boracite": 1000, "Nissonite": 10}},
           "Bazzite": {"Chance": 3321000, "Multis": {"Jade": 1e15, "Diamond": 1e9, "Bismuth": 100000, "Nissonite": 100}},
           "Cornubite": {"Chance": 5216000, "Multis": {"Emerald": 1e12, "Ion": 1e6, "Boracite": 100000, "Nissonite": 1000}},
           "Kostovite": {"Chance": 7521000, "Multis": {"Sapphire": 1e15, "Starlight": 1.9e10, "Nissonite": 10000, "Orpiment": 15}},
           "Minium": {"Chance": 10526000, "Multis": {"Diamond": 1e15, "Bismuth": 100000, "Orpiment": 100}},
           "Nyerereite": {"Chance": 22878000, "Multis": {"Ruby": 1e21, "Uranium": 1e12, "Orpiment": 650}},
           "Peridot": {"Chance": 60648000, "Multis": {"Obsidian": 1e99, "Starlight": 1e21, "Nissonite": 1e6, "Opriment": 5000}},
           "Realgar": {"Chance": 80632000, "Multis": {"Diamond": 1e22, "Ion": 1e12, "Opriment": 500, "Tetra": 1.25}},
           "Ereus": {"Chance": 100742000, "Multis": {"Cash": Mantissa(1,300), "Ruby": 1e33, "Bismuth": 1e15, "Nissonite": 1e9, "Tetra": 1e10, "Volt": 50000, "Aquamarine": 1000, "Lollipop": 25, "Stargazed Metal": 20, "Gyge": 5, "Auly Plate": 3, "Shell Piece": 1.1}},
           "Existence": {"Chance": 500000000, "Multis": {"Cash": Mantissa(1,303), "Multiplier": Mantissa(1,303), "Rebirths": Mantissa(1,303), "Stone": Mantissa(1,303), "White Gems": Mantissa(1,303), "Crystal": Mantissa(1,303), "Iron": 1e273, "Gold": 1e243, "Quartz": 1e213, "Jade": 1e183, "Obsidian": 1e153, "Ruby": 1e123, "Emerald": 1e93, "Sapphire": 1e63, "Diamond": 1e45, "Starlight": 1e30, "Ion": 1e15, "Uranium": 1e12, "Bismuth": 1e9, "Boracite": 1e6, "Nissonite": 10000, "Orpiment": 100, "Tetra": 4, "Aquamarine": 1e9, "Lollipop": 150, "C0RR8PT10N": 5, "Gyge": 97.2, "Auly Plate": 10, "Shell Piece": 3}}
    }
  }
}
def_stat_increment = {"Stats":{}}
for cat, item in abs_stat_info.items():
    if cat != "Geode":
      for key in item.keys():
          def_stat_increment["Stats"][key] = 0
    else:
      for g_cat, g_item in item.items():
          for key in g_item.keys():
            def_stat_increment["Stats"][key] = 0
def_stat_increment["Stats"]["Testium"] = 1
stat_increment = def_stat_increment
abs_stat_info["Exclusive"]["Ivory"] = {"Multis": {item: 1.5 for item in def_stat_increment["Stats"].keys()}}
def_stat_increment["Stats"]["Ivory"] = 0
e_event = True
cash_type = "Cash"
multi_type = "Multiplier"
rebirth_type = "Rebirths"
gem_type = "Gems"
e_type = "Event Power"
reset_key = "Main Progression"
stat_gradients = {
    "Gems": {"Colours": ["#f9fb7c", "#fefe01"], "Angle": 180},
    "Event Power": {"Colours": ["#00ff7c", "#00ff02"], "Angle": 180},
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
    "Mint": {"Colours": ["#c6ffd0", "#58fbd7"], "Angle": 90},
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
    "Grail": {"Colours": ["#faa701", "#f3f37a"], "Angle": 90},
    "Box": {"Colours": ["#a25320", "#aa555c"], "Angle": 90},
    "Lead": {"Colours": ["#1e2020", "#191b1c"], "Angle": 90},
    "Pseudomalachite": {"Colours": ["#00b995", "#00f1ea"], "Angle": 90},
    "Osmium": {"Colours": ["#a9cec7", "#7fc4b6"], "Angle": 90},
    "Yhed": {"Colours": ["#2c251b", "#2c251b"], "Angle": 90},
    "Hexaferrum": {"Colours": ["#8ee2fd", "#d5ffc7"], "Angle": 90},
    "Spectrolite": {"Colours": ["#1f1c3f", "#d5ffcf"], "Angle": 180},
    "Hectam": {"Colours": ["#5510ff", "#5544ff"], "Angle": 180},
    "Frostone": {"Colours": ["#00d6db", "#005a6d"], "Angle": 180},
    "Neptunian": {"Colours": ["#0015ff", "#0050ff"], "Angle": 180},
    "Clouminance": {"Colours": ["#6dded0", "#2a565f"], "Angle": 180},
    "Galarium": {"Colours": ["#7700ff", "#090088", "#7700ff"], "Angle": 145},
    "Unova": {"Colours": ["#00ffff", "#000000", "#00ffff"], "Angle": 145},
    "Borax": {"Colours": ["#ac5353", "#52adad"], "Angle": 90},
    "Axiom": {"Colours": ["#1d72ff", "#388dff"], "Angle": 90},
    "Vergemite": {"Colours": ["#cd3d00", "#7e1900"], "Angle": 90},
    "Zanyte": {"Colours": ["#cb4eb1", "#5af609"], "Angle": 90},
    "Secretum": {"Colours": ["#ff7700", "#ff6161"], "Angle": 180},
    "Mortalstone": {"Colours": ["#ff00ff", "#ff00ff", "#000000", "#000000"], "Angle": 145},
    "Uzik": {"Colours": ["#269069", "#2cb196"], "Angle": 90},
    "Omet": {"Colours": ["#55D946", "#55D946"], "Angle": 0},
    "Badges": {"Colours":
    ["#b50202",
        "#b50202",
        "#9af119",
        "#ea5bda",
        "#a356ef",
        "#a356ef"],
        "Angle": 9},
    "Stellarite": {"Colours": ["#094887", "#015e8c"], "Angle": 90},
    "Galaxite": {"Colours": ["#821ced", "#2f2f2f", "#6e2eea"], "Angle": 180},
    "Graphite": {"Colours": ["#ed3636", "#757780", "#4866d0"], "Angle": 90},
    "Darkmatter": {"Colours": ["#000000", "#000000"], "Angle": 90},
    "Starglass": {"Colours": ["#1b74ff", "#4226ff"], "Angle": 90, "S_Colour": "#000000", "S_Width": 1.5},
    "Testium": {"Colours": ["#4747f3", "#34348c", "#0000ff"], "Angle": 145},
    "Ivory": {"Colours": ["#fef5ba", "#d3f5ea"], "Angle": 90},
    "Alpha Point": {"Colours": ["#ff7fff", "#d935e6"], "Angle": 90},
    "Leaf": {"Colours": ["#ffdc7f", "#ffdc7f"], "Angle": 0},
    "Acorn": {"Colours": ["#787822", "#787822"], "Angle": 0},
    "Pine": {"Colours": ["#6d3800", "#6d3800"], "Angle": 0},
    "Chestnut": {"Colours": ["#643920", "#724a33"], "Angle": 135},
    "Candy": {"Colours": ["#ffffff", "#ffaa01", "#ffffff", "#ffaa01", "#edca86"], "Angle": 90},
    "Bat": {"Colours": ["#000000", "#18181e"], "Angle": 135},
    "Wicked Branch": {"Colours": ["#0a1f28", "#1d1811"], "Angle": 135},
    "Bone": {"Colours": ["#e0e0e0", "#8c8c8c"], "Angle": 180},
    "Mushroom": {"Colours": ["#ff8a8a", "#ff0c0c", "#ffffff", "#ff0c0c", "#ffffff", "#ff5959"], "Angle": 90},
    "Pumpkin": {"Colours": ["#ffff00", "#ffbc63"], "Angle": 135},
    "Clover": {"Colours": ["#40ff7f", "#14ff74"], "Angle": 135},
    "Heart": {"Colours": ["#ff007f", "#ff004e"], "Angle": 135},
    "Orange Pumpkin": {"Colours": ["#c8640c", "#5b3311"], "Angle": 135},
    "Ray": {"Colours": ["#ffeca7", "#fff2c0"], "Angle": 90},
    "Patriotic Crystal": {"Colours": ["#ff7e7e", "#ffffff", "#8bbfff"], "Angle": 135},
    "Aureal Gem": {"Colours": ["#ffff7f", "#f890ff"], "Angle": 135},
    "Fragment": {"Colours": ["#ffffff", "#434343"], "Angle": 135},
    "Sweet": {"Colours": ["#f9a7f9", "#ffaa7f"], "Angle": 90},
    "Ichor Flower": {"Colours": ["#ffaa7f", "#aa0000"], "Angle": 90},
    "Halved Heart": {"Colours": ["#ff0000", "#000000"], "Angle": 90},
    "Rainbow": {"Colours": ["#ff0000", "#ff7600", "#eee300", "#7bf72e", "#01fcc7", "#005dfe", "#ff00ea"], "Angle": 90},
    "Unicorn": {"Colours": ["#55aaff", "#ffaaff"], "Angle": 90},
    "Rose": {"Colours": ["#fe577e", "#a0fa03"], "Angle": 90},
    "Wickedite": {"Colours": ["#55557f", "#aa557f"], "Angle": 90},
    "Heartium": {"Colours": ["#ff53fa", "#f70202"], "Angle": 90},
    "Eternal Rose": {"Colours": ["#4a68f9", "#01fdfe"], "Angle": 90},
    "Lucky Clover": {"Colours": ["#d0f37a", "#1aff7f"], "Angle": 180},
    "Golden Clover": {"Colours": ["#ffec1d", "#f0af7f"], "Angle": 180},
    "Diamond Clover": {"Colours": ["#3ec1ff", "#00ffad"], "Angle": 90},
    "Leprechaun's Hat": {"Colours": ["#55ff00", "#000000", "#ffff00", "#000000", "#55ff00"], "Angle": 90},
    "Supreme Clover": {"Colours": ["#54c8fa", "#8affff"], "Angle": 90},
    "Cloverite": {"Colours": ["#3d3d3d", "#59a57e", "#777979", "#57f608", "#777979", "#59a57e", "#3d3d3d"], "Angle": 145},
    "Ace": {"Colours": ["#000000", "#fe0000", "#00003a", "#0000ec", "#00003a", "#fe0000", "#000000"], "Angle": 145},
    "777": {"Colours": ["#000000", "#ffff00", "#000000", "#ffff00", "#000000", "#ffff00", "#000000"], "Angle": 145},
    "Holy Clover": {"Colours": ["#87ffe5", "#23ff99"], "Angle": 90},
    "Red Clover": {"Colours": ["#c8371b", "#36c965"], "Angle": 90},
    "Death Clover": {"Colours": ["#00351a", "#00cc66"], "Angle": 90},
    "Oblivion Clover": {"Colours": ["#2b297f", "#08d87f"], "Angle": 90},
    "Giant Clover": {"Colours": ["#009c61", "#00e376"], "Angle": 90},
    "Albino Clover": {"Colours": ["#ffffff", "#ff0000", "#ffffff", "#55ffaa"], "Angle": 90},
    "Tripetaled": {"Colours": ["#00ff7f", "#00b915"], "Angle": 90},
    "Oddium": {"Colours": ["#585800", "#000000", "#5d0000"], "Angle": 90},
    "Dualpetaled": {"Colours": ["#3dc25c", "#17e823"], "Angle": 90},
    "Core Clover": {"Colours": ["#00c3e8", "#00e6ca"], "Angle": 90},
    "Luckant": {"Colours": ["#55ff00", "#55fff6", "#55ff00"], "Angle": 145},
    "Jackpotium": {"Colours": ["#000000", "#ffff00", "#000000", "#fa6801", "#ffff00", "#fa6801", "#000000", "#ffff00", "#000000"], "Angle": 145},
    "Reality": {"Colours": ["#ffffff", "#ffffff", "#2f2f2f", "#ffffff", "#ffffff"], "Angle": 145, "S_Colour": "#8f93bc", "S_Width": 1},
    "Goldenium": {"Colours": ["#ffff7f", "#ffff7f"], "Angle": 90},
    "Lightroom": {"Colours": ["#ffdfff", "#f255f2", "#ffdfff"], "Angle": 180},
    "Dazzlium": {"Colours": ["#f9a754", "#ff7c00"], "Angle": 180},
    "Juled": {"Colours": ["#47f17f", "#18c27f"], "Angle": 180},
    "Tempested": {"Colours": ["#07004c", "#260148"], "Angle": 180},
    "Cyclone": {"Colours": ["#103e3f", "#103e3f", "#103e3f", "#00d7dc", "#103e3f", "#103e3f", "#103e3f"], "Angle": 180},
    "Koanite": {"Colours": ["#100e02", "#282602", "#100e02"], "Angle": 180},
    "Torbdenum": {"Colours": ["#1f5340", "#39845f", "#1f5340"], "Angle": 180},
    "Darnite": {"Colours": ["#170d00", "#3e7300", "#390800"], "Angle": 180},
    "Wubium": {"Colours": ["#5500ff", "#55557f", "#5500ff"], "Angle": 145},
    "Woofern": {"Colours": ["#47475c", "#47475c", "#525277", "#474761", "#474761"], "Angle": 180, "S_Colour": "#353675", "Angle": 180},
    "Acastar": {"Colours": ["#ffff0d", "#a2ff5d", "#5cffa3", "#1bffff"], "Angle": 90},
    "Zincton": {"Colours": ["#ffff00", "#ffff00"], "Angle": 90},
    "Prismatum": {"Colours": ["#000000", "#02a3f2", "#54f303", "#fd0d0d", "#ffffff"], "Angle": 90},
    "Vine": {"Colours": ["#047354", "#00674a", "#007f5d"], "Angle": 90},
    "Dew": {"Colours": ["#9ed5b5", "#a7d8d8"], "Angle": 90},
    "Daisy": {"Colours": ["#fbff82", "#edf074"], "Angle": 90},
    "Tulip": {"Colours": ["#f24e25", "#faea04"], "Angle": 180},
    "Aster": {"Colours": ["#c426ff", "#c426ff"], "Angle": 90},
    "Honeysuckle": {"Colours": ["#ffffb8", "#fcff49", "#ffffb8"], "Angle": 90},
    "Trollius": {"Colours": ["#ffeda6", "#ffeda6"], "Angle": 90},
    "Nymphea": {"Colours": ["#ffc765", "#d4bafb", "#ffc765"], "Angle": 90},
    "Sunflower": {"Colours": ["#f4ff6a", "#fefd97", "#ffdd52"], "Angle": 90},
    "Yarrow": {"Colours": ["#ff858c", "#f44d6c", "#ff6f89"], "Angle": 90},
    "Windflower": {"Colours": ["#8cf3f4", "#70c0b8", "#a3f3cf"], "Angle": 90},
    "Bachelor's Button": {"Colours": ["#091df9", "#63adba", "#091df9"], "Angle": 90},
    "Egg": {"Colours": ["#fed1ab", "#fcabd9"], "Angle": 90},
    "Tainted Egg": {"Colours": ["#d5badb", "#a6fea1", "#b3dadb"], "Angle": 90},
    "Spotted Egg": {"Colours": ["#f5ff9b", "#000000", "#a1fbff", "#000000", "#acffaa"], "Angle": 90},
    "Equinox Egg": {"Colours": ["#323232", "#c0c0c0"], "Angle": 90},
    "Sugar Egg": {"Colours": ["#e188d6", "#fda5e3", "#e188d6"], "Angle": 90},
    "Time Egg": {"Colours": ["#8f743a", "#44371a", "#8f743a"], "Angle": 90},
    "Malicious Egg": {"Colours": ["#246800", "#c2fe9d", "#246800", "#86ff79"], "Angle": 145},
    "Stained Glass Egg": {"Colours": ["#9ff8fc", "#b4aaff", "#fcabd9"], "Angle": 90},
    "Space Egg": {"Colours": ["#382932", "#332b56"], "Angle": 90},
    "Gravitational Egg": {"Colours": ["#0008b2", "#0039ff"], "Angle": 90},
    "EGG9000": {"Colours": ["#ff005a", "#ff0087", "#ff005a"], "Angle": 90},
    "Dust Devil Egg": {"Colours": ["#ffbb45", "#ffd07e", "#ffbb45"], "Angle": 90},
    "Black Iron Fabergé": {"Colours": ["#101010", "#2a2a2a", "#101010"], "Angle": 90},
    "Gilded Fabergé": {"Colours": ["#857608", "#f6d519", "#99771f"], "Angle": 90},
    "Royal Fabergé": {"Colours": ["#a811ff", "#fc279d"], "Angle": 90},
    "Easter Basket": {"Colours": ["#fcb1ad", "#fbfca6", "#c4feb4", "#aaaaf5", "#f5a4f7", "#ffa4b0"], "Angle": 90},
    "Egg of Destiny": {"Colours": ["#ffffff", "#ffffff", "#000000", "#ffffff", "#ffffff"], "Angle": 145},
    "Shinestone": {"Colours": ["#383838", "#ffff7f"], "Angle": 90},
    "Yen": {"Colours": ["#a59a43", "#fefea5", "#bfc043"], "Angle": 90},
    "Ascension": {"Colours": ["#0016fe", "#003fff"], "Angle": 90},
    "Translucid Gem": {"Colours": ["#99fdff", "#5cffff", "#98ffd2"], "Angle": 90},
    "Luminant Crystal": {"Colours": ["#e981ff", "#f166f4", "#80c3f3"], "Angle": 90},
    "Exotic Metal": {"Colours": ["#a8a985", "#f4f5a6", "#9c9d7a"], "Angle": 90},
    "Polyhedral Gold": {"Colours": ["#728f5d", "#b3b507", "#728f5d"], "Angle": 90},
    "Luxurious Quartz": {"Colours": ["#86e6db", "#d09ff9", "#f3d1aa"], "Angle": 90},
    "Scarlet Jade": {"Colours": ["#b15291", "#43654a", "#b15291"], "Angle": 90},
    "Reflected Obsidian": {"Colours": ["#1d181a", "#7a636e", "#5b4c62", "#151117"], "Angle": 90},
    "Chromio": {"Colours": ["#868700", "#22f300", "#0d857a"], "Angle": 90},
    "Clusterized Diamond": {"Colours": ["#fbb4ff", "#bdf8f2", "#fbb4ff", "#bdf8f2", "#fbb4ff", "#bdf8f2", "#fbb4ff", "#bdf8f2", "#fbb4ff"]},
    "Cosmodryal": {"Colours": ["#6826ff", "#9483fa"], "Angle": 90},
    "Augmented Ion": {"Colours": ["#ff0000", "#000000", "#52ec04"], "Angle": 90},
    "Symmetrite": {"Colours": ["#5500fd", "#f10014", "#51e606"], "Angle": 90},
    "Levigated Bismuth": {"Colours": ["#cbc7ff", "#b4ddc0", "#e9e5a9", "#f0afc2", "#cbc7ff"], "Angle": 90},
    "Niflhemic Boracite": {"Colours": ["#00ffff", "#5500ff"], "Angle": 90},
    "Encored Nissonite": {"Colours": ["#aaffff", "#5fffff", "#aaffff", "#5fffff"], "Angle": 90},
    "Ethereal Orpiment": {"Colours": ["#ff5500", "#049fed"], "Angle": 90},
    "Charged Tetra": {"Colours": ["#0055ff", "#fc0103", "#0055ff"], "Angle": 90},
    "Overclocked Volt": {"Colours": ["#ffff00", "#ffffff", "#ffff00"], "Angle": 90},
    "Agate": {"Colours": ["#afffff", "#ffffff"], "Angle": 90},
    "Bustamite": {"Colours": ["#555500", "#551800"], "Angle": 90},
    "Polycrase": {"Colours": ["#ffff7f", "#ffaa7f"], "Angle": 90},
    "Stolzite": {"Colours": ["#fc5400", "#aaaa00"], "Angle": 90},
    "Zeunerite": {"Colours": ["#f50202", "#ff5500"], "Angle": 90},
    "Phosphophyllite": {"Colours": ["#5555ff", "#00ffff", "#00aaff"], "Angle": 90},
    "Haxonite": {"Colours": ["#55ff7f", "#000000"], "Angle": 90},
    "Glaucodot": {"Colours": ["#ffffff", "#8a694c", "#ffffff"], "Angle": 90},
    "Dyscrasite": {"Colours": ["#5e5e5e", "#ffffff"], "Angle": 90},
    "Bazzite": {"Colours": ["#97e1f5", "#3fd2ff"], "Angle": 90},
    "Cornubite": {"Colours": ["#a9fd7e", "#a9fd00"], "Angle": 90},
    "Kostovite": {"Colours": ["#eea0ee", "#ffffff", "#eea0ee", "#ffffff", "#eea0ee"], "Angle": 90},
    "Minium": {"Colours": ["#5e5e12", "#a7a77a", "#5e5e12"], "Angle": 90},
    "Nyerereite": {"Colours": ["#00aa05", "#33aa7f"], "Angle": 90},
    "Peridot": {"Colours": ["#07a07b", "#54fefe", "#02ac82"], "Angle": 90},
    "Realgar": {"Colours": ["#ff0300", "#fffa00"], "Angle": 90},
    "Ereus": {"Colours": ["#ffff84", "#ffffff", "#ffff84"], "Angle": 90},
    "Existence": {"Colours": ["#000000", "#000000", "#000000", "#ffffff", "#000000", "#000000", "#000000"], "Angle": 0},
    "Master Cash": {"Colours": ["#5dbc20", "#4fa61c"], "Angle": 90},
    "Master Multiplier": {"Colours": ["#f7916a","#e13f30"], "Angle": 90},
    "Master Rebirths": {"Colours": ["#b2909e","#6d5c96"], "Angle": 90},
    "Master Stone": {"Colours": ["#b08f73","#9a795d"], "Angle": 90},
    "Master White Gems": {"Colours": ["#e0b791","#ddae87"], "Angle": 90},
    "Master Crystal": {"Colours": ["#502971","#511d7c"], "Angle": 90},
    "Master Iron": {"Colours": ["#42340a","#373010"], "Angle": 90},
    "Master Gold": {"Colours": ["#fdc84d","#fec887","#ffc800"], "Angle": 135},
    "Master Quartz": {"Colours": ["#ffc89b","#48c69b","#cac89b"], "Angle": 135},
    "Master Jade": {"Colours": ["#004300","#004300","#038e4c","#00a244"], "Angle": 135},
    "Master Obsidian": {"Colours": ["#000000","#000000","#140202","#000000","#000000"], "Angle": 135},
    "Master Ruby": {"Colours": ["#f93026","#f9231c"], "Angle": 90},
    "Master Emerald": {"Colours": ["#98c953","#bdc861","#aac84f"], "Angle": 90},
    "Master Sapphire": {"Colours": ["#2a219b","#41349b"], "Angle": 90},
    "Master Diamond": {"Colours": ["#00859b","#00859b","#00859b","#f7c69b","#00859b","#f7c69b","#00859b","#00859b"], "Angle": 90},
    "Master Starlight": {"Colours": ["#ffc89b","#ffc89b","#ffc816","#3fc881","#f7c69b","#3fc881","#ffc816","#ffc89b","#ffc89b"], "Angle": 90},
    "Master Ion": {"Colours": ["#ffc800", "#ffc800","#000000","#007f96","#000000"], "Angle": 135},
    "Master Uranium": {"Colours": ["#55c84d","#00c800"], "Angle": 90},
    "Master Bismuth": {"Colours": ["#ff906f","#ff906f","#9ac86e","#ae9d98","#ff747f"], "Angle": 90},
    "Master Boracite": {"Colours": ["#00859b","#fbc89b","#0186a7"], "Angle": 90},
    "Master Nissonite": {"Colours": ["#9ac9a5","#53439e"], "Angle": 90},
    "Master Orpiment": {"Colours": ["#ba0101","#ff4000"], "Angle": 90},
    "Master Tetra": {"Colours": ["#275b43","#3f3a93"], "Angle": 90},
    "Master Volt": {"Colours": ["#000000","#000000","#f8bd00","#000000","#493a00"], "Angle": 90},
    "Master Aquamarine": {"Colours": ["#283055","#0c9240"], "Angle": 90},
    "Master Lollipop": {"Colours": ["#ffc89b","#ff1712"], "Angle": 90},
    "Prime Alpha Key": {"Colours": ["#bc0164","#ea008e"], "Angle": 90},
    "Master Mint": {"Colours": ["#b1c880","#61c488"], "Angle": 180},
    "Master Gems": {"Colours": ["#f9fb7c", "#fefe01"], "Angle": 180},
    "Master Event Power": {"Colours": ["#00ff7c", "#00ff02"], "Angle": 180},
    "Default": {"Colours": ["#ffffff", "#ffffff"], "Angle": 0},
}
cythrex_data = {
    "Cash": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "The most basic currency to exist, provided to you by AIHA Corp.",
        "obtainment": "Always obtainable, never runs out"
    },
    "Multiplier": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "A technology created by AIHA Corp. It generates Cash at a faster speed.",
        "obtainment": '''First found in the Spawn realm. Also can be obtained by:
- Stone Geode at a 1/2 chance
- Buttons found in: C, CB, IS, GQ, QW, JF, OA, CT, UW, VS, Recover Hall'''
    },
    "Rebirths": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "Further technology created AIHA Corp. Requires the recreation of the body, in turn more funds are given by AIHA Corp.",
        "obtainment": '''First found in the Spawn realm. Also can be obtained by:
- Stone Geode at a 1/10 chance
- Buttons found in: C, CB, IS, GQ, QW, JF, OA, CT, UW, VS, Recover Hall'''
    },
    "Stone": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "The first true ore. Has marginal value to AIHA Corp and hence leads to more Cash and Rebirths being given.",
        "obtainment": '''First found in the Spawn realm. Also can be obtained by:
- Stone Geode at a 1/20 chance
- White Gems Geode at a 1/6 Chance
- Crystal Geode at a 1/5 Chance
- Buttons found in: C, CB, IS, GQ, QW, JF, OA, CT, UW, VS, Recover Hall'''
    },
    "White Gems": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "A less common Ore, can be found in Caves of minimal depth.",
        "obtainment": '''First found in the Caves realm. Also can be obtained by:
- Stone Geode at a 1/333 chance
- White Gems Geode at a 1/10 Chance
- Crystal Geode at a 1/4 Chance
- Iron Geode at a 1/20 Chance
- Buttons found in: CB, IS, GQ, QW, JF, OA, CT, UW, VS, Recover Hall'''
    },
    "Crystal": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "A minorly rare Ore, typically found in deeper segments of Caves.",
        "obtainment": '''First found in the Crystal Beneaths realm. Also can be obtained by:
- White Gems Geode at a 1/20 Chance
- Crystal Geode at a 1/4 Chance
- Iron Geode at a 1/10 Chance
- Buttons found in: IS, GQ, QW, JF, OA, CT, UW, VS, Recover Hall'''
    },
    "Iron": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "A rather sturdy metal that can be useful to create simple items. Because of its various uses Iron often has more proper mining efforts.",
        "obtainment": '''First found in the Iron Shafts realm. Also can be obtained by:
- Crystal Geode at a 1/1,162 Chance
- Iron Geode at a 1/5 Chance
- Gold Geode at a 1/6 Chance
- Buttons found in: GQ, QW, JF, OA, CT, UW, VS, Recover Hall'''
    },
    "Gold": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "Although Gold lacks common use, it is often used for jewellary and with its rarity gains value from that.",
        "obtainment": '''First found in the Golden Quarry realm. Also can be obtained by:
- Gold Geode at a 1/4 Chance
- Quartz Geode at a 1/8 Chance
- Jade Geode at a 1/2 Chance
- Buttons found in: QW, JF, OA, CT, UW, VS, Recover Hall'''
    },
    "Quartz": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "A semi-precious stone, contains more value in its non-white variants.",
        "obtainment": '''First found in the Quartz Walkway realm. Also can be obtained by:
- Gold Geode at a 1/33 Chance
- Quartz Geode at a 1/5 Chance
- Jade Geode at a 1/4 Chance
- Buttons found in: QW, JF, OA, CT, UW, VS, Recover Hall'''
    },
    "Jade": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "A semi-precious stone that to some has minor spirtiual value.",
        "obtainment": '''First found in the Jade Forest realm. Also can be obtained by:
- Quartz Geode at a 1/16 Chance
- Jade Geode at a 1/10 Chance
- Obsidian Geode at a 1/10 Chance
- Buttons found in: OA, CT, UW, VS, Recover Hall'''
    },
    "Obsidian": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "Obsidian is known to be volcanic glass formed upon the cooling of lava. Due to its nature Obsidian is abundant in the Obsidian Abyss however AIHA Corp. has brought it to many of the other realms of Buttonia.",
        "obtainment": '''First found in the Obsidian Abyss realm. Also can be obtained by:
- Jade Geode at a 1/1,000 Chance
- Obsidian Geode at a 1/5 Chance
- Buttons found in: CT, UW, VS, Recover Hall'''
    },
    "Ruby": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "A rather precious, typically red gem. Ruby is apart of the RGB gem trifecta.",
        "obtainment": '''First found in the Colour Temple realm. Also can be obtained by:
- Obsidian Geode at a 1/20 Chance
- Ruby Geode at a 1/5 Chance
- Emerald Geode at a 1/10 Chance
- Sapphire Geode at a 1/20 Chance
- Diamond Geode at a 1/3 Chance
- Buttons found in: ET, UW, VS, Recover Hall'''
    },
    "Emerald": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "A rather precious, typically green gem. Emerald is apart of the RGB gem trifecta.",
        "obtainment": '''First found in the Colour Temple realm. Also can be obtained by:
- Ruby Geode at a 1/10 Chance
- Emerald Geode at a 1/5 Chance
- Sapphire Geode at a 1/10 Chance
- Diamond Geode at a 1/3 Chance
- Buttons found in: ET, UW, VS, Recover Hall'''
    },
    "Sapphire": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "A rather precious, typically blue gem. Sapphire is apart of the RGB gem trifecta.",
        "obtainment": '''First found in the Colour Temple realm. Also can be obtained by:
- Sapphire Geode at a 1/20 Chance
- Emerald Geode at a 1/20 Chance
- Sapphire Geode at a 1/5 Chance
- Diamond Geode at a 1/3 Chance
- Buttons found in: ET, UW, VS, Recover Hall'''
    },
    "Diamond": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "Often considered the most precious gem and has the highest natural toughness. Its value exponentially decreased after AIHA Corp.'s innovation of asteroid mining.",
        "obtainment": '''First found in the Extraterrestrial Orbits realm. Also can be obtained by:
- Starlight Geode at a 1/10 Chance
- Ion Geode at a 1/2 Chance
- Buttons found in: EI, UW, SD, IP, VS, Recover Hall'''
    },
    "Starlight": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "The first ore to transcend regular bounds. Starlight is formed from an endless refraction of... starlight, eventually some of its essence fuses with the rock it touches and forms this ore. AIHA Corp. has patented a method to forcefully condense starlight into rock hence forming the Starlight ore.",
        "obtainment": '''First found in the Extraterrestrial Orbits realm. Also can be obtained by:
- Diamond Geode at a 1/1,666 Chance
- Starlight Geode at a 1/5 Chance
- Ion Geode at a 1/4 Chance
- Buttons found in: EI, UW, SD, IP, VS, Recover Hall'''
    },
    "Ion": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "Ion was an ore first created by AIHA Corp. It was formed by continuously bombarding stone with various ions, eventually this caused a transformation to be undergone creating a highly conductive and reactive material that we now call Ion.",
        "obtainment": '''First found in the Empyrean Island realm. Also can be obtained by:
- Starlight Geode at a 1/333 Chance
- Ion Geode at a 1/10 Chance
- Buttons found in: UW, SD, IP, FP, VS, Recover Hall'''
    },
    "Uranium": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "This Uranium is not true uranium, for safety purposes all the radioactive segments of Uranium have been extracted and removed condensed into a different ore and sent to plaent [REDACTED] by AIHA Corp. The desolation seen in Uranium Wastelands was caused by the initial radioactivity of Uranium.",
        "obtainment": '''First found in the Uranium Wastelands realm. Also can be obtained by:
- Ion Geode at a 1/4,000 Chance
- Uranium Geode at a 1/5 Chance
- Boracite Geode at a 1/20 Chance
- Buttons found in: SD, IP, FP, VS, Recover Hall'''
    },
    "Bismuth": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "Bismuth is a rather colourful ore and a stat Uranium often reaches during the decay process. AIHA Corp. has patented a method to prevent further decay upon reaching Bismuth.",
        "obtainment": '''First found in the Smooth Depths realm. Also can be obtained by:
- Uranium Geode at a 1/666 Chance
- Bismuth Geode at a 1/4 Chance
- Boracite Geode at a 1/10 Chance
- Nissonite Geode at a 1/20 Chance
- Buttons found in: IP, FP, VS, Recover Hall'''
    },
    "Boracite": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "Boracite is known to be extremely similar to Bismuth, the reason for this is simply due to the formation process of Boracite. Boracite is formed by fusing a small amount of Nissonite with Bismuth giving it its aquamarine colour.",
        "obtainment": '''First found in the Icy Palace realm. Also can be obtained by:
- Bismuth Geode at a 1/100 Chance
- Boracite Geode at a 1/5 Chance
- Nissonite Geode at a 1/10 Chance
- Buttons found in: FP, T, VS, Recover Hall'''
    },
    "Nissonite": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "Nissonite is an unusually rare mineral. Nissonite is specifically formed by long-term exposure to perma-frost requiring billions of years in perfect conditions to form small amounts.",
        "obtainment": '''First found in the Icy Palace realm. Also can be obtained by:
- Boracite Geode at a 1/150 Chance
- Nissonite Geode at a 1/5 Chance
- Orpiment Geode at a 1/100 Chance
- Buttons found in: FP, T, VS, Recover Hall'''
    },
    "Orpiment": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "Orpiment is a highly valuable ore having many technological uses and being the basis for the creation of most artifical ores. AIHA Corp. is known to have a monopoly over the Orpiment supply, generating Orpiment on an artificial floating island.",
        "obtainment": '''First found in the Floating Purgatory realm. Also can be obtained by:
- Orpiment Geode at a 1/20 Chance
- Buttons found in: T, VS, AT, FC Recover Hall'''
    },
    "Tetra": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "Tetra is an entirely artificial ore, created by AIHA Corp. as the perfect building material. It is believed that Tetratum was entirely made using Tetra.",
        "obtainment": '''First found in the Tetratum realm. Also can be obtained by:
- Buttons found in: VS, AT, FC Recover Hall'''
    },
    "Volt": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "Volt is not a traditional ore. Rather Volt is formed by the forced condension of trillions of electrons to create this highly conductive ore. Volt is known to hold an extreme negative charge that is dangerous without proper equipment.",
        "obtainment": '''First found in the Voltaic Sector realm. Also can be obtained by:
- Buttons found in: AT, FC Recover Hall'''
    },
    "Aquamarine": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "Aquamarine is known to only be found at the bottom of extremely deep oceans, only being found on approximately 0.001% of planets. The process of forming Aquamarine is still unknown even to AIHA Corp.",
        "obtainment": '''First found in the Abyssal Trenches realm. Also can be obtained by:
- Buttons found in: FC'''
    },
    "Lollipop": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "This ore is not to be confused with the typical sweet treat, it was first discovered on a far-off planet and its supplies is stil extremely limited hence it has high value.",
        "obtainment": '''First found in the Flourish Candylands realm. Also can be obtained by:
- Buttons found in: Anticovery Hall'''
    },
    "C0RR8PT10N": {
        "tags": ["Main", "BS:ED", "Stats"],
        "lore": "This ore is considered to be highly unnatural, it was first created by continuously bombarding rocks with various unstable elements, its believed this eventually led to a 'data overflow' which caused the ore to corrupt into what it is now, experiments are still ongoing hence any quantity of this ore is extremely valuable yet extremely dangerous.",
        "obtainment": '''Only found in the Mechanical Room realm'''
    },
    "Stargazed Metal": {
        "tags": ["Main", "BS:ED", "Time Lost Ascension", "TLA", "Transcendant"],
        "lore": "The first of the transcended ores, AIHA Corp. has no information about its contents as it is simply theorised to exist, it is thought to be created by exposing metal to the extreme cosmic radiation created by the Singularity. Further research is needed, any proof of existence is highly appreciated.",
        "obtainment": '''It is unknown if this ore exists, if it were to exist it would likely be obtained in a place that unites dimensions.'''
    },
    "Gyge": {
        "tags": ["Main", "BS:ED", "Time Lost Ascension", "TLA", "Transcendant"],
        "lore": "Gyge is a member of the theoritical transcendant ores, it is theorised to be the perfect catalyst reducing activation energy for experiments to zero or even into the negatives. If Gyge were to exist it would revolutionise the field of science as we know it. AIHA Corp. will reward any proof of its existence.",
        "obtainment": '''It is unknown if this ore exists, if it were to exist it would likely be obtained in a place that unites dimensions.'''
    },
    "Auly Plate": {
        "tags": ["Main", "BS:ED", "Time Lost Ascension", "TLA", "Transcendant"],
        "lore": "Auly Plate is theorised to be an almost perfect material, easily malleable but also extremely rigid when necessary, it is also theorised to be harder than nearly all known and theorised materials. Any proof to Auly Plate's existence will lead to massive rewards from AIHA Corp.",
        "obtainment": '''It is unknown if this ore exists, if it were to exist it would likely be obtained in a place that unites dimensions.'''
    },
    "Shell Piece": {
        "tags": ["Main", "BS:ED", "Time Lost Ascension", "TLA", "Transcendant", "The Shell", "Universe"],
        "lore": '''Shell Piece is the only material capable of containing the Singularity, although it does require the help of some other materials for such a difficult task, the world needs someone to obtain Shell Piece lest the universe collapses. Good luck, you shall need it.''',
        "obtainment": '''The location of this ore is unknown, but it is theorised that it would be found in a place that unites dimensions.'''
    },
    "Singularity": {
        "tags": ["Main", "BS:ED", "Time Lost Ascension", "TLA", "Transcendant", "The Shell", "Universe"],
        "lore": '''The Singularity must be contained lest the universe collapses. Search for it, search for it, it must be somewhere, somewhere that we cannot see.''',
        "obtainment": '''We do not know where the Singularity is, as if it was an illusion beyond our vision.'''
    },
    "Capsuled Singularity": {
        "tags": ["Main", "BS:ED", "Time Lost Ascension", "TLA", "Transcendant", "The Shell", "Universe"],
        "lore": '''An impossibility, if this were to be created the universe would be saved.''',
        "obtainment": '''5 Shell Piece, 1 Prime Alpha Key, 1 Singularity, 250Sx Shroomite Bars, 1UDe Gems. Combine them and seal away the Singularity for good.'''
    },
    "Starglass": {
        "tags": ["Secret", "BS:ED", "Starglass"],
        "lore": "placeholder",
        "obtainment": "placeholder"
    },
    "Darkmatter": {
        "tags": ["Secret", "BS:ED", "Darkmatter"],
        "lore": "placeholder",
        "obtainment": "placeholder"
    },
    "Ivory": {
        "tags": ["Exclusive", "P2W", "BS:ED"],
        "lore": "An extremely rare ore that seems to only have one copy available at any given time.",
        "obtainment": "Given to VIPs in AIHA Corp."
    }
}
MANTISSA_THRESHOLD = 1e300
luck = 6
crit_luck = 6
geode_speed= 1
bulk_roll= 4
voltaic_radar = True
music = ["Catswing.mp3", "Flamewall.mp3", "Ambrosia.mp3"]
# Source - https://stackoverflow.com/a
# Posted by luke, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-30, License - CC BY-SA 3.0
FILE_ATTRIBUTE_HIDDEN = 0x02
FILE_ATTRIBUTE_SYSTEM = 0x04
def write_hidden(file_name, data):
    # Find user's Documents folder
    docs = Path.home() / "Documents"

    # For *nix, prefix with .
    final_name = file_name
    if os.name != 'nt':
        final_name = "." + file_name

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
#End of atrributions stuff
def trig_check(input):
    input = input.lower()
    required = ["sin", "cos", "tan", "cot", "sec", "csc"]
    def present(text):
        return re.search(rf"(?<![a-z]){text}(?![a-z])", input)
    return all(present(text) for text in required)
def blinded():
    if not os.path.exists(Path.home()/"Documents"/"toodarktosee"):
      print("Traceback (most recent call last):")
      print('  File "Module.py", line 128, in <module>')
      print("    test_function()")
      print("RuntimeError: Unexpected internal failure")
      print(colorama.Fore.BLACK + "YOU'RE JUST TOO BLIND TO SEE IT.")
      write_hidden(Path.home()/"Documents"/"toodarktosee", "Are you not afraid of what cannot be seen? \n You search for the impossible, what has never been found \n Yet you wish to harness its energy, the energy of DARKMATTER.")
      root.close()
def secret_input(area):
    INPUT = input("Input: ").title()
    if INPUT == "Totality" and os.path.exists(Path.home()/"Documents"/"toodarktosee"):
        print("You're own the right track!")
        secrets["Darkmatter_1"] = True
        print(colorama.Fore.BLACK, "RGltZW5zaW9uIGJyZWFr")
    if area == "Wormhole":
      if INPUT == "Andromeda":
          print("You feel as if the wormhole was beginning to reopen")
          secrets["Galaxite_1"] = True
      elif INPUT == "Cassiopeia":
          print("You feel the fabric of spacetime shift")
          secrets["Galaxite_2"] = True
      elif INPUT == "Defractured":
          print("You feel the wormhole begin to stabilise")
          secrets["Galaxite_3"] = True
      elif INPUT == "Endless Night" and secrets["Darkmatter_1"]:
          secrets["Darkmatter_2"] = True
      if all((secrets["Galaxite_1"], secrets["Galaxite_2"], secrets["Galaxite_3"], stat_increment["Secret"]["Galaxite"]["Value"] == 0)):
          print("An exit has opened, congratulations on your escape.")
          stat_increment["Secret"]["Galaxite"]["Value"] = 1
    elif area == "Tetratum":
        if trig_check(INPUT):
            stat_increment["Secret"]["Graphite"]["Value"] = 1
def Geode_roll(btn, geode, luck=1, geode_speed=1, bulk_roll=1):
    global stat_increment
    local_crit = crit_luck + upgrades["crit_luck"]["effect"]*upgrades["crit_luck"]["current_lvl"]
    local_luck = luck + upgrades["geode_luck"]["effect"]*upgrades["geode_luck"]["current_lvl"]
    btn.setEnabled(False)
    stat_increment = geode.open(stat_increment, local_luck, bulk_roll, local_crit)
    QTimer.singleShot(int(geode_speed*1000), lambda: btn.setEnabled(True))
def load_check(req, unit, buttons):
    global stat_increment, container, scroll_area, content, layout
    amount = stat_increment["Stats"][unit]
    req = float_to_mantissa(req) if isinstance(amount, Mantissa) else req
    if amount >= req:
      container.deleteLater()  # remove old scroll area
      container, scroll_area, content = tkinter_frames.create_scrollable_area(root, buttons, voltaic_radar=voltaic_radar)
      layout.addWidget(container, 2, 1, 3, 3)
def load_world(req, unit, initial_area, cash, multiplier, rebirths, gems, reset, event_power=False):
    global stat_increment, container, scroll_area, container, content, layout, cash_type, multi_type, rebirth_type, gem_type, e_event, e_type, cash_l, multi_l, re_l, reset_key
    amount = stat_increment["Stats"][unit]
    req = float_to_mantissa(req) if isinstance(amount, Mantissa) else req
    if amount >= req:
      container.deleteLater()  # remove old scroll area
      container, scroll_area, content = tkinter_frames.create_scrollable_area(root, initial_area, voltaic_radar=voltaic_radar)
      layout.addWidget(container, 2, 1, 3, 3)
      cash_type = cash
      multi_type = multiplier
      rebirth_type = rebirths
      gem_type = gems
      if event_power:
          e_type = event_power
      e_event = event_power
      reset_key = reset
      cash = stat_increment["Stats"][cash_type]
      c_msg = cash if not isinstance(cash, Mantissa) else cash.to_string()
      cash_l.setText(f"{cash_type}: {c_msg}")
      multi = stat_increment["Stats"][multi_type]
      m_msg = multi if not isinstance(multi, Mantissa) else multi.to_string()
      multi_l.setText(f"{multi_type}: {m_msg}")
      rebirths = stat_increment["Stats"][rebirth_type]
      re_msg = rebirths if not isinstance(rebirths, Mantissa) else rebirths.to_string()
      re_l.setText(f"{rebirth_type}: {re_msg}")
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
       global upgrades, secrets
       if os.path.exists("savefile.json"): # If you have saved before
        with open("savefile.json", "r")  as file: # Read the file
          try:
            data = deserialize(json.load(file)) # Attempt to return backup data
            try:
              for upgrade in upgrades.keys():
                  upgrades[upgrade]["current_lvl"] = data["Upgrades"][upgrade]
            except:
                upgrades = def_upgrades
            try:
                secrets = data["Keys"]
            except:
                secrets = def_secrets
            for item in def_stat_increment["Stats"].keys():
                data["Stats"].setdefault(item,0)
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
def Save(collection, upgrades, secrets):
        '''Saves your data to a json file, and makes the previous file a backup'''
        collection["Upgrades"] = {}
        collection["Upgrades"] = {upgrade: upgrades[upgrade]["current_lvl"] for upgrade in upgrades.keys()}
        collection["Keys"] = secrets
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
    global stat_increment, crit_luck, cash_type, multi_type, rebirth_type
    local_crit = crit_luck + upgrades["crit_luck"]["effect"]*upgrades["crit_luck"]["current_lvl"]
    total = Mantissa(1, 0)  # Start as 1 in Mantissa form
    keys = list(abs_stat_info.keys())
    for key in keys:
      stat_list = list(abs_stat_info[key].keys())
      for item in stat_list:
          try:
            amount = stat_increment["Stats"].get(item)
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
          total *= Mantissa(1, 0) + (multiplier * amount_m * multi_2)
      if key == "Geode":
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
                  total *= Mantissa(1, 0) + (multiplier * amount_m * multi_2)
    # Ensure we don't return zero
    if total.num == 0:
        return Mantissa(1, 0)

    if total.exp < math.log(MANTISSA_THRESHOLD, 10):
        total = round(total.to_float(), 2)
        total = float_to_mantissa(total)
    total *= 2 if random.randint(1,500//local_crit) == 1 and not isinstance(total,Mantissa) else float_to_mantissa(2) if random.randint(1,500//local_crit) == 1 and isinstance(total, Mantissa) else 1 if not isinstance(total, Mantissa) else Mantissa(1,0)
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
    multi *= 1+(max(1,upgrades["cash_multi"]["current_lvl"]*upgrades["cash_multi"]["effect"])*max(1,upgrades["cash_multi_2"]["current_lvl"]*upgrades["cash_multi_2"]["effect"])) if not isinstance(multi, Mantissa) else float_to_mantissa(1+(max(1,upgrades["cash_multi"]["current_lvl"]*upgrades["cash_multi"]["effect"])*max(1,upgrades["cash_multi_2"]["current_lvl"]*upgrades["cash_multi_2"]["effect"])))
    # Compute approximate float multiplier
    approx_multiplier = multiplier_m.to_float() if hasattr(multiplier_m, "to_float") else float(multiplier_m)

    # Compute delay and speed ratio
    base_delay = 250
    base_delay /= max(1,upgrades["cash_speed"]["current_lvl"])
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
    display_val = val.to_string() if hasattr(val, "to_string") else val
    cash_l.setText(f"{cash_type}: {display_val}")
    QTimer.singleShot(delay, cash_increase)
    # Schedule next increment
def gem_increase():
    global stat_increment, gem_type
    stat_increment["Stats"][gem_type] += (1+upgrades["gem_timer_amount"]["current_lvl"]*upgrades["gem_timer_amount"]["effect"])
    if upgrades["gem_speed"]["current_lvl"] == 0:
        period = 60000
    else:
        period = 60000//(upgrades["gem_speed"]["effect"]*upgrades["gem_speed"]["current_lvl"])
    QTimer.singleShot(period, gem_increase)
def event_increase():
    global stat_increment, e_event, e_type
    if e_event:
      stat_increment["Stats"][e_type] += (1+upgrades["event_timer_amount"]["current_lvl"]*upgrades["event_timer_amount"]["effect"])
      if upgrades["event_speed"]["current_lvl"] == 0:
          period = 60000
      else:
          period = 60000//(upgrades["event_speed"]["effect"]*upgrades["event_speed"]["current_lvl"])
      QTimer.singleShot(period, event_increase)
def cost_button(unit, cost, unit_2, receive):
    global cash_l, multi_l, stat_increment, cash_type, multi_type

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
        cash_val = stat_increment["Stats"][cash_type]
        cash_text = cash_val.to_string() if isinstance(cash_val, Mantissa) else cash_val
        cash_l.setText(f"{cash_type}: {cash_text}")

        multi_val = stat_increment["Stats"][multi_type]
        multi_text = multi_val.to_string() if isinstance(multi_val, Mantissa) else multi_val
        multi_l.setText(f"{multi_type}: {multi_text}")

        stat_increment["Stats"]["Buttons Pressed"] += 1
def reset_button(cost, unit, reward, unit_2):
    global cash_l, multi_l, re_l, stat_increment, cash_type, multi_type, rebirth_type, reset_key

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
        r_text = stat_increment["Stats"][rebirth_type] if not isinstance(stat_increment["Stats"][rebirth_type], Mantissa) else stat_increment['Stats'][rebirth_type].to_string()
        # Update labels
        cash_l.setText(f"{cash_type}: {stat_increment['Stats'][cash_type]}")
        multi_l.setText(f"{multi_type}: {stat_increment['Stats'][multi_type]}")
        re_l.setText(f"{rebirth_type}: {r_text}")
        stat_increment["Stats"]["Buttons Pressed"] += 1
def reset_button_special(cost, unit, reward, unit_2, resets=[]):
    global cash_l, multi_l, re_l, stat_increment, cash_type, multi_type, rebirth_type

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
        m_text = stat_increment["Stats"][multi_type] if not isinstance(stat_increment["Stats"][multi_type], Mantissa) else stat_increment["Stats"][multi_type].to_string()
        r_text = stat_increment["Stats"][rebirth_type] if not isinstance(stat_increment["Stats"][rebirth_type], Mantissa) else stat_increment["Stats"][rebirth_type].to_string()
        # Update labels
        cash_l.setText(f"{cash_type}: {stat_increment['Stats'][cash_type]}")
        multi_l.setText(f"{multi_type}: {m_text}")
        re_l.setText(f"{rebirth_type}: {r_text}")
        stat_increment["Stats"]["Buttons Pressed"] += 1
def recovery_button_set(req, unit, Set, unit_2):
    global stat_increment
    amount = stat_increment["Stats"][unit]
    if isinstance(amount, Mantissa) and not isinstance(req, Mantissa):
        req = float_to_mantissa(req)
    if not isinstance(amount, Mantissa) and isinstance(req, Mantissa):
        amount = float_to_mantissa(amount)
    if amount >= req:
        if stat_increment["Stats"][unit_2] < Set:
          stat_increment["Stats"][unit_2] = Set
    else:
     pass
def recovery_button_fetch(req, unit, recovery, unit_2):
    global stat_increment, cash_type, multi_type, rebirth_type
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
      c_msg = cash if not isinstance(cash, Mantissa) else cash.to_string()
      cash_l.setText(f"{cash_type}: {c_msg}")
      multi = stat_increment["Stats"][multi_type]
      m_msg = multi if not isinstance(multi, Mantissa) else multi.to_string()
      multi_l.setText(f"{multi_type}: {m_msg}")
      rebirths = stat_increment["Stats"][rebirth_type]
      re_msg = rebirths if not isinstance(rebirths, Mantissa) else rebirths.to_string()
      re_l.setText(f"{rebirth_type}: {re_msg}")
    else:
     pass
def image_load(path):
    path = os.path.abspath(path)
    webbrowser.open(f"file://{path}")
if __name__ == "__main__":
  app = QApplication(sys.argv)
  
  root = Window()
  root.setWindowTitle("BS:ED but bad")
  cash_l = QLabel()
  multi_l = QLabel()
  re_l = QLabel()
  root.setWindowTitle("BS:ED but bad")
  root.setMinimumSize(QSize(100,100))
  root.setWindowIcon(QIcon("Quant.png"))
  layout = QGridLayout()
  central = QWidget()
  central.setLayout(layout)
  temp = Load()
  if temp != None:
     stat_increment = temp
  cash = stat_increment["Stats"]['Cash']
  c_msg = cash if not isinstance(cash, Mantissa) else cash.to_string()
  cash_l.setText(f"Cash: {c_msg}")
  multi = stat_increment["Stats"]['Multiplier']
  m_msg = multi if not isinstance(multi, Mantissa) else multi.to_string()
  multi_l.setText(f"Multiplier: {m_msg}")
  rebirths = stat_increment["Stats"]['Rebirths']
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
                      "Starglass": {"Chance": 929221841},
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
                      "Event Power": {"Chance": 33},
                      "Silver": {"Chance": 142, "Multis": {"Multiplier": 10, "White Gems": 5, "Iron": 2}},
                      "Platinum": {"Chance": 32000, "Multis": {"White Gems": 10, "Crystal": 20, "Iron": 15, "Gold": 3, "Quartz": 2}},
                      "Mythril": {"Chance": 2000000, "Multis": {"Cash": 999, "Crystal": 5, "Iron": 10, "Gold": 50, "Quartz": 100}}},
                      25, "Iron")
  gold_geode = Geode({"Gold": {"Chance": 4},
                      "Iron": {"Chance": 6},
                      "Quartz": {"Chance": 33},
                      "Mushroom": {"Chance": 100},
                      "Pumpkin": {"Chance": 125},
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
  sacred_geode = Geode({"Grail": {"Chance": 2, "Multis": {"Starlight": 2, "Ion": 2, "Uranium": 2}},
                        "Box": {"Chance": 3500000, "Multis": {"Obsidian": 3, "Ruby": 3, "Emerald": 3, "Sapphire": 3, "Bismuth": 3, "Boracite": 3}}},
                       1e9, "Gems")
  bismuth_geode = Geode({"Lead": {"Chance": 2, "Multis": {"Iron": 10000, "Obsidian": 5, "Ruby": 5, "Emerald": 5, "Sapphire": 5, "Diamond": 5}},
                         "Bismuth": {"Chance": 4},
                         "Pseudomalachite": {"Chance": 10, "Multis": {"Diamond": 6, "Uranium": 2, "Bismuth": 1.15}},
                         "Boracite": {"Chance": 100},
                         "Osmium": {"Chance": 1428, "Multis": {"Bismuth": 5}},
                         "Yhed": {"Chance": 45000, "Multis": {"Cash": 80000, "Rebirths": 80000, "White Gems": 80000, "Iron": 80000, "Quartz": 800, "Obsidian": 800, "Emerald": 8, "Diamond": 8, "Ion": 8, "Bismuth": 8}},
                         "Hexaferrum": {"Chance": 300000, "Multis": {"Ruby": 3000, "Emerald": 2000, "Sapphire": 1000, "Diamond": 160, "Uranium": 40, "Bismuth": 15, "Boracite": 3}}},
                        50, "Bismuth")
  boracite_geode = Geode({"Boracite": {"Chance": 5},
                          "Bismuth": {"Chance": 10},
                          "Uranium": {"Chance": 20},
                          "Nissonite": {"Chance": 150},
                          "Spectrolite": {"Chance": 4000, "Multis": {"Starlight": 5, "Ion": 5, "Bismuth": 5, "Boracite": 3}},
                          "Hectam": {"Chance": 25000, "Multis": {"Crystal": 100, "Quartz": 100, "Jade": 100, "Ruby": 100, "Emerald": 100, "Diamond": 100, "Boracite": 10}}},
                         1000, "Boracite")
  nissonite_geode = Geode({"Nissonite": {"Chance": 5},
                           "Boracite": {"Chance": 10},
                           "Bismuth": {"Chance": 20},
                           "Frostone": {"Chance": 1250, "Multis": {"Rebirths": 15, "Crystal": 15, "Quartz": 15, "Sapphire": 15, "Diamond": 15, "Boracite": 15, "Nissonite": 4, "Mint": 1.04}},
                           "Neptunian": {"Chance": 6666, "Multis": {"Cash": 2, "Multiplier": 3, "Rebirths": 30, "Ion": 1.5, "Uranium": 2, "Bismuth": 3, "Boracite": 30, "Nissonite": 10}},
                           "Clouminance": {"Chance": 19000, "Multis": {"Diamond": 100, "Starlight": 100, "Ion": 100, "Boracite": 100, "Nissonite": 20}},
                           "Galarium": {"Chance": 600000, "Multis": {"Diamond": 300, "Starlight": 300, "Nissonite": 45}},
                           "Unova": {"Chance": 5000000, "Multis": {"Cash": 1111, "Multiplier": 1111, "Rebirths": 1111, "Stone": 1111, "White Gems": 1111, "Crystal": 1111, "Iron": 1111, "Gold": 1111, "Quartz": 1111, "Jade": 1111, "Obsidian": 1111, "Ruby": 1111, "Emerald": 1111, "Sapphire": 1111, "Diamond": 1111, "Starlight": 1111, "Ion": 1111, "Uranium": 1111, "Bismuth": 1111, "Boracite": 1111, "Nissonite": 111, "Orpiment": 7, "Mint": 11.1, "Gems": 1.1}}},
                          5, "Nissonite")
  orpiment_geode = Geode({"Borax": {"Chance": 3, "Multis": {"Boracite": 20}},
                          "Axiom": {"Chance": 10, "Multis": {"Boracite": 15, "Nissonite": 10}},
                          "Orpiment": {"Chance": 20},
                          "Vergemite": {"Chance": 33, "Multis": {"Bismuth": 25, "Orpiment": 1.01}},
                          "Nissonite": {"Chance": 100},
                          "Zanyte": {"Chance": 13000, "Multis": {"Iron": 10, "Gold": 10, "Quartz": 10, "Jade": 10, "Obsidian": 10, "Ruby": 10, "Emerald": 10, "Sapphire": 10, "Diamond": 10, "Starlight": 10, "Ion": 10, "Uranium": 10, "Bismuth": 10, "Boracite": 10, "Nissonite": 10, "Orpiment": 4}},
                          "Secretum": {"Chance": 100000, "Multis": {"Orpiment": 12}},
                          "Mortalstone": {"Chance": 750000, "Multis": {"Cash": 999, "Multiplier": 999, "Rebirths": 999, "Stone": 999, "White Gems": 999, "Crystal": 999, "Iron": 999, "Gold": 999, "Quartz": 999, "Jade": 999, "Obsidian": 999, "Ruby": 999, "Emerald": 999, "Sapphire": 999, "Diamond": 999, "Starlight": 999, "Ion": 999, "Uranium": 999, "Bismuth": 999, "Boracite": 100, "Nissonite": 100, "Orpiment": 15, "Gems": 10}}},
                         2, "Orpiment")
  mint_geode = Geode({"Mint": {"Chance": 2},
                      "Alpha Point": {"Chance": 2},
                      "Chestnut": {"Chance": 5},
                      "Bat": {"Chance": 8},
                      "Wicked Branch": {"Chance": 33},
                      "Bone": {"Chance": 80},
                      "Uzik": {"Chance": 69420, "Multis": {"Jade": 10, "Mint": 5}},
                      "Omet": {"Chance": 133371, "Multis": {"Cash": 100000, "Mint": 20}}}, 2000, "Mint")
  #----------- EVENT GEODES --------------
  hearted_geode = Geode({"Sweet": {"Chance": 2, "Multis": {"Cash": 3, "Multiplier": 2, "Flower": 2.5, "Love": 1.5}},
                         "Ichor Flower": {"Chance": 8, "Multis": {"Cash": 5, "Rebirths": 3, "Stone": 1.5, "Heart": 2}},
                         "Halved Heart": {"Chance": 20, "Multis": {"White Gems": 2, "Love": 5, "Heart": 3}},
                         "Rainbow": {"Chance": 100, "Multis": {"Cash": 3, "Multiplier": 3, "Rebirths": 3, "Crystal": 3, "Flower": 7, "Heart": 4}},
                         "Unicorn": {"Chance": 333, "Multis": {"Cash": 7, "Multiplier": 7, "Rebirths": 7, "Stone": 7, "White Gems": 7, "Crystal": 7, "Flower": 7, "Heart": 7}},
                         "Rose": {"Chance": 4000, "Multis": {"Gold": 5, "Quartz": 3, "Flower": 50, "Love": 20, "Heart": 10}},
                         "Wickedite": {"Chance": 17500, "Multis": {"Stone": 10, "White Gems": 10, "Crystal": 10, "Iron": 10, "Gold": 10, "Quartz": 10, "Jade": 10, "Obsidian": 10, "Heart": 1/1.4}},
                         "Heartium": {"Chance": 280000, "Multis": {"Multiplier": 100, "Stone": 100, "Crystal": 100, "Jade": 10, "Ruby": 5, "Sapphire": 3, "Flower": 50, "Love": 50, "Heart": 50}},
                         "Eternal Rose": {"Chance": 1250000, "Multis": {"Cash": 1000, "Multiplier": 1000, "Stone": 1000, "White Gems": 1000, "Crystal": 1000, "Iron": 1000, "Gold": 1000, "Quartz": 1000, "Jade": 1000, "Obsidian": 1000, "Ruby": 100, "Emerald": 100, "Sapphire": 100, "Nissonite": 4, "Flower": 1000, "Love": 1000, "Heart": 1000}},
                         }, 50, "Heart")
  luck_geode = Geode({"Lucky Clover": {"Chance": 4, "Multis": {"Cash": 2, "Clover": 1.05}},
                      "Golden Clover": {"Chance": 20, "Multis": {"Cash": 1.8, "Multiplier": 1.75, "Clover": 1.15}},
                      "Diamond Clover": {"Chance": 100, "Multis": {"Multiplier": 2, "Rebirths": 3.5, "Clover": 1.25}},
                      "Leprechaun's Hat": {"Chance": 200, "Multis": {"Rebirths": 3, "Stone": 1.8, "Clover": 1.32}},
                      "Supreme Clover": {"Chance": 12000, "Multis": {"Crystal": 3, "Quartz": 4.5, "Clover": 1.75}},
                      "Cloverite": {"Chance": 35000, "Multis": {"Stone": 10, "Gold": 5, "Jade": 3, "Emerald": 1.25, "Clover": 2.5}},
                      "Ace": {"Chance": 1600000, "Multis": {"Cash": 6, "Multiplier": 6, "Rebirths": 6, "Stone": 6, "Crystal": 6, "Quartz": 6, "Ruby": 6, "Emerald": 6, "Sapphire": 6, "Diamond": 6, "Clover": 12.5}},
                      "777": {"Chance": 7777777, "Multis": {"Cash": 777, "Multiplier": 777, "Rebirths": 777, "Stone": 77, "White Gems": 77, "Crystal": 77, "Iron": 77, "Gold": 77, "Quartz": 77, "Jade": 77, "Obsidian": 77, "Ruby": 77, "Emerald": 77, "Sapphire": 77, "Clover": 77.7}}
                      }, 3, "Clover")
  clover_geode = Geode({"Holy Clover": {"Chance": 3, "Multis": {"Quartz": 2, "Ruby": 1.5, "Clover": 1.45}},
                        "Red Clover": {"Chance": 6, "Multis": {"Multiplier": 3, "White Gems": 1.15, "Obsidian": 3, "Ruby": 3, "Clover": 1.55}},
                        "Death Clover": {"Chance": 20, "Multis": {"Stone": 5, "White Gems": 5, "Iron": 5, "Obsidian": 5, "Clover": 1.65}},
                        "Oblivion Clover": {"Chance": 40, "Multis": {"Obsidian": 6, "Sapphire": 6, "Clover": 1.8}},
                        "Giant Clover": {"Chance": 285, "Multis": {"Cash": 15, "Multiplier": 15, "Rebirths": 15, "Stone": 15, "Crystal": 15, "Clover": 2}},
                        "Albino Clover": {"Chance": 1000, "Multis": {"Stone": 8, "White Gems": 8, "Iron": 8, "Ruby": 8, "Clover": 2.5}},
                        "Tripetaled": {"Chance": 15000, "Multis": {"Cash": 3, "Multiplier": 3, "Rebirths": 3, "Stone": 3, "White Gems": 3, "Crystal": 3, "Iron": 3, "Gold": 3, "Quartz": 3, "Jade": 3, "Obsidian": 3, "Ruby": 3, "Emerald": 3, "Sapphire": 3, "Diamond": 3, "Clover": 3}},
                        "Oddium": {"Chance": 55000, "Multis": {"Stone": 30, "Iron": 30, "Obsidian": 30, "Ruby": 30, "Emerald": 30, "Clover": 5}},
                        "Dualpetaled": {"Chance": 120000, "Multis": {"Cash": 10, "Multiplier": 10, "Rebirths": 10, "Stone": 10, "White Gems": 10, "Crystal": 10, "Iron": 10, "Gold": 10, "Quartz": 10, "Jade": 10, "Clover": 10}},
                        "Core Clover": {"Chance": 1000001, "Multis": {"Cash": 100, "Rebirths": 100, "White Gems": 100, "Gold": 100, "Jade": 100, "Ruby": 100, "Mint": 10, "Clover": 25}},
                        "Jackpotium": {"Chance": 8000000, "Multis": {"Cash": 1e5, "Multiplier": 1e5, "Rebirths": 1e5, "Stone": 1e5, "White Gems": 1e5, "Crystal": 1e5, "Nissonite": 1000, "Orpiment": 8, "Clover": 1000}},
                        "Reality": {"Chance": 50000000, "Multis": {"Cash": 1e9, "Multiplier": 1e9, "Rebirths": 1e9, "Stone": 1e9, "White Gems": 1e9, "Crystal": 1e9, "Iron": 1e9, "Gold": 1e9, "Quartz": 1e9, "Jade": 1e9, "Obsidian": 1e9, "Ruby": 1e9, "Emerald": 1e9, "Sapphire": 1e9, "Diamond": 1e9, "Starlight": 1e9, "Ion": 1e9, "Uranium": 1e5, "Bismuth": 1e5, "Boracite": 1e5, "Nissonite": 1e5, "Orpiment": 10, "Mint": 1e9, "Clover": 1e9}}
                        }, 1e8, "Clover")
  celebrative_geode = Geode({"Goldenium": {"Chance": 2, "Multis": {"Cash": 1.5, "Multiplier": 1.2}},
                             "Lightroom": {"Chance": 5, "Multis": {"Obsidian": 1.75}},
                             "Dazzlium": {"Chance": 11, "Multis": {"Cash": 2, "Multiplier": 1.7, "Rebirths": 1.7}},
                             "Juled": {"Chance": 50, "Multis": {"Rebirths": 2, "Stone": 1.8}},
                             "Tempested": {"Chance": 400, "Multis": {"Rebirths": 3, "Crystal": 1.5}},
                             "Cyclone": {"Chance": 13000, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2}},
                             "Koanite": {"Chance": 21000, "Multis": {"Crystal": 5, "Quartz": 3}},
                             "Torbdenum": {"Chance": 45000, "Multis": {"Gold": 12, "Jade": 10, "Obsidian": 5}},
                             "Darnite": {"Chance": 100000, "Multis": {"Cash": 1000, "Ruby": 2, "Emerald": 2, "Sapphire": 2}},
                             "Wubium": {"Chance": 500000, "Multis": {"Rebirths": 653, "Crystal": 25, "Obsidian": 8, "Diamond": 3}},
                             "Woofern": {"Chance": 1150000, "Multis": {"Cash": 27, "Multiplier": 27, "Rebirths": 27, "Stone": 27, "White Gems": 27, "Crystal": 27, "Iron": 27, "Gold": 27, "Quartz": 27, "Jade": 27, "Obsidian": 27, "Ion": 10, "Bismuth": 2}},
                             "Acastar": {"Chance": 4750000, "Multis": {"Rebirths": 100, "Quartz": 100, "Sapphire": 100, "Diamond": 100, "Starlight": 100, "Ion": 100}},
                             "Zincton": {"Chance": 9000000, "Multis": {"Cash": 5, "Multiplier": 5, "Rebirths": 5, "Stone": 5, "White Gems": 5, "Crystal": 5, "Iron": 5, "Gold": 5, "Quartz": 5, "Jade": 5, "Orpiment": 3.5}},
                             "Prismatum": {"Chance": 17500000, "Multis": {"Iron": 20, "Gold": 20, "Quartz": 20, "Jade": 20, "Obsidian": 20, "Ruby": 20, "Emerald": 20, "Sapphire": 20, "Diamond": 20, "Starlight": 20, "Ion": 20, "Uranium": 20, "Bismuth": 20, "Boracite": 20, "Nissonite": 20, "Orpiment": 8.5}}},
                            10, "Rebirths")
  spring_geode = Geode({"Vine": {"Chance": 4, "Multis": {"Cash": 10, "Rebirths": 5}},
                        "Dew": {"Chance": 6, "Multis": {"Cash": 25, "Multiplier": 30, "Stone": 20}},
                        "Daisy": {"Chance": 12, "Multis": {"Cash": 100, "Stone": 25, "White Gems": 10}},
                        "Tulip": {"Chance": 33, "Multis": {"Multiplier": 20, "Crystal": 10}},
                        "Aster": {"Chance": 10000, "Multis": {"Stone": 1000, "Gold": 250, "Quartz": 100}},
                        "Honeysuckle": {"Chance": 27500, "Multis": {"Rebirths": 2500, "Iron": 50, "Jade": 25}},
                        "Trollius": {"Chance": 75000, "Multis": {"Stone": 1000, "Crystal": 250, "Gold": 200, "Jade": 100}},
                        "Nymphea": {"Chance": 255000, "Multis": {"White Gems": 2500, "Quartz": 150, "Obsidian": 5}},
                        "Sunflower": {"Chance": 800000, "Multis": {"Stone": 200, "Gold": 1000, "Ruby": 5}},
                        "Yarrow": {"Chance": 3000000, "Multis": {"Cash": 1e6, "Ruby": 200, "Emerald": 200, "Sapphire": 200}},
                        "Windflower": {"Chance": 5000000, "Multis": {"Multiplier": 10000, "Iron": 250, "Obsidian": 50, "Diamond": 15}},
                        "Bachelor's Button": {"Chance": 12500000, "Multis": {"Rebirths": 1e5, "Gold": 500, "Emerald": 35, "Starlight": 5}}
                        }, 25, "Stone")
  easter_geode = Geode({"Egg": {"Chance": 4, "Multis": {"Cash": 2}},
                        "Tainted Egg": {"Chance": 5, "Multis": {"Cash": 10, "Multiplier": 10}},
                        "Spotted Egg": {"Chance": 8, "Multis": {"Rebirths": 10}},
                        "Equinox Egg": {"Chance": 20, "Multis": {"Stone": 10}},
                        "Sugar Egg": {"Chance": 15000, "Multis": {"Multiplier": 100, "White Gems": 15, "Crystal": 10}},
                        "Time Egg": {"Chance": 50500, "Multis": {"Quartz": 25, "Obsidian": 1.1}},
                        "Malicious Egg": {"Chance": 125000, "Multis": {"Rebirths": 10000, "Iron": 1000, "Jade": 20}},
                        "Stained Glass Egg": {"Chance": 6000000, "Multis": {"Stone": 3, "White Gems": 3, "Crystal": 3, "Iron": 3, "Gold": 3, "Quartz": 3, "Jade": 3, "Obsidian": 3, "Ruby": 3}},
                        "Space Egg": {"Chance": 6000000, "Multis": {"White Gems": 42, "Crystal": 42, "Obsidian": 10, "Ruby": 2}},
                        "Gravitational Egg": {"Chance": 6000000, "Multis": {"Cash": 4, "Multiplier": 4, "Rebirths": 4, "Stone": 4, "White Gems": 4, "Crystal": 4, "Iron": 4, "Gold": 4, "Quartz": 4, "Jade": 4, "Obsidian": 4}},
                        "EGG9000": {"Chance": 6000000, "Multis": {"Stone": 9000, "White Gems": 9000, "Crystal": 9000, "Iron": 9000, "Gold": 9000, "Quartz": 900, "Jade": 90, "Obsidian": 9}},
                        "Dust Devil Egg": {"Chance": 6000000, "Multis": {"Multiplier": 3e6, "White Gems": 300, "Quartz": 35, "Obsidian": 3, "Ruby": 2.5}},
                        "Black Iron Fabergé": {"Chance": 25000000, "Multis": {"Iron": 1e12, "Obsidian": 1e6, "Uranium": 1.25}},
                        "Gilded Fabergé": {"Chance": 25000000, "Multis": {"Cash": 1e12, "Stone": 1000, "Crystal": 500, "Emerald": 100, "Sapphire": 5}},
                        "Royal Fabergé": {"Chance": 25000000, "Multis": {"Cash": 1e9, "Gold": 1e6, "Diamond": 5, "Uranium": 1.5}},
                        "Easter Basket": {"Chance": 100000000, "Multis": {"Cash": 100, "Multiplier": 100, "Rebirths": 100, "Stone": 100, "White Gems": 100, "Crystal": 100, "Iron": 100, "Gold": 100, "Quartz": 100, "Jade": 100, "Obsidian": 100, "Ruby": 100, "Emerald": 100, "Sapphire": 100, "Diamond": 100, "Starlight": 100, "Ion": 100, "Uranium": 100, "Bismuth": 100, "Boracite": 25, "Nissonite": 10, "Orpiment": 5, "Orpiment_2": 5, "Tetra": 10000, "Volt": 100, "Aquamarine": 15, "Lollipop": 5, "Stargazed Metal": 15, "Gyge": 5, "Auly Plate": 2}},
                        "Egg of Destiny": {"Chance": 1000000000000, "Multis": {"Cash": Mantissa(1,303), "Multiplier": Mantissa(1,303), "Rebirths": Mantissa(1,303), "Stone": Mantissa(1,303), "White Gems": Mantissa(1,303), "Crystal": Mantissa(1,303), "Iron": Mantissa(1,303), "Gold": Mantissa(1,303), "Quartz": Mantissa(1,303), "Jade": Mantissa(1,303), "Obsidian": Mantissa(1,303), "Ruby": Mantissa(1,303), "Emerald": Mantissa(1,303), "Sapphire": Mantissa(1,303), "Diamond": Mantissa(1,303), "Starlight": Mantissa(1,303), "Ion": Mantissa(1,303), "Uranium": Mantissa(1,303), "Bismuth": Mantissa(1,303), "Boracite": Mantissa(1,303), "Nissonite": Mantissa(1,303), "Orpiment": Mantissa(1,303), "Tetra": Mantissa(1,303), "Volt": Mantissa(1,303), "Aquamarine": Mantissa(1,303), "Lollipop": Mantissa(1,303), "C0RR8PT10N": Mantissa(1,303), "Stargazed Metal": 1e100, "Gyge": 1e50, "Auly Plate": 1e25, "Shell Piece": 100000, "Prime Alpha Key": 1000}}
                        }, 7, "Event Power")
  fabled_geode = Geode({"Shinestone": {"Chance": 5, "Multis": {"Cash": 1e12, "Rebirths": 1e9}},
                        "Yen": {"Chance": 5, "Multis": {"Cash": 2, "Multiplier": 2}},
                        "Ascension": {"Chance": 5, "Multis": {"Rebirths": 800, "Stone": 400, "White Gems": 200, "Crystal": 100, "Iron": 50, "Gold": 25}},
                        "Translucid Gem": {"Chance": 10, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2}},
                        "Luminant Crystal": {"Chance": 10, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2}},
                        "Exotic Metal": {"Chance": 20, "Multis": {"Cash": 2, 'Multiplier': 2, "Rebirths": 2, "Stone": 2, "Crystal": 2}},
                        "Polyhedral Gold": {"Chance": 20, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "Crystal": 2, "Iron": 2}},
                        "Luxurious Quartz": {"Chance": 33, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "Crystal": 2, "Iron": 2, "Gold": 2}},
                        "Scarlet Jade": {"Chance": 33, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2}},
                        "Reflected Obsidian": {"Chance": 100, "Multis": {"Cash": 2, "Multiplier": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2}},
                        "Chromio": {"Chance": 100, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2}},
                        "Clusterized Diamond": {"Chance": 200, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2}},
                        "Cosmodryal": {"Chance": 200, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2}},
                        "Augmented Ion": {"Chance": 1000, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2, "Starlight": 2}},
                        "Symmetrite": {"Chance": 1000, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2, "Ion": 2}},
                        "Levigated Bismuth": {"Chance": 2000, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2, "Ion": 2, "Uranium": 2}},
                        "Niflhemic Boracite": {"Chance": 4000, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2, "Ion": 2, "Uranium": 2, "Bismuth": 2}},
                        "Encored Nissonite": {"Chance": 4000, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2, "Ion": 2, "Uranium": 2, "Bismuth": 2, "Boracite": 2}},
                        "Ethereal Orpiment": {"Chance": 12500, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2, "Ion": 2, "Uranium": 2, "Bismuth": 2, "Boracite": 2, "Nissonite": 2}},
                        "Charged Tetra": {"Chance": 30000, "Multis": {"Cash": 1.5, "Multiplier": 1.5, "Rebirths": 1.5, "Stone": 1.5, "White Gems": 1.5, "Crystal": 1.5, "Iron": 1.5, "Gold": 1.5, "Quartz": 1.5, "Jade": 1.5, "Obsidian": 1.5, "Ruby": 1.5, "Emerald": 1.5, "Sapphire": 1.5, "Diamond": 1.5, "Ion": 1.5, "Uranium": 1.5, "Bismuth": 1.5, "Boracite": 1.5, "Nissonite": 1.5, "Orpiment": 1.5}},
                        "Overclocked Volt": {"Chance": 75000, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2, "Sapphire": 2, "Diamond": 2, "Ion": 2, "Uranium": 2, "Bismuth": 2, "Boracite": 2, "Nissonite": 2, "Orpiment": 2}},
                        "Agate": {"Chance": 125000, "Multis": {"Jade": 1e9, "Diamond": 1e9, "Ion": 1e5}},
                        "Bustamite": {"Chance": 175000, "Multis": {"Iron": 1e9, "Sapphire": 1000, "Starlight": 20000}},
                        "Polycrase": {"Chance": 262000, "Multis": {"Cash": 1e15, "Stone": 1e12, "Quartz": 1e9, "Ruby": 1e6}},
                        "Stolzite": {"Chance": 363000, "Multis": {"Gold": 1e12, "Emerald": 1e9, "Uranium": 100}},
                        "Zeunerite": {"Chance": 532000, "Multis": {"Jade": 1e12, "Emerald": 1e9, "Starlight": 1000, "Boracite": 100}},
                        "Phosphophyllite": {"Chance": 750000, "Multis": {"Sapphire": 1e9, "Diamond": 2e6, "Ion": 1000, "Uranium": 400}},
                        "Haxonite": {"Chance": 958000, "Multis": {"Ruby": 1e6, "Emerald": 1e15, "Starlight": 1e12, "Boracite": 600}},
                        "Glaucodot": {"Chance": 987000, "Multis": {"Diamond": 1000, "Starlight": 1000, "Ion": 1000, "Uranium": 1000, "Bismuth": 1e6}},
                        "Dyscrasite": {"Chance": 1525000, "Multis": {"Sapphire": 1e7, "Ion": 10000, "Boracite": 1000, "Nissonite": 10}},
                        "Bazzite": {"Chance": 3321000, "Multis": {"Jade": 1e15, "Diamond": 1e9, "Bismuth": 100000, "Nissonite": 100}},
                        "Cornubite": {"Chance": 5216000, "Multis": {"Emerald": 1e12, "Ion": 1e6, "Boracite": 100000, "Nissonite": 1000}},
                        "Kostovite": {"Chance": 7521000, "Multis": {"Sapphire": 1e15, "Starlight": 1.9e10, "Nissonite": 10000, "Orpiment": 15}},
                        "Minium": {"Chance": 10526000, "Multis": {"Diamond": 1e15, "Bismuth": 100000, "Orpiment": 100}},
                        "Nyerereite": {"Chance": 22878000, "Multis": {"Ruby": 1e21, "Uranium": 1e12, "Orpiment": 650}},
                        "Peridot": {"Chance": 60648000, "Multis": {"Obsidian": 1e99, "Starlight": 1e21, "Nissonite": 1e6, "Opriment": 5000}},
                        "Realgar": {"Chance": 80632000, "Multis": {"Diamond": 1e22, "Ion": 1e12, "Opriment": 500, "Tetra": 1.25}},
                        "Ereus": {"Chance": 100742000, "Multis": {"Cash": Mantissa(1,300), "Ruby": 1e33, "Bismuth": 1e15, "Nissonite": 1e9, "Tetra": 1e10, "Volt": 50000, "Aquamarine": 1000, "Lollipop": 25, "Stargazed Metal": 20, "Gyge": 5, "Auly Plate": 3, "Shell Piece": 1.1}},
                        "Existence": {"Chance": 500000000, "Multis": {"Cash": Mantissa(1,303), "Multiplier": Mantissa(1,303), "Rebirths": Mantissa(1,303), "Stone": Mantissa(1,303), "White Gems": Mantissa(1,303), "Crystal": Mantissa(1,303), "Iron": 1e273, "Gold": 1e243, "Quartz": 1e213, "Jade": 1e183, "Obsidian": 1e153, "Ruby": 1e123, "Emerald": 1e93, "Sapphire": 1e63, "Diamond": 1e45, "Starlight": 1e30, "Ion": 1e15, "Uranium": 1e12, "Bismuth": 1e9, "Boracite": 1e6, "Nissonite": 10000, "Orpiment": 100, "Tetra": 4, "Aquamarine": 1e9, "Lollipop": 150, "C0RR8PT10N": 5, "Gyge": 97.2, "Auly Plate": 10, "Shell Piece": 3}}
                        }, 1000, "Diamond")
  #----------- AREAS --------------
  Spawn_Buttons = {
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
         ("Stone Geode: 1M Stone", lambda btn: Geode_roll(btn, stone_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
         ("White Gems Geode: 30 White Gems", lambda btn: Geode_roll(btn, gems_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
         ("Jade Geode: 500 Jade", lambda btn: Geode_roll(btn, jade_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
         ("Uranium Geode: 12 Uranium", lambda btn: Geode_roll(btn, uranium_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
      ],
      "Area Teleports": [
         ("Caves (req: 10 Stone)", lambda: load_check(10, "Stone", Cave_Buttons)),
         ("Crystal Beneaths (req: 300 White Gems)", lambda: load_check(300, "White Gems", Crystal_Buttons)),
         ("Iron Shafts (req: 100 Crystal)", lambda: load_check(100, "Crystal", Iron_Buttons)),
         ("Golden Quarry (req: 750 Iron)", lambda: load_check(750,"Iron",Gold_Buttons)),
         ("Quartz Walkway (req: 75 Gold)", lambda: load_check(75,"Gold", Quartz_Buttons)),
         ("Jade Forest (req: 450 Quartz)", lambda: load_check(450,"Quartz", Jade_Buttons)),
         ("Obsidian Abyss (req: 80 Jade)", lambda: load_check(80, "Jade", Obsidian_Buttons)),
         ("Colour Temple (req: 5 Obsidian)", lambda: load_check(5, "Obsidian", Colour_Buttons)),
         ("Extraterrestrial Orbits (req: 50k Sapphire)", lambda: load_check(5e4, "Sapphire", ET_Buttons)),
         ("Empyrean Island (req: 100 Starlight)", lambda: load_check(100, "Starlight", Ion_Buttons)),
         ("Uranium Wastelands (req: 3 Ion)", lambda: load_check(3, "Ion", Uranium_Buttons)),
         ("Smooth Depths (req: 15 Uranium)", lambda: load_check(15, "Uranium", Bismuth_Buttons)),
         ("Icy Palace (req: 50 Bismuth)", lambda: load_check(50, "Bismuth", Icy_Buttons)),
         ("Floating Purgatory (req: 10 Nissonite)", lambda: load_check(10, "Nissonite", Orpiment_Buttons)),
         ("Tetratum (req: 500 Orpiment)", lambda: load_check(500, "Orpiment", Tetra_Buttons)),
         ("Voltaic Sector (req: 50 Tetra)", lambda: load_check(50, "Tetra", Volt_Buttons)),
         ("Abyssal Trenches (req: 3 Volt)", lambda: load_check(3, "Volt", Aquamarine_Buttons)),
         ("Flourish Candylands (req: 25 Aquamarine)", lambda: load_check(25, "Aquamarine", Lollipop_Buttons)),
         ("Minty Grooves (req: 5 Rebirths)", lambda: load_check(5, "Rebirths", Mint_Buttons)),
         ("Geode Site (req: 1 Lollipop)", lambda: load_check(1, "Lollipop", Geode_Buttons)),
         ("Elysian Stratosphere (req: 100 Lollipop)", lambda: load_world(100, "Lollipop", Elysian_Buttons, "Master Cash", "Master Multiplier", "Master Rebirths", "Master Gems", "Mastery", "Master Event Power")),
         ("Recover Hall (req: 0 Cash)", lambda: load_check(0, "Cash", Recover_Hall_Buttons))
     ],
     "Extra": [
         ("Console inputs", lambda: secret_input("Spawn"))
     ]
  }
  Cave_Buttons = {
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
         ("Crystal Beneaths (req: 300 White Gems)", lambda: load_check(300, "White Gems", Crystal_Buttons)),
         ("Spawn (req: 0 Cash)", lambda: load_check(0, "Cash", Spawn_Buttons)),
         ("Recover Hall (req: 0 Cash)", lambda: load_check(0, "Cash", Recover_Hall_Buttons))
      ]
  }
  Recover_Hall_Buttons = {
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
          ("Orpiment Geode: 2 Orpiment", lambda btn: Geode_roll(btn, orpiment_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
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
          ("Anticovery Hall (req: 1 Testium)", lambda: load_check(1, "Testium", Anticovery_Buttons)),
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
          ("Spawn (req: 0 Cash)", lambda: load_check(0, "Cash", Spawn_Buttons)),
          ("Caves (req: 10 Stone)", lambda: load_check(10, "Stone", Cave_Buttons)),
          ("Crystal Beneaths (req: 300 White Gems)", lambda: load_check(300, "White Gems", Crystal_Buttons)),
          ("Iron Shafts (req: 100 Crystal)", lambda: load_check(100, "Crystal", Iron_Buttons)),
          ("Golden Quarry (req: 750 Iron)", lambda: load_check(750,"Iron",Gold_Buttons)),
          ("Quartz Walkway (req: 75 Gold)", lambda: load_check(75,"Gold", Quartz_Buttons)),
          ("Jade Forest (req: 450 Quartz)", lambda: load_check(450,"Quartz", Jade_Buttons)),
          ("Obsidian Abyss (req: 80 Jade)", lambda: load_check( 80, "Jade", Obsidian_Buttons)),
          ("Colour Temple (req: 5 Obsidian)", lambda: load_check( 5, "Obsidian", Colour_Buttons)),
          ("Extraterrestrial Orbits (req: 50k Sapphire)", lambda: load_check( 5e4, "Sapphire", ET_Buttons)),
          ("Empyrean Island (req: 100 Starlight)", lambda: load_check( 100, "Starlight", Ion_Buttons)),
          ("Uranium Wastelands (req: 3 Ion)", lambda: load_check( 3, "Ion", Uranium_Buttons)),
          ("Smooth Depths (req: 15 Uranium)", lambda: load_check( 15, "Uranium", Bismuth_Buttons)),
          ("Icy Palace (req: 50 Bismuth)", lambda: load_check( 50, "Bismuth", Icy_Buttons)),
          ("Icy Palace (req: 1 Nissonite)", lambda: load_check( 1, "Nissonite", Icy_Buttons)),
          ("Floating Purgatory (req: 10 Nissonite)", lambda: load_check( 10, "Nissonite", Orpiment_Buttons)),
          ("Tetratum (req: 500 Orpiment)", lambda: load_check( 500, "Orpiment", Tetra_Buttons)),
          ("Voltaic Sector (req: 50 Tetra)", lambda: load_check( 50, "Tetra", Volt_Buttons)),
          ("Abyssal Trenches (req: 3 Volt)", lambda: load_check( 3, "Volt", Aquamarine_Buttons)),
          ("Flourish Candylands (req: 25 Aquamarine)", lambda: load_check( 25, "Aquamarine", Lollipop_Buttons)),
          ("Minty Grooves (req: 5 Rebirths)", lambda: load_check( 5, "Rebirths", Mint_Buttons)),
      ]
  }
  Crystal_Buttons = {
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
          ("Crystal Geode: 100 Crystal", lambda btn: Geode_roll(btn, crystal_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll))
      ],
      "Area Teleports": [
         ("Iron Shafts (req: 100 Crystal)", lambda: load_check(100, "Crystal", Iron_Buttons)),
         ("Spawn (req: 0 Cash)", lambda: load_check(0, "Cash", Spawn_Buttons)),
         ("Recover Hall (req: 0 Cash)", lambda: load_check(0, "Cash", Recover_Hall_Buttons))
      ]
  }
  Iron_Buttons = {
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
          ("Iron Geode: 25 Iron", lambda btn: Geode_roll(btn, iron_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check(0, "Cash", Spawn_Buttons)),
         ("Recover Hall (req: 0 Cash)", lambda: load_check(0, "Cash", Recover_Hall_Buttons)),
         ("Golden Quarry (req: 750 Iron)", lambda: load_check(750,"Iron",Gold_Buttons)),
      ]
  }
  Gold_Buttons = {
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
          ("Gold Geode: 60 Gold", lambda btn: Geode_roll(btn, gold_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check(0, "Cash", Spawn_Buttons)),
         ("Recover Hall (req: 0 Cash)", lambda: load_check(0, "Cash", Recover_Hall_Buttons))
      ]
  }
  Quartz_Buttons = {
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
          ("Quartz Geode: 30 Quartz", lambda btn: Geode_roll(btn, quartz_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check(0, "Cash", Spawn_Buttons)),
         ("Recover Hall (req: 0 Cash)", lambda: load_check(0, "Cash", Recover_Hall_Buttons))
      ]
  }
  Jade_Buttons = {
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
           ("Emoji Geode: 1k Gems", lambda btn: Geode_roll(btn, emoji_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check(0, "Cash", Spawn_Buttons)),
         ("Recover Hall (req: 0 Cash)", lambda: load_check(0, "Cash", Recover_Hall_Buttons))
      ]
  }
  Obsidian_Buttons = {
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
          ("Obsidian Geode: 1 Obsidian", lambda btn: Geode_roll(btn, obsidian_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check(0, "Cash", Spawn_Buttons)),
         ("Recover Hall (req: 0 Cash)", lambda: load_check(0, "Cash", Recover_Hall_Buttons))
      ]
  }
  Colour_Buttons = {
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
          ("100 Boracite: 1 Hexaferrum", lambda: cost_button( "Boracite", 100, "Hexaferrum", 1, "Geode")),
          ("15 Yrnote: 1 Antimatter", lambda: cost_button("Geode", "Yrnote", 15, "Antimatter", 1, "Geode")),
          ("100 Pseudomalachite: 1 Yhed", lambda: cost_button("Geode", "Pseudomalachite", 100, "Yhed", 1, "Geode")),
          ("1e3030 Stone: 1 Dezyp", lambda: cost_button( "Stone", Mantissa(1,3030), "Dezyp", 1, "Geode")),
          ("10M Dezyp: 1 Podrillium", lambda: cost_button("Geode", "Dezyp", 1e7, "Podrillium", 1, "Geode")),
      ],
      "Geodes": [
          ("Ruby Geode: 100k Ruby", lambda btn: Geode_roll(btn, ruby_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Emerald Geode: 100k Emerald", lambda btn: Geode_roll(btn, emerald_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Sapphire Geode: 100k Sapphire", lambda btn: Geode_roll(btn, sapphire_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check(0, "Cash", Spawn_Buttons)),
         ("Recover Hall (req: 0 Cash)", lambda: load_check(0, "Cash", Recover_Hall_Buttons))
      ]
  }
  ET_Buttons = {
      "Ruby": [
          ("50Sx Obsidian: 3 Ruby", lambda: reset_button( 5e22, "Obsidian", 3, "Ruby")),
          ("600Sp Obsidian: 10 Ruby", lambda: reset_button( 6e26, "Obsidian", 10, "Ruby")),
          ("20No Obsidian: 40 Ruby", lambda: reset_button( 2e31, "Obsidian", 40, "Ruby")),
      ],
      "Emerald": [
          ("3Qn Ruby: 5 Emerald", lambda: cost_button("Ruby",3e18, "Emerald", 5)),
          ("400Qn Ruby: 14 Emerald", lambda: cost_button("Ruby",4e20, "Emerald", 14)),
          ("10Sx Ruby: 40 Emerald", lambda: cost_button("Ruby",1e22, "Emerald", 40)),
      ],
      "Sapphire": [
          ("2B Emerald: 10 Sapphire", lambda: cost_button( "Emerald", 2e9, "Sapphire", 10)),
          ("50B Emerald: 30 Sapphire", lambda: cost_button( "Emerald", 5e10, "Sapphire", 30)),
          ("400T Emerald: 100 Sapphire", lambda: cost_button( "Emerald", 4e14, "Sapphire", 100)),
      ],
      "Diamond": [
          ("500k Sapphire: 1 Diamond", lambda: reset_button( 5e5, "Sapphire", 1, "Diamond")),
          ("3M Sapphire: 3 Diamond", lambda: reset_button( 3e6, "Sapphire", 3, "Diamond")),
          ("15M Sapphire: 10 Diamond", lambda: reset_button( 1.5e7, "Sapphire", 10, "Diamond")),
      ],
      "Starlight": [
          ("5 Diamond: 1 Starlight", lambda: reset_button( 5, "Diamond", 1, "Starlight")),
          ("30 Diamond: 4 Starlight", lambda: reset_button( 30, "Diamond", 4, "Starlight")), 
          ("86 Diamond: 10 Starlight", lambda: reset_button( 86, "Diamond", 10, "Starlight")),
      ],
      "Recovery": [
          ("1 Ruby: 50 Jade (Fetch)", lambda: recovery_button_fetch(1, "Ruby", 50, "Jade")),
      ],
      "Geodes": [
          ("Diamond Geode: 2.5k Diamond", lambda btn: Geode_roll(btn, diamond_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Starlight Geode: 60 Starlight", lambda btn: Geode_roll(btn, starlight_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Ion Geode: 5 Ion", lambda btn: Geode_roll(btn, ion_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check(0, "Cash", Spawn_Buttons)),
         ("Recover Hall (req: 0 Cash)", lambda: load_check(0, "Cash", Recover_Hall_Buttons))
      ],
      "                                                                                                                                                                              ": [],
      "???": [("1 Stellarite (req: 300k Sapphire)", lambda: recovery_button_set( 300000, "Sapphire", 1, "Stellarite", "Secret")),
              ("Wormhole's Breech (req: 1 Stellarite)", lambda: load_check("Secret", 1, "Stellarite", Wormhole_Buttons))],
      "                                                                                                                                            ": []
  }
  Ion_Buttons = {
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
         ("Spawn (req: 0 Cash)", lambda: load_check(0, "Cash", Spawn_Buttons)),
         ("Recover Hall (req: 0 Cash)", lambda: load_check(0, "Cash", Recover_Hall_Buttons))
      ]
  }
  Uranium_Buttons = {
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
          ("Scared Geode: 1B Gems", lambda btn: Geode_roll(btn, sacred_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check(0, "Cash", Spawn_Buttons)),
         ("Recover Hall (req: 0 Cash)", lambda: load_check(0, "Cash", Recover_Hall_Buttons))
      ]
  }
  Bismuth_Buttons = {
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
          ("Bismuth Geode: 50 Bismuth", lambda btn: Geode_roll(btn, bismuth_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check(0, "Cash", Spawn_Buttons)),
         ("Recover Hall (req: 0 Cash)", lambda: load_check(0, "Cash", Recover_Hall_Buttons))
      ]
  }
  Icy_Buttons = {
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
          ("Boracite Geode: 1k Boracite", lambda btn: Geode_roll(btn, boracite_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Nissonite Geode: 5 Nissonite", lambda btn: Geode_roll(btn, nissonite_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check(0, "Cash", Spawn_Buttons)),
         ("Recover Hall (req: 0 Cash)", lambda: load_check(0, "Cash", Recover_Hall_Buttons))
      ]
  }
  Orpiment_Buttons = {
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
         ("Spawn (req: 0 Cash)", lambda: load_check(0, "Cash", Spawn_Buttons)),
         ("Recover Hall (req: 0 Cash)", lambda: load_check(0, "Cash", Recover_Hall_Buttons))
      ]
  }
  Tetra_Buttons = {
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
         ("Spawn (req: 0 Cash)", lambda: load_check(0, "Cash", Spawn_Buttons)),
         ("Recover Hall (req: 0 Cash)", lambda: load_check(0, "Cash", Recover_Hall_Buttons))
      ],
      "Extra": [
          ("Console Input", lambda: secret_input("Tetratum"))
      ],
      "???": [
          ("Graphite Puzzle", lambda: image_load("graphite.png"))
      ]
  }
  Volt_Buttons = {
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
          ("1e108003 Iron: 1e320 Gold", lambda: reset_button(Mantissa(1,108003), "Iron", 1e320,"Gold")),
          ("1e109003 Iron: 1e360 Gold", lambda: reset_button(Mantissa(1,109003), "Iron", 1e360,"Gold")),
          ("1e110003 Iron: 1e400 Gold", lambda: reset_button(Mantissa(1,110003), "Iron", 1e400,"Gold")),
          ("1e111003 Iron: 1e440 Gold", lambda: reset_button(Mantissa(1,111003), "Iron", 1e440,"Gold")),
          ("1e112003 Iron: 1e480 Gold", lambda: reset_button(Mantissa(1,112003), "Iron", 1e480,"Gold")),
          ("1e113003 Iron: 1e520 Gold", lambda: reset_button(Mantissa(1,113003), "Iron", 1e520,"Gold")),
          ("1e114003 Iron: 1e560 Gold", lambda: reset_button(Mantissa(1,114003), "Iron", 1e560,"Gold")),
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
         ("Spawn (req: 0 Cash)", lambda: load_check(0, "Cash", Spawn_Buttons)),
         ("Recover Hall (req: 0 Cash)", lambda: load_check(0, "Cash", Recover_Hall_Buttons))
      ],
      "Unknown": [("", lambda: blinded())]
  }
  Aquamarine_Buttons = {
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
         ("Spawn (req: 0 Cash)", lambda: load_check(0, "Cash", Spawn_Buttons)),
         ("Recover Hall (req: 0 Cash)", lambda: load_check(0, "Cash", Recover_Hall_Buttons))
      ]
  }
  Lollipop_Buttons = {
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
         ("Spawn (req: 0 Cash)", lambda: load_check(0, "Cash", Spawn_Buttons)),
         ("Recover Hall (req: 0 Cash)", lambda: load_check(0, "Cash", Recover_Hall_Buttons))
      ]
  }
  Anticovery_Buttons = {
      "Lollipop": [
          ("1M Aquamarine: 75 Lollipop", lambda: reset_button( 1e6, "Aquamarine", 75, "Lollipop")),
          ("100M Aquamarine: 300 Lollipop", lambda: reset_button( 1e8, "Aquamarine", 300, "Lollipop")),
          ("10B Aquamarine: 1.5k Lollipop", lambda: reset_button( 1e10, "Aquamarine", 1500, "Lollipop")),
          ("1T Aquamarine: 5k Lollipop", lambda: reset_button( 1e12, "Aquamarine", 5000, "Lollipop")),
          ("10Qd Aquamarine: 10k Lollipop", lambda: reset_button( 1e16, "Aquamarine", 10000, "Lollipop")),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check(0, "Cash", Spawn_Buttons)),
         ("Recover Hall (req: 0 Cash)", lambda: load_check(0, "Cash", Recover_Hall_Buttons))
      ]
  }
  Mint_Buttons = {
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
          ("Mint Geode: 2k Mint", lambda btn: Geode_roll(btn, mint_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check(0, "Cash", Spawn_Buttons)),
         ("Recover Hall (req: 0 Cash)", lambda: load_check(0, "Cash", Recover_Hall_Buttons))
      ]
  }
  Geode_Buttons = {
      "Event Stats": [
          ("7.5k Event Power: 3 Clover", lambda: cost_button( "Event Power", 7500, "Clover", 3)),
          ("15k Event Power: 25 Heart", lambda: cost_button( "Event Power", 15000, "Heart", 25)),
          ("400 Event Power: 10 Orange Pumpkin", lambda: cost_button( "Event Power", 400, "Orange Pumpkin", 10)),
          ("2k Event Power: 8 Ray", lambda: cost_button("Event Power", 2000, "Ray", 8)),
          ("1.2k Ray: 10 Patriotic Crystal", lambda: reset_button_special(1200, "Ray", 10, "Patriotic Crystal", ["Ray"])),
          ("500 Patriotic Crystal: 3 Aureal Gem", lambda: reset_button_special(500, "Patriotic Crystal", 3, "Aureal Gem", "Event", ["Ray", "Patriotic Crystal"])),
          ("180 Aureal Gem: 1 Fragment", lambda: reset_button_special(180, "Aureal Gem", 1, "Fragment", ["Ray", "Patriotic Crystal", "Aureal Gem"]))
      ],
      "Geodes": [
          ("Hearted Geode: 50 Heart", lambda btn: Geode_roll(btn, hearted_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Luck Geode: 3 Clover", lambda btn: Geode_roll(btn, luck_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Clover Geode: 100M Clover", lambda btn: Geode_roll(btn, clover_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Celebrative Geode: 10 Rebirths", lambda btn: Geode_roll(btn, celebrative_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Spring Geode: 25 Stone", lambda btn: Geode_roll(btn, spring_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Easter Geode: 7 Event Power", lambda btn: Geode_roll(btn, easter_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
          ("Fabled Geode: 1k Diamond", lambda btn: Geode_roll(btn, fabled_geode, luck, (1-(upgrades["geode_speed"]["effect"]*upgrades["geode_speed"]["current_lvl"])), bulk_roll)),
      ],
      "Area Teleports": [
      ],
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check(0, "Cash", Spawn_Buttons)),
         ("Recover Hall (req: 0 Cash)", lambda: load_check(0, "Cash", Recover_Hall_Buttons))
      ]
  }
  Elysian_Buttons = {
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
      "Tempestuar Buttons": [
          ("1Qd Master Multiplier: 30k Master Rebirths", lambda: reset_button(1e15, "Master Multiplier", 30000, "Master Rebirths")),
          ("100Qd Master Multiplier: 75k Master Rebirths", lambda: reset_button(1e17, "Master Multiplier", 75000, "Master Rebirths")),
          ("1Sx Master Multiplier: 300k Master Rebirths", lambda: reset_button(1e21, "Master Multiplier", 300000, "Master Rebirths")),
          ("1No Master Multiplier: 1.5M Master Rebirths", lambda: reset_button(1e30, "Master Multiplier", 1.5e6, "Master Rebirths")),
      ],
      "Recovery Buttons": [
          ("1 Master Stone: 4.5 Master Multiplier (fetch)", lambda: recovery_button_fetch(1, "Master Stone", 4.5, "Master Multiplier")),
          ("12 Master Stone: 150 Master Rebirths (sets)", lambda: recovery_button_fetch(12, "Master Stone", 150, "Master Rebirths")),
          ("1 Master White Gems: 1 Master Rebirths (fetch)", lambda: recovery_button_fetch(1, "Master White Gems", 1, "Master Rebirths"))
      ]
  }
  Wormhole_Buttons = {
      "Area Teleports": [
         ("Spawn (req: 0 Cash)", lambda: load_check(0, "Cash", Spawn_Buttons)),
         ("Recover Hall (req: 0 Cash)", lambda: load_check(0, "Cash", Recover_Hall_Buttons))
      ],
      "???": [
          ("Puzzle 1", lambda: image_load("Galaxite/Galaxite1.png")),
          ("Puzzle 2", lambda: image_load("Galaxite/Galaxite2.png")),
          ("Puzzle 3", lambda: image_load("Galaxite/Galaxite3.png"))
      ],
      "Extra": [
          ("Console Input", lambda: secret_input("Wormhole"))
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
              self._populate_initial_stats()
  
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
  
          def _populate_initial_stats(self):
              for category, stats in abs_stat_info.items():
                  # Category label
                  cat = QLabel(category)
                  cat.setStyleSheet("font-weight: bold; font-size: 24px; margin-top: 8px;")
                  self.grid.addWidget(cat, self.current_row, 0, 1, 2)
                  self.current_row += 1
                  if category == "Geode":
                      for geode, geode_stats in stats.items():
                          g_cat = QLabel(geode)
                          g_cat.setStyleSheet("font-weight: bold; font-size: 16px; margin-top: 8px;")
                          self.grid.addWidget(g_cat, self.current_row, 0, 1, 2)
                          self.current_row += 1
                          stat_items = geode_stats.items()
                          for stat_name, stat_data in stat_items:
                              self._add_new_stat_row(category, stat_name)
                  else:
                    stat_items = stats.items()
                  if category != "Geode":
                    for stat_name, stat_data in stat_items:
                      self._add_new_stat_row(category, stat_name)
  
          # -------------------------------------------------------
  
          def _add_new_stat_row(self, category, stat_name):
  
              # Stat name
              if stat_name in list(stat_gradients.keys()):
                  gradient = stat_gradients[stat_name].get("Colours", ["#ffffff", "#ffffff"])
                  angle = stat_gradients[stat_name].get("Angle", 90)
                  stroke_colour = stat_gradients[stat_name].get("S_Colour")
                  stroke_width = stat_gradients[stat_name].get("S_Width", 0)
              else:
                  gradient = stat_gradients["Default"]["Colours"]
                  angle = stat_gradients["Default"]["Angle"]
                  stroke_colour = None
                  stroke_width = 0
              name_label = GradientLabel(stat_name, gradient, angle, stroke_color=stroke_colour, stroke_width=stroke_width)
              self.grid.addWidget(name_label, self.current_row, 0)
  
              # Value formatting
              try:
                value = stat_increment.get(stat_name)
    
                if isinstance(value, Mantissa):
                    text = value.to_string()
                elif isinstance(value, (int, float)):
                    text = str(round(value, 6))
                else:
                    text = str(0)
    
                value_label = QLabel(text)
                self.grid.addWidget(value_label, self.current_row, 1, alignment=Qt.AlignRight)
    
                # Store for later updates
                self.stat_labels[(category, stat_name)] = value_label
    
                self.current_row += 1
              except AttributeError:
                  pass
  
          # -------------------------------------------------------
  
          def update_stats(self, stat_increment):
  
              # Update values of existing stats
              for (category, stat_name), label in list(self.stat_labels.items()):
                  try:
                      value = stat_increment["Stats"][stat_name]
  
                      if isinstance(value, Mantissa):
                          text = value.to_string()
                      elif isinstance(value, (int, float)):
                          text = str(round(value, 6))
                      else:
                          text = str(0)
  
                      label.setText(text)
  
                  except KeyError:
                      label.setText("0")
  
              # Detect new stats dynamically
              for category, stats in abs_stat_info.items():
                  stat_items = stats.items()
                  if category != "Geode":
                    for stat_name, stat_data in stat_items:
                        if (category, stat_name) not in self.stat_labels:
                            self._add_new_stat_row(category, stat_name)
  
      # ----------------------------
      # Create and show the dialog
      # ----------------------------
      win = StatMenu(parent)
      win.show()
      return win
  def open_boosts_menu(parent):
    class UpgradeMenu(QDialog):
        def __init__(self, save_data, parent=None):
            super().__init__(parent)
    
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
    
            #layout
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
            if stat_increment["Stats"]["Gems"] < cost:
                return  # or display a popup
    
            # Apply purchase
            stat_increment["Stats"]["Gems"] -= cost
            level += 1
            self.save_data[upgrade_id]["current_lvl"] = level
    
            # Update UI
            level_label.setText(f"Level: {level}/{info['max_level']}")
            if level >= info["max_level"]:
                buy_button.setDisabled(True)
            else:
                cost_label.setText(f"Cost: {upgrade_cost(info, level)} gems")
    win = UpgradeMenu(upgrades, parent)
    win.show()
    return win
  stat_menu = QPushButton("Open Stat Menu")
  stat_menu.clicked.connect(lambda: open_stat_menu(root, stat_increment))
  boosts_menu = QPushButton("Boosts")
  boosts_menu.clicked.connect(lambda: open_boosts_menu(root))
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
  if 'simpleaudio' in sys.modules and 'pydub' in sys.modules:
    threading.Thread(target=play_music, daemon=True).start()
  cash_increase()
  gem_increase()
  event_increase()
  root.show()
  app.exec()