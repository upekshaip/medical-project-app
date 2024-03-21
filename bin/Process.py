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
from openpyxl.chart import PieChart, Reference

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
        


