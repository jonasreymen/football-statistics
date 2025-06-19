from typing import List
from sqlalchemy import bindparam, text
import pandas as pd
import numpy as np

class StatisticsDataProvider():
    def __init__(self, engine) -> None:
        self.engine = engine
        
    def get_player_stats(self, squad_players_ids: List[int] = []) -> pd.DataFrame:
        query = """
            SELECT p.id as "player_id", p.name, f.id as "fixture_id", st.statistic_type, fcsps.value as "value", f.date as "fixture_date", sp.type as "type_player", sp.role_group as "role_group"
            FROM fixture_player_statistic fcsps 
            INNER JOIN statistic_type st ON st.id = fcsps.statistic_type_id
            INNER JOIN squad_player sp ON sp.id = fcsps.squad_player_id
            INNER JOIN squad s On s.id = sp.squad_id
            INNER JOIN club c ON c.id = s.club_id
            INNER JOIN player p On p.id = sp.player_id
            INNER JOIN fixture_club_participation fcp ON fcp.id = fcsps.fixture_club_participation_id
            INNER JOIN fixture f ON f.id = fcp.fixture_id
            WHERE sp.`type` IS NOT NULL
            AND st.is_included_in_analysis is TRUE
        """
        
        params = {}
        
        if squad_players_ids:
            params["squad_player_ids"] = squad_players_ids
            query += " AND sp.id IN :squad_player_ids"
            
            query_text = text(query).bindparams(bindparam("squad_player_ids", expanding=True))
        else:
            query_text = text(query)
        
        df = pd.read_sql(query_text,con=self.engine, params=params)
        
        pivoted = df.pivot_table(
            index=["fixture_id", "fixture_date", "player_id", "name", "type_player", "role_group"],
            columns="statistic_type",
            values="value",
            aggfunc="first"
        ).reset_index()
        
        return self.enhance_df(pivoted)

    def enhance_df(self, df: pd.DataFrame) -> pd.DataFrame:
        sorted_df = df.sort_values(by=["fixture_date"])
        sorted_df['match_index'] = sorted_df.groupby(['player_id']).cumcount()
        sorted_df['block'] = (sorted_df['match_index'] // 5) + 1
        
        return sorted_df