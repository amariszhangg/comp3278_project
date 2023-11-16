import sys
import database

from PyQt5.QtWidgets import QApplication, QFrame, QWidget, QMainWindow, QMessageBox
from PyQt5.QtWidgets import QStackedWidget, QHBoxLayout, QLabel

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

import tkinter.messagebox as MessageBox

from FaceRecognition.faces import FaceRecognition

app = QApplication(sys.argv)
main_window = QMainWindow()
main_window.setWindowTitle("Intelligent Course Management System")

from login_gui import login_widget
from main_gui import main_widget

main_stack = QStackedWidget()
main_stack.addWidget(login_widget)
main_stack.addWidget(main_widget)

def idlogin():
    # Write login logic here (scan face -> if recognized redirect to main page)
    # For now, it will always redirect to main page (login page = 0, main page = 1)
    user_input = login_widget.e_id.text()
    if user_input == "":
        MessageBox.showinfo("Insert Status", "All fields are required")
    else:
        user = database.get_student(user_input)
        # check if any user is found
        if (user != None):
            logedin_user = user
            login()
        else:
            MessageBox.showinfo("Insert Status", "*User not found in database.")
            main_stack.setCurrentIndex(0)

def facelogin():
    # Write login logic here (scan face -> if recognized redirect to main page)
    # For now, it will always redirect to main page (login page = 0, main page = 1)

    # call recognize
    frame, face_id = self.face_recognize.recognise()
        # render
        Qframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        Qframe = QImage(Qframe, Qframe.shape[1], Qframe.shape[0], Qframe.strides[0], QImage.Format_RGB888)
        self.cam_feed.setPixmap(QPixmap.fromImage(Qframe))

        # verify the face id
        if (face_id != None):
            if (face_id == self.user_face_id):
                self.consec_check += 1
            else:
                self.user_face_id = face_id
                self.consec_check = 1

            # login
            if (self.consec_check >= self.consec_check_required):
                self.consec_check = 0

                # get user by face id
                user = self.main_window.db.get_student_by_face_id(self.user_face_id)

                # check if user is in the database
                if (user != None):
                    self.main_window.user = user
                    self.login()
                else:
                    self.login_status_label.setHidden(False)
                    self.login_status_label.setText("*User not found in database.")
    main_stack.setCurrentIndex(1)

def logout():
    # TODO Write logic to update logout time
    main_stack.setCurrentIndex(0)

def login():
    # turn off the camera thread
    if self.flg_conn:
        self.connect()

    # set users variable
    last_login_log = self.main_window.db.get_student_last_login_log(self.main_window.user.studentId)
    self.main_window.main_app_widget.last_login_log = last_login_log
    self.main_window.main_app_widget.current_login_time = datetime.datetime.now()

    # update page content retriving user's data
    self.main_window.main_app_widget.home_tab.update_content()
    self.main_window.main_app_widget.timetable_tab.init_UI()
    self.main_window.main_app_widget.timetable_tab.update_content()
    self.main_window.main_app_widget.course_tab.init_UI()

    # go to home page
    main_stack.setCurrentIndex(1)


login_widget.login_button.clicked.connect(idlogin)
login_widget.loginwithface_button.clicked.connect(facelogin)
main_widget.logout_button.clicked.connect(logout)

main_window.setCentralWidget(main_stack)

main_window.resize(850, 534)
main_window.setMaximumSize(850, 534)
main_window.setMinimumSize(850, 534)

main_window.show()

sys.exit(app.exec_())



