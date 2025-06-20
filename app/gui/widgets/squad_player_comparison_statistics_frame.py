from matplotlib.figure import Figure
from pandas import DataFrame
import ttkbootstrap as ttk
from app.gui.widgets.auto_resizing_canvas import AutoResizingCanvas
from app.models.models import SquadPlayerComparison
from app.utils.statistics_data_provider import StatisticsDataProvider
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ttkbootstrap.scrolled import ScrolledFrame

class SquadPlayerComparisonStatisticsFrame(ScrolledFrame):
    def __init__(self, parent: ttk.Frame, data_provider: StatisticsDataProvider, comparison: SquadPlayerComparison) -> None:
        super().__init__(parent, height=1000, padding=50)
        self.data_provider: StatisticsDataProvider = data_provider
        
        self.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.build(comparison)
    
    def build(self, comparison: SquadPlayerComparison) -> None:
        df = self.data_provider.get_player_stats([
            comparison.squad_player_1.id,
            comparison.squad_player_2.id
        ])
        
        tabControl = ttk.Notebook(self)
        
        goals_per_90 = self.build_goals_per_90_frame(tabControl, df)
        goals_per_90.pack(fill=ttk.X, expand=ttk.YES)
        
        shots_per_90 = self.build_shots_per_90_block(tabControl, df)
        shots_per_90.pack(fill=ttk.X, expand=ttk.YES)
        
        shots_on_per_90 = self.build_shots_on_per_90_block(tabControl, df)
        shots_on_per_90.pack(fill=ttk.X, expand=ttk.YES)
        
        shots_on_pc = self.build_shots_on_pc_block(tabControl, df)
        shots_on_pc.pack(fill=ttk.X, expand=ttk.YES)
        
        dribbles_pc = self.build_dribbles_success_pc_frame(tabControl, df)
        dribbles_pc.pack(fill=ttk.X, expand=ttk.YES)
        
        duels = self.build_duels_won_pc_frame(tabControl, df)
        duels.pack(fill=ttk.X, expand=ttk.YES)
        
        passes_pc = self.build_passes_pc_frame(tabControl, df)
        passes_pc.pack(fill=ttk.X, expand=ttk.YES)
        
        tabControl.add(goals_per_90, text="Goals / 90")
        tabControl.add(shots_per_90, text="Shots / 90")
        tabControl.add(shots_on_per_90, text="Shots on / 90")
        tabControl.add(shots_on_pc, text="Shots on success %")
        tabControl.add(dribbles_pc, text="Dribbles success %")
        tabControl.add(duels, text="Duels won success %")
        tabControl.add(passes_pc, text="passes %")

        tabControl.pack(expand=ttk.YES, fill=ttk.BOTH)
        
    def build_goals_per_90_frame(self, parent: ttk.Frame, df: DataFrame) -> ttk.Frame:
        df_copy = df.copy()
        df_copy['gp90'] = (df_copy['goals.total'] / df_copy['games.minutes'])*90
        
        return self.generate_statistic_frame(
            parent,
            df_copy,
            "gp90",
            "Goals / 90 per Block",
            "Goals / 90"
        )
    
    def build_shots_per_90_block(self, parent: ttk.Frame, df: DataFrame) -> ttk.Frame:
        df_copy = df.copy()
        df_copy['shots_per_90'] = (df_copy['shots.total'] / df_copy['games.minutes'])*90
        
        return self.generate_statistic_frame(
            parent,
            df_copy,
            "shots_per_90",
            "Shots / 90 per Block",
            "Shots / 90"
        )
    
    def build_shots_on_per_90_block(self, parent: ttk.Frame, df: DataFrame) -> ttk.Frame:
        df_copy = df.copy()
        df_copy['shots_on_per_90'] = (df_copy['shots.on'] / df_copy['games.minutes'])*90
        
        return self.generate_statistic_frame(
            parent,
            df_copy,
            "shots_on_per_90",
            "Shots on / 90 per Block",
            "Shots on / 90"
        )

    def build_shots_on_pc_block(self, parent: ttk.Frame, df: DataFrame) -> ttk.Frame:
        df_copy = df.copy()
        df_copy['shots_on_pc'] = (df_copy['shots.on'] / df_copy['shots.total']) *100
        
        return self.generate_statistic_frame(
            parent,
            df_copy,
            "shots_on_pc",
            "Shots on % per Block",
            "Shots on %"
        )
        
    def build_dribbles_success_pc_frame(self, parent: ttk.Frame, df: DataFrame) -> ttk.Frame:
        df_copy = df.copy()
        df_copy['dribbles_success_pc'] = (df_copy['dribbles.success'] / df_copy['dribbles.attempts'])*100

        return self.generate_statistic_frame(
            parent,
            df_copy,
            "dribbles_success_pc",
            "Goals / 90 per Block",
            "Goals / 90"
        )
    
    def build_passes_pc_frame(self, parent: ttk.Frame, df: DataFrame) -> ttk.Frame:        
        df_copy = df.copy()
        df_copy['passes_success_percentage'] = (df_copy['passes.accuracy'] / df_copy['passes.total'])*100
        
        return self.generate_statistic_frame(
            parent,
            df_copy,
            "passes_success_percentage",
            "Passes Success % per Block",
            "Passes Success %"
        )

    def build_duels_won_pc_frame(self, parent: ttk.Frame, df: DataFrame) -> ttk.Frame:        
        df_copy = df.copy()
        df_copy['duels_won_percentage'] = (df_copy['duels.won'] / df_copy['duels.total'])*100
        
        return self.generate_statistic_frame(
            parent,
            df_copy,
            "duels_won_percentage",
            "Duels won % per Block",
            "Duels won %"
        )

    def build_frame(self, parent: ttk.Frame, figure: Figure):
        frame = ttk.Frame(parent)
        passes_frame = AutoResizingCanvas(frame, figure)
        passes_frame.pack(fill=ttk.X, expand=ttk.YES)
        frame.pack(fill=ttk.X, expand=ttk.YES, padx=20, pady=20)
        return frame

    def generate_statistic_frame(self, parent: ttk.Frame, df: DataFrame, field: str, title: str, field_name: str):        
        grouped_df = df.groupby(["player_id", "block"])
        
        agg_df = grouped_df.agg({
            "name": "first",
            field: "mean",
        }).reset_index()
        
        agg_df["rolling"] = (
            agg_df.groupby("player_id")[field]
                .rolling(window=3, min_periods=1)
                .mean()
                .reset_index(level=0, drop=True)
        )
        
        return self.build_frame(
            parent,
            self.build_figure(
                agg_df,
                field,
                title,
                field_name
            )
        )
        
    def build_figure(self, df: DataFrame, field: str, title, field_name: str) -> plt.Figure:
        fig, ax = plt.subplots(figsize=(3, 4))

        for name, group in df.groupby("name"):
            ax.plot(group["block"], group[field], marker="o", label=name)
            ax.plot(group["block"], group["rolling"], linestyle='--', label=f"{name} (rolling)")

        ax.set_title(title)
        ax.set_xlabel("Block")
        ax.set_ylabel(field_name)
        ax.legend(title="Player")
        ax.grid(True)
        fig.tight_layout()
        
        plt.close(fig)
        
        return fig