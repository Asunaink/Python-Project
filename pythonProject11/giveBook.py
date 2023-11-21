from tkinter import * #Импорт всех классов и функций из библиотеки Tkinter
from tkinter import ttk #Импорт виджетов ttk (themed Tkinter) для улучшения внешнего вида интерфейса
import sqlite3 # Импорт модуля SQLite для работы с базами данных sqlite
from tkinter import messagebox #Импорт модуля для создания всплывающих сообщений

# Создание подключения к базе данных sglite и создание объекта курсора для выполнения операций с базой данных
con = sqlite3.connect("library.db")
cur = con.cursor()


class GiveBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("400x400+550+200")#Установка размеров окна
        self.title("Lend Book")#Установка заголовка окна
        self.resizable(False, False)#Отключение возможности изменения размеров окна
        query = "SELECT * FROM books WHERE status=0"#Формирование запроса к базе данных для выбора всех книг с status=0
        books = cur.execute(query).fetchall()#Выполнение запроса и получение списка всех книг
        book_list = []#Создание пустого списка book_list, в который будут добавлены данные о книгах.
        for book in books:#Цикл, который проходится по каждой книге в результатах запроса
            book_list.append(str(book[0]) + "-" + book[1])#Добавление книги в виде строки в формате "ID-Название" в список book_list

        query2 = "SELECT * FROM member"
        members = cur.execute(query2).fetchall()
        member_list = []
        for member in members:
            member_list.append(str(member[0]) + "-" + member[1])

            # Top frame

        self.topFrame = Frame(self, height=70, bg="#8B7D6B")
        self.topFrame.pack(fill=X)

        # bottom frame
        self.bottomFrame = Frame(self, height=330, bg="#F5F5DC")
        self.bottomFrame.pack(fill=X)

        # heading,date
        heading = Label(self.topFrame, text="Lend Book", font="times 20 bold", bg="#8B7D6B")
        heading.place(x=110, y=10)

        # Entries, labels
        # name
        self.book_name = StringVar()
        self.lbl_name = Label(self.bottomFrame, text="Book name:", font="times 15 bold", bg="#F5F5DC")
        self.lbl_name.place(x=40, y=40)
        self.combo_name = ttk.Combobox(self.bottomFrame, textvariable=self.book_name)
        self.combo_name["values"] = book_list
        self.combo_name.place(x=150, y=45)

        # phone
        self.member_name = StringVar()
        self.lbl_phone = Label(self.bottomFrame, text="Member :", font="times 15 bold", bg="#F5F5DC")
        self.lbl_phone.place(x=40, y=80)
        self.combo_member = ttk.Combobox(self.bottomFrame, textvariable=self.member_name)
        self.combo_member["values"] = member_list
        self.combo_member.place(x=150, y=85)

        # Button
        button = Button(self.bottomFrame, text="Lend Book", bg="#8B7D6B", fg="white", command=self.lendBook)#Создание кнопки "Lend Book" для осуществления операции выдачи книги
        button.place(x=160, y=210)

    def lendBook(self):#Определение функции lendBook, которая выполняет операцию выдачи книги участнику
        book_name = self.book_name.get()#Получение имени книги из переменной self.book_name
        self.book_id = book_name.split("-")[0]
        member_name = self.member_name.get()

        if (book_name and member_name != ""):#Проверка, что оба поля (имя книги и участника) заполнены
            try:
                query = "INSERT INTO 'borrows' (book_id,member_id) VALUES(?,?)"#Формирование запроса на вставку записи в таблицу 'borrows' с данными о выданной книге и участнике
                cur.execute(query, (book_name, member_name))
                con.commit()#Подтверждение изменений в базе данных
                messagebox.showinfo("Success", "Successfully added", icon="info")
                cur.execute("UPDATE book SET status =? WHERE book_id=?", (1, self.book_id))
                con.commit()
            except:
                messagebox.showinfo("Error", "Can not add", icon="warning")

        else:
            messagebox.showinfo("Error", "Fields can not be empty", icon="warning")