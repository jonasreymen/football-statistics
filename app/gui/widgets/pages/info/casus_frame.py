from turtle import color
from numpy import size
import ttkbootstrap as ttk

class CasusFrame(ttk.Frame):
    def __init__(self, parent: ttk.Frame) -> None:
        super().__init__(parent)
        
        self.build()
    
    def build(self) -> None:        
        title = "Onderzoeksvraag"
        text = """
        Hoe evolueren de technische en tactische prestaties van voetballers gedurende een seizoen,
        en hoe verschillen deze evoluties tussen basisspelers en spelers met beperkte speelfrequentie?
        """
        ttk.Label(self, text=title, font=("Helvetica", 30), bootstyle="info").pack(pady=20, padx=20)
        ttk.Label(self, text=text, font=("Helvetica", 15)).pack(pady=20, padx=20)
        
        title = "Hypothetische uitkomst"
        text = """
        Je zou verwachten dat basisspelers een meer positieve evolutie zullen ervaren dan spelers die minder
        frequent op het veld staan. Spelers die minder frequent op het plein staan zijn wisselvalliger en
        presteren net iets minder waardoor hun groei pas later op het seizoen merkbaar zal zijn.
        """
        ttk.Label(self, text=title, font=("Helvetica", 30), bootstyle="info").pack(pady=20, padx=20)
        ttk.Label(self, text=text, font=("Helvetica", 15)).pack(pady=20, padx=20)