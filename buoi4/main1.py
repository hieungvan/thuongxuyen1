import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QFormLayout, QLabel, QMessageBox
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np


class GeometryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ứng dụng Hỗ trợ Môn Hình Học')

        # Layout chính
        self.layout = QVBoxLayout()

        # Chọn 2D hay 3D
        self.dimension_combo = QComboBox(self)
        self.dimension_combo.addItems(['2D', '3D'])
        self.dimension_combo.currentIndexChanged.connect(
            self.update_shape_list)
        self.layout.addWidget(self.dimension_combo)

        # ComboBox chọn hình
        self.shape_combo = QComboBox(self)
        self.shape_combo.currentIndexChanged.connect(self.update_form)
        self.layout.addWidget(self.shape_combo)

        # Form nhập các thông số
        self.form_layout = QFormLayout()
        self.param_inputs = {}
        self.layout.addLayout(self.form_layout)

        # Nút vẽ hình
        self.draw_button = QPushButton('Vẽ Hình', self)
        self.draw_button.clicked.connect(self.open_draw_window)
        self.layout.addWidget(self.draw_button)

        # Label hiển thị chu vi và diện tích
        self.result_label = QLabel(self)
        self.layout.addWidget(self.result_label)

        self.setLayout(self.layout)
        self.update_shape_list()

    def update_shape_list(self):
        dimension = self.dimension_combo.currentText()
        self.shape_combo.clear()

        if dimension == '2D':
            self.shape_combo.addItems(
                ['Hình Vuông', 'Hình Chữ Nhật', 'Tam Giác', 'Hình Tròn'])
        elif dimension == '3D':
            self.shape_combo.addItems(
                ['Hình Cầu', 'Hình Trụ', 'Hình Nón', 'Hộp Chữ Nhật'])

        self.update_form()

    def update_form(self):
        # Xóa các ô nhập cũ
        for i in reversed(range(self.form_layout.count())):
            self.form_layout.itemAt(i).widget().deleteLater()

        # Lấy hình đã chọn
        shape = self.shape_combo.currentText()
        self.param_inputs.clear()

        if shape == 'Hình Vuông':
            self.param_inputs['Cạnh'] = QLineEdit(self)
            self.form_layout.addRow('Cạnh:', self.param_inputs['Cạnh'])
        elif shape == 'Hình Chữ Nhật':
            self.param_inputs['Chiều dài'] = QLineEdit(self)
            self.param_inputs['Chiều rộng'] = QLineEdit(self)
            self.form_layout.addRow(
                'Chiều dài:', self.param_inputs['Chiều dài'])
            self.form_layout.addRow(
                'Chiều rộng:', self.param_inputs['Chiều rộng'])
        elif shape == 'Tam Giác':
            self.param_inputs['Cạnh a'] = QLineEdit(self)
            self.param_inputs['Cạnh b'] = QLineEdit(self)
            self.param_inputs['Cạnh c'] = QLineEdit(self)
            self.form_layout.addRow('Cạnh a:', self.param_inputs['Cạnh a'])
            self.form_layout.addRow('Cạnh b:', self.param_inputs['Cạnh b'])
            self.form_layout.addRow('Cạnh c:', self.param_inputs['Cạnh c'])
        elif shape == 'Hình Tròn':
            self.param_inputs['Bán kính'] = QLineEdit(self)
            self.form_layout.addRow('Bán kính:', self.param_inputs['Bán kính'])
        elif shape == 'Hình Cầu':
            self.param_inputs['Bán kính'] = QLineEdit(self)
            self.form_layout.addRow('Bán kính:', self.param_inputs['Bán kính'])
        elif shape == 'Hình Trụ':
            self.param_inputs['Bán kính'] = QLineEdit(self)
            self.param_inputs['Chiều cao'] = QLineEdit(self)
            self.form_layout.addRow('Bán kính:', self.param_inputs['Bán kính'])
            self.form_layout.addRow(
                'Chiều cao:', self.param_inputs['Chiều cao'])
        elif shape == 'Hình Nón':
            self.param_inputs['Bán kính'] = QLineEdit(self)
            self.param_inputs['Chiều cao'] = QLineEdit(self)
            self.form_layout.addRow('Bán kính:', self.param_inputs['Bán kính'])
            self.form_layout.addRow(
                'Chiều cao:', self.param_inputs['Chiều cao'])
        elif shape == 'Hộp Chữ Nhật':
            self.param_inputs['Chiều dài'] = QLineEdit(self)
            self.param_inputs['Chiều rộng'] = QLineEdit(self)
            self.param_inputs['Chiều cao'] = QLineEdit(self)
            self.form_layout.addRow(
                'Chiều dài:', self.param_inputs['Chiều dài'])
            self.form_layout.addRow(
                'Chiều rộng:', self.param_inputs['Chiều rộng'])
            self.form_layout.addRow(
                'Chiều cao:', self.param_inputs['Chiều cao'])

    def open_draw_window(self):
        shape = self.shape_combo.currentText()
        if not self.validate_inputs():
            return  # If validation fails, stop the function

        if self.dimension_combo.currentText() == '2D':
            self.draw_2d(shape)
        else:
            self.draw_3d(shape)

    def validate_inputs(self):
        # Kiểm tra các giá trị có hợp lệ hay không (có phải số dương không)
        for label, input_field in self.param_inputs.items():
            try:
                value = float(input_field.text())
                if value <= 0:
                    raise ValueError
            except ValueError:
                self.show_error_message(f"Giá trị '{label}' phải là số dương.")
                return False
        return True

    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Lỗi nhập liệu")
        msg.setText(message)
        msg.exec_()

    def draw_2d(self, shape):
        self.figure, self.ax = plt.subplots()
        self.ax.clear()

        if shape == 'Hình Vuông':
            side = float(self.param_inputs['Cạnh'].text())
            self.ax.add_patch(
                Rectangle((0, 0), side, side, fill=None, edgecolor='r'))
            self.ax.set_xlim([0, side + 1])
            self.ax.set_ylim([0, side + 1])
            perimeter = 4 * side
            area = side ** 2

        elif shape == 'Hình Chữ Nhật':
            length = float(self.param_inputs['Chiều dài'].text())
            width = float(self.param_inputs['Chiều rộng'].text())
            self.ax.add_patch(
                Rectangle((0, 0), length, width, fill=None, edgecolor='b'))
            self.ax.set_xlim([0, length + 1])
            self.ax.set_ylim([0, width + 1])
            perimeter = 2 * (length + width)
            area = length * width

        elif shape == 'Tam Giác':
            a = float(self.param_inputs['Cạnh a'].text())
            b = float(self.param_inputs['Cạnh b'].text())
            c = float(self.param_inputs['Cạnh c'].text())

            # Kiểm tra tam giác hợp lệ
            if a + b <= c or a + c <= b or b + c <= a:
                self.show_error_message(
                    "Các cạnh đã nhập không tạo thành tam giác hợp lệ.")
                return

            # Vẽ tam giác vuông hoặc tam giác thường
            if a**2 + b**2 == c**2:  # Tam giác vuông
                self.ax.add_patch(
                    Polygon([(0, 0), (a, 0), (0, b)], fill=None, edgecolor='g'))
                self.ax.set_xlim([0, max(a, b) + 1])
                self.ax.set_ylim([0, max(a, b) + 1])
            else:  # Tam giác thường
                self.ax.add_patch(Polygon(
                    [(0, 0), (a, 0), (a / 2, np.sqrt(b**2 - (a / 2)**2))], fill=None, edgecolor='g'))
                self.ax.set_xlim([0, max(a, b) + 1])
                self.ax.set_ylim([0, max(a, b) + 1])

            perimeter = a + b + c
            s = (a + b + c) / 2
            area = (s * (s - a) * (s - b) * (s - c)) ** 0.5

        elif shape == 'Hình Tròn':
            radius = float(self.param_inputs['Bán kính'].text())
            self.ax.add_patch(Circle((0, 0), radius, fill=None, edgecolor='r'))
            self.ax.set_xlim([-radius - 1, radius + 1])
            self.ax.set_ylim([-radius - 1, radius + 1])
            perimeter = 2 * np.pi * radius
            area = np.pi * radius ** 2

        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

        self.display_results(perimeter, area)

    def draw_3d(self, shape):
        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(111, projection='3d')
        self.ax.clear()

        if shape == 'Hình Cầu':
            radius = float(self.param_inputs['Bán kính'].text())
            phi, theta = np.mgrid[0:2 * np.pi:50j, 0:np.pi:25j]
            x = radius * np.sin(theta) * np.cos(phi)
            y = radius * np.sin(theta) * np.sin(phi)
            z = radius * np.cos(theta)
            self.ax.plot_surface(x, y, z, color='b')
            volume = 4 / 3 * np.pi * radius ** 3
            surface_area = 4 * np.pi * radius ** 2

        elif shape == 'Hình Trụ':
            radius = float(self.param_inputs['Bán kính'].text())
            height = float(self.param_inputs['Chiều cao'].text())
            z = np.linspace(0, height, 50)
            theta = np.linspace(0, 2 * np.pi, 50)
            theta_grid, z_grid = np.meshgrid(theta, z)
            x_grid = radius * np.cos(theta_grid)
            y_grid = radius * np.sin(theta_grid)
            self.ax.plot_surface(x_grid, y_grid, z_grid, color='r')
            volume = np.pi * radius ** 2 * height
            surface_area = 2 * np.pi * radius * (radius + height)

        elif shape == 'Hình Nón':
            radius = float(self.param_inputs['Bán kính'].text())
            height = float(self.param_inputs['Chiều cao'].text())
            z = np.linspace(0, height, 50)
            theta = np.linspace(0, 2 * np.pi, 50)
            theta_grid, z_grid = np.meshgrid(theta, z)
            x_grid = radius * (1 - z_grid / height) * np.cos(theta_grid)
            y_grid = radius * (1 - z_grid / height) * np.sin(theta_grid)
            self.ax.plot_surface(x_grid, y_grid, z_grid, color='g')
            volume = (1 / 3) * np.pi * radius ** 2 * height
            surface_area = np.pi * radius * \
                (radius + (radius ** 2 + height ** 2) ** 0.5)

        elif shape == 'Hộp Chữ Nhật':
            length = float(self.param_inputs['Chiều dài'].text())
            width = float(self.param_inputs['Chiều rộng'].text())
            height = float(self.param_inputs['Chiều cao'].text())
            points = np.array([[0, 0, 0], [length, 0, 0], [length, width, 0], [0, width, 0],
                               [0, 0, height], [length, 0, height], [length, width, height], [0, width, height]])
            vertices = [[points[j] for j in [0, 1, 2, 3]], [points[j] for j in [4, 5, 6, 7]],
                        [points[j] for j in [0, 1, 5, 4]], [points[j]
                                                            for j in [2, 3, 7, 6]],
                        [points[j] for j in [0, 3, 7, 4]], [points[j] for j in [1, 2, 6, 5]]]
            self.ax.add_collection3d(Poly3DCollection(
                vertices, facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))
            volume = length * width * height
            surface_area = 2 * (length * width + length *
                                height + width * height)

        self.ax.set_box_aspect([1, 1, 1])  # Aspect ratio is 1:1:1
        plt.show()

        self.display_results(volume, surface_area)

    def display_results(self, val1, val2):
        if self.dimension_combo.currentText() == '2D':
            self.result_label.setText(
                f"Chu vi: {val1:.2f}, Diện tích: {val2:.2f}")
        else:
            self.result_label.setText(
                f"Thể tích: {val1:.2f}, Diện tích bề mặt: {val2:.2f}")

    def clear_inputs(self):
        for key in self.param_inputs:
            self.param_inputs[key].clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GeometryApp()
    ex.show()
    sys.exit(app.exec_())
