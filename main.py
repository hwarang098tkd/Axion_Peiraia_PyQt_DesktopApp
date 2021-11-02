import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRect, QPropertyAnimation, QParallelAnimationGroup, QDate
from PyQt5 import QtGui, QtWidgets

import login_main
from login_main import Ui_MainWindow
import google_calendar
import sys
import login_query

global members_list
global ids


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
        widgets.tkd_rb.clicked.connect(self.radio_refresh)
        widgets.all_rb.clicked.connect(self.radio_refresh)
        widgets.fencing_rb.clicked.connect(self.radio_refresh)
        widgets.olpo_rb.clicked.connect(self.radio_refresh)
        ####################################################
        widgets.members_cbb.currentIndexChanged.connect(self.list_names_combobox)
        widgets.new_member_btn.clicked.connect(self.new_btn)
        self.installEventFilter(self)
        self.displayTime()
        widgets.toolBar_fm.hide()
        widgets.home_bt.setStyleSheet(buttons_style)

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
        if calendar_list[0] == "empty":
            print("No Calendar Events")
            widgets.calendar_error_lb.setText("No Calendar Events")
        else:
            print("Calendar List:")
            print(calendar_list)
            print("Each Item:")
            for item in calendar_list:
                dayWeek = datetime.datetime.strptime(item[0], '%d-%m-%Y').strftime('%A')
                print(item[0], dayWeek, item[1], item[2], item[3])
                if dayWeek == 'Monday':
                    pass
                elif dayWeek == 'Tuesday':
                    pass
                elif dayWeek == 'Wednesday':
                    pass
                elif dayWeek == 'Thursday':
                    pass
                elif dayWeek == 'Friday':
                    print("Friday event added")
                    # layout1 = QFormLayout()
                    # layout1.setGeometry(QRect(0, 0, 128, 280))
                    # spacerr = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Fixed)
                    # item1 = QLabel(item[3])
                    # item2 = QLabel(item[1])
                    # item3 = QLabel(item[0])
                    # layout1.addItem(spacerr)
                    # layout1.addWidget(item1)
                    # layout1.addWidget(item2)
                    # layout1.addWidget(item3)
                    #
                    # widgets.friday_fm.setLayout(layout1)
                    # item1.setStyleSheet('''color: rgb(0, 0, 0);background-color: '#2c3531';''')
                    # item2.setStyleSheet('''color: rgb(0, 0, 0);background-color: '#2c3531';''')
                    # item3.setStyleSheet('''color: rgb(0, 0, 0);background-color: '#2c3531';''')
                    # item1.setFixedSize(131, 25)
                    # item2.setFixedSize(131, 25)
                    # item3.setFixedSize(131, 25)
                    # item1.setAlignment(Qt.AlignCenter)
                    # item2.setAlignment(Qt.AlignCenter)
                    # item3.setAlignment(Qt.AlignCenter)

                elif dayWeek == 'Saturday':
                    pass
                elif dayWeek == 'Saturday':
                    pass
            print("##################### END of Calendar event List ##############################")

    def refresh_stats(self):
        # MEMBERS STATS
        members_array = login_query.connection.login_members_stats(self, widgets.user_tb.text(), widgets.pass_tb.text())
        # home page
        widgets.sum_members.setText(str(members_array[0]))
        widgets.sum_tkd.setText(str(members_array[1]))
        widgets.sum_fencing.setText(str(members_array[2]))
        widgets.sum_oplo.setText(str(members_array[3]))
        # members page
        widgets.members_sum_lb.setText(str(members_array[0]))
        widgets.members_tkd_lb.setText(str(members_array[1]))
        widgets.members_fenc_lb.setText(str(members_array[2]))
        widgets.members_oplo_lb.setText(str(members_array[3]))
        # # #
        self.radio_refresh()
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

    def radio_refresh(self):
        widgets.members_cbb.clear()
        members_list = login_query.connection.login_members_names(self, widgets.user_tb.text(), widgets.pass_tb.text(),sport_definition(self))
        widgets.members_cbb.addItems(members_list)
        self.clear_editlines()
        widgets.add_ref_btn.setText("ΚΑΤΑΧΩΡΗΣΗ")

    def new_btn(self):
        self.clear_editlines()
        self.reset_combobox()
        widgets.add_ref_btn.setText("ΚΑΤΑΧΩΡΗΣΗ")

    def reset_combobox(self):
        widgets.members_cbb.setCurrentIndex(0)

    def clear_editlines(self):
        list_empty = []
        list_empty2 = []
        for i in range(0, 25):
            list_empty2.append("-")
        list_empty.append(list_empty2)
        self.put_info(list_empty)

    def list_names_combobox(self):
        name = widgets.members_cbb.currentText()
        info_list = login_query.connection.member_info(self, widgets.user_tb.text(), widgets.pass_tb.text(), name)
        if info_list:
            self.put_info(info_list)
        widgets.add_ref_btn.setText("ΕΝΗΜΕΡΩΣΗ")

    def put_info(self, list):
        print(list)
        widgets.LAST_NAME.setText(list[0][1])
        widgets.FIRST_NAME.setText(list[0][2])
        widgets.FATHER_NAME.setText(list[0][3])
        widgets.MOTHER_NAME.setText(list[0][4])
        widgets.BIRTHDATE.setText(list[0][5])
        widgets.BIRTH_PLACE.setText(list[0][6])
        widgets.NATIONALITY.setText(list[0][7])
        widgets.PROFESSION.setText(list[0][8])
        widgets.ID_NUMBER.setText(list[0][9])
        widgets.ADDRESS_STREET.setText(list[0][10])
        widgets.ADDRESS_NUMBER.setText(list[0][11])
        widgets.REGION.setText(list[0][12])
        widgets.HOME_PHONE.setText(list[0][13])
        widgets.MOTHER_PHONE.setText(list[0][14])
        widgets.FATHER_PHONE.setText(list[0][15])
        widgets.EMAIL.setText(list[0][16])
        widgets.SPORT.setText(list[0][17])
        widgets.DATE_SUBSCRIBE.setText(list[0][18])
        widgets.EMERG_PHONE.setText(list[0][19])
        widgets.BARCODE.setText(list[0][20])
        widgets.CELL_PHONE.setText(list[0][21])
        widgets.BARCODE_1.setText(list[0][22])
        widgets.SPORT_1.setText(list[0][23])
        widgets.PAY_DAY.setText(str(list[0][24]))

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
        try:
            if self.offset is not None and event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.pos() - self.offset)
            else:
                super().mouseMoveEvent(event)
        except Exception as e:
            print("error raised on mouseMoveEvent")

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)


def sport_definition(self):
    if widgets.olpo_rb.isChecked():
        sport = "OPLOMAXIA"
    elif widgets.all_rb.isChecked():
        sport = "SPORT"
    elif widgets.fencing_rb.isChecked():
        sport = "FENCING"
    elif widgets.tkd_rb.isChecked():
        sport = "TAEKWON-DO"
    print("Radio BTN selected:", sport)
    return sport
    # for i in range(widgets.radio_btns_layout.count()):
    #     radio_button=widgets.radio_btns_layout.itemAt(i).widget()
    #
    #     #print(radio_button.objectName(), radio_button.isChecked())


def resetStyle(self, btnName):
    for w in self.ui.toolBar_fm.findChildren(QPushButton):
        if w.objectName() != btnName:
            w.setStyleSheet("")


# Create the application object
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    sys.exit(app.exec_())
