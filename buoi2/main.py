from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QGridLayout, QVBoxLayout, QHBoxLayout, QStackedWidget, QLineEdit,QWidget, QLayout, QSpacerItem, QSizePolicy,QMessageBox, QFileDialog, QTableWidget, QTableWidgetItem, QComboBox
from PyQt6.QtCore import Qt
import numpy as np
import pandas as pd

class MainWindow (QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.tin_hieu_main = False
        self.tin_hieu_table = False
        self.tin_hieu_space_table = False
        self.gui_main()
        
        
    def gui_main(self):
        self.setWindowTitle("Numpy PMNMN")
        self.setGeometry(100, 100, 600, 400)

        self.label_toan = QLabel("Điểm toán")
        self.label_toan.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_toan.setMaximumSize(180, 40)
        self.edt_toan = QLineEdit()
        self.edt_toan.setMaximumSize(180, 40)
        
        self.label_van = QLabel("Điểm văn")
        self.label_van.setMaximumSize(180, 40)
        self.label_van.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edt_van = QLineEdit()
        self.edt_van.setMaximumSize(180, 40)
        
        self.btn_xn = QPushButton("Xác nhận")
        self.btn_xn.setMaximumSize(100, 50)
        self.btn_clear = QPushButton("Clear")
        self.btn_clear.setMaximumSize(100, 50)
        self.btn_import = QPushButton("Import")
        self.combo_option = self.add_option(["Không", "Tăng dần", "Giảm dần", "TB lớn nhất", "TB nhỏ nhất"])
        self.btn_export = QPushButton("Export")
        
        self.lb_diemTB = QLabel("Điểm TB")
        self.lb_diemTB.setAlignment(Qt.AlignmentFlag.AlignCenter)