from PyQt6.QtWidgets import QLabel, QComboBox, QWidget, QPushButton, QVBoxLayout
from PyQt6.QtGui import QFont
from functools import partial
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
# from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.figure import Figure
import numpy as np
import time

def create_text(self, label_text:str, position:list=[0,0], font_size=12, bold=False):
    font = QFont("Arial", font_size)
    font.setBold(bold)
    label = QLabel(self)
    label.setText(label_text)
    label.setFont(font)
    label.move(position[0], position[1])
    return label

def create_combobox(config:dict, config_key: str, combo_listener, items: list[str]=[]) -> QComboBox:
    combo = QComboBox()
    config[config_key] = combo.currentText()
    combo.addItems(items)
    combo.currentTextChanged.connect(combo_listener)
    return combo
    
def create_button(label:str = '', size: list|None = None, button_function = None,pos:list=[0,0], icon_file=None):
    button = QPushButton()
    if size:
        button.setFixedSize(size[0], size[1])
    button.move(pos[0],pos[1])
    button.setText(label)
    if icon_file:
        button.setIcon(icon_file)
    button.clicked.connect(button_function)
    return button

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        
        
        
        
        
        
        
class graph_display(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        # static canvas
        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(NavigationToolbar(static_canvas, self))
        layout.addWidget(static_canvas)

        self._static_ax = static_canvas.figure.subplots()
        t = np.linspace(0, 10, 501)
        self._static_ax.plot(t, np.tan(t), ".")

        # # dynamic canvas
        # dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        # layout.addWidget(dynamic_canvas)
        # layout.addWidget(NavigationToolbar(dynamic_canvas, self))

        # self._dynamic_ax = dynamic_canvas.figure.subplots()
        # # Set up a Line2D.
        # self.xdata = np.linspace(0, 10, 101)
        # self._update_ydata()
        # self._line, = self._dynamic_ax.plot(self.xdata, self.ydata)
        # # The below two timers must be attributes of self, so that the garbage
        # # collector won't clean them after we finish with __init__...

        # # The data retrieval may be fast as possible (Using QRunnable could be
        # # even faster).
        # self.data_timer = dynamic_canvas.new_timer(1)
        # self.data_timer.add_callback(self._update_ydata)
        # self.data_timer.start()
        # # Drawing at 50Hz should be fast enough for the GUI to feel smooth, and
        # # not too fast for the GUI to be overloaded with events that need to be
        # # processed while the GUI element is changed.
        # self.drawing_timer = dynamic_canvas.new_timer(20)
        # self.drawing_timer.add_callback(self._update_canvas)
        # self.drawing_timer.start()

    # def _update_ydata(self):
    #     # Shift the sinusoid as a function of time.
    #     self.ydata = np.sin(self.xdata + time.time())

    # def _update_canvas(self):
    #     self._line.set_data(self.xdata, self.ydata)
    #     self._line.figure.canvas.draw_idle()