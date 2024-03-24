import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from bin.Runtime import RunTiime as RT
from bin.Config import AppConfig as AC

class MainUI(QMainWindow):

    def __init__(self):
        super(MainUI, self).__init__()
        loadUi("config/ux.ui", self)
        self.setWindowTitle(AC.APP_NAME)
        self.setWindowIcon(QIcon(AC.LOGO_ICO_PATH))
        rt = RT(self)
        rt.buttons()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    app.exec_()