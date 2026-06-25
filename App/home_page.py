from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout # type: ignore
from Components.connection_group import ConnectionGroup
from Components.controller_group import ControllerGroup
from Components.output_group import OutputGroup
from Components.serial_monitor import SerialMonitor
from Components.graph_plotter import GraphPlotter
from Components.data_logger import DataLogger
from Components.daq_worker import Worker

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        
        
        # -----------------------
        # DAQ Process
        # -----------------------
        self.connection =  ConnectionGroup()
        self.connection.setObjectName("connection_grup")
        self.serial_monitor = SerialMonitor(self.connection.serial)
        
        self.logger = DataLogger()
        self.output = OutputGroup()
        
        self.graph_plotter = GraphPlotter()
        self.graph_plotter.setFixedHeight(300)
        self.daq_worker = Worker(self.connection, self.logger, self.output, self.graph_plotter)
        self.controller = ControllerGroup(self.daq_worker, self.graph_plotter, self.logger)
        
        
        
        
        # -----------------------
        # Layout
        # -----------------------
        
        layout = QVBoxLayout(self)
        control_output_layout = QVBoxLayout(self)
        low_part_layout = QHBoxLayout(self)
        
        control_output_layout.addWidget(self.controller)
        control_output_layout.addWidget(self.output)
        low_part_layout.addLayout(control_output_layout)
        low_part_layout.addWidget(self.serial_monitor)
        
        layout.addWidget(self.connection)
        layout.addWidget(self.graph_plotter)
        layout.addLayout(low_part_layout)
        