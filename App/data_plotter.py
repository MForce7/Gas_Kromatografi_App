from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from Components.graph_plotter import GraphPlotter
from Components.folder_group import FolderGroup
from Components.available_file_group import AvailableFileGroup

class DataPlotter(QWidget):
    def __init__(self):
        super().__init__()
        self.num_signals = 1
        layout = QVBoxLayout(self)
        # -----------------------
        # Graph Plotter
        # -----------------------
        self.file_graph_plotter = GraphPlotter()
        self.file_graph_plotter.setFixedHeight(300)
        
        # -----------------------
        # Data Manager
        # -----------------------
        self.folder_group = FolderGroup()
        self.file_group = AvailableFileGroup(self.file_graph_plotter, ".csv")
        self.folder_group.folder_changed.connect(self.file_group.load_files)
        
        # -----------------------
        # Layout
        # -----------------------
        layout.addWidget(self.file_graph_plotter)
        layout.addWidget(self.folder_group)
        layout.addWidget(self.file_group)
