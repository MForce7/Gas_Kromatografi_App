from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout # type: ignore

from Components.graph_plotter import GraphPlotter
from Components.calibration_worker import CalibrationWorker   
from Components.controller_group import CalibrationControllerGroup
from Components.serial_monitor import SerialMonitor
from Components.connection_group import ConnectionGroup
from Components.data_logger import DataLogger
from Components.daq_worker import Worker

class CalibrationPage(QWidget):
    def __init__(self):
        super().__init__()
        
        self.cal_config:dict = {
            "interval_seconds": 20,
            "threshold1": 5,
            "threshold2": 5,
            "max_violations": 50,
            "status": "Idle",
        }
        
        self.connection =  ConnectionGroup()
        self.connection.setObjectName("connection_grup")
        self.serial_monitor = SerialMonitor(self.connection.serial)
        self.logger = DataLogger()
        self.graph_plotter = GraphPlotter()
        
        self.calibrator = CalibrationWorker(
            threshold1=self.cal_config["threshold1"],
            threshold2=self.cal_config["threshold2"],
            connection=self.connection,
            logger=self.logger,
            graph_plotter=self.graph_plotter,
            cooldown_duration=self.cal_config["interval_seconds"],
            required_stable_count=self.cal_config["max_violations"]
        )

        self.cal_controller = CalibrationControllerGroup(self.calibrator)
        
        # -----------------------
        # Layout
        # -----------------------
        
        layout = QVBoxLayout(self)
        low_part_layout = QGridLayout(self)
        
        low_part_layout.addWidget(self.serial_monitor, 0, 0, 1, 1)
        low_part_layout.addWidget(self.cal_controller, 0, 5, 1, 5)
        
        layout.addWidget(self.connection)
        layout.addWidget(self.graph_plotter)
        layout.addLayout(low_part_layout)
        # layout.addLayout(low_part_layout)
        