import ttkbootstrap as ttk
from app.gui.page_navigator_interface import PageNavigatorInterface
from app.gui.widgets.toolbar import ToolbarBuilder

class PageLayout(ttk.Frame):
    page_toolbar: ToolbarBuilder = None
    page_content: ttk.Frame = None
    
    def __init__(self, parent: ttk.Frame, page_navigator: PageNavigatorInterface) -> None:
        super().__init__(parent)
        self.page_navigator = page_navigator
        
        self.__configure_grid()
        self.build()
    
    def build(self) -> None:
        self.page_toolbar = self.build_toolbar()
        self.page_content = self.build_page_content()
    
    def build_toolbar(self) -> None:
        frame = ttk.Frame(self, bootstyle="secondary")
        
        toolbar = ToolbarBuilder(self.page_navigator, frame)
        toolbar.build()
        
        frame.grid(row=0, column=0, sticky="nsew")
        
        return toolbar
    
    def build_page_content(self) -> None:
        frame = ttk.Frame(self, name="content_frame")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid(row=0, column=1, sticky="nsew")
        
        return frame
    
    def __configure_grid(self) -> None:
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0, minsize=300)
        self.grid_columnconfigure(1, weight=1, minsize=750)