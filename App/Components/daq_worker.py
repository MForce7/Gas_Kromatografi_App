from PySide6.QtCore import QTimer
import time
import re


class Worker:

    _pattern = re.compile(
        r"TVOC \(ppb\):\s*(\d+)"
    )

    def __init__(
        self,
        connection,
        logger,
        output,
        graph_plotter
    ):
        self.connection = connection
        self.output = output
        self.data_logger = logger
        self.graph_plotter = graph_plotter

        self.receiving_data = False
        self._is_connected = False

        self.start_time = 0
        self.duration = 0
        self.mode = None

        self.daq_status = False

        self.duration_timer = QTimer()
        self.duration_timer.setInterval(500)
        self.duration_timer.timeout.connect(self._check_duration)

        self.output.clicked_save_button.connect(self._finalize)

    # =====================================================
    # PUBLIC METHODS
    # =====================================================

    def start_with_timer(self, duration_sec: int):

        if duration_sec <= 0:
            print("Durasi tidak valid")
            return

        self.mode = "timer"
        self.duration = duration_sec
        self.start_time = time.monotonic()

        self._start()

        self.duration_timer.start()

        print("Mode TIMER dimulai")

    def start_continuous(self):

        self.mode = "continuous"

        self._start()

        print("Mode CONTINUOUS dimulai")

    def stop(self, finalize=True):

        if not self.receiving_data:
            return

        self.duration_timer.stop()

        self._stop_serial()
        self._disconnect_signal()

        self.receiving_data = False
        self.daq_status = False

        print("Proses dihentikan")

        if finalize and self.data_logger.data:
            self._finalize()

    # =====================================================
    # INTERNAL
    # =====================================================

    def _start(self):

        self.receiving_data = True
        self.daq_status = True

        self.data_logger.reset()

        self._connect_signal()
        self._start_serial()

    def _start_serial(self):

        self.connection.serial.send('4')
        self.connection.serial.send('1')

    def _stop_serial(self):

        self.connection.serial.send('0')
        self.connection.serial.send('5')

    def _check_duration(self):

        if self.mode != "timer":
            return

        elapsed = time.monotonic() - self.start_time

        if elapsed >= self.duration:
            print("Durasi selesai")
            self.stop(finalize=True)

    def _connect_signal(self):

        if not self._is_connected:
            self.connection.serial.data_received.connect(self.on_logging)
            self._is_connected = True

    def _disconnect_signal(self):

        if self._is_connected:
            try:
                self.connection.serial.data_received.disconnect(self.on_logging)
            except TypeError:
                pass

            self._is_connected = False

    def _finalize(self):

        if self.output.auto_save_state:

            final_path = self.output.get_output_path()

            self.data_logger.export_csv(final_path)

            print(f"Data disimpan ke: {final_path}")

    # =====================================================
    # DATA HANDLING
    # =====================================================

    def parse_sensor_data(self, text: str):

        match = self._pattern.search(text)

        if match is None:
            return None

        return int(match.group(1))

    def on_logging(self, text: str):
        
        if not self.receiving_data:
            return

        try:

            values = self.parse_sensor_data(text)

            if values is None:
                return

            self.data_logger.add_sample(values)

            self._flush_plot()

        except Exception as e:

            print(f"Caught an error: {e}")

            self._finalize()

    def _flush_plot(self):

        self.graph_plotter.plot_from_lists(
            self.data_logger.data
        )