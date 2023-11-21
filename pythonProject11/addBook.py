from tkinter import *  # Импорт всех классов и функций из библиотеки tkinter
from tkinter import messagebox  # Импорт функции для создания всплывающих окон
import sqlite3  # Импорт модуля для работы с базой данных SQLite

con = sqlite3.connect('library.db')  # Подключение к базе данных SQLite с именем файла "library.db"
cur = con.cursor()  # Создание объекта курсора для работы с базой данных


class AddBook(Toplevel):  # Создание нового класса AddBook, наследующего от Toplevel (окно верхнего уровня)
    def __init__(self):  # Определение метода инициализации класса
        Toplevel.__init__(self)  # Вызов инициализатора класса Toplevel для создания окна
        self.geometry("400x400+550+200")  # Установка размеров и положения окна
        self.title("Add book")  # Установка заголовка окна
        self.resizable(False, False)  # Запрет изменения размеров окна

        self.topFrame = Frame(self, height=70,bg="#8B7D6B")  # Создание верхнего фрейма с определенными характеристиками
        self.topFrame.pack(fill=X)  # Размещение верхнего фрейма в окне

        self.bottomFrame = Frame(self, height=330,bg="#F5F5DC")  # Создание нижнего фрейма с определенными характеристиками
        self.bottomFrame.pack(fill=X)  # Размещение нижнего фрейма в окне

        heading = Label(self.topFrame, text="Add Book", font="times 20 bold",bg="#8B7D6B")  # Создание метки "Add Book" в верхнем фрейме
        heading.place(x=130, y=10)  # Размещение метки в определенном месте внутри верхнего фрейма

        self.lbl_name = Label(self.bottomFrame, text="Name:", font="times 15 bold", bg="#F5F5DC")  # Создание метки "Name:" в нижнем фрейме
        self.lbl_name.place(x=40, y=40)  # Размещение метки "Name:" в определенном месте внутри нижнего фрейма
        self.ent_name = Entry(self.bottomFrame, width=30, bd=4)  # Создание поля ввода для имени книги в нижнем фрейме
        self.ent_name.insert(0, "Please enter a book name")  # Установка текста-подсказки для поля ввода
        self.ent_name.place(x=150, y=45)  # Размещение поля ввода в определенном месте внутри нижнего фрейма

        # Аналогичные операции выполняются для полей ввода для автора и количества страниц
        # author
        self.lbl_author = Label(self.bottomFrame, text="Author:", font="times 15 bold", bg="#F5F5DC")
        self.lbl_author.place(x=40, y=80)
        self.ent_author = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_author.insert(0, "Please enter an author")
        self.ent_author.place(x=150, y=85)

        # page
        self.lbl_page = Label(self.bottomFrame, text="Page:", font="times 15 bold", bg="#F5F5DC")
        self.lbl_page.place(x=40, y=120)
        self.ent_page = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_page.insert(0, "Please enter a page size")
        self.ent_page.place(x=150, y=125)

        button = Button(self.bottomFrame, text="Add Book", bg="#8B7D6B", fg="white",command=self.addBook)  # Создание кнопки "Add Book" в нижнем фрейме
        button.place(x=160, y=210)  # Размещение кнопки в определенном месте внутри нижнего фрейма

    def addBook(self):  # Определение метода для добавления книги в базу данных
        name = self.ent_name.get()  # Получение значения из поля ввода имени книги
        author = self.ent_author.get()  # Получение значения из поля ввода автора книги
        page = self.ent_page.get()  # Получение значения из поля ввода количества страниц книги

        if name and author and page != "":  # Проверка наличия всех значений
            try:
                query = "INSERT INTO 'books' (Name, Author, page) VALUES(?, ?, ?)"  # Создание SQL-запроса для добавления информации о книге в базу данных
                cur.execute(query, (name, author, page))  # Выполнение SQL-запроса с полученными значениями
                con.commit()  # Применение изменений к базе данных
                messagebox.showinfo("Success", "Successfully added",icon='info')  # Отображение сообщения об успешном добавлении книги
            except:
                messagebox.showinfo("Error", "Can not add to database",icon='warning')  # Отображение сообщения об ошибке при добавлении книги
        else:
            messagebox.showinfo("Error", "Fields can not be empty",icon='warning')  # Отображение сообщения об ошибке, если поля ввода пусты










