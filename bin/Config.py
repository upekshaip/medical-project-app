class AppConfig(object):
    APP_NAME = "MedSync"
    DB_NAME = "MedSync"
    DB_PATH = f"app/{DB_NAME}/"

    IMAGE_URL_PATH = "http://localhost/web/kusal/img/"
    MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    QR_SCANNER = ""

    INSTITUTE_ADDRESS = "No.585, Kandy Road, Nittambuwa."
    INSTITUTE_PHONE1 = "0332052345"
    INSTITUTE_PHONE2 = "0776970029"
    INSTITUTE_EMAIL = "collegeofalexandriana@gmail.com"

    SETTINGS_JSON_PATH = "config/settings.json"
    LOGO_ICO_PATH = "config/logo.ico"
    CAM_INPUT_ID = 0

    # WARNINGS
    INTERNET_ERR_WARN = "Internet Connection Error"
    INTERNET_ERR_MSG = "Please Connect to the internet. No connection!"


    # PATIENT
    PATIENT_DATA = None
    DOCTOR_DATA = None
    
    
    
    # Admin Accounts
    ACCOUNTS = [{"username": "user1", "password": "pass1"}, {"username": "user2", "password": "pass2"}, {"username": "user3", "password": "pass3"}]
    LOGGED_IN = False