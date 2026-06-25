import sys, os

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication, QPushButton, QVBoxLayout,
    QHBoxLayout, QWidget, QMainWindow, QStackedWidget
)
from PySide6.QtCore import QSize, Qt, QFile, QTextStream
import ctypes

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
    "com.sayid.gcanalyzer"
)
import App.GUI.Assets.assets_rc


from home_page import HomePage
from data_plotter import DataPlotter


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setFixedSize(1080, 620)
        self.setWindowTitle("Kromatografi Gas")

        # -----------------------
        # Central Widget
        # -----------------------
        central = QWidget()
        self.setCentralWidget(central)
        central.setObjectName("main_widget")

        main_layout = QHBoxLayout(central)

        # -----------------------
        # Sidebar
        # -----------------------
        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout(sidebar_widget)
        
        sidebar_widget.setFixedSize(80, 600)
        # sidebar_widget.set
        # sidebar_widget.setStyleSheet()
        sidebar_widget.setObjectName("sidebar")

        # Buttons
        btn_home = QPushButton()
        btn_home.setIcon(QIcon(":/img/Home.png"))
        btn_home.setIconSize(QSize(35, 35))
        btn_home.setObjectName("home_button")
        btn_home.setCursor(Qt.PointingHandCursor)

        btn_settings = QPushButton()
        btn_settings.setIcon(QIcon(":/img/Graph.png"))
        btn_settings.setIconSize(QSize(35, 35))
        btn_settings.setObjectName("setting_button")
        btn_settings.setCursor(Qt.PointingHandCursor)

        # Connections
        btn_home.clicked.connect(self.show_home)
        btn_settings.clicked.connect(self.show_plot)
        # btn_calibrate.clicked.connect(self.show_calibrate)

        sidebar_layout.addWidget(btn_home) 
        sidebar_layout.addWidget(btn_settings)
        # sidebar_layout.addWidget(btn_calibrate)
        sidebar_layout.addStretch()

        # -----------------------
        # Pages
        # -----------------------
        self.stack = QStackedWidget()
        self.stack.addWidget(HomePage())
        self.stack.addWidget(DataPlotter())
        # Layout Composition
        main_layout.addWidget(sidebar_widget, 1)
        main_layout.addWidget(self.stack, 4)

    # -----------------------
    # Navigation Methods
    # -----------------------
    def show_home(self):
        self.stack.setCurrentIndex(0)

    def show_plot(self):
        self.stack.setCurrentIndex(1)

# ==============================
# App Entry
# ==============================
if __name__ == "__main__":
    os.environ["QT_QPA_PLATFORM"] = "windows:darkmode=1"
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/img/Icon.ico"))
    # Load global stylesheet
    try:
        # file = QFile(":/Style/global_style.qss")
        # if file.open(QFile.ReadOnly | QFile.Text):
        #     stream = QTextStream(file)
        #     app.setStyleSheet(stream.readAll())
        #     file.close()
        file = QFile(":/Style/global_style.qss")
        file.open(QFile.ReadOnly)
        app.setStyleSheet(bytes(file.readAll()).decode("utf-8"))
        file.close()
        
    except FileNotFoundError:
        print("Stylesheet not found.")

    window = MainWindow()
    # window.setWindowIcon(QIcon("GUI/Assets/img/Icon.ico"))
    window.setWindowIcon(QIcon(":/img/Icon.ico"))
    window.show()

    sys.exit(app.exec())
