import random
import time
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
from cryptography.fernet import Fernet
from datetime import datetime
from PIL import ImageTk, Image
from splash_screen import SplashScreen
from encryption import encrypt_file, decrypt_file
from keys import generate_key, import_key, export_key
import tkinter as tk
import os

class App:
    def __init__(self, master):
        self.master = master
        master.title("SafeCryption")
        #Notebook widget for tabs
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill="both", expand=True)
        self.key = None
        self.filenames = []
        
        #SplashScreen to show logo before the app displays
        self.splash_screen = SplashScreen(master)
        self.master.after(5000, self.show_main_app)
        #SplashScreen attributes
    def show_main_app(self):
        self.splash_screen.close_splash_screen()
        self.master.attributes('-topmost', True)
        self.master.lift()
        self.master.focus_force()
        
        #Image objects
        img1 = Image.open(os.path.join("Images", "lock.png"))
        img1 = img1.resize((50, 50))
        self.encrypt_photo = ImageTk.PhotoImage(img1)
        
        img2 = Image.open(os.path.join("Images", "decryption.png"))
        img2 = img2.resize((50, 50))
        self.decryption_photo = ImageTk.PhotoImage(img2)
        
        img3 = Image.open(os.path.join("Images", "help.png"))
        img3 = img3.resize((50, 50))
        self.help_photo = ImageTk.PhotoImage(img3)
        
        img4 = Image.open(os.path.join("Images", "key.png"))
        img4 = img4.resize((50, 50))
        self.key_photo = ImageTk.PhotoImage(img4)
        
        img5 = Image.open(os.path.join("Images", "export.png"))
        img5 = img5.resize((50, 50))
        self.export_photo = ImageTk.PhotoImage(img5)
        
        img6 = Image.open(os.path.join("Images", "select.png"))
        img6 = img6.resize((50, 50))
        self.select_photo = ImageTk.PhotoImage(img6)
        
        img7 = Image.open(os.path.join("Images", "import.png"))
        img7 = img7.resize((50, 50))
        self.import_photo = ImageTk.PhotoImage(img7)
        
        #Font for tabs
        self.notebook_style = ttk.Style()
        self.notebook_style.configure('TNotebook.Tab', font=('Helvetica', 10, "bold"))
        
        #Home Tab
        self.home_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.home_tab, text="Home")
        self.home_label = Label(self.home_tab, text= "Welcome to SafeCryption", font= ("Helvetica", 16, "bold"),background='#ADD8E6')
        self.home_label.pack(pady=10)
        #Encrypt and Decrypt buttons at home tab
        self.encrypt_button = Button(self.home_tab, text="Encrypt", font=("Helvetica", 10, "bold"),height=70, width=100, image=self.encrypt_photo, compound="top", command=lambda: self.notebook.select(self.encryption_tab))
        self.encrypt_button.pack(pady=10, padx=25, side="left", anchor="n")
        self.decrypt_button = Button(self.home_tab, text="Decrypt", font=("Helvetica", 10, "bold"),height=70, width=100, image=self.decryption_photo, compound="top", command=lambda: self.notebook.select(self.decryption_tab))
        self.decrypt_button.pack(pady=10, padx=25, side="left", anchor="n")
        self.help_button = Button(self.home_tab, text="Help me", font=("Helvetica", 10, "bold"),height=70, width=100, image=self.help_photo, compound="top", command=lambda: self.notebook.select(self.help_tab))
        self.help_button.pack(pady=10, padx=25, side="left", anchor="n")   
        
        #Background colour of tabs
        new_style = ttk.Style()
        new_style.configure('TFrame', background='#ADD8E6')
        self.home_tab.style = new_style
        self.home_tab.configure(style='TFrame')     
        
        #Encryption tab
        self.encryption_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.encryption_tab, text="Encrypt")

        #Key label and buttons
        self.key_label = Label(self.encryption_tab, text="Keys", font=("Helvetica", 16, "bold"), background='#ADD8E6')
        self.key_label.pack(pady=10)
        self.key_button = Button(self.encryption_tab, text="Generate Encryption Key", command=self.generate_keys, font=("Helvetica", 10, "bold"), image=self.key_photo, compound="top")
        self.key_button.pack(pady=5)
        self.key_export_button = Button(self.encryption_tab, text="Export Key", command=self.export_keys, font=("Helvetica", 10, "bold"), width=160, image=self.export_photo, compound="top")
        self.key_export_button.pack(pady=5)

        #File selection label and buttons
        self.file_label = Label(self.encryption_tab, text="File", font=("Helvetica", 16, "bold"), background='#ADD8E6')
        self.file_label.pack(pady=10)
        self.file_select_button = Button(self.encryption_tab, text="Select File", command=self.select_file, font=("Helvetica", 10, "bold"), width=160, image=self.select_photo, compound="top")
        self.file_select_button.pack(pady=5)
        self.encrypt_button = Button(self.encryption_tab, text="Encrypt File", command=self.encrypt, font=("Helvetica", 12, "bold"),width=160, image=self.encrypt_photo, compound="top")
        self.encrypt_button.pack(pady=5)
        
        # Initialization of the encryption key/file variable
        self.key = None
        self.filenames = None
        
        #Decryption tab
        self.decryption_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.decryption_tab, text= "Decrypt")
        
        #Decryption key label and buttons
        self.decrypt_key_label = Label(self.decryption_tab, text="Decryption Key", font=("Helvetica", 16, "bold"), background='#ADD8E6')
        self.decrypt_key_label.pack(pady=10)
        self.decrypt_key_button = Button(self.decryption_tab, text="Import Key", command=self.import_keys, font=("Helvetica", 10, "bold") ,width=160, image=self.import_photo, compound="top")
        self.decrypt_key_button.pack(pady=5)
        
        #Decryption file selection label and buttons
        self.decrypt_file_label = Label(self.decryption_tab, text="Encrypted File", font=("Helvetica", 16), background='#ADD8E6')
        self.decrypt_file_label.pack(pady=10)
        self.decrypt_file_select_button = Button(self.decryption_tab, text="Select Encrypted File", command=self.select_file, font=("Helvetica", 10, "bold"), width=160, image=self.select_photo, compound="top")
        self.decrypt_file_select_button.pack(pady=5)
        self.decrypt_button = Button(self.decryption_tab, text="Decrypt File", command=self.decrypt, font=("Helvetica", 12, "bold"),width=160 , image=self.decryption_photo, compound="top")
        self.decrypt_button.pack(pady=5)
        
        # Initialization of the decryption key/file variable
        self.key = None
        self.filenames = None
        
        #Help Tab
        self.help_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.help_tab, text= "Help")
        
        #Help Menu
        self.help_label = Label(self.help_tab, text= "Help", font= ("Helvetica", 16, "bold"), background='#ADD8E6')
        self.help_label.pack(pady=10)
        self.help_var = StringVar()
        self.help_var.set("Q&A")
        self.help_dropdown = OptionMenu(self.help_tab, self.help_var, "What can I encrypt?", "I lost my encryption key", "Can I send encrypted files to people?",
                                        "Can I create my own encryption key","What is an encryption key?", "Is there a limit on the file size?", "How do I know if a file in encrypted?",
                                        command=self.update_help_answer)
        self.help_dropdown.pack(pady=10)
        
        #Widgets for help answers
        self.help_answer = Text(self.help_tab, width=60, height=10, borderwidth=2, relief="groove", font=("Helvetica", 12), padx=5, pady=5)
        self.help_answer.pack(pady=10)
        
    def update_help_answer(self, selection):
        self.help_answer.delete("1.0", END)
        
        if selection == "What can I encrypt?":
            answer = "You can encrypt any type of file, including text documents, images, videos, and more."
        elif selection == "I lost my encryption key":
            answer = "Unfortunately, if you lose your encryption key, there is no way to recover it. Make sure to export your encryption key when you are encrypting any file!"
        elif selection == "Can I send encrypted files to people?":
            answer = "Yes, you can send encrypted files to other people as long as they have the decryption key. Make sure to send the key securely to ensure the security of your files."
        elif selection == "Can I create my own encryption key":
            answer = "Yes, you can create your own encryption key using the 'Generate Encryption Key' button on the Encryption tab."
        elif selection == "What is an encryption key?":
            answer = "An encryption key is a sequence of characters used to encrypt and decrypt files. It is important to keep your key secure and not share it with anyone else."
        elif selection == "Is there a limit on the file size?":
            answer = "There is no limit on the size of files you can encrypt or decrypt, but larger files may take longer to process."
        elif selection == "How do I know if a file in encrypted?":
            answer = "If you try to open an encrypted file without the key, it will appear as gibberish."
        else:
            answer = ""
        
        self.help_answer.insert(END, answer)
        
    #Progress bar
    def show_progress_bar(self):
        self.progress_window = tk.Toplevel(self.master)
        self.progress_window.attributes('-topmost', True)
        self.progress_bar = ttk.Progressbar(self.progress_window, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=10)
    def hide_progress_bar(self):
        self.progress_window.destroy()
        
    def generate_keys(self):
        #Reference the Generate keys from keys
        generate_key(self)

    def export_keys(self):
        #Reference export key from keys
        export_key(self)
                
    def import_keys(self):
        #Reference import key from keys
        import_key(self)

    def select_file(self):
        # Show a file selection dialog
        self.filenames = filedialog.askopenfilenames()
    
    #Encryption
    def encrypt(self):
        if self.filenames:
            encrypt_file(self, self.filenames)

    #Decryption
    def decrypt(self):
        if self.filenames:
            decrypt_file(self, self.filenames)
            
        
#Root window
root = Tk()

#Set size of window
root.geometry("500x600")
app = App(root)
root.mainloop()