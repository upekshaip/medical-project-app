import random
import string
import pyqrcode
import pyqrcode
import os
import math
import json
from bin.Config import AppConfig as AC
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import qrcode

class Helper:
    def __init__(self):
        pass

    def generate_code(self, type):
        chars = f"0123456789{string.ascii_lowercase}{string.ascii_uppercase}"
        chars_roles = f"0123456789{string.ascii_uppercase}"

        if type == "":
            # UID
            num = random.choices(chars, k=16)
            id = "".join(num)
            return id
        
        if type == "d":
            # doctor
            num = random.choices(chars_roles, k=10)
            id = "".join(num)
            id = "DR" + id
            return id

        if type == "e":
            # employee
            num = random.choices(chars_roles, k=10)
            id = "".join(num)
            id = "EM" + id
            return id
        
    def create_id(self, usercode):
        # Generate QR code
        url = pyqrcode.create(usercode)
        url.png(f'config/{usercode}-qr.png', scale=20)
        print("qr code created.")


    def generate_id(self, usercode, first_name, last_name):
        # Create QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(usercode)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_path = f"config/{usercode}-qr.png"
        qr_img.save(qr_path)

        # Load frame and QR Code images using PIL
        frame_path = f'config/frame.png'
        frame = Image.open(frame_path)
        qr_code = Image.open(qr_path)

        # Resize QR Code
        qr_code = qr_code.resize((640, 640))

        # Paste QR Code onto frame
        QR_LEFT = 60
        QR_UP = 300
        frame.paste(qr_code, (QR_LEFT, QR_UP))

        # Draw text on the image
        draw = ImageDraw.Draw(frame)
        font1 = ImageFont.truetype("arial.ttf", 100)
        font2 = ImageFont.truetype("arial.ttf", 75)
        font3 = ImageFont.truetype("arial.ttf", 45)

        # First name and last name
        draw.text((710, 380), f'{first_name} {last_name}', font=font1, fill=(0, 0, 0))

        # Usercode
        draw.text((710, 530), usercode, font=font2, fill=(0, 0, 0))

        draw.text((710, 700), AC.INSTITUTE_ADDRESS, font=font3, fill=(0, 0, 0))
        draw.text((710, 760), f"{AC.INSTITUTE_PHONE1} / {AC.INSTITUTE_PHONE2}", font=font3, fill=(0, 0, 0))
        draw.text((710, 820), AC.INSTITUTE_EMAIL, font=font3, fill=(0, 0, 0))


        # Draw polygon line
        border_width = -50
        polygon_coords = [
            (QR_LEFT - border_width, QR_UP - border_width),
            (QR_LEFT - border_width, QR_UP + qr_code.height + border_width),
            (QR_LEFT + qr_code.width + border_width, QR_UP + qr_code.height + border_width),
            (QR_LEFT + qr_code.width + border_width, QR_UP - border_width)
        ]
        draw.polygon(polygon_coords, outline=(0, 0, 0), width=4)

        # Save the final image
        os.remove(qr_path)

        today_date = datetime.now().strftime('%Y-%m-%d')
        self.create_sub_dir("id", today_date)

        my_path = f"id/{today_date}/{usercode}.png"
        frame.save(my_path)
        print("Process finished.")
        return my_path

    
    def overlay_images(self, user_id):
        today_date = datetime.now().strftime('%Y-%m-%d')
        self.create_sub_dir("id", today_date)
        background_image_path = "config/background.png"
        overlay_image_path = f"config/{user_id}-id.png"
        output_image_path = f"id/{today_date}/{user_id}.png"
        
        background = Image.open(background_image_path)
        overlay = Image.open(overlay_image_path)

        # A4 half size

        height = 638
        width = math.floor((1980 * height) / 1080)
        # width = math.floor(2480 / 2)
        # height = math.floor((width * 1080) / 1920)
        standered_width = 1013
        standered_height = 638
    
        overlay = overlay.resize((width, height))

        overlay_with_alpha = Image.new("RGBA", overlay.size, (0, 0, 0, 0))
        overlay_with_alpha.paste(overlay, (0, 0))

        background.paste(overlay_with_alpha, (0, 0), overlay_with_alpha)
        background.save(output_image_path)
        

    def create_directory(self, dir_name):
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
            print("Directory ", dir_name,  " Created ")
    
    def create_sub_dir(self, dir, sub_dir):
        self.create_directory(dir)
        if not os.path.exists(f"{dir}/{sub_dir}"):
            os.mkdir(f"{dir}/{sub_dir}")
            print("Directory ", f"{dir}/{sub_dir}",  " Created ")
    
    def show_warning_popup(self, message, warn):
        # create a message box with the warning message and an "OK" button to dismiss the popup
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowIcon(QIcon(AC.LOGO_ICO_PATH))
        msg.setText(message)
        msg.setWindowTitle(f"Warning - {warn}")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def info(self, message):
        # create a message box with the warning message and an "OK" button to dismiss the popup
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowIcon(QIcon(AC.LOGO_ICO_PATH))
        msg.setText(message)
        msg.setWindowTitle("Notice")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def create_receipt_pic(self, info, student_id):
        self.create_id(student_id)
        original_image = Image.open("config/receipt.png")
        
        x,y = original_image.size
        area = 1280
        start_point_x = math.floor((x - area) / 2)
        start_point_y = 40
        
        qr = Image.open(f"config/{student_id}-qr.png")
        qr_width, qr_height = qr.size
        # qr_position = ((x - qr_width) // 2, start_point_y)
        qr_position = (start_point_x + area - qr_width, start_point_y)
        original_image.paste(qr, qr_position)


        draw = ImageDraw.Draw(original_image)
        teacher_font = ImageFont.truetype("arial.ttf", size=70)
        subject_font = ImageFont.truetype("arial.ttf", size=100)
        current_datetime = datetime.now()

        draw.text((start_point_x, (qr_height // 2)), f"Student ID: {student_id}", font=teacher_font, fill="black", stroke_width=2)
        draw.text((start_point_x, (qr_height // 2) + 80), f"Date: {current_datetime.date()}", font=teacher_font, fill="black", stroke_width=2)
        draw.text((start_point_x, (qr_height // 2) + 160), f"Time: {current_datetime.strftime('%H:%M:%S')}", font=teacher_font, fill="black", stroke_width=2)
        start_point_y += qr_height
        draw.text((0, start_point_y), f"{'-' * 120}", font=teacher_font, fill="black", stroke_width=2)
        start_point_y += 10
        draw.text((0, start_point_y), f"{'-' * 120}", font=teacher_font, fill="black", stroke_width=2)
        start_point_y += 100
        total = 0
        for cls in info:
            teacher = f"{cls['teacher']}"
            month = f"{cls['month']}"
            subject = cls["subject"]
            
            price = f"{cls['fee']} LKR"
            if cls["fee"] == "Free":
                price = "Free"
                total += 0
            else:
                price = f"{cls['fee']} LKR"
                total += int(cls['fee'])
           
            draw.text((start_point_x, start_point_y), teacher, font=teacher_font, fill="black", stroke_width=2)
            if month == "onetime":
                draw.text((start_point_x + 1000, start_point_y), month, font=teacher_font, fill="black", stroke_width=2)
            else:
                draw.text((start_point_x + 1100, start_point_y), month, font=teacher_font, fill="black", stroke_width=2)
            start_point_y += 80
            draw.text((start_point_x, start_point_y), subject, font=subject_font, fill="black", stroke_width=2)
            draw.text((start_point_x + 800, start_point_y), price, font=subject_font, fill="black", stroke_width=2)
            start_point_y += 200
        
        draw.text((0, start_point_y), f"{'-' * 120}", font=teacher_font, fill="black", stroke_width=2)
        start_point_y += 80
        draw.text((start_point_x, start_point_y), "Total", font=subject_font, fill="black", stroke_width=2)
        draw.text((start_point_x + 800, start_point_y), f"{str(total)} LKR", font=subject_font, fill="black", stroke_width=2)
        start_point_y += 250
        draw.text((0, start_point_y), f"{'-' * 120}", font=teacher_font, fill="black", stroke_width=2)

        # Define starting position for the text
        original_image.save("config/receipt.png")
        os.remove(f"config/{student_id}-qr.png")

        
    def get_cam_input_id(self):
        if os.path.exists(AC.SETTINGS_JSON_PATH):
            with open(AC.SETTINGS_JSON_PATH, "r") as jf:
                data = json.load(jf)
                return data["cam_input_id"]
        else:
            return None
    
    def get_accounts(self):
        if os.path.exists(AC.SETTINGS_JSON_PATH):
            with open(AC.SETTINGS_JSON_PATH, "r") as jf:
                data = json.load(jf)
                return data["accounts"]
        else:
            return None
        
    def ts_to_date(self, ts):
        dt_object_local = datetime.fromtimestamp(int(ts))
        formatted_date = dt_object_local.strftime('%d-%m-%Y')
        formatted_time = dt_object_local.strftime('%H:%M:%S')
        
        return formatted_date, formatted_time