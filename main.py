import sys
from database import *

from PyQt5.QtWidgets import QApplication, QFrame, QWidget, QMainWindow, QMessageBox
from PyQt5.QtWidgets import QStackedWidget, QHBoxLayout, QLabel

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


app = QApplication(sys.argv)
main_window = QMainWindow()
main_window.setWindowTitle("Intelligent Course Management System")

from login_gui import login_widget
from main_gui import main_widget

main_stack = QStackedWidget()
main_stack.addWidget(login_widget)
main_stack.addWidget(main_widget)

def login():
    # Write login logic here (scan face -> if recognized redirect to main page)
    # For now, it will always redirect to main page (login page = 0, main page = 1)
    main_stack.setCurrentIndex(1)

def logout():
    # TODO Write logic to update logout time
    main_stack.setCurrentIndex(0)

login_widget.login_button.clicked.connect(login)
main_widget.logout_button.clicked.connect(logout)

main_window.setCentralWidget(main_stack)

main_window.resize(850, 534)
main_window.setMaximumSize(850, 534)
main_window.setMinimumSize(850, 534)

main_window.show()

sys.exit(app.exec_())



