import os
from app.gui.page_name import PageName
from app.gui.page_navigator import PageNavigator
from app.gui.widgets.pages.comparison_entry_page import ComparisonEntryPage
from app.gui.widgets.pages.comparison_statistic_detail_page import ComparisonStatisticDetailPage
from app.gui.widgets.pages.comparison_statistic_page import ComparisonStatisticPage
from app.gui.widgets.pages.general_statistic_page import GeneralStatisticPage
from app.gui.widgets.pages.page import Page
from app.gui.widgets.page_layout import PageLayout
from app.gui.widgets.page_root import PageRoot
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.gui.widgets.pages.info.information_page import InformationPage
from app.gui.widgets.pages.sync_page import SyncPage
from app.utils.statistics_data_provider import StatisticsDataProvider

class GuiApp():
    def __init__(self):
        self.engine = create_engine(os.getenv("DATABASE_CONNECTION"))
    
    def run(self) -> None:
        root = PageRoot()
        navigator = PageNavigator()
        
        page_layout = PageLayout(root, navigator)
        page_layout.grid(row=0, column=0, sticky="nsew")
        
        navigator.register_pages(self.generate_pages(page_layout.page_content, navigator))
        
        navigator.navigate(PageName.INFORMATION_PAGE.value)
        
        root.mainloop()
    
    def generate_pages(self, root: PageRoot, navigator: PageNavigator) -> list[Page]:
        session = self.create_session()
        statistics_data_provider = StatisticsDataProvider(self.engine)
        
        return [
            ComparisonEntryPage(root, session, navigator),
            GeneralStatisticPage(root, statistics_data_provider),
            ComparisonStatisticPage(root, session, navigator),
            ComparisonStatisticDetailPage(root, statistics_data_provider),
            SyncPage(root),
            
            # info pages
            InformationPage(root),
        ]
    
    def create_session(self) -> Session:
        Session = sessionmaker(bind=self.engine)
        return Session()