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
        pass

    def switch_main_pages(self, title, page):
        self.app.menu_title.setText(title)
        self.app.doctor_view.setCurrentWidget(page)

    def doctor_login(self):
        username = self.app.login_username.text().strip()
        password = self.app.login_password.text()
        is_authenticated = self.dbh.check_doctor(username, password)
        if is_authenticated:
            print(is_authenticated)
            self.app.doctor_view.setCurrentWidget(self.app.dashboard)
            self.app.stackedWidget.setCurrentWidget(self.app.main_page)
        else:
            print("Wrong Username or Password")
