import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QComboBox, QFormLayout, QHBoxLayout
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
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

        # Form nhập các thông số
        self.form_layout = QFormLayout()  # Khởi tạo form layout trước
        self.param_inputs = {}

        # Gọi update_shape_list sau khi form_layout đã được khởi tạo
        self.update_shape_list()  # Cập nhật danh sách hình dựa vào 2D/3D
        self.layout.addWidget(self.shape_combo)
        self.shape_combo.currentIndexChanged.connect(self.update_form)

        self.layout.addLayout(self.form_layout)

        # Nút tính toán
        self.calculate_button = QPushButton('Tính Toán', self)
        self.calculate_button.clicked.connect(self.calculate)
        self.layout.addWidget(self.calculate_button)

        # Nút vẽ hình
        self.draw_button = QPushButton('Vẽ Hình', self)
        self.draw_button.clicked.connect(self.draw_shape)
        self.layout.addWidget(self.draw_button)

        # Hiển thị kết quả
        self.result_label = QLabel('Kết quả sẽ hiển thị ở đây', self)
        self.layout.addWidget(self.result_label)

        # Canvas để vẽ hình
        # Ban đầu không cần projection 3D
        self.figure, self.ax = plt.subplots(subplot_kw={"projection": None})
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)

    def update_shape_list(self):
        dimension = self.dimension_combo.currentText()
        self.shape_combo.clear()

        if dimension == '2D':
            self.shape_combo.addItems(
                ['Hình Vuông', 'Hình Chữ Nhật', 'Tam Giác', 'Hình Tròn', 'Tứ Giác'])
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

        # Tạo các ô nhập cho mỗi loại hình
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
        elif shape == 'Tứ Giác':
            self.param_inputs['Cạnh a'] = QLineEdit(self)
            self.param_inputs['Cạnh b'] = QLineEdit(self)
            self.param_inputs['Cạnh c'] = QLineEdit(self)
            self.param_inputs['Cạnh d'] = QLineEdit(self)
            self.form_layout.addRow('Cạnh a:', self.param_inputs['Cạnh a'])
            self.form_layout.addRow('Cạnh b:', self.param_inputs['Cạnh b'])
            self.form_layout.addRow('Cạnh c:', self.param_inputs['Cạnh c'])
            self.form_layout.addRow('Cạnh d:', self.param_inputs['Cạnh d'])
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

    def calculate(self):
        shape = self.shape_combo.currentText()

        try:
            if shape == 'Hình Vuông':
                side = float(self.param_inputs['Cạnh'].text())
                perimeter = 4 * side
                area = side ** 2
                self.result_label.setText(
                    f'Chu vi: {perimeter}, Diện tích: {area}')
            elif shape == 'Hình Chữ Nhật':
                length = float(self.param_inputs['Chiều dài'].text())
                width = float(self.param_inputs['Chiều rộng'].text())
                perimeter = 2 * (length + width)
                area = length * width
                self.result_label.setText(
                    f'Chu vi: {perimeter}, Diện tích: {area}')
            elif shape == 'Tam Giác':
                a = float(self.param_inputs['Cạnh a'].text())
                b = float(self.param_inputs['Cạnh b'].text())
                c = float(self.param_inputs['Cạnh c'].text())
                perimeter = a + b + c
                s = perimeter / 2
                area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
                self.result_label.setText(
                    f'Chu vi: {perimeter}, Diện tích: {area}')
            elif shape == 'Hình Tròn':
                radius = float(self.param_inputs['Bán kính'].text())
                perimeter = 2 * 3.1416 * radius
                area = 3.1416 * radius ** 2
                self.result_label.setText(
                    f'Chu vi: {perimeter}, Diện tích: {area}')
            elif shape == 'Hình Cầu':
                radius = float(self.param_inputs['Bán kính'].text())
                surface_area = 4 * 3.1416 * radius ** 2
                volume = (4 / 3) * 3.1416 * radius ** 3
                self.result_label.setText(
                    f'Diện tích: {surface_area}, Thể tích: {volume}')
            elif shape == 'Hình Trụ':
                radius = float(self.param_inputs['Bán kính'].text())
                height = float(self.param_inputs['Chiều cao'].text())
                surface_area = 2 * 3.1416 * radius * (radius + height)
                volume = 3.1416 * radius ** 2 * height
                self.result_label.setText(
                    f'Diện tích: {surface_area}, Thể tích: {volume}')
            elif shape == 'Hình Nón':
                radius = float(self.param_inputs['Bán kính'].text())
                height = float(self.param_inputs['Chiều cao'].text())
                surface_area = 3.1416 * radius * \
                    (radius + (radius**2 + height**2) ** 0.5)
                volume = (1 / 3) * 3.1416 * radius ** 2 * height
                self.result_label.setText(
                    f'Diện tích: {surface_area}, Thể tích: {volume}')
            elif shape == 'Hộp Chữ Nhật':
                length = float(self.param_inputs['Chiều dài'].text())
                width = float(self.param_inputs['Chiều rộng'].text())
                height = float(self.param_inputs['Chiều cao'].text())
                surface_area = 2 * (length * width + width *
                                    height + length * height)
                volume = length * width * height
                self.result_label.setText(
                    f'Diện tích: {surface_area}, Thể tích: {volume}')
        except ValueError:
            self.result_label.setText("Vui lòng nhập đúng giá trị.")

    def draw_shape(self):
        shape = self.shape_combo.currentText()

        # Xóa hình cũ trước khi vẽ hình mới
        self.ax.clear()

        if self.dimension_combo.currentText() == '2D':
            self.ax.set_projection(None)  # Đặt lại projection cho 2D
            if shape == 'Hình Vuông':
                side = float(self.param_inputs['Cạnh'].text())
                self.ax.add_patch(
                    Rectangle((0, 0), side, side, fill=None, edgecolor='r'))
                self.ax.set_xlim([0, side + 1])
                self.ax.set_ylim([0, side + 1])
            elif shape == 'Hình Chữ Nhật':
                length = float(self.param_inputs['Chiều dài'].text())
                width = float(self.param_inputs['Chiều rộng'].text())
                self.ax.add_patch(
                    Rectangle((0, 0), length, width, fill=None, edgecolor='b'))
                self.ax.set_xlim([0, length + 1])
                self.ax.set_ylim([0, width + 1])
            elif shape == 'Tam Giác':
                a = float(self.param_inputs['Cạnh a'].text())
                # tạm thời vẽ tam giác đều
                self.ax.add_patch(
                    Polygon([(0, 0), (a, 0), (a/2, a)], fill=None, edgecolor='g'))
                self.ax.set_xlim([0, a + 1])
                self.ax.set_ylim([0, a + 1])
            elif shape == 'Hình Tròn':
                radius = float(self.param_inputs['Bán kính'].text())
                self.ax.add_patch(
                    Circle((0, 0), radius, fill=None, edgecolor='purple'))
                self.ax.set_xlim([-radius - 1, radius + 1])
                self.ax.set_ylim([-radius - 1, radius + 1])

            self.ax.set_aspect('equal')

        elif self.dimension_combo.currentText() == '3D':
            self.ax = self.figure.add_subplot(
                111, projection='3d')  # Đặt lại projection cho 3D
            if shape == 'Hình Cầu':
                radius = float(self.param_inputs['Bán kính'].text())
                u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
                x = radius * np.cos(u) * np.sin(v)
                y = radius * np.sin(u) * np.sin(v)
                z = radius * np.cos(v)
                self.ax.plot_surface(x, y, z, color='b')
            elif shape == 'Hình Trụ':
                radius = float(self.param_inputs['Bán kính'].text())
                height = float(self.param_inputs['Chiều cao'].text())
                z = np.linspace(0, height, 50)
                theta = np.linspace(0, 2.*np.pi, 50)
                theta_grid, z_grid = np.meshgrid(theta, z)
                x_grid = radius*np.cos(theta_grid)
                y_grid = radius*np.sin(theta_grid)
                self.ax.plot_surface(x_grid, y_grid, z_grid, color='r')
            elif shape == 'Hình Nón':
                radius = float(self.param_inputs['Bán kính'].text())
                height = float(self.param_inputs['Chiều cao'].text())
                theta = np.linspace(0, 2.*np.pi, 50)
                r = np.linspace(0, radius, 50)
                R, Theta = np.meshgrid(r, theta)
                X = R * np.cos(Theta)
                Y = R * np.sin(Theta)
                Z = height - (height/radius) * R
                self.ax.plot_surface(X, Y, Z, color='g')
            elif shape == 'Hộp Chữ Nhật':
                length = float(self.param_inputs['Chiều dài'].text())
                width = float(self.param_inputs['Chiều rộng'].text())
                height = float(self.param_inputs['Chiều cao'].text())
                x = [0, 0, length, length, 0, 0, length, length]
                y = [0, width, width, 0, 0, width, width, 0]
                z = [0, 0, 0, 0, height, height, height, height]
                verts = [[x[0], y[0], z[0]], [x[1], y[1], z[1]],
                         [x[2], y[2], z[2]], [x[3], y[3], z[3]]]
                verts += [[x[4], y[4], z[4]], [x[5], y[5], z[5]],
                          [x[6], y[6], z[6]], [x[7], y[7], z[7]]]
                self.ax.add_collection3d(Poly3DCollection(
                    [verts], color='cyan', alpha=0.6))

        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GeometryApp()
    window.show()
    sys.exit(app.exec_())
