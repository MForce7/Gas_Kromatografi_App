from PySide6.QtWidgets import (
    QWidget,
    QSpinBox,
    QHBoxLayout
)
from PySide6.QtCore import QTimer


class DurationInputWidget(QWidget):
    """
    Widget input durasi (menit & detik).
    Sekarang mendukung countdown.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

        # Timer internal
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_countdown)

        self._remaining_seconds = 0
        self._initial_seconds = 0

    # ================= UI =================
    def _setup_ui(self):
        self.minutes_spin = QSpinBox()
        self.minutes_spin.setRange(0, 999)
        self.minutes_spin.setSuffix(" m")
        self.minutes_spin.setKeyboardTracking(False)

        self.seconds_spin = QSpinBox()
        self.seconds_spin.setRange(0, 59)
        self.seconds_spin.setSuffix(" s")
        self.seconds_spin.setKeyboardTracking(False)
        self.seconds_spin.setValue(1)

        layout = QHBoxLayout(self)
        layout.addWidget(self.minutes_spin)
        layout.addWidget(self.seconds_spin)

    # ================= API =================

    def total_seconds(self) -> int:
        return self.minutes_spin.value() * 60 + self.seconds_spin.value()

    def get_time(self) -> tuple[int, int]:
        return self.minutes_spin.value(), self.seconds_spin.value()

    def set_time(self, minutes: int, seconds: int):
        self.minutes_spin.setValue(minutes)
        self.seconds_spin.setValue(seconds)

    def reset(self):
        self.minutes_spin.setValue(0)
        self.seconds_spin.setValue(0)

    # ================= COUNTDOWN =================

    def start_countdown(self):
        """
        Mulai hitung mundur dari nilai saat ini.
        """
        self._initial_seconds = self.total_seconds()
        self._remaining_seconds = self._initial_seconds

        if self._remaining_seconds <= 0:
            return

        self.minutes_spin.setEnabled(False)
        self.seconds_spin.setEnabled(False)

        self._timer.start(1000)  # tiap 1 detik

    def stop_countdown(self):
        self._timer.stop()
        self.minutes_spin.setEnabled(True)
        self.seconds_spin.setEnabled(True)

    def _update_countdown(self):
        self._remaining_seconds -= 1

        if self._remaining_seconds <= 0:
            self._timer.stop()
            self._restore_initial_time()
            return

        minutes = self._remaining_seconds // 60
        seconds = self._remaining_seconds % 60
        self.set_time(minutes, seconds)

    def _restore_initial_time(self):
        """
        Kembalikan ke nilai sebelum countdown dimulai.
        """
        minutes = self._initial_seconds // 60
        seconds = self._initial_seconds % 60
        self.set_time(minutes, seconds)

        self.minutes_spin.setEnabled(True)
        self.seconds_spin.setEnabled(True)
