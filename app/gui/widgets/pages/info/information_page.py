from app.gui.page_name import PageName
from app.gui.widgets.pages.info.code_statistics_frame import CodeStatisticsFrame
from app.gui.widgets.pages.page import Page
import ttkbootstrap as ttk
from app.gui.widgets.pages.info.casus_frame import CasusFrame
from app.gui.widgets.pages.info.code_frame import CodeFrame
from app.gui.widgets.pages.info.conclusion_frame import ConclusionFrame
from app.gui.widgets.pages.info.data_frame import DataFrame
from app.gui.widgets.pages.info.filter_cleaning_frame import FilterCleaningFrame
from app.gui.widgets.pages.info.source_frame import SourceFrame

class InformationPage(Page):
    def __init__(self, parent: ttk.Frame) -> None:
        super().__init__(parent, name=PageName.INFORMATION_PAGE.value)
        
        self.slides = [
            {
                "name": "Casus",
                "widget": CasusFrame
            },
            {
                "name": "Source",
                "widget": SourceFrame
            },
            {
                "name": "Data",
                "widget": DataFrame
            },
            {
                "name": "Filtering / cleaning",
                "widget": FilterCleaningFrame
            },
            {
                "name": "Code",
                "widget": CodeFrame
            },
            {
                "name": "Code statistics",
                "widget": CodeStatisticsFrame
            },
            {
                "name": "Conclusion",
                "widget": ConclusionFrame
            },
        ]
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)
        
        self.slide_navigation = ttk.Frame(self, padding=20, bootstyle="secondary")
        self.slide_content = ttk.Frame(self)
        self.button_frame = ttk.Frame(self, padding=20, bootstyle="secondary")
        
        self.slide_content.grid_rowconfigure(0, weight=1)
        self.slide_content.grid_columnconfigure(0, weight=1)
        
        self.current = None
    
    def build(self, request_data: dict = {}) -> None:
        self.slide_navigation.grid(column=0, row=0, sticky="nsew")
        self.slide_content.grid(column=0, row=1, sticky="nsew")
        self.button_frame.grid(column=0, row=2, sticky="nsew")
        
        self.build_navigation()
        
        self.navigate(self.slides[0])
    
    def build_navigation(self):
        for i, slide in enumerate(self.slides):
            button = ttk.Button(self.slide_navigation, command=lambda slide=slide: self.navigate(slide), text=slide["name"], bootstyle="info-outline")
            button.grid(row=0, column=i, padx=20)

    def navigate(self, slide: dict):
        self.clear_frame(self.slide_content)
        
        self.current = slide
        frame: ttk.Frame = slide["widget"](self.slide_content)        
        frame.grid(row=0, column=0, sticky="nsew")
        
        self.build_button_frame(slide)
    
    def build_button_frame(self, slide):
        self.clear_frame(self.button_frame)

        # Create left and right "zones"
        left_frame = ttk.Frame(self.button_frame, bootstyle="secondary")
        right_frame = ttk.Frame(self.button_frame, bootstyle="secondary")

        left_frame.pack(side=ttk.LEFT, fill=ttk.X, expand=True)
        right_frame.pack(side=ttk.RIGHT, fill=ttk.X, expand=True)

        current_index = self.slides.index(slide)

        if current_index > 0:
            previous_slide = self.slides[current_index - 1]
            button = ttk.Button(
                left_frame,
                command=lambda: self.navigate(previous_slide),
                text=f"{previous_slide['name']}",
                bootstyle="warning-outline",
                width=25
            )
            button.pack(anchor="w", padx=20)

        if current_index < len(self.slides) - 1:
            next_slide = self.slides[current_index + 1]
            button = ttk.Button(
                right_frame,
                command=lambda: self.navigate(next_slide),
                text=f"{next_slide['name']}",
                bootstyle="success",
                width=25
            )
            button.pack(anchor="e", padx=20)
    
    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()