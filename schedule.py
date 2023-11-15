from PyQt5.QtWidgets import QApplication, QFrame, QWidget, QMainWindow, QMessageBox, QLabel
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QWidget, QStackedWidget
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QSize

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

schedule_widget = QWidget()

schedule_layout = QVBoxLayout()
schedule_layout.setAlignment(Qt.AlignCenter)

schedule_layout.addWidget(QLabel("This is schedule page"))

schedule_widget.setLayout(schedule_layout)
