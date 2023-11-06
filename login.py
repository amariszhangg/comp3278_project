from tkinter import *
import tkinter.messagebox as MessageBox
import mysql.connector as mysql
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
    id = e_id.get()

    if id == "":
        MessageBox.showinfo("Insert Status", "All fields are required")
    else:
        conn = mysql.connect(user='root', password='AmarisSQL1', database='facerecognition',
                                      auth_plugin='mysql_native_password')
        cursor = conn.cursor()
        cursor.execute("use facerecognition")
        cursor.execute("select * from Student where student_id=%s", (id,))
        result = cursor.fetchone()
        if not result:
            invalid_id()

        else:
            root.destroy()

            sys.path.append("FaceRecognition")
            import faces_gui

# GUI
root = Tk()
root.geometry("600x300")
root.title("Intelligent Course Management System")

w = Label(root, text='Intelligent Course Management System', font="Times 30 italic bold")
w.pack()

id = Label(root, text='Enter ID', font="Bold 20")
id.place(x=200, y=90)

e_id = Entry()
e_id.place(x=280, y=93)

insert = Button(root, text="Login", font="Italic 20", bg="white", command=insert)
insert.place(x=240, y=130)

root.mainloop()
