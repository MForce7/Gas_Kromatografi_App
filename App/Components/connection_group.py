from PySide6.QtWidgets import (
    QGroupBox,
    QLabel,
    QComboBox,
    QHBoxLayout,
    QPushButton
)

from PySide6.QtCore import QTimer

from serial.tools import list_ports
from Components.serial_worker import SerialReader

class ConnectionGroup(QGroupBox):
    # def __init__(self, baud_rate, com_port):
    def __init__(self):
        super().__init__("Connection")
        self.config:dict={
            'comPort': 'COM1',
            'baudRate': '9600'
        }
        # self.setObjectName("connection_grup")
        self.serial = SerialReader(self.config)
        layout = QHBoxLayout(self)

        # -----------------------
        # Label
        # -----------------------
        lbl_com = QLabel("COM Port:")
        lbl_baud = QLabel("Baudrate:")

        # -----------------------
        # ComboBox
        # -----------------------
        self.cb_com = QComboBox()
        self.cb_baud = QComboBox()

        # -----------------------
        # Refresh Button
        # -----------------------
        self.refresh_button = QPushButton("Reload")
        self.refresh_button.clicked.connect(self.update_com_list)
        
        # Baudrate options
        baudrates = ["9600", "19200", "38400", "57600", "115200"]
        self.cb_baud.addItems(baudrates)
        self.cb_baud.setCurrentText("9600")

        # Text Changed
        # com_changed = partial(self.cb_com_changed, self.restart_connection)
        self.cb_com.currentTextChanged.connect(self.cb_com_changed)
        self.cb_baud.currentTextChanged.connect(self.cb_baud_changed)

        # reset connection
        self.disconnect_button = QPushButton("Disconnect")
        self.disconnect_button.clicked.connect(self.serial.disconnect)

        layout.addWidget(lbl_com)
        layout.addWidget(self.cb_com)
        layout.addWidget(lbl_baud)
        layout.addWidget(self.cb_baud)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.disconnect_button)

    def update_com_list(self):
        ports = [port.device for port in list_ports.comports()]
        current = self.cb_com.currentText()

        if ports != [self.cb_com.itemText(i) for i in range(self.cb_com.count())]:
            self.cb_com.clear()
            self.cb_com.addItems(ports)

            if current in ports:
                self.cb_com.setCurrentText(current)
    
    def cb_com_changed (self, value):
        self.config['comPort'] = value
        self.serial.restart()
        
    def cb_baud_changed(self, value):
        self.config['baudRate'] = value
        self.serial.restart()