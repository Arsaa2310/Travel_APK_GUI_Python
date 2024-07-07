import sqlite3
import bcrypt
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import customtkinter
import tkinter as tk
from datetime import datetime, timedelta
from tkcalendar import DateEntry
from PIL import ImageTk,Image
import heapq
import random

s_root = Tk()
s_root.geometry('800x700+300+50')
s_root.overrideredirect(True)
load_splash_bg = Image.open('./Assets/splash_screen.png')
render_splash = ImageTk.PhotoImage(load_splash_bg)
img_splash = Label(s_root, image=render_splash)
img_splash.image = render_splash
img_splash.place(x=0, y=0)

s_root.after(500, s_root.destroy)
s_root.mainloop()

class App:
    def __init__(self):
        self.app = customtkinter.CTk()
        self.app.title('PAKSU AIR PLANE')
        self.app.geometry('800x700+300+50')
        self.app.iconbitmap('./Assets/root_icon.ico')
        self.app.config(bg='#001220')

        self.font1 = ('Helvetica',25,'bold')
        self.font2 = ('Arial',17,'bold')
        self.font3 = ('Arial',13,'bold')
        self.font4 = ('Arial',13,'bold','underline')

        self.conn = sqlite3.connect('data.db')
        self.cursor = self.conn.cursor()

        # ==================== CREAETE TABLE users =================== #
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                      username TEXT NOT NULL,
                      password TEXT NOT NULL,
                      role TEXT NOT NULL)''')
        
        # ==================== CREAETE TABLE penerbangan =================== #
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS penerbangan (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    maskapai TEXT,
                    asal_keberangkatan TEXT,
                    tujuan_keberangkatan TEXT,
                    tanggal_keberangkatan DATE,
                    jam_keberangkatan TEXT,
                    tujuan_kedatangan TEXT,
                    jumlah_kursi_ekonomi INTEGER,
                    jumlah_kursi_vip INTEGER,
                    jumlah_pemesan INTEGER)''')
        
        self.login()

    def create_signup_frame(self):
        self.frame1 = customtkinter.CTkFrame(self.app,width=800,height=700)
        self.frame1.place(x=0,y=0)

        self.load_add_bg = Image.open('./Assets/bg_signup.png')
        self.render_add_plane = ImageTk.PhotoImage(self.load_add_bg)
        self.img_add_plane = Label(self.frame1, image=self.render_add_plane)
        self.img_add_plane.place(x=0, y=0)

        self.username_entry = customtkinter.CTkEntry(self.frame1,font=self.font2,text_color='#001a2e',bg_color='#fff',border_color='#004780',border_width=3,placeholder_text='Username',placeholder_text_color='#a3a3a3',width=200,height=50)
        self.username_entry.place(x=296.3,y=247.5)

        self.password_entry = customtkinter.CTkEntry(self.frame1,font=self.font2,show='*',text_color='#001a2e',bg_color='#fff',border_color='#004780',border_width=3,placeholder_text='Password',placeholder_text_color='#a3a3a3',width=200,height=50)
        self.password_entry.place(x=296.3,y=375.8)

        self.signup_button = customtkinter.CTkButton(self.frame1,command=self.signup,font=self.font2,text_color='#fff',text='Sign up',fg_color='#00965d',hover_color='#006e44',bg_color='#fff',cursor='hand2',corner_radius=5,width=120)
        self.signup_button.place(x=296.3,y=459.4)

        self.login_label = customtkinter.CTkLabel(self.frame1,font=self.font4,text='Sudah punya akun?',text_color='#000',bg_color='#D2E0DD')
        self.login_label.place(x=296.3,y=500)

        self.login_button = customtkinter.CTkButton(self.frame1,command=self.login,font=self.font4,text_color="#00bf77",text='Login',fg_color='#D2E0DD',hover_color='#001220',cursor='hand2',width=40)
        self.login_button.place(x=435,y=500)

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username != '' and password != '':
            self.cursor.execute('SELECT username FROM users WHERE username=?', [username])
            if self.cursor.fetchone() is not None:
                messagebox.showerror('Error', 'Username already exists.')
            else:
                encoded_password = password.encode('utf-8')
                hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
                self.cursor.execute('INSERT INTO users VALUES (?, ?, ?)', [username,hashed_password, 0])
                self.conn.commit()
                messagebox.showinfo('Success', 'Account has been created.')
        else:
            messagebox.showerror('Error', 'Enter all data.')

    def login(self):
        self.frame2 = customtkinter.CTkFrame(self.app,width=800,height=700)
        self.frame2.place(x=0,y=0)

        self.load_add_bg = Image.open('./Assets/bg_login.png')
        self.render_add_plane = ImageTk.PhotoImage(self.load_add_bg)
        self.img_add_plane = Label(self.frame2, image=self.render_add_plane)
        self.img_add_plane.place(x=0, y=0)

        self.username_entry2 = customtkinter.CTkEntry(self.frame2,font=self.font2,text_color='#000',fg_color='#fff',bg_color='#fff',border_color='#004780',border_width=3,placeholder_text='Username',placeholder_text_color='#a3a3a3',width=200,height=50)
        self.username_entry2.place(x=296.3,y=247.5)

        self.password_entry2 = customtkinter.CTkEntry(self.frame2,font=self.font2,show='*',text_color='#000',fg_color='#fff',bg_color='#fff',border_color='#004780',border_width=3,placeholder_text='Password',placeholder_text_color='#a3a3a3',width=200,height=50)
        self.password_entry2.place(x=296.3,y=375.8)

        self.login_button2 = customtkinter.CTkButton(self.frame2,command=self.login_account,font=self.font2,text_color='#fff',text='Login',fg_color='#00965d',hover_color='#006e44',bg_color='#fff',cursor='hand2',corner_radius=5,width=120)
        self.login_button2.place(x=296.3,y=459.4)

        self.login_label = customtkinter.CTkLabel(self.frame2,font=self.font4,text='Belum punya akun?',text_color='#000',bg_color='#D2E0DD')
        self.login_label.place(x=296.3,y=500)

        self.signup_button = customtkinter.CTkButton(self.frame2,command=self.create_signup_frame,font=self.font4,text_color="#00bf77",text='Sign Up',fg_color='#D2E0DD',hover_color='#001220',cursor='hand2',width=40)
        self.signup_button.place(x=435,y=500)

    def login_account(self):
        username = self.username_entry2.get()
        password = self.password_entry2.get()
        global role
        check_role = self.cursor.execute('SELECT role FROM users WHERE username = ?', [username])
        checked = self.cursor.fetchone()
        role = checked[0]
        if username != '' and password != '':
            self.cursor.execute('SELECT password FROM users WHERE username=?', [username])
            result = self.cursor.fetchone()
            if result:
                if bcrypt.checkpw(password.encode('utf-8'), result[0]):
                    if role == '0':
                        self.dashboard_users()
                    else:
                        self.dashboard_admins()
                else:
                    messagebox.showerror('Err','Invalid password')
            else:
                messagebox.showerror('Err', 'Invalid username')
        else:
            messagebox.showerror('Err', 'Input username password')

    def dashboard_admins(self):
        frame3 = customtkinter.CTkFrame(self.app, bg_color='#003220', fg_color='#003220', width=800, height=700)
        frame3.place(x=0, y=0)

        username = self.username_entry2.get()
        password = self.password_entry2.get()

        check_role = self.cursor.execute('SELECT role FROM users WHERE username = ?', [username])
        checked = self.cursor.fetchone()
        role = checked[0]

        if role == '0':
            role = 'Users'
        else:
            role = 'Admins'


        self.load_add_bg = Image.open('./Assets/bg_user.png')
        self.render_add_plane = ImageTk.PhotoImage(self.load_add_bg)
        self.img_add_plane = Label(frame3, image=self.render_add_plane)
        self.img_add_plane.place(x=0, y=0)
    
        self.username_label = customtkinter.CTkLabel(frame3,font=self.font3,text=f' Username: {username} ',text_color='#000',bg_color='#86F8FC')
        self.username_label.place(x=19.8,y=39.5)

        self.role_label = customtkinter.CTkLabel(frame3,font=self.font3,text=f' Role: {role} ',text_color='#000',bg_color='#86F8FC')
        self.role_label.place(x=19.8,y=65)

        button1 = customtkinter.CTkButton(frame3, text="PENERBANGAN", font=self.font2, text_color='#fff', bg_color='#14B291',
                                          hover_color='#005940',fg_color='#14B291', width=20)
        button1.place(x=130.5, y=397.8)

        button2 = customtkinter.CTkButton(frame3, text="LIST TIKET", font=self.font2, text_color='#fff', bg_color='#14B291',
                                          hover_color='#005940',fg_color='#14B291', width=20)
        button2.place(x=344.8, y=397.8)

        button4 = customtkinter.CTkButton(frame3, text="LIST USER", font=self.font2, text_color='#fff', bg_color='#14B291',
                                          hover_color='#005940',fg_color='#14B291', width=20)
        button4.place(x=555.5, y=397.8)

        button3 = customtkinter.CTkButton(frame3, text="LOGOUT", font=self.font2, text_color='#fff', bg_color='#14B280',
                                          hover_color='#005940',fg_color='#14B291', width=20)
        button3.place(x=365.3, y=555.2)
        button3.configure(command=lambda: [self.login(), frame3.destroy()])

        def menu1_action():
            self.frame5 = customtkinter.CTkFrame(self.app, bg_color='#003220', fg_color='#003220', width=1800, height=1200)
            self.frame5.place(x=0, y=0)

            self.load_add_bg = Image.open('./Assets/bg_penerbangan.png')
            self.render_add_plane = ImageTk.PhotoImage(self.load_add_bg)
            self.img_add_plane = Label(self.frame5, image=self.render_add_plane)
            self.img_add_plane.place(x=0, y=0)
                
            buttonback1 = customtkinter.CTkButton(self.frame5, text="<", font=self.font2, text_color='#fff', bg_color='#003220',
                                            hover_color='#005940', width=20)
            buttonback1.place(x=10, y=10)
            buttonback1.configure(command=lambda: [self.dashboard_admins(), self.frame5.destroy()])
            
            # Define tree before using it
                        # Define tree before using it
            style = ttk.Style()
            style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
            style.configure("Treeview", font=("Helvetica", 10))
            tree = ttk.Treeview(self.frame5, column=("column1", "column2", "column3","column4", "column5", "column6","column7", "column8"), show='headings')
            tree.heading("#1", text="ID FLIGHT")
            tree.column('#1', width=100, anchor=tk.CENTER)
            tree.heading("#2", text="MASKAPAI")
            tree.column('#2', width=100, anchor=tk.CENTER)
            tree.heading("#3", text="ASAL")
            tree.column('#3', width=100, anchor=tk.CENTER)
            tree.heading("#4", text="TUJUAN")
            tree.column('#4', width=100, anchor=tk.CENTER)
            tree.heading("#5", text="TANGGAL")
            tree.column('#5', width=100, anchor=tk.CENTER)
            tree.heading("#6", text="JAM")
            tree.column('#6', width=100, anchor=tk.CENTER)
            tree.heading("#7", text="HARGA EKO")
            tree.column('#7', width=120, anchor=tk.CENTER)
            tree.heading("#8", text="HARGA VIP")
            tree.column('#8', width=100, anchor=tk.CENTER)
            tree.pack()
            tree.place(x=30.1, y=207)
            
            # Ambil data penerbangan dari database
            self.cursor.execute('SELECT ID_FLIGHT, maskapai, asal_keberangkatan, tujuan_keberangkatan, tanggal_keberangkatan, jam_keberangkatan, harga_eko_keberangkatan, harga_vip_keberangkatan FROM penerbangan')
            penerbangan = self.cursor.fetchall()
            
            # Filter dan urutkan penerbangan berdasarkan tanggal dan jam keberangkatan
            today = datetime.now()
            valid_penerbangan = []
            
            for row in penerbangan:
                tanggal_jam_str = f"{row[4]} {row[5]}"
                tanggal_jam = datetime.strptime(tanggal_jam_str, "%Y-%m-%d %H:%M")
                if tanggal_jam > today:
                    heapq.heappush(valid_penerbangan, (tanggal_jam, row))
            
            # Masukkan data yang sudah diurutkan ke dalam treeview
            while valid_penerbangan:
                _, row = heapq.heappop(valid_penerbangan)
                tree.insert("", tk.END, values=row)

            # Add Entry for CRUD Operations
            self.frame5_add = customtkinter.CTkFrame(self.app, bg_color='#4D421A', fg_color='#4D421A', width=400, height=320)
            self.frame5_add.place(x=30.1, y=361.5)
            self.login_label2 = customtkinter.CTkLabel(self.frame5_add,font=self.font1,text='TAMBAH PENERBANGAN',text_color='#fff',bg_color='#4D421A')
            self.login_label2.place(x=60,y=10)
            id_flight = customtkinter.CTkEntry(self.frame5_add, font=self.font2, placeholder_text='ID FLIGHT', width=100)
            id_flight.place(x=20, y=45)
            maskapai_lurd = ["SR AIR", "J AIRPLANE", "GARUDA", "MERPATI", "SINGA AIR"]
            maskapai_combobox = ttk.Combobox(self.frame5_add, values=maskapai_lurd, font=self.font2, width=10)
            maskapai_combobox.place(x=20, y=105)
            maskapai_combobox.set("MASKAPAI") 
            asal_lurd = ["KEDIRI", "SURABAYA", "JAKARTA", "MALANG"]
            asal_combobox = ttk.Combobox(self.frame5_add, values=asal_lurd, font=self.font2, width=10)
            asal_combobox.place(x=20, y=155)
            asal_combobox.set("ASAL") 
            tujuan_lurd = ["KEDIRI", "SURABAYA", "JAKARTA", "MALANG"]
            tujuan_combobox = ttk.Combobox(self.frame5_add, values=tujuan_lurd, font=self.font2, width=10)
            tujuan_combobox.place(x=20, y=205)
            tujuan_combobox.set("TUJUAN") 
            dates = [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
            tanggal_flight_combobox = ttk.Combobox(self.frame5_add, values=dates, font=self.font2, width=10)
            tanggal_flight_combobox.set("Select Date")
            tanggal_flight_combobox.place(x=20, y=255)
            jam_flight_list = ["04:30", "05:00", "08:00", "11:00", "12:30", "14:00", "17:00", "20:00"]
            jam_flight_combobox = ttk.Combobox(self.frame5_add, values=jam_flight_list, font=self.font2, width=10)
            jam_flight_combobox.place(x=20, y=305)
            jam_flight_combobox.set("18:00") 
            harga_eko_tambah = customtkinter.CTkEntry(self.frame5_add, font=self.font2, placeholder_text='HARGA EKO', width=100)
            harga_eko_tambah.place(x=180, y=45)
            harga_vip_tambah = customtkinter.CTkEntry(self.frame5_add, font=self.font2, placeholder_text='HARGA VIP', width=100)
            harga_vip_tambah.place(x=180, y=85)

            # Add Entry for CRUD Operations
            self.frame5_delete = customtkinter.CTkFrame(self.frame5, bg_color='#4D421A', fg_color='#4D421A', width=300, height=320)
            self.frame5_delete.place(x=460, y=361.5)
            self.login_label2 = customtkinter.CTkLabel(self.frame5_delete,font=self.font1,text='HAPUS PENERBANGAN',text_color='#fff',bg_color='#4D421A')
            self.login_label2.place(x=10,y=10)
            self.cursor.execute('SELECT ID_FLIGHT FROM penerbangan')
            delete_flight_row = [row[0] for row in self.cursor.fetchall()]
            # Create a dropdown (Combobox) for Username
            delete_flight = ttk.Combobox(self.frame5_delete, values=delete_flight_row, font=self.font2, width=10)
            delete_flight.place(x=20, y=60)
            delete_flight.set("Select ID FLIGHT") 

            # Function to Update Treeview
            def update_treeview():
                for item in tree.get_children():
                    tree.delete(item)
                
                # Ambil data penerbangan dari database
                self.cursor.execute('SELECT * FROM penerbangan')
                penerbangan = self.cursor.fetchall()
                
                # Filter dan urutkan penerbangan berdasarkan tanggal dan jam keberangkatan
                today = datetime.now()
                valid_penerbangan = []
                
                for row in penerbangan:
                    tanggal_jam_str = f"{row[4]} {row[5]}"
                    tanggal_jam = datetime.strptime(tanggal_jam_str, "%Y-%m-%d %H:%M")
                    if tanggal_jam > today:
                        heapq.heappush(valid_penerbangan, (tanggal_jam, row))
                
                # Masukkan data yang sudah diurutkan ke dalam treeview
                while valid_penerbangan:
                    _, row = heapq.heappop(valid_penerbangan)
                    tree.insert("", tk.END, values=row)

            # Add Functionality to Add, Update, Delete Records
            def add_record():
                id_flight_value = id_flight.get()
                maskapai_value = maskapai_combobox.get()
                asal_value = asal_combobox.get()
                tujuan_type_value = tujuan_combobox.get()
                tanggal_value = tanggal_flight_combobox.get()
                jam_value = jam_flight_combobox.get()
                harga_eko_tambah_value = harga_eko_tambah.get()
                harga_vip_tambah_value = harga_vip_tambah.get()

                self.cursor.execute('''
                    INSERT INTO penerbangan (ID_FLIGHT, maskapai, asal_keberangkatan, tujuan_keberangkatan, tanggal_keberangkatan, jam_keberangkatan, harga_eko_keberangkatan, harga_vip_keberangkatan)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                    (id_flight_value, maskapai_value, asal_value, tujuan_type_value, tanggal_value, jam_value, harga_eko_tambah_value, harga_vip_tambah_value))
                self.conn.commit()
                update_treeview()

            def update_record():
                username_value = username_combobox.get()
                flight_id_value = flight_id_entry.get()
                ticket_type_value = jenis_tiket_combobox.get()
                seat_value = seat_entry.get()
                name_value = name_entry.get()
                phone_value = phone_entry.get()
                id_card_value = id_card_entry.get()
                
                self.cursor.execute('''
                    UPDATE pemesanan_pesawat
                    SET username=?, id_flight=?, jenis_tiket=?, kursi=?, nama=?, nomor_hp=?, id_card=?
                    WHERE id=?''', 
                    (username_value, flight_id_value, ticket_type_value, seat_value, name_value, phone_value, id_card_value, id_value))
                self.conn.commit()
                update_treeview()

            def delete_record():
                no_tiket = delete_flight.get()
                
                self.cursor.execute('DELETE FROM penerbangan WHERE ID_FLIGHT=?', (no_tiket,))
                self.conn.commit()
                update_treeview()

            add_button = customtkinter.CTkButton(self.frame5_add, text="Add", font=self.font2, text_color='#fff', bg_color='#4D421A',
                                                hover_color='#005940', command=add_record)
            add_button.place(x=180, y=125)

            # update_button = customtkinter.CTkButton(self.frame5, text="Update", font=self.font2, text_color='#fff', bg_color='#fff',
            #                                         hover_color='#005940', command=update_record)
            # update_button.place(x=525.8, y=310)

            delete_button = customtkinter.CTkButton(self.frame5_delete, text="Delete", font=self.font2, text_color='#fff', bg_color='#4D421A',
                                                    hover_color='#005940', command=delete_record)
            delete_button.place(x=20, y=125)

        


        def menu2_action():
            self.frame6 = customtkinter.CTkFrame(self.app, width=1800, height=1200)
            self.frame6.place(x=0, y=0)
            
            self.load_add_bg = Image.open('./Assets/bg_datatiket.png')
            self.render_add_plane = ImageTk.PhotoImage(self.load_add_bg)
            self.img_add_plane = Label(self.frame6, image=self.render_add_plane)
            self.img_add_plane.place(x=0, y=0)

            buttonback1 = customtkinter.CTkButton(self.frame6, text="<", font=self.font2, text_color='#fff', bg_color='#003220',
                                                hover_color='#005940', width=20)
            buttonback1.place(x=10, y=10)
            buttonback1.configure(command=lambda: [self.dashboard_admins(), self.frame6.destroy()])



            style = ttk.Style()
            style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
            style.configure("Treeview", font=("Helvetica", 10))

            tree = ttk.Treeview(self.frame6, column=("column1", "column2", "column3", "column4", "column5", "column6", "column7", "column8"), show='headings')
            tree.heading("#1", text="ID")
            tree.column('#1', width=50, anchor=tk.CENTER)
            tree.heading("#2", text="USERNAME")
            tree.column('#2', width=120, anchor=tk.CENTER)
            tree.heading("#3", text="ID FLIGHT")
            tree.column('#3', width=100, anchor=tk.CENTER)
            tree.heading("#4", text="JENIS TIKET")
            tree.column('#4', width=120, anchor=tk.CENTER)
            tree.heading("#5", text="KURSI")
            tree.column('#5', width=95, anchor=tk.CENTER)
            tree.heading("#6", text="NAMA")
            tree.column('#6', width=100, anchor=tk.CENTER)
            tree.heading("#7", text="NOMER HP")
            tree.column('#7', width=120, anchor=tk.CENTER)
            tree.heading("#8", text="ID CARD")
            tree.column('#8', width=120, anchor=tk.CENTER)
            tree.pack()
            tree.place(x=30.1, y=207)

            checkUsers = self.cursor.execute('SELECT * FROM pemesanan_pesawat')
            checked = self.cursor.fetchall()
            users = checked

            for row in users:
                print(row) 
                tree.insert("", tk.END, values=row)

            # Add Entry Widgets for CRUD Operations
            self.frame6_add = customtkinter.CTkFrame(self.frame6,bg_color='#4D421A', fg_color='#4D421A', width=400, height=175)
            self.frame6_add.place(x=30.1, y=361.5)
            self.login_label2 = customtkinter.CTkLabel(self.frame6_add,font=self.font1,text='TAMBAH',text_color='#fff',bg_color='#4D421A')
            self.login_label2.place(x=150,y=10)
            # Fetch usernames from the users table
            self.cursor.execute('SELECT username FROM users WHERE role = 0')
            usernames = [row[0] for row in self.cursor.fetchall()]
            # Create a dropdown (Combobox) for Username
            username_combobox = ttk.Combobox(self.frame6_add, values=usernames, font=self.font2, width=10)
            username_combobox.place(x=20, y=60)
            username_combobox.set("Select Username") 
            self.cursor.execute('SELECT ID_FLIGHT FROM penerbangan')
            flight_id_list = [row[0] for row in self.cursor.fetchall()]
            flight_id_entry = ttk.Combobox(self.frame6_add, values=flight_id_list, font=self.font2, width=10)
            flight_id_entry.place(x=20, y=100)
            flight_id_entry.set("Select ID FLIGHT") 
            id_card_options = ["Ekonomi", "Vip"]
            jenis_tiket_combobox = ttk.Combobox(self.frame6_add, values=id_card_options, font=self.font2, width=10)
            jenis_tiket_combobox.place(x=20, y=140)
            jenis_tiket_combobox.set("Jenis Tiket") 
            seat_entry = customtkinter.CTkEntry(self.frame6_add, font=self.font2, placeholder_text='Kursi', width=100)
            seat_entry.place(x=150, y=60)
            name_entry = customtkinter.CTkEntry(self.frame6_add, font=self.font2, placeholder_text='Nama', width=100)
            name_entry.place(x=150, y=100)
            phone_entry = customtkinter.CTkEntry(self.frame6_add, font=self.font2, placeholder_text='Nomer HP', width=100)
            phone_entry.place(x=270, y=60)
            id_card_entry = customtkinter.CTkEntry(self.frame6_add, font=self.font2, placeholder_text='ID Card', width=100)
            id_card_entry.place(x=270, y=100)

            # Add Update Widgets for CRUD Operations
            self.frame6_update = customtkinter.CTkFrame(self.frame6, bg_color='#4D421A', fg_color='#4D421A', width=300, height=320)
            self.frame6_update.place(x=460, y=361.5)
            self.login_label2 = customtkinter.CTkLabel(self.frame6_update, font=self.font1, text='UPDATE', text_color='#fff', bg_color='#4D421A')
            self.login_label2.place(x=83, y=10)
            # Fetch id_pemesanan from the pemesanan_pesawat table
            self.cursor.execute('SELECT id FROM pemesanan_pesawat')
            id_pemesanan_update = [row[0] for row in self.cursor.fetchall()]
            id_pemesanan_update_combobox = ttk.Combobox(self.frame6_update, values=id_pemesanan_update, font=self.font2, width=10)
            id_pemesanan_update_combobox.place(x=20, y=60)
            id_pemesanan_update_combobox.set("Select ID")  # Set default value
            # Define input fields
            username_update = customtkinter.CTkEntry(self.frame6_update, font=self.font2, placeholder_text='Username', width=100)
            username_update.place(x=20, y=100)
            id_flight_update = customtkinter.CTkEntry(self.frame6_update, font=self.font2, placeholder_text='ID FLIGHT', width=100)
            id_flight_update.place(x=140, y=100)
            jenis_tiket_update_combobox = customtkinter.CTkEntry(self.frame6_update, font=self.font2, placeholder_text='Jenis Tiket', width=100)
            jenis_tiket_update_combobox.place(x=20, y=140)
            seat_entry_update = customtkinter.CTkEntry(self.frame6_update, font=self.font2, placeholder_text='Kursi', width=100)
            seat_entry_update.place(x=20, y=180)
            name_entry_update = customtkinter.CTkEntry(self.frame6_update, font=self.font2, placeholder_text='Nama', width=100)
            name_entry_update.place(x=20, y=220)
            phone_entry_update = customtkinter.CTkEntry(self.frame6_update, font=self.font2, placeholder_text='Nomer HP', width=100)
            phone_entry_update.place(x=140, y=180)
            id_card_entry_update = customtkinter.CTkEntry(self.frame6_update, font=self.font2, placeholder_text='ID Card', width=100)
            id_card_entry_update.place(x=140, y=140)

            def fill_entries(event):
                selected_id = id_pemesanan_update_combobox.get()
                if selected_id:
                    self.cursor.execute('SELECT username_pemesan, id_penerbangan, jenis_tiket, nomer_kursi, nama_pemesan, nomer_hp_pemesan, idcard_pemesan FROM pemesanan_pesawat WHERE id=?', (selected_id,))
                    result = self.cursor.fetchone()
                    if result:
                        username_update.delete(0, tk.END)
                        username_update.insert(0, result[0])
                        id_flight_update.delete(0, tk.END)
                        id_flight_update.insert(0, result[1])
                        jenis_tiket_update_combobox.delete(0, tk.END)
                        jenis_tiket_update_combobox.insert(0, result[2])
                        seat_entry_update.delete(0, tk.END)
                        seat_entry_update.insert(0, result[3])
                        name_entry_update.delete(0, tk.END)
                        name_entry_update.insert(0, result[4])
                        phone_entry_update.delete(0, tk.END)
                        phone_entry_update.insert(0, result[5])
                        id_card_entry_update.delete(0, tk.END)
                        id_card_entry_update.insert(0, result[6])

            id_pemesanan_update_combobox.bind("<<ComboboxSelected>>", fill_entries)

            ###### TEMPAT ALGORITMA SEARCHING
            self.frame6_search = customtkinter.CTkFrame(self.frame6, bg_color='#4D421A', fg_color='#4D421A', width=400, height=130)
            self.frame6_search.place(x=30, y=550)
            self.login_label2 = customtkinter.CTkLabel(self.frame6_search, font=self.font1, text='SEARCH', text_color='#fff', bg_color='#4D421A')
            self.login_label2.place(x=170, y=10)

            search_entry = customtkinter.CTkEntry(self.frame6_search, font=self.font2, placeholder_text='Search by Name', width=200)
            search_entry.place(x=100, y=60)

            # Sort and Search Function
            def sort_and_search():
                search_text = search_entry.get().lower()
                
                self.cursor.execute('SELECT * FROM pemesanan_pesawat')
                rows = self.cursor.fetchall()

                # Sort by name
                rows_sorted = sorted(rows, key=lambda x: x[5].lower())  # Assuming 'nama_pemesan' is the 6th column (index 5)

                # Filter by search text
                filtered_rows = [row for row in rows_sorted if search_text in row[5].lower()]

                # Clear Treeview
                for item in tree.get_children():
                    tree.delete(item)

                # Insert filtered rows
                for row in filtered_rows:
                    tree.insert("", tk.END, values=row)

            search_button = customtkinter.CTkButton(self.frame6_search, text="Search", font=self.font2, text_color='#fff', bg_color='#4D421A',
                                                hover_color='#005940', command=sort_and_search)
            search_button.place(x=150, y=100)


            # Function to Update Treeview
            def update_treeview():
                for item in tree.get_children():
                    tree.delete(item)
                checkUsers = self.cursor.execute('SELECT * FROM pemesanan_pesawat')
                checked = self.cursor.fetchall()
                users = checked
                for row in users:
                    tree.insert("", tk.END, values=row)
            
            # Add Functionality to Add, Update, Delete Records
            def add_record():
                username_value = username_combobox.get()
                flight_id_value = flight_id_entry.get()
                ticket_type_value = jenis_tiket_combobox.get()
                seat_value = seat_entry.get()
                name_value = name_entry.get()
                phone_value = phone_entry.get()
                id_card_value = id_card_entry.get()
                
                self.cursor.execute('''
                    INSERT INTO pemesanan_pesawat (username_pemesan, id_penerbangan, jenis_tiket, nomer_kursi, nama_pemesan, nomer_hp_pemesan, idcard_pemesan)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                    (username_value, flight_id_value, ticket_type_value, seat_value, name_value, phone_value, id_card_value))
                self.conn.commit()
                update_treeview()

            def update_record():
                username_value = username_update.get()
                flight_id_value = id_flight_update.get()
                ticket_type_value = jenis_tiket_update_combobox.get()
                seat_value = seat_entry_update.get()
                name_value = name_entry_update.get()
                phone_value = phone_entry_update.get()
                id_card_value = id_card_entry_update.get()
                id_value = id_pemesanan_update_combobox.get()  # Ambil ID dari combobox

                self.cursor.execute('''
                    UPDATE pemesanan_pesawat
                    SET username_pemesan=?, id_penerbangan=?, jenis_tiket=?, nomer_kursi=?, nama_pemesan=?, nomer_hp_pemesan=?, idcard_pemesan=?
                    WHERE id=?''', 
                    (username_value, flight_id_value, ticket_type_value, seat_value, name_value, phone_value, id_card_value, id_value))
                self.conn.commit()
                
                update_treeview()

            def delete_record():
                id_value = id_entry.get()
                
                self.cursor.execute('DELETE FROM pemesanan_pesawat WHERE id=?', (id_value,))
                self.conn.commit()
                update_treeview()
                

            add_button = customtkinter.CTkButton(self.frame6_add, text="Add", font=self.font2, text_color='#fff', bg_color='#4D421A',
                                                hover_color='#005940', command=add_record)
            add_button.place(x=70, y=260-118)

            update_button = customtkinter.CTkButton(self.frame6_update, text="Update", font=self.font2, text_color='#fff', bg_color='#4D421A',
                                                    hover_color='#005940', command=update_record)
            update_button.place(x=140, y=260)

            delete_button = customtkinter.CTkButton(self.frame6, text="Delete", font=self.font2, text_color='#fff', bg_color='#4D421A',
                                                    hover_color='#005940', command=delete_record)
            delete_button.place(x=260, y=621-118)

        def menu4_action():
            self.frame4 = customtkinter.CTkFrame(self.app, bg_color='#003220', fg_color='#003220', width=1800, height=1200)
            self.frame4.place(x=0, y=0)
            
            self.load_add_bg = Image.open('./Assets/bg_datauser.png')
            self.render_add_plane = ImageTk.PhotoImage(self.load_add_bg)
            self.img_add_plane = Label(self.frame4, image=self.render_add_plane)
            self.img_add_plane.place(x=0, y=0)


            buttonback1 = customtkinter.CTkButton(self.frame4, text="<", font=self.font2, text_color='#fff', bg_color='#003220',
                                            hover_color='#005940', width=20)
            buttonback1.place(x=10, y=10)
            buttonback1.configure(command=lambda: [self.dashboard_admins(), self.frame4.destroy()])

            style = ttk.Style()
            style.configure("Treeview.Heading", font=("Helvetica", 16, "bold"))
            style.configure("Treeview", font=("Helvetica", 13))


            tree = ttk.Treeview(self.frame4, column=("column1", "column2", "column3"), show='headings')
            tree.heading("#1", text="NAMA")
            tree.heading("#2", text="PASSWORD")
            tree.heading("#3", text="ROLE")
            tree.pack()
            tree.place(x=80, y=212.4)

            for i in range(3):
                tree.column('#' + str(i), minwidth=300, stretch=0)
                tree.heading(i, text="Column {}".format(i))
            tree.column('#0', stretch=0)

            checkUsers = self.cursor.execute('SELECT * FROM users')
            checked = self.cursor.fetchall()
            users = checked

            for row in users:
                print(row) 
                tree.insert("", tk.END, values=row)

        button1.configure(command=menu1_action)
        button2.configure(command=menu2_action)
        button4.configure(command=menu4_action)


    def dashboard_users(self):
        frame3 = customtkinter.CTkFrame(self.app, width=800, height=700)
        frame3.place(x=0, y=0)

        username = self.username_entry2.get()
        password = self.password_entry2.get()

        check_role = self.cursor.execute('SELECT role FROM users WHERE username = ?', [username])
        checked = self.cursor.fetchone()
        role = checked[0]

        if role == '0':
            role = 'Users'
        else:
            role = 'Admins'

        self.load_add_bg = Image.open('./Assets/bg_user.png')
        self.render_add_plane = ImageTk.PhotoImage(self.load_add_bg)
        self.img_add_plane = Label(frame3, image=self.render_add_plane)
        self.img_add_plane.place(x=0, y=0)
    
        self.username_label = customtkinter.CTkLabel(frame3,font=self.font3,text=f' Username: {username} ',text_color='#000',bg_color='#86F8FC')
        self.username_label.place(x=19.8,y=39.5)

        self.role_label = customtkinter.CTkLabel(frame3,font=self.font3,text=f' Role: {role} ',text_color='#000',bg_color='#86F8FC')
        self.role_label.place(x=19.8,y=65)

        button1 = customtkinter.CTkButton(frame3, text="CEK JADWAL", font=self.font2, text_color='#fff', bg_color='#14B291',
                                          hover_color='#005940',fg_color='#14B291', width=20)
        button1.place(x=136.5, y=397.8)

        button2 = customtkinter.CTkButton(frame3, text="PESAN TIKET", font=self.font2, text_color='#fff', bg_color='#14B291',
                                          hover_color='#005940',fg_color='#14B291', width=20)
        button2.place(x=336.8, y=397.8)

        button3 = customtkinter.CTkButton(frame3, text="TIKET SAYA", font=self.font2, text_color='#fff', bg_color='#14B291',
                                          hover_color='#005940',fg_color='#14B291', width=20)
        button3.place(x=544.5, y=397.8)

        button4 = customtkinter.CTkButton(frame3, text="LOGOUT", font=self.font2, text_color='#fff', bg_color='#14B280',
                                          hover_color='#005940',fg_color='#14B291', width=20)
        button4.place(x=365.3, y=555.2)
        button4.configure(command=lambda: [self.login(), frame3.destroy()])

        def menu1_action():
            self.frame_menu1_cek = customtkinter.CTkFrame(self.app, bg_color='#003220', fg_color='#003220', width=1800, height=1200)
            self.frame_menu1_cek.place(x=0, y=0)
            
            self.load_add_bg = Image.open('./Assets/bg_jadwal.png')
            self.render_add_plane = ImageTk.PhotoImage(self.load_add_bg)
            self.img_add_plane = Label(self.frame_menu1_cek, image=self.render_add_plane)
            self.img_add_plane.place(x=0, y=0)

            buttonback1 = customtkinter.CTkButton(self.frame_menu1_cek, text="<", font=self.font2, text_color='#fff', bg_color='#003220',
                                            hover_color='#005940', width=20)
            buttonback1.place(x=10, y=10)
            buttonback1.configure(command=lambda: [self.dashboard_users(), self.frame_menu2_pesan.destroy()])
            
            # Define tree before using it
            style = ttk.Style()
            style.configure("Treeview.Heading", font=("Helvetica", 16, "bold"))
            style.configure("Treeview", font=("Helvetica", 13))

            tree = ttk.Treeview(self.frame_menu1_cek, column=("column1", "column2", "column3","column4", "column5", "column6","column7", "column8"), show='headings')
            tree.heading("#1", text="ID FLIGHT")
            tree.column('#1', width=120, anchor=tk.CENTER)
            tree.heading("#2", text="MASKAPAI")
            tree.column('#2', width=120, anchor=tk.CENTER)
            tree.heading("#3", text="ASAL")
            tree.column('#3', width=120, anchor=tk.CENTER)
            tree.heading("#4", text="TUJUAN")
            tree.column('#4', width=120, anchor=tk.CENTER)
            tree.heading("#5", text="TANGGAL")
            tree.column('#5', width=120, anchor=tk.CENTER)
            tree.heading("#6", text="JAM")
            tree.column('#6', width=100, anchor=tk.CENTER)
            tree.heading("#7", text="HARGA EKO")
            tree.column('#7', width=140, anchor=tk.CENTER)
            tree.heading("#8", text="HARGA VIP")
            tree.column('#8', width=120, anchor=tk.CENTER)
            tree.pack()
            tree.place(x=20.3, y=201)
            
            # Ambil data penerbangan dari database
            self.cursor.execute('SELECT ID_FLIGHT, maskapai, asal_keberangkatan, tujuan_keberangkatan, tanggal_keberangkatan, jam_keberangkatan, harga_eko_keberangkatan, harga_vip_keberangkatan FROM penerbangan')
            penerbangan = self.cursor.fetchall()
            
            # Filter dan urutkan penerbangan berdasarkan tanggal dan jam keberangkatan
            today = datetime.now()
            valid_penerbangan = []
            
            for row in penerbangan:
                tanggal_jam_str = f"{row[4]} {row[5]}"
                tanggal_jam = datetime.strptime(tanggal_jam_str, "%Y-%m-%d %H:%M")
                if tanggal_jam > today:
                    heapq.heappush(valid_penerbangan, (tanggal_jam, row))
            
            # Masukkan data yang sudah diurutkan ke dalam treeview
            while valid_penerbangan:
                _, row = heapq.heappop(valid_penerbangan)
                tree.insert("", tk.END, values=row)

        def menu2_action():
            self.frame_menu2_pesan = customtkinter.CTkFrame(self.app, bg_color='#003220', fg_color='#003220', width=1800, height=1200)
            self.frame_menu2_pesan.place(x=0, y=0)

            self.load_add_bg = Image.open('./Assets/bg_pesantiket.png')
            self.render_add_plane = ImageTk.PhotoImage(self.load_add_bg)
            self.img_add_plane = Label(self.frame_menu2_pesan, image=self.render_add_plane)
            self.img_add_plane.place(x=0, y=0)
                
            buttonback1 = customtkinter.CTkButton(self.frame_menu2_pesan, text="<", font=self.font2, text_color='#fff', bg_color='#003220',
                                            hover_color='#005940', width=20)
            buttonback1.place(x=10, y=10)
            buttonback1.configure(command=lambda: [self.dashboard_users(), self.frame_menu2_pesan.destroy()])
            
            # Define tree before using it
            style = ttk.Style()
            style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
            style.configure("Treeview", font=("Helvetica", 10))
            tree = ttk.Treeview(self.frame_menu2_pesan, column=("column1", "column2", "column3","column4", "column5", "column6","column7", "column8"), show='headings')
            tree.heading("#1", text="ID FLIGHT")
            tree.column('#1', width=100, anchor=tk.CENTER)
            tree.heading("#2", text="MASKAPAI")
            tree.column('#2', width=100, anchor=tk.CENTER)
            tree.heading("#3", text="ASAL")
            tree.column('#3', width=100, anchor=tk.CENTER)
            tree.heading("#4", text="TUJUAN")
            tree.column('#4', width=100, anchor=tk.CENTER)
            tree.heading("#5", text="TANGGAL")
            tree.column('#5', width=100, anchor=tk.CENTER)
            tree.heading("#6", text="JAM")
            tree.column('#6', width=100, anchor=tk.CENTER)
            tree.heading("#7", text="HARGA EKO")
            tree.column('#7', width=120, anchor=tk.CENTER)
            tree.heading("#8", text="HARGA VIP")
            tree.column('#8', width=100, anchor=tk.CENTER)
            tree.pack()
            tree.place(x=17.5, y=199)
            
            # Ambil data penerbangan dari database
            self.cursor.execute('SELECT ID_FLIGHT, maskapai, asal_keberangkatan, tujuan_keberangkatan, tanggal_keberangkatan, jam_keberangkatan, harga_eko_keberangkatan, harga_vip_keberangkatan FROM penerbangan')
            penerbangan = self.cursor.fetchall()
            
            # Filter dan urutkan penerbangan berdasarkan tanggal dan jam keberangkatan
            today = datetime.now()
            valid_penerbangan = []
            
            for row in penerbangan:
                tanggal_jam_str = f"{row[4]} {row[5]}"
                tanggal_jam = datetime.strptime(tanggal_jam_str, "%Y-%m-%d %H:%M")
                if tanggal_jam > today:
                    heapq.heappush(valid_penerbangan, (tanggal_jam, row))
            
            # Masukkan data yang sudah diurutkan ke dalam treeview
            while valid_penerbangan:
                _, row = heapq.heappop(valid_penerbangan)
                tree.insert("", tk.END, values=row)

            self.frame_menu2_tiket = customtkinter.CTkFrame(self.frame_menu2_pesan, bg_color='#4D421A', fg_color='#4D421A', width=751.8, height=311.9)
            self.frame_menu2_tiket.place(x=17.5,y=361.5)
            
            # Search Asal Tujuan
            def search_asaltujuan():
                def linear_search(asal_input1, tujuan_input2):
                    self.cursor.execute('SELECT asal_keberangkatan FROM penerbangan')
                    self.data_asal = list(set(row[0] for row in self.cursor.fetchall()))
                    self.cursor.execute('SELECT tujuan_keberangkatan FROM penerbangan')
                    self.data_tujuan = list(set(row[0] for row in self.cursor.fetchall()))

                    index_asal = next((i for i, val in enumerate(self.data_asal) if val.lower() == asal_input1.lower()), -1)
                    index_tujuan = next((i for i, val in enumerate(self.data_tujuan) if val.lower() == tujuan_input2.lower()), -1)

                    return index_asal, index_tujuan, self.data_asal, self.data_tujuan  

                asal_input1 = asal_maskapai_list_pesantiket.get()
                tujuan_input2 = tujuan_maskapai_list_pesantiket.get()

                index_asal, index_tujuan, self.data_asal, self.data_tujuan = linear_search(asal_input1, tujuan_input2)

                if index_asal != -1 and index_tujuan != -1:
                    self.cursor.execute('SELECT ID_FLIGHT, maskapai, asal_keberangkatan, tujuan_keberangkatan, tanggal_keberangkatan, jam_keberangkatan, harga_eko_keberangkatan, harga_vip_keberangkatan FROM penerbangan WHERE asal_keberangkatan=? AND tujuan_keberangkatan=?', (self.data_asal[index_asal], self.data_tujuan[index_tujuan]))
                    result = self.cursor.fetchall()
                    
                    if result:
                        # Hapus semua item di treeview sebelum memasukkan data yang baru
                        for item in tree.get_children():
                            tree.delete(item)
                        # Masukkan data baru ke treeview
                        for row in result:
                            tree.insert("", tk.END, values=row)
                        print(result)
                    else:
                        messagebox.showerror('Err', f"Tidak ditemukan data penerbangan dari '{self.data_asal[index_asal]}' ke '{self.data_tujuan[index_tujuan]}'.")
            
            # Input fields
            self.cursor.execute('SELECT asal_keberangkatan FROM penerbangan')
            asal_maskapai_list = list(set(row[0] for row in self.cursor.fetchall()))
            asal_maskapai_list_pesantiket = ttk.Combobox(self.frame_menu2_tiket, values=asal_maskapai_list, font=self.font2, width=10)
            asal_maskapai_list_pesantiket.place(x=20, y=30)
            asal_maskapai_list_pesantiket.set("Pilih Asal")
            self.cursor.execute('SELECT tujuan_keberangkatan FROM penerbangan')
            tujuan_maskapai_list = list(set(row[0] for row in self.cursor.fetchall()))
            tujuan_maskapai_list_pesantiket = ttk.Combobox(self.frame_menu2_tiket, values=tujuan_maskapai_list, font=self.font2, width=10)
            tujuan_maskapai_list_pesantiket.place(x=180, y=30)
            tujuan_maskapai_list_pesantiket.set("Pilih Asal")
            def update_maskapai_pesantiket(event):
                asal = asal_maskapai_list_pesantiket.get()
                tujuan = tujuan_maskapai_list_pesantiket.get()
                if asal != "Pilih Asal" and tujuan != "Pilih Tujuan":
                    self.cursor.execute('SELECT maskapai FROM penerbangan WHERE asal_keberangkatan=? AND tujuan_keberangkatan=?', (asal, tujuan))
                    maskapai_pesantiket_list = list(set(row[0] for row in self.cursor.fetchall()))
                    maskapai_pesantiket['values'] = maskapai_pesantiket_list
                    if maskapai_pesantiket_list:
                        maskapai_pesantiket.set(maskapai_pesantiket_list[0])
                    else:
                        maskapai_pesantiket.set('Maskapai tidak tersedia')  
            asal_maskapai_list_pesantiket.bind("<<ComboboxSelected>>", update_maskapai_pesantiket)
            tujuan_maskapai_list_pesantiket.bind("<<ComboboxSelected>>", update_maskapai_pesantiket)
            maskapai_pesantiket = ttk.Combobox(self.frame_menu2_tiket, values=[], font=self.font2, width=15)
            maskapai_pesantiket.place(x=20, y=75)
            maskapai_pesantiket.set("Maskapai")
            tanggal_keberangkatan_pesantiket = customtkinter.CTkEntry(self.frame_menu2_tiket, font=self.font2, placeholder_text='TANGGAL', width=20)
            tanggal_keberangkatan_pesantiket.place(x=20, y=165)
            jam_keberangkatan_pesantiket = customtkinter.CTkEntry(self.frame_menu2_tiket, font=self.font2, placeholder_text='JAM', width=100)
            jam_keberangkatan_pesantiket.place(x=350, y=23+35+35+35)

            tiket_option_pesantiket = ['VIP', 'Economy']

            def on_tiket_selected(event):
                if jenis_tiket_pesantiket.get() == "VIP":
                    ambil_seat_button.place(x=230, y=260)
                    self.kursi_pesantiket.place(x=140, y=260)
                else:
                    ambil_seat_button.place_forget()
                    self.kursi_pesantiket.place_forget()

                


            self.kursi_pesantiket = customtkinter.CTkEntry(self.frame_menu2_tiket, font=self.font2, placeholder_text='NO KURSI', width=60)
            self.kursi_pesantiket.place_forget()

            jenis_tiket_pesantiket = ttk.Combobox(self.frame_menu2_tiket, values=tiket_option_pesantiket, font=self.font2, width=8)
            jenis_tiket_pesantiket.place(x=20, y=210)
            jenis_tiket_pesantiket.set("Jenis Tiket")
            jenis_tiket_pesantiket.bind("<<ComboboxSelected>>", on_tiket_selected)
            self.cursor.execute('SELECT ID_FLIGHT FROM penerbangan')
            flight_id_list = [row[0] for row in self.cursor.fetchall()]
            flight_id_list_pesantiket = ttk.Combobox(self.frame_menu2_tiket, values=flight_id_list, font=self.font2, width=20)
            flight_id_list_pesantiket.place(x=20, y=120)
            flight_id_list_pesantiket.set("Select ID FLIGHT") 
            nama_pesantiket = customtkinter.CTkEntry(self.frame_menu2_tiket, font=self.font2, placeholder_text='NAMA', width=100)
            nama_pesantiket.place(x=350, y=23)
            nomorhp_pesantiket = customtkinter.CTkEntry(self.frame_menu2_tiket, font=self.font2, placeholder_text='NO HP', width=100)
            nomorhp_pesantiket.place(x=350, y=23+35)
            idcard_pesantiket = customtkinter.CTkEntry(self.frame_menu2_tiket, font=self.font2, placeholder_text='ID CARD', width=100)
            idcard_pesantiket.place(x=350, y=23+35+35)
        
            def select_seat_func():

                framexx = customtkinter.CTkFrame(self.frame_menu2_pesan, bg_color='#4D421A', fg_color='#4D421A', width=100, height=100)
                framexx.place(x=500, y=230)

                #self.login_label2 = customtkinter.CTkLabel(framexx, font=self.font1, text='PESAN TIKET', text_color='#fff', bg_color='#001220')
                #self.login_label2.place(x=100, y=0)

                # Data untuk tata letak bangku pesawat
                rows = 10
                cols = 6
                seat_labels = [
                    "A1", "B1", "", "C1", "D1", "",
                    "A2", "B2", "", "C2", "D2", "",
                    "A3", "B3", "", "C3", "D3", "",
                    "A4", "B4", "", "C4", "D4", "",
                    "A5", "B5", "", "C5", "D5", "",
                    "", "", "", "", "", "",
                    "A6", "B6", "", "C6", "D6", "",
                    "A7", "B7", "", "C7", "D7", "",
                    "A8", "B8", "", "C8", "D8", "",
                    "A9", "B9", "", "C9", "D9", "",
                ]

                buttons = []
                bangku_dipilih = tk.StringVar()

                for i in range(rows):
                    for j in range(cols):
                        if seat_labels[i * cols + j] != "":
                            label = seat_labels[i * cols + j]
                            button = tk.Button(framexx, text=label, width=4, height=2,
                                            command=lambda lbl=label: select_seat(lbl))
                            button.grid(row=i, column=j, padx=5, pady=5)  # Tambahkan padding jika diperlukan
                            buttons.append(button)
                        else:
                            # Spacer for aisle
                            frame = tk.Frame(framexx, width=10, height=2)
                            frame.grid(row=i, column=j)

                # Spacer for aisle
                for i in range(rows):
                    frame = tk.Frame(framexx, width=10, height=2)
                    frame.grid(row=i, column=cols)

                # Add some padding
                for j in range(cols + 1):
                    frame = tk.Frame(framexx, width=10, height=2)
                    frame.grid(row=rows, column=j)

                def select_seat(seat_label):
                    bangku_dipilih.set(seat_label)
                    self.bangku_fix = seat_label
                    print(self.bangku_fix)
                    self.kursi_pesantiket.delete(0, tk.END)
                    self.kursi_pesantiket.insert(0, seat_label)
                    # Menutup jendela setelah bangku dipilih
                    framexx.destroy()

            def fill_entries(event):
                selected_id = flight_id_list_pesantiket.get()
                if selected_id:
                    self.cursor.execute('SELECT maskapai, asal_keberangkatan, tujuan_keberangkatan, tanggal_keberangkatan, jam_keberangkatan FROM penerbangan WHERE ID_FLIGHT=?', (selected_id,))
                    result = self.cursor.fetchone()
                    if result:
                        maskapai_pesantiket.delete(0, tk.END)
                        maskapai_pesantiket.insert(0, result[0])
                        asal_maskapai_list_pesantiket.delete(0, tk.END)
                        asal_maskapai_list_pesantiket.insert(0, result[1])
                        tujuan_maskapai_list_pesantiket.delete(0, tk.END)
                        tujuan_maskapai_list_pesantiket.insert(0, result[2])
                        tanggal_keberangkatan_pesantiket.delete(0, tk.END)
                        tanggal_keberangkatan_pesantiket.insert(0, result[3])
                        jam_keberangkatan_pesantiket.delete(0, tk.END)
                        jam_keberangkatan_pesantiket.insert(0, result[4])

            flight_id_list_pesantiket.bind("<<ComboboxSelected>>", fill_entries)

            def update_treevieww():
                self.cursor.execute('SELECT ID_FLIGHT, maskapai, asal_keberangkatan, tujuan_keberangkatan, tanggal_keberangkatan, jam_keberangkatan, harga_eko_keberangkatan, harga_vip_keberangkatan FROM penerbangan')
                penerbangan = self.cursor.fetchall()
                
                # Filter dan urutkan penerbangan berdasarkan tanggal dan jam keberangkatan
                today = datetime.now()
                valid_penerbangan = []
                
                for row in penerbangan:
                    tanggal_jam_str = f"{row[4]} {row[5]}"
                    tanggal_jam = datetime.strptime(tanggal_jam_str, "%Y-%m-%d %H:%M")
                    if tanggal_jam > today:
                        heapq.heappush(valid_penerbangan, (tanggal_jam, row))
                
                # Masukkan data yang sudah diurutkan ke dalam treeview
                while valid_penerbangan:
                    _, row = heapq.heappop(valid_penerbangan)
                    tree.insert("", tk.END, values=row)

            def assign_random_seat():
                seat_number = random.randint(1, 100)  # Sesuaikan dengan jumlah kursi yang tersedia
                return f'{seat_number}'

            def add_record():
                username_pesantiket_value = self.username_entry2.get()
                flight_id_list_pesantiket_value = flight_id_list_pesantiket.get()
                jenis_tiket_pesantiket_value = jenis_tiket_pesantiket.get()
                if jenis_tiket_pesantiket_value == "Ekonomi":
                    kursi_pesantiket_value = assign_random_seat()
                else:
                    kursi_pesantiket_value = self.kursi_pesantiket.get()
                nama_pesantiket_value = nama_pesantiket.get()
                nomorhp_pesantiket_value = nomorhp_pesantiket.get()
                idcard_pesantiket_value = idcard_pesantiket.get()
                
                self.cursor.execute('''
                    INSERT INTO pemesanan_pesawat (username_pemesan, id_penerbangan, jenis_tiket, nomer_kursi, nama_pemesan, nomer_hp_pemesan, idcard_pemesan)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                    (username_pesantiket_value, flight_id_list_pesantiket_value, jenis_tiket_pesantiket_value, kursi_pesantiket_value, nama_pesantiket_value, nomorhp_pesantiket_value, idcard_pesantiket_value))
                self.conn.commit()
                update_treevieww()

            add_button = customtkinter.CTkButton(self.frame_menu2_tiket, text="Add", font=self.font2, text_color='#fff', bg_color='#4D421A',
                                                hover_color='#005940', command=add_record)
            add_button.place(x=350, y=23+35+35+45+35)

            search_asaltujuan_button = customtkinter.CTkButton(self.frame_menu2_tiket, text="Search", font=self.font2, text_color='#fff', bg_color='#4D421A',
                                                hover_color='#005940', command=search_asaltujuan, corner_radius=5,width=90)
            search_asaltujuan_button.place(x=20, y=23+35+35+45+35+45)
            
            ambil_seat_button = customtkinter.CTkButton(self.frame_menu2_tiket, text="Pilih kursi", font=self.font2, text_color='#fff', bg_color='#4D421A',
                                                        hover_color='#005940', command=select_seat_func, corner_radius=5, width=90)
            ambil_seat_button.place(x=260, y=380)
            ambil_seat_button.place_forget()

            self.load_add_bg1 = Image.open('./Assets/denah_pesawat.png')
            self.render_add_plane1 = ImageTk.PhotoImage(self.load_add_bg1)
            self.img_add_plane1 = Label(self.frame_menu2_tiket, image=self.render_add_plane1)
            self.img_add_plane1.place(x=555.1, y=375)
            self.img_add_plane1.place_forget()

        def menu3_action():
            self.frame_menu3_tiketsaya = customtkinter.CTkFrame(self.app, bg_color='#003220', fg_color='#003220', width=1800, height=1200)
            self.frame_menu3_tiketsaya.place(x=0, y=0)
            
            self.load_add_bg = Image.open('./Assets/bg_my.png')
            self.render_add_plane = ImageTk.PhotoImage(self.load_add_bg)
            self.img_add_plane = Label(self.frame_menu3_tiketsaya, image=self.render_add_plane)
            self.img_add_plane.place(x=0, y=0)
            buttonback1 = customtkinter.CTkButton(self.frame_menu3_tiketsaya, text="<", font=self.font2, text_color='#fff', bg_color='#003220',
                                            hover_color='#005940', width=20)
            buttonback1.place(x=10, y=10)
            buttonback1.configure(command=lambda: [self.dashboard_users(), self.frame_menu3_tiketsaya.destroy()])            
            # Define tree before using it
            style = ttk.Style()
            style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
            style.configure("Treeview", font=("Helvetica", 10))
            tree = ttk.Treeview(self.frame_menu3_tiketsaya, column=("column1", "column2", "column3","column4", "column5", "column6","column7"), show='headings')
            tree.heading("#1", text="USERNAME")
            tree.column('#1', width=100, anchor=tk.CENTER)
            tree.heading("#2", text="ID FLIGHT")
            tree.column('#2', width=100, anchor=tk.CENTER)
            tree.heading("#3", text="JENIS TIKET")
            tree.column('#3', width=140, anchor=tk.CENTER)
            tree.heading("#4", text="NOMOR KURSI")
            tree.column('#4', width=140, anchor=tk.CENTER)
            tree.heading("#5", text="NAMA PENUMPANG")
            tree.column('#5', width=140, anchor=tk.CENTER)
            tree.heading("#6", text="NO HP")
            tree.column('#6', width=140, anchor=tk.CENTER)
            tree.heading("#7", text="ID CARD")
            tree.column('#7', width=140, anchor=tk.CENTER)
            tree.pack()
            tree.place(x=38.3, y=169)
            
            user_id = self.username_entry2.get()
            checkPenerbangan = self.cursor.execute('SELECT username_pemesan, id_penerbangan, jenis_tiket, nomer_kursi, nama_pemesan, nomer_hp_pemesan, idcard_pemesan FROM pemesanan_pesawat WHERE username_pemesan=?', (user_id,))
            checked = self.cursor.fetchall()
            users = checked

            for row in users:
                print(row) 
                tree.insert("", tk.END, values=row)

            # Delete Option
            self.frame_menu3_tiketsaya = customtkinter.CTkFrame(self.app, bg_color='#4D421A', fg_color='#4D421A', width=400, height=200)
            self.frame_menu3_tiketsaya.place(x=38.3, y=359)
            self.login_label2 = customtkinter.CTkLabel(self.frame_menu3_tiketsaya,font=self.font1,text='HAPUS TIKET',text_color='#fff',bg_color='#4D421A')
            self.login_label2.place(x=115,y=10)
            username_pemesan_value = self.username_entry2.get()
            self.cursor.execute('SELECT id_penerbangan FROM pemesanan_pesawat WHERE username_pemesan=?', (username_pemesan_value,))
            flight_id_list = [row[0] for row in self.cursor.fetchall()]
            flight_id_list_pesantiket = ttk.Combobox(self.frame_menu3_tiketsaya, values=flight_id_list, font=self.font2, width=20)
            flight_id_list_pesantiket.place(x=20, y=60)
            flight_id_list_pesantiket.set("Select ID FLIGHT") 


            def update_treeview():
                for item in tree.get_children():
                    tree.delete(item)
                checkUsers = self.cursor.execute('SELECT username_pemesan, id_penerbangan, jenis_tiket, nomer_kursi, nama_pemesan, nomer_hp_pemesan, idcard_pemesan FROM pemesanan_pesawat WHERE username_pemesan=?', (user_id,))
                checked = self.cursor.fetchall()
                users = checked
                for row in users:
                    tree.insert("", tk.END, values=row)
                    
            def delete_record():
                id_value = flight_id_list_pesantiket.get()
                delete_tiket_value = self.username_entry2.get()

                try:
                    self.cursor.execute("DELETE FROM pemesanan_pesawat WHERE id_penerbangan=? AND username_pemesan=?", (id_value, delete_tiket_value))
                    self.conn.commit()
                    messagebox.showinfo("Success", "Record deleted successfully")
                    update_treeview()
                except Exception as e:
                    messagebox.showerror("Error", f"Error deleting record: {str(e)}")
                update_treeview()

            delete_button = customtkinter.CTkButton(self.frame_menu3_tiketsaya, text="Delete", font=self.font2, text_color='#fff', bg_color='#4D421A',
                                                    hover_color='#005940', command=delete_record)
            delete_button.place(x=20, y=100)

        button1.configure(command=menu1_action)
        button2.configure(command=menu2_action)
        button3.configure(command=menu3_action)

    def mainloop(self):
        self.app.mainloop()


if __name__ == "__main__":
    my_app = App()
    my_app.mainloop()