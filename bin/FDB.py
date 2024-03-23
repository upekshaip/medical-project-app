import time
import pyrebase
import math
from bin.Cred import Cred
from bin.Config import AppConfig as AC
from bin.Helper import Helper

class DB:

    def __init__(self, status):
        self.helper = Helper()

        try:
            firebase = pyrebase.initialize_app(Cred.FIREBASE_CONF)
            self.db = firebase.database()
            print(f"DB connect ok: {status}")
        except:
            self.helper.show_warning_popup(message="No internet connection. Please check your network.",warn="No internet connection")
            print("No internet connection. Please check your network.")


    def check_doctor(self, username, password):
        try:
            data = self.db.child(f"{AC.DB_PATH}/doctors/{username}").get().val()
            if type(data) == list:
                return False
            
            elif data:
                data = dict(data)
                if username == data["uid"] and password == data["password"]:
                    return data
                else:
                    return False
            else:
                return False
        except:
            self.helper.show_warning_popup(AC.INTERNET_ERR_MSG, AC.INTERNET_ERR_WARN)
            return None
        
    def get_doctor(self, uid):
        try:
            data = self.db.child(f"{AC.DB_PATH}/doctors/{uid}").get().val()
            if type(data) == list:
                return False
            
            elif data:
                data = dict(data)
                return data
            else:
                return False
        except:
            self.helper.show_warning_popup(AC.INTERNET_ERR_MSG, AC.INTERNET_ERR_WARN)
            return None
        
    def set_doc_details(self, data):
        _data = {
            "full_name": data[0],
            "uid": data[1],
            "first_name": data[2],
            "last_name": data[3],
            "gender": data[4],
            "dob": data[5],
            "nic": data[6],
            "mbbs": data[7],
            "address_l1": data[8],
            "address_l2": data[9],
            "phone": data[10],
            "email": data[11],
            "district": data[12]
        }
        try:
            self.db.child(f"{AC.DB_PATH}/doctors/{data[1]}").update(_data)
        except:
            self.helper.show_warning_popup(message="No internet connection. Please check your network.",warn="No internet connection")


    def get_patient(self, patient_id):
        try:
            data = self.db.child(f"{AC.DB_PATH}/users/{patient_id}").get().val()
            if type(data) == list:
                return False
            
            elif data:
                data = dict(data)
                return data
            
            else:
                return False
        except:
            self.helper.show_warning_popup(AC.INTERNET_ERR_MSG, AC.INTERNET_ERR_WARN)
            return None
        
    
    def get_reports(self, patient_id):
        try:
            data = self.db.child(f"{AC.DB_PATH}/reports/{patient_id}").get().val()
            if type(data) == list:
                return False
            
            elif data:
                data = dict(data)
                return data
            
            else:
                return False
        except:
            self.helper.show_warning_popup(AC.INTERNET_ERR_MSG, AC.INTERNET_ERR_WARN)
            return None
        
        
    def get_all_doctors(self):
        try:
            data = self.db.child(f"{AC.DB_PATH}/doctors").get().val()
            if type(data) == list:
                return False
            
            elif data:
                data = dict(data)
                return data
            
            else:
                return False
        except:
            self.helper.show_warning_popup(AC.INTERNET_ERR_MSG, AC.INTERNET_ERR_WARN)
            return None
        
    def add_sub_report(self, main_report_id, topic, description, type, images):
        patient = AC.PATIENT_DATA["uid"]
        doctor = AC.DOCTOR_DATA["uid"]
        sub_record_id = self.helper.generate_code("")

        _data = {
            "ts": int(math.floor(time.time())),
            "topic": topic,
            "description": description,
            "type": type,
            "patient": patient,
            "doctor": doctor,
            "sub_record_id": sub_record_id,
            "images": images
        }

        try:
            self.db.child(f"{AC.DB_PATH}/reports/{patient}/{main_report_id}/content/{sub_record_id}").set(_data)
            return True
        except:
            self.helper.show_warning_popup(message="No internet connection. Please check your network.",warn="No internet connection")
            return False
        
    def add_main_report(self, topic, description):
        patient = AC.PATIENT_DATA["uid"]
        doctor = AC.DOCTOR_DATA["uid"]
        record_id = self.helper.generate_code("")

        _data = {
            "ts": int(math.floor(time.time())),
            "topic": topic,
            "description": description,
            "patient": patient,
            "doctor": doctor,
            "record_id": record_id,
            "status": "Active"
        }
        try:
            self.db.child(f"{AC.DB_PATH}/reports/{patient}/{record_id}").set(_data)
            return True
        except:
            self.helper.show_warning_popup(message="No internet connection. Please check your network.",warn="No internet connection")
            return False
        
    def change_status(self, main_report_id, status):
        patient = AC.PATIENT_DATA["uid"]
        try:
            self.db.child(f"{AC.DB_PATH}/reports/{patient}/{main_report_id}/status").set(status)
            return True
        except:
            self.helper.show_warning_popup(message="No internet connection. Please check your network.",warn="No internet connection")
            return False

    def get_user_by_nic(self, nic):
        try:
            data = self.db.child(f"{AC.DB_PATH}/nic/{nic}").get().val()
            if type(data) == list:
                return False
            
            elif data:
                return data
            
            else:
                return False
        except:
            self.helper.show_warning_popup(AC.INTERNET_ERR_MSG, AC.INTERNET_ERR_WARN)
            return None