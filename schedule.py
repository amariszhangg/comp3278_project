from PyQt5.QtWidgets import QApplication, QFrame, QWidget, QMainWindow, QMessageBox, QLabel
from PyQt5.QtWidgets import QStackedWidget, QTableWidget
from PyQt5.QtWidgets import QWidget, QStackedWidget
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QTableWidgetItem
from PyQt5.QtCore import Qt, QSize

from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt
import math
import database

schedule_widget = QWidget()

schedule_layout = QVBoxLayout()
schedule_layout.setAlignment(Qt.AlignCenter)

schedule = QTableWidget()
schedule.setColumnCount(8)
schedule.setRowCount(28)
schedule.verticalHeader().hide()
schedule.setHorizontalHeaderLabels(("", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"))

for i in range(14):
    schedule.setSpan(i * 2, 0, 2, 1)
    time = f"0{i+8}:00"
    if (i >= 2):
        time = f"{i+8}:00"
    time_item = QTableWidgetItem(time)
    time_item.setFlags(Qt.ItemIsEnabled)
    schedule.setItem(i * 2, 0, time_item)

student_schedule = database.getSchedule(1)

for student_course in student_schedule:
    course_code = student_course[0]
    start_date_time = student_course[1]
    end_date_time = student_course[2]
    venue = student_course[3]

    column = start_date_time.isoweekday()

    row = math.ceil((start_date_time.hour - 8) * 60 / 30) + 1
    rowSpan = math.ceil((end_date_time - start_date_time).seconds / 60 / 30)

    schedule.setSpan(row, column, rowSpan, 1)
    time_item = QTableWidgetItem(f"{course_code}\n{venue}")
    time_item.setFlags(Qt.ItemIsEnabled)
    time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    time_item.setBackground(QColor("#4AA080"))
    schedule.setItem(row, column, time_item)
    
schedule_layout.addWidget(schedule)


schedule_widget.setLayout(schedule_layout)
