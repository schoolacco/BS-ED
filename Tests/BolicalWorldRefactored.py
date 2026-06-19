from __future__ import annotations
import sys
import numpy as np
import re
import random
import scipy.special as sci
from functools import partial
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor
import warnings
from dataclasses import dataclass
from enum import Enum
warnings.filterwarnings("ignore")
np.seterr(all="ignore")
stylesheet = open("Tests/graphite.qss", "r")
stylesheet = stylesheet.read()
app = QApplication(sys.argv)
class BolicalWorld(QDialog):
    class ShopPage(QWidget):
        pass
    class GraphPuzzle(QWidget):
        class GameState(Enum):
            MODE_NORMAL = 0x0
            MODE_SKY_HIGH = 0x1
        pass
app.exec()