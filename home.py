from PyQt5.QtWidgets import QApplication, QFrame, QWidget, QMainWindow, QLabel
from PyQt5.QtWidgets import QStackedWidget, QTextEdit 
from PyQt5.QtWidgets import QWidget, QStackedWidget
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QSize

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from dotenv import load_dotenv
load_dotenv()

home_widget = QWidget()

home_layout = QVBoxLayout()
home_layout.setAlignment(Qt.AlignCenter)

home_layout.addWidget(QLabel("This is home page"))

home_widget.setLayout(home_layout)



# 1 Create database connection
myconn = mysql.connector.connect(host="localhost",
    user=os.environ["MYSQL_USER"],
    passwd=os.environ["MYSQL_PASSWORD"],
    database=os.environ["MYSQL_DATABASE"])
cursor = myconn.cursor()

student_id = 2  # change to imported student id
def check_class():
    today = datetime.now().date()  # today's date
    time = datetime.now().time()  # current time
    cursor.execute(  # this sql query does not work
        f"SELECT * FROM Schedule WHERE DATE(start_time)='{today}' AND '{time}' <= TIME(start_time) NATURAL JOIN SELECT course_code FROM Enrolled WHERE student_id='{student_id}' AS E ORDER BY start_time LIMIT 1")
    earliest = cursor.fetchone()
    print(earliest)
    time_diff = earliest[1] - datetime.now()  # get time difference from the next earliest class
    if time_diff.total_seconds()//60 <= 60:
        print("You have class in the next hour")
        return True
    print("No class in the next hour")
    return False
