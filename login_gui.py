import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from dotenv import load_dotenv
import mysql.connector as mysql

load_dotenv()

# when student ID does not exist
def invalid_id():
    message = QMessageBox()
    message.setText("Invalid student ID")
    message.setStyleSheet("QMessageBox { background-color: red; color: white; }")
    message.exec_()

# insert student ID
def insert():
    student_id = e_id.text()

    if student_id == "":
        QMessageBox.information(window, "Insert Status", "All fields are required")
    else:
        conn = mysql.connect(
            user=os.environ["MYSQL_USER"],
            passwd=os.environ["MYSQL_PASSWORD"],
            database=os.environ["MYSQL_DATABASE"],
            auth_plugin='mysql_native_password')
        cursor = conn.cursor()
        cursor.execute(f'use {os.environ["MYSQL_DATABASE"]}')
        cursor.execute("select * from Student where student_id=%s", (student_id,))
        result = cursor.fetchone()
        if not result:
            invalid_id()
        else:
            window.close()
            sys.path.append("FaceRecognition")
            import faces_gui


class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setParent(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create a label for the title
        title_label = QLabel("Intelligent Course Management System")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title_label,alignment=Qt.AlignCenter)

        self.setLayout(layout)


app = QApplication(sys.argv)
main_window = QMainWindow()
main_window.setWindowTitle("Intelligent Course Management System")

# Create the original interface widget
interface_widget = QWidget(main_window)
main_window.setCentralWidget(interface_widget)

# Create a vertical layout for the original interface
layout = QVBoxLayout(interface_widget)
layout.setAlignment(Qt.AlignCenter)  # Center align the contents

# Create the custom title bar
title_bar = CustomTitleBar(interface_widget)
layout.addWidget(title_bar)

# Create a horizontal layout for the logo and transparent box
logo_layout = QHBoxLayout()

# Create the logo label
logo_label = QLabel(interface_widget)
logo_label.setPixmap(QIcon("login.png").pixmap(300, 300))  # Set your logo image path here
logo_label.setAlignment(Qt.AlignCenter)
logo_layout.addWidget(logo_label)

layout.addLayout(logo_layout)

# Create background
pixmap = QPixmap("login_background.jpg")
pal = QPalette()
pal.setBrush(QPalette.Window, QBrush(pixmap))
main_window.setPalette(pal)

# Create the ID label
id_label = QLabel("Enter ID", interface_widget)
id_label.setFont(QFont("Arial", 14))
id_label.setAlignment(Qt.AlignCenter)
id_label.setFixedSize(200,30)
id_label.setStyleSheet(
    """
    QLabel {
    background-color: rgb(255,255,255);
    color: black;
    }
    """
)
# Create the input field
e_id = QLineEdit(interface_widget)
e_id.setFixedWidth(300)
e_id.setFixedHeight(45)
e_id.setStyleSheet(
    """
    QLineEdit {
    background-color: rgb(255,255,255);
    color: black;
    }
    """
)
e_id.setAlignment(Qt.AlignCenter)

# Create the login button
login_button = QPushButton("Login")
login_button.setFont(QFont("Arial", 14))
login_button.setStyleSheet(
    """
    QPushButton {
        background-color: rgba(76, 175, 80, 200);
        color: white;
        border-radius: 5px;
        padding: 10px;
    }

    QPushButton:hover {
        background-color: rgba(69, 160, 73, 200);
    }
    """
)
login_button.setFixedWidth(300)
login_button.setFixedHeight(45)

# Create transparent box
box_layout = QVBoxLayout()
transparent_box = QFrame(interface_widget)
transparent_box.setLayout(box_layout)
box_layout.addWidget(id_label, alignment=Qt.AlignCenter)
box_layout.addWidget(e_id, alignment=Qt.AlignCenter)
box_layout.addWidget(login_button, alignment=Qt.AlignCenter)
transparent_box.setFixedWidth(500)
transparent_box.setFixedHeight(150)
transparent_box.setStyleSheet("background-color: rgba(0, 0, 0, 150); border-radius: 10px;")
layout.addWidget(transparent_box)


# Connect the button's clicked signal to the insert function
login_button.clicked.connect(insert)

main_window.resize(850, 534)
main_window.setMaximumSize(850, 534)
main_window.setMinimumSize(850, 534)

main_window.show()

sys.exit(app.exec_())