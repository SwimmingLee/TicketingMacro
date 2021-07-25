import sys
from PyQt5.QtWidgets import * #QApplication, QWidget, QLabel, QLineEdit, QDateTimeEdit, QPushButton, QVBoxLayout, QCheckBox, QHBoxLayout
from PyQt5.QtCore import Qt, QDate, QDateTime
from PyQt5.QtGui import QIcon
from interpark_driver import InterparkMacro

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('SwimmingLee Interpark Macro')
        self.setWindowIcon(QIcon('swim_con.png'))

        self.ticketing_info = QLabel('시범용입니다. ', self)
        self.ticketing_info.setAlignment(Qt.AlignCenter)

        self.ticketing_info_font = self.ticketing_info.font()
        self.ticketing_info_font.setPointSize(20)
        self.ticketing_info.setFont(self.ticketing_info_font)

        self.date_time_label = QLabel('Date: ')
        self.date_time_edit = QDateTimeEdit(self, calendarPopup=True)
        self.date_time_edit.setDateTime(QDateTime.currentDateTime())
        self.date_time_edit.setMinimumDateTime(
            QDateTime(2021, 1, 1, 00, 00, 00))
        self.date_time_edit.setMaximumDateTime(
            QDateTime(2030, 12, 31, 00, 00, 00))
        self.date_time_edit.setDisplayFormat('yyyy.MM.dd hh:mm')

        self.id_label = QLabel('ID: ')
        self.id_edit = QLineEdit(self)
        self.id_edit.setPlaceholderText("Set your Interpark ID")

        self.pw_label = QLabel('PW: ')
        self.pw_edit = QLineEdit(self)
        self.pw_edit.setEchoMode(QLineEdit.Password)
        self.pw_edit.setPlaceholderText("Set your Interpark password")

        self.show_label = QLabel('Show Code: ')
        self.show_edit = QLineEdit(self)
        self.show_edit.setPlaceholderText("Set your Interpark show code")

        self.login_btn = QPushButton('Login', self)
        self.login_btn.setCheckable(True)
        self.login_btn.clicked.connect(self.login)

        self.ticketing_btn = QPushButton('Start', self)
        self.ticketing_btn.setCheckable(True)
        self.ticketing_btn.clicked.connect(self.start_ticketing)

        self.safety_booking_check_box = QCheckBox("안심예매", self)

        self.phone_number_label = QLabel('Phone Number: ')
        self.phone_number_edit1 = QLineEdit(self)
        self.phone_number_edit2 = QLineEdit(self)
        self.phone_number_edit3 = QLineEdit(self)
        self.id_edit.setPlaceholderText("Set your Interpark ID")

        self.birth_day_label = QLabel('Brith Day: ')
        self.birth_day_edit = QLineEdit(self)
        self.birth_day_edit.setPlaceholderText("Set your Birth Day")

        # self.check_box.move(20, 20)
        
        layout = QVBoxLayout()
        layout.addWidget(self.ticketing_info)

        layout.addWidget(self.id_label)
        layout.addWidget(self.id_edit)

        layout.addWidget(self.pw_label)
        layout.addWidget(self.pw_edit)

        layout.addWidget(self.show_label)
        layout.addWidget(self.show_edit)

        layout.addWidget(self.date_time_label)
        layout.addWidget(self.date_time_edit)

        layout.addWidget(self.safety_booking_check_box)

        layout.addWidget(self.login_btn)
        layout.addWidget(self.ticketing_btn)

        layout.addWidget(self.phone_number_label)
        
        phone_layout = QHBoxLayout()
        phone_layout.addWidget(self.phone_number_edit1)
        phone_layout.addWidget(self.phone_number_edit2)
        phone_layout.addWidget(self.phone_number_edit3)
        layout.addLayout(phone_layout)

        layout.addWidget(self.birth_day_label)
        layout.addWidget(self.birth_day_edit)

        self.setLayout(layout)

        self.setGeometry(300, 300, 300, 200)    
        self.move(300, 300)
        self.resize(400, 200)
        self.show()

    def get_id(self):
        return self.id_edit.text()

    def get_pw(self):
        return self.pw_edit.text()

    def get_show_id(self):
        return self.show_edit.text()

    def get_want_date(self):
        want_date = self.date_time_edit.date()
        want_year = want_date.year()
        want_month = want_date.month()
        want_day = want_date.day()
        return want_year, want_month, want_day

    def get_want_time(self):
        want_time = self.date_time_edit.time().toString('hh:mm')
        return want_time

    def get_birth_day(self):
        birth_day = self.birth_day_edit.text()
        return birth_day

    def get_phone_number(self):
        phone_number = [self.phone_number_edit1.text(), self.phone_number_edit2.text(), self.phone_number_edit3.text()]
        return phone_number

    def login(self):
        id = self.get_id()
        pw = self.get_pw()
        show_id = self.get_show_id()

        want_year, want_month, want_day = self.get_want_date()
        want_time = self.get_want_time()

        self.driver = InterparkMacro()
        self.driver.login(id, pw, show_id)

        # 안심예매가 아니라면 티켓팅 안내 팝업이 뜬다
        if not self.safety_booking_check_box.isChecked():
            self.driver.close_tickting_info_popup()
        self.driver.click_want_date(want_year, want_month, want_day, want_time)

    def start_ticketing(self):
        birth_day = self.get_birth_day()
        phone_number = self.get_phone_number()
        # self.driver.switch_to.window(self.driver.window_handles[0])
        # self.driver.get_window_position(self.driver.window_handles[0])
        self.driver.click_book_btn()
        self.driver.switching_focus()
        
        if self.safety_booking_check_box.isChecked():
            self.driver.wait_safety_booking()
        else:
            self.driver.close_ticketing_check_popup()

        self.driver.click_want_seat()
        self.driver.click_ticket_price()
        
        self.driver.insert_oder_info(birth_day , phone_number)
        self.driver.click_payment_method('농협(중앙)')
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
