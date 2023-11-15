from PyQt5.QtWidgets import QApplication, QFrame, QWidget, QMainWindow, QLabel
from PyQt5.QtWidgets import QStackedWidget, QTextEdit 
from PyQt5.QtWidgets import QWidget, QStackedWidget
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QSize

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

home_widget = QWidget()

home_layout = QVBoxLayout()
home_layout.setAlignment(Qt.AlignCenter)

home_layout.addWidget(QLabel("This is home page"))

home_widget.setLayout(home_layout)