import ttkbootstrap as ttk

from app.gui.page_name import PageName
from app.gui.page_navigator_interface import PageNavigatorInterface
from app.gui.widgets.navigating_button import NavigatingButton

class ToolbarBuilder():
    def __init__(self, page_navigator: PageNavigatorInterface, root) -> None:
        self.page_navigator = page_navigator
        self.root = root
    
    def build(self) -> None:
        self.root.grid_columnconfigure(0, weight=1)
        
        NavigatingButton(
            self.root,
            self.page_navigator,
            PageName.SYNCHRONISATION_PAGE.value,
            text="Synchronization"
        ).grid(sticky="nsew", pady=10, padx=10)
        
        NavigatingButton(
            self.root,
            self.page_navigator,
            PageName.COMPARISON_ENTRY_PAGE.value,
            text="Add a comparison entry"
        ).grid(sticky="nsew", pady=10, padx=10)
        
        NavigatingButton(
            self.root,
            self.page_navigator,
            PageName.COMPARISON_STATISTIC_PAGE.value,
            text="Comparison statistics"
        ).grid(sticky="nsew", pady=10, padx=10)
        
        NavigatingButton(
            self.root,
            self.page_navigator,
            PageName.GENERAL_STATISTIC_PAGE.value,
            text="General statistics"
        ).grid(sticky="nsew", pady=10, padx=10)