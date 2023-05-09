import tkinter as tk
import time
import os
from PIL import ImageTk, Image

class SplashScreen(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.attributes("-topmost", True)
        self.overrideredirect(True)
        self.geometry("600x600")
        self.after(5000, self.close_splash_screen)
        self.logo = tk.PhotoImage(file="Images/splash.png")
        self.label = tk.Label(self, image=self.logo)
        self.label.place(relx=0.5, rely=0.5, anchor="center")
        
    def close_splash_screen(self):
        self.destroy()
        