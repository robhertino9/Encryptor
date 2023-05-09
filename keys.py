from tkinter import messagebox, filedialog
from cryptography.fernet import Fernet
    
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