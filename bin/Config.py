class AppConfig(object):
    APP_NAME = "MedSync"
    DB_NAME = "MedSync"
    DB_PATH = f"app/{DB_NAME}/"

    IMAGE_URL_PATH = "http://localhost/web/kusal/img/"
    IMAGE_UPLOAD_API_URL = "http://localhost/web/kusal/includes/api.inc.php"

    MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    REPORT_TYPES = ["Prescription","Referral Letter", "Diagnosis","Treatment Plan", "Lab Test Result", "Surgery","Imaging Test Result", "Therapy Session Notes", "Follow-up Instructions", "Medical Procedure", "Medical History", "Immunization Record"]
    QR_SCANNER = ""
    DISTRICTS = ["Ampara","Anuradhapura","Badulla","Batticaloa","Colombo","Galle","Gampaha","Hambantota","Jaffna","Kalutara","Kandy","Kegalle","Kilinochchi","Kurunegala","Mannar","Matale","Matara","Monaragala","Mullaitivu","Nuwara Eliya","Polonnaruwa","Puttalam","Ratnapura","Trincomalee","Vavuniya"]
    

    INSTITUTE_ADDRESS = "55/1, Pitipana"
    INSTITUTE_PHONE1 = "0332052345"
    INSTITUTE_PHONE2 = "0776970029"
    INSTITUTE_EMAIL = "medsync0@gmail.com"

    SETTINGS_JSON_PATH = "config/settings.json"
    LOGO_ICO_PATH = "config/logo.ico"
    CAM_INPUT_ID = 0

    # WARNINGS
    INTERNET_ERR_WARN = "Internet Connection Error"
    INTERNET_ERR_MSG = "Please Connect to the internet. No connection!"


    # PATIENT
    PATIENT_DATA = None
    DOCTOR_DATA = None
    SERVICE_ACCOUNT_LOGGED = None
    
    # EMAIL STM
    EMAIL = "medsync0@gmail.com"
    EMAIL_PASSWORD = "cjusazqsyoavqkgy"
    EMAIL_SUBJECT = "Your MedSync User ID Card"

    # Admin Accounts
    ACCOUNTS = [{"username": "user1", "password": "pass1"}, {"username": "user2", "password": "pass2"}, {"username": "user3", "password": "pass3"}]
    LOGGED_IN = False