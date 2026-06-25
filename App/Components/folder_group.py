# folder_group.py
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QFileDialog
)

from PySide6.QtCore import Signal
class FolderGroup(QGroupBox):
    folder_changed = Signal(str)

    def __init__(self):
        super().__init__("Folder")

        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("Select data folder...")

        self.browse_btn = QPushButton("Browse")

        layout = QHBoxLayout(self)
        layout.addWidget(self.path_edit)
        layout.addWidget(self.browse_btn)

        self.browse_btn.clicked.connect(self.browse_folder)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.path_edit.setText(folder)
            self.folder_changed.emit(folder)
