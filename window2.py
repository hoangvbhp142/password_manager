from tkinter import PhotoImage, Tk, Label, Button, Entry, Frame, END, Toplevel
from cryptography.fernet import Fernet
from tkinter import ttk
from db_operation import Database
from PIL import Image, ImageTk

class center_frame_window: 
    def __init__(self,root, database):
        with open("key.key", 'rb') as file:
            self.key =  file.read()
        self.fernet = Fernet(self.key)
        img = PhotoImage(file='img\icon.png')
        self.database = database
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("850x420+40+40")
        self.root.configure(bg="orange")
        self.root.resizable(False,False)
        self.root.iconphoto(False,img)
        
        self.center_frame = Frame(root, bg="#d3d3d3")
        self.center_frame.grid(row=0, column=0, padx=10, pady=10)

        self.frame = Frame(self.center_frame,highlightbackground='brown',highlightthickness=2 ,padx=10,pady=20)
        self.frame.grid()
        self.frame1 = Frame(self.center_frame,highlightbackground='black',highlightthickness=1 ,padx=10,pady=20)
        self.frame1.grid()
        
        #Create
        self.create_buttons()
        self.create_records_tree()
        
        self.search_entry = Entry(self.frame,width=20,font = ('Arial',12))
        Button(self.frame,text='Search',background='#def3f6',font = ('Arial',12),width=20, command=self.search).grid(row= self.row_num,column=self.col_num)
        self.col_num +=1
        self.search_entry.grid(row = self.row_num,column = self.col_num)
        
        
    def create_buttons(self):
        self.row_num = 0
        self.col_num = 0
        buttons_info = (('Add','#def3f6',self.add_btn), ('Update','#def3f6',self.update_btn),('Copy Password','#def3f6',self.copy_password),('Delete' , 'red',self.delete_record),('Show All Records','#def3f6',self.show_record),('Encrypt Password','#def3f6',self.encrypt_password))   
        for button in buttons_info:
            if button[0] == 'Show All Records':
                self.row_num += 1
                self.col_num = 0
            Button(self.frame, text=button[0],background=button[1],foreground='black',font=('Arial',12),width=20,pady=1,command=button[2]).grid(row=self.row_num,column=self.col_num,padx= 5,pady=10)    
            self.col_num += 1
    
    def create_entry_labels(self,add_window):
        col_num = row_num = 0
        labels_info =('ID','Website','Username','Password') 
        for label_info in labels_info:
            Label(add_window,text=label_info,font=('Arial',12),padx=5,pady=3).grid(row=row_num,column=col_num,padx=5,pady=2)
            row_num += 1
               
    def create_entry_boxes(self,add_window):
        self.entry_boxes = []
        row_num = 0
        col_num = 1
        for i in range(4):
            showw = ""
            if i == 3:
                showw = "*"
            entry_box = Entry(add_window,width=20,font=("Arial",12),show=showw)
            entry_box.grid(row=row_num,column=col_num,padx=5,pady=2)
            row_num += 1
            self.entry_boxes.append(entry_box)
            
    def create_records_tree(self):
        self.data = []
        # columns = ('ID','Website','Username','Password')
        # self.records_tree = ttk.Treeview(self.center_frame,columns=columns,show='headings')
        # self.records_tree.heading('ID',text='ID')
        # self.records_tree.heading('Website',text='Website')
        # self.records_tree.heading('Username',text='Username')
        # self.records_tree.heading('Password',text='Password')
        # self.records_tree.grid(padx=10, pady=10)
        columns = ("ID", "Website", "Username", "Password")
        self.records_tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.records_tree.heading("ID", text="ID")
        self.records_tree.heading("Website", text="Website")
        self.records_tree.heading("Username", text="Username")
        self.records_tree.heading("Password", text="Password")

        self.records_tree["display"] = ("Website", "Username")
        def item_selected(event):
            for selected_item in self.records_tree.selection():
                item = self.records_tree.item(selected_item)
                self.data = item["values"]
                # record = item["values"]
                # for entry_box, item in zip(self.entry_boxes, record):
                #     entry_box.delete(0, END)
                #     entry_box.insert(0, item)

        self.records_tree.bind("<<TreeviewSelect>>", item_selected)

        self.records_tree.grid()
            
    def add_btn(self):
        self.add_window = Tk()
        self.add_window.title("Add new record")
        self.add_window.resizable(False,False)
        self.create_entry_labels(self.add_window)
        self.create_entry_boxes(self.add_window)
        add_window_btn = Button(self.add_window, text='Add',font=('Arial',12),width=10,pady=1,background='#def3f6',command=self.add_record).grid(row=4,column=0,padx= 5,pady=10)
        self.add_window.mainloop()

    def update_btn(self):
        self.update_window = Tk()
        self.update_window.title("Update record")
        self.update_window.resizable(False,False)
        self.create_entry_labels(self.update_window)
        self.create_entry_boxes(self.update_window)

        for entry_box, item in zip(self.entry_boxes, self.data):
            entry_box.delete(0, END)
            entry_box.insert(0, item)

        update_window_btn = Button(self.update_window, text='Update',font=('Arial',12),width=10,pady=1,background='#def3f6',command=self.update_record).grid(row=4,column=0,padx= 5,pady=10)
        self.update_window.mainloop()

    def add_record(self):
        website = self.entry_boxes[1].get()
        username = self.entry_boxes[2].get()
        password = self.entry_boxes[3].get().encode()
        data = {"website": website, "username": username, "password": password}
        self.database.create_record(data)
        self.show_record()
        
    def update_record(self):
        ID = self.entry_boxes[0].get()
        website = self.entry_boxes[1].get()
        username = self.entry_boxes[2].get()
        password = self.entry_boxes[3].get().encode()

        data = {"ID": ID, "website": website, "username": username, "password": password}
        self.database.update_record(data)
        self.show_record()    
    
    def delete_record(self):
        if len(self.data) == 0:
            return
        ID = self.data[0]
        self.database.delete_record(ID)
        self.show_record()

    def show_record(self):
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)

        password_list = self.database.show_records()
        for record in password_list:
            self.records_tree.insert("", END,
                                     values=(record[0], record[3], record[4], record[5]))
    
    def encrypt_password(self):
        pass
    
    def show_message(self, title_box: str = None, message: str = None):
        TIME_TO_WAIT = 900
        root = Toplevel(self.root)
        background = "green"
        if title_box == "Error":
            background = "red"
        root.geometry("200x50+600+300")
        root.title(title_box)
        Label(root, text=message, background=background,
              font=("Time New Roman", 15), fg="white").pack()
        try:
            root.after(TIME_TO_WAIT, root.destroy)
        except Exception as e:
            print("Error", e)

    def copy_password(self):
        if len(self.data) == 0:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(self.fernet.decrypt(bytes(self.data[3][2:-1], 'utf-8')).decode())
        message = "Copied"
        title = "Copy"
        if self.data[3] == "":
            message = "Box is empty"
            title = "Error"
        self.show_message(title, message)    
    
    def search(self):
        website = self.search_entry.get()
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)

        password_list = self.database.search_record(website)
        for record in password_list:
            self.records_tree.insert("", END,
                                     values=(record[0], record[3], record[4], record[5]))