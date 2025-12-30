import pyautogui
import time

# -------- SETTINGS --------
point_a = (953, 120)   # (x, y)
point_b = (1023, 800)   # (x, y)

move_time = 1        # seconds to move between points
pause_between = 0   # seconds to wait between moves
# --------------------------

# Give yourself a moment to switch windows
time.sleep(5)

# Move to Point A smoothly
while True:
  pyautogui.moveTo(point_a[0], point_a[1], duration=move_time)

  time.sleep(pause_between)

# Move to Point B smoothly
  pyautogui.moveTo(point_b[0], point_b[1], duration=move_time)
