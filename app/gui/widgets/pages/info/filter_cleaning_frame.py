import os
from pathlib import Path
import ttkbootstrap as ttk

class FilterCleaningFrame(ttk.Frame):
    def __init__(self, parent: ttk.Frame) -> None:
        super().__init__(parent)
        self.build()
    
    def build(self) -> None:        
        title = "Cleaning"
        ttk.Label(self, text=title, font=("Helvetica", 30), bootstyle="info").pack(pady=20, padx=20)
        
        self.stats_image = ttk.PhotoImage(file=Path(os.getcwd() + "/app/assets/statistics_fields.png").resolve())
        ttk.Label(self, image=self.stats_image).pack(pady=20, padx=20)
        
        title = "Filtering"
        text = """
        Competition: Jupiler Pro League
        Team: KRC Genk
        Season: 2024-2025
        """
        ttk.Label(self, text=title, font=("Helvetica", 30), bootstyle="info").pack(pady=20, padx=20)
        ttk.Label(self, text=text, font=("Helvetica", 15)).pack(pady=20, padx=20)
        
        self.image = ttk.PhotoImage(file=Path(os.getcwd() + "/app/assets/filtering.png").resolve())
        ttk.Label(self, image=self.image).pack(pady=20, padx=20)
