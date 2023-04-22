from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
import tkinter as tk
from cryptography.fernet import Fernet
class App:
    def __init__(self, master):
        self.master = master
        master.title("File Encryption App")

        # Create the key label and buttons
        self.key_label = Label(master, text="Key:")
        self.key_label.pack()
        self.key_button = Button(master, text="Generate Key", command=self.generate_key)
        self.key_button.pack()
        self.key_export_button = Button(master, text="Export Key", command=self.export_key)
        self.key_export_button.pack()

        # Create the file selection label and buttons
        self.file_label = Label(master, text="File:")
        self.file_label.pack()
        self.file_select_button = Button(master, text="Select File", command=self.select_file)
        self.file_select_button.pack()
        self.encrypt_button = Button(master, text="Encrypt File", command=self.encrypt_file)
        self.encrypt_button.pack()
        self.decrypt_button = Button(master, text="Decrypt File", command=self.decrypt_file)
        self.decrypt_button.pack()

        # Initialize the key variable
        self.key = None

        # Initialize the file variable
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
            with open(filename, "wb") as f:
                f.write(self.key)
            messagebox.showinfo("Success", "The key has been exported to {}.".format(filename))

    def select_file(self):
        # Show a file selection dialog
        self.filename = filedialog.askopenfilename()

    def encrypt_file(self):
        if self.key is None:
            messagebox.showerror("Error", "Please generate a key.")
        elif self.filename is None:
            messagebox.showerror("Error", "Please select a file.")
        else:
            # Encrypt the file using the key
            cipher_suite = Fernet(self.key)
            with open(self.filename, "rb") as f:
                plaintext = f.read()
            encrypted_text = cipher_suite.encrypt(plaintext)
            with open(self.filename, "wb") as f:
                f.write(encrypted_text)
            messagebox.showinfo("Success", "The file has been encrypted.")

    def decrypt_file(self):
        if self.key is None:
            messagebox.showerror("Error", "Please generate a key.")
        elif self.filename is None:
            messagebox.showerror("Error", "Please select a file.")
        else:
            # Decrypt the file using the key
            cipher_suite = Fernet(self.key)
            with open(self.filename, "rb") as f:
                encrypted_text = f.read()
            decrypted_text = cipher_suite.decrypt(encrypted_text)
            with open(self.filename, "wb") as f:
                f.write(decrypted_text)
            messagebox.showinfo("Success", "File has been decrypted!")
            
#Root window
root = Tk()
#Set size of window
root.geometry("800x600")
app = App(root)
root.mainloop()