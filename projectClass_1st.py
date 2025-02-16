from tkinter import Tk, Label,Frame,Entry,Button,messagebox,simpledialog,StringVar,filedialog,Checkbutton,BooleanVar
from tkinter.ttk import Combobox
import time
from PIL import Image,ImageTk
import autotable_creation
import random
import sqlite3
import gmail
from tkintertable import TableCanvas, TableModel
import re
import shutil
import string
import os

#Window screen   ---> first to define window screen                                   ===========================================                                              
win = Tk()
win.title('Banking-System')
win.state('zoomed')
win.resizable(width=False, height=False)
win.configure(bg='red4')

#image logo on top left corner of parent window(win)                                  ===========================================
try:
    img = Image.open('1stLogo.jpg').resize((145, 95))
    bit_image = ImageTk.PhotoImage(img, master=win)
    logo_label = Label(win, image=bit_image,bg='red4')
    logo_label.place(relx=0,rely=0)
    # pass
except OSError:
    messagebox.showerror("Error","Image file not found")   




# Header Section of parent window(win)                                                                            ===========================================
Header_title = Label(win, text='Banking Automation',relief='flat', font=('arial', 30, 'bold'),bg='red4', fg='#FF7D40')
Header_title.place(relx=.12,rely=0)


def update_time():
    global current_date,current_time
    current_date = time.strftime("%d/%b/%Y")
    current_time = time.strftime("%H:%M:%S")
    header_date.configure(text=f'Date- {current_date} ')
    header_time.configure(text=f'Time- {current_time} ')

    header_date.after(1000,update_time)# 1000 miliseconds = 1 second before calling the update_time function again.

header_date = Label(win, text='',relief='flat', font=('arial', 15, 'bold'), bg='red4',fg='darkgoldenrod2')
header_date.place(relx=.12,rely=.1)

header_time = Label(win, text='',relief='flat', font=('arial', 15, 'bold'), bg='red4',fg='darkgoldenrod2')
header_time.place(relx=.88,rely=.1)
#footer section of parent window(win)                                                                              ===============================================
# footer_title=Label(win,text='Developed by: Manish Arya\nEmail : mannuarya2002@gmail.com\nProject Guide : Mr. Aditya Kumar',font=('arial', 15, 'bold'), bg='red4')
# footer_title.pack(side='bottom'9)
footer_title=Label(win,text='Project Guide : Mr. Aditya Kumar',relief='flat',font=('arial', 15, 'bold'),fg='floralwhite',bg='red4')
footer_title.pack(side='bottom')
footer_title=Label(win,text='Email : mannuarya2002@gmail.com',relief='flat',font=('arial', 15, 'bold'),fg='#33A1C9', bg='red4')
footer_title.pack(side='bottom')
footer_title=Label(win,text='Developed by: Manish Arya',relief='flat',font=('arial', 15, 'bold'),fg='floralwhite', bg='red4')
footer_title.pack(side='bottom')


#function to create a child window of parent window(win)           ---- login screen========================================================================



def main_screen():      #function
    frm=Frame(win,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='floralwhite')
    frm.place(relx=0,rely=.14,relwidth=1,relheight=.74)

    def Exit():
        resp=messagebox.askyesno('Exit','Do you want to exit?\nKindly confirm!')
        if resp:
            win.destroy()

    def toggle_password():
        if show_var.get():
            pass_entry.config(show='')
        else:
            pass_entry.config(show='*')

    forgot_btn=Button(frm,text='Exit',width=10,font=('arial',15,'bold'),bd=5,bg='red4',fg='floralwhite',command=Exit,cursor='hand2')
    forgot_btn.pack(side='top',anchor='e')


    acnt_label=Label(frm,text='Accnt.no.',font=('arial',20,'bold'),bg='floralwhite',fg='red4')
    acnt_label.place(relx=.3,rely=.2)
    acnt_entry=Entry(frm,font=('arial',20,'bold'),bd=5,relief='groove')
    acnt_entry.place(relx=.45,rely=.2)
    acnt_entry.focus()

 
    pass_label=Label(frm,text='Pass',font=('arial',20,'bold'),bg='floralwhite',fg='red4')
    pass_label.place(relx=.3,rely=.3)
    pass_entry=Entry(frm,font=('arial',20,'bold'),bd=5,show='*',relief='groove')
    pass_entry.place(relx=.45,rely=.3)

    # Define show_var BEFORE using it
    show_var = BooleanVar(value=False)
    # Checkbox to show or hide the password
    show_check = Checkbutton(frm, text='Show Password', font=('arial', 10,'bold'),fg='darkgoldenrod2',bg='floralwhite',variable=show_var, onvalue=True, offvalue=False,command=toggle_password,cursor='hand2')
    show_check.place(relx=.45, rely=.39)

    role_label=Label(frm,text='Role',font=('arial',20,'bold'),bg='floralwhite',fg='red4')
    role_label.place(relx=.3,rely=.45)
    role_cb=Combobox(frm,font=('arial',20,'bold'),values=['User','Admin'],state='readonly',cursor='hand2',height=5)      #combo box  ========================================
    role_cb.current(0)
    role_cb.place(relx=.45,rely=.45)

    global cap
    cap=''
    def gen_captcha():
        global cap
            # Generates a random 6-character captcha
        cap = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return cap

        # global cap
        # d=str(random.randint(0,9))
        # cap=cap+d
        # ch=chr(random.randint(65,90))
        # cap=cap+ch

        # d=str(random.randint(0,9))
        # cap=cap+d
        # ch=chr(random.randint(65,90))
        # cap=cap+ch
    
        # d=str(random.randint(0,9))
        # cap=cap+d
        # ch=chr(random.randint(65,90))
        # cap=cap+ch
        # return cap
    #login button Function #                                                     ============================================================    
    def login_click():
        global uacn
        global uname
        try:
            uacn=acnt_entry.get().strip()
            upass=pass_entry.get().strip()            
            urole=role_cb.get().strip()

            if len(uacn) == 0 or len(upass) == 0:
                messagebox.showerror("Error","Entries can't be empty.")
                return

            if not re.fullmatch('[0-9 ]+',uacn):
                messagebox.showerror('Error','Kindly enter valid Account number!')
                return
            if not re.fullmatch('[0-9a-zA-Z@#$%&* ]+',upass):
                messagebox.showerror('Error','Kindly enter valid Password!')
                return
            if len(uacn) == 0 or len(upass) == 0:
                messagebox.showwarning("Empty Entries","Acn or Pass can't be empty.")
                return
            
            if captcha_entry.get()!= cap:
                messagebox.showerror("login","Invaid Captcha")
                return
            
            


            uacn=int(uacn)
            if uacn==0 and upass=='a' and urole=='Admin':
                frm.destroy()
                Admin_win()
            elif urole=='User':
                con_obj=sqlite3.connect(database='BankDetails.sqlite')
                cur_obj=con_obj.cursor()
                cur_obj.execute('select * from users where users_acno=? and users_pass=?',(uacn,upass))
                tup=cur_obj.fetchone()
                if tup==None:
                    messagebox.showerror("Error","Invalid Account No. or Password")
                else:
                    global uname
                    uname=tup[2]
                    frm.destroy()
                    User_win()
            else:
                messagebox.showerror('Error',"Invalid Role.")
        except ValueError:
            messagebox.showinfo("Login","Enter valid details according to your role. ")

    def RESET():
        acnt_entry.delete(0,"end")
        pass_entry.delete(0,"end")
        acnt_entry.focus()

    # Function to refresh captcha
    def refresh_captcha():
        global gen_captcha_Lab
        # Clear the old captcha by setting text to an empty string
        gen_captcha_Lab.config(text='')
        gen_captcha_Lab.destroy()
        # Generate new captcha and update the label
        new_captcha = gen_captcha()
        gen_captcha_Lab = Label(frm, text=new_captcha, relief='flat', font=('arial', 20, 'bold'),bg='floralwhite', fg='green')
        gen_captcha_Lab.place(relx=.45, rely=.54)
        # gen_captcha_Lab.config(text=new_captcha)


    #buttons                                                                    ===================================================================
    global gen_captcha_Lab
    gen_captcha_Lab=Label(frm,text=gen_captcha(),relief='flat',font=('arial',20,'bold'),bg='floralwhite',fg='green')
    gen_captcha_Lab.place(relx=.45,rely=.54)

    refresh_img = Image.open('refresh.png').resize((25, 25))
    refresh_icon = ImageTk.PhotoImage(refresh_img)    # Refresh button to generate new captcha
    refresh_btn = Button(frm, image=refresh_icon,font=('arial', 10),command=refresh_captcha, relief='flat', bg='floralwhite',fg='darkgoldenrod2',cursor='hand2')
    refresh_btn.place(relx=.55, rely=.56)
    # Necessary to prevent image garbage collection
    refresh_btn.image = refresh_icon

    Captcha_Lab=Label(frm,text='Captcha',font=('arial',20,'bold'),bg='floralwhite',fg='red4')
    Captcha_Lab.place(relx=.3,rely=.65)
    captcha_entry=Entry(frm,font=('arial',20,'bold'),bd=5,relief='groove')
    captcha_entry.place(relx=.45,rely=.65)

    login_btn=Button(frm,text='Login',relief='raised',width=6,font=('arial',15,'bold'),bd=5,bg='red4',fg='floralwhite',command=login_click,cursor='hand2')
    login_btn.place(relx=.7,rely=.65)
    reset_btn=Button(frm,text='Reset',command=RESET,relief='raised',width=6,font=('arial',15,'bold'),bd=5,bg='red4',fg='floralwhite',cursor='hand2')
    reset_btn.place(relx=.7,rely=.8)
    forgot_btn=Button(frm,text='Forgot Password',relief='raised',width=15,font=('arial',15,'bold'),bd=5,bg='red4',fg='floralwhite',command=forgot_pass_win,cursor='hand2')
    forgot_btn.place(relx=.52,rely=.8)

  


#Admin screen inside frm(main_screen) window ---> nested function                           =======================================================================    
def Admin_win():
    admn_frm=Frame(win,highlightbackground='black',highlightthickness=2)
    admn_frm.configure(bg='floralwhite')
    admn_frm.place(relx=0,rely=.14,relwidth=1,relheight=.74)
    

    #currently active child frame locator variable
    current_child_frm   =   None

    #function to destroy current child frame
    def destroy_current_child_frm():
        nonlocal current_child_frm
        if current_child_frm:
            current_child_frm.destroy()
            current_child_frm = None


    #logout function inside Admin_win() function                           =======================================================================
    def AdminLgout_click():
        resp=messagebox.askyesno('logout','Do you want to logout?\nKindly confirm!')
        if resp :       #default is always True this is why we don't use if resp ==True:
            admn_frm.destroy()
            main_screen()
 

 
 

    def create_click():
        destroy_current_child_frm()
        nonlocal current_child_frm
        current_child_frm=Frame(admn_frm,highlightbackground='black',highlightthickness=2)
        current_child_frm.configure(bg='red4')
        current_child_frm.place(relx=.2,rely=.11,relwidth=.6,relheight=.8)
        inner_create_frm_title_label=Label(current_child_frm,text='Create-Users',relief='flat',font=('arial',10,'bold'),bg='red4',fg='floralwhite')
        inner_create_frm_title_label.pack()

        def open_acn():
            uname=user_name_entry.get().strip()
            umob=user_mob_entry.get().strip()
            uemail=user_email_entry.get().strip()
            uadhar=user_adhar_entry.get().strip()
            ubal=0
            upass=str(random.randint(100000,999999))
            current_date = time.strftime("%d/%b/%Y")

            if len(uname) == 0 or len(umob) ==0 or len(uemail) == 0 or len(uadhar) == 0:
                messagebox.showerror('Error','Empty fields are not allowed.')
                return
            
            # if len(umob) != 10 or len(uadhar) !=12:
            #     messagebox.showerror('Error','')
            if not re.fullmatch('[a-zA-Z ]+',uname):
                messagebox.showerror('Error','Kindly enter valid name')
                return
            
            if not re.fullmatch('[6-9][0-9]{9}',umob):
                messagebox.showerror('Error','Invalid Mobile Number')
                return
            
            if not re.fullmatch('[a-z0-9_.]+@[a-z]+[.][a-z]+',uemail):
                messagebox.showerror('Error','Invalid Email Format')
                return

            if not re.fullmatch('[0-9]{12}',uadhar):
                messagebox.showerror('Error','Invalid Aadhar Number')
                return
            
            con_obj=sqlite3.connect(database='BankDetails.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('insert into users(users_pass,users_name,users_mob,users_email,users_balance,users_adhar,users_opendate)values(?,?,?,?,?,?,?)',(upass,uname,umob,uemail,ubal,uadhar,current_date))
            con_obj.commit()
            con_obj.close()

            con_obj=sqlite3.connect(database='BankDetails.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select max(users_acno) from users')
            tup=cur_obj.fetchone()
            uacno=tup[0]
            con_obj.close()

            try:
                gmail_con=gmail.GMail('mannuarya2002@gmail.com','zrth fyvp pywf lkee')
                umsg=f'''Hello,{uname}
                Welcome to our XYZ Bank
                Your Account is : {uacno}
                Your Pass is : {upass}
                Kindly change your password when you login first time

                Thanks 
                For choosing
                XYZ Bank
                '''
                msg=gmail.Message(to=uemail,subject='Account Opened',text=umsg)
                gmail_con.send(msg)
                messagebox.showinfo('open account','Account created and kindly check your email for account/password')
            except:
                messagebox.showerror('open account','Account created but email not sent')

        def RESET():
            user_name_entry.delete(0,'end')
            user_email_entry.delete(0,'end')
            user_mob_entry.delete(0,'end')
            user_adhar_entry.delete(0,'end')
            user_name_entry.focus()

        user_name_label=Label(current_child_frm,text='Name',font=('arial',15,'bold'),bg='red4',fg='floralwhite')
        user_name_label.place(relx=.1,rely=.1)
        user_name_entry=Entry(current_child_frm,font=('arial',15,'bold'),bd=3,relief='groove')
        user_name_entry.place(relx=.1,rely=.2)
        user_name_entry.focus()

        user_email_label=Label(current_child_frm,text='Email',font=('arial',15,'bold'),bg='red4',fg='floralwhite')
        user_email_label.place(relx=.6,rely=.1)
        user_email_entry=Entry(current_child_frm,font=('arial',15,'bold'),bd=3,relief='groove')
        user_email_entry.place(relx=.6,rely=.2)

        user_mob_label=Label(current_child_frm,text='Mobile',font=('arial',15,'bold'),bg='red4',fg='floralwhite')
        user_mob_label.place(relx=.1,rely=.3)
        user_mob_entry=Entry(current_child_frm,font=('arial',15,'bold'),bd=3,relief='groove')
        user_mob_entry.place(relx=.1,rely=.4)

        user_adhar_label=Label(current_child_frm,text='Aadhaar',font=('arial',15,'bold'),bg='red4',fg='floralwhite')
        user_adhar_label.place(relx=.6,rely=.3)
        user_adhar_entry=Entry(current_child_frm,font=('arial',15,'bold'),bd=3,relief='groove')
        user_adhar_entry.place(relx=.6,rely=.4)

        open_acnt_btn=Button(current_child_frm,command=open_acn,text='Open',relief='raised',font=('arial',15,'bold'),bd=5,bg='floralwhite',fg='red4',width=10,cursor='hand2')
        open_acnt_btn.place(relx=.3,rely=.65)

        reset_acnt_btn=Button(current_child_frm,command=RESET,text='Reset',relief='raised',font=('arial',15,'bold'),bd=5,bg='floralwhite',fg='red4',width=10,cursor='hand2')
        reset_acnt_btn.place(relx=.5,rely=.65)


    def View_click():
        current_child_frm=Frame(admn_frm,highlightbackground='black',highlightthickness=2)
        current_child_frm.configure(bg='red4')
        current_child_frm.place(relx=.2,rely=.11,relwidth=.6,relheight=.8)

        inner_view_frm_title_label=Label(current_child_frm,text='View-Users',relief='flat',font=('arial',10,'bold'),bg='red4',fg='floralwhite')
        inner_view_frm_title_label.pack()


        # Update the table with filtered data."""
        def update_table(filtered_data):
            model = TableModel()                # Create a new model instance
            model.importDict(filtered_data)     # Import the filtered data
            table.model = model                 # Assign new model to table
            table.redraw()                      # Refresh the table UI
        
        
        # Search function to filter data based on Account Number input."""
        def search_data():
            search_id = search_var.get().strip()    # Get entered Account Number
            
            if not search_id:                       # If empty, show full data   
               View_ALL()      
            else:
                # Fetch fresh data to prevent errors
                all_data = fetch_data()
                # Filter data based on Acn No
                filtered_data = {k: v for k, v in all_data.items() if str(v["Acn No"]) == search_id}
                
                if not filtered_data:               # If no match found, show error message
                    messagebox.showerror("Error", "Account Number not found!")
                else:
                    update_table(filtered_data)     # Update table with filtered results

  
        #Fetch data dynamically from the database."""
        def fetch_data():
            data = {}
            con_obj = sqlite3.connect(database='BankDetails.sqlite')
            cur_obj = con_obj.cursor()
            cur_obj.execute("SELECT * FROM users")

            i = 1
            for tup in cur_obj:
                data[f"{i}"] = {
                    "Acn No": tup[0], "Name": tup[2], "Balance": tup[5],
                    "Open Date": tup[7], "Aadhar": tup[6], "Email": tup[4], "Mobile": tup[3]
                }
                i += 1

            con_obj.close()
            return data  # Return the fetched data dictionary
        def View_ALL():
            update_table(fetch_data())

        # UI Setup
        frame = Frame(current_child_frm)
        frame.place(relx=.05, rely=.17, relwidth=.9)

        # Search input field
        search_var = StringVar()

        search_label = Label(current_child_frm,relief='flat',bg='red4',fg='floralwhite', text="Enter Acn No:", font=('Arial', 13, 'bold'))
        search_label.place(relx=0.22, rely=0.1)

        search_entry = Entry(current_child_frm, textvariable=search_var, font=('Arial', 12),relief='groove')
        search_entry.place(relx=0.43, rely=0.1, relwidth=0.3)

        search_button = Button(current_child_frm, text="Search", command=search_data,relief='raised',font=('arial',12,'bold'),bd=5,bg='red4',fg='floralwhite',cursor='hand2')
        search_button.place(relx=0.74, rely=0.07)

        ViewAll_button = Button(current_child_frm, text="View All",command=View_ALL,relief='raised',font=('arial',12,'bold'),bd=5,bg='red4',fg='floralwhite',cursor='hand2')
        ViewAll_button.place(relx=0.85, rely=0.07)

        # Table setup
        data = fetch_data()  # Get initial data from the database
        model = TableModel()
        model.importDict(data)

        table = TableCanvas(frame, model=model, editable=False)
        table.show()

        # frame = Frame(current_child_frm)
        # frame.place(relx=.05, rely=.1,relwidth=.9)

        # data={}
        # i=1
        # con_obj=sqlite3.connect(database='BankDetails.sqlite')
        # cur_obj=con_obj.cursor()
        # cur_obj.execute("select * from users")

        # for tup in cur_obj:
        #         data[f"{i}"] = {"Acn No": tup[0], "Name":tup[2], "Balance": tup[5], "Open Date": tup[7], "Aadhar":tup[6], "Email":tup[4], "Mobile":tup[3]}
        #         i+=1
        # con_obj.close()

        # model = TableModel()
        # model.importDict(data)

        # table = TableCanvas(frame, model=model, editable=False)
        # table.show()


    def Delete_click():
        current_child_frm=Frame(admn_frm,highlightbackground='black',highlightthickness=2)
        current_child_frm.configure(bg='red4')
        current_child_frm.place(relx=.2,rely=.11,relwidth=.6,relheight=.8)

        inner_delete_frm_title_label=Label(current_child_frm,text='Delete-Users',relief='flat',font=('arial',10,'bold'),bg='red4',fg='floralwhite')
        inner_delete_frm_title_label.pack()

        def delete_DB():
            uacn=delete_acnt_entry.get().strip()

            if not uacn:  # Check if input is empty
                messagebox.showwarning("Warning", "Please enter an Account Number!")
                return
            try:
                con_obj=sqlite3.connect(database='BankDetails.sqlite')
                cur_obj=con_obj.cursor()
                cur_obj.execute('delete from users where users_acno=?',(uacn,))
                cur_obj.execute('delete from txn where txn_acno=?',(uacn,))
                con_obj.commit()
                con_obj.close()
                messagebox.showinfo('delete',f'User with account number {uacn} is deleted.')
            except:
                messagebox.showwarning("Delete","Account No not found")

        def RESET():
            delete_acnt_entry.delete(0,'end')
            delete_acnt_entry.focus()
        
        delete_acnt_label=Label(current_child_frm,text='Account.No.',font=('arial',15,'bold'),bg='red4',fg='floralwhite')
        delete_acnt_label.place(relx=.41,rely=.2)
        delete_acnt_entry=Entry(current_child_frm,font=('arial',15,'bold'),bd=5,relief='groove')
        delete_acnt_entry.place(relx=.33,rely=.3)
        delete_acnt_entry.focus()

        delete_acnt_btn=Button(current_child_frm,command=delete_DB,text='Delete',relief='raised',font=('arial',15,'bold'),bd=5,bg='floralwhite',fg='red4',width=10,cursor='hand2')
        delete_acnt_btn.place(relx=.3,rely=.65)

        rdelete_view_btn=Button(current_child_frm,command=RESET,text='Reset',relief='raised',font=('arial',15,'bold'),bd=5,bg='floralwhite',fg='red4',width=10,cursor='hand2')
        rdelete_view_btn.place(relx=.5,rely=.65)


    admn_label=Label(admn_frm,text='Welcome,Admin',font=('arial',10,'bold'),bg='floralwhite',fg='red4')
    admn_label.place(relx=0,rely=0)
    #logout button                                                               ========================================================                                                           
    logout_btn=Button(admn_frm,text='Logout',relief='raised',width=10,font=('arial',15,'bold'),bd=5,bg='red4',fg='floralwhite',command=AdminLgout_click,cursor='hand2')
    logout_btn.pack(side='top',anchor='e')
    #Admin nested frame inside admn_frm(admin_win)  for buttons                =======================================================================
    admn_btn_frm=Frame(admn_frm,highlightbackground='floralwhite')
    admn_btn_frm.configure(bg='floralwhite')
    admn_btn_frm.place(relx=0,rely=.3,relwidth=.15,relheight=.34)
    #buttons inside admn_btn_frm                                        =======================================================================
    create_btn=Button(admn_btn_frm,text='Create-User',relief='raised',font=('arial',15,'bold'),bd=7,fg='floralwhite',bg='red4',width=14,command=create_click,cursor='hand2')
    create_btn.grid(row=0,column=0,pady=2)
    View_btn=Button(admn_btn_frm,text='View-User',relief='raised',font=('arial',15,'bold'),bd=7,fg='floralwhite',bg='red4',width=14,command=View_click,cursor='hand2')
    View_btn.grid(row=1,column=0,pady=2)
    delete_btn=Button(admn_btn_frm,text='Delete-User',relief='raised',font=('arial',15,'bold'),bd=7,fg='floralwhite',bg='red',width=14,command=Delete_click,cursor='hand2')
    delete_btn.grid(row=2,column=0,pady=2)


#forgot password screen inside frm(main_screen) window ---> nested function                   =======================================================================
def forgot_pass_win():
    frgt_frm=Frame(win,highlightbackground='black',highlightthickness=2)
    frgt_frm.configure(bg='floralwhite')
    frgt_frm.place(relx=0,rely=.14,relwidth=1,relheight=.74)

    def Back_click():
        frgt_frm.destroy()
        main_screen()

    def get_password():
        uacn=frgt_acnt_entry.get().strip()
        uemail=frgt_email_entry.get().strip()
        umob=frgt_mob_entry.get().strip()

        if len(uacn) == 0 or len(umob) ==0 or len(uemail) == 0:
                messagebox.showerror('Error','Empty fields are not allowed.')
                return

        if not re.fullmatch('[0-9 ]+',uacn):
                messagebox.showerror('Error','Kindly enter valid Account number!')
                return

        if not re.fullmatch('[6-9][0-9]{9}',umob):
                messagebox.showerror('Error','Invalid Mobile Number')
                return
            
        if not re.fullmatch('[a-z0-9_.]+@[a-z]+[.][a-z]+',uemail):
            messagebox.showerror('Error','Invalid Email Format')
            return

        con_obj=sqlite3.connect(database='BankDetails.sqlite')
        cur_obj=con_obj.cursor()
        cur_obj.execute('select users_name,users_pass from users where users_acno=? and users_email=? and users_mob=?',(uacn,uemail,umob))
        tup=cur_obj.fetchone()
        con_obj.close()

        if tup==None:
            messagebox.showerror('Forgot pass',"Invalid Details")
        else:
            try:
                gmail_con=gmail.GMail('mannuarya2002@gmail.com','zrth fyvp pywf lkee')
                umsg=f'''Hello,{tup[0]}
                Welcome to our XYZ Bank
                Your Pass is : {tup[1]}

                Thanks 
                For choosing
                XYZ Bank
                '''
                msg=gmail.Message(to=uemail,subject='Your password has been recoverd',text=umsg)
                gmail_con.send(msg)
                messagebox.showinfo('Email sent','Your password is sent to your email address')
            except Exception as e:
                messagebox.showerror('Forgot pass','some error occurred email not sent')
                print(e)

    def RESET():
        frgt_acnt_entry.delete(0,'end')
        frgt_email_entry.delete(0,'end')
        frgt_mob_entry.delete(0,'end')
        frgt_acnt_entry.focus()

    def toggle_email():
        if show_email.get():
            frgt_email_entry.config(show='')
        else:
            frgt_email_entry.config(show='*')

    def toggle_mobile():
        if show_mob.get():
            frgt_mob_entry.config(show='')
        else:
            frgt_mob_entry.config(show='*')

    Back_btn=Button(frgt_frm,text='Back',relief='raised',font=('arial',15,'bold'),bd=5,bg='red4',fg='floralwhite',command=Back_click,cursor='hand2')
    Back_btn.place(relx=0,rely=0)

    

    frgt_acnt_label=Label(frgt_frm,text='Accnt.no.',font=('arial',20,'bold'),bg='floralwhite',fg='red4')
    frgt_acnt_label.place(relx=.3,rely=.2)
    frgt_acnt_entry=Entry(frgt_frm,font=('arial',20,'bold'),bd=5,relief='groove')
    frgt_acnt_entry.place(relx=.45,rely=.2)
    frgt_acnt_entry.focus()


    frgt_email_label=Label(frgt_frm,text='Email',font=('arial',20,'bold'),bg='floralwhite',fg='red4')
    frgt_email_label.place(relx=.3,rely=.3)
    frgt_email_entry=Entry(frgt_frm,font=('arial',20,'bold'),bd=5,show='*',relief='groove')
    frgt_email_entry.place(relx=.45,rely=.3)
    # Define show_var BEFORE using it
    show_email = BooleanVar(value=False)
    # Checkbox to show or hide the password
    show_check = Checkbutton(frgt_frm, text='Show Email', font=('arial', 10,'bold'),fg='darkgoldenrod2',bg='floralwhite',variable=show_email, onvalue=True, offvalue=False,command=toggle_email,cursor='hand2')
    show_check.place(relx=.45, rely=.38)

    frgt_mob_label=Label(frgt_frm,text='Mob.',font=('arial',20,'bold'),bg='floralwhite',fg='red4')
    frgt_mob_label.place(relx=.3,rely=.43)
    frgt_mob_entry=Entry(frgt_frm,font=('arial',20,'bold'),bd=5,show='*',relief='groove')
    frgt_mob_entry.place(relx=.45,rely=.43)
    # Define show_var BEFORE using it
    show_mob = BooleanVar(value=False)
    # Checkbox to show or hide the password
    show_check = Checkbutton(frgt_frm, text='Show Mobile', font=('arial', 10,'bold'),fg='darkgoldenrod2',bg='floralwhite',variable=show_mob, onvalue=True, offvalue=False,command=toggle_mobile,cursor='hand2')
    show_check.place(relx=.45, rely=.51)

    submit_btn=Button(frgt_frm,command=get_password,text='submit',relief='raised',font=('arial',14,'bold'),bd=5,bg='red4',fg='floralwhite',cursor='hand2')
    submit_btn.place(relx=.45,rely=.56)

    reset_btn=Button(frgt_frm,command=RESET,text='Reset',relief='raised',font=('arial',14,'bold'),bd=5,bg='red4',fg='floralwhite',cursor='hand2')
    reset_btn.place(relx=.63,rely=.56)


def User_win():
    user_frm=Frame(win,highlightbackground='black',highlightthickness=2)
    user_frm.configure(bg='floralwhite')
    user_frm.place(relx=0,rely=.14,relwidth=1,relheight=.74)


    if os.path.exists(f'{uacn}.png'):
        profileImg=ImageTk.PhotoImage(Image.open(f'{uacn}.png').resize((150, 150)),master=win)
    else:
        profileImg=ImageTk.PhotoImage(Image.open('default.png').resize((150, 150)),master=win)
    pic_lbl=Label(user_frm,image=profileImg)
    pic_lbl.image=profileImg
    pic_lbl.place(relx=.010,rely=.05)

    def update_Profile_img():
        path=filedialog.askopenfilename()
        shutil.copy(path,f'{uacn}.png')


        profileImg=ImageTk.PhotoImage(Image.open(path).resize((150, 150)),master=win)
        pic_lbl=Label(user_frm,image=profileImg)
        pic_lbl.image=profileImg
        pic_lbl.place(relx=.010,rely=.05)


    uplaod_prfl=Button(user_frm,command=update_Profile_img,text='Upload Profile',font=('arial',10),bd=5,bg='floralwhite',fg='red4',cursor='hand2')
    uplaod_prfl.place(relx=.010,rely=.36)


    #currently active child frame locator variable
    current_child_frm = None

    #function to destroy current child frame
    def destroy_current_child_frm():
        nonlocal current_child_frm
        if current_child_frm:
            current_child_frm.destroy()
            current_child_frm = None
    # logout function inside Admin_win() function                           =======================================================================
    def User_logout_click():
        resp=messagebox.askyesno('logout','Do you want to logout?\nKindly confirm!')
        if resp :       #default is always True this is why we don't use if resp ==True:
            user_frm.destroy()
            main_screen()

    def check_bal():
        destroy_current_child_frm()
        nonlocal current_child_frm
        current_child_frm=Frame(user_frm,highlightbackground='black',highlightthickness=2)
        current_child_frm.configure(bg='red4')
        current_child_frm.place(relx=.2,rely=.11,relwidth=.6,relheight=.8)

        check_Bal_title_label=Label(current_child_frm,text='Check-Balance',font=('arial',10,'bold'),bg='red4',fg='floralwhite')
        check_Bal_title_label.pack()

        #chk_dtl_frm nested frame inside current_child_frm(user_win)  for labels               =======================================================================
        chk_dtl_frm=Frame(current_child_frm,highlightbackground='floralwhite')
        chk_dtl_frm.configure(bg='red4')
        chk_dtl_frm.place(relx=.25,rely=.2,relwidth=.45,relheight=.5)


        con_obj=sqlite3.connect(database='BankDetails.sqlite')
        cur_obj=con_obj.cursor()
        cur_obj.execute('select users_balance,users_opendate,users_adhar from users where users_Acno=?',(uacn,))
        tup=cur_obj.fetchone()
        con_obj.close()




        check_Bal_acnt_label=Label(chk_dtl_frm,text='Account.No.',font=('arial',15,'bold'),bg='red4',fg='floralwhite')
        check_Bal_acnt_label.grid(row=0,column=0)
        check_Bal_acnt_label=Label(chk_dtl_frm,text=uacn,font=('arial',15,'bold'),bd=5,bg='red4',fg='darkgoldenrod2')
        check_Bal_acnt_label.grid(row=0,column=1)

        check_Bal_label=Label(chk_dtl_frm,text='Balance',font=('arial',15,'bold'),bg='red4',fg='floralwhite')
        check_Bal_label.grid(row=1,column=0)
        check_Bal_label=Label(chk_dtl_frm,text=f'₹ {tup[0]}',font=('arial',15,'bold'),bd=5,bg='red4',fg='darkgoldenrod2')
        check_Bal_label.grid(row=1,column=1)

        check_open_date_label=Label(chk_dtl_frm,text='Open Date',font=('arial',15,'bold'),bg='red4',fg='floralwhite')
        check_open_date_label.grid(row=3,column=0)
        check_open_date_label=Label(chk_dtl_frm,text=f'{tup[1]}',font=('arial',15,'bold'),bd=5,bg='red4',fg='darkgoldenrod2')
        check_open_date_label.grid(row=3,column=1)

        check_ifsc_label=Label(chk_dtl_frm,text='Aadhar',font=('arial',15,'bold'),bg='red4',fg='floralwhite')
        check_ifsc_label.grid(row=4,column=0)
        check_ifsc_label=Label(chk_dtl_frm,text=f'{tup[2]}',font=('arial',15,'bold'),bd=5,bg='red4',fg='darkgoldenrod2')
        check_ifsc_label.grid(row=4,column=1)

        # check_Bal_btn=Button(chk_dtl_frm,text='View',relief='raised',font=('arial',15,'bold'),bd=5,bg='floralwhite',fg='red4',width=10,cursor='hand2')
        # check_Bal_btn.grid(row=5,column=1,pady=10)
    
    def update_details():
        destroy_current_child_frm()
        nonlocal current_child_frm
        current_child_frm=Frame(user_frm,highlightbackground='black',highlightthickness=2)
        current_child_frm.configure(bg='red4')
        current_child_frm.place(relx=.2,rely=.11,relwidth=.6,relheight=.8)

        updt_dtl_title_label=Label(current_child_frm,text='Update-Details',relief='flat',font=('arial',10,'bold'),bg='red4',fg='floralwhite')
        updt_dtl_title_label.pack()

        def updt_dtail_btn():
            uname=updt_name_entry.get().strip()
            uemail=updt_email_entry.get().strip()
            umob=updt_mob_entry.get().strip()
            upass=updt_pass_entry.get().strip()

            if len(uname) == 0 or len(umob) ==0 or len(uemail) == 0 or len(upass) == 0:
                messagebox.showerror('Error','Empty fields are not allowed.')
                return

            if not re.fullmatch('[A-Za-z ]+',uname):
                messagebox.showerror('Error','Kindly enter valid name!')
                return
            if not re.fullmatch('[a-z0-9_.]+@[a-z]+[.][a-z]+',uemail):
                messagebox.showerror('Error','Invalid Email Format')
                return
            if not re.fullmatch('[6-9][0-9]{9}',umob):
                messagebox.showerror('Error','Kindly enter valid number!')
                return
            if not re.fullmatch('[A-Za-z0-9@_]+',upass):
                messagebox.showerror('Error','Kindly enter valid pass!')
                return



            con_obj=sqlite3.connect(database='BankDetails.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('update users set users_name=?,users_pass=?,users_email=?,users_mob=? where users_acno=?',(uname,upass,uemail,umob,uacn))
            con_obj.commit()
            con_obj.close()
            messagebox.showinfo("Update","Details Updated")

            con_obj=sqlite3.connect(database='BankDetails.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select * from users where users_acno=?',(uacn,))
            updt_tup=cur_obj.fetchone()
            con_obj.close()
            try:
                gmail_con=gmail.GMail('mannuarya2002@gmail.com','zrth fyvp pywf lkee')
                umsg=f'''Hello,{updt_tup[2]}
                Your Details are updated successfully.
                Your Account is : {updt_tup[0]}
                Your Email is : {updt_tup[4]}
                Your Mobile is : {updt_tup[3]}
                Your Pass is : {updt_tup[1]}

                Thanks 
                For choosing
                XYZ Bank
                '''
                msg=gmail.Message(to=uemail,subject='Account Updated..',text=umsg)
                gmail_con.send(msg)
                messagebox.showinfo('Updation Email','An updation email has sent to your email address.')
            except:
                messagebox.showerror('Updated','Error in sending email')



        con_obj=sqlite3.connect(database='BankDetails.sqlite')
        cur_obj=con_obj.cursor()
        cur_obj.execute('select * from users where users_acno=?',(uacn,))
        tup=cur_obj.fetchone()
        con_obj.close()

        def RESET():
            updt_name_entry.delete(0,'end')
            updt_email_entry.delete(0,'end')
            updt_mob_entry.delete(0,'end')
            updt_pass_entry.delete(0,'end')
            updt_name_entry.focus()



        updt_name_label=Label(current_child_frm,text='Name',font=('arial',15,'bold'),bg='red4',fg='floralwhite')
        updt_name_label.place(relx=.1,rely=.1)
        updt_name_entry=Entry(current_child_frm,font=('arial',15,'bold'),bd=3,relief='groove')
        updt_name_entry.place(relx=.1,rely=.2)
        updt_name_entry.insert(0,tup[2])
        updt_name_entry.focus()

        updt_email_label=Label(current_child_frm,text='Email',font=('arial',15,'bold'),bg='red4',fg='floralwhite')
        updt_email_label.place(relx=.6,rely=.1)
        updt_email_entry=Entry(current_child_frm,font=('arial',15,'bold'),bd=3,relief='groove')
        updt_email_entry.place(relx=.6,rely=.2)
        updt_email_entry.insert(0,tup[4])

        updt_mob_label=Label(current_child_frm,text='Mobile',font=('arial',15,'bold'),bg='red4',fg='floralwhite')
        updt_mob_label.place(relx=.1,rely=.3)
        updt_mob_entry=Entry(current_child_frm,font=('arial',15,'bold'),bd=3,relief='groove')
        updt_mob_entry.place(relx=.1,rely=.4)
        updt_mob_entry.insert(0,tup[3])

        updt_pass_label=Label(current_child_frm,text='Pass',font=('arial',15,'bold'),bg='red4',fg='floralwhite')
        updt_pass_label.place(relx=.6,rely=.3)
        updt_pass_entry=Entry(current_child_frm,font=('arial',15,'bold'),bd=3,relief='groove')
        updt_pass_entry.place(relx=.6,rely=.4)
        updt_pass_entry.insert(0,tup[1])

        updt_dtls_btn=Button(current_child_frm,command=updt_dtail_btn,text='Update',relief='raised',font=('arial',15,'bold'),bd=5,bg='floralwhite',fg='red4',width=10,cursor='hand2')
        updt_dtls_btn.place(relx=.25,rely=.65)

        updt_reseDdtls_btn=Button(current_child_frm,command=RESET,text='Reset',relief='raised',font=('arial',15,'bold'),bd=5,bg='floralwhite',fg='red4',width=10,cursor='hand2')
        updt_reseDdtls_btn.place(relx=.58,rely=.65)

    def Deposite():
        destroy_current_child_frm()
        nonlocal current_child_frm
        current_child_frm=Frame(user_frm,highlightbackground='black',highlightthickness=2)
        current_child_frm.configure(bg='red4')
        current_child_frm.place(relx=.2,rely=.11,relwidth=.6,relheight=.8)

        depst_title_label=Label(current_child_frm,text='Deposite',relief='flat',font=('arial',10,'bold'),bg='red4',fg='floralwhite')
        depst_title_label.pack()

        def deposite_bal():
            entry_str=depst_entry.get().strip()

            if not entry_str:
                messagebox.showerror('Error','Entries cannot be empty.')
                return
            
            if not re.fullmatch('[0-9]+',entry_str):
                messagebox.showerror('Error','Kindly enter valid number!')
                return    
            
            uamt=float(entry_str)

        # uamt=float(depst_entry.get().strip())
       


            con_obj=sqlite3.connect(database='BankDetails.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select users_balance from users where users_acno=?',(uacn,))
            ubal=cur_obj.fetchone()[0]
            con_obj.close()

            con_obj=sqlite3.connect(database='BankDetails.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('update users set users_balance=users_balance+? where users_acno=?',(uamt,uacn))
            con_obj.commit()
            con_obj.close()

    
            con_obj=sqlite3.connect(database='BankDetails.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('insert into txn(txn_acno,txn_type,txn_date,txn_amt,txn_update_bal)values(?,?,?,?,?)',(uacn,'Credit(+)',f'{current_date}/{current_time}',uamt,ubal+uamt))
            con_obj.commit()
            con_obj.close() 
            messagebox.showinfo('Deposite',f'Amount {uamt} Deposited and updated balance {ubal+uamt} Successfully')

 

        depst_label=Label(current_child_frm,text='Amount',font=('arial',15,'bold'),bg='red4',fg='floralwhite')
        depst_label.place(relx=.26,rely=.35)
        depst_entry=Entry(current_child_frm,font=('arial',15,'bold'),bd=5,relief='groove')
        depst_entry.place(relx=.43,rely=.35)
        depst_entry.focus()

        depst_btn=Button(current_child_frm,command=deposite_bal,text='Deposite',relief='raised',font=('arial',15,'bold'),bd=5,bg='floralwhite',fg='red4',width=10,cursor='hand2')
        depst_btn.place(relx=.56,rely=.56)

    def withdraw():
        destroy_current_child_frm()
        nonlocal current_child_frm
        current_child_frm=Frame(user_frm,highlightbackground='black',highlightthickness=2)
        current_child_frm.configure(bg='red4')
        current_child_frm.place(relx=.2,rely=.11,relwidth=.6,relheight=.8)

        withdraw_title_label=Label(current_child_frm,text='Withdraw',font=('arial',10,'bold'),bg='red4',fg='floralwhite')
        withdraw_title_label.pack()

        def withdraw_bal():
            entry_str=wthdrw_entry.get().strip()

            if not entry_str:
                messagebox.showerror('Error','Entries cannot be empty.')
                return
            
            if not re.fullmatch('[0-9]+',entry_str):
                messagebox.showerror('Error','Kindly enter valid number!')
                return    
            
            uamt=float(entry_str)

            con_obj=sqlite3.connect(database='BankDetails.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select users_balance from users where users_acno=?',(uacn,))
            ubal=cur_obj.fetchone()[0]
            con_obj.close()

            if uamt<=ubal:
                con_obj=sqlite3.connect(database='BankDetails.sqlite')
                cur_obj=con_obj.cursor()
                cur_obj.execute('update users set users_balance=users_balance-? where users_acno=?',(uamt,uacn))
                con_obj.commit()
                con_obj.close()

                
                con_obj=sqlite3.connect(database='BankDetails.sqlite')
                cur_obj=con_obj.cursor()
                cur_obj.execute('insert into txn(txn_acno,txn_type,txn_date,txn_amt,txn_update_bal)values(?,?,?,?,?)',(uacn,'Debit(-)',f'{current_date}{current_time}',uamt,ubal-uamt))
                con_obj.commit()
                con_obj.close() 
                messagebox.showinfo('Withdraw',f'Amount {uamt} Withdrawn and updated balance {ubal-uamt} Successfully')
            else:
                messagebox.showerror('Withdraw',f'Insufficient Balance\nAvailable Balance : {ubal}')


        wthdrw_label=Label(current_child_frm,text='Amount',font=('arial',15,'bold'),bg='red4',fg='floralwhite')
        wthdrw_label.place(relx=.26,rely=.35)
        wthdrw_entry=Entry(current_child_frm,font=('arial',15,'bold'),bd=5,relief='groove')
        wthdrw_entry.place(relx=.43,rely=.35)
        wthdrw_entry.focus()

        wthdrw_btn=Button(current_child_frm,command=withdraw_bal,text='Withdraw',relief='raised',font=('arial',15,'bold'),bd=5,bg='floralwhite',fg='red4',width=10,cursor='hand2')
        wthdrw_btn.place(relx=.56,rely=.56)


    def transfer():
        destroy_current_child_frm()
        nonlocal current_child_frm
        current_child_frm=Frame(user_frm,highlightbackground='black',highlightthickness=2)
        current_child_frm.configure(bg='red4')
        current_child_frm.place(relx=.2,rely=.11,relwidth=.6,relheight=.8)

        trnsfr_title_label=Label(current_child_frm,text='Transfer-Amount',relief='flat',font=('arial',10,'bold'),bg='red4',fg='floralwhite')
        trnsfr_title_label.pack()

        def trnsfr_bal():
            entry_amnt_str=trnsfer_amnt_entry.get().strip()
            entry_toacn=trnsfer_to_entry.get().strip()

            if not entry_amnt_str:
                messagebox.showerror('Error','Entries cannot be empty.')
                return
            if not entry_toacn:
                messagebox.showerror('Error','Entries cannot be empty.')
                return
            if not re.fullmatch('[0-9]+',entry_amnt_str):
                messagebox.showerror('Error','Kindly enter valid number!')
                return    
            if not re.fullmatch('[0-9]+',entry_toacn):
                messagebox.showerror('Error','Kindly enter valid number!')
                return  
            
            uamt=float(entry_amnt_str)
            toacn=int(entry_toacn)

            con_obj=sqlite3.connect(database='BankDetails.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select users_balance,users_email from users where users_acno=?',(uacn,))
            tup=cur_obj.fetchone()
            ubal=tup[0]
            uemail=tup[1]
            con_obj.close()

            if uamt<=ubal:

                con_obj=sqlite3.connect(database='BankDetails.sqlite')
                cur_obj=con_obj.cursor()
                cur_obj.execute('select  * from users where users_acno=?',(toacn,))
                tup=cur_obj.fetchone()
                con_obj.close()

                if tup == None:
                    messagebox.showerror("Transfer","Invalid Account Number\nTo Account not found.")
                else:
                    otp=random.randint(1000,9999)
                    try:
                        gmail_con=gmail.GMail('mannuarya2002@gmail.com','zrth fyvp pywf lkee')
                        umsg=f'''Hello,{uname}
                        OTP verification.
                        Your OTP is : {otp}

                        kindly verify this otp to complete your transaction.

                        Thanks 
                        For choosing
                        XYZ Bank
                        '''
                        msg=gmail.Message(to=uemail,subject='OTP verification for your transfer',text=umsg)
                        gmail_con.send(msg)
                        messagebox.showinfo('Transfer','We have send OTP to your registered email address.')

                        UOTP=simpledialog.askinteger('OTP','Enter OTP')
                        if otp==UOTP:
                            con_obj=sqlite3.connect(database='BankDetails.sqlite')
                            cur_obj=con_obj.cursor()
                            cur_obj.execute('update users set users_balance=users_balance-? where users_acno=?',(uamt,uacn))
                            cur_obj.execute('update users set users_balance=users_balance+? where users_acno=?',(uamt,toacn))

                            con_obj.commit()
                            con_obj.close()

                            tobal=tup[5]

                            con_obj=sqlite3.connect(database='BankDetails.sqlite')
                            cur_obj=con_obj.cursor()
                            cur_obj.execute('insert into txn(txn_acno,txn_type,txn_date,txn_amt,txn_update_bal)values(?,?,?,?,?)',(uacn,'Debit(-)',f'{current_date}{current_time}',uamt,ubal-uamt))
                            cur_obj.execute('insert into txn(txn_acno,txn_type,txn_date,txn_amt,txn_update_bal)values(?,?,?,?,?)',(toacn,'Credit(+)',f'{current_date}{current_time}',uamt,tobal+uamt))

                            con_obj.commit()
                            con_obj.close() 
                            messagebox.showinfo('transfer',f'Amount {uamt} transfered and updated balance {ubal-uamt} Successfully')
                        else:
                            messagebox.showerror("OTP","Invalid OTP")
                    except:
                        messagebox.showerror('Transfer','Error in sending email')
            else:
                messagebox.showerror('transfer',f'Insufficient Balance\nAvailable Balance : {ubal}')

        trnsfer_to_label=Label(current_child_frm,text='To Acnt.',font=('arial',15,'bold'),bg='red4',fg='floralwhite')
        trnsfer_to_label.place(relx=.26,rely=.25)
        trnsfer_to_entry=Entry(current_child_frm,font=('arial',15,'bold'),bd=5,relief='groove')
        trnsfer_to_entry.place(relx=.43,rely=.25)
        trnsfer_to_entry.focus()

        trnsfer_amnt_label=Label(current_child_frm,text='Amount',font=('arial',15,'bold'),bg='red4',fg='floralwhite')
        trnsfer_amnt_label.place(relx=.26,rely=.45)
        trnsfer_amnt_entry=Entry(current_child_frm,font=('arial',15,'bold'),bd=5,relief='groove')
        trnsfer_amnt_entry.place(relx=.43,rely=.45)

        depst_btn=Button(current_child_frm,command=trnsfr_bal,text='Transfer',relief='raised',font=('arial',15,'bold'),bd=5,bg='floralwhite',fg='red4',width=10,cursor='hand2')
        depst_btn.place(relx=.56,rely=.65)


    def transection():
        destroy_current_child_frm()
        nonlocal current_child_frm
        current_child_frm=Frame(user_frm,highlightbackground='black',highlightthickness=2)
        current_child_frm.configure(bg='red4')
        current_child_frm.place(relx=.2,rely=.11,relwidth=.6,relheight=.8)

        frame = Frame(current_child_frm)
        frame.place(relx=.10, rely=.1,relwidth=.8)

        data={}
        i=1
        con_obj=sqlite3.connect(database='BankDetails.sqlite')
        cur_obj=con_obj.cursor()
        cur_obj.execute("select * from txn where txn_acno=?",(uacn,))

        for tup in cur_obj:
                data[f"{i}"] = {"Txn ID": tup[1], "Txn Amnt": tup[4], "Txn Date": tup[3], "Txn type":tup[2], "Updtd Bal":tup[5]}
                i+=1
        con_obj.close()

        model = TableModel()
        model.importDict(data)

        table = TableCanvas(frame, model=model, editable=False)
        table.show()

        transection_title_label=Label(current_child_frm,text='Transection-History',font=('arial',10,'bold'),bg='red4',fg='floralwhite')
        transection_title_label.pack()


    #logout button                                                               ========================================================                                                           
    logout_btn=Button(user_frm,text='Logout',relief='raised',width=10,font=('arial',15,'bold'),bd=5,bg='red4',fg='floralwhite',command=User_logout_click,cursor='hand2')
    logout_btn.pack(side='top',anchor='e')

    user_label=Label(user_frm,text=f'Welcome,{uname}',font=('arial',10,'bold'),bg='floralwhite',fg='red4')
    user_label.place(relx=0,rely=0)

    #user left nested frame inside user_frm(user_win)  for buttons                =======================================================================
    user_left_btn_frm=Frame(user_frm,highlightbackground='floralwhite')
    user_left_btn_frm.configure(bg='floralwhite')
    user_left_btn_frm.place(relx=.002,rely=.45,relwidth=.15,relheight=.34)
    #buttons inside user_btn_frm                                        =======================================================================
    check_bal_btn=Button(user_left_btn_frm,text='Check-Balance',relief='raised',font=('arial',15,'bold'),bd=7,fg='floralwhite',bg='red4',width=14,command=check_bal,cursor='hand2')
    check_bal_btn.grid(row=0,column=0)
    updt_dtls_btn=Button(user_left_btn_frm,text='Update-Details',relief='raised',font=('arial',15,'bold'),bd=7,fg='floralwhite',bg='red4',width=14,command=update_details,cursor='hand2')
    updt_dtls_btn.grid(row=1,column=0,pady=2)
    deposite_btn=Button(user_left_btn_frm,text='Deposite',relief='raised',font=('arial',15,'bold'),bd=7,fg='floralwhite',bg='red4',width=14,command=Deposite,cursor='hand2')
    deposite_btn.grid(row=2,column=0,pady=2)

    #user right nested frame inside user_frm(user_win)  for buttons                =======================================================================
    user_right_btn_frm=Frame(user_frm,highlightbackground='floralwhite')
    user_right_btn_frm.configure(bg='floralwhite')
    user_right_btn_frm.place(relx=.85,rely=.45,relwidth=.15,relheight=.35)
    #buttons inside user_btn_frm
    wthdrw_btn=Button(user_right_btn_frm,text='Withdraw',relief='raised',font=('arial',15,'bold'),bd=7,fg='floralwhite',bg='red4',width=14,command=withdraw,cursor='hand2')
    wthdrw_btn.grid(row=1,column=0)
    trnsfr_btn=Button(user_right_btn_frm,text='Transfer',relief='raised',font=('arial',15,'bold'),bd=7,fg='floralwhite',bg='red4',width=14,command=transfer,cursor='hand2')
    trnsfr_btn.grid(row=2,column=0,pady=2)
    trnsaction_btn=Button(user_right_btn_frm,text='Transection',relief='raised',font=('arial',15,'bold'),bd=7,fg='floralwhite',bg='red4',width=14,command=transection,cursor='hand2')
    trnsaction_btn.grid(row=3,column=0,pady=2)


main_screen() 
update_time()
win.mainloop()