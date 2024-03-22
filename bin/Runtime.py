from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit, QFileIconProvider, QDialog, QLineEdit, QTableWidgetItem, QLabel, QTreeWidgetItem
from PyQt5.QtCore import QUrl, Qt, QDate
from PyQt5.QtGui import QDesktopServices, QPixmap
from bin.Config import AppConfig as AC
from bin.Process import Process
from datetime import date

class RunTiime():

    def __init__(self, app):
        self.app = app
        self.process = Process(app)
        self.process.start_process()
 
    def buttons(self):

        # DASHBOARD BTNS
        self.app.menu_dash.clicked.connect(lambda: self.process.switch_main_pages("Dashboard", self.app.dashboard))
        self.app.menu_history.clicked.connect(lambda: self.process.switch_to_history_page())
        self.app.menu_profile.clicked.connect(lambda: self.process.switch_to_profile())
        self.app.menu_settings.clicked.connect(lambda: self.app.stackedWidget.setCurrentWidget(self.app.settings_page))

        # LOG IN
        self.app.login_btn.clicked.connect(lambda: self.process.doctor_login())
        
        # SEARCH BTN 
        self.app.search_patient_btn.clicked.connect(lambda: self.process.search_patient())
        self.app.close_patient_session.clicked.connect(lambda: self.process.close_patient_session())
        self.app.scan_qr_btn.clicked.connect(lambda: self.process.open_scanner())

        # ROPORT BTNS
        self.app.new_main_record.clicked.connect(lambda: self.process.switch_to_main_record())
        self.app.new_sub_record.clicked.connect(lambda: self.process.switch_to_sub_record())
        self.app.change_status_btn.clicked.connect(lambda: self.process.change_status())

        # SUB REPORT BTN
        self.app.add_image_btn.clicked.connect(lambda: self.process.openFileDialog())
        self.app.clear_images.clicked.connect(lambda: self.app.sub_images.setText(""))
        self.app.add_new_sub_report.clicked.connect(lambda: self.process.add_new_sub_report())
        self.app.add_new_main_report.clicked.connect(lambda: self.process.add_new_main_report())

        # LOGOUT
        self.app.menu_logout.clicked.connect(lambda: self.process.logout_process())
        
        # Profile
        self.app.edit_profile.clicked.connect(lambda: self.process.save_doctor_profile())
        self.app.reset_profile.clicked.connect(lambda: self.process.reset_doctor_profile())
        
        # Settings
        self.app.back_btn.clicked.connect(lambda: self.app.stackedWidget.setCurrentWidget(self.app.main_page))
        self.app.settings_save_btn.clicked.connect(lambda: self.process.save_settings())



        
        # today_date = date.today()
        # day = today_date.strftime('%d-%m-%Y').split("-")
        # self.app.payment_date_input.setDate(QDate(int(day[2]), int(day[1]), int(day[0])))

        # # Login
        # self.app.login_btn.clicked.connect(lambda: self.process.login_process())
        # self.app.menu_logout.clicked.connect(lambda: self.process.logout_process())

        # # Hall availability page
        # self.app.hall_btn.clicked.connect(lambda: self.app.stackedWidget.setCurrentWidget(self.app.hall_pg))
        # self.app.hall_input.addItems(self.process.get_halls())
        # self.app.hall_day_input.currentIndexChanged.connect(lambda: self.process.hall_search_process(self.app.hall_day_input.currentText(), self.app.hall_input.currentText()))
        # self.app.hall_input.currentIndexChanged.connect(lambda: self.process.hall_search_process(self.app.hall_day_input.currentText(), self.app.hall_input.currentText()))


        # # MENU
        # self.app.menu_dash.clicked.connect(lambda: self.app.stackedWidget.setCurrentWidget(self.app.dashboard_pg))
        # self.app.menu_st_register.clicked.connect(lambda: self.process.click_student_register())
        # self.app.student_reg_btn.clicked.connect(lambda: self.process.click_student_register())
        # self.app.menu_st.clicked.connect(lambda: self.app.stackedWidget.setCurrentWidget(self.app.students_pg))
        # self.app.menu_tch.clicked.connect(lambda: self.app.stackedWidget.setCurrentWidget(self.app.teacher_pg))
        # self.app.menu_cls.clicked.connect(lambda: self.app.stackedWidget.setCurrentWidget(self.app.class_page))
        # self.app.create_cls_btn.clicked.connect(lambda: self.process.create_class_process())
        # self.app.new_teacher_btn.clicked.connect(lambda: self.process.create_teacher_process())
        # # settings
        # self.app.settings_btn.clicked.connect(lambda: self.process.settings_reset())
        # self.app.go_dash_btn.clicked.connect(lambda: self.app.stackedWidget_main.setCurrentWidget(self.app.main_page))
        # self.app.reload_printer_btn.clicked.connect(lambda: self.process.settings_process())
        # self.app.save_settings_btn.clicked.connect(lambda: self.process.save_settings())
        # self.app.reset_settings_btn.clicked.connect(lambda: self.process.settings_reset())
        # self.app.contact_btn.clicked.connect(lambda: self.process.contact_me())



        # # Edit student details
        # self.app.st_edit_reset.clicked.connect(lambda: self.process.reset_student_edit())
        # self.app.student_details_btn.clicked.connect(lambda: self.process.load_st_details())
        # self.app.search_student.textChanged.connect(
        #     lambda: self.process.search_student(self.app.search_student.text()))
        # self.app.st_edit_save.clicked.connect(lambda: self.process.save_student_edit())
        

        # # Other buttons
        # # Student registration
        # self.app.st_code_btn.clicked.connect(lambda: self.process.generate_code("s"))
        # self.app.st_reg_save.clicked.connect(lambda: self.process.save_student_reg())
        # self.app.st_reg_clear.clicked.connect(lambda: self.process.clear_student_reg())

        # # Teacher registration
        # self.app.tea_code_btn.clicked.connect(lambda: self.process.generate_code("t"))
        # self.app.tea_reg_save.clicked.connect(lambda: self.process.save_teacher_reg())
        # self.app.tea_reg_clear.clicked.connect(lambda: self.process.clear_teacher_reg())

        # # Edit Teacher
        # self.app.tea_edit_save.clicked.connect(lambda: self.process.save_teacher_edit())
        # self.app.tea_edit_reset.clicked.connect(lambda: self.process.reset_teacher_edit())
        # self.app.teacher_details_btn.clicked.connect(lambda: self.process.load_teacher_details())
        # self.app.search_teacher.textChanged.connect(
        #     lambda: self.process.search_teacher(self.app.search_teacher.text()))
        
        
        # # Class registration
        # self.app.cls_reg_save.clicked.connect(lambda: self.process.save_class_reg())
        # self.app.cls_reg_clear.clicked.connect(lambda: self.process.clear_class_reg())
        # self.app.cls_hall_reg.addItems(self.process.get_halls())
        # self.app.cls_hall_edit.addItems(self.process.get_halls())

       

        # # class edit
        # self.app.cls_edit_save.clicked.connect(lambda: self.process.save_class_edit())
        # self.app.class_details_btn.clicked.connect(lambda: self.process.click_class_details_btn())
        # self.app.class_status_comboBox.currentIndexChanged.connect(lambda: self.process.load_class_details(self.app.class_status_comboBox.currentText()))
        # self.app.search_class.textChanged.connect(
        #     lambda: self.process.search_class(self.app.search_class.text()))
        # self.app.cls_edit_reset.clicked.connect(lambda: self.process.reset_class_edit())


        # # Payment buttons
        # self.app.payment_search_btn.clicked.connect(lambda: self.process.payment_handle(self.app.payment_search.text()))
        # self.app.payment_table.setColumnWidth(1, 150)
        # self.app.payment_table.setColumnWidth(0, 150)
        # self.app.pay_btn.clicked.connect(lambda: self.process.payment_process())
        # self.app.qr_scan_btn.clicked.connect(lambda: self.process.open_scanner())
        # self.app.payment_clear_btn.clicked.connect(lambda: self.process.payment_table_reset(self.app.payment_student_id.text()))

        # # class report
        # self.app.cls_report_btn.clicked.connect(lambda: self.process.class_report_process())
        # self.app.save_report_btn.clicked.connect(lambda: self.process.save_the_report())

       

        # Setting the logo
        # pixmap = QPixmap("config/logo.ico")
        # self.app.logo.setPixmap(pixmap)
        # image_path = "logo.ico"
        # pixmap = QPixmap(image_path)
        # self.app.logo.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))


    def run(self):
        pass