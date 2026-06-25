from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QStyle, QApplication, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QIcon
from GUI.gui_component import create_text, create_combobox, create_button, MplCanvas, graph_display
from Components.serial_connection import port_detection
from functools import partial
from Components.listeners import *

class Main_Page(QWidget):
    def __init__(self):
        super().__init__()
        self.config:dict={}
        self.baud_list:list = ['9600', '19200', '38400', '57600', '115200']
        
        #Connection
        self.comm_label = create_text(self, 'Com Port')
        comm_listener = partial(combo_listener, self.config, 'Comm_Port')
        self.comm_list = create_combobox(self.config, 'Comm_Port', comm_listener)
        self.refresh_icon = QApplication.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload) # pyright: ignore[reportOptionalMemberAccess]
        refresh_comm = partial(port_detection, self.comm_list)
        self.refresh_comm_btn = create_button(button_function=refresh_comm, icon_file=self.refresh_icon, size=[25,25])
        self.baudrate_label = create_text(self, 'Baud_rate')
        baudrate_listener = partial(combo_listener, self.config, 'Baud_rate')
        self.baudrate_list=create_combobox(self.config, 'Baudrate_List', baudrate_listener, self.baud_list)
        
        self.spacer = QSpacerItem(100, 100, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        
        
        #Graph
        self.graph = MplCanvas(self)
        # self.graph.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        # self.graph.draw()
        
        # graph_layout = QVBoxLayout(self)
        # graph_panel = graph_display()
        
        # graph_layout.addWidget(graph_panel)
        # graph_panel.setMaximumSize(700, 300)
        # graph_layout.setSizeConstraints(100, 100)
        
        
        
        
        
        comm_layout = QGridLayout(self)
        comm_layout.addWidget(self.comm_label, 0, 0)
        comm_layout.addWidget(self.comm_list, 0, 1)
        comm_layout.addWidget(self.refresh_comm_btn, 0, 2)
        comm_layout.addWidget(self.baudrate_label, 0, 3)
        comm_layout.addWidget(self.baudrate_list, 0, 4)
        comm_layout.addItem(self.spacer, 0, 5)
        
        
        
        # main_layout = QHBoxLayout(self)
        # main_layout.addLayout(comm_layout)
        # main_layout.addLayout(graph_layout)
        
