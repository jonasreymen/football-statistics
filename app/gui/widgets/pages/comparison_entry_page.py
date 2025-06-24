from app.gui.page_name import PageName
from app.gui.page_navigator_interface import PageNavigatorInterface
from app.gui.widgets.pages.page import Page
import ttkbootstrap as ttk

from app.gui.widgets.player_comparison_form import SquadPlayerComparisonForm

class ComparisonEntryPage(Page):
    def __init__(self, parent: ttk.Frame, session, navigator: PageNavigatorInterface) -> None:
        super().__init__(parent, name=PageName.COMPARISON_ENTRY_PAGE.value)
        self.session = session
        self.navigator = navigator
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
    
    def build(self, request_data: dict = {}) -> None:        
        frame = ttk.Frame(self, name="title_frame")
        ttk.Label(frame, text="Insert a comparison page").pack(pady=10, padx=10)
        frame.grid(column=0, row=0, sticky="nsew")
        
        self.build_form()
        
    def build_form(self) -> None:
        form = SquadPlayerComparisonForm(self, self.session, self.navigator)
        form.grid(row=1, column=0, sticky="nsew")