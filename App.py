import sys
# from bin.Runtime import RunTiime as RT
# pyqt
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

# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle("Tree Widget Example")
#         self.setGeometry(100, 100, 400, 300)

#         self.treeWidget = QTreeWidget(self)
#         self.treeWidget.setHeaderLabels(["Key", "Value"])
#         self.setCentralWidget(self.treeWidget)

#         # Adding top-level items
#         item1 = QTreeWidgetItem(self.treeWidget, ["Item 1", "Value 1"])
#         item2 = QTreeWidgetItem(self.treeWidget, ["Item 2", "Value 2"])

#         # Adding child items
#         child1 = QTreeWidgetItem(item1, ["Child 1", "Child Value 1"])
#         child2 = QTreeWidgetItem(item1, ["Child 2", "Child Value 2"])

#         # Adding more child items
#         subchild1 = QTreeWidgetItem(child2, ["Subchild 1", "Subchild Value 1"])
#         subchild2 = QTreeWidgetItem(child2, ["Subchild 2", "Subchild Value 2"])

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())
