import time
import pyrebase
import math
from datetime import datetime
from bin.Cred import Cred
from bin.Config import AppConfig as AC
from bin.Helper import Helper
from requests.exceptions import ConnectionError
import random
import string

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
        
