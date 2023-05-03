from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
from cryptography.fernet import Fernet
from datetime import datetime
import tkinter as tk
import os


class App:
    def __init__(self, master):
        self.master = master
        master.title("File Encryption App")
        
        #Notebook widget for tabs
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill="both", expand=True)
        
        #Home Tab
        self.home_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.home_tab, text="Home")
        
        #Encrypt and Decrypt buttons at home tab
        self.home_label = Label(self.home_tab, text="Home", font=("Helvetica", 16))
        self.home_label.pack(pady=10)
        self.encrypt_button = Button(self.home_tab, text="Encrypt", font=("Helvetica", 10), command=lambda: self.notebook.select(self.encryption_tab))
        self.encrypt_button.pack(pady=10)
        self.decrypt_button = Button(self.home_tab, text="Decrypt", font=("Helvetica", 10), command=lambda: self.notebook.select(self.decryption_tab))
        self.decrypt_button.pack(pady=10)
        
        #Encryption tab
        self.encryption_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.encryption_tab, text="Encrypt")

        #Key label and buttons
        self.key_label = Label(self.encryption_tab, text="Keys", font=("Helvetica", 16))
        self.key_label.pack(pady=10)
        self.key_button = Button(self.encryption_tab, text="Generate Encryption Key", command=self.generate_key, font=("Helvetica", 9))
        self.key_button.pack(pady=5)
        self.key_export_button = Button(self.encryption_tab, text="Export Key", command=self.export_key, font=("Helvetica", 10))
        self.key_export_button.pack(pady=5)

        #File selection label and buttons
        self.file_label = Label(self.encryption_tab, text="File", font=("Helvetica", 16))
        self.file_label.pack(pady=10)
        self.file_select_button = Button(self.encryption_tab, text="Select File", command=self.select_file, font=("Helvetica", 10))
        self.file_select_button.pack(pady=5)
        self.encrypt_button = Button(self.encryption_tab, text="Encrypt File", command=self.encrypt_file, font=("Helvetica", 12))
        self.encrypt_button.pack(pady=5)
        
        # Initialization of the encryption key/file variable
        self.key = None
        self.filename = None
        
        #Decryption tab
        self.decryption_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.decryption_tab, text= "Decrypt")
        
        #Decryption key label and buttons
        self.decrypt_key_label = Label(self.decryption_tab, text="Decryption Key", font=("Helvetica", 16))
        self.decrypt_key_label.pack(pady=10)
        self.decrypt_key_button = Button(self.decryption_tab, text="Import Key", command=self.import_key, font=("Helvetica", 10))
        self.decrypt_key_button.pack(pady=5)
        
        #Decryption file selection label and buttons
        self.decrypt_file_label = Label(self.decryption_tab, text="Encrypted File", font=("Helvetica", 16))
        self.decrypt_file_label.pack(pady=10)
        self.decrypt_file_select_button = Button(self.decryption_tab, text="Select Encrypted File", command=self.select_file, font=("Helvetica", 10))
        self.decrypt_file_select_button.pack(pady=5)
        self.decrypt_button = Button(self.decryption_tab, text="Decrypt File", command=self.decrypt_file, font=("Helvetica", 12))
        self.decrypt_button.pack(pady=5)
        
        # Initialization of the decryption key/file variable
        self.key = None
        self.filename = None

    def generate_key(self):
        # Generate a random key for encryption
        self.key = Fernet.generate_key()
        messagebox.showinfo("Success", "A random key has been generated.")

    def export_key(self):
        # Export the key to a file
        if self.key is None:
            messagebox.showerror("Error", "Please generate a key.")
        else:
            filename = filedialog.asksaveasfilename(defaultextension=".key")
            if not filename:
                return
            with open(filename, "wb") as f:
                f.write(self.key)
                messagebox.showinfo("Success", "Key has been exported to {}".format(filename))
                
    def import_key(self):
        #File selection
        filename = filedialog.askopenfilename()
        
        #If user exits dialog do nothing
        if not filename:
            return
        
        #Read the key
        with open(filename, "rb") as f:
            key = f.read()
            
        #check if the key is valid
        try:
            Fernet(key)
        except:
            messagebox.showerror("Error", "Invalid key file")
            return
        
        #Key variable to imported key
        self.key = key
        messagebox.showinfo("Success", "Key has been imported from {}".format(filename))

    def select_file(self):
        # Show a file selection dialog
        self.filenames = filedialog.askopenfilenames()
        
    
    def encrypt_file(self):
        ENCRYPTED_FILE_SIGNATURE = b"ENCRYPTED:" 
        #Error Handling
        if self.key is None:
            messagebox.showerror("Error", "Please generate a key.")
            return
        if not hasattr(self, 'filenames') or not self.filenames:
            messagebox.showerror("Error", "Please one or more files.")
            return
        cipher_suite = Fernet(self.key)
        
        for filename in self.filenames:
            if not os.path.isfile(filename):
                messagebox.showerror("Error", "Selected file does not exist.")
                continue
            elif filename.startswith(ENCRYPTED_FILE_SIGNATURE.decode()):
                messagebox.showerror("Error", "Selected file is already encrypted!")
                continue
            # Encrypt the file using the key
            with open(filename, "rb") as f:
                plaintext = f.read()
            encrypted_text = cipher_suite.encrypt(plaintext)
            encrypted_text = ENCRYPTED_FILE_SIGNATURE + encrypted_text
            with open(filename, "wb") as f:
                f.write(encrypted_text)
                f.flush()
                os.fsync(f.fileno())
            messagebox.showinfo("Success", "The file has been encrypted.")

    def decrypt_file(self):
        ENCRYPTED_FILE_SIGNATURE = b"ENCRYPTED:" 
        #Error Handling
        if self.key is None:
            messagebox.showerror("Error", "Please generate a key.")
        if not hasattr(self, 'filenames') or not self.filenames:
            messagebox.showerror("Error", "Please one or more files.")
        else:
            cipher_suite = Fernet(self.key)
        for filename in self.filenames:
            if not os.path.isfile(filename):
                messagebox.showerror("Error", "Selected file does not exist")
                continue
            with open(filename, "rb") as f:
                signature = f.read(len(ENCRYPTED_FILE_SIGNATURE))
                if signature != ENCRYPTED_FILE_SIGNATURE:
                    messagebox.showerror("Error", "Selected file is not encrypted")
                    continue
            
            # Decrypt the file using the key
                encrypted_text = f.read()
            try:
                decrypted_text = cipher_suite.decrypt(encrypted_text)
            except:
                messagebox.showerror("Error", "Incorrect Decryption key, please try again!")
                return
            with open(filename, "wb") as f:
                f.write(decrypted_text)
                f.flush()
                os.fsync(f.fileno())
                messagebox.showinfo("Success", "File has been decrypted and saved!")
            
        
#Root window
root = Tk()

#Set size of window
root.geometry("400x400")
app = App(root)
root.mainloop()