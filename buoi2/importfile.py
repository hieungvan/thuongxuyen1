from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QGridLayout, QVBoxLayout, QHBoxLayout, QStackedWidget, QLineEdit, QWidget, QLayout, QSpacerItem, QSizePolicy, QMessageBox, QFileDialog, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
import numpy as np
import pandas as pd


def open_dialog_file(self):
    # Mở dialog chế độ chọn tệp
    self.filePath, _ = QFileDialog.getOpenFileName(self, "Chọn tệp")
    print('File đã chọn: ', self.filePath)
    self.filePath = self.filePath.replace("/", "//")

    if len(self.filePath) > 0:
        lastPath = self.filePath.split(".")[-1]

        if lastPath == 'csv':
            self.data = pd.read_csv(self.filePath)
            if check_data_import(self.data) == True:
                self.show_table_widget(self.data)
                self.combo_option.setCurrentText("Không")
            else:
                self.show_message("Chỉ có điểm Toán, Văn, TB")

        elif lastPath == "xlsx":
            self.data = pd.read_excel(self.filePath)
            if check_data_import(self.data) == True:
                self.show_table_widget(self.data)
            else:
                self.show_message("Chỉ có điểm Toán, Văn, TB")

        else:
            self.show_message("Không đúng file (xlsx, csv)")


def check_data_import(data):
    # Kiểm tra dữ liệu chỉ chứa các cột 'Toán', 'Văn', 'TB'
    required_columns = ['Toán', 'Văn', 'TB']
    return all(col in data.columns for col in required_columns)
