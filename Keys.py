import encryptor
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
from cryptography.fernet import Fernet
import os

class App:
    def __init__(self, master):
        self.master = master

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
                messagebox.showinfo("Key sucessfully exported to {}.".format(filename))

    def load_key(self):
        #Load a key from a file
        filename = filedialog.askopenfilename(defaultextension=".key")
        if not filename:
            return
        with open(filename, "rb") as f:
            self.key = f.read()
            messagebox.showinfo("Success", "Key has been loaded from {} .".format(filename))