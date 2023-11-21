from tkinter import * #Импорт всех классов и функций из библиотеки Tkinter
from tkinter import ttk #Импорт виджетов ttk (themed Tkinter) для улучшения внешнего вида интерфейса
import sqlite3# Импорт модуля SQLite для работы с базами данных sqlite
import addBook,addmember, giveBook
from tkinter import messagebox #Импорт модуля для создания всплывающих сообщений

# Создание подключения к базе данных sglite и создание объекта курсора для выполнения операций с базой данных
con = sqlite3.connect("library.db")
cur = con.cursor()
#Определение класса Main, который содержит методы и интерфейс для управления библиотекой
class Main(object):
    def __init__(self, master):
        self.master = master

        def displayStatistics(evt): #Объявление функции displayStatistics, которая принимает аргумент evt
            count_books=cur.execute("SELECT count (book_id) FROM books").fetchall() #Запрос к базе данных для подсчета общего количества книг в библиотеке
            count_member= cur.execute("SELECT count (ID) FROM member").fetchall() #Запрос к базе данных для подсчета общего числа членов библиотеки
            taken_books = cur.execute("SELECT  count(status) FROM books WHERE status=1").fetchall() #Запрос к базе данных для подсчета количества книг, которые взяты
            print(count_books)
            self.lbl_book_count.config(text='Total:'+ ' '+str(count_books[0][0])+" " + 'books in library') # Установка текста для виджета lbl_book_count, отображающего общее количество книг в библиотеке
            self.lbl_members_count.config(text="Total member : " + str(count_member[0][0])) #Установка текста для виджета lbl_members_count, отображающего общее количество members библиотеки
            self.lbl_taken_count.config(text="Taken books :"+' '+ str(taken_books[0][0]))#Установка текста для виджета lbl_taken_count, отображающего количество взятых книг в библиотеке
            displayBooks(self)#Вызов функции displayBooks, предположительно для обновления списка книг или других элементов интерфейса, связанных с отображением списка книг

        def displayBooks(self):
            books = cur.execute("SELECT * FROM books").fetchall()# Выполнение запроса к базе данных для выбора всех данных из таблицы books
            count = 0 #отслеживания порядкового номера вставки книги в список

            self.list_book.delete(0,END)#Очистка содержимого виджета list_book списка книг, перед тем как добавить новые данные
            for book in books: #Цикл, проходящий через каждую строку результата запроса книг
                print(book)
                self.list_book.insert(count, str(book[0]) + "-" + book[1])#Вставка строки в list_book. Добавление информации о книге в формате "ID-Название книги"
                count += 1 # Увеличение счетчика, чтобы в следующий раз вставить запись на одну строку ниже в списке

            def bookInfo(evt):
                value = str(self.list_book.get(self.list_book.curselection())) #Получение значения выбранного элемента из list_book
                id = value.split('-')[0] #Получение ID книги из строки, разделенной по символу -
                book = cur.execute("SELECT * FROM books WHERE book_id=?",(id,)) #Выполнение запроса к базе данных для получения информации о книге с определенным ID
                book_info = book.fetchall() #Получение информации о книге в виде списка кортежей
                print(book_info)
                self.list_details.delete(0,'end')

                self.list_details.insert(0,"Book Name : "+book_info[0][1]) #Вставка в list_details информации о названии книги из полученных данных
                self.list_details.insert(1,"Author : "+book_info[0][2]) #Вставка информации об авторе книги в list_details
                self.list_details.insert(2,"Page : "+book_info[0][3]) # Вставка информации о страницах книги в list_details.
                if book_info[0][4] == 0: #Проверка статуса книги
                    self.list_details.insert(4,"Status : Available")
                else:
                    self.list_details.insert(4,"Status : Not Available")

            def doubleClick(evt): #функции doubleClick, будет вызываться при двойном щелчке на элементе в list_book
                global given_id #переменная, для использования ее значения в других частях программы
                value = str(self.list_book.get(self.list_book.curselection())) # Получение значения выбранного элемента из list_book в виде строки
                given_id =value.split("-")[0] #Получение ID книги из строки, разделенной  "-"
                give_book = GiveBook() #Создание экземпляра класса GiveBook(), для отображения окна выдачи книги (в другой части кода)



            self.list_book.bind('<<ListboxSelect>>',bookInfo)  # Привязка события выбора элемента в list_book к bookInfo, это событие вызывается при выборе элемента в списке книг
            self.tabs.bind('<<NotebookTabChanged>>',displayStatistics)  # Привязка события изменения вкладки в tabs к displayStatistics. Вызывается при изменении выбранной вкладки
            self.list_book.bind("<Double-Button-1>",doubleClick)  # Привязка двойного щелчка мыши в list_book к doubleClick. Выполняет код в doubleClick при двойном щелчке

        mainFrame= Frame(self.master)
        mainFrame.pack()

        topFrame = Frame(mainFrame, width=1200, height=70, bg="#F5F5DC", padx=20, relief=SUNKEN, borderwidth=2)
        topFrame.pack(side=TOP, fill=X)  # Размещение topFrame внутри основной рамки в верхней части окна

        centerFrame = Frame(mainFrame, width=1200,height=700, relief=RIDGE, bg="#8B7D6B")  # Создание рамки centerFrame внутри основной рамки
        centerFrame.pack(side=TOP)  # Размещение centerFrame внутри основной рамки в верхней части окна

        centerLeftFrame = Frame(centerFrame, width=900, height=700, bg="#8B7D6B", borderwidth=2,relief="sunken")  # Создание рамки centerLeftFrame внутри centerFrame
        centerLeftFrame.pack(side=LEFT)  # Размещение centerLeftFrame внутри centerFrame слева

        centerRightFrame = Frame(centerFrame, width=600, height=700, bg="#FFE4C4", borderwidth=2, relief="sunken")  # Создание рамки centerRightFrame внутри centerFrame
        centerRightFrame.pack()

        #Search bar
        search_bar = LabelFrame(centerRightFrame, width=440, height=75,bg="#F5F5DC")  # Создание рамки search_bar внутри centerRightFrame
        search_bar.pack(fill=BOTH)  # Размещение search_bar внутри centerRightFrame. fill=BOTH означает, что рамка будет заполняться как по горизонтали, так и по вертикали
        self.lbl_search = Label(search_bar, text="Search:", font="times 10 bold", bg="#F5F5DC",fg='black')  # Создание текстовой метки "Search" внутри рамки search_bar
        self.lbl_search.grid(row=0, column=0, padx=20,pady=10)  # Размещение текстовой метки lbl_search в рамке search_bar.
        self.ent_search = Entry(search_bar, width=20,bd=10)  # Создание текстового поля ent_search внутри рамки search_bar
        self.ent_search.grid(row=0, column=1, columnspan=2, padx=5, pady=5)  # Размещение текстового поля ent_search
        self.btn_search = Button(search_bar, text="Find", font="times 10", bg="#8B7D6B", fg="white",command=self.searchBooks)  # Создание кнопки "Find" внутри рамки search_bar. При нажатии будет вызываться функция searchBooks
        self.btn_search.grid(row=0, column=3, padx=10, pady=10)  # Размещение кнопки btn_search

        #List bar
        list_bar = LabelFrame(centerRightFrame, width=440, height=170,bg="#F5F5DC")  # Создание рамки list_bar внутри centerRightFrame,будет содержать элементы интерфейса для сортировки списка книг
        list_bar.pack(fill=BOTH)
        lbl_list = Label(list_bar, text=" Sort by:", font='times 16 bold', fg='#8B7D6B',bg='#F5F5DC')  # Создание текстовой метки "Sort by" внутри рамки list_bar для указания сортировки
        lbl_list.grid(row=0, column=0)  # Размещение текстовой метки lbl_list
        self.listChoice = IntVar()  # Создание переменной типа IntVar, для выбора опции сортировки
        rb1 = Radiobutton(list_bar, text='All Books', var=self.listChoice, value=1,bg="#F5F5DC")  # Создание радиокнопки "All Books" внутри рамки list_bar
        rb2 = Radiobutton(list_bar, text='In library', var=self.listChoice, value=2, bg="#F5F5DC")  # Создание радиокнопки "In library" внутри рамки list_bar
        rb3 = Radiobutton(list_bar, text='Borrowed Books', var=self.listChoice, value=3,bg="#F5F5DC")  # Создание радиокнопки "Borrowed Books" внутри рамки list_bar
        # Размещение
        rb1.grid(row=1, column=0)
        rb2.grid(row=1, column=1)
        rb3.grid(row=1, column=2)
        btn_list = Button(list_bar, text="list", bg="#8B7D6B", fg='white', font='times 10',command=self.listBooks)  # Создание кнопки "list" внутри рамки list_bar
        btn_list.grid(row=2, column=2, padx=40, pady=10)

        # image
        lib_bar = Frame(centerRightFrame, width=400, height=600)  # Создание рамки lib_bar внутри centerRightFrame
        lib_bar.pack(fill=BOTH)
        self.img_library = PhotoImage(file="icons/library.png")  # Загрузка изображения
        self.lblImg = Label(lib_bar, image=self.img_library)
        self.lblImg.grid(row=0)


        #add member button
        self.iconmember = PhotoImage(file="icons/users.png")  # Загрузка изображения
        self.btnmember = Button(topFrame, bg="#8B7D6B", padx=5,command=self.addMember)  # Создание кнопки
        self.btnmember.configure(image=self.iconmember, height=18, compound=LEFT)  # Настройка кнопки btnmember для отображения изображения
        self.btnmember.pack(side=LEFT)

        #add book
        self.iconbook = PhotoImage(file="icons/add.png")
        self.btnbook = Button(topFrame,bg="#8B7D6B", image=self.iconbook, height=18, compound=LEFT, command=self.addBook)  # Создание кнопки
        self.btnbook.pack(side=LEFT, padx=5)

        #give Book
        self.icongive = PhotoImage(file="icons/givebook.png")
        self.btngive = Button(topFrame, text="Give Book", bg="#8B7D6B", fg="white", font="times 10", width=90,height=18, padx=10, image=self.icongive, compound=LEFT,command=self.giveBook)
        self.btngive.pack(side=LEFT)

        #TABS
        self.tabs = ttk.Notebook(centerLeftFrame, width=900, height=700)
        self.tabs.pack()
        self.tab1_icon = PhotoImage(file="icons/management.png")
        self.tab2_icon = PhotoImage(file="icons/static.png")
        self.tab1 = ttk.Frame(self.tabs)  # Создание фрейма для первой вкладки
        self.tab2 = ttk.Frame(self.tabs)  # Создание фрейма для второй вкладки
        self.tabs.add(self.tab1, text="Management Library", image=self.tab1_icon, compound=LEFT)
        self.tabs.add(self.tab2, text="Statistics", image=self.tab2_icon, compound=LEFT)

        # list books
        self.list_book = Listbox(self.tab1, width=60, height=50, bd=5,font="times 12 bold")  # Создание списка книг внутри фрейма tab1
        self.sb = Scrollbar(self.tab1, orient=VERTICAL)
        self.list_book.grid(row=0, column=0, padx=(10, 0), pady=10, sticky=N)
        self.sb.config(command=self.list_book.yview)  # Настройка ползунка
        self.list_book.config(yscrollcommand=self.sb.set)
        self.sb.grid(row=0, column=0, sticky=N + S + E)

        # detail
        self.list_details = Listbox(self.tab1, width=80, height=40, bd=5, font="times 12 bold")  #
        self.list_details.grid(row=0, column=1, padx=(10, 0), pady=10, sticky=N)
        self.lbl_book_count = Label(self.tab2, text="", pady=30, font="times 12 bold")
        self.lbl_book_count.grid(row=0)
        self.lbl_members_count = Label(self.tab2, text="", pady=30, font="times 12 bold")
        self.lbl_members_count.grid(row=1, sticky=W)
        self.lbl_taken_count = Label(self.tab2, text="", pady=30, font="times 12 bold")
        self.lbl_taken_count.grid(row=2, sticky=W)

        # functions
        displayBooks(self)  # отображает список книг
        displayStatistics(self) # отображает статистику о книгах и участниках

    def addBook(self):  # метод создает экземпляр класса AddBook, отвечающего за добавление новой книги в библиотеку
            add = addBook.AddBook()

    def addMember(self):
        member = addmember.AddMember()


    def searchBooks(self):#Этот метод выполняет поиск книги на основе текста, введенного в поле поиска
        value= self.ent_search.get()#Получает значение из поля поиска для поиска книг по имени.
        search= cur.execute("SELECT*FROM books where name LIKE ?",('%'+value+'%',)).fetchall()#Использует полученное значение для выполнения SQL-запроса, который ищет книги
        print(search)
        self.list_book.delete(0,END)#Очищает список книг в интерфейсе перед отображением результатов поиска
        count=0
        for book in search:#используется для добавления найденных книг в список книг, отображаемый в интерфейсе.
            self.list_book.insert(count,str(book[0])+"-"+book[1])
            count +=1

    def listBooks(self):  # отвечает за отображение всех книг, книг в библиотеке и взятых книг, в зависимости от выбора пользователя с помощью self.listChoice
        value = self.listChoice.get()  # Получает значение выбора пользователя из виджета Radiobutton
        if value == 1:  # Если пользователь выбрал опцию "All Books", выполняется запрос, чтобы извлечь все книги из базы данных. ПОтом список книг очищается
            allbooks = cur.execute("SELECT *FROM books").fetchall()
            self.list_book.delete(0, END)

            count = 0
            for book in allbooks:
                self.list_book.insert(count, str(book[0]) + "-" + book[1])
                count += 1
        elif value == 2:  # Если выбрана опция "In library", выполняется запрос для извлечения книг, находящихся в библиотеке
            books_in_library = cur.execute("SELECT * FROM books WHERE status=?", (0,)).fetchall()  # Запрос к базе данных для получения книг, находящихся в библиотеке (status=0).
            self.list_book.delete(0, END)
            count = 0
            for book in books_in_library:  # перебирает книги из books_in_library и добавляет их в self.list_book в формате "ID-Название". Каждая книга получает свой порядковый номер в списке
                self.list_book.insert(count, str(book[0]) + "-" + book[1])
                count += 1
        else:
            taken_books = cur.execute("SELECT * FROM books WHERE status =?", (1,)).fetchall()  # ыбор книг с status=1, книг, которые в данный момент находятся у мемберов библиотеки
            self.list_book.delete(0, END)

            count = 0
            for book in taken_books:
                self.list_book.insert(count, str(book[0]) + "-" + book[1])
                count += 1

    def giveBook(self):
        give_book = giveBook.GiveBook()



class GiveBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("400x400+550+200")
        self.title("Lend Book")
        self.resizable(False, False)
        global given_id
        self.book_id = int(given_id)
        query = "SELECT * FROM books"
        books = cur.execute(query).fetchall()
        book_list = []
        for book in books:
            book_list.append(str(book[0]) + "-" + book[1])

        query2 = "SELECT * FROM member"  # запрашивает всех участников из базы данных.
        members = cur.execute(query2).fetchall()  # Выполнение запроса к базе данных и получение списка всех участников.
        member_list = []
        for member in members:  # Цикл перебирает всех участников и добавляет их в member_list в формате "ID-Имя".
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
        self.book_name = StringVar()  # Установка начального значения выпадающего списка на основе self.book_id
        self.lbl_name = Label(self.bottomFrame, text="Book name:", font="times 15 bold", bg="#F5F5DC")
        self.lbl_name.place(x=40, y=40)
        self.combo_name = ttk.Combobox(self.bottomFrame, textvariable=self.book_name)
        self.combo_name["values"] = book_list
        self.combo_name.current(self.book_id - 1)
        self.combo_name.place(x=150, y=45)

        # phone
        self.member_name = StringVar()
        self.lbl_phone = Label(self.bottomFrame, text="Member :", font="times 15 bold", bg="#F5F5DC")
        self.lbl_phone.place(x=40, y=80)
        self.combo_member = ttk.Combobox(self.bottomFrame, textvariable=self.member_name)
        self.combo_member["values"] = member_list
        self.combo_member.place(x=150, y=85)

        # Button
        button = Button(self.bottomFrame, text="Lend Book", bg="#8B7D6B", fg="white",command=self.lendBook)  # Создание кнопки "Lend Book" для осуществления операции выдачи книги
        button.place(x=160, y=210)

    def lendBook(self):  # Определение функции lendBook, которая выполняет операцию выдачи книги участнику
            book_name = self.book_name.get()  # Получение имени книги из переменной self.book_name
            member_name = self.member_name.get()  # Получение имени участника из переменной self.member_name

            if (book_name and member_name != ""):  # Проверка, что оба поля (имя книги и участника) заполнены
                try:
                    query = "INSERT INTO 'borrows' (book_id,member_id) VALUES(?,?)"  # Формирование запроса на вставку записи в таблицу 'borrows' с данными о выданной книге и участнике
                    cur.execute(query, (book_name, member_name))
                    con.commit()  # Подтверждение изменений в базе данных
                    messagebox.showinfo("Success", "Successfully added",
                                        icon="info")  # Вывод информационного сообщения об успешном выполнении операции
                    cur.execute("UPDATE book SET status =? WHERE book_id=?",
                                (1, self.book_id))  # Обновление статуса книги
                    con.commit()
                except:  # ывод сообщения об ошибке, если операция не удалась из-за исключения или если поля не заполнены
                    messagebox.showinfo("Error", "Can not add", icon="warning")

            else:
                messagebox.showinfo("Error", "Fields can not be empty", icon="warning")

    # Основная функция main(), которая создает графический интерфейс с помощью Tkinter, используя класс Main для управления интерфейсом.








def main():
    root = Tk()
    app = Main(root)
    root.title("Library Management System")
    root.geometry("1200x700+350+200")
    root.mainloop()
#Проверка, запущен ли файл напрямую. Если это так, вызывается функция main() для запуска программы.
if __name__== '__main__':
   main()
