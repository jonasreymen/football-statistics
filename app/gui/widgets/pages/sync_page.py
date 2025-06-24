from app.controllers.SynchronisationHandler import SynchronizationHandler
from app.gui.page_name import PageName
from app.gui.widgets.pages.page import Page
import ttkbootstrap as ttk
import sys
import threading

from app.utils.redirector import Redirector

class SyncPage(Page):
    def __init__(self, parent: ttk.Frame) -> None:
        super().__init__(parent, name=PageName.SYNCHRONISATION_PAGE.value)
    
    def build(self, request_data: dict = {}) -> None:        
        frame = ttk.Frame(self)
        
        btn = ttk.Button(
            frame,
            text="Start synchronisation",
            command=lambda: threading.Thread(target=self.start_synchronisation, daemon=True).start()
        )
        btn.grid(column=0, row=0,padx=10, pady=10)
        
        text_output = ttk.Text(frame, wrap='word', height=10, width=50)
        text_output.grid(column=0, row=1, padx=10, pady=10, sticky="nsew")
        
        # TODO add sync enablers from db fields competition_season and club fields: is_sync_enabled (checkboxes or search field or both)
        
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        self.grid_rowconfigure(0, weight=1)
        
        frame.grid(column=0, row=0,padx=10, pady=10, sticky="nsew")
        
        sys.stdout = Redirector(text_output)
    
    def start_synchronisation(self) -> None:
        sync = SynchronizationHandler()
        sync.run()