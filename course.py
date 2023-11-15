from PyQt5.QtWidgets import QApplication, QFrame, QWidget, QMainWindow, QMessageBox, QLabel
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QWidget, QStackedWidget
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QSize

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

course_widget = QWidget()

course_layout = QVBoxLayout()
course_layout.setAlignment(Qt.AlignCenter)

course_layout.addWidget(QLabel("This is course page"))

course_widget.setLayout(course_layout)
