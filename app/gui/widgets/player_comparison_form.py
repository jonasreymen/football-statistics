import ttkbootstrap as ttk

from app.gui.page_name import PageName
from app.gui.page_navigator_interface import PageNavigatorInterface
from app.gui.widgets.squad_player_combobox import SquadPlayerCombobox
from app.models.models import SquadPlayer, SquadPlayerComparison
from sqlalchemy.orm.session import Session
from tkinter import messagebox

class SquadPlayerComparisonForm(ttk.Frame):
    def __init__(self, root, session, navigator: PageNavigatorInterface) -> None:
        super().__init__(root)
        self.session: Session = session
        self.navigator = navigator
        self.__init_widgets()
    
    def __init_widgets(self) -> None:
        SquadPlayerCombobox(self, self.session, name="player_1", width=100).pack(padx=20, pady=20)
        SquadPlayerCombobox(self, self.session, name="player_2", width=100).pack(padx=20, pady=20)
        ttk.Button(self, text="Save", command=lambda: self.save(), width=30).pack(padx=20, pady=20)
    
    def save(self) -> None:
        try:            
            player_1 = self.session.query(SquadPlayer).get(self.nametowidget("player_1").get())
            player_2 = self.session.query(SquadPlayer).get(self.nametowidget("player_2").get())
            
            comparison = SquadPlayerComparison()
            comparison.squad_player_1 = player_1
            comparison.squad_player_2 = player_2
            
            self.session.add(comparison)
            self.session.commit()
            
            self.navigator.navigate(
                PageName.COMPARISON_STATISTIC_DETAIL_PAGE.value,
                {"comparison": comparison}
            )
        except Exception as e:
            messagebox.showerror(e, e)