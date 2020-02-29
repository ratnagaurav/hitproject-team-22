from tkinter import *	
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename
import sqlite3
import os


def newFile():
    global file
    note.title("Untitled - Notepad")
    file = None
    TextArea.delete(1.0, END)

def open_select():
    file = var.get()
    if file == "":
        file = None
    else:
        note.title(os.path.basename(file) + " - Notepad")
        TextArea.delete(1.0, END)
        f = open(file, "r")
        TextArea.insert(1.0, f.read())
        f.close()
    open_window.destroy()
def openFile():
    global file
    global open_window
    open_window=Toplevel(note)
    open_window.title("Open Files")
    open_window.geometry('300x250')
    
    Label(open_window, text="Select a file",font=('calibri',13)).pack(anchor='w')
    with open('file_data.txt','r') as f:
        d=f.read()
    a=eval(d)
    for key in a.keys():
        if key==username_verify.get(): #change krna hai
            temp_file_list=a[key]
    

    
    if temp_file_list==[]:
    	open_window.destroy()
    	showinfo('Info','No files saved')

    else:
	    global var
	    var = StringVar()
	    var.set("radio") #for initializing

	    for item in temp_file_list:
	        Radiobutton(open_window, text=os.path.basename(item), variable=var, value=item).pack(anchor='w')

	    Button(open_window,text="Open", command=open_select).pack()

    


def saveFile():
    global file
    if file == None:
        file = asksaveasfilename(initialfile = 'Untitled.txt', defaultextension=".txt",
                           filetypes=[("All Files", "*.*"),
                                     ("Text Documents", "*.txt")])
        if file =="":
            file = None

        else:
            #Save as a new file
            f = open(file, "w")
            f.write(TextArea.get(1.0, END))
            f.close()

            note.title(os.path.basename(file) + " - Notepad")
    else:
        # Save the file
        f = open(file, "w")
        f.write(TextArea.get(1.0, END))
        f.close()

    with open('file_data.txt','r') as f:
        d=f.read()
    a=eval(d)
    for key in a.keys():
        if key==username_verify.get():           #change krna hai
            a[key].append(file)

    with open('file_data.txt','w') as f:
        f.write(str(a))                        

def quitApp():
    note.destroy()

def cut():
    TextArea.event_generate(("<<Cut>>"))

def copy():
    TextArea.event_generate(("<<Copy>>"))

def paste():
    TextArea.event_generate(("<<Paste>>"))

def about():
    showinfo("Notepad", "Notepad by Ratna Gaurav")

def notepad():
    global note
    note = Toplevel(root)
    note.title("Untitled - Notepad")
    note.wm_iconbitmap("1.ico")
    note.geometry("644x788")

    #Add TextArea
    global TextArea
    global file
    TextArea = Text(note, font="lucida 13")
    file = None
    TextArea.pack(expand=True, fill=BOTH)

    # Lets create a menubar
    MenuBar = Menu(note)

    #File Menu Starts
    FileMenu = Menu(MenuBar, tearoff=0)
    # To open new file
    FileMenu.add_command(label="New", command=newFile)

    #To Open already existing file
    FileMenu.add_command(label="Open", command = openFile)

    # To save the current file

    FileMenu.add_command(label = "Save", command = saveFile)
    FileMenu.add_separator()
    FileMenu.add_command(label= "Logout",command= quitApp)
    FileMenu.add_command(label = "Exit", command = quitApp)
    MenuBar.add_cascade(label = "File", menu=FileMenu)
    # File Menu ends

    # Edit Menu Starts
    EditMenu = Menu(MenuBar, tearoff=0)
    #To give a feature of cut, copy and paste
    EditMenu.add_command(label = "Cut", command=cut)
    EditMenu.add_command(label = "Copy", command=copy)
    EditMenu.add_command(label = "Paste", command=paste)

    MenuBar.add_cascade(label="Edit", menu = EditMenu)

    # Edit Menu Ends

    # Help Menu Starts
    HelpMenu = Menu(MenuBar, tearoff=0)
    HelpMenu.add_command(label = "About Notepad", command=about)
    MenuBar.add_cascade(label="Help", menu=HelpMenu)

    # Help Menu Ends

    note.config(menu=MenuBar)

    #Adding Scrollbar
    Scroll = Scrollbar(TextArea)
    Scroll.pack(side=RIGHT,  fill=Y)
    Scroll.config(command=TextArea.yview)
    TextArea.config(yscrollcommand=Scroll.set)

def register_user():
	username_info=username.get()
	password_info=password.get()


	#code to write user file names
	with open('file_data.txt','r') as f:
		d=f.read()
	# a contains dictionary of user file in dict format
	a=eval(d)
	a.update({username_info:[]})
	#writing back the dict value in file
	with open('file_data.txt','w') as f:
		f.write(str(a))



	if username_info=="":
		empty_username()
	elif password_info=="":
		empty_password()
	else:
		#Database connection logic
		conn=sqlite3.connect('notepad_user.db')
		c=conn.cursor()
		c.execute("INSERT INTO users VALUES(:username,:password)",

			{
				'username':username_info,
				'password':password_info
			})


		conn.commit()
		conn.close()
		showinfo('Info','Successfully Registered')

	username_entry.delete(0, END)
	password_entry.delete(0, END)
	

def invalid_credentials():
	showinfo('Error','Incorrect Username or Password')

def empty_username():
	showinfo('Error',"Username can't be empty")

def empty_password():
	showinfo('Error',"Password can't be empty")



def login_verify():
	username_info=username_verify.get()
	password_info=password_verify.get()

	conn=sqlite3.connect('notepad_user.db')
	c=conn.cursor()

	c.execute("SELECT * FROM users WHERE (username=:user AND password=:pass)", {'user':username_info,'pass':password_info})
	result=c.fetchone()

	if result!=None:
		notepad()
		login_window.destroy()
	else:
		invalid_credentials()
		username_login_entry.delete(0, END)
		password_login_entry.delete(0, END)

	conn.commit()
	conn.close()

	
def login():
	global login_window
	login_window=Toplevel(root)
	login_window.title("Login")
	login_window.geometry("300x250")

	Label(login_window, text="Please enter details below to login").pack()
	Label(login_window, text="").pack()
 
	global username_verify
	global password_verify
 
	username_verify = StringVar()
	password_verify = StringVar()
 
	global username_login_entry
	global password_login_entry
 
	Label(login_window, text="Username").pack()
	username_login_entry = Entry(login_window, textvariable=username_verify)
	username_login_entry.pack()

	Label(login_window, text="").pack()

	Label(login_window, text="Password").pack()
	password_login_entry = Entry(login_window, textvariable=password_verify, show='*')
	password_login_entry.pack()

	Label(login_window, text="").pack()

	Button(login_window, text="Login", width=10, height=1, command = login_verify).pack()

def register():
	global reg_window
	reg_window=Toplevel(root)
	reg_window.geometry('300x250')
	reg_window.title('Registeration Details')

	global username
	global password
	global username_entry
	global password_entry

	username=StringVar()
	password=StringVar()

	Label(reg_window,text="Please enter the Details",font=('Calibri',13)).pack()

	username_label=Label(reg_window,text="Username",font=('Calibri',12))
	username_label.pack()
	username_entry=Entry(reg_window,textvariable=username)
	username_entry.pack()
	password_label=Label(reg_window,text="Password",font=('Calibri',12))
	password_label.pack()
	password_entry=Entry(reg_window,textvariable=password, show='*')
	password_entry.pack()

	Label(reg_window,text="").pack()

	Button(reg_window, text='Register',width='10', height='1',command=register_user).pack()



def first_screen():
	global root
	root = Tk()
	root.geometry('300x250')
	root.title('Welcome to NoteBook')
	root.wm_iconbitmap('1.ico')
	Label(text="Login/Register",width='300',height='2',font=('Calibri',13)).pack()
	Label(text="").pack()

	Button(text="Login",width='30',height='2',command=login).pack()
	Label(text="OR",height='2').pack()

	Button(text="Register",width='30',height='2',command=register).pack()


	root.mainloop()
first_screen()