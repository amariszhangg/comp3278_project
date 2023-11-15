from PyQt5.QtWidgets import QApplication, QFrame, QWidget, QMainWindow, QMessageBox
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QWidget, QStackedWidget
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QSize

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

main_widget = QWidget()

nav_layout = QVBoxLayout()

navbar = QWidget()
navbar.setLayout(nav_layout)
navbar.setStyleSheet('''
    QWidget {
        background-color: #4AA080;
    }
''')
button_stylesheet = '''
            QToolButton {
                background-color: #4AA080;
                color: white;
                border: 0;
                border-radius: 5px;
                width: 100%;
                padding: 10px;
            }

            QToolButton:hover {
                background-color: #34AD81;
            }
        '''


home_button = QToolButton()
home_button.setText("Home")
home_button.setIcon(QIcon('assets/home.png'))
home_button.setIconSize(QSize(35, 35))
home_button.setStyleSheet(button_stylesheet)
home_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

timetable_button = QToolButton()
timetable_button.setText("Timetable")
timetable_button.setIcon(QIcon('assets/calendar.png'))
timetable_button.setIconSize(QSize(35, 35))
timetable_button.setStyleSheet(button_stylesheet)
timetable_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

course_button = QToolButton()
course_button.setText("Course")
course_button.setIcon(QIcon('assets/course.png'))
course_button.setIconSize(QSize(35, 35))
course_button.setStyleSheet(button_stylesheet)
course_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

logout_button = QToolButton()
logout_button.setText("Logout")
logout_button.setIcon(QIcon('assets/logout.png'))
logout_button.setIconSize(QSize(35, 35))
logout_button.setStyleSheet(button_stylesheet)
logout_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
main_widget.logout_button = logout_button

nav_layout.addWidget(home_button)
nav_layout.addWidget(timetable_button)
nav_layout.addWidget(course_button)
nav_layout.addWidget(logout_button)

stack = QStackedWidget()

from home import home_widget
from schedule import schedule_widget
from course import course_widget

stack.addWidget(home_widget)
stack.addWidget(schedule_widget)
stack.addWidget(course_widget)

# default as home
stack.setCurrentIndex(0)

def switch_tab_generator(i):
    return lambda : stack.setCurrentIndex(i)

home_button.clicked.connect(switch_tab_generator(0))
timetable_button.clicked.connect(switch_tab_generator(1))
course_button.clicked.connect(switch_tab_generator(2))

main_layout = QHBoxLayout()
main_layout.addWidget(navbar)
main_layout.addWidget(stack)
main_layout.setStretch(0, 1)
main_layout.setStretch(1, 9)

main_widget.setLayout(main_layout)