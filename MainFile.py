from tkinter import *
from tkinter import ttk
from random import *

#colors
reds = ['brown1', 'crimson', 'firebrick2', 'lightcoral', 'orangered2', 'red2', 'tomato3', 'violetred3', 'red4', 'orange', 'mediumvioletred']
greens = ['steelblue3', 'turquoise4', 'skyblue3', 'royalblue3', 'blue3', 'navy', 'midnightblue', 'indigo', 'dodgerblue3', 'deepskyblue3', 'cornflowerblue']
blocked = ['Марка','Модель','Цилиндры']

def rebuild():
    global headings, content, table
    table.forget()
    table = ttk.Treeview(window, columns = ['ID'] + headings, show = 'headings', selectmode = 'browse')
    table.column('ID', width=100, anchor='c')
    table.heading('ID', text='ID')
    for i in range(len(headings)):
        table.column(headings[i], width=100, anchor='c')
        table.heading(headings[i], text=headings[i])
    table.pack(side=TOP)
    num = 1
    for val in content:
        val = [str(num)] + val
        table.insert(parent='', index=END, values = val)
        num += 1
    vsb = Scrollbar(table, orient=VERTICAL, command=table.yview)
    table.config(yscrollcommand=vsb.set)

def save_check():
    global CTS
    if CTS == 3:
        save()

def save():
    global headings, content, CTS, save_frame
    with open('BD.txt', 'w', encoding='UTF-8') as file:
        file.write('|'.join(headings + ['\n']))
        for char_str in content:
            file.write('|'.join(char_str + ['\n']))
        file.close()
    CTS = 0
    save_label = Label(save_frame, text='$', fg='blue')
    save_label.pack(side=LEFT)
    

def foreign():
    global last_fr
    last_fr.forget()

#search
def search():
    global search_entry, content, headings
    try:
        search_res = search_entry.get().title()
        rows = []
        for row in content:
            if search_res in row:
                row = [content.index(row) + 1] + row
                rows.append(row)
        if len(rows) == 0:
            raise ValueError
        search_window = Tk()
        search_window.title("Необходимые строки")
        search_table = ttk.Treeview(search_window, columns = ['ID'] + headings, show = 'headings', selectmode = 'browse')
        search_table.column('ID', width=100, anchor='c')
        search_table.heading('ID', text='ID')
        for i in range(len(headings)):
            search_table.column(headings[i], width=100, anchor='c')
            search_table.heading(headings[i], text=headings[i])
        search_table.pack()
        for row in rows:
            search_table.insert(parent='', index=END, values = row)
    except ValueError:
        status.config(text='Таких элементов не существует', fg=choice(reds))
    
def search_fr():
    global last_fr, search_entry
    foreign()
    search_frame = Frame(window, width=200, height=200, borderwidth=5, relief=GROOVE)
    search_title = Label(search_frame, text='ПОИСК', font='Calibri 18 bold')
    search_label = Label(search_frame, text='номер строки')
    search_entry = Entry(search_frame, width=30)
    search_button1 = Button(search_frame, text='НАЙТИ', bg='red', fg='white', width=25, command=search)
    search_frame.pack(side=BOTTOM, padx=20)
    search_title.pack(pady=10)
    search_label.pack()
    search_entry.pack()
    search_button1.pack(pady=5)
    last_fr = search_frame

#add
def add():
    global add_entry, content, headings, CTS
    add_res = add_entry.get()
    added = [sub.title() for sub in add_res.split()]
    if len(added) > len(headings):
        status.config(text='Слишком много значений', fg=choice(reds))
    else:
        if add_res == '':
            content.append([' ' for sub in headings])
            status.config(text='Добавлена пустая строка', fg=choice(greens))
        else:
            content.append(added)
            x = len(headings) - len(content[-1])
            for _ in range(x):
                content[-1].append(' ')
            status.config(text='Добавлена строка со значениями', fg=choice(greens))
        CTS += 1
        save_check()
        rebuild()
    
def add_fr():
    global last_fr, add_entry
    foreign()
    add_frame = Frame(window, width=200, height=200, borderwidth=5, relief=GROOVE)
    add_title = Label(add_frame, text='ДОБАВЛЕНИЕ', font='Calibri 18 bold')
    add_label = Label(add_frame, text='значения строки')
    add_entry = Entry(add_frame, width=30)
    add_button1 = Button(add_frame, text='ДОБАВИТЬ', bg='blue', fg='white', width=25, command=add)
    add_frame.pack(side=BOTTOM, padx=20)
    add_title.pack(pady=10)
    add_label.pack()
    add_entry.pack()
    add_button1.pack(pady=5)
    last_fr = add_frame

#edit
def edit():
    global edit_entry_row, edit_entry_col, edit_entry_new, content, headings, CTS
    try:
        edit_row = int(edit_entry_row.get())
        edit_col = edit_entry_col.get().title()
        if edit_col in blocked:
            raise ZeroDivisionError
        edit_col = headings.index(edit_col)
        if edit_row <= 0 or edit_row > len(content):
            raise IndexError
        edit_new = edit_entry_new.get().title()
        content[edit_row - 1][edit_col] = edit_new
        status.config(text='Изменено', fg=choice(greens))
        CTS += 1
        save_check()
        rebuild()
    except ValueError:
        status.config(text='Введена некорректная характеристика', fg=choice(reds))
    except IndexError:
        status.config(text='Несуществующая строка', fg=choice(reds))
    except ZeroDivisionError:
        status.config(text='Неизменяемая характеристика', fg=choice(reds))

def edit_fr():
    global last_fr, edit_entry_row, edit_entry_col, edit_entry_new
    foreign()
    edit_frame = Frame(window, width=200, height=200, borderwidth=5, relief=GROOVE)
    edit_title = Label(edit_frame, text='ИЗМЕНЕНИЕ', font='Calibri 18 bold')
    edit_label_row = Label(edit_frame, text='номер строки')
    edit_entry_row = Entry(edit_frame, width=30)
    edit_label_col = Label(edit_frame, text='изменяемая характеристика')
    edit_entry_col = Entry(edit_frame, width=30)
    edit_label_new = Label(edit_frame, text='новое значение')
    edit_entry_new = Entry(edit_frame, width=30)
    edit_button1 = Button(edit_frame, text='ИЗМЕНИТЬ', bg='white', fg='white', width=25, command=edit)
    edit_frame.pack(side=BOTTOM, padx=20)
    edit_title.pack(pady=10)
    edit_label_row.pack()
    edit_entry_row.pack()
    edit_label_col.pack()
    edit_entry_col.pack()
    edit_label_new.pack()
    edit_entry_new.pack()
    edit_button1.pack(pady=5)
    last_fr = edit_frame

#expand
def expand():
    global expand_entry, content, headings, CTS
    expand_res = expand_entry.get().title()
    if expand_res not in headings and expand_res != 'Id':
        headings.append(expand_res)
        for string in content:
            string.append(' ')
        status.config(text='Добавлена новая характеристика', fg=choice(greens))
        CTS += 1
        save_check()
        rebuild()
    else:
        status.config(text='Эта характеристика уже в таблице', fg=choice(reds))
    
def expand_fr():
    global last_fr, expand_entry
    foreign()
    expand_frame = Frame(window, width=200, height=200, borderwidth=5, relief=GROOVE)
    expand_title = Label(expand_frame, text='РАСШИРЕНИЕ', font='Calibri 18 bold')
    expand_label = Label(expand_frame, text='новая характеристика')
    expand_entry = Entry(expand_frame, width=30)
    expand_button1 = Button(expand_frame, text='РАСШИРИТЬ', bg='pink', fg='white', width=25, command=expand)
    expand_frame.pack(side=BOTTOM, padx=20)
    expand_title.pack(pady=10)
    expand_label.pack()
    expand_entry.pack()
    expand_button1.pack(pady=5)
    last_fr = expand_frame

#delete
def delete():
    global delete_entry, content, headings, CTS
    try:
        delete_res = int(delete_entry.get())
        if delete_res <= 0 or delete_res > len(content):
            raise IndexError
        del content[delete_res - 1]
        status.config(text='Строка удалена', fg=choice(greens))
        CTS += 1
        save_check()
        rebuild()
    except ValueError:
        status.config(text='Некорректные данные', fg=choice(reds))
    except IndexError:
        status.config(text='Несуществующая строка', fg=choice(reds))
    
def delete_fr():
    global last_fr, delete_entry
    foreign()
    delete_frame = Frame(window, width=200, height=200, borderwidth=5, relief=GROOVE)
    delete_title = Label(delete_frame, text='УДАЛЕНИЕ', font='Calibri 18 bold')
    delete_label = Label(delete_frame, text='номер строки')
    delete_entry = Entry(delete_frame, width=30)
    delete_button1 = Button(delete_frame, text='УДАЛИТЬ', bg='black', fg='white', width=25, command=delete)
    delete_frame.pack(side=BOTTOM, padx=20)
    delete_title.pack(pady=10)
    delete_label.pack()
    delete_entry.pack()
    delete_button1.pack(pady=5)
    last_fr = delete_frame

#narrow
def narrow():
    global narrow_entry, content, headings, CTS
    try:
        narrow_res = narrow_entry.get().title()
        if narrow_res in blocked:
            raise ZeroDivisionError
        narrow_res = headings.index(narrow_res)
        del headings[narrow_res]
        for string in content:
            del string[narrow_res]
        status.config(text='Характеристика удалена', fg=choice(greens))
        CTS += 1
        save_check()
        rebuild()
    except ZeroDivisionError:
        status.config(text='Нельзя такое удалять', fg=choice(reds))
    except ValueError:
        status.config(text='Некорректные данные', fg=choice(reds))

def narrow_fr():
    global last_fr, narrow_entry
    foreign()
    narrow_frame = Frame(window, width=200, height=200, borderwidth=5, relief=GROOVE)
    narrow_title = Label(narrow_frame, text='СУЖЕНИЕ', font='Calibri 18 bold')
    narrow_label = Label(narrow_frame, text='ненужная характеристика')
    narrow_entry = Entry(narrow_frame, width=30)
    narrow_button1 = Button(narrow_frame, text='СУЗИТЬ', bg='green', fg='white', width=25, command=narrow)
    narrow_frame.pack(side=BOTTOM, padx=20)
    narrow_title.pack(pady=10)
    narrow_label.pack()
    narrow_entry.pack()
    narrow_button1.pack(pady=5)
    last_fr = narrow_frame

#content
with open('BD.txt', 'r+', encoding='UTF-8') as file:
    file = file.readlines()
    headings = file[0].split('|')[:-1]
    content = [sub.split('|')[:-1] for sub in file[1:]]
CTS = 0

#window
window = Tk()
window.title('ППЧ')

#title
status = Label(window, text='', font='Calibri 18')
status.pack()
last_fr = Label(window, text='')
last_fr.pack()

#buttons
main_frame = Frame(window, width=200, height=200, borderwidth=10, relief=GROOVE)
frame_label = Label(main_frame, text='команды', font='Calibri 16 bold')
search_button = Button(main_frame, text='ПОИСК', bg='yellow', fg='white', width=30, command=search_fr)
add_button = Button(main_frame, text='ДОБАВЛЕНИЕ', bg='blue', fg='white', width=30, command=add_fr)
edit_button = Button(main_frame, text='ИЗМЕНЕНИЕ', bg='black', fg='white', width=30, command=edit_fr)
expand_button = Button(main_frame, text='РАСШИРЕНИЕ', bg='red', fg='white', width=30, command=expand_fr)
delete_button = Button(main_frame, text='УДАЛЕНИЕ', bg='white', fg='white', width=30, command=delete_fr)
narrow_button = Button(main_frame, text='СУЖЕНИЕ', bg='green', fg='white', width=30, command=narrow_fr)
save_button = Button(main_frame, text='СОХРАНЕНИЕ', bg='pink', fg='white', width=30, command=save)
frame_label.pack()
search_button.pack()
add_button.pack()
edit_button.pack()
expand_button.pack()
delete_button.pack()
narrow_button.pack()
save_button.pack()
main_frame.pack(side=LEFT, padx=20)

#save
save_frame = Frame(window)
save_frame.pack(side=BOTTOM)

#table
table = ttk.Treeview(window, columns = ['ID'] + headings, show = 'headings', selectmode = 'browse')
table.column('ID', width=100, anchor='c')
table.heading('ID', text='ID')
for i in range(len(headings)):
    table.column(headings[i], width=100, anchor='c')
    table.heading(headings[i], text=headings[i])
table.pack(side=TOP)
#values+scrolling
num = 1
for val in content:
    val = [str(num)] + val
    table.insert(parent='', index=END, values = val)
    num += 1
vsb = Scrollbar(table, orient=VERTICAL, command=table.yview)
table.config(yscrollcommand=vsb.set)

window.mainloop()
