from enum import StrEnum

class PageName(StrEnum):
    COMPARISON_ENTRY_PAGE: str = "comparison_entry_page"
    COMPARISON_STATISTIC_PAGE: str = "comparison_statistic_page"
    COMPARISON_STATISTIC_DETAIL_PAGE: str = "comparison_statistic_detail_page"
    GENERAL_STATISTIC_PAGE: str = "general_statistic_page"
    SYNCHRONISATION_PAGE: str = "sync_page"