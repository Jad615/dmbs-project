from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import customtkinter #UI library for Tkinter
import sqlite3
import time as tm

#App theme (light or dark)
customtkinter.set_appearance_mode("light")
#Button theme
customtkinter.set_default_color_theme("dark-blue")

#Create root = main window
root = customtkinter.CTk()
root.title("EECE Management System") #title
root.iconbitmap('eece.ico') #icon
root.geometry("1000x650") #dimension
root.resizable(0,0) #disable min/max

#Connect database
conn = sqlite3.connect('EECE.db') #database file
c=conn.cursor() #create cursor
conn.commit() #commit changes
conn.close() #close database

style = ttk.Style() #use ttk styles
style.theme_use('default')

style.configure("Treeview", #configure style of treeview
    background="#D3D3D3",
    foreground="black",
    rowheight=25,
    fieldbackground="#D3D3D3")

style.map('Treeview', #set background when selecting record
    background=[('selected',"#347083")])

my_menu = Menu(root) #menu
root.config(menu=my_menu)

tree_frame = customtkinter.CTkFrame(root) #create tree frame
tree_frame.pack(pady=10)

tree_scrollbar = Scrollbar(tree_frame) #create scrollbar
tree_scrollbar.pack(side=RIGHT,fill=Y)

DataTree = ttk.Treeview(tree_frame,yscrollcommand=tree_scrollbar.set,selectmode="extended") #create treeview
DataTree.pack()

tree_scrollbar.config(command=DataTree.yview) #configure scrollbar going in Y axis

DataTree['columns'] = ("ID","Title","Type","Department") #create columns in treeview [ID | Title | Type | Department]
DataTree.column("#0",width=0,stretch=NO)
DataTree.column("ID",anchor=CENTER,width=35)
DataTree.column("Title",anchor=W,width=739)
DataTree.column("Type",anchor=CENTER,width=90)
DataTree.column("Department",anchor=CENTER,width=90)

DataTree.heading("#0",text="",anchor=W) #configure headings
DataTree.heading("ID",text="ID",anchor=W)
DataTree.heading("Title",text="Title",anchor=CENTER)
DataTree.heading("Type",text="Type",anchor=CENTER)
DataTree.heading("Department",text="Department",anchor=CENTER)

DataTree.tag_configure('oddrow',background="white") #change color for oddrow
DataTree.tag_configure('evenrow',background="lightblue") #change color for evenrow

data_frame = LabelFrame(root,text="Entry Box",font=("arial",13,"bold")) #Entry box labelframe
data_frame.pack(fill="x",expand="yes",padx=20)

data_frame2 = LabelFrame(root,text="")
data_frame2.pack(fill="x",expand="yes",padx=20)

data_frame3 = LabelFrame(root,text="Search",font=("arial",13,"bold"))
data_frame3.pack(fill="x",expand="yes",padx=20)

search_label = customtkinter.CTkLabel(data_frame3,text="Search Keyword",font=("MacOS",15,"bold"))
search_label.grid(row=0,column=0,padx=10,pady=10)
search_entry = Entry(data_frame3,font=("arial",10),width=113)
search_entry.grid(row=0,column=1,padx=10,pady=10)

title_label = customtkinter.CTkLabel(data_frame,text="Title",font=("MacOS",15,"bold")) #entry for title
title_label.grid(row=0,column=0,padx=10,pady=10)
title_entry = Entry(data_frame,font=("arial",10),width=125)
title_entry.grid(row=0,column=1,padx=10,pady=10)

type_label = customtkinter.CTkLabel(data_frame2,text="Type",font=("MacOS",15,"bold")) #entry for type
type_label.grid(row=1,column=0,padx=10,pady=10)
type_entry = Entry(data_frame2,font=("arial",10))
type_entry.grid(row=1,column=1,padx=10,pady=10)

dept_label = customtkinter.CTkLabel(data_frame2,text="Department",font=("MacOS",15,"bold")) #entry for department
dept_label.grid(row=1,column=2,padx=10,pady=10)
dept_entry = Entry(data_frame2,font=("arial",10))
dept_entry.grid(row=1,column=3,padx=10,pady=10)

id_label = customtkinter.CTkLabel(data_frame2,text="ID",font=("MacOS",15,"bold")) #entry for id
id_label.grid(row=1,column=4,padx=10,pady=10)
id_entry = Entry(data_frame2,font=("arial",10))
id_entry.grid(row=1,column=5,padx=10,pady=10)

def display_time(): #display time function
    cur_time = tm.strftime('%I:%M:%S %p')
    clock_label['text'] = cur_time
    root.after(1000,display_time)

def search_record(): #search record function MAIN
    lookup = search_entry.get()

    for record in DataTree.get_children():
        DataTree.delete(record)
    
    conn = sqlite3.connect('EECE.db')
    c=conn.cursor()

    c.execute("SELECT rowid, * FROM EECE WHERE TITLE LIKE ?", ('%'+lookup+'%',))
    records = c.fetchall()
    
    global count
    count = 0
    for record in records:
        if count % 2 == 0:
            DataTree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[2],record[3],record[4]),tags=('evenrow',))
        else:
            DataTree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[2],record[3],record[4]),tags=('oddrow',))
        count += 1
    conn.commit()
    conn.close()
    
'''def search_fn(): #search function window
    global search_entry,search
    search = customtkinter.CTkToplevel(root)
    search.title("Lookup Records")
    search.geometry("400x200")
    search.iconbitmap('eece.ico')
    search.resizable(0,0)

    search_frame = LabelFrame(search,text="Keyword",font=("arial",13,"bold"))
    search_frame.pack(padx=10,pady=10)
    search_entry = Entry(search_frame,font=("arial",10,"bold"),width=50)
    search_entry.pack(padx=20,pady=20)

    search_btn = customtkinter.CTkButton(search,text="Search Records",font=("arial",12),command=search_record)
    search_btn.pack(padx=20,pady=20)'''

def select_record(e): #selecting a record
    title_entry.delete(0,END)
    type_entry.delete(0,END)
    dept_entry.delete(0,END)
    id_entry.delete(0,END)
    
    selected = DataTree.focus()
    values = DataTree.item(selected,'values')

    id_entry.insert(0,values[0])
    title_entry.insert(0,values[1])
    type_entry.insert(0,values[2])
    dept_entry.insert(0,values[3])
    

def clear_entry(): #clear entries
    title_entry.delete(0,END)
    type_entry.delete(0,END)
    dept_entry.delete(0,END)
    id_entry.delete(0,END)
    search_entry.delete(0,END)

def remove_one(): #remove one data
    
    x = DataTree.selection()[0]
    DataTree.delete(x)

    conn = sqlite3.connect('EECE.db')
    c=conn.cursor()
    c.execute("DELETE from EECE WHERE oid="+id_entry.get())

    conn.commit()
    conn.close()

    clear_entry()
        
       

'''def remove_many(): #remove selected data

    x = DataTree.selection()
    id_delete = []
    for record in x:
        id_delete.append(DataTree.item(record,'values')[0])
    for record in x:
        DataTree.delete(record)
    
    conn = sqlite3.connect('EECE.db')
    c=conn.cursor()
    c.executemany("DELETE FROM EECE WHERE id = ?",[(a,) for a in id_delete])

    conn.commit()
    conn.close()

    clear_entry()'''



def refresh(): #refresh DB
    for record in DataTree.get_children():
        DataTree.delete(record)
    
    root.after(1000,query_db)

def update(): #update one data
    selected = DataTree.focus()
    DataTree.item(selected,text="",values=(id_entry.get(),title_entry.get(),type_entry.get(),dept_entry.get()))

    conn = sqlite3.connect('EECE.db')
    c=conn.cursor()
    c.execute("""UPDATE EECE SET
    Title = :title,
    Type = :type,
    Department = :department

    WHERE oid = :oid""",
    {
        'title': title_entry.get(),
        'type': type_entry.get(),
        'department': dept_entry.get(),
        'oid': id_entry.get()
    }
    )
    
    conn.commit()
    conn.close()

    clear_entry()
    messagebox.showinfo("Task","Successfully Updated")

def query_db(): #show DB
    conn = sqlite3.connect('EECE.db')
    c=conn.cursor()

    c.execute("SELECT rowid, * FROM EECE")
    records = c.fetchall()
    
    global count
    count = 0
    for record in records:
        if count % 2 == 0:
            DataTree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[2],record[3],record[4]),tags=('evenrow',))
        else:
            DataTree.insert(parent='',index='end',iid=count,text='',values=(record[0],record[2],record[3],record[4]),tags=('oddrow',))
        count += 1
    conn.commit()
    conn.close()

def add_rec(): #add data
    conn = sqlite3.connect('EECE.db')
    c=conn.cursor()
    c.execute("INSERT INTO EECE VALUES(:id,:title,:type,:department)",
    {
        'id': id_entry.get(),
        'title': title_entry.get(),
        'type': type_entry.get(),
        'department': dept_entry.get(),
    })

    conn.commit()
    conn.close()

    clear_entry()

    DataTree.delete(*DataTree.get_children())

    query_db()

    messagebox.showinfo("Task","Successfully Added")

'''search_menu = Menu(my_menu,tearoff=0) #create search menu
my_menu.add_cascade(label="Search",menu=search_menu)
search_menu.add_command(label="Search",command=search_fn,font=("arial",12))'''

clock_label = Label(root,font=("arial",12),bg='black',fg='green') #display clock
clock_label.pack(pady=2)

btn_frame = LabelFrame(root,text="Commands",font=("arial",13,"bold")) #create button frame
btn_frame.pack(fill="x",expand="yes",padx=20)

update_btn = customtkinter.CTkButton(btn_frame,text="Update Record",font=("arial",12),command=update) #update button
update_btn.grid(row=0,column=0,padx=10,pady=10)

add_btn = customtkinter.CTkButton(btn_frame,text="Add Record",font=("arial",12),command=add_rec) #add button
add_btn.grid(row=0,column=1,padx=10,pady=10)

refresh_btn = customtkinter.CTkButton(btn_frame,text="Refresh Records",font=("arial",12),command=refresh) #refresh button
refresh_btn.grid(row=0,column=2,padx=10,pady=10)

search_btn = customtkinter.CTkButton(btn_frame,text="Search Keyword",font=("arial",12),command=search_record) #remove one button
search_btn.grid(row=0,column=3,padx=10,pady=10)

remove_many_btn = customtkinter.CTkButton(btn_frame,text="Delete Record",font=("arial",12,),command=remove_one) #remove many button
remove_many_btn.grid(row=0,column=4,padx=10,pady=10) 

clear_btn = customtkinter.CTkButton(btn_frame,text="Clear Entry Box",font=("arial",12),command=clear_entry) #clear button
clear_btn.grid(row=0,column=7,padx=10,pady=10)

DataTree.bind("<ButtonRelease-1>",select_record) #bind right click for select

#execute display DB and time
query_db() 
display_time()

root.mainloop() #loop desktop app