from tkinter import *
class Mantissa:
    def __init__(self, mantissa, exponent):
        self.num = mantissa
        self.exp = exponent
    def __mul__(a, b):
      # a and b are (mantissa, exponent) tuples
      new_mantissa = a.num * b.num
      new_exponent = a.exp + b.exp
      
      # Normalize if mantissa >= 10
      while new_mantissa >= 10:
          new_mantissa /= 10
          new_exponent += 1
      return Mantissa(new_mantissa, new_exponent)
    def __add__(a, b):
      # Ensure a has the bigger exponent
      if a.exp < b.exp:
          a, b = b, a  # swap references, do not mutate
  
      diff = a.exp - b.exp
      if diff > 300:  # treat b as negligible
          return Mantissa(a.num, a.exp)
  
      # Safe addition for reasonably close exponents
      new_mantissa = a.num + b.num * 10**-diff
      while new_mantissa >= 10:
        new_mantissa /= 10
        a.exp += 1
      return Mantissa(new_mantissa, a.exp)
    def __round__(self, num):
        return self
    def __ge__(self, other):
        return True if self.exp > other.exp else False
    def __sub__(a,b):
        b.num = -b.num
        return a + b
    def __truediv__(a,b):
        mantissa = a.num/b.num
        exp = a.exp-b.exp
        while mantissa <= 1:
            mantissa*= 10
            exp -= 1
        return Mantissa(mantissa, exp)
    def to_string(self):
       return f"{self.num:.3f}e{self.exp}"
    def to_dict(self):
        return {"__mantissa__": True, "number": self.num, "exponent": self.exp}

    @classmethod
    def from_dict(cls, data):
        return cls(data["number"], data["exponent"])
    def to_float(self):
        """Convert the Mantissa to a regular float. Warning: may overflow for huge exponents."""
        return self.num * (10 ** self.exp) if self.exp < 300 else self

class tkinter_frames:
  def create_scrollable_area(parent, button_groups, bg="black", text_color="white"):
    """
    Creates a scrollable frame with grouped buttons arranged in columns.

    Returns (container, canvas, scrollable_frame, v_scrollbar, h_scrollbar)
    """
    # Container that holds canvas + scrollbars
    container = Frame(parent, bg=bg)
    container.pack(fill="both", expand=True)

    # Canvas and scrollbars
    canvas = Canvas(container, bg=bg, highlightthickness=0)
    v_scroll = Scrollbar(container, orient="vertical", command=canvas.yview)
    h_scroll = Scrollbar(container, orient="horizontal", command=canvas.xview)

    # Frame that will hold the actual content
    scrollable_frame = Frame(canvas, bg=bg)

    # Add the frame into the canvas once and keep its id
    window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Configure canvas scrolling
    canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

    # Grid layout for the container so scrollbars sit correctly
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    canvas.grid(row=0, column=0, sticky="nsew")
    v_scroll.grid(row=0, column=1, sticky="ns")
    h_scroll.grid(row=1, column=0, sticky="ew")

    # When the content frame changes size, update scrollregion
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

        # If content is narrower than canvas, stretch it to avoid awkward left alignment
        content_req_w = scrollable_frame.winfo_reqwidth()
        canvas_w = canvas.winfo_width()
        if content_req_w < canvas_w:
            canvas.itemconfig(window_id, width=canvas_w)
        else:
            # allow the frame to keep its requested width so horizontal scroll can appear
            canvas.itemconfig(window_id, width=content_req_w)

    scrollable_frame.bind("<Configure>", on_frame_configure)

    # When the canvas is resized (window resized), optionally update child width
    def on_canvas_configure(event):
        # If content narrower than canvas, make child match canvas to fill horizontally
        content_req_w = scrollable_frame.winfo_reqwidth()
        if content_req_w < event.width:
            canvas.itemconfig(window_id, width=event.width)
        # otherwise leave the child width alone (so scrollregion and horizontal scrollbar are driven by child size)
    canvas.bind("<Configure>", on_canvas_configure)

    # Populate content (columns)
    for col_index, (group_name, buttons) in enumerate(button_groups.items()):
        Label(scrollable_frame, text=group_name, bg=bg, fg=text_color,
              font=("Arial", 12, "bold")).grid(row=0, column=col_index, pady=(10, 5))
        for row_index, (text, command) in enumerate(buttons, start=1):
            Button(scrollable_frame, text=text, bg=bg, fg=text_color,
                   command=command, width=40).grid(
                row=row_index, column=col_index, padx=5, pady=5, sticky="n"
            )

    return container, canvas, scrollable_frame, v_scroll, h_scroll
  
import random

class Geode:
    def __init__(self, items, cost, unit):
        """
        items: dict -> { "ItemName": rarity_weight }
        Lower weight = rarer item
        cost: Mantissa or float, automatically converted unless exponent >= 300
        unit: key in save file currency dictionary (e.g. "Gems", "Crystals")
        """
        self.items = items
        self.cost = cost.to_float() if isinstance(cost, Mantissa) and cost.exp < 300 else cost
        self.unit = unit

    def open(self, file, luck=1.0):
      luck += (random.randint(100, 777) / 100) - 1
  
      if file["Main"][self.unit]["Value"] < self.cost:
          return file
      file["Main"][self.unit]["Value"] -= self.cost
  
      adjusted_items = {}
  
      # Adjust weights with luck (only common items)
      for item, data in self.items.items():
          weight = data["Chance"]
          if weight >= 10001:
              weight /= luck
          adjusted_items[item] = max(weight, 1e-6)
  
      # Normalize total sum to original
      Total = sum(v["Chance"] for v in self.items.values())
      new_total = sum(adjusted_items.values())
      scale = Total / new_total
      for item in adjusted_items:
          adjusted_items[item] *= scale
  
      # Convert to probabilities (inverse weighting)
      total = sum(1 / w for w in adjusted_items.values())
      probabilities = [1 / w / total for w in adjusted_items.values()]
  
      # Roll item
      item = random.choices(list(adjusted_items.keys()), weights=probabilities, k=1)[0]
      print(item)
      # Add item to inventory
      if file["Main"].get(item) is not None:
          file["Main"][item]["Value"] += 2 if random.randint(1,500) == 1 else 1
      elif file["Geode"].get(item) is not None:
          file["Geode"][item]["Value"] += 2 if random.randint(1,500) == 1 else 1
      else:
          file["Geode"][item] = {"Multis": self.items[item]["Multis"], "Value": 1}
      file["Extra"]["Geodes Opened"]["Value"] += 1
      return file




