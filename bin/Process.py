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
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QLabel, QVBoxLayout, QWidget, QTreeWidgetItem, QTextBrowser
from PyQt5.QtGui import QPixmap
from io import BytesIO
import webbrowser

class Process:
    def __init__(self, app):
        self.app = app
        self.helper = Helper()
        self.dbh = DB("ok")
        self.db = self.dbh.db

    def start_process(self):
        self.app.patient_info_frame.hide()
        self.app.close_patient_session.hide()

    def switch_main_pages(self, title, page):
        self.app.menu_title.setText(title)
        self.app.doctor_view.setCurrentWidget(page)

    def doctor_login(self):
        username = self.app.login_username.text().strip()
        password = self.app.login_password.text()
        is_authenticated = self.dbh.check_doctor(username, password)
        if is_authenticated:
            
            AC.DOCTOR_DATA = is_authenticated

            self.app.doctor_view.setCurrentWidget(self.app.dashboard)
            self.app.stackedWidget.setCurrentWidget(self.app.main_page)
        elif is_authenticated is False:
            print("Wrong Username or Password")

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
        self.switch_main_pages("Sub History", self.app.sub_history)
        self.app.main_title.setText(report["topic"])
        self.app.main_description.setText(report["description"])
        main_doctor = f'{docs[report["doctor"]]["first_name"]} {docs[report["doctor"]]["last_name"]}'
        self.app.main_doctor.setText(main_doctor)
        self.app.main_date.setText(str(self.timestamp_to_datetime(report["ts"])))

        # sub_history_tree
        self.app.sub_history_tree.clear()
        self.app.sub_history_tree.setColumnWidth(0, 600)
        self.app.sub_history_tree.setColumnWidth(1, 400)
        self.app.sub_history_tree.setColumnWidth(2, 300)
        self.app.sub_history_tree.setHeaderLabels(["Info", "Doctor", "Time"])
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
                    text_browser3.setPlainText(sub_report["description"].strip())  # Removing leading/trailing whitespace
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

