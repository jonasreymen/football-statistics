from io import BytesIO
import ttkbootstrap as ttk
import requests
from PIL import Image, ImageTk
from app.models.models import Club, Player, Season, Squad, SquadPlayer, SquadPlayerComparison

class SquadPlayerComparisonInfoFrame(ttk.Frame):
    def __init__(self, parent: ttk.Frame, comparison: SquadPlayerComparison) -> None:
        super().__init__(parent)
        
        self.build(comparison)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
    
    def build(self, comparison: SquadPlayerComparison) -> None:
        player_1 = self.build_player_block(comparison.squad_player_1)
        player_1.grid(column=0, row=0, sticky="nsew")
        
        ttk.Label(self, text=f"VS").grid(column=1, row=0, sticky="nsew")
        
        player_2 = self.build_player_block(comparison.squad_player_2)
        player_2.grid(column=2, row=0, sticky="nsew")
    
    def build_player_block(self, squad_player: SquadPlayer) -> ttk.Frame:
        frame = ttk.Frame(self)
        
        player: Player = squad_player.player
        squad: Squad = squad_player.squad
        club: Club = squad.club
        season: Season = squad.season
        
        self.build_image_block(player.photo_url, frame).pack(padx=10, pady=10)
        ttk.Label(frame, text=f"{player.firstname} {player.lastname}").pack(pady=10, padx=10)
        ttk.Label(frame, text=f"{club.name}").pack(pady=10, padx=10)
        ttk.Label(frame, text=f"Season {season.name}-{season.end}").pack(pady=10, padx=10)
    
        return frame

    def build_image_block(self, url: str, parent: ttk.Frame) -> ttk.Label:
        response = requests.get(url)
        image_data = BytesIO(response.content)
        
        image = Image.open(image_data)
        photo = ImageTk.PhotoImage(image)
        
        # this is really strange to do it like this
        label = ttk.Label(parent, image=photo)
        label.image = photo
        
        return label