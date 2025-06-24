from app.gui.page_name import PageName
from app.gui.widgets.general_statistics_frame import GeneralStatisticsFrame
from app.gui.widgets.pages.page import Page
import ttkbootstrap as ttk
from app.utils.statistics_data_provider import StatisticsDataProvider

class GeneralStatisticPage(Page):    
    def __init__(self, parent: ttk.Frame, statistics_data_provider) -> None:
        super().__init__(parent, name=PageName.GENERAL_STATISTIC_PAGE.value)
        self.data_provider: StatisticsDataProvider = statistics_data_provider
    
    def build(self, request_data: dict = {}) -> None:
        title_frame = ttk.Frame(self, name="title_frame")
        ttk.Label(title_frame, text="General statistics").pack(pady=10, padx=10)
        title_frame.grid(column=0, row=0, sticky="ew")
        
        statistics_frame = GeneralStatisticsFrame(self, self.data_provider)
        statistics_frame.grid_columnconfigure(0, weight=1)        
        statistics_frame.grid(column=0, row=1, sticky="nsew")
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)