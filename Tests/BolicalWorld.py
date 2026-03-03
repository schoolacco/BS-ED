import sys
import numpy as np
import re
import random
from functools import partial
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
np.seterr(all="ignore")
stylesheet = open("Tests/graphite.qss", "r")
stylesheet = stylesheet.read()
# ---------- CONFIG ----------

TOLERANCE = 0.01  # Allowed error for match check
MODE_NORMAL = "normal"
MODE_SKY_HIGH = "sky_high"

# ---------- UTILITY: preprocess input ----------
def preprocess_for_eval(expr: str) -> str:
    expr = expr.replace(" ", "")
    expr = expr.replace("^", "**")
    #while "|" in expr:
    #    expr = re.sub(r"\|([^|]+)\|", r"abs(\1)", expr)
    funcs = "|".join(["sin","cos","tan","abs","pi","sinh","cosh","tanh","e", "sqrt", "exp"])
    expr = re.sub(rf"(\d+(\.\d+)?)(?=(x|\(|{funcs})\b)", r"\1*", expr)
    expr = re.sub(r"([x)])(\d+(\.\d+)?)", r"\1*\2", expr)
    expr = re.sub(rf"([x)])(?=({funcs})\()", r"\1*", expr)
    expr = re.sub(r"\)\(", r")*(", expr)
    return expr
def break_asymptotes(y, threshold=10):
    y = y.astype(float).copy()

    # Break on non-finite values
    y[~np.isfinite(y)] = np.nan

    # Detect large jumps between consecutive points
    dy = np.abs(np.diff(y))

    # Insert NaNs AFTER large jumps
    jump_indices = np.where(dy > threshold)[0] + 1
    y[jump_indices] = np.nan

    return y

# ---------- SAFE EVAL ENV ----------
SAFE_ENV = {
    "sin": np.sin, "cos": np.cos, "tan": np.tan,
    "abs": np.abs, "pi": np.pi,
    "sinh": np.sinh, "cosh": np.cosh, "tanh": np.tanh,
    "e": np.e, "sqrt": np.sqrt, "exp": np.exp, "ln": np.log,
    "arcsin": np.arcsin, "arccos": np.arccos, "arctan": np.arctan,
    "arcsinh": np.arcsinh, "arccosh": np.arccosh, "arctanh": np.arctanh
}

def eval_expr(expr, x):
    expr = preprocess_for_eval(expr)
    env = SAFE_ENV.copy()
    env["x"] = x
    return eval(expr, {"__builtins__": {}}, env)

# ---------- RANDOM EQUATION GENERATOR ----------
LINEAR_FUNCS = ["linear"]
POLYNOMIAL_FUNCS = ["quadratic","cubic","quartic"]
HYPERBOLAS = ["1/x","1/x^2","1/(x+a)^2"]
TRIG_FUNCS = ["sin","cos","tan"]
HYPERBOLIC_FUNCS = ["sinh","cosh","tanh"]
OTHER_FUNCS = ["abs","sqrt","exp", "ln", "arcsin", "arccos", "arctan", "arcsinh", "arccosh", "arctanh"]

def random_constant(low=-5, high=5, allow_float=True):
    constant = 0
    while constant == 0:
      constant =  round(random.uniform(low, high), 1) if allow_float else random.randint(low, high)
    return constant

def generate_linear():
    a = random.randint(-10,10)
    b = random.randint(-10,10)
    return f"{a}*x + {b}"

def generate_polynomial():
    degree = random.randint(2,4)
    factors = [f"(x - {random.randint(-5,5)})" for _ in range(degree)]
    a = random.choice([-3,-2,-1,1,2,3])
    return f"{a}*{'*'.join(factors)}"

def generate_hyperbola(chain=True):
    eq = "x"
    for _ in range(random.randint(1,2) if chain else 1):
        shift = random.choice([-1,1,2])
        power = random.choice([1,2])
        eq = f"1/({eq}+{shift})**{power}"
    return eq

def generate_trig(chained=False):
    func = random.choice(TRIG_FUNCS)
    a = random.choice([-2,-1,1,2])
    freq = random.randint(1,3)
    shift = random.choice([-2,-1,1,2])
    inner = "x"
    if chained:
        inner = f"{random.choice([lambda: f'x**{random.randint(2,4)}', lambda: generate_hyperbola(chain=True), lambda: generate_trig(chained=True)])()}"  # can chain with simple expressions
    return f"{a}*{func}({freq}*{inner} + {shift})"

def generate_hyper_trig(chained=False):
    func = random.choice(HYPERBOLIC_FUNCS)
    a = random.choice([-2,-1,0,1,2])
    freq = random.randint(1,3)
    shift = random.choice([-2,-1,1,2])
    inner = "x"
    if chained:
        inner = f"{random.choice([lambda: f'x**{random.randint(2,4)}',lambda: f'x{random.randint(-10,10)}', lambda: generate_trig(chained=True), lambda: generate_hyper_trig(chained=True), lambda: generate_hyperbola(chain=True)])()}"
    return f"{a}*{func}({freq}*{inner} + {shift})"

def generate_other_func(chained=False):
    func = random.choice(OTHER_FUNCS)
    a = random_constant(-2,2)
    inside = f"x + {random_constant(-2,2)}"
    if chained:
        inside = f"{random.choice([lambda:generate_trig(chained=True), lambda:generate_hyper_trig(chained=True), lambda: f'x**{random.randint(2,10)}', lambda: generate_hyperbola(chain=True), lambda:generate_other_func(chained=True)])()}"
    return f"{a}*{func}({inside})"

def generate_level_equation(level:int, bonus=False):
    """
    Generates an equation according to the rules for levels 1-10.
    If bonus=True, derivative/integral mode (handled outside).
    """
    terms = []

    if level == 1:
        # Linear only
        return generate_linear()
    elif level == 2:
        # Quadratics–quartics
        return generate_polynomial()
    elif level == 3:
        # Hyperbolas, can chain but no addition
        return generate_hyperbola(chain=True)
    elif level == 4:
        # Trig & hyperbolic trig, addition allowed, no chaining
        for _ in range(random.randint(2,4)):
            terms.append(random.choice([generate_trig, generate_hyper_trig])(chained=False))
        return " + ".join(terms)
    elif level == 5:
        # Linear + trig/hyperbolic trig, addition + chaining allowed
        linear = generate_linear()
        trig_term = random.choice([generate_trig, generate_hyper_trig])(chained=True)
        return f"{linear} + {trig_term}"
    elif level == 6:
        # Trig/hyperbolic + powers + hyperbolas, chaining allowed, no linear or addition
        choices = [lambda: generate_trig(chained=True), lambda: generate_hyper_trig(chained=True), lambda: generate_hyperbola(chain=True)]
        return random.choice(choices)()
    elif level == 7:
        # Chaining of all prior content, no addition
        choices = [lambda: generate_hyperbola(chain=True),
                   lambda: generate_trig(chained=True),
                   lambda: generate_hyper_trig(chained=True)]
        return random.choice(choices)()
    elif level == 8:
        # Level 7 + other functions, chaining allowed
        choices = [lambda: generate_other_func(chained=True)]
        return random.choice(choices)()
    elif level == 9:
        # Addition of functions, no chaining
        for _ in range(random.randint(4,8)):
            choices = [generate_linear, generate_polynomial,
                       lambda: generate_trig(chained=False),
                       lambda: generate_hyper_trig(chained=False),
                       generate_hyperbola, lambda: generate_other_func(chained=False)]
            terms.append(random.choice(choices)())
        return " + ".join(terms)
    elif level == 10:
        # Addition of chained + unchained functions
        for _ in range(random.randint(8,15)):
            choices = [generate_linear, generate_polynomial, generate_hyperbola,
                       lambda: generate_trig(chained=True),
                       lambda: generate_hyper_trig(chained=True),
                       lambda: generate_other_func(chained=True)]
            terms.append(random.choice(choices)())
        return " + ".join(terms)
    else:
        return generate_linear()  # fallback

# ---------- NUMERIC MATCH CHECK ----------
def check_match_numeric(target_expr, player_expr, x, tol=TOLERANCE):
    try:
        y_target = np.array(eval_expr(target_expr, x), dtype=float)
        y_player = np.array(eval_expr(player_expr, x), dtype=float)
        y_target[~np.isfinite(y_target)] = np.nan
        y_player[~np.isfinite(y_player)] = np.nan
        error = np.nanmean(np.abs(y_target - y_player))
        return error < tol
    except Exception:
        return False
#(15/100^0.4) * x^0.4 + 0.85x
def max_gradient_percentile(x, y, percentile=95, xmin=0, xmax=100):
    mask = (x >= xmin) & (x <= xmax) & np.isfinite(y)
    if np.count_nonzero(mask) < 2:
        return np.inf

    dy_dx = np.gradient(y[mask], x[mask])
    slopes = np.abs(dy_dx)

    return np.nanpercentile(slopes, percentile)

def reaches_height(x, y, target=100, xmin=0, xmax=100):
    mask = (x >= xmin) & (x <= xmax) & np.isfinite(y)
    if not np.any(mask):
        return False
    return np.nanmax(y[mask]) >= target

def is_trivial_linear(x, y, tol=1e-3):
    finite = np.isfinite(y)
    if np.count_nonzero(finite) < 3:
        return False

    dx = np.diff(x[finite])
    dy = np.diff(y[finite])

    slopes = dy / dx
    return np.all(np.abs(slopes - 1) < tol)


def sky_high_check(x, y):
    if not np.any(np.isfinite(y)):
        return False, "Graph is empty"
    
    if is_trivial_linear(x, y):
        return False, "Trivial linear solution (y = x) is not allowed"
    
    if max_gradient_percentile(x, y) > 1.22:
        return False, "Gradient exceeded 45°"

    if not reaches_height(x, y):
        return False, "Did not reach y = 100"
    # Must touch origin
    idx = np.argmin(np.abs(x - 0))
    y_at_zero = y[idx]
    
    if not np.isfinite(y_at_zero) or abs(y_at_zero) > 1e-2:
        return False, "Graph must pass through the origin (0, 0)"

    return True, "Sky High Structuring complete, perhaps you are worthy of Esadrhium."


# ---------- GUI ----------
class GameState:
    def __init__(self, mode=MODE_NORMAL):
        self.points = 0
        self.level = 1
        self.unlocks = {"sky_high": False}
        self.mode = mode
class BolicalWorld(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setStyleSheet(stylesheet)
            self.setWindowTitle("Bolical World")
            self.resize(800,600)
            self.state = GameState()
            self.stack = QStackedWidget() # Things don't die now
            self.setCentralWidget(self.stack)
            
            self.menu = self.create_menu()
            self.guide = self.create_guide()
            self.shop = ShopPage(game_state=self.state, parent=self)
            self.difficulty_select = self.create_difficulty_select()
            self.graph = GraphPuzzle(game_state=self.state, parent=self)
            
            for page in [self.menu, self.guide, self.shop, self.difficulty_select, self.graph]:
                self.stack.addWidget(page)
            self.stack.setCurrentWidget(self.menu)
        def create_menu(self):
            page = QWidget()
            layout = QVBoxLayout(page)
            layout.setAlignment(Qt.AlignCenter)
            
            title = QLabel("Bolical World")
            title.setStyleSheet("color: #00ff88; font-size: 32px; font-weight: bold;")
            title.setAlignment(Qt.AlignCenter)
            layout.addWidget(title)
            
            play = QPushButton("Play")
            guide = QPushButton("Guide")
            shop = QPushButton("Shop")
            self.structure = QPushButton("Sky High Structuring")
            self.structure.hide()
            for btn in (play, guide, shop, self.structure):
                btn.setFixedSize(200, 50)
                layout.addWidget(btn)
            play.clicked.connect(lambda: self.stack.setCurrentWidget(self.difficulty_select))
            guide.clicked.connect(lambda: self.stack.setCurrentWidget(self.guide))
            shop.clicked.connect(lambda: self.open_shop())
            self.structure.clicked.connect(lambda: self.start_structuring())
            
            return page
        def create_guide(self):
            page = QWidget()
            layout = QVBoxLayout(page)
            
            guide = QLabel("Goal: Guess the equation of the graph. Use sin, cos, tan, etc.\nYou earn points by matching the target equation. Difficulty increases points although graphs will become exponentially harder.\nLevel 1 graphs give you 1 point\nLevel 2 graphs give you 3 points\nLevel 3 graphs give you 5 points\nLevel 4 graphs give you 10 points\nLevel 5 graphs give you 30 points\nLevel 6 graphs give you 50 points\nLevel 7 graphs give you 100 points\nLevel 8 graphs give you 500 points\nLevel 9 graphs give you 10,000 points and are not recommended\nLevel 10 graphs give you 1,000,000 points but are nearly imposssible to crack.")
            guide.setWordWrap(True)
            guide.setStyleSheet("color: #00ff88; font-size: 14px;")
            layout.addWidget(guide)
            
            back = QPushButton("Back")
            back.clicked.connect(lambda: self.stack.setCurrentWidget(self.menu))
            layout.addWidget(back)
            return page
        def create_difficulty_select(self):
            page = QWidget()
            layout = QVBoxLayout(page)
            layout.setAlignment(Qt.AlignCenter)
            
            label = QLabel("Select Difficulty")
            label.setStyleSheet("color: #00ff88; font-size: 24px;")
            layout.addWidget(label)
            
            for i in range(1, 11):
                btn = QPushButton(f"Level {i}")
                btn.setFixedSize(150, 40)
                btn.clicked.connect(lambda checked, lvl=i: self.start_game(lvl))
                layout.addWidget(btn)
            
            back = QPushButton("Back")
            back.clicked.connect(lambda: self.stack.setCurrentWidget(self.menu))
            layout.addWidget(back)
            return page
        def start_game(self, level):
            self.state.level = level
            # recreate the graph puzzle with new difficulty
            self.graph.next_graph(level)
            self.graph.title.setText(f"Bolical World | LEVEL {level}")
            self.stack.setCurrentWidget(self.graph)
        def start_structuring(self):
            self.state.mode = MODE_SKY_HIGH
            self.graph.reset_sky_high()
            self.stack.setCurrentWidget(self.graph)
        def open_shop(self):
            self.shop.points_label.setText(f"Points: {self.state.points}")
            self.stack.setCurrentWidget(self.shop)
class ShopPage(QWidget):
    def __init__(self, game_state, parent=None):
        super().__init__(parent)
        self.state = game_state
        self.parentwin = parent
        self.setStyleSheet("background-color: black;")
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        # Title
        title = QLabel("Shop")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #00ff88; font-size: 20px; font-weight: bold;")
        self.layout.addWidget(title)

        # Points display
        self.points_label = QLabel(f"Points: {self.state.points}")
        self.points_label.setAlignment(Qt.AlignCenter)
        self.points_label.setStyleSheet("color: #00ffaa; font-size: 14px;")
        self.layout.addWidget(self.points_label)

        # Scrollable area for items
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        self.shop_widget = QWidget()
        self.shop_layout = QGridLayout(self.shop_widget)
        self.shop_layout.setContentsMargins(10, 10, 10, 10)
        self.shop_layout.setSpacing(15)
        
        self.scroll_area.setWidget(self.shop_widget)
        self.layout.addWidget(self.scroll_area)
        self.item_buttons = {}

        # Example shop items
        self.items = [
            {"name": "Tetra", "price": 5, "type": "infinite", "purchased": False},
            {"name": "Sky High Structuring", "price": 100, "type": "1 purchase", "purchased": False},
            {"name": "Graphite", "price": 500, "type": "1 purchase", "purchased": False},
            {"name": "Tesseract", "price": 1000000, "type": "1 purchase", "purchased": False}
        ]

        self.item_buttons = {}
        self.build_shop()

        # Back button
        back_btn = QPushButton("Back to Menu")
        back_btn.setStyleSheet(stylesheet)
        back_btn.clicked.connect(self.go_back)
        self.layout.addWidget(back_btn)

    def build_shop(self):
      self.item_buttons = {}
      for row, item in enumerate(self.items):
          name_label = QLabel(item["name"])
          name_label.setStyleSheet("color: #00ffaa; font-size: 14px;")
          self.shop_layout.addWidget(name_label, row, 0)
  
          price_btn = QPushButton()
          price_btn.setStyleSheet(stylesheet)
          price_btn.clicked.connect(partial(self.buy_item, item))
  
          self.shop_layout.addWidget(price_btn, row, 1)
          self.item_buttons[item["name"]] = price_btn
  
          self.update_item_button(item)
    def showEvent(self, event):
       super().showEvent(event)
       self.update_points()



    def update_item_button(self, item):
        btn = self.item_buttons[item["name"]]
        if item["type"] == "1 purchase" and item["purchased"]:
            btn.setText("Purchased")
            btn.setEnabled(False)
            btn.setStyleSheet("color: #555; background-color: #001100; border: 1px solid #004400; padding: 8px; font-size: 14px;")
        else:
            btn.setText(f"{item['price']} pts")
            btn.setEnabled(self.state.points >= item["price"])

    def buy_item(self, item):
        if item["type"] == "1 purchase" and item["purchased"]:
            return  # Safety check

        if self.state.points >= item["price"]:
            self.state.points -= item["price"]

            if item["type"] == "1 purchase":
                item["purchased"] = True

            if item["name"] == "Sky High Structuring":
                self.state.unlocks["sky_high"] = True
                self.parentwin.structure.show()

            self.update_points()
    def update_points(self):
        self.points_label.setText(f"Points: {self.state.points}")
        for item in self.items:
            self.update_item_button(item)

    def go_back(self):
        if self.parentwin:
            self.parentwin.stack.setCurrentWidget(self.parentwin.menu)
class GraphPuzzle(QWidget):
    def __init__(self, game_state, parent=None):
        super().__init__(parent)
        self.state = game_state
        self.parentwin = parent
        self.setWindowTitle("Bolical World")
        self.resize(800,600)
        self.setStyleSheet("background-color: black;")

        layout = QVBoxLayout(self)
        layout.setSpacing(6)

        # Title
        self.title = QLabel(f"Bolical World | LEVEL {'?'}")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: #00ff88; font-size: 18px; font-weight: bold;")
        layout.addWidget(self.title)

        # Hint
        hint = QLabel("Enter an equation f(x). Allowed: sin, cos, tan, abs, pi, e, sinh, cosh, tanh, sqrt, exp, ln, inverse trig/hyperbolic")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet("color: #00aa66; font-size: 11px;")
        layout.addWidget(hint)

        # Input
        self.input = QLineEdit()
        self.input.setPlaceholderText("e.g. sin(x) + 0.5*cos(2*x)")
        self.input.setStyleSheet("""
            QLineEdit {
                background-color: black;
                color: #00ff88;
                border: 1px solid #00aa66;
                padding: 6px;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.input)

        # Canvas
        self.fig = Figure(facecolor="black")
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setFocusPolicy(Qt.StrongFocus)
        self.canvas.setFocus()
        layout.addWidget(self.canvas, 1)
        self.canvas.mpl_connect("scroll_event", self.on_scroll)
        self._press_event = None
        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("button_release_event", self.on_release)
        self.canvas.mpl_connect("motion_notify_event", self.on_motion)
        self.canvas.mpl_connect("key_press_event", self.on_key)
        self.ax = self.fig.add_subplot(111)
        self._style_axes()

        # Back/Skip buttons
        btn_layout = QHBoxLayout()
        back_btn = QPushButton("Back")
        skip_btn = QPushButton("Skip")
        back_btn.clicked.connect(self.go_back)
        skip_btn.clicked.connect(lambda: self.next_graph(skip=True))
        self.skip_btn = skip_btn
        btn_layout.addWidget(back_btn)
        btn_layout.addWidget(skip_btn)
        layout.addLayout(btn_layout)

        # Data
        self.points_per_level = {1:1,2:3,3:5,4:10,5:30,6:50,7:100,8:500,9:10000,10:1000000}
        self.x_sky = np.linspace(0, 100, 20000)
        self.x_norm = np.linspace(-10, 10, 20000)

        # Target
        #self.target_equation = equation
        #self.y_target = eval_expr(self.target_equation, self.x)
        #y_target = np.array(self.y_target, dtype=float)
        #y_target[~np.isfinite(y_target)] = np.nan
        #y_target = break_asymptotes(y_target)
        #self.y_target = y_target
        #self.target_line, = self.ax.plot(self.x, self.y_target,
        #                                 linestyle="--", linewidth=1.5,
        #                                 color="#007744", alpha=0.8)
        self.player_line, = self.ax.plot([],[], linewidth=2, color="#00ff88")
#
        self.canvas.draw()
        self.solved = False

        self.input.textChanged.connect(self.update_graph)
        
        self.next_button = QPushButton("Next Challenge")
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: #002211;
                color: #00ffaa;
                border: 1px solid #00aa66;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #003322;
            }
        """)
        self.next_button.clicked.connect(lambda: self.next_graph(skip=False))
        self.next_button.hide()
        self.sky_lbl = QLabel()
        self.sky_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.sky_lbl)
        if self.state.mode == MODE_SKY_HIGH:
            self.sky_lbl.setText("Sky High Structuring | Max slope ≤ 1 | Reach y = 100 between x = 0 and 100")
        else:
            self.sky_lbl.hide()
        layout.addWidget(self.next_button)
    def _style_axes(self): 
        self.ax.set_facecolor("black") 
        self.ax.grid(True, color="#003322", linewidth=0.5) 
        for spine in self.ax.spines.values(): 
            spine.set_color("#006644") 
        self.ax.tick_params(colors="#00aa66") 
        if self.state.mode == MODE_SKY_HIGH:
            self.ax.set_xlim(0,100)
            self.ax.set_ylim(0,110)
        else:
            self.ax.set_xlim(-10,10) 
            self.ax.set_ylim(-20,20)
    def update_graph(self): 
        if self.solved: 
            return 
        self._style_axes()
        expr = self.input.text().strip() 
        if not expr: 
            self.player_line.set_data([],[]) 
            self.canvas.draw_idle() 
            return 
        try: 
          sanitized_expr = preprocess_for_eval(expr) 
          x = self.x_sky if self.state.mode == MODE_SKY_HIGH else self.x_norm
          y_player = eval_expr(sanitized_expr, x)
          y_player = np.array(y_player, dtype=float)
          y_player[~np.isfinite(y_player)] = np.nan
          y_player = break_asymptotes(y_player)
          
          self.player_line.set_data(x, y_player)

          if self.state.mode == MODE_SKY_HIGH:
             success, reason = sky_high_check(x, y_player)
             self.sky_lbl.setText(reason)
             if success:
                 self.on_success()
          elif check_match_numeric(self.target_equation, expr, self.x_norm): 
              self.on_success() 
          self.canvas.draw_idle() 
        except Exception: 
            pass
    # ----- NEW METHODS ADDED -----
    def go_back(self):
      if self.parentwin:
          if self.state.mode == MODE_SKY_HIGH:
              self.state.mode = MODE_NORMAL
              self.parentwin.stack.setCurrentWidget(self.parentwin.menu)
          else:
              self.parentwin.stack.setCurrentWidget(self.parentwin.difficulty_select)


    def next_graph(self, skip=False):
        """Generate next graph. If skip=True, no points are awarded."""
        # Clear old UI state
        self.ax.cla()
        self._style_axes()
        self.solved = False
        self.input.setDisabled(False)
        self.input.clear()

        if hasattr(self, "success"):
              self.success.hide()
        if hasattr(self, "sky_lbl"):
            self.sky_lbl.hide()
        self.next_button.hide()
        if self.state.mode == MODE_SKY_HIGH:
            return
        # Generate new equation
        global equation
        equation = generate_level_equation(self.state.level)
        equation = preprocess_for_eval(equation)

        # Numeric evaluation
        self.target_equation = equation
        self.y_target = eval_expr(self.target_equation, self.x_norm)
        y_target = np.array(self.y_target, dtype=float)
        y_target[~np.isfinite(y_target)] = np.nan
        y_target = break_asymptotes(y_target)
        if not np.any(np.isfinite(y_target)):
            self.next_graph(skip=True)
            return
        if np.count_nonzero(np.isfinite(y_target)) < 10:
            self.next_graph(skip=True)
            return
        self.y_target = y_target
        self.target_line, = self.ax.plot(self.x_norm, self.y_target,
                                         linestyle="--", linewidth=1.5,
                                         color="#007744", alpha=0.8)
        self.player_line, = self.ax.plot([],[], linewidth=2, color="#00ff88")

        self.ax.relim()
        self.ax.autoscale_view()
        self.ax.set_autoscale_on(False)
        self.skip_btn.setDisabled(self.state.mode == MODE_SKY_HIGH)
        self.canvas.draw_idle()
        print(equation)

    def on_success(self):
        """Call when player matches the equation."""
        self.solved = True
        self.input.setDisabled(True)
        self.player_line.set_color("#00ffaa")
        self.target_line.set_alpha(0.3)

        # Award points immediately
        self.state.points += self.points_per_level[self.state.level]
        self.success = QLabel(f"MATCH CONFIRMED! Points: {self.state.points}")
        self.success.setAlignment(Qt.AlignCenter)
        self.success.setStyleSheet("color: #00ffaa; font-size: 16px; font-weight: bold;")
        self.layout().addWidget(self.success)
        self.next_button.show()
        self.canvas.draw_idle()
    def on_scroll(self, event): 
        if event.inaxes != self.ax: 
            return # Ignore scrolls outside the graph 
        base_scale = 1.2 
        ax = self.ax 
        cur_xlim = ax.get_xlim() 
        cur_ylim = ax.get_ylim() 
        xdata = event.xdata 
        ydata = event.ydata 
        if xdata is None or ydata is None: 
            return 
        scale_factor = 1 / base_scale if event.button == "up" else base_scale 
        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor 
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor 
        relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0]) 
        rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0]) 
        ax.set_xlim( xdata - new_width * (1 - relx), xdata + new_width * relx ) 
        ax.set_ylim( ydata - new_height * (1 - rely), ydata + new_height * rely ) 
        self.canvas.draw_idle() 
    def on_press(self, event): 
        if event.inaxes != self.ax: 
            return 
        self._press_event = event.xdata, event.ydata, self.ax.get_xlim(), self.ax.get_ylim() 
    def on_release(self, event): 
        self._press_event = None 
    def on_motion(self, event): 
        if self._press_event is None or event.inaxes != self.ax: 
            return 
        xpress, ypress, (x0, x1), (y0, y1) = self._press_event 
        dx = xpress - event.xdata 
        dy = ypress - event.ydata 
        self.ax.set_xlim(x0 + dx, x1 + dx) 
        self.ax.set_ylim(y0 + dy, y1 + dy) 
        self.canvas.draw_idle()
    def on_key(self, event): 
        if event.key == "enter" and self.solved: self.next_graph()
    def reset_sky_high(self):
      self.next_graph(True)
      self.solved = False
      self.input.setDisabled(False)
      self.input.clear()
  
      self.ax.cla()
      self._style_axes()
  
      self.title.setText("SKY HIGH STRUCTURING")
  
      self.sky_lbl.setText(
          "Goal: Reach y = 100\n"
          "Constraints:\n"
          "• Mustn't be overly steep a majority of the time (max = approx 50°)\n"
          "• 0 ≤ x ≤ 100\n"
          "• Must touch origin (0,0)\n"
          "• No skipping allowed\n"
          "• Solution requires level of creativity, cheap solutions are disallowed"
      )
      self.sky_lbl.show()
  
      self.next_button.hide()
  
      self.player_line, = self.ax.plot([], [], linewidth=2, color="#00ff88")
      self.skip_btn.setDisabled(True)
      self.canvas.draw_idle()

# ---------- RUN ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BolicalWorld()
    window.show()
    sys.exit(app.exec())