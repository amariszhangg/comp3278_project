from tkinter import *
import tkinter.messagebox as MessageBox
import mysql.connector as mysql


def insert():
    id = e_id.get()

    if id == "":
        MessageBox.showinfo("Insert Status", "All fields are required")
    else:
        conn = mysql.connect(user='root', password='AmarisSQL1', database='project',
                                      auth_plugin='mysql_native_password')


root = Tk()
root.geometry("600x300")
root.title("Intelligent Course Management System")

w = Label(root, text='Intelligent Course Management System', font="Times 30 italic bold")
w.pack()

#msg = Message(root, text="Welcome")
#msg.pack()

id = Label(root, text='Enter ID', font="Bold 20")
id.place(x=200, y=90)

e_id = Entry()
e_id.place(x=280, y=93)

insert = Button(root, text="Login", font="Italic 20", bg="white", command=insert)
insert.place(x=240, y=130)

root.mainloop()