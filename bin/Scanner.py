from PyQt5.QtWidgets import QWidget, QVBoxLayout, QDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
import cv2
import numpy as np
import os
import json
from pyzbar.pyzbar import decode
from PyQt5.QtWidgets import QWidget, QLabel,QVBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt
from bin.Config import AppConfig as AC


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scan the QR code")
        self.display_width = 1280
        self.display_height = 720

        self.image_label = QLabel(self)
        self.image_label.resize(self.display_width, self.display_height)
        self.text_label = QLabel('Webcam')

        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.text_label)
        self.setLayout(vbox)


        cam_data = 0
        if os.path.exists(AC.SETTINGS_JSON_PATH):
            with open(AC.SETTINGS_JSON_PATH, "r") as jf:
                cam_data = json.load(jf)
                cam_data = cam_data["cam_input_id"]
            
        self.capture = cv2.VideoCapture(cam_data)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.read_qr_code)
        self.timer.start(100)  # Set the interval in milliseconds (e.g., 100ms)

    def read_qr_code(self):
        success, img = self.capture.read()
        if success:
            for barcode in decode(img):
                my_data = barcode.data.decode("utf-8")
                print(my_data)

                color = (0, 0, 255)
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(img, [pts], True, color, 3)

                pts2 = barcode.rect
                text_on_display = f"{my_data}"
                cv2.putText(img, text_on_display, (pts2[0], pts2[1]),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                self.qr_code_read(my_data)

            qt_img = self.convert_cv_qt(img)
            self.image_label.setPixmap(qt_img)

    def qr_code_read(self, qr_data):
        print(f"QR Code Read: {qr_data}")
        AC.QR_SCANNER = qr_data
       
        self.timer.stop()  # Stop the timer to prevent further scanning
        self.capture.release()  # Release the webcam capture
        self.parent().close() 

    def convert_cv_qt(self, img):
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(
            rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(
            self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


class QRScanner(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QR Code Scanner")
        self.setWindowIcon(QIcon(AC.LOGO_ICO_PATH))
        self.setGeometry(200, 200, 800, 600)

        self.app = App()

        vbox = QVBoxLayout()
        vbox.addWidget(self.app)
        self.setLayout(vbox)

    def closeEvent(self, event):
        self.app.capture.release()
        event.accept()
