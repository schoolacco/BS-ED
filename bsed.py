from tkinter import *
from tkinter import ttk
import simpleaudio as sa
import json
from pydub import AudioSegment
import time
import datetime
import threading
import math
import os
import random
from Module import Mantissa, tkinter_frames, Geode
MANTISSA_THRESHOLD = 1e300
luck = 6
def Geode_roll(geode, luck=1):
    global stat_increment
    stat_increment = geode.open(stat_increment,luck)
def load_check(key, req, unit, buttons):
    global stat_increment, frame, canvas, scrollbar, x_scrollbar, container
    amount = stat_increment[key][unit]["Value"]
    req = float_to_mantissa(req) if isinstance(amount, Mantissa) else req
    if amount >= req:
        container.pack_forget()
        frame.grid_forget()
        canvas.grid_forget()
        scrollbar.grid_forget()
        x_scrollbar.grid_forget()
        container, canvas, frame, scrollbar, x_scrollbar = tkinter_frames.create_scrollable_area(root, buttons)
def float_to_mantissa(value: float) -> Mantissa:
      """Converts a float or int into a Mantissa representation."""
      if value == 0:
          return Mantissa(0, 0)
      exponent = int(math.floor(math.log10(abs(value))))
      mantissa = value / (10 ** exponent)
      return Mantissa(mantissa, exponent)

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
       if os.path.exists("savefile.json"): # If you have saved before
        with open("savefile.json", "r")  as file: # Read the file
          try:
           return deserialize(json.load(file)) # Attempt to return the data
          except json.JSONDecodeError: # If file is corrupted
             print("Savefile is corrupted, attempting to load backup if it exists...")
             if os.path.exists("backup.json"): # If you have a backup
                with open("backup.json", "r") as file: # Read the backup file
                   try:
                      return deserialize(json.load(file)) # Attempt to return backup data
                   except json.JSONDecodeError: # If corrupted
                      print("Backup file is also corrupted.")
                      return None
             else:
              print("Backup file does not exist.")
              return None
       else:
          print("You have never saved before.")
          return None # Return your empty collection
def Save(collection):
        '''Saves your data to a json file, and makes the previous file a backup'''
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
def save():
   Save(stat_increment)
   root.destroy()
def calculate_multi(unit):
    """Calculates total multiplier for a given unit, supporting Mantissa instances."""
    global stat_increment
    total = Mantissa(1, 0)  # Start as 1 in Mantissa form
    keys = list(stat_increment.keys())
    for key in keys:
      stat_list = list(stat_increment[key].keys())
      for item in stat_list:
          amount = stat_increment[key][item].get("Value")
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
    total *= 2 if random.randint(1,500) == 1 and not isinstance(total,Mantissa) else float_to_mantissa(2) if random.randint(1,500) == 1 and isinstance(total, Mantissa) else 1 if not isinstance(total, Mantissa) else Mantissa(1,0)
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

    # Compute approximate float multiplier
    approx_multiplier = multiplier_m.to_float() if hasattr(multiplier_m, "to_float") else float(multiplier_m)

    # Compute delay and speed ratio
    base_delay = 250
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
    if isinstance(stat_increment["Main"]["Cash"]["Value"], Mantissa):
       cash_scaling = float_to_mantissa(cash_scaling) if not isinstance(cash_scaling, Mantissa) else cash_scaling
    cash_increment = Mantissa(1, 0) * multi * cash_scaling
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
    cash_l.config(text=f"Cash: {display_val}")

    # Schedule next increment
    root.after(delay, cash_increase)
def gem_increase():
    global stat_increment
    stat_increment["Main"]["Gems"]["Value"] += 1
    root.after(60000, gem_increase)
def cost_button(key, unit, cost, unit_2, receive):
    global cash_l, multi_l, stat_increment

    value = stat_increment[key][unit]["Value"]

    if isinstance(value, Mantissa) and not isinstance(cost, Mantissa):
        cost = float_to_mantissa(cost)

    # Check if the player can afford it
    if value >= cost:
        # Deduct cost
        stat_increment[key][unit]["Value"] -= cost

        # Calculate the increment (reward)
        Multi = calculate_multi(unit_2)
        if isinstance(Multi, Mantissa):
             receive = float_to_mantissa(receive)
        increment = Multi*receive
        # Add the increment
        if not isinstance(stat_increment[key][unit_2]["Value"], Mantissa):
            increment = increment.to_float()
        stat_increment[key][unit_2]["Value"] += increment

        # Update labels
        cash_val = stat_increment["Main"]["Cash"]["Value"]
        cash_text = cash_val.to_string() if isinstance(cash_val, Mantissa) else cash_val
        cash_l.config(text=f"Cash: {cash_text}")

        multi_val = stat_increment["Main"]["Multiplier"]["Value"]
        multi_text = multi_val.to_string() if isinstance(multi_val, Mantissa) else multi_val
        multi_l.config(text=f"Multiplier: {multi_text}")

        # Increment button presses (safe for Mantissa or float)
        bp_val = stat_increment["Extra"]["Buttons Pressed"]["Value"]
        stat_increment["Extra"]["Buttons Pressed"]["Value"] += 1

def reset_button(key, cost, unit, reward, unit_2):
    global cash_l, multi_l, re_l, stone_l, stat_increment

    cost_m = float_to_mantissa(cost)

    current_value = stat_increment[key][unit]['Value']
    if isinstance(current_value, Mantissa):
        current_number = current_value.to_float()
    else:
        current_number = current_value
    stat_list = list(stat_increment[key].keys())
    if current_number >= cost:
        # Reset all lower-tier stats before unit_2
        for i in range(stat_list.index(unit_2)):
            stat_increment[key][stat_list[i]]["Value"] = Mantissa(0, 0) if isinstance(stat_increment[key][stat_list[i]]["Value"], Mantissa) else 0

        multi = calculate_multi(unit_2)
        if multi.exp < math.log(MANTISSA_THRESHOLD,10):
            multi = multi.to_float()-1
            if multi * reward < reward:
                multi += 1
            multi = float_to_mantissa(multi)
        reward_m = float_to_mantissa(reward) * multi

        if not isinstance(reward_m, Mantissa):
            reward_m = float_to_mantissa(reward_m)

        if isinstance(stat_increment[key][unit_2]["Value"], Mantissa):
            stat_increment[key][unit_2]["Value"] += reward_m
        else:
            stat_increment[key][unit_2]["Value"] += reward_m.to_float()

        # Update labels
        cash_l.config(text=f"Cash: {stat_increment['Main']['Cash']['Value']}")
        multi_l.config(text=f"Multiplier: {stat_increment['Main']['Multiplier']['Value']}")
        re_l.config(text=f"Rebirths: {stat_increment['Main']['Rebirths']['Value']}")
        stat_increment["Extra"]["Buttons Pressed"]["Value"] += 1

def recovery_button_set(key, req, unit, Set, unit_2):
    global stat_increment

    amount = stat_increment[key][unit]["Value"]
    if amount >= req:
        if stat_increment[key][unit_2]["Value"] < Set:
          stat_increment[key][unit_2]["Value"] = Set
    else:
     pass
def recovery_button_fetch(key, req, unit, recovery, unit_2):
    global stat_increment
    amount = stat_increment[key][unit]["Value"]
    if amount >= req:
      multi = calculate_multi(unit_2)
      multi = multi.to_float() if isinstance(multi, Mantissa) else multi
      if multi == 0:
          multi = 1
      stat_increment[key][unit_2]["Value"] += recovery*multi
      cash_l.config(text=f"Cash: {stat_increment[key]['Cash']['Value']}")
      multi_l.config(text=f"Multiplier: {stat_increment[key]['Multiplier']['Value']}")
      re_l.config(text=f"Rebirths: {stat_increment[key]['Rebirths']['Value']}")
    else:
     pass
root = Tk()
cash_l = Label(root)
multi_l = Label(root)
re_l = Label(root)
stone_l = Label(root)
stat_increment = {"Main": {"Cash": {"Value": 0, "Multis": None}, "Multiplier":  {"Value": 0, "Multis": None}, "Rebirths":  {"Value": 0, "Multis": {"Multiplier": 2}}, "Stone": {"Value": 0, "Multis": {"Cash": 1.5, "Rebirths": 2}}, "White Gems": {"Value": 0, "Multis": {"Multiplier": 1.5, "Stone": 1.8}}, "Crystal": {"Value": 0, "Multis": {"Cash": 2, "White Gems": 3}}, "Iron": {"Value": 0, "Multis": {"Rebirths": 1.5, "Crystal": 2}}, "Gold": {"Value": 0, "Multis": {"Cash": 2, "Stone": 2, "Iron": 2}}, "Quartz": {"Value": 0, "Multis": {"Multiplier": 10, "Rebirths": 2, "Stone": 5, "White Gems": 3, "Crystal": 2, "Gold": 2}}, "Jade": {"Value": 0, "Multis": {"Cash": 3, "Rebirths": 10, "Stone": 4, "Crystal": 4, "Quartz": 3}}, "Obsidian": {"Value": 0, "Multis": {"Rebirths": 15, "Stone": 15,"White Gems": 15, "Crystal": 10, "Iron": 10, "Gold": 7.5, "Jade": 5}}, "Ruby": {"Value": 0, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2}}, "Emerald": {"Value": 0, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2}}, "Sapphire": {"Value": 0, "Multis": {"Cash": 2, "Multiplier": 2, "Rebirths": 2, "Stone": 2, "White Gems": 2, "Crystal": 2, "Iron": 2, "Gold": 2, "Quartz": 2, "Jade": 2, "Obsidian": 2, "Ruby": 2, "Emerald": 2}}, "Diamond": {"Value": 0, "Multis": {"Emerald": 3, "Sapphire": 2}}, "Starlight": {"Value": 0, "Multis": {"Ruby": 6, "Sapphire": 3, "Diamond": 3}}, "Ion": {"Value": 0, "Multis": {"Jade": 4, "Ruby": 2, "Emerald": 10, "Sapphire": 1.4, "Diamond": 5, "Starlight": 5}}, "Uranium": {"Value": 0, "Multis": {"Crystal": 100, "Sapphire": 60, "Starlight": 5, "Ion": 2.2}}, "Bismuth": {"Value": 0, "Multis": {"Ruby": 50, "Emerald": 25, "Sapphire": 12, "Diamond": 3, "Ion": 2.5, "Uranium": 2}} , "Boracite": {"Value": 0, "Multis": {"Starlight": 5, "Uranium": 3, "Bismuth": 1.5}}, "Nissonite": {"Value": 0, "Multis": {"Obsidian": 5, "Bismuth": 2.75, "Boracite": 2.25}}, "Orpiment": {"Value": 0, "Multis": {"Cash": 23, "Multiplier": 22, "Rebirths": 21, "Stone": 20, "White Gems": 19, "Crystal": 18, "Iron": 17, "Gold": 16, "Quartz": 15, "Jade": 14, "Obsidian": 13, "Ruby": 12, "Emerald": 11, "Sapphire": 10, "Diamond": 9, "Starlight": 8, "Ion": 7, "Uranium": 6, "Bismuth": 5, "Boracite": 4, "Nissonite": 3}}, "Tetra": {"Value": 0, "Multis": {"Diamond": 1e4, "Boracite": 30, "Nissonite": 10, "Orpiment": 2.5}}, "Volt": {"Value": 0, "Multis": {"Uranium": 100, "Nissonite": 4, "Tetra": 2}}, "Aquamarine": {"Value": 0, "Multis": {"Obsidian": 1e6, "Ion": 500, "Uranium": 400, "Nissonite": 5, "Volt": 2.1}}, "Lollipop": {"Value": 0, "Multis": {"Emerald": 8152, "Sapphire": 4096, "Diamond": 2048, "Starlight": 1024, "Ion": 512, "Uranium": 256, "Bismuth": 128, "Boracite": 64, "Nissonite": 32, "Orpiment": 16, "Tetra": 8, "Volt": 4, "Aquamarine": 2}}, "C0RR8PT10N": {"Value": 0, "Multis": {"Cash": 6, "Multiplier": 6, "Rebirths": 6, "Stone": 6, "White Gems": 6, "Crystal": 6, "Iron": 6, "Gold": 6, "Quartz": 6, "Jade": 6, "Obsidian": 6, "Ruby": 6, "Emerald": 6, "Sapphire": 6, "Diamond": 6, "Starlight": 6, "Ion": 6, "Uranium": 6, "Bismuth": 6, "Boracite": 6, "Nissonite": 6, "Orpiment": 2.3, "Tetra": 6, "Volt": 6, "Aquamarine": 4, "Lollipop": 3}}, "Stargazed Metal": {"Value": 0, "Multis": {"Cash": 1e100, "Multiplier": 1e100, "Rebirths": 1e100, "Stone": 1e100, "White Gems": 1e100, "Crystal": 1e100, "Iron": 1e100, "Gold": 1e100, "Quartz": 1e100, "Jade": 1e100, "Obsidian": 7.5, "Ruby": 7.5, "Emerald": 7.5, "Aquamarine": 2.25, "Lollipop": 2.25, "C0RR8PT10N": 3}}, "Gyge": {"Value": 0, "Multis": {"Ruby": 1e25, "Emerald": 1e25, "Sapphire": 1e25, "Diamond": 1e25, "Starlight": 1e25, "Ion": 1e25, "Uranium": 1e25, "Bismuth": 1e25, "Boracite": 1e25, "Nissonite": 1e25, "Volt": 18, "Lollipop": 7, "C0RR8PT10N": 10, "Stargazed Metal": 2}}, "Auly Plate": {"Value": 0, "Multis": {"Cash": Mantissa(1,288290), "Orpiment": 1.61, "Tetra": 3.12, "Volt": 6.25, "Aquamarine": 12.5, "Lollipop": 18, "C0RR8PT10N": 50, "Stargazed Metal": 5, "Gyge": 2}}, "Shell Piece": {"Value": 0, "Multis": {"Cash": 1e75, "Multiplier": 1e75, "Rebirths": 1e75, "Stone": 1e75, "White Gems": 1e75, "Crystal": 1e75, "Iron": 1e75, "Gold": 1e75, "Quartz": 1e75, "Jade": 1e75, "Obsidian": 1e75, "Ruby": 1e75, "Emerald": 1e75, "Sapphire": 1e75, "Diamond": 1e75, "Starlight": 1e75, "Ion": 1e75, "Uranium": 1e75, "Bismuth": 1e75, "Boracite": 1e75, "Nissonite": 1e75, "Orpiment": 1e75, "Tetra": 100, "Volt": 100, "Aquamarine": 100, "Lollipop": 100, "C0RR8PT10N": 100, "Mint": 100, "Gems": 20, "Metal": 100, "Press": 100, "Microparticles": 100, "Star": 100, "Robot": 100, "Prototype": 100}}, "Singularity": {"Value": 0, "Multis": {"Cash": Mantissa(1,987654321), "Volt": 1200, "C0RR8PT10N": 150, "Gyge": 4, "Auly Plate": 2.5, "Gems": 75}}, "Capsuled Singularity": {"Value": 0, "Multis": {"Cash": Mantissa(1,303030303), "Ruby": Mantissa(1,266664), "Emerald": Mantissa(1,266664), "Sapphire": Mantissa(1,266664), "Diamond": Mantissa(1,266664), "Starlight": Mantissa(1,133337), "Ion": Mantissa(1,666666), "Uranium": Mantissa(1,333333), "Bismuth": Mantissa(1,12555), "Boracite": Mantissa(1,5555), "Nissonite": Mantissa(1,2222), "Orpiment": Mantissa(1,1000), "Tetra": Mantissa(1,500), "Volt": 1e150, "Aquamarine": 1e75, "Lollipop": 1e25, "C0RR8PT10N": 1e6, "Stargazed Metal": 2500, "Gyge": 500, "Auly Plate": 25, "Shell Piece": 2.5, "Prototype": 1240, "Gems": 300}}, "Gems": {"Value": 0, "Multis": None}}, "Extra": {"Buttons Pressed": {"Value": 0, "Multis": None}, "Geodes Opened": {"Value": 0, "Multis": None}}, "Geode": {}} # Gems technically aren't part of main progression, they're just placed here for temporary convenience
stat_list = list(stat_increment["Main"].keys())
root.title("BS:ED but bad")
root.configure(bg="black")
root.config(width=1000,height=1000)
root.minsize(100,100)
root.maxsize(5000,5000)
root.geometry("500x500+20+120")
photo = PhotoImage(file="Quant.png")
root.wm_iconphoto(False, photo) 
Nb = ttk.Notebook(root, cursor="circle") # Insert notebook and change cursor
s = ttk.Style()
s.configure('TFrame', background="black") #Change Style() to create bgs for frames
temp = Load()
if temp != None:
   stat_increment = temp
root.protocol("WM_DELETE_WINDOW", save)
cash = stat_increment['Main']['Cash']['Value']
c_msg = cash if not isinstance(cash, Mantissa) else cash.to_string()
cash_l.config(text=f"Cash: {c_msg}", bg="black", fg="white")
cash_l.pack()
multi = stat_increment['Main']['Multiplier']['Value']
m_msg = multi if not isinstance(multi, Mantissa) else multi.to_string()
multi_l.config(text=f"Multiplier: {m_msg}", bg="black", fg="white")
multi_l.pack()
re_l.config(text=f"Rebirths: {stat_increment['Main']['Rebirths']['Value']}", bg="black", fg="white")
re_l.pack()
stone_geode = Geode({"Multiplier": {"Chance": 3},
                     "Rebirths": {"Chance": 10},
                     "Stone": {"Chance": 20},
                     #"Mint": 33,
                     "White Gems": {"Chance": 333},
                     "Dezyp": {"Chance": 12000, "Multis": {"Cash": 15, "Rebirths": 20, "Stone": 2, "White Gems": 2}},
                     "Podrillium": {"Chance": 1000000000, "Multis": {"C0RR8PT10N": Mantissa(1,3003)}}}, 1e6, "Stone") #Podrillium is real guys!!! Trust!!!
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
       ("Stone Geode: 1M Stone", lambda: Geode_roll(stone_geode, luck)),
       ("White Gems Geode: 30 White Gems", lambda: Geode_roll(gems_geode, luck))
    ],
    "Area Teleports": [
       ("Caves (req: 10 Stone)", lambda: load_check("Main",10, "Stone", Cave_Buttons)),
       ("Crystal Beneaths (req: 300 White Gems)", lambda: load_check("Main",300, "White Gems", Crystal_Buttons)),
       ("Iron Shafts (req: 100 Crystal)", lambda: load_check("Main",100, "Crystal", Iron_Buttons)),
       ("Golden Quarry (req: 750 Iron)", lambda: load_check("Main",750,"Iron",Gold_Buttons)),
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
        ("3 Ion: 1 Starlight (Sets)", lambda: recovery_button_fetch("Main",3, "Ion", 1, "Starlight")),
    ],
    "Uranium Wastelands": [
        ("100 Ion: 1e2000 Multiplier (Fetch)", lambda: recovery_button_fetch("Main",100, "Ion", Mantissa(1,2000), "Multiplier")),
        ("1T Gems: 1e45 Obsidian (Sets)", lambda: recovery_button_set("Main",1e12, "Gems", 1e45, "Obsidian")),
        ("1M Starlight: 1No Sapphire (Sets)", lambda: recovery_button_set("Main",1e6, "Starlight", 1e30, "Sapphire")),
        ("1 Uranium: 25 Diamond (Sets)", lambda: recovery_button_set("Main",1, "Uranium", 25, "Diamond")),
        ("3 Uranium: 1 Ion (Sets))", lambda: recovery_button_set("Main",3, "Uranium", 1, "Ion")),
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
        ("Golden Quarry (req: 750 Iron)", lambda: load_check("Main",750,"Iron",Gold_Buttons))
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
        ("Crystal Geode: 100 Crystal", lambda: Geode_roll(crystal_geode, luck))
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
        ("Iron Geode: 25 Iron", lambda: Geode_roll(iron_geode, luck)),
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
    "Area Teleports": [
       ("Spawn (req: 0 Cash)", lambda: load_check("Main",0, "Cash", Spawn_Buttons)),
       ("Recover Hall (req: 0 Cash)", lambda: load_check("Main",0, "Cash", Recover_Hall_Buttons))
    ]
}
def open_stat_menu():
    global stat_increment, root

    # If the window already exists, bring it to front
    if hasattr(open_stat_menu, "window") and open_stat_menu.window.winfo_exists():
        open_stat_menu.window.lift()
        return

    stat_window = Toplevel(root)
    open_stat_menu.window = stat_window
    stat_window.title("Stats Menu")
    stat_window.configure(bg="black")
    stat_window.geometry("300x400")
    photo = PhotoImage(file="Quant.png")
    stat_window.wm_iconphoto(False, photo)

    # Scrollbar setup
    canvas = Canvas(stat_window, bg="black")
    scrollbar = Scrollbar(stat_window, orient="vertical", command=canvas.yview)
    scroll_frame = Frame(canvas, bg="black")

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Header labels
    Label(scroll_frame, text="Stat", bg="black", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=5)
    Label(scroll_frame, text="Value", bg="black", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=10, pady=5)

    # Dynamic stat labels
    stat_labels = {}  # { (category, stat): label }
    current_row = 1

    for category, stats in stat_increment.items():
        # Category label
        Label(scroll_frame, text=category, bg="black", fg="white", font=("Arial", 10, "bold")).grid(
            row=current_row, column=0, columnspan=2, sticky="w", pady=(10, 2)
        )
        current_row += 1

        for stat_name, stat_data in stats.items():
            Label(scroll_frame, text=stat_name, bg="black", fg="white").grid(
                row=current_row, column=0, padx=10, pady=2, sticky="w"
            )

            value = stat_data["Value"]
            if isinstance(value, Mantissa):
                value_str = value.to_string()
            else:
                value_str = str(round(value, 6)) if isinstance(value, (int, float)) else str(value)

            lbl = Label(scroll_frame, text=value_str, bg="black", fg="white")
            lbl.grid(row=current_row, column=1, padx=10, pady=2, sticky="e")

            stat_labels[(category, stat_name)] = lbl
            current_row += 1

    # Update function
    def update_labels():
        for (category, stat_name), lbl in stat_labels.items():
            try:
                value = stat_increment[category][stat_name]["Value"]
                if isinstance(value, Mantissa):
                    value_str = value.to_string()
                else:
                    value_str = str(round(value, 6)) if isinstance(value, (int, float)) else str(value)
                lbl.config(text=value_str)
            except KeyError:
                lbl.config(text="N/A")  # fallback if stat is removed dynamically
        stat_window.after(25, update_labels)  # update every 0.25s for efficiency

    update_labels()


Button(text="Open Stat Menu", bg="black", fg="white", command= lambda: open_stat_menu()).pack()
container, canvas, frame, scrollbar, x_scrollbar = tkinter_frames.create_scrollable_area(root, Spawn_Buttons)
def play_music():
    '''This constantly loops background music'''
    # Export to raw data
    while True:
      song = AudioSegment.from_mp3("Catswing.mp3")
      playback = sa.play_buffer( #I'm not going to act like I understand what these are used for
            song.raw_data,
            num_channels=song.channels,
            bytes_per_sample=song.sample_width,
            sample_rate=song.frame_rate
        )
      playback.wait_done() # This waits until the song is finished before continuing

# Run in a thread
threading.Thread(target=play_music, daemon=True).start()
cash_increase()
gem_increase()
root.mainloop()