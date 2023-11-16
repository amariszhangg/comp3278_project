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

def recognize_faces():
    # Create database connection
    myconn = mysql.connector.connect(host="localhost",
        user=os.environ["MYSQL_USER"],
        passwd=os.environ["MYSQL_PASSWORD"],
        database=os.environ["MYSQL_DATABASE"])
    date = datetime.utcnow()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    cursor = myconn.cursor()

    # Load recognize and read label from model
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("FaceRecognition/train.yml")

    labels = {"person_name": 1}
    with open("FaceRecognition/labels.pickle", "rb") as f:
        labels = pickle.load(f)
        labels = {v: k for k, v in labels.items()}

    # Create text-to-speech engine
    engine = pyttsx3.init()
    rate = engine.getProperty("rate")
    engine.setProperty("rate", 175)

    # Define camera and detect face
    face_cascade = cv2.CascadeClassifier('FaceRecognition/haarcascade/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            id_, conf = recognizer.predict(roi_gray)

            if conf >= 30:
                font = cv2.QT_FONT_NORMAL
                id = 0
                id += 1
                name = labels[id_]
                current_name = name
                color = (255, 0, 0)
                stroke = 2
                cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))

                select = "SELECT student_id, name, DAY(login_date), MONTH(login_date), YEAR(login_date) FROM Student WHERE name='%s'" % (name)
                name = cursor.execute(select)
                result = cursor.fetchall()
                data = "error"

                for x in result:
                    data = x

                if data == "error":
                    print("The student", current_name, "is NOT FOUND in the database.")
                else:
                    # Update the data in the database
                    update = "UPDATE Student SET login_date=%s WHERE name=%s"
                    val = (date, current_name)
                    cursor.execute(update, val)
                    update = "UPDATE Student SET login_time=%s WHERE name=%s"
                    val = (current_time, current_name)
                    cursor.execute(update, val)
                    myconn.commit()

                    hello = ("Hello ", current_name, "You did attendance today")
                    print(hello)
                    engine.say(hello)
                    # engine.runAndWait()

            else:
                color = (255, 0, 0)
                stroke = 2
                font = cv2.QT_FONT_NORMAL
                cv2.putText(frame, "UNKNOWN", (x, y), font, 1, color, stroke, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))
                hello = ("Your face is not recognized")
                print(hello)
                engine.say(hello)
                # engine.runAndWait()

        cv2.imshow('Attendance System', frame)
        k = cv2.waitKey(20) & 0xff
        if k == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def login():
    user_input = login_widget.e_id.text()
    if user_input == "":
        QMessageBox.information(login_widget, "Insert Status", "All fields are required")
    else:
        user = database.getStudent(user_input)
        if user is not None:
            logedin_user = user
            recognize_faces()
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
