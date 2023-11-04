# this runs after face recog, but will probably be merged onto faces.py/faces_gui.py
# enter your own passwd and database
# this current code is for selecting all the relevant info to be used in displaying the timetable/class within next hour
import mysql.connector


conn = mysql.connector.connect(host="localhost", user="root", passwd="  ", database="  ")
cursor = conn.cursor()
cursor.execute("SELECT student_id, name, login_time FROM Student WHERE student_id='2'")
student_info = cursor.fetchall()
student_id = student_info[0][0]

# show courses taken
cursor.execute("SELECT course_code FROM Enrolled WHERE student_id='%s'" % student_id)
courses = cursor.fetchall()
print(courses)

# show each course's info
cursor.execute("SELECT * FROM Course WHERE course_code='%s'" % courses[0][0])
course_info = cursor.fetchall()
print(course_info)

#show schedule
cursor.execute("SELECT * FROM Schedule NATURAL JOIN (SELECT course_code FROM Enrolled WHERE student_id='%s') as courses ORDER BY start_time" % student_id)
schedule = cursor.fetchall()
print(schedule)

# show each course's material sections
cursor.execute("SELECT * FROM CourseMaterialSection WHERE course_code='%s'" % courses[0][0])
course_sections = cursor.fetchall()
print(course_sections)

# show each course material
cursor.execute("SELECT * FROM Material WHERE course_code='%s'" % courses[0][0])
course_materials = cursor.fetchall()
print(course_materials)

# show each course's latest message
cursor.execute("SELECT * FROM TeacherMessage WHERE course_code='%s' ORDER BY post_time DESC LIMIT 1" % courses[0][0])
latest_message = cursor.fetchall()
print(latest_message)
