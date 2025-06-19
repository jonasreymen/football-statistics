import ttkbootstrap as ttk
from typing import List
from sqlalchemy.orm.session import Session
from app.models.models import SquadPlayer

class SquadPlayerCombobox(ttk.Combobox):
    def __init__(self, parent, session, *args, **kwargs) -> None:
        self.session: Session = session
        
        self.items: dict = self.get_values()
        self.selected_value = ttk.StringVar()
        super().__init__(parent, values=list(self.items.keys()), textvariable=self.selected_value, *args, **kwargs)
    
    def get_values(self):# -> list:
        squadPlayers: List[SquadPlayer] = self.session.query(SquadPlayer).all()
        
        mapped = {}
        for squadPlayer in squadPlayers:
            player_name = f"{squadPlayer.player.name} - {squadPlayer.squad.season.name} ({squadPlayer.squad.club.name})"
            
            mapped[player_name] = squadPlayer.id
        return mapped
    
    def get(self):
        value = self.selected_value.get()
        
        return self.items[value]