import ttkbootstrap as ttk

class CodeStatisticsFrame(ttk.Frame):
    def __init__(self, parent: ttk.Frame) -> None:
        super().__init__(parent)
        self.build()
    
    def build(self) -> None:        
        title = "Statistics code"
        ttk.Label(self, text=title, font=("Helvetica", 30), bootstyle="info").grid(row=0, column=0, pady=20, padx=20, columnspan=3, sticky="n")
        
        comparison_code = """
        df = df.sort_values(by=["fixture_date"])
        df['match_index'] = df.groupby(['player_id']).cumcount()
        df['block'] = (df['match_index'] // 5) + 1
        
        df['gp90'] = (df['goals.total'] / df['games.minutes'])*90
        
        grouped_df = df.groupby(["player_id", "block"])
        
        agg_df = grouped_df.agg({
            "name": "first",
            "gp90": "mean",
        }).reset_index()
        
        agg_df["rolling"] = (
            agg_df.groupby("player_id")["gp90"]
                .rolling(window=3, min_periods=1)
                .mean()
                .reset_index(level=0, drop=True)
        )
        """
        ttk.Label(self, text="Squad player comparison", bootstyle="info").grid(row=1, column=0, sticky="n")
        ttk.Label(self, text=comparison_code, justify="left", anchor="w").grid(row=2, column=0, pady=20, padx=20, sticky="n")
        
        
        general_linregr = """
        df = df.sort_values(by=["fixture_date"])
        
        grouped_df = df.groupby(['role_group', 'type_player', "player_id"])
        
        df['cumulative_minutes'] = grouped_df['games.minutes'].cumsum()
        df['cumulative_goals'] = grouped_df['goals.total'].cumsum()
        df['cumulative_goals_per_1'] = df['cumulative_goals'] / df['cumulative_minutes']
        df['cumulative_goals_per_90'] = df['cumulative_goals_per_1']*90
        df['match_index'] = grouped_df.cumcount()
        """
        ttk.Label(self, text="General statistics (lineair regression)", bootstyle="info").grid(row=1, column=1, sticky="n")
        ttk.Label(self, text=general_linregr, justify="left", anchor="w").grid(row=2, column=1, pady=20, padx=20, sticky="n")
        
        
        general_line = """
        df = df.sort_values(by=["fixture_date"])
        
        df['gpm'] = df['goals.total'] / df['games.minutes']
        df['gp90'] = df['gpm']*90
        
        df["rolling_gpm"] = (
            df.groupby("player_id")["gp90"]
                .rolling(window=5, min_periods=1)
                .mean()
                .reset_index(level=0, drop=True)
        )
        
        groups_df = df.groupby([
            'role_group',
            'type_player',
            'fixture_date'
        ])["rolling_gpm"].mean().reset_index()
        filtered_df = groups_df.dropna(subset=["rolling_gpm"])
        """
        ttk.Label(self, text="General statistics (line)", bootstyle="info").grid(row=1, column=2, sticky="n")
        ttk.Label(self, text=general_line, justify="left", anchor="w").grid(row=2, column=2, pady=20, padx=20, sticky="n")

        self.grid_columnconfigure(0, weight=1, minsize=400)
        self.grid_columnconfigure(1, weight=1, minsize=400)
        self.grid_columnconfigure(2, weight=1, minsize=400)