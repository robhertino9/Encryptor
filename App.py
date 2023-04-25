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
        self.notebook.pack(fill=BOTH, expand=True)
        
        #Create encryption tab
        self.encryption_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.encryption_tab, text="Encrypt")

        # Create the key label and buttons
        self.key_label = Label(self.encryption_tab, text="Keys", font=("Helvetica", 16))
        self.key_label.pack(pady=10)
        self.key_button = Button(self.encryption_tab, text="Generate Encryption Key", command=self.generate_key, font=("Helvetica", 9))
        self.key_button.pack(pady=5)
        self.key_export_button = Button(self.encryption_tab, text="Export Key", command=self.export_key, font=("Helvetica", 10))
        self.key_export_button.pack(pady=5)

        # Create the file selection label and buttons
        self.file_label = Label(self.encryption_tab, text="File", font=("Helvetica", 16))
        self.file_label.pack(pady=10)
        self.file_select_button = Button(self.encryption_tab, text="Select File", command=self.select_file, font=("Helvetica", 10))
        self.file_select_button.pack(pady=5)
        self.encrypt_button = Button(self.encryption_tab, text="Encrypt File", command=self.encrypt_file, font=("Helvetica", 12))
        self.encrypt_button.pack(pady=5)
        
        # Initialize the encryption key variable
        self.key = None

        # Initialize the encryption file variable
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
        
        # Initialize the decryption key variable
        self.key = None

        # Initialize the decryption file variable
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
        self.filename = filedialog.askopenfilename()
    
    def encrypt_file(self):
        #Error Handling
        if self.key is None:
            messagebox.showerror("Error", "Please generate a key.")
        elif self.filename is None:
            messagebox.showerror("Error", "Please select a file.")
        elif not os.path.isfile(self.filename):
            messagebox.showerror("Error", "Selected file does not exist.")
        elif self.filename.endswith(".encrypted"):
            messagebox.showerror("Error", "Selected file is already encrypted!")
        else:
            # Encrypt the file using the key
            cipher_suite = Fernet(self.key)
            with open(self.filename, "rb") as f:
                plaintext = f.read()
            encrypted_text = cipher_suite.encrypt(plaintext)
            with open(self.filename + ".encrypted", "wb") as f:
                f.write(encrypted_text)
            messagebox.showinfo("Success", "The file has been encrypted.")

    def decrypt_file(self):
        #Error Handling
        if self.key is None:
            messagebox.showerror("Error", "Please generate a key.")
        elif self.filename is None:
            messagebox.showerror("Error", "Please select a file.")
        elif not os.path.isfile(self.filename):
            messagebox.showerror("Error", "Selected file does not exist")
        elif not self.filename.endswith(".encrypted"):
            messagebox.showerror("Error", "Selected file is not encrypted")
        else:
            # Decrypt the file using the key
            cipher_suite = Fernet(self.key)
            with open(self.filename, "rb") as f:
                encrypted_text = f.read()
            decrypted_filename =  datetime.now().strftime("%Y%m%d_") + os.path.basename(os.path.splitext(self.filename)[0])
            try:
                decrypted_text = cipher_suite.decrypt(encrypted_text)
            except:
                messagebox.showerror("Error", "Incorrect Decryption key, please try again!")
                return
            #Ask user where they want the decrypted file to be saved
            filetypes = [('All files', '*.*')]
            initial_dir = os.path.expanduser('~/Documents')
            save_file_path = filedialog.asksaveasfilename(filetypes=filetypes, initialdir=initial_dir, initialfile=decrypted_filename)
            if save_file_path:
                with open(decrypted_filename, "wb") as f:
                 f.write(decrypted_text)
                messagebox.showinfo("Success", "File has been decrypted and saved!")
            else:
                 messagebox.showerror("Error", "Please choose a valid file path!")
            
        
#Root window
root = Tk()

#Set size of window
root.geometry("400x400")
app = App(root)
root.mainloop()