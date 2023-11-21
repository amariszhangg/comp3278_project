from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from datetime import datetime
import database
import data

home_widget = QWidget()

home_layout = QVBoxLayout()
home_layout.setAlignment(Qt.AlignCenter)

home_widget.setLayout(home_layout)

label = QLabel("abc")
home_layout.addWidget(label)

welcome = QLabel()
home_layout.addWidget(welcome)
welcome.setAlignment(Qt.AlignCenter)
welcome.setFont(QFont('Arial', 70))

login = QLabel()
home_layout.addWidget(login)

stay = QLabel()
home_layout.addWidget(stay)


# check if you have class
def check_class():  
    lecture = database.getUpcomingClass(data.student_id)
    if lecture:
        course_code = lecture[0]
        start_time = lecture[1]
        time_diff = start_time - datetime.now()
        if time_diff.total_seconds() // 60 <= 60:
            return f"You have {course_code} in the next hour at {start_time.time()}"  + \
                f"Please see the relevant course materials."
    
    return "No class in the next hour."


# update homepage
def update_home_content():
    label.setText(check_class())  
    #show name 
    student_name = database.getStudent(data.student_id)[1]
    welcome.setText(f"Hello {student_name}")
    #show last login time
    last_login = database.LoginTime(data.student_id)
    login.setText(f"Last login: {last_login}")
    #show how long does the user stay
    staytime = database.StayTime(data.student_id)
    stay.setText(f"Stay Time: {staytime}")
