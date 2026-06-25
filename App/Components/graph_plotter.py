from __future__ import annotations

import csv
import os
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from PySide6.QtWidgets import QWidget, QVBoxLayout


class GraphPlotter(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("graph_canvas")

        plt.style.use("seaborn-v0_8-darkgrid")

        self.figure = Figure(figsize=(6, 5), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.ax: Axes
        self.line: Line2D

        self._init_plot()

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def _init_plot(self):

        self.figure.clear()

        self.ax = self.figure.add_subplot(111)

        self.line, = self.ax.plot([], [], linewidth=1.5)

        # self.ax.set_title("TVOC")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("TVOC (ppb)")
        self.ax.grid(True, alpha=0.4)

        self.canvas.draw()

    # =====================================================
    # PUBLIC
    # =====================================================

    def plot_from_csv(self, path):

        path = Path(path)

        with path.open(newline="", encoding="utf-8") as f:

            reader = csv.DictReader(f)

            rows = list(reader)

        self.plot_from_lists(rows)

    def plot_from_lists(self, rows):

        if not rows:
            return

        try:
            if "TVOC" in rows[0]:
                x = [float(row["time"]) for row in rows]
                y = [float(row["TVOC"]) for row in rows]
            else:
                x = [float(row["time"]) for row in rows]
                y = [float(row["sig2"]) for row in rows]

        except (KeyError, ValueError) as exc:
            raise ValueError(f"Gagal parsing data: {exc}") from exc

        self.line.set_data(x, y)

        self.ax.relim()
        self.ax.autoscale_view()

        self.canvas.draw_idle()

    # =====================================================
    # EMPTY
    # =====================================================

    def init_empty_plot(self):

        self.line.set_data([], [])

        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)

        self.canvas.draw_idle()