import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt

class ImageProcessor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.img = None
        self.processed_img = None

    def initUI(self):
        self.setWindowTitle('Image Processor')
        self.setGeometry(100, 100, 800, 600)  # Set window size

        # Labels to display images
        self.original_label = QLabel('Original Image')
        self.original_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_label.setFixedSize(400, 400)

        self.processed_label = QLabel('Processed Image')
        self.processed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.processed_label.setFixedSize(400, 400)

        # Buttons
        self.btn_open = QPushButton('Open Image')
        self.btn_open.clicked.connect(self.open_image)

        self.btn_blur = QPushButton('Blur Image')
        self.btn_blur.clicked.connect(self.apply_blur)

        self.btn_sharpen = QPushButton('Sharpen Image')
        self.btn_sharpen.clicked.connect(self.apply_sharpen)

        self.btn_bw = QPushButton('Black & White Image')
        self.btn_bw.clicked.connect(self.apply_bw)

        self.btn_bg_remove = QPushButton('Remove Background')
        self.btn_bg_remove.clicked.connect(self.remove_background)

        self.btn_save = QPushButton('Save Processed Image')
        self.btn_save.clicked.connect(self.save_image)

        # Layout for buttons
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.btn_open)
        button_layout.addWidget(self.btn_blur)
        button_layout.addWidget(self.btn_sharpen)
        button_layout.addWidget(self.btn_bw)
        button_layout.addWidget(self.btn_bg_remove)
        button_layout.addWidget(self.btn_save)
        
        # Add spacer to center the buttons
        button_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # Layout for images
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.original_label)
        image_layout.addWidget(self.processed_label)

        # Main layout to arrange image and buttons
        main_layout = QVBoxLayout()
        main_layout.addLayout(image_layout)
        main_layout.addLayout(button_layout)

        # Add spacer to center the layout
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def open_image(self):
        # Open file dialog to select image
        options = QFileDialog.Option.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Images (*.png *.jpg *.jpeg)', options=options)
        file_name = file_name.split('E:/Nam 4/Mã nguồn mở/B3/thuongxuyen1/buoi5_opencv/')[-1]
        print(file_name)
        if file_name:
            self.img = cv2.imread(file_name)
            if self.img is None:
                print("Error: Unable to load image.")
            else:
                self.display_image(self.img, self.original_label)

    def display_image(self, img, label):
        # Convert image to QImage and display in label
        height, width, channel = img.shape
        bytes_per_line = 3 * width
        q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(q_img)
        label.setPixmap(pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio))

    def apply_blur(self):
        if self.img is not None:
            kernel = np.ones((5, 5), np.float32) / 25.0
            self.processed_img = cv2.filter2D(self.img, -1, kernel)
            self.display_image(self.processed_img, self.processed_label)

    def apply_sharpen(self):
        if self.img is not None:
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            self.processed_img = cv2.filter2D(self.img, -1, kernel)
            self.display_image(self.processed_img, self.processed_label)

    def apply_bw(self):
        if self.img is not None:
            self.processed_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            self.processed_img = cv2.cvtColor(self.processed_img, cv2.COLOR_GRAY2BGR)  # Convert to BGR for consistency
            self.display_image(self.processed_img, self.processed_label)

    def remove_background(self):
        if self.img is not None:
            def onTrackbarChange(value):
                self.blk_thresh = value
                self.update_background_removal()  # Cập nhật kết quả khi thanh trượt thay đổi

            def valueScaling(value):
                min_value = 150
                max_value = 200
                new_min = 250
                new_max = 255
                scaled_value = (value - min_value) * (new_max - new_min) / (max_value - min_value) + new_min + 20
                return int(scaled_value)

            # Thiết lập ngưỡng ban đầu
            self.blk_thresh = 200
            scaled_thresh = valueScaling(self.blk_thresh)

            # Tạo cửa sổ và thanh trượt
            window_name = 'Background Removed'
            cv2.namedWindow(window_name)
            cv2.createTrackbar('Threshold', window_name, scaled_thresh, 150, onTrackbarChange)

            # Cập nhật ảnh khi giá trị thanh trượt thay đổi
            self.update_background_removal()

    def update_background_removal(self):
        if self.img is not None:
            # Chuyển ảnh sang grayscale và làm mờ
            gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)

            # Áp dụng ngưỡng
            _, threshold_img = cv2.threshold(blur, self.blk_thresh, 255, cv2.THRESH_BINARY)

            # Tạo mask ngược từ ảnh ngưỡng
            mask = 255 - threshold_img

            # Áp dụng mask lên ảnh gốc
            result = cv2.bitwise_and(self.img, self.img, mask=mask)

            # Hiển thị ảnh đã xử lý lên label
            self.processed_img = result
            self.display_image(self.processed_img, self.processed_label)

            # Hiển thị trong cửa sổ OpenCV (tuỳ chọn)
            cv2.imshow('Background Removed', result)





    def save_image(self):
        if self.processed_img is not None:
            file_name, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', 'PNG Files (*.png);;JPEG Files (*.jpg)')
            if file_name:
                cv2.imwrite(file_name, self.processed_img)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageProcessor()
    window.show()
    sys.exit(app.exec())
