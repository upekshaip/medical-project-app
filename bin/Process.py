from PyQt5.QtWidgets import QTreeView, QAbstractItemView, QApplication, QTreeWidgetItem, QTableWidgetItem, QCheckBox, QTreeWidget, QSizePolicy
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,QVBoxLayout, QFrame, QComboBox
from PyQt5.QtGui import QPixmap, QImage, QDesktopServices, QIcon
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QDate
import random
import string
from datetime import datetime
import os
import math
import time
import json
from bin.Config import AppConfig as AC
from bin.Helper import Helper
from bin.FDB import DB
from bin.Scanner import QRScanner
from openpyxl import Workbook
from PyQt5.QtWidgets import QFrame, QLabel, QScrollArea, QTextBrowser
from openpyxl.chart import PieChart, Reference
import sys
import requests
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QLabel, QVBoxLayout, QWidget, QTreeWidgetItem, QTextBrowser, QFileDialog
from PyQt5.QtGui import QPixmap
from io import BytesIO
import webbrowser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

class Process:
    def __init__(self, app):
        self.app = app
        self.helper = Helper()
        self.dbh = DB("ok")
        self.db = self.dbh.db

    def start_process(self):
        self.json_data_handle()
        self.app.patient_info_frame.hide()
        self.app.close_patient_session.hide()
        self.app.sub_type.addItems(AC.REPORT_TYPES)
        self.app.d_district.addItems(AC.DISTRICTS)
        self.app.d_dob.setCalendarPopup(True)
        self.app.cam_input.setValue(AC.CAM_INPUT_ID)


    def json_data_handle(self):
        self.create_directory("config")
        if os.path.exists(AC.SETTINGS_JSON_PATH):
            with open(AC.SETTINGS_JSON_PATH, "r") as jf:
                cam_data = json.load(jf)
                AC.CAM_INPUT_ID = cam_data["cam_input_id"]
                AC.ACCOUNTS = cam_data["accounts"]
        else:
            settings_data = {
                "cam_input_id": AC.CAM_INPUT_ID,
                "accounts": AC.ACCOUNTS
            }
            with open(AC.SETTINGS_JSON_PATH, 'w') as json_file:
                json.dump(settings_data, json_file)

    
    def save_json_file(self):
        settings_data = {
            "cam_input_id": AC.CAM_INPUT_ID,
            "accounts": AC.ACCOUNTS
        }
        self.create_directory("config")
        if os.path.exists(AC.SETTINGS_JSON_PATH):
            with open(AC.SETTINGS_JSON_PATH, 'w') as json_file:
                json.dump(settings_data, json_file)

    def save_settings(self):
        AC.CAM_INPUT_ID = self.app.cam_input.value()
        self.save_json_file()
        self.helper.info("Settings Saved!")


    def create_directory(self, dir_name):
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
            print("Directory ", dir_name,  " Created ")

    def switch_main_pages(self, title, page):
        self.app.menu_title.setText(title)
        self.app.doctor_view.setCurrentWidget(page)

    def doctor_login(self):
        username = self.app.login_username.text().strip()
        password = self.app.login_password.text()
        
        self.app.login_username.setText("")
        self.app.login_password.setText("")
        self.app.login_info.setText("")

        if username and password:
            is_authenticated = self.dbh.check_doctor(username, password)
            if is_authenticated:
                
                AC.DOCTOR_DATA = is_authenticated

                self.switch_main_pages("Dashboard", self.app.dashboard)
                self.app.stackedWidget.setCurrentWidget(self.app.main_page)
            elif is_authenticated is False:
                self.app.login_info.setText("Wrong Username or Password")
        
        else:
            self.app.login_info.setText("Wrong Username or Password")
    
    def service_login(self):
        username = self.app.service_login_username.text().strip()
        password = self.app.service_login_password.text()
        
        self.app.user_info_frame.hide()
        self.app.generate_id.hide()

        self.app.service_login_username.setText("")
        self.app.service_login_password.setText("")
        self.app.service_login_info.setText("")
        
        if username and password:
            is_authenticated = self.check_service_account(username, password)
            if is_authenticated:
                
                AC.SERVICE_ACCOUNT_LOGGED = is_authenticated
                self.app.stackedWidget.setCurrentWidget(self.app.service_area)
            
            else:
                self.app.service_login_info.setText("Wrong Username or Password")
        
        else:
            self.app.service_login_info.setText("Wrong Username or Password")

    
    def check_service_account(self, username, password):
        for acc in AC.ACCOUNTS:
            if acc["username"] == username and acc["password"] == password:
                return True
        return False



    def logout_service_account(self):
        AC.SERVICE_ACCOUNT_LOGGED = False
        self.app.stackedWidget.setCurrentWidget(self.app.emplooyee_login_page)

    def search_user(self):
        self.app.user_info_frame.hide()
        self.app.generate_id.hide()

        patient_id = self.app.search_user_id.text()
        if (patient_id != ""):
            
            patient_data = ""
            
            if (len(patient_id) > 10):
                patient_data = self.dbh.get_user_by_nic(patient_id)
                if patient_data and patient_data is not False:
                    patient_data = self.dbh.get_patient(patient_data)
            else:
                patient_data = self.dbh.get_patient(patient_id)

            if (patient_data):
                self.app.patient_info_frame.show()
                self.app.close_patient_session.show()

                # form data setting
                self.app.user_first_name.setText(f'{patient_data["first_name"]}')
                self.app.user_last_name.setText(f'{patient_data["last_name"]}')
                self.app.user_full_name.setText(f'{patient_data["full_name"]}')
                self.app.user_nic.setText(f'{patient_data["nic"]}')
                self.app.user_uid.setText(f'{patient_data["uid"]}')
                self.app.user_district.setText(f'{patient_data["district"]}')
                self.app.user_email.setText(f'{patient_data["email"]}')

                self.app.user_info_frame.show()
                self.app.generate_id.show()


            elif patient_data is False:
                self.helper.show_warning_popup("Did not found the user. Try again", "Invalid user ID")
        else:
            self.helper.show_warning_popup("Did not found the user. Try again", "Invalid user ID")


    def search_patient(self):
        patient_id = self.app.patient_id_input.text()
        if (patient_id != ""):
      
            patient_data = self.dbh.get_patient(patient_id)
            if (patient_data):
                AC.PATIENT_DATA = patient_data

                self.app.patient_info_frame.show()
                self.app.close_patient_session.show()

                # form data setting
                self.app.patient_name.setText(f'{patient_data["first_name"]} {patient_data["last_name"]}')
                self.app.patient_full_name.setText(f'{patient_data["full_name"]}')
                self.app.nic.setText(f'{patient_data["nic"]}')
                age = datetime.now().year - int(patient_data["dob"].split("-")[0])
                self.app.age.setText(f'{age}')
                self.app.gender.setText(f'{patient_data["gender"]}')
                self.app.dob.setText(f'{patient_data["dob"]}')
                self.app.blood_group.setText(f'{patient_data["blood"]}')
                self.app.phone.setText(f'{patient_data["phone"]}')
                self.app.email.setText(f'{patient_data["email"]}')
                self.app.address.setText(f'{patient_data["address_l1"]}, {patient_data["address_l1"]}, {patient_data["district"]}')

                self.app.emg_name.setText(f'{patient_data["emg_name"]}')
                self.app.emg_relation.setText(f'{patient_data["rel_name"]}')
                self.app.emg_phone.setText(f'{patient_data["emg_phone"]}')
                self.app.emg_address.setText(f'{patient_data["emg_address_l1"]}, {patient_data["emg_address_l1"]}, {patient_data["emg_district"]}')

                self.app.med_allergies.setText(f'{patient_data["med_allergy"]}')
                self.app.med_surgeries.setText(f'{patient_data["med_surgery"]}')
                self.app.med_chronic.setText(f'{patient_data["med_chronic"]}')


            elif patient_data is False:
                self.helper.show_warning_popup("Did not found the patient. Try again", "Invalid Patient ID")
        else:
            self.helper.show_warning_popup("Did not found the patient. Try again", "Invalid Patient ID")


    def close_patient_session(self):
        AC.PATIENT_DATA = None
        self.app.patient_info_frame.hide()
        self.app.close_patient_session.hide()
        
    
    def switch_to_history_page(self):
        self.app.menu_title.setText("Patient History")
        self.app.doctor_view.setCurrentWidget(self.app.history)
        
        if AC.PATIENT_DATA is not None:
            self.app.history_info.setText("You can add main and sub reports")
            self.app.new_main_record.show()
            self.app.treeWidget.show()
            self.show_history_report()

        else:
            self.app.history_info.setText("Please select patient on dashboard first. Then come back to see the details")
            self.app.new_main_record.hide()
            self.app.treeWidget.hide()
            
            


    def show_history_report(self):
        report = self.dbh.get_reports(AC.PATIENT_DATA["uid"])
        db_doctor_data = self.dbh.get_all_doctors()

        if report and db_doctor_data:
            self.app.treeWidget.clear()
            self.app.treeWidget.setHeaderLabels(["Topic", "Doctor", "Time", "Action", "Status"])
            self.app.treeWidget.setColumnWidth(0, 600)
            self.app.treeWidget.setColumnWidth(1, 300)
            self.app.treeWidget.setColumnWidth(2, 300)
            self.app.treeWidget.setColumnWidth(4, 300)
            for main_key, main_report in report.items():
                main_doctor = f'{db_doctor_data[main_report["doctor"]]["first_name"]} {db_doctor_data[main_report["doctor"]]["last_name"]}'
                main_item = QTreeWidgetItem(self.app.treeWidget, [main_report["topic"], main_doctor, str(self.timestamp_to_datetime(main_report["ts"])), "", main_report["status"]])
                
                button = QPushButton("View")
                self.app.treeWidget.setItemWidget(main_item, 3, button)
                # button.clicked.connect(lambda _, report=main_report, key=main_key : self.view_history(report, key))
                button.clicked.connect(lambda _, report=main_report, key=main_key, docs=db_doctor_data: self.view_history(report, key, docs))
                
                if "content" in main_report.keys():
                    for sub_key, sub_report in main_report["content"].items():
                        sub_doctor = f'{db_doctor_data[sub_report["doctor"]]["first_name"]} {db_doctor_data[sub_report["doctor"]]["last_name"]}'
                        child1 = QTreeWidgetItem(main_item, [sub_report["topic"], sub_doctor, str(self.timestamp_to_datetime(sub_report["ts"]))])
                        

    
    def view_history(self, report, key, docs):
        # adding the main info
        self.app.status_combo.clear()
        self.app.status_combo.addItems(["Active", "Inactive", "Stable"])

        self.switch_main_pages("Sub History", self.app.sub_history)
        self.app.main_title.setText(report["topic"])
        self.app.main_description.setText(report["description"])
        main_doctor = f'{docs[report["doctor"]]["first_name"]} {docs[report["doctor"]]["last_name"]}'
        self.app.main_doctor.setText(main_doctor)
        self.app.main_date.setText(str(self.timestamp_to_datetime(report["ts"])))
        self.app.main_report_id.setText(report["record_id"])
        self.app.status_combo.setCurrentText(report["status"])

        # sub_history_tree
        self.app.sub_history_tree.clear()
        self.app.sub_history_tree.setHeaderLabels(["Info", "Doctor", "Time"])
        self.app.sub_history_tree.setColumnWidth(0, 600)
        self.app.sub_history_tree.setColumnWidth(1, 300)
        self.app.sub_history_tree.setColumnWidth(2, 300)
        if "content" in report.keys():
            for sub_key, sub_report in report["content"].items():
                sub_doctor = f'{docs[sub_report["doctor"]]["first_name"]} {docs[sub_report["doctor"]]["last_name"]}'
                main_item = QTreeWidgetItem(self.app.sub_history_tree, [sub_report["topic"], sub_doctor, str(self.timestamp_to_datetime(sub_report["ts"]))])
                child1 = QTreeWidgetItem(main_item, [f'Type: {sub_report["type"]}'])
                
                child2 = QTreeWidgetItem(main_item, [''])
                text_browser = QTextBrowser()
                text_browser.setPlainText(sub_report["description"].strip())  # Removing leading/trailing whitespace
                
                self.app.sub_history_tree.setItemWidget(child2, 0, text_browser)
                self.app.sub_history_tree.setFirstItemColumnSpanned(child2, True)
                

                if "images" in sub_report.keys():
                    child3 = QTreeWidgetItem(main_item, [''])
                    text_browser3 = QTextBrowser()
                    text_browser3.setPlainText(sub_report["description"].strip())
                    text_browser3.setFixedHeight(210)
                    self.app.sub_history_tree.setItemWidget(child3, 0, text_browser3)
                    self.app.sub_history_tree.setFirstItemColumnSpanned(child3, True)
                    
                    table_widget = self.add_images_to_table(sub_report["images"])
                    self.app.sub_history_tree.setItemWidget(child3, 1, table_widget)


    def download_image(self, url):
        url = f"{AC.IMAGE_URL_PATH}{url}"
        response = requests.get(url)
        if response.status_code == 200:
            return BytesIO(response.content)
        else:
            return None

    def add_images_to_table(self, image_urls):
        table_widget = QTableWidget(2, len(image_urls))
        
        # Set the fixed height for all images (adjust as needed)
        image_height = 100
        
        for i, url in enumerate(image_urls):
            # Download the image
            widget = QWidget()
            layout = QVBoxLayout()
            
            image_data = self.download_image(url)
            
            if image_data:
                # Create a QPixmap from the image data
                pixmap = QPixmap()
                pixmap.loadFromData(image_data.getvalue())
                
                # Create a QLabel to display the image
                label = QLabel()
                label.setFixedHeight(image_height)
                label.setPixmap(pixmap.scaledToHeight(image_height))

                button = QPushButton("Open")
                button.clicked.connect(lambda checked, u=url: self.open_image_in_browser(u))
                layout.addWidget(button)
                
                # Add the QLabel to the table as a QTableWidgetItem
                table_widget.setItem(0, i, QTableWidgetItem())
                table_widget.setCellWidget(0, i, label)
                table_widget.setRowHeight(0, 100)
            
            widget.setLayout(layout)
            table_widget.setCellWidget(1, i, widget)
            table_widget.setRowHeight(1, 75)
        
        return table_widget

    def open_image_in_browser(self, url):
        url = f"{AC.IMAGE_URL_PATH}{url}"
        webbrowser.open(url)

    def change_status(self):
        status = self.app.status_combo.currentText()
        main_report_id = self.app.main_report_id.text()

        self.dbh.change_status(main_report_id, status)
        self.helper.info(f"Status Changed to {status}!")



    def timestamp_to_datetime(self, timestamp):
        # Convert timestamp to datetime object
        dt_object = datetime.fromtimestamp(timestamp)
        return dt_object


    #  CAMERA OPEN FUNCTION
    def open_scanner(self):
        qr_scanner = QRScanner()
        qr_scanner.exec_()
        print(f"FINAL: {AC.QR_SCANNER}")
        self.app.patient_id_input.setText(str(AC.QR_SCANNER))
        self.search_patient()
        AC.QR_SCANNER = ""
    
    
    def open_scanner_search_user(self):
        qr_scanner = QRScanner()
        qr_scanner.exec_()
        print(f"FINAL: {AC.QR_SCANNER}")
        self.app.search_user_id.setText(str(AC.QR_SCANNER))
        self.search_user()
        AC.QR_SCANNER = ""

    def genarate_id(self):
        uid_code = self.app.user_uid.text()
        first_name = self.app.user_first_name.text()
        last_name = self.app.user_last_name.text()
        email = self.app.user_email.text()
        message = f"Dear {first_name} {last_name},\n\nPlease find attached your User ID card.\n\nThank you,\nMedSync."

        path = self.helper.generate_id(uid_code, first_name, last_name)
        
        self.send_email(email, message, path)
        self.helper.info("User ID generated!")
        
        self.app.user_info_frame.hide()
        self.app.generate_id.hide()
        self.app.search_user_id.setText("")
        

    
    def openFileDialog(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self.app, "Select Images", "", "Image Files (*.png *.jpg)", options=options)
        
        if files:
            # Wrap each file path with double quotes
            files_with_quotes = ['"{0}"'.format(file) for file in files]
            self.app.sub_images.setText(", ".join(files_with_quotes))



    def add_new_main_report(self):
        topic = self.app.new_main_topic.text()
        description = self.app.new_main_description.toPlainText()
        if (topic and description):
            self.app.main_report_info.setText("")
            if (self.dbh.add_main_report(topic, description)):
                self.helper.info("New main record added!")
                self.switch_to_history_page()
                self.main_report_clear()

        else:
            self.app.main_report_info.setText("Please fill out the required feilds")


    def sub_report_clear(self):
        self.app.sub_topic.setText("")
        self.app.sub_type.setCurrentText(AC.REPORT_TYPES[0])
        self.app.sub_description.setText("")
        self.app.sub_images.setText("")
        self.app.sub_report_info.setText("")
    
    def main_report_clear(self):
        self.app.new_main_topic.setText("")
        self.app.new_main_description.setText("")
        self.app.main_report_info.setText("")

    def switch_to_main_record(self):
        self.main_report_clear()
        self.switch_main_pages("Add New Report", self.app.new_report)
    
    def switch_to_sub_record(self):
        self.sub_report_clear()
        self.switch_main_pages("Add New Sub Report", self.app.new_sub_report)


    def add_new_sub_report(self):
        #ID -> self.app.main_report_id
        main_report_id = self.app.main_report_id.text()
        sub_topic = self.app.sub_topic.text()
        sub_type = self.app.sub_type.currentText()
        sub_description = self.app.sub_description.toPlainText()
        sub_images = str(self.app.sub_images.text()).split(",")
        sub_images = [image.replace('"', "").strip() for image in sub_images if len(image) > 0]
        server_img_path = self.upload_images(sub_images)

        if (main_report_id and sub_topic and sub_description and sub_type):
            self.app.sub_report_info.setText("")
            if(self.dbh.add_sub_report(main_report_id, sub_topic,sub_description, sub_type, server_img_path)):
                self.helper.info("New sub record added!")
                self.switch_to_history_page()
                self.sub_report_clear()
                
        else:
            self.app.sub_report_info.setText("Please fill out the required feilds")

        
    def logout_process(self):

        AC.PATIENT_DATA = None
        AC.DOCTOR_DATA = None
        self.app.stackedWidget.setCurrentWidget(self.app.doctor_login_page)
        self.app.doctor_view.setCurrentWidget(self.app.dashboard)
        self.app.login_info.setText("")


    def upload_images(self, image_paths):
        files = []
        if len(image_paths) > 0:
            for path in image_paths:
                files.append(('images[]', open(path, 'rb')))
            
            response = requests.post(AC.IMAGE_UPLOAD_API_URL, files=files)
            
            if response.status_code == 200:
                unique_file_names = response.json()
                print("Uploaded successfully. Unique filenames:", unique_file_names)
                return unique_file_names

            else:
                print("Failed to upload images. Status code:", response.status_code)
                return []
        else:
            return []
        

    def reset_doctor_profile(self):
        data = self.dbh.get_doctor(AC.DOCTOR_DATA["uid"])
        AC.DOCTOR_DATA = data
        if data:
            self.app.d_full_name.setText(data["full_name"])
            self.app.d_uid.setText(data["uid"])
            self.app.d_first_name.setText(data["first_name"])
            self.app.d_last_name.setText(data["last_name"])
            self.app.d_gender.setCurrentText(data["gender"])
            self.app.d_district.setCurrentText(data["district"])

            year, month, day = map(int, data["dob"].split('-'))
            date = QDate(year, month, day)
            self.app.d_dob.setDate(date)

            self.app.d_nic.setText(data["nic"])
            self.app.d_mbbs.setText(data["mbbs"])
            self.app.d_address_l1.setText(data["address_l1"])
            self.app.d_address_l2.setText(data["address_l2"])
            self.app.d_phone.setText(data["phone"])
            self.app.d_email.setText(data["email"])

    def save_doctor_profile(self):
        full_name = self.app.d_full_name.text()
        uid = self.app.d_uid.text()
        first_name = self.app.d_first_name.text()
        last_name = self.app.d_last_name.text()
        gender = self.app.d_gender.currentText()
        date = str(self.app.d_dob.text()).replace("/", "-")
        nic = self.app.d_nic.text()
        mbbs = self.app.d_mbbs.text()
        address_l1 = self.app.d_address_l1.text()
        address_l2 = self.app.d_address_l2.text()
        phone = self.app.d_phone.text()
        email = self.app.d_email.text()
        district = self.app.d_district.currentText()

        data = [full_name, uid, first_name, last_name, gender, date, nic, mbbs, address_l1, address_l2, phone, email, district]
        is_ok = True
        for item in data:
            if not item:
                self.app.profile_info.setText("All feilds are required")
                is_ok = False
                break
        if is_ok:
            self.dbh.set_doc_details(data)
            self.reset_doctor_profile()
            self.helper.info("Doctor details updated!")
            


    def switch_to_profile(self):
        self.switch_main_pages("Profile", self.app.profile)
        self.reset_doctor_profile()


    def send_email(self, receiver_email, message, image_path):
        # Set up the SMTP server
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Create a multipart message
        msg = MIMEMultipart()
        msg['From'] = AC.EMAIL
        msg['To'] = receiver_email
        msg['Subject'] = AC.EMAIL_SUBJECT

        # Attach message
        msg.attach(MIMEText(message, 'plain'))

        # Attach image
        with open(image_path, 'rb') as file:
            img = MIMEImage(file.read(), name=os.path.basename(image_path))
        msg.attach(img)

        # Start the SMTP session
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Start TLS for security
            server.starttls()
            # Log in to the SMTP server
            server.login(AC.EMAIL, AC.EMAIL_PASSWORD)
            # Send the email
            server.sendmail(AC.EMAIL, receiver_email, msg.as_string())