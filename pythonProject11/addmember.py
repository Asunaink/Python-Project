from tkinter import *
from tkinter import messagebox
import sqlite3

con = sqlite3.connect('library.db')
cur = con.cursor()

class AddMember(Toplevel):
    def __init__(self):
     Toplevel.__init__(self)
     self.geometry("400x400+550+200")
     self.title("Add Member")
     self.resizable(False,False)

#FRAME#

#Top frame

     self.topFrame = Frame(self, height=70, bg="#8B7D6B")
     self.topFrame.pack(fill=X)

#bottom frame
     self.bottomFrame = Frame(self, height=330, bg="#F5F5DC")
     self.bottomFrame.pack(fill=X)


#heading,date
     heading = Label(self.topFrame, text="Add Member", font="times 20 bold",bg="#8B7D6B")
     heading.place(x=110, y=10)


#Entries, labels
     #name
     self.lbl_name = Label(self.bottomFrame, text="Name:", font="times 15 bold", bg="#F5F5DC")
     self.lbl_name.place(x=40, y=40)
     self.ent_name = Entry(self.bottomFrame, width=30, bd=4)
     self.ent_name.insert(0,"Please enter a name")
     self.ent_name.place(x=150, y=45)

     #phone
     self.lbl_phone = Label(self.bottomFrame, text="Phone:", font="times 15 bold", bg="#F5F5DC")
     self.lbl_phone.place(x=40, y=80)
     self.ent_phone = Entry(self.bottomFrame, width=30, bd=4)
     self.ent_phone.insert(0, "Please enter a phone number")
     self.ent_phone.place(x=150, y=85)

     #Button
     button= Button(self.bottomFrame, text="Add Person", bg="#8B7D6B",fg="white",command=self.addMember)
     button.place(x=160, y=210)

    def addMember(self):
         name = self.ent_name.get()
         phone = self.ent_phone.get()


         if(name and phone !=""):
             try:
                 query="INSERT INTO 'member' (Name, Phone) VALUES(?, ?)"
                 cur.execute(query,(name, phone))
                 con.commit()
                 messagebox.showinfo("Success","Successfully added",icon='info')


             except:
                 messagebox.showinfo("Error", "Can not add to database", icon='warning')

         else:
             messagebox.showinfo("Error", "Fields can not be empty", icon='warning')


