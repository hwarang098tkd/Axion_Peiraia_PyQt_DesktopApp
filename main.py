from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import Qt, QRect, QPropertyAnimation, QPoint, QParallelAnimationGroup, QDateTime, QDate
from login_main import Ui_MainWindow
import google_calendar
import sys
import login_query


class LoginWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global buttons_style
        buttons_style = "QToolTip { background-color: black } QPushButton { border-left: 5px solid #88b1b2; border-radius: 13px 0px 0px 13px; background-color: #116466} "
        global widgets
        widgets = self.ui
        global start_pos_x
        start_pos_x = 150
        global start_pro_y
        start_pro_y = 150
        self.baseHeight = 369
        self.extendedHeight = 400
        self.rect = QRect(start_pos_x, start_pro_y, 320, self.baseHeight)
        self.setGeometry(self.rect)
        # this will hide the title bar
        self.setWindowFlag(Qt.FramelessWindowHint)
        widgets.toggle_bt.clicked.connect(self.buttonClick)
        widgets.home_bt.clicked.connect(self.buttonClick)
        widgets.taek_bt.clicked.connect(self.buttonClick)
        widgets.fencing_bt.clicked.connect(self.buttonClick)
        widgets.oplo_bt.clicked.connect(self.buttonClick)
        widgets.eco_bt.clicked.connect(self.buttonClick)
        widgets.prese_bt.clicked.connect(self.buttonClick)
        widgets.members_bt.clicked.connect(self.buttonClick)
        ####################################################
        widgets.login_btn.clicked.connect(self.pressed)
        ####################################################
        widgets.main_exit_btn.clicked.connect(self.close)  # doesnt need def(function)
        widgets.minim_btn.clicked.connect(self.showMinimized)  # doesnt need def(function)
        ####################################################
        widgets.main_exit2_btn.clicked.connect(self.close)  # doesnt need def(function)
        widgets.minim2_btn.clicked.connect(self.showMinimized)  # doesnt need def(function)
        ####################################################
        self.installEventFilter(self)
        self.displayTime()
        widgets.toolBar_fm.hide()
        self.show()

    def displayTime(self):
        now = QDate.currentDate()
        widgets.title_date.setText(now.toString(Qt.DefaultLocaleLongDate))

    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "home_bt":
            widgets.stackedWidget.setCurrentWidget(widgets.home_page)
            resetStyle(self, btnName)
            btn.setStyleSheet(buttons_style)

        # SHOW TKD PAGE
        if btnName == "taek_bt":
            widgets.stackedWidget.setCurrentWidget(widgets.taekwondo_page)
            resetStyle(self, btnName)
            btn.setStyleSheet(buttons_style)

        # SHOW FENCING PAGE
        if btnName == "fencing_bt":
            widgets.stackedWidget.setCurrentWidget(widgets.fencing_page)
            resetStyle(self, btnName)
            btn.setStyleSheet(buttons_style)

        # SHOW OPLOMAXIA PAGE
        if btnName == "oplo_bt":
            widgets.stackedWidget.setCurrentWidget(widgets.oplomaxia_page)
            resetStyle(self, btnName)
            btn.setStyleSheet(buttons_style)

        # SHOW ECONOMICS PAGE
        if btnName == "eco_bt":
            widgets.stackedWidget.setCurrentWidget(widgets.econ_page)
            resetStyle(self, btnName)
            btn.setStyleSheet(buttons_style)

        # SHOW PRESENTERS PAGE
        if btnName == "prese_bt":
            widgets.stackedWidget.setCurrentWidget(widgets.presenters_page)
            resetStyle(self, btnName)
            btn.setStyleSheet(buttons_style)

        # SHOW MEMBERS PAGE
        if btnName == "members_bt":
            widgets.stackedWidget.setCurrentWidget(widgets.menbers_page)
            resetStyle(self, btnName)
            btn.setStyleSheet(buttons_style)

    def pressed(self):
        if (widgets.user_tb.text() == "" or widgets.user_tb.text() == "Username") and (
                widgets.pass_tb.text() == "" or widgets.pass_tb.text() == "Password"):
            widgets.info_lb.setText("No username and password")
            print("No username and password inserted")
        elif widgets.user_tb.text() == "" or widgets.user_tb.text() == "Username":
            widgets.info_lb.setText("no username")
            print("No username inserted")
        elif widgets.pass_tb.text() == "" or widgets.pass_tb.text() == "Password":
            print("No password inserted")
            widgets.info_lb.setText("no password")
        else:
            widgets.info_lb.setText("")
            widgets.info_lb.setStyleSheet("color: white")
            result = login_query.connection.login_connection(self, widgets.user_tb.text(), widgets.pass_tb.text())
            self.refresh_calendar()  # refresh calendar
            widgets.info_lb.setText(result)

            if result == "Connection established":
                # REFRESH STASTS
                self.refresh_stats()

                # Re-COLOR MAIN TOOLBAR
                widgets.maintoolbar_fm.setStyleSheet("background-color: \'#0d5051\';")
                # Re-COLOR MAIN BOT TOOLBAR
                widgets.maintoolbarBot_fm.setStyleSheet("background-color: \'#0d5051\';")

                animation_time = 300
                end_height = 800
                end_width = 1050
                # ANIMATION WINDOW
                self.main_window = QPropertyAnimation(self, b'geometry')
                self.main_window.setDuration(animation_time + 200)
                self.main_window.setStartValue(QRect(start_pos_x, start_pro_y, 320, 369))
                self.main_window.setEndValue(QRect(start_pos_x, start_pro_y, end_width, end_height))

                # ANIMATION MAIN TOOLBAR FRAME
                self.maintoolbar_fm = QPropertyAnimation(self.ui.maintoolbar_fm, b'geometry')
                self.maintoolbar_fm.setDuration(animation_time)
                self.maintoolbar_fm.setStartValue(QRect(0, 0, 1111, 35))
                self.maintoolbar_fm.setEndValue(QRect(0, 0, end_width, 35))

                # ANIMATION MAIN BOT TOOLBAR FRAME
                self.maintoolbarBot_fm = QPropertyAnimation(self.ui.maintoolbarBot_fm, b'geometry')
                self.maintoolbarBot_fm.setDuration(animation_time)
                self.maintoolbarBot_fm.setStartValue(QRect(0, 800 - 35, 1111, 35))
                self.maintoolbarBot_fm.setEndValue(QRect(0, 800 - 35, end_width, 35))

                # ANIMATION LOGIN FRAME
                self.basic_fm_1 = QPropertyAnimation(self.ui.login_fm, b'geometry')
                self.basic_fm_1.setDuration(animation_time)
                self.basic_fm_1.setStartValue(QRect(0, 0, 320, 369))
                self.basic_fm_1.setEndValue(QRect(0, 0, 60, end_height))

                # ANIMATION MAIN FRAME
                self.basic_fm_2 = QPropertyAnimation(self.ui.main_fm, b'geometry')
                self.basic_fm_2.setDuration(animation_time)
                self.basic_fm_2.setStartValue(QRect(0, 0, 300, 369))
                self.basic_fm_2.setEndValue(QRect(0, 0, end_width, end_height))

                # GROUP ANIMATION
                self.group = QParallelAnimationGroup()
                self.group.addAnimation(self.main_window)
                self.group.addAnimation(self.maintoolbar_fm)
                self.group.addAnimation(self.maintoolbarBot_fm)
                self.group.addAnimation(self.basic_fm_1)
                self.group.addAnimation(self.basic_fm_2)
                self.group.start()
                ######################################################
                widgets.toolBar_fm.show()

    def refresh_calendar(self):
        calendar_list = google_calendar.calendar_data.main(self)
        print("Calendar List:")
        print(calendar_list)

    def refresh_stats(self):
        # MEMBERS STATS
        members_array = login_query.connection.login_members_stats(self, widgets.user_tb.text(), widgets.pass_tb.text())
        widgets.sum_members.setText(str(members_array[0]))
        widgets.sum_tkd.setText(str(members_array[1]))
        widgets.sum_fencing.setText(str(members_array[2]))
        widgets.sum_oplo.setText(str(members_array[3]))
        # PRESENTERS STATS
        prese_array = login_query.connection.login_presents_stats(self, widgets.user_tb.text(), widgets.pass_tb.text())
        widgets.sum_pres.setText(str(prese_array[0]))
        widgets.sum_tkd_pre.setText(str(prese_array[1]))
        widgets.sum_fencing_pre.setText(str(prese_array[2]))
        widgets.sum_oplo_pre.setText(str(prese_array[3]))
        # ECONOMICS STATS
        econ_array = login_query.connection.login_economics_stats(self, widgets.user_tb.text(), widgets.pass_tb.text())
        widgets.sum_eco_lb.setText(str(econ_array[0]))
        widgets.tkd_eco_lb.setText(str(econ_array[1]))
        widgets.fencing_eco_lb.setText(str(econ_array[2]))
        widgets.oplo_eco_lb.setText(str(econ_array[3]))
        widgets.expe_eco_lb.setText(str(econ_array[4]))

    def keyPressEvent(self, qKeyEvent):  # αναγνωριζει τα enter και καλει την συναρτηση οταν πατιεται το login button
        print(qKeyEvent.key())
        if qKeyEvent.key() == Qt.Key_Return or qKeyEvent.key() == Qt.Key_Enter:
            self.pressed()
            print('Enter pressed')

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


def resetStyle(self, btnName):
    for w in self.ui.toolBar_fm.findChildren(QPushButton):
        if w.objectName() != btnName:
            w.setStyleSheet("")
    print("resetStyle")


# Create the application object
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    sys.exit(app.exec_())
