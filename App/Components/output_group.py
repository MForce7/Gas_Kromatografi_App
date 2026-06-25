import os
from PySide6.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QGridLayout,
)

from PySide6.QtCore import QStandardPaths, Signal


class OutputGroup(QGroupBox):
    clicked_save_button: Signal = Signal()
    
    def __init__(self):
        super().__init__("Output")

        layout = QGridLayout(self)

        # -----------------------
        # Default Documents path
        # -----------------------
        self.output_dir = QStandardPaths.writableLocation(
            # QStandardPaths.DocumentsLocation
            QStandardPaths.StandardLocation.DocumentsLocation
        )
        self.auto_save_state = True

        # -----------------------
        # Widgets
        # -----------------------
        lbl_folder = QLabel("Folder:")
        lbl_file = QLabel("File:")

        self.txt_folder = QLineEdit(self.output_dir)
        self.txt_folder.setReadOnly(True)
        self.txt_folder.textChanged.connect(self.set_output_dir)

        self.btn_browse = QPushButton("Browse")
        self.btn_browse.clicked.connect(self.browse_folder)

        self.txt_file = QLineEdit("output_data.csv")
        # self.debug_button = QPushButton("tester")
        # self.debug_button.clicked.connect(self.get_output_path)
        # self.tesisi = self.get_output_path()

        self.auto_save_checkbox = QCheckBox("Auto Save")
        self.auto_save_checkbox.setChecked(True)
        self.auto_save_checkbox.stateChanged.connect(self.auto_save)
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.clicked_save_button.emit)


        
        
        
        # -----------------------
        # Layout
        # -----------------------
        layout.addWidget(lbl_folder, 0, 0)
        layout.addWidget(self.txt_folder, 0, 1, 1, 2)
        layout.addWidget(self.btn_browse, 0, 3)

        layout.addWidget(lbl_file, 1, 0)
        layout.addWidget(self.txt_file, 1, 1)
        layout.addWidget(self.auto_save_checkbox, 1, 2)
        layout.addWidget(self.save_button, 1, 3)
        # layout.addWidget(self.debug_button, 1, 2)

    # -----------------------
    # Browse folder
    # -----------------------
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Output Folder",
            self.txt_folder.text()
        )
        if folder:
            self.txt_folder.setText(folder)


    def auto_save(self, state):
        if state == 2:  # Checked
            print('on')
            self.auto_save_state = True
        else:
            print('off')
            self.auto_save_state = False
            # self.label.setText("Status: OFF")





    # -----------------------
    # Safe output path (NO overwrite)
    # -----------------------
    def get_output_path(self):
        folder = self.txt_folder.text()
        filename = self.txt_file.text()

        base, ext = os.path.splitext(filename)
        if not ext:
            ext = ".txt"

        full_path = os.path.join(folder, base + ext)

        counter = 1
        while os.path.exists(full_path):
            full_path = os.path.join(
                folder,
                f"{base}({counter}){ext}"
            )
            counter += 1
        # print(full_path)
        return full_path
    
    def set_output_dir(self, text):
        self.output_dir = text