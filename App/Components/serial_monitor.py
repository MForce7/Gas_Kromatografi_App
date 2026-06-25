# serial_monitor.py
from PySide6.QtWidgets import ( # type: ignore
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton
)

class SerialMonitor(QGroupBox):
    def __init__(self, serial):
        super().__init__("Serial Monitor")
        self.serial = serial
        
        # UI
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.input = QLineEdit()
        self.input.setPlaceholderText("Type command and press Send")
        self.send_btn = QPushButton("Send")

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input)
        input_layout.addWidget(self.send_btn)
        layout = QVBoxLayout(self)
        layout.addWidget(self.output)
        layout.addLayout(input_layout)

        # Serial thread
        self.serial.data_received.connect(self._append_text)
        self.serial.status.connect(self._append_text)

        self.send_btn.clicked.connect(self._send)
        self.input.returnPressed.connect(self._send)

        # AUTO START
        self.serial.start()

    def _append_text(self, text):
        self.output.append(text)

    def _send(self):
        text = self.input.text().strip()
        if text:
            self.serial.send(text)
            self.output.append(f"> {text}")
            self.input.clear()
        # print(self.serial.running)

    def close_event(self, event):
        self.serial.stop()
        self.serial.wait()
        event.accept()
