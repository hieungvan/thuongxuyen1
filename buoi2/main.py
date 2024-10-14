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

        
        if self.tin_hieu_main == False:
            self.btn_xn.clicked.connect(self.xac_nhan_thong_tin)
            self.btn_clear.clicked.connect(self.clear_data)
            self.btn_import.clicked.connect(self.open_dialog_file_import)
            self.combo_option.currentTextChanged.connect(self.open_combo_option)
            
            self.btn_export.clicked.connect(self.open_dialog_file_export)
            self.tin_hieu_main = True
        
        self.layoutBTN = QHBoxLayout()
        self.layoutBTN.addWidget(self.btn_xn)
        self.layoutBTN.addWidget(self.btn_clear)
        
        
        self.vLayoutInput = QVBoxLayout()
        
        self.vLayoutInput.setSpacing(1)
        self.vLayoutInput.addWidget(self.label_toan)
        self.vLayoutInput.addWidget(self.edt_toan)
        self.vLayoutInput.addWidget(self.label_van)
        self.vLayoutInput.addWidget(self.edt_van)
        self.vLayoutInput.addWidget(self.lb_diemTB)
        self.vLayoutInput.addLayout(self.layoutBTN)
        self.vLayoutInput.addWidget(self.btn_import)
        self.vLayoutInput.addWidget(self.combo_option)
        self.vLayoutInput.addWidget(self.btn_export)
        
        
        # HSpace và VSpace dùng addItem
        
        self.Hspace = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.Vspace = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        
        self.hLayout = QHBoxLayout()
        self.hLayout.addItem(self.Hspace)
        #Layout dùng addlayout
        self.hLayout.addLayout(self.vLayoutInput)
        self.hLayout.addItem(self.Hspace)
        
        self.vLayoutFinal = QVBoxLayout()
        self.vLayoutFinal.setSpacing(1)
        self.vLayoutFinal.addItem(self.Vspace)
        self.vLayoutFinal.addLayout(self.hLayout)
        self.vLayoutFinal.addItem(self.Vspace)
        
        # Tạp một QWidget trung tâm
        self.central_widget = QWidget()
        
        self.central_widget.setLayout(self.vLayoutFinal)
        self.setCentralWidget(self.central_widget)
    
    def add_option(self, listItem):
        combo_box = QComboBox()
        for item in listItem:
            combo_box.addItem(item)
        return combo_box
    
    def open_combo_option(self):
        
        if self.tin_hieu_table == True:
            itemChoosed = self.combo_option.currentText()
            # Gọi các hàm sắp xếp
            print(itemChoosed)
            
            if itemChoosed == "Tăng dần":
                data_diem = pd.read_csv("data_diem.csv")
                self.data = sap_xep_tang_dan(data_diem, "TB")
                self.show_table_widget(self.data)
            elif itemChoosed == "Giảm dần":
                data_diem = pd.read_csv("data_diem.csv")
                self.data = sap_xep_giam_dan(data_diem, "TB")
                self.show_table_widget(self.data)
            elif itemChoosed == "TB lớn nhất":
                data_diem = pd.read_csv("data_diem.csv")
                self.data= hoc_sinh_diem_TB_cao_nhat(data_diem)
                self.show_table_widget(self.data)
            elif itemChoosed == "TB nhỏ nhất":
                data_diem = pd.read_csv("data_diem.csv")
                self.data= hoc_sinh_diem_TB_thap_nhat(data_diem)
                self.show_table_widget(self.data)
            else:
                data_diem = pd.read_csv("data_diem.csv")
                self.show_table_widget(data_diem)
        else:
            self.show_message("Chưa có dữ liệu")
            
    def xac_nhan_thong_tin(self):
        # try:
        strToan = self.edt_toan.text()
        strVan = self.edt_van.text()
        if (strToan != '' and strVan != ''):
            diemToan = float(strToan)
            diemVan = float(strVan)
            diemTB = np.sum([diemToan, diemVan])/2
            
            contentMess = f"Toán {diemToan} - Văn {diemVan}"
            self.show_message(contentMess)
            if self.tin_hieu_table == False:
                self.show_message("Bạn phải import dữ liệu để hiển thị")
                self.lb_diemTB.setText(f"TB: {diemTB}")
            
            else:
                
                self.lb_diemTB.setText(f"TB: {diemTB}")
                self.oldData = pd.read_csv("data_diem.csv")
                self.insert_new_data(self.oldData, pd.DataFrame([[diemToan, diemVan, diemTB]], columns=["Toán", "Văn", "TB"]))
        else: 
            self.show_message("Vui lòng nhập điểm")
        
            
    
    def clear_data(self):
        self.edt_toan.clear()
        self.edt_van.clear()
        
    def show_message(self, content):
        # Tạo QMessageBox
        msg_box = QMessageBox()

        # Thiết lập tiêu đề và nội dung
        msg_box.setWindowTitle("Thông báo")
        msg_box.setText(str(content))
        msg_box.setIcon(QMessageBox.Icon.Question)  
        msg_box.exec()
    
    def show_table_widget(self, dataFrame):
        label = dataFrame.columns
        numberRow = len(dataFrame)
        numberColumn = len(label)
        
        
        TBMax = np.max(dataFrame["TB"])
        print("Điểm TB Max: ", TBMax)
        TBMin = np.min(dataFrame["TB"])
        print("Điểm TB Min: ", TBMin)
        
        

        # Kiểm tra xem bảng đã tồn tại chưa, nếu có thì xóa bảng cũ
        # Tạo bảng mới với số dòng và số cột tương ứng
        self.qTable = QTableWidget(numberRow, numberColumn)
        self.qTable.setHorizontalHeaderLabels([str(lbl) for lbl in label])

        # Điền dữ liệu vào bảng
        for row in range(numberRow):
            for col in range(numberColumn):
                data_index = dataFrame.iloc[row][col]
                item = QTableWidgetItem(str(data_index))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Căn giữa
                self.qTable.setItem(row, col, item)
                self.qTable.setColumnWidth(col, 100)

        # Thiết lập chiều rộng của bảng dựa trên số cột
        total_width = numberColumn * 100
        self.qTable.setFixedWidth(total_width+10)
        
        if self.tin_hieu_table == False: # cập nhật lần 1
            self.oldTable = self.qTable
            self.lbTBMax = QLabel()
            self.lbTBMax.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.lbTBMin = QLabel()
            self.lbTBMin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.HLayoutTableFinal = QHBoxLayout()
            self.HLayoutTableFirst = QHBoxLayout()
            self.VLayoutTBMinMax = QVBoxLayout()
            
            self.HLayoutTableFirst.addWidget(self.oldTable)
            self.HLayoutTableFinal.addItem(self.Hspace)
            self.HLayoutTableFinal.addLayout(self.HLayoutTableFirst)
            self.HLayoutTableFinal.addItem(self.Hspace)
            
            self.VLayoutTBMinMax.addWidget(self.lbTBMin)
            self.VLayoutTBMinMax.addWidget(self.lbTBMax)
            
            self.lbTBMax.setText(f"Điểm TB Max: {TBMax}")
            self.lbTBMin.setText(f"Điểm TB Min: {TBMin}")
            self.vLayoutInput.addLayout(self.VLayoutTBMinMax)
            self.vLayoutFinal.addLayout(self.HLayoutTableFinal)
            self.vLayoutFinal.addItem(self.Vspace)
            self.tin_hieu_table = True

        if self.oldTable != self.qTable:
            self.HLayoutTableFirst.removeWidget(self.oldTable)
            
            print("--: Replace")
            self.oldTable = self.qTable
            self.HLayoutTableFirst.addWidget(self.oldTable)
            self.lbTBMax.setText(f"Điểm TB Max: {TBMax}")
            self.lbTBMin.setText(f"Điểm TB Min: {TBMin}")
        
    def insert_new_data(self, oldData, newData):
        self.dataInsert = pd.concat([newData, oldData])
        print(self.dataInsert)
        self.show_table_widget(self.dataInsert)
        self.data = self.dataInsert
        self.dataInsert.to_csv("data_diem.csv", index=False)
        
        
    def open_dialog_file_import(self):
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

    def open_dialog_file_export(self):
        
        try:
            fileName, _ = QFileDialog().getSaveFileName(self, "Lưu file")
            
            if len(fileName) > 0:
                lastPath = fileName.split(".")[-1]
                print("Last: ", lastPath)
                if lastPath not in ["csv", "xlsx"]:
                    self.show_message("Chỉ file .csv và .xlsx")
                else:
                    self.data.to_csv(fileName, index=False)
                    self.show_message("Lưu thành công")
        except:
            self.show_message("Chưa có dữ liệu")

              
def check_data_import(dataFrame):
    label = dataFrame.columns
    
    if len(label) != 3 or "Toán" not in label or "Văn" not in label or "TB" not in label:
        return False
    else:
        return True

def sap_xep_tang_dan(data, column_name):
    data_tang_dan = data.sort_values(by=[column_name])
    return data_tang_dan
def sap_xep_giam_dan(data, column_name):
    data_giam_dan = data.sort_values(by=[column_name],ascending = False)
    return data_giam_dan
            
def hoc_sinh_diem_TB_cao_nhat(data):
    max_TB = np.max(data["TB"])
    data_maxTB = data[data["TB"] == max_TB]
    return data_maxTB 

def hoc_sinh_diem_TB_thap_nhat(data):
    min_TB = np.min(data["TB"])
    data_minTB = data[data["TB"] == min_TB]
    return data_minTB

      
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()