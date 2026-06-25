from PySide6.QtCore import QThread, Signal
from queue import Queue, Empty
import serial
import time


class SerialReader(QThread):
    data_received = Signal(str)
    status = Signal(str)

    def __init__(self, config: dict):
        super().__init__()
        self.config = config
        self.running = True
        self.ser = None
        self.connected = False
        self._send_queue: Queue[str] = Queue()  # ← antrian perintah

    def run(self):
        port = self.config['comPort']
        baudrate = self.config['baudRate']

        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            self.status.emit(f"Connected to {port}")
        except Exception as e:
            self.status.emit(f"Error: {e}")
            return

        self.connected = False

        while self.running:
            try:
                # 1. Kirim semua perintah yang antri
                while not self._send_queue.empty():
                    try:
                        text = self._send_queue.get_nowait()
                        self.ser.write((text + "\n").encode())
                        time.sleep(0.05)  # beri jeda antar perintah ke Arduino
                    except Empty:
                        break

                # 2. Baca data masuk
                if self.ser.in_waiting:
                    line = self.ser.readline().decode(errors="ignore").strip()
                    if line == "ESP32 Ready":
                        self.connected = True
                        self.status.emit("Device connected")
                    if line:
                        self.data_received.emit(line)

            except Exception as e:
                self.status.emit(str(e))
                break

        if self.ser and self.ser.is_open:
            self.ser.close()
            self.status.emit("Serial closed")

    def send(self, text: str) -> None:
        """Aman dipanggil dari thread manapun — hanya masukkan ke queue."""
        self._send_queue.put(text)

    def stop(self) -> None:
        self.running = False

    def restart(self) -> None:
        if self.isRunning():
            self.status.emit("Restarting serial...")
            self.running = False
            self.wait()

        # Bersihkan queue lama sebelum restart
        while not self._send_queue.empty():
            try:
                self._send_queue.get_nowait()
            except Empty:
                break

        self.running = True
        self.start()
    
    def disconnect(self):
        self.stop()
        if hasattr(self, 'ser') and self.ser and self.ser.is_open:
            self.ser.close()