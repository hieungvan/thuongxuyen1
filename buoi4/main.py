import sys
import sympy as sp
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QComboBox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MathApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ứng dụng hỗ trợ môn Giải tích')

        # Layout chính
        layout = QVBoxLayout()

        # Ô nhập phương trình
        self.equation_input = QLineEdit(self)
        self.equation_input.setPlaceholderText(
            'Nhập phương trình (ví dụ: x**2 + 2*x + 1)')
        layout.addWidget(self.equation_input)

        # ComboBox chọn loại tính toán
        self.operation_combo = QComboBox(self)
        self.operation_combo.addItems(
            ['Đạo hàm', 'Tích phân', 'Nguyên hàm', 'Vẽ đồ thị'])
        layout.addWidget(self.operation_combo)

        # Nút tính toán
        self.calculate_button = QPushButton('Tính', self)
        self.calculate_button.clicked.connect(self.calculate)
        layout.addWidget(self.calculate_button)

        # Kết quả hiển thị
        self.result_label = QLabel('Kết quả sẽ hiển thị ở đây', self)
        layout.addWidget(self.result_label)

        # Canvas để vẽ đồ thị
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def calculate(self):
        expr = self.equation_input.text()
        operation = self.operation_combo.currentText()

        x = sp.symbols('x')
        try:
            # Chuyển biểu thức chuỗi thành biểu thức toán học
            equation = sp.sympify(expr)
            if operation == 'Đạo hàm':
                result = sp.diff(equation, x)
                self.result_label.setText(f'Đạo hàm: {result}')
            elif operation == 'Tích phân':
                # Tích phân từ 0 đến 1 (có thể thay đổi)
                result = sp.integrate(equation, (x, 0, 1))
                self.result_label.setText(f'Tích phân từ 0 đến 1: {result}')
            elif operation == 'Nguyên hàm':
                result = sp.integrate(equation, x)
                self.result_label.setText(f'Nguyên hàm: {result}')
            elif operation == 'Vẽ đồ thị':
                self.plot_graph(equation)
        except Exception as e:
            self.result_label.setText(f'Lỗi: {e}')

    def plot_graph(self, equation):
        x_vals = range(-10, 11)
        y_vals = [equation.subs('x', x) for x in x_vals]
        self.ax.clear()
        self.ax.plot(x_vals, y_vals)
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MathApp()
    window.show()
    sys.exit(app.exec_())
