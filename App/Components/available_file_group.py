# available_file_group.py
import os
from PySide6.QtWidgets import (
    QGroupBox,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem
)

from PySide6.QtCore import Signal

class AvailableFileGroup(QGroupBox):
    file_clicked = Signal(str)

    def __init__(self, graph_plotter, file_ext: str = ".csv"):
        super().__init__("Available Files")
        
        self.file_ext = file_ext
        self.graph_plotter = graph_plotter
        # folder_path TIDAK boleh None setelah load_files dipanggil
        self.folder_path = ""  # selalu string

        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.on_item_clicked)

        layout = QVBoxLayout(self)
        layout.addWidget(self.list_widget)

    def load_files(self, folder_path: str) -> None:
        # validasi keras
        assert os.path.isdir(folder_path), f"Invalid folder path: {folder_path}"

        self.folder_path = folder_path
        self.list_widget.clear()

        for fname in sorted(os.listdir(folder_path)):
            if fname.endswith(self.file_ext):
                self.list_widget.addItem(fname)

    def on_item_clicked(self, item: QListWidgetItem) -> None:
        # pastikan load_files sudah dipanggil
        assert self.folder_path != "", "folder_path belum diset. Panggil load_files() dulu."

        full_path = os.path.join(self.folder_path, item.text())
        print(full_path)
        self.file_clicked.emit(full_path)
        self.graph_plotter.plot_from_csv(full_path)