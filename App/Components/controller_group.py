from PySide6.QtWidgets import ( # type: ignore
    QGroupBox,
    QLabel,
    QSpinBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QDoubleSpinBox,
    QFormLayout,
)

from Components.duration_timer import DurationInputWidget
from Components.stopwatch_siplay import StopwatchDisplayWidget

class ControllerGroup(QGroupBox):

    def __init__(self, daq_worker, graph_plotter, logger):
        super().__init__("Controller")

        self.daq_worker = daq_worker
        self.graph_plotter = graph_plotter
        self.logger = logger
        main_layout = QHBoxLayout(self)

        # -----------------------
        # Stopwatch worker
        # -----------------------
        self.stopwatch = StopwatchDisplayWidget() 
        
        
        # -----------------------
        # Input Signal
        # -----------------------
        input_layout = QHBoxLayout()

        lbl_input = QLabel("Input Signal:")
        self.spin_signal = QSpinBox()
        self.spin_signal.setRange(1, 5)
        self.spin_signal.setValue(1)
        self.spin_signal.setSingleStep(1)

        # -----------------------
        # Timer Duration
        # -----------------------
        self.timer = DurationInputWidget()
        
        
        # -----------------------
        # Measure Button
        # -----------------------
        self.btn_measure = QPushButton("Measure")
        self.btn_measure.clicked.connect(
            lambda: (self.daq_worker.start_with_timer(self.timer.total_seconds()), self.timer.start_countdown())
        )
        self.btn_start = QPushButton("Start")
        self.btn_start.clicked.connect(
            lambda: (self.daq_worker.start_continuous(), self.stopwatch.start())
        )
        # self.btn_start.clicked.connect(self.start_system)
        
        self.btn_stop = QPushButton("Stop")
        self.btn_stop.clicked.connect(
            lambda: (self.daq_worker.stop(), self.stopwatch.stop(), self.stopwatch.reset())
        )
        # self.btn_stop.clicked.connect(self.stop_system)
        
    
        
        
        # -----------------------
        # Layout Combine
        # -----------------------
        timer_layout = QHBoxLayout()
        timer_layout.addWidget(self.timer)
        measure_mode_layout = QVBoxLayout()
        measure_mode_layout.addWidget(self.btn_measure)
        measure_mode_layout.addLayout(timer_layout)
        
        start_stop_layout = QHBoxLayout()
        start_stop_layout.addWidget(self.btn_start)
        start_stop_layout.addWidget(self.btn_stop)
        continue_mode_layout = QVBoxLayout()
        continue_mode_layout.addLayout(start_stop_layout)
        continue_mode_layout.addWidget(self.stopwatch)
        
        main_layout.addLayout(input_layout)
        main_layout.addLayout(measure_mode_layout)
        main_layout.addLayout(continue_mode_layout)