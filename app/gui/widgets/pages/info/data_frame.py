import ttkbootstrap as ttk

class DataFrame(ttk.Frame):
    def __init__(self, parent: ttk.Frame) -> None:
        super().__init__(parent)
        self.build()
    
    def build(self) -> None:        
        title = "Data"
        text = """
        Season: start, end
        Club: name
        Competition: name, type
        Player: name, firstname, lastname, birth, photo_url
        Statistics: type, value
        Fixture: date, teams, type(Home, Away)
        
        Statistics types:
            - shots.on
            - shots.total
            - passes.total
            - passes.accuracy
            - dribbles.attempts
            - dribbles.success
            - duels.total
            - duels.won
            - games.minutes
            - goals.total
        """
        ttk.Label(self, text=title, font=("Helvetica", 30), bootstyle="info").pack(pady=20, padx=20)
        ttk.Label(self, text=text, font=("Helvetica", 15)).pack(pady=20, padx=20)
    