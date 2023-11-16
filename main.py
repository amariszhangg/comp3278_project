import sys
import database
from PyQt5.QtWidgets import QApplication, QFrame, QWidget, QMainWindow, QMessageBox
from PyQt5.QtWidgets import QStackedWidget, QHBoxLayout, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import tkinter.messagebox as MessageBox
from tkinter import *
import urllib
import numpy as np
import mysql.connector
import cv2
import pyttsx3
import pickle
from datetime import datetime
import sys
import os
from dotenv import load_dotenv

app = QApplication(sys.argv)
main_window = QMainWindow()
main_window.setWindowTitle("Intelligent Course Management System")

from login_gui import login_widget
from main_gui import main_widget

main_stack = QStackedWidget()
main_stack.addWidget(login_widget)
main_stack.addWidget(main_widget)

load_dotenv()


def login():
    user_input = login_widget.e_id.text()
    if user_input == "":
        QMessageBox.information(login_widget, "Insert Status", "All fields are required")
    else:
        user = database.getStudent(user_input)
        if user is not None:
            logedin_user = user
            with open("FaceRecognition/faces.py", 'r') as file:
                code = file.read()
                exec(code)
            main_stack.setCurrentIndex(1)
        else:
            QMessageBox.critical(login_widget, "Oops", "User not found in database.")

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
