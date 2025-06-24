import ttkbootstrap as ttk

class ConclusionFrame(ttk.Frame):
    def __init__(self, parent: ttk.Frame) -> None:
        super().__init__(parent)
        self.build()
    
    def build(self) -> None:        
        title = "Conclusie"
        ttk.Label(self, text=title, font=("Helvetica", 30), bootstyle="info").pack(pady=20, padx=20, anchor="w")

        ttk.Label(self, text="Attackers", font=("Helvetica", 15), bootstyle="info").pack(pady=(20, 5), padx=20, anchor="w")
        text = """
        Regular: Consistent, met een lichte opwaartse trend over het hele seizoen op bijna elke metric.
        Occasional: Volatiel — sterke start (goals & on target), maar geleidelijke daling naarmate het seizoen vordert.
        """
        ttk.Label(self, text=text, font=("Helvetica", 15), justify="left").pack(pady=(0, 20), padx=40, anchor="w")

        ttk.Label(self, text="Midfield", font=("Helvetica", 15), bootstyle="info").pack(pady=(10, 5), padx=20, anchor="w")
        text = """
        Regular: Consistent, met een lichte tot matige stijging.
        Occasional: Volatiel — goede start, maar afnemend richting het einde.

        Bijkomende observatie:
        Voor verschillende metrics (zoals passes en dribbles) zien we een duidelijke daling aan het einde van het seizoen bij beide groepen.
        """
        ttk.Label(self, text=text, font=("Helvetica", 15), justify="left").pack(pady=(0, 20), padx=40, anchor="w")

        ttk.Label(self, text="Defenders", font=("Helvetica", 15), bootstyle="info").pack(pady=(10, 5), padx=20, anchor="w")
        text = """
        Regular: Consistent, met een lichte tot matige stijging.
        Occasional: Zeer volatiel — prestaties schommelen sterk per match.

        Bijkomende observatie:
        Bij passes daalt het niveau richting het einde van het seizoen bij beide groepen.
        """
        ttk.Label(self, text=text, font=("Helvetica", 15), justify="left").pack(pady=(0, 20), padx=40, anchor="w")