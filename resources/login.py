from tkinter import *
def boot()
    login = Tk()
    login.geometry('250x100')
    login.resizable(width = 0, height = 0)
    login.title("Login")

    welcome = Label(login, text = "Enter Username and Password", font="Calibri 11")
    welcome.place(x=35, y=0)
    #Username 
    ulabel = Label(login, text = "Username:", font="Calibri 9")
    ulabel.place(x=0,y=20)
    username = Entry(login, font="Calibri")
    username.place(x=65, y=20, width = 185, height = 20)
    #Password
    plabel = Label(login, text = "Password:", font="Calibri 9")
    plabel.place(x=0,y=40)
    password = Entry(login,  show="*", font="Calibri")
    password.place(x=65, y=40, width = 185, height = 20)

    submit = Button(login, text="Submit", font="Calibri")
    submit.place(x=10,y=65, width = 230, height = 30)
