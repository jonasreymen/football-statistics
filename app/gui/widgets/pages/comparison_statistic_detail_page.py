from app.gui.page_name import PageName
from app.gui.widgets.pages.page import Page
import ttkbootstrap as ttk
from app.gui.widgets.squad_player_comparison_info_frame import SquadPlayerComparisonInfoFrame
from app.gui.widgets.squad_player_comparison_statistics_frame import SquadPlayerComparisonStatisticsFrame
from app.models.models import SquadPlayerComparison
from app.utils.statistics_data_provider import StatisticsDataProvider

class ComparisonStatisticDetailPage(Page):
    def __init__(self, parent: ttk.Frame, data_provider) -> None:
        super().__init__(parent, name=PageName.COMPARISON_STATISTIC_DETAIL_PAGE.value)
        self.data_provider: StatisticsDataProvider = data_provider
        self.force_reload = True
    
    def build(self, request_data: dict = {}) -> None:
        assert("comparison" in request_data)
        assert(isinstance(request_data["comparison"], SquadPlayerComparison))
        
        comparison: SquadPlayerComparison = request_data["comparison"]
        
        SquadPlayerComparisonInfoFrame(self, comparison).grid(column=0, row=0, sticky="nsew")
        
        statistics_frame = SquadPlayerComparisonStatisticsFrame(
            self,
            self.data_provider,
            comparison
        )
        statistics_frame.grid(column=0, row=1, sticky="nsew")
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)