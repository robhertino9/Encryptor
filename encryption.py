from cryptography.fernet import Fernet
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
import random
import time

def __init__(self, app_instance):
    self.key = None
    self.filenames = None
    self.app = app_instance

def encrypt_file(self, filenames):
        ENCRYPTED_FILE_SIGNATURE = b"ENCRYPTED:" 
        #Error Handling
        if self.key is None:
            messagebox.showerror("Error", "Please generate a key.")
            return
        
        cipher_suite = Fernet(self.key) #Takes in 32-byte encryption key set's it to self.key
        
        self.show_progress_bar()
        self.progress_bar["value"] = 0
        self.progress_bar.update()
        for idx, filename in enumerate(self.filenames):
            if not os.path.isfile(filename):
                messagebox.showerror("Error", f"{filename} does not exist.")
                continue
            elif filename.startswith(ENCRYPTED_FILE_SIGNATURE.decode()):
                messagebox.showerror("Error", f"{filename} is already encrypted")
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
                #Progress bar
                self.progress_bar.lift()
                for i in range (1, 101):
                    self.progress_bar["value"] = i
                    self.progress_bar.update()
                    time.sleep(random.uniform(0.01, 0.05))
            messagebox.showinfo("Success", "The file has been encrypted.")
        self.hide_progress_bar()

def decrypt_file(self, filenames):
        ENCRYPTED_FILE_SIGNATURE = b"ENCRYPTED:" 
        #Error Handling
        if self.key is None:
            messagebox.showerror("Error", "Please generate or import a key.")
            return
        
        cipher_suite = Fernet(self.key)
        
        self.show_progress_bar()
        self.progress_bar["value"] = 0
        self.progress_bar.update()
        for idx,filename in enumerate(self.filenames):
            if not os.path.isfile(filename):
                messagebox.showerror("Error", f"{filenames} does not exist")
                continue
            with open(filename, "rb") as f:
                signature = f.read(len(ENCRYPTED_FILE_SIGNATURE))
                if signature != ENCRYPTED_FILE_SIGNATURE:
                    messagebox.showerror("Error", f"{filenames} is not encrypted")
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
                #Progress bar
                if signature == ENCRYPTED_FILE_SIGNATURE:
                    for i in range(1, 101):
                        self.progress_bar["value"] = i
                        self.progress_bar.update()
                        time.sleep(random.uniform(0.01, 0.05))
                    messagebox.showinfo("Success", "File has been decrypted and saved!")                
            self.hide_progress_bar()