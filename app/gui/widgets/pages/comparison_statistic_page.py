from typing import List
from app.gui.page_name import PageName
from app.gui.page_navigator_interface import PageNavigatorInterface
from app.gui.widgets.pages.page import Page
import ttkbootstrap as ttk
from sqlalchemy.orm.session import Session

from app.models.models import SquadPlayerComparison

class ComparisonStatisticPage(Page):
    def __init__(self, parent: ttk.Frame, session, page_navigator: PageNavigatorInterface) -> None:
        super().__init__(parent, name=PageName.COMPARISON_STATISTIC_PAGE.value)
        self.session: Session = session
        self.page_navigator = page_navigator
        self.force_reload = True
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
    
    def build(self, request_data: dict = {}) -> None:
        self.show_buttons()
    
    def show_buttons(self) -> None:        
        frame = ttk.Frame(self)
        frame.grid(column=0, row=0, sticky="nsew")
        
        comparisons: List[SquadPlayerComparison] = self.session.query(SquadPlayerComparison).all()
        
        for key, comparison in enumerate(comparisons):
            button = ttk.Button(
                master=frame,
                text=f"{comparison.squad_player_1.player.name} vs {comparison.squad_player_2.player.name}",
                bootstyle="success",
                command=lambda comparison=comparison: self.page_navigator.navigate(PageName.COMPARISON_STATISTIC_DETAIL_PAGE.value, {"comparison": comparison})
            )
            button.grid(column=key % 3, row=key // 3, sticky="nsew", pady=30, padx=30)
            
            frame.grid_rowconfigure(key // 3, weight=1)
        
        for i in range(3):
            frame.grid_columnconfigure(i, weight=1)