from tkinter import *
from tkinter import ttk
import random
#import simpleaudio as sa
import json
#from pydub import AudioSegment
import time
import datetime
import threading
import math
def cash_increase():
    global stat_increment, cash_l
    multi = 1
    if stat_increment["Multiplier"] == 0:
       stat_increment["Multiplier"] = 1
    if stat_increment["Multiplier"] > 100:
       multi = (stat_increment["Multiplier"]-100)//10
    stat_increment["Cash"] += 1 * multi
    cash_l.config(text=f"Cash: {stat_increment['Cash']}")
    root.after(int(math.ceil(float(100 / stat_increment["Multiplier"]))), cash_increase)
def multi_button(cost, multi):
   global cash_l, multi_l, stat_increment
   stat_multi = 1
   if stat_increment["Rebirths"] > 0:
      stat_multi = stat_increment["Rebirths"]*2
   if stat_increment["Cash"] > cost:
     stat_increment["Cash"] -= cost
     stat_increment["Multiplier"] += multi*stat_multi
     cash_l.config(text=f"Cash: {stat_increment['Cash']}")
     multi_l.config(text=f"Multiplier: {stat_increment['Multiplier']-1}")
   else:
      pass
def reset_button(cost, unit, reward):
   global cash_l, multi_l, re_l
   if unit > cost:
      stat_increment["Multiplier"] = 0
      stat_increment["Cash"] = 0
      stat_increment["Rebirths"] += reward
      cash_l.config(text=f"Cash: {stat_increment['Cash']}")
      multi_l.config(text=f"Multiplier: {stat_increment['Multiplier']-1}")
      re_l.config(text=f"Rebirths: {stat_increment['Rebirths']}")
   else:
      pass
stat_increment = {"Cash": 0, "Multiplier": 0, "Rebirths": 0, "Stone": 0, "White Gems": 0, "Crystal": 0, "Iron": 0, "Gold": 0, "Quartz": 0, "Jade": 0, "Obsidian": 0, "Ruby": 0, "Emerald": 0, "Sapphire": 0, "Diamond": 0, "Starlight": 0, "Ion": 0, "Uranium": 0, "Bismuth": 0 , "Boracite": 0, "Nissonite": 0, "Orpiment": 0, "Tetra": 0, "Volt": 0, "Aquamarine": 0, "Lollipop": 0, "C0RR8PT10N": 0, "Stargrazed Metal": 0, "Gyge": 0, "Auly Plate": 0, "Shell Piece": 0, "Singularity": 0, "Capsuled Singularity": 0}
stat_list = list(stat_increment.keys())
root = Tk()
root.title("BS:ED but bad")
root.configure(bg="black")
root.config(width=1000,height=1000)
root.minsize(100,100)
root.maxsize(5000,5000)
root.geometry("500x500+20+120")
photo = PhotoImage(file="Program/Quant.png")
root.wm_iconphoto(False, photo) 
Nb = ttk.Notebook(root, cursor="circle") # Insert notebook and change cursor
s = ttk.Style()
s.configure('TFrame', background="black") #Change Style() to create bgs for frames
cash_l = Label(root, text=f"Cash: {stat_increment['Cash']}", bg="black", fg="white")
cash_l.pack()
multi_l = Label(root, text=f"Multiplier: {stat_increment['Multiplier']-1}", bg="black", fg="white")
multi_l.pack()
re_l = Label(root, text=f"Rebirths: {stat_increment['Rebirths']}", bg="black", fg="white")
re_l.pack()
Button(root, text="10 Cash: 1 Multiplier", bg="black", fg="white", command=lambda: multi_button(10,1)).pack()
Button(root, text="1000 Cash: 10 Multiplier", bg="black", fg="white", command=lambda: multi_button(1000,10)).pack()
Button(root, text="100 Multiplier: 1 Rebirths", bg="black", fg="white", command=lambda: reset_button(100,stat_increment["Multiplier"],1)).pack()
Button(root, text="5000 Multiplier: 5 Rebirths", bg="black", fg="white", command=lambda: reset_button(5000,stat_increment["Multiplier"],5)).pack()
cash_increase()
root.mainloop()