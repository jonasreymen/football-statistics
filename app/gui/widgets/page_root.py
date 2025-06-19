import ttkbootstrap as ttk

class PageRoot(ttk.Window):
    def __init__(self) -> None:
        super().__init__(themename="darkly")
        
        self.minsize(width=1000, height=1000)

        self.title("Football statistics")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)