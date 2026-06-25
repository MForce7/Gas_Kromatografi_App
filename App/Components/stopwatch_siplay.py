from PySide6.QtWidgets import QWidget, QLineEdit, QHBoxLayout
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont


class StopwatchDisplayWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._elapsed_seconds = 0
        self._is_running = False
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_time)
        self._setup_ui()
        self._update_display()

    # ================= UI =================

    def _setup_ui(self):
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QHBoxLayout(self)
        layout.addWidget(self.display)

    # ================= Stopwatch Logic =================

    def start(self):
        if not self._is_running:
            self._timer.start(1000)
            self._is_running = True

    def stop(self):
        if self._is_running:
            self._timer.stop()
            self._is_running = False

    def toggle(self):
        if self._is_running:
            self.stop()
        else:
            self.start()

    def reset(self):
        self.stop()
        self._elapsed_seconds = 0
        self._update_display()

    def is_running(self) -> bool:
        return self._is_running

    # ================= Internal =================

    def _update_time(self):
        self._elapsed_seconds += 1
        self._update_display()

    def _update_display(self):
        minutes = self._elapsed_seconds // 60
        seconds = self._elapsed_seconds % 60
        self.display.setText(f"{minutes:02d}:{seconds:02d}")
