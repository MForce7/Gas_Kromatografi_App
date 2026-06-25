from PySide6.QtCore import QObject, QTimer, Signal
import time, re


class CalibrationWorker(QObject):
    # ================= SIGNAL =================
    data_updated = Signal(list)
    auto_scale_triggered = Signal()
    ready_state = Signal()
    status_changed = Signal(str)  # "idle" | "calibrating"

    def __init__(
        self,
        threshold1: float,
        threshold2: float,
        connection,
        logger,
        graph_plotter,
        cooldown_duration,
        required_stable_count
    ):
        super().__init__()

        # ================= CONFIG =================
        self.threshold1 = threshold1
        self.threshold2 = threshold2

        self.cooldown_duration = cooldown_duration
        self.required_stable_count = required_stable_count

        # ================= DEPENDENCY =================
        self.connection = connection
        self.data_logger = logger
        self.graph_plotter = graph_plotter

        # ================= STATE =================
        self.receiving_data = False
        self._is_connected = False
        self.mode = None  # "manual" | "auto"

        # ================= AUTO SCALE STATE =================
        self.cooldown_until = 0
        self.last_scale_time = None
        self.stable_count = 0

        # ================= PLOT TIMER =================
        self.plot_timer = QTimer()
        self.plot_timer.setInterval(300)
        self.plot_timer.timeout.connect(self._flush_plot)

    # =====================================
    # PUBLIC API
    # =====================================

    def start_manual_scale(self):
        self._safe_restart()
        self.mode = "manual"
        self._reset_auto_state()
        self._start()
        self.status_changed.emit("calibrating")
        print("MODE: MANUAL")

    def scale(self):
        """Manual trigger scaling"""
        print("MANUAL SCALE → kirim '2'")
        try:
            if self.connection and self.connection.serial:
                self.connection.serial.send("2")
        except Exception as e:
            print("Serial error:", e)

    def start_auto_scale(self):
        self._safe_restart()
        self.mode = "auto"
        self._reset_auto_state()
        self._start()
        print("MODE: AUTO")
        self.status_changed.emit("calibrating")

    def stop(self):
        if not self.receiving_data:
            return
        
        self.status_changed.emit("idle")

        self.plot_timer.stop()
        self._stop_serial()
        self._disconnect_signal()

        self.receiving_data = False
        self._reset_auto_state()

        print("STOP")

    # =====================================
    # CORE
    # =====================================

    def _safe_restart(self):
        if self.receiving_data:
            self.stop()

    def _start(self):
        self.receiving_data = True
        self.data_logger.reset()

        self._connect_signal()
        self._start_serial()
        self.plot_timer.start()

    def _start_serial(self):
        try:
            self.connection.serial.send("4")
            self.connection.serial.send("1")
        except Exception as e:
            print("Serial start error:", e)

    def _stop_serial(self):
        try:
            self.connection.serial.send("0")
            self.connection.serial.send("5")
        except Exception as e:
            print("Serial stop error:", e)

    def _connect_signal(self):
        if not self._is_connected:
            self.connection.serial.data_received.connect(self._on_data)
            self._is_connected = True

    def _disconnect_signal(self):
        if self._is_connected:
            try:
                self.connection.serial.data_received.disconnect()
            except Exception:
                pass
            self._is_connected = False

    # =====================================
    # DATA HANDLING
    # =====================================

    _pattern = re.compile(
        r"TCD \(mV\):\s*([-+]?\d*\.?\d+)\s*\|\s*TVOC \(ppb\):\s*(\d+)"
    )

    def parse_sensor_data(self, text: str):
        match = self._pattern.search(text)
        if not match:
            return None
        return [float(match.group(1)), int(match.group(2))]

    def _on_data(self, text: str):
        if not self.receiving_data:
            return

        try:
            values = self.parse_sensor_data(text)
            if not values:
                return

            # ================= LOG =================
            self.data_logger.add_sample(values)
            self.data_updated.emit(values)

            # ================= AUTO SCALE =================
            if self.mode == "auto":
                self._process_auto_scale(values)

        except Exception as e:
            print("Error parsing data:", e)

    def _flush_plot(self):
        if not self.data_logger.data:
            return

        try:
            self.graph_plotter.plot_from_lists(
                self.data_logger.data,
                ["time", "sig1", "sig2"]
            )
        except Exception as e:
            print("Plot error:", e)

    # =====================================
    # AUTO SCALE LOGIC (FINAL)
    # =====================================

    def _process_auto_scale(self, data):
        now = time.time()

        # ================= COOLDOWN =================
        if now < self.cooldown_until:
            return

        is_violation = (
            data[0] > self.threshold1 or
            data[1] > self.threshold2
        )

        # ================= SETELAH PERNAH SCALE =================
        if self.last_scale_time is not None:

            if not is_violation:
                self.stable_count += 1
            else:
                self.stable_count = 0

            # ================= STABIL → STOP =================
            if self.stable_count >= self.required_stable_count:
                print("STABIL → STOP ✅")
                self.ready_state.emit()
                self.stop()
                return

        # ================= SCALE =================
        if is_violation:
            self.scale()  # ⬅️ pakai API baru

            self.auto_scale_triggered.emit()

            self.last_scale_time = now
            self.cooldown_until = now + self.cooldown_duration
            self.stable_count = 0

    # =====================================
    # RESET STATE
    # =====================================

    def _reset_auto_state(self):
        self.cooldown_until = 0
        self.last_scale_time = None
        self.stable_count = 0