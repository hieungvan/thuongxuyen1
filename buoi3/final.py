import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit, QHBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt
import os


class DiemThongKeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Thống kê và Quản lý điểm môn Python'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 600, 300)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        

        # Nhãn nhập dữ liệu sinh viên mới
        self.labelNhap = QLabel('NHẬP DỮ LIỆU SINH VIÊN MỚI', self)
        self.labelNhap.setAlignment(Qt.AlignCenter)  # Căn giữa nhãn
        layout.addWidget(self.labelNhap)

        # Layout nhập dữ liệu
        inputLayout = QHBoxLayout()

        self.lopInput = QLineEdit(self)
        self.lopInput.setPlaceholderText('Lớp')
        inputLayout.addWidget(self.lopInput)

        self.hoTenInput = QLineEdit(self)
        self.hoTenInput.setPlaceholderText('Họ và tên')
        inputLayout.addWidget(self.hoTenInput)

        self.maSVInput = QLineEdit(self)
        self.maSVInput.setPlaceholderText('Mã sinh viên')
        inputLayout.addWidget(self.maSVInput)

        self.diemInput = QLineEdit(self)
        self.diemInput.setPlaceholderText('Điểm')
        inputLayout.addWidget(self.diemInput)

        layout.addLayout(inputLayout)

        # Nút thêm dữ liệu sinh viên
        self.btnThemSV = QPushButton('Thêm sinh viên và lưu vào CSV', self)
        # Thay đổi kích thước cho hợp lý
        self.btnThemSV.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.btnThemSV, alignment=Qt.AlignCenter)

        # Nút hiện bảng thông tin sinh viên
        self.btnHienBang = QPushButton('Hiện bảng thông tin sinh viên', self)
        self.btnHienBang.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.btnHienBang, alignment=Qt.AlignCenter)

        # Nút mở file CSV
        self.btnOpenFile = QPushButton('Mở file CSV', self)
        self.btnOpenFile.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.btnOpenFile, alignment=Qt.AlignCenter)

        # Nút thống kê lớp có nhiều điểm A nhất
        self.btnThongKe = QPushButton('Thống kê lớp có nhiều điểm A nhất', self)
        self.btnThongKe.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.btnThongKe, alignment=Qt.AlignCenter)

        # Nút vẽ đồ thị phân bố điểm
        self.btnVeDoThi = QPushButton('Vẽ biểu đồ phân bố điểm cho từng lớp', self)
        self.btnVeDoThi.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.btnVeDoThi, alignment=Qt.AlignCenter)

        self.setLayout(layout)

        # Kết nối các nút với các hàm tương ứng
        self.btnThemSV.clicked.connect(self.themSinhVien)
        self.btnHienBang.clicked.connect(self.hienBangSinhVien)
        self.btnOpenFile.clicked.connect(self.openFileDialog)
        self.btnThongKe.clicked.connect(self.thongKeLop)
        self.btnVeDoThi.clicked.connect(self.veDoThiTheoTungLop)

    def openFileDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Mở file CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if fileName:
            self.fileName = fileName
            self.data = pd.read_csv(fileName)
            QMessageBox.information(self, "Thông báo", f'Đã chọn file: {fileName}')
        else:
            QMessageBox.warning(self, "Lỗi", "Chưa chọn file CSV.")

    def thongKeLop(self):
        if hasattr(self, 'data'):
            lop_a = self.data[self.data['Diem'] == 'A']
            thong_ke_lop = lop_a['Lop'].value_counts()

            if thong_ke_lop.empty:
                QMessageBox.warning(self, "Thông báo","Không có sinh viên nào đạt điểm A.")
            else:
                lop_nhieu_a_nhat = thong_ke_lop.idxmax()
                so_sv_dat_a = thong_ke_lop.max()

                QMessageBox.information(self, "Thông báo",f'Lớp có nhiều sinh viên đạt điểm A nhất: {lop_nhieu_a_nhat} ({so_sv_dat_a} sinh viên)')

                sv_dat_a = lop_a[lop_a['Lop'] == lop_nhieu_a_nhat]

                self.tableWindow = QWidget()
                self.tableWindow.setWindowTitle(f'Danh sách sinh viên đạt điểm A - Lớp {lop_nhieu_a_nhat}')
                self.tableWindow.setGeometry(100, 100, 600, 400)

                layout = QVBoxLayout()

                tableWidget = QTableWidget()
                tableWidget.setRowCount(len(sv_dat_a))
                tableWidget.setColumnCount(len(sv_dat_a.columns))
                tableWidget.setHorizontalHeaderLabels(sv_dat_a.columns)

                for i in range(len(sv_dat_a)):
                    for j in range(len(sv_dat_a.columns)):
                        tableWidget.setItem(i, j, QTableWidgetItem(str(sv_dat_a.iloc[i, j])))

                tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

                layout.addWidget(tableWidget)
                self.tableWindow.setLayout(layout)
                self.tableWindow.show()
        else:
            QMessageBox.warning(self, "Lỗi", "Chưa có dữ liệu sinh viên nào.")

    def hienBangSinhVien(self):
        if hasattr(self, 'data'):
            self.tableWindow = QWidget()
            self.tableWindow.setWindowTitle('Bảng thông tin sinh viên')
            self.tableWindow.setGeometry(100, 100, 600, 400)

            layout = QVBoxLayout()

            tableWidget = QTableWidget()
            tableWidget.setRowCount(len(self.data))
            tableWidget.setColumnCount(len(self.data.columns))
            tableWidget.setHorizontalHeaderLabels(self.data.columns)

            for i in range(len(self.data)):
                for j in range(len(self.data.columns)):
                    tableWidget.setItem(i, j, QTableWidgetItem(str(self.data.iloc[i, j])))

            tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            layout.addWidget(tableWidget)
            self.tableWindow.setLayout(layout)
            self.tableWindow.show()
        else:
            QMessageBox.warning(self, "Lỗi", "Chưa có dữ liệu sinh viên nào.")

    def themSinhVien(self):
        lop = self.lopInput.text()
        ho_ten = self.hoTenInput.text()
        ma_sv = self.maSVInput.text()
        diem = self.diemInput.text()

        if not lop or not ho_ten or not ma_sv or not diem:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return

        if not hasattr(self, 'fileName'):
            QMessageBox.warning(self, "Lỗi", "Chưa chọn file CSV.")
            return

        new_data = pd.DataFrame({
            'Lop': [lop],
            'HoTen': [ho_ten],
            'MaSV': [ma_sv],
            'Diem': [diem]
        })

        if os.path.exists(self.fileName):
            new_data.to_csv(self.fileName, mode='a', header=False, index=False)
        else:
            new_data.to_csv(self.fileName, index=False)

        QMessageBox.information(self, "Thành công", "Sinh viên đã được thêm vào file CSV.")

        self.lopInput.clear()
        self.hoTenInput.clear()
        self.maSVInput.clear()
        self.diemInput.clear()

        self.data = pd.read_csv(self.fileName)

    def veDoThiTheoTungLop(self):
        if hasattr(self, 'data'):
            ds_lop = self.data['Lop'].unique()
            for lop in ds_lop:
                lop_data = self.data[self.data['Lop'] == lop]
                thong_ke_diem = lop_data['Diem'].value_counts().reindex(['A', 'B+', 'B', 'C+', 'C', 'D+', 'D', 'F'], fill_value=0)

                plt.figure()
                thong_ke_diem.plot(kind='bar', color=[ 'blue', 'orange', 'green', 'red', 'purple', 'pink', 'gray', 'brown'])
                plt.title(f'Phân bố điểm lớp {lop}')
                plt.xlabel('Điểm')
                plt.ylabel('Số sinh viên')
                plt.xticks(rotation=0)
                plt.show()
        else:
            QMessageBox.warning(self, "Lỗi", "Chưa có dữ liệu sinh viên nào.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DiemThongKeApp()
    ex.show()
    sys.exit(app.exec_())
