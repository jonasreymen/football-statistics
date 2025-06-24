import ttkbootstrap as ttk

class SourceFrame(ttk.Frame):
    def __init__(self, parent: ttk.Frame) -> None:
        super().__init__(parent)
        self.build()
    
    def build(self) -> None:        
        title = "Bronnen"
        text = """
        Data source: https://www.api-football.com/ 
        Type data: API - application/json
        Endpoints:
            /leagues
            /seasons
            /teams (league - season)
            /players (team - season - league)
            /fixtures (fixtures - season - team - league)
            /fixtures/players (fixture)
        """
        ttk.Label(self, text=title, font=("Helvetica", 30), bootstyle="info").pack(pady=20, padx=20)
        ttk.Label(self, text=text, font=("Helvetica", 15)).pack(pady=20, padx=20)
    