import time
import pyrebase
import math
from bin.Cred import Cred
from bin.Config import AppConfig as AC
from bin.Helper import Helper
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


    def generate_code(self, type):
        if type == "s":
            # user
            try:
                num = random.choices("0123456789", k=6)
                letters = random.choices(string.ascii_uppercase, k=2)
                id = "".join(num + letters)

                data = self.db.child(f"{AC.DB_PATH}/students/{id}").get().val()
                if data:
                    return self.generate_code("s")
                else:
                    return id
            except:
                return None

        if type == "t":
            # teacher
            try:
                num = random.choices("0123456789", k=6)
                letters = random.choices(string.ascii_uppercase, k=2)
                id = "".join(num + letters) + "T"

                data = self.db.child(f"{AC.DB_PATH}/teachers/{id}").get().val()
                if data:
                    return self.generate_code("t")
                else:
                    return id
            except:
                return None

        if type == "e":
            try:
                num = random.choices("0123456789", k=6)
                letters = random.choices(string.ascii_uppercase, k=2)
                id = "".join(num + letters) + "E"
                
                data = self.db.child(f"{AC.DB_PATH}/employees/{id}").get().val()
                if data:
                    return self.generate_code("e")
                else:
                    return id
            except:
                return None
            # employee

        if type == "c":
            # class
            try:
                num = random.choices("0123456789", k=13)
                letters = random.choices(string.ascii_uppercase, k=2)
                id = "".join(num + letters) + "C"

                data = self.db.child(f"{AC.DB_PATH}/classes/{id}").get().val()
                if data:
                    return self.generate_code("c")
                else:
                    return id
            except:
                return None
    
    
    
    
    def add_student(self, data):
        # [st_fname, st_lname, st_code, st_birthday, st_school, st_contact, st_gender, st_g_name, st_g_contact, st_address1, st_address2, reg_classes]
        code = data[2]
        _data = {
            "first_name": data[0],
            "last_name": data[1],
            "student_code": data[2],
            "birthday": data[3],
            "school": data[4],
            "contact": data[5],
            "gender": data[6],
            "g_name": data[7],
            "g_contact": data[8],
            "address_l1": data[9],
            "address_l2": data[10],
            "registered": data[11],
            "ts": str(math.floor(time.time())),
            "password": f"{data[5]}{data[2][-2:]}"
        }
        try:
            self.db.child(f"{AC.DB_PATH}/students/{code}").set(_data)
            print(f"{code} - Student added to the database")
        except:
            self.helper.show_warning_popup(message="No internet connection. Please check your network.",warn="No internet connection")

    def update_student(self, data):
        # [st_fname, st_lname, st_code, st_birthday, st_school, st_contact, st_gender, st_g_name, st_g_contact, st_address1, st_address2, st_role, reg_classes]
        code = data[2]
        _data = {
            "first_name": data[0],
            "last_name": data[1],
            "birthday": data[3],
            "school": data[4],
            "contact": data[5],
            "gender": data[6],
            "g_name": data[7],
            "g_contact": data[8],
            "address_l1": data[9],
            "address_l2": data[10],
            "registered": data[11],
            "password": data[12]
        }
        try:
            self.db.child(f"{AC.DB_PATH}/students/{code}").update(_data)
            print(f"{code} - Student details updated")
        except:
            self.helper.show_warning_popup(message="No internet connection. Please check your network.",warn="No internet connection")
    
    
    def update_teacher(self, data):
        # [teacher_fname, teacher_lname, teacher_code, teacher_birthday, teacher_school, teacher_contact, teacher_gender, teacher_address1, teacher_address2, teacher_password]
        code = data[2]
        _data = {
            "first_name": data[0],
            "last_name": data[1],
            "birthday": data[3],
            "school": data[4],
            "contact": data[5],
            "gender": data[6],
            "address_l1": data[7],
            "address_l2": data[8],
            "password": data[9]
        }
        try:
            self.db.child(f"{AC.DB_PATH}/teachers/{code}").update(_data)
            print(f"{code} - Teacher details updated")
        except:
            self.helper.show_warning_popup(message="No internet connection. Please check your network.",warn="No internet connection")


    def update_class(self, data):
        # data = [cls_code, cls_teacher, cls_subject, cls_grade, cls_year, cls_type, cls_start_date, cls_end_date, cls_status, cls_medium, income_percentage, cls_type, day, cls_hall, start_time, end_time]
        code = data[0]
        _data = {
            "teacher": data[1],
            "subject": data[2],
            "type": data[5],
            "grade": data[3],
            "year": data[4],
            "start_date": data[6],
            "fee": data[7],
            "status": data[8],
            "medium": data[9],
            "percentage": data[10],
            "cls_type": data[11],
            "day": data[12],
            "hall": data[13],
            "start": data[14],
            "end": data[15],
            "group_link": data[16]
        }

        try:
            self.db.child(f"{AC.DB_PATH}/classes/{code}").update(_data)
            print(f"{code} - Class details updated")
        except:
            self.helper.show_warning_popup(message="No internet connection. Please check your network.",warn="No internet connection")

   
    def add_teacher(self, data):
        # [st_fname, st_lname, st_code, st_birthday, st_school, st_contact, st_gender, st_g_name, st_g_contact, st_address1, st_address2]
        code = data[2]
        _data = {
            "first_name": data[0],
            "last_name": data[1],
            "teacher_code": data[2],
            "birthday": data[3],
            "school": data[4],
            "contact": data[5],
            "gender": data[6],
            "address_l1": data[7],
            "address_l2": data[8],
            "ts": str(math.floor(time.time())),
            "password": f"{data[5]}{data[2][-2:]}"
        }
        try:
            self.db.child(f"{AC.DB_PATH}/teachers/{code}").set(_data)
            print(f"{code} - Teacher added to the database")
        except:
            self.helper.show_warning_popup(message="No internet connection. Please check your network.",warn="No internet connection")
        

    def add_class(self, data):
        # data = [cls_code, cls_teacher, cls_subject, cls_grade, cls_year, cls_type, cls_start_date, cls_end_date, cls_status, cls_medium, income_percentage, cls_type, day, cls_hall, start_time, end_time]
        code = data[0]
        _data = {
            "teacher": data[1],
            "class_code": data[0],
            "subject": data[2],
            "type": data[5],
            "grade": data[3],
            "year": data[4],
            "start_date": data[6],
            "fee": data[7],
            "status": data[8],
            "medium": data[9],
            "ts": str(math.floor(time.time())),
            "percentage": data[10],
            "cls_type": data[11],
            "day": data[12],
            "hall": data[13],
            "start": data[14],
            "end": data[15],
            "group_link": data[16]
        }
        try:
            self.db.child(f"{AC.DB_PATH}/classes/{code}").set(_data)
            print(f"{code} - Class added to the database")
        except:
            self.helper.show_warning_popup(message="No internet connection. Please check your network.",warn="No internet connection")

    
    def get_all_teachers(self):
        try:
            data = self.db.child(f"{AC.DB_PATH}/teachers").get().val()
            if type(data) == list:
                return None
            elif data:
                return dict(data)
            else:
                return None
        except:
            return None

    def get_classes(self):
        try:
            data = self.db.child(f"{AC.DB_PATH}/classes").get().val()
            if type(data) == list:
                return None
            elif data:
                return dict(data)
            else:
                return None
        except:
            return None

    def get_all_students(self):
        try:
            data = self.db.child(f"{AC.DB_PATH}/students").get().val()
            if type(data) == list:
                return None
            elif data:
                return dict(data)
            else:
                return None
        except:
            return None

    def get_student_details(self, id):
        try:
            data = self.db.child(f"{AC.DB_PATH}/students/{id}").get().val()
            if data:
                return dict(data)
            else:
                return None
        except:
            return None

    def get_teacher_details(self, id):
        try:
            data = self.db.child(f"{AC.DB_PATH}/teachers/{id}").get().val()
            if data:
                return dict(data)
            else:
                return None
        except:
            return None

    def get_class_details(self, id):
        try:
            data = self.db.child(f"{AC.DB_PATH}/classes/{id}").get().val()
            if data:
                return dict(data)
            else:
                return None
        except:
            return None

    def student_payment(self, student_id, cls, month, fee):
        if month != "" and fee != "":

            _data = {
                "ts": str(math.floor(time.time())),
                "fee": fee,
                "month": str(month),
                "class_code": cls
            }
            try:
                self.db.child(f"{AC.DB_PATH}/payments/{student_id}/{cls}/{str(month)}").set(_data)
            except:
                self.helper.show_warning_popup(message="No internet connection. Please check your network.",warn="No internet connection")

    
    def get_student_payment_details(self, student_id):
        try:
            data = self.db.child(f"{AC.DB_PATH}/payments/{student_id}").get().val()
            if type(data) == list:
                return None
            elif data:
                return dict(data)
            else:
                return None
        except:
            return None 

    def get_all_payments(self):
        try:
            data = self.db.child(f"{AC.DB_PATH}/payments").get().val()
            if type(data) == list:
                return None
            elif data:
                return dict(data)
            else:
                return None
        except:
            return None
        
    def get_dash_data(self):
        student_data = self.get_all_students()
        st_data = {}
        if student_data:
            st_data = student_data

        class_data = self.get_classes()

        teacher_data = self.get_all_teachers()
        teach_data = {}
        if teacher_data:
            teach_data = teacher_data

        active_cls = []
        inactive_cls = []
        if class_data:
            active_cls = [{cls:val} for cls, val in class_data.items() if cls != "0" and val["status"] == "active"]
            inactive_cls = [{cls:val} for cls, val in class_data.items() if cls != "0" and val["status"] == "inactive"]

        return st_data, teach_data, active_cls, inactive_cls
    
    # def get_usernames()