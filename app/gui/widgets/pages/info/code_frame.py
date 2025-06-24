import os
from pathlib import Path
import ttkbootstrap as ttk

class CodeFrame(ttk.Frame):
    def __init__(self, parent: ttk.Frame) -> None:
        super().__init__(parent)
        self.build()
    
    def build(self) -> None:        
        title = "Code"
        ttk.Label(self, text=title, font=("Helvetica", 30), bootstyle="info").grid(row=0, column=0, pady=20, padx=20, columnspan=2)
        
        self.sync_image = ttk.PhotoImage(file=Path(os.getcwd() + "/app/assets/synchronization.png").resolve())
        ttk.Label(self, image=self.sync_image).grid(row=1, column=0, pady=20, padx=20, sticky="n")
        
        self.nav_image = ttk.PhotoImage(file=Path(os.getcwd() + "/app/assets/navigation.png").resolve())
        ttk.Label(self, image=self.nav_image).grid(row=1, column=1, pady=20, padx=20, sticky="n")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)