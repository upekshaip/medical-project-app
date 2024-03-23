from bin.Process import Process

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
        self.app.service_login_btn.clicked.connect(lambda: self.process.service_login())
        self.app.doc_switch_btn.clicked.connect(lambda: self.app.stackedWidget.setCurrentWidget(self.app.doctor_login_page))
        self.app.switch_service_btn.clicked.connect(lambda: self.app.stackedWidget.setCurrentWidget(self.app.emplooyee_login_page))
        
        
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
        self.app.menu_logout_service.clicked.connect(lambda: self.process.logout_service_account())
        
        # Profile
        self.app.edit_profile.clicked.connect(lambda: self.process.save_doctor_profile())
        self.app.reset_profile.clicked.connect(lambda: self.process.reset_doctor_profile())
        
        # Settings
        self.app.back_btn.clicked.connect(lambda: self.app.stackedWidget.setCurrentWidget(self.app.main_page))
        self.app.settings_save_btn.clicked.connect(lambda: self.process.save_settings())

        # SERVICE ACCOUNT
        self.app.search_user_btn.clicked.connect(lambda: self.process.search_user())
        self.app.scan_qr_user_btn.clicked.connect(lambda: self.process.open_scanner_search_user())
        self.app.generate_id.clicked.connect(lambda: self.process.genarate_id())
        