from abc import ABC, abstractmethod
import ttkbootstrap as ttk
from app.gui.widgets.page_interface import PageInterface

class Page(ttk.Frame, PageInterface, ABC):
    def __init__(self, parent: ttk.Frame, name: str) -> None:
        super().__init__(parent, name=name)
        self.name = name
        self.is_build = False
        self.force_reload = False
    
    @abstractmethod
    def build(self, data: dict = {}) -> None:
        pass
    
    def load(self, data: dict = {}) -> None:
        if self.is_build is False or self.force_reload is True:
            self.build(data)
            self._configure_grid()
            self.is_build = True
        self.tkraise()
    
    def _configure_grid(self) -> None:
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1, minsize=750)
        self.grid(row=0, column=0, sticky="nsew")