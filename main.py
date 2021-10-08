from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

import sys

from login_main import Ui_MainWindow


class LoginWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui
        # this will hide the title bar
        self.setWindowFlag(Qt.FramelessWindowHint)
        widgets.pushButton.clicked.connect(self.pressed)
        widgets.main_exit_btn.clicked.connect(self.close) #doesnt need def(function)
        widgets.minim_btn.clicked.connect(self.showMinimized) #doesnt need def(function)

        self.show()


    def pressed(self):
        print("Login Button clicked")
        if (widgets.lineEdit.text() == "" or widgets.lineEdit.text() == "Username") and (widgets.lineEdit_2.text() == "" or widgets.lineEdit_2.text() == "Password"):
            widgets.info_lb.setText("No username and password")
            print("No username and password inserted")
        elif widgets.lineEdit.text() == "" or widgets.lineEdit.text() == "Username":
            widgets.info_lb.setText("no username")
            print("No username inserted")
        elif widgets.lineEdit_2.text() == "" or widgets.lineEdit_2.text() == "Password":
            print("No password inserted")
            widgets.info_lb.setText("no password")
        else:
            widgets.info_lb.setText("")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)



# Create the application object
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    sys.exit(app.exec_())
