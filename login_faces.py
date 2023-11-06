import urllib
import numpy as np
import mysql.connector
from tkinter import *
import tkinter.messagebox as MessageBox
import cv2
import pyttsx3
import pickle
from datetime import datetime
import sys


# when student ID does not exist
def invalid_id():
    label = Label(root, text="Invalid student ID",
                     background="red",
                     foreground="white")
    label.place(x=360, y=135)
    label.after(3000, label.destroy)


# insert student ID
def insert():
    user_id = e_id.get()
    if user_id == "":
        MessageBox.showinfo("Insert Status", "All fields are required")
    else:
        conn = mysql.connector.connect(user='root', password='  ', database='   ',
                                      auth_plugin='mysql_native_password')
        cursor = conn.cursor()
        cursor.execute("use comp")
        cursor.execute("select * from Student where student_id=%s", (user_id,))
        result = cursor.fetchone()

        if not result:
            invalid_id()

        root.destroy()


# Login GUI
root = Tk()
root.geometry("600x300")
root.title("Intelligent Course Management System")

w = Label(root, text='Intelligent Course Management System', font="Times 30 italic bold")
w.pack()

id = Label(root, text='Enter ID', font="Bold 20")
id.place(x=200, y=90)

e_id = Entry()
e_id.place(x=280, y=93)
user_id = e_id.get()

insert = Button(root, text="Login", font="Italic 20", bg="white", command=insert)
insert.place(x=240, y=130)

root.mainloop()

# 1 Create database connection
myconn = mysql.connector.connect(host="localhost", user="root", passwd="  ", database="  ")
date = datetime.utcnow()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
cursor = myconn.cursor()


#2 Load recognize and read label from model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("/Users/amaris/PycharmProjects/pythonProject/FaceRecognition/train.yml")

labels = {"person_name": 1}
with open("/Users/amaris/PycharmProjects/pythonProject/FaceRecognition/labels.pickle", "rb") as f:
    labels = pickle.load(f)
    labels = {v: k for k, v in labels.items()}

# create text to speech
engine = pyttsx3.init()
rate = engine.getProperty("rate")
engine.setProperty("rate", 175)

# Define camera and detect face
face_cascade = cv2.CascadeClassifier('/Users/amaris/PycharmProjects/pythonProject/FaceRecognition/haarcascade/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

# 3 Open the camera and start face recognition
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

    for (x, y, w, h) in faces:
        print(x, w, y, h)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        # predict the id and confidence for faces
        id_, conf = recognizer.predict(roi_gray)
        print(conf)

        # If the face is recognized
        if conf >= 10:
            # print(id_)
            # print(labels[id_])
            font = cv2.QT_FONT_NORMAL
            id = 0
            id += 1
            name = labels[id_]
            current_name = name
            color = (255, 0, 0)
            stroke = 2
            cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))

            # Find the student's information in the database.
            select = "SELECT student_id, name, DAY(login_time), MONTH(login_time), YEAR(login_time) FROM Student WHERE name='%s'" % (name)
            name = cursor.execute(select)
            result = cursor.fetchall()
            # print(result)
            data = "error"

            for x in result:
                data = x

            # If the student's information is not found in the database
            if data == "error":
                print("The student", current_name, "is NOT FOUND in the database.")

            # If the student's information is found in the database
            else:
                """
                Implement useful functions here.
                Check the course and classroom for the student.
                    If the student has class room within one hour, the corresponding course materials
                        will be presented in the GUI.
                    if the student does not have class at the moment, the GUI presents a personal class 
                        timetable for the student.
                """
                # Update the data in database
                update = "UPDATE Student SET login_time=%s WHERE name=%s"
                val = (now, current_name)
                cursor.execute(update, val)
                #update = "UPDATE Student SET login_time=%s WHERE name=%s"
                #val = (current_time, current_name)
                #cursor.execute(update, val)
                myconn.commit()

                hello = f"Hello {current_name}."
                print(hello)
                engine.say(hello)
                #engine.runAndWait()
                cap.release()

        # If the face is unrecognized
        else:
            color = (255, 0, 0)
            stroke = 2
            font = cv2.QT_FONT_NORMAL
            cv2.putText(frame, "UNKNOWN", (x, y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))
            hello = "Your face is not recognized."
            print(hello)
            engine.say(hello)
            #engine.runAndWait()
            cap.release()

    cv2.imshow('Face Recogniser', frame)
    k = cv2.waitKey(20) & 0xff
    if k == ord('q'):
        break
    break

cap.release()
cv2.destroyAllWindows()
