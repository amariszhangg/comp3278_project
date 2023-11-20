from PyQt5.QtWidgets import QApplication, QFrame, QWidget, QMainWindow, QLabel
from PyQt5.QtWidgets import QStackedWidget, QTextEdit 
from PyQt5.QtWidgets import QWidget, QStackedWidget
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QSize

from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import database
from datetime import datetime
import data

home_widget = QWidget()

home_layout = QVBoxLayout()
home_layout.setAlignment(Qt.AlignCenter)

home_widget.setLayout(home_layout)

label = QLabel("abc")
home_layout.addWidget(label)

# change to imported student id
def check_class():
    lecture = database.getUpcomingClass(data.student_id)

    print(data.student_id)

    if (lecture != None):
        course_code = lecture[0]
        start_time = lecture[1]
        time_diff = start_time - datetime.now()
        if time_diff.total_seconds() // 60 <= 60:
            return f"You have {course_code} in the next hour at {start_time.time()}"  + \
                f"Please see the relevant course materials."
    
    return "No class in the next hour."

def update_home_content():
    label.setText(check_class())
    
    student_name = database.getStudent(data.student_id)[1]
    welcome = QLabel()
    welcome.setText(f"Hello {student_name}")
    home_layout.addWidget(welcome)
    welcome.setAlignment(Qt.AlignCenter)
    welcome.setFont(QFont('Arial', 70))

    last_login = database.LoginTime(data.student_id)
    login = QLabel()
    login.setText(f"Last login: {last_login}")
    home_layout.addWidget(login)
