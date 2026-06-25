import csv
import os
import re
import time


class DataLogger:

    def __init__(self):
        self.reset()

    # =====================================================
    # DATA BUFFER
    # =====================================================

    def reset(self):
        """Reset buffer dan waktu awal."""
        self.data = []
        self.t0 = time.perf_counter()

    def add_sample(self, tvoc):

        t = time.perf_counter() - self.t0

        self.data.append({
            "time": round(t, 6),
            "TVOC": float(tvoc)
        })

    # =====================================================
    # EXPORT CSV
    # =====================================================

    def export_csv(self, filename, directory=None):

        if not self.data:
            raise RuntimeError("Tidak ada data untuk disimpan.")

        if not isinstance(filename, str):
            raise TypeError("filename harus berupa string.")

        filename = filename.strip()

        if not filename:
            raise ValueError("filename tidak boleh kosong.")

        name, _ = os.path.splitext(filename)
        filename = f"{name}.csv"

        if directory:
            os.makedirs(directory, exist_ok=True)
            base_path = directory
        else:
            base_path = "."

        pattern = re.compile(
            rf"^{re.escape(name)}(?:\((\d+)\))?\.csv$"
        )

        existing_numbers = []

        for file in os.listdir(base_path):

            match = pattern.match(file)

            if match:
                existing_numbers.append(
                    int(match.group(1)) if match.group(1) else 0
                )

        if existing_numbers:
            filename = f"{name}({max(existing_numbers)+1}).csv"

        filepath = os.path.join(base_path, filename)

        with open(filepath, "w", newline="", encoding="utf-8") as f:

            writer = csv.DictWriter(
                f,
                fieldnames=["time", "TVOC"]
            )

            writer.writeheader()
            writer.writerows(self.data)

        return filepath