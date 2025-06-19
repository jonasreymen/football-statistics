from pandas import DataFrame
import ttkbootstrap as ttk
from app.gui.widgets.auto_resizing_canvas import AutoResizingCanvas
from app.utils.statistics_data_provider import StatisticsDataProvider
import matplotlib.pyplot as plt
from ttkbootstrap.scrolled import ScrolledFrame
import seaborn as sns

class GeneralStatisticsFrame(ScrolledFrame):
    def __init__(self, parent: ttk.Frame, data_provider: StatisticsDataProvider) -> None:
        super().__init__(parent, height=1000, padding=50)
        self.enable_scrolling()
        
        self.data_provider: StatisticsDataProvider = data_provider
        self.colors = {
            "occasional": "blue",
            "regular": "orange"
        }
        
        self.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)
        self.build()
    
    def build(self) -> None:
        df = self.data_provider.get_player_stats()
        
        tabControl = ttk.Notebook(self)
        
        goals = self.build_goals_per_90_frame(df, tabControl)
        goals.pack(fill=ttk.X, expand=ttk.YES)
        
        shots_per_90 = self.build_shots_per_90_frame(df, tabControl)
        shots_per_90.pack(fill=ttk.X, expand=ttk.YES)
        
        shots_on = self.build_shots_on_frame(df, tabControl)
        shots_on.pack(fill=ttk.X, expand=ttk.YES)
        
        shots_on_pc = self.build_shots_on_pc_frame(df, tabControl)
        shots_on_pc.pack(fill=ttk.X, expand=ttk.YES)
        
        dribbles = self.build_dribbles_success_frame(df, tabControl)
        dribbles.pack(fill=ttk.X, expand=ttk.YES)
        
        duels = self.build_duels_won_pc_frame(df, tabControl)
        duels.pack(fill=ttk.X, expand=ttk.YES)
        
        passes = self.build_passes_success_frame(df, tabControl)
        passes.pack(fill=ttk.X, expand=ttk.YES)
        
        tabControl.add(goals, text="Goals / 90")
        tabControl.add(shots_per_90, text="Shots / 90")
        tabControl.add(shots_on, text="Shots on / 90")
        tabControl.add(shots_on_pc, text="Shots on success %")
        tabControl.add(dribbles, text="Dribbles success %")
        tabControl.add(duels, text="Duels won success %")
        tabControl.add(passes, text="Passes success %")

        tabControl.pack(expand=ttk.YES, fill=ttk.BOTH)
    
    def build_goals_per_90_frame(self, df: DataFrame, parent) -> ttk.Frame:
        goals_90_growth_frame = self.get_goals_per_90_growth_figures(df)
        cumulative_goals_per_90_frame = self.get_cumulative_goals_per_90_figures(df)
        
        return self.build_matching_frame_blocks(parent, goals_90_growth_frame, cumulative_goals_per_90_frame)
    
    def build_matching_frame_blocks(self, parent, mapped_growth_figures, mapped_linregr_figures):
        roles = mapped_growth_figures.keys() | mapped_linregr_figures.keys()
        
        frame = ttk.Frame(parent)
        for i,role in enumerate(roles):
            canvas_wrapper = AutoResizingCanvas(frame, mapped_growth_figures[role])
            canvas_wrapper.grid(row=i, column=0, sticky="nsew", pady=20, padx=20)
            
            canvas_wrapper = AutoResizingCanvas(frame, mapped_linregr_figures[role])
            canvas_wrapper.grid(row=i, column=1, sticky="nsew", pady=20, padx=20)
        
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        
        return frame
    
    def build_shots_per_90_frame(self, df:DataFrame, parent: ttk.Frame) -> ttk.Frame:
        shots_per_90_growth_frame = self.get_shots_per_90_growth_figures(df)
        cumulative_shots_90_frame = self.get_cumulative_shots_per_90_figures(df)
        
        return self.build_matching_frame_blocks(parent, shots_per_90_growth_frame, cumulative_shots_90_frame)
    
    def build_shots_on_frame(self, df: DataFrame, parent: ttk.Frame) -> ttk.Frame:
        shots_on_per_90_growth_frame = self.get_shots_on_per_90_growth_figures(df)        
        cumulative_shots_on_per_90_frame = self.get_cumulative_shots_on_per_90_figures(df)
        
        return self.build_matching_frame_blocks(parent, shots_on_per_90_growth_frame, cumulative_shots_on_per_90_frame)
    
    def build_shots_on_pc_frame(self, df: DataFrame, parent: ttk.Frame):
        shots_on_pc_growth_frame = self.get_shots_on_pc_growth_figures(df)
        cumulative_shots_on_pc_frame = self.get_cumulative_shots_on_pc_figures(df)
        
        return self.build_matching_frame_blocks(parent, shots_on_pc_growth_frame, cumulative_shots_on_pc_frame)
    
    def build_dribbles_success_frame(self, df:DataFrame, parent: ttk.Frame) -> ttk.Frame:
        cumulative_dribbles_success_pc_frame = self.get_cumulative_dribbles_success_pc_figures(df)
        dribbles_success_growth_frame = self.get_dribbles_success_growth_figures(df)
        
        return self.build_matching_frame_blocks(parent, dribbles_success_growth_frame, cumulative_dribbles_success_pc_frame)
    
    def build_passes_success_frame(self, df:DataFrame, parent: ttk.Frame) -> ttk.Frame:
        cumulative_passes_success_pc_frame = self.get_cumulative_passes_success_pc_figures(df)
        passes_success_growth_frame = self.get_passes_success_pc_growth_figures(df)
        
        return self.build_matching_frame_blocks(parent, passes_success_growth_frame, cumulative_passes_success_pc_frame)
    
    def build_duels_won_pc_frame(self, df:DataFrame, parent: ttk.Frame) -> ttk.Frame:        
        cumulative_duels_won_pc_percentage_frame = self.get_cumulative_duels_won_pc_figures(df)
        duels_won_pc_growth_frame = self.get_duels_won_pc_growth_figures(df)
        
        return self.build_matching_frame_blocks(parent, duels_won_pc_growth_frame, cumulative_duels_won_pc_percentage_frame)

    def get_goals_per_90_growth_figures(self, df: DataFrame):# -> dict:
        df_copy = df.copy()
        
        df_copy['gpm'] = df_copy['goals.total'] / df_copy['games.minutes']
        df_copy['gp90'] = df_copy['gpm']*90
        
        df_copy["rolling_gpm"] = (
            df_copy.groupby("player_id")["gp90"]
                .rolling(window=5, min_periods=1)
                .mean()
                .reset_index(level=0, drop=True)
        )
        
        groups_df = df_copy.groupby(['role_group', 'type_player', 'fixture_date'])["rolling_gpm"].mean().reset_index()
        filtered_df = groups_df.dropna(subset=["rolling_gpm"])
        
        return self.build_role_line_graphs(filtered_df, "rolling_gpm", "Rolling goals / 90")
    
    def get_shots_per_90_growth_figures(self, df: DataFrame):
        df_copy = df.copy()
        df_copy['shots_per_90'] = (df_copy['shots.total']/df_copy['games.minutes'])*90
        
        df_copy["rolling_shots_per_90"] = (
            df_copy.groupby("player_id")["shots_per_90"]
                .rolling(window=5, min_periods=5)
                .mean()
                .reset_index(level=0, drop=True)
        )
        groups_df = df_copy.groupby(['role_group', 'type_player', 'fixture_date'])["rolling_shots_per_90"].mean().reset_index()
        filtered_df = groups_df.dropna(subset=["rolling_shots_per_90"])
        
        return self.build_role_line_graphs(filtered_df, "rolling_shots_per_90", "Rolling shots / 90")
    
    def get_cumulative_shots_on_pc_figures(self, df: DataFrame):
        df_copy = df.copy()
        
        grouped_df = df_copy.groupby(['role_group', 'type_player', "player_id"])
        
        df_copy['match_index'] = grouped_df.cumcount()
        df_copy['cumulative_shots_on'] = grouped_df['shots.on'].cumsum()
        df_copy['cumulative_shots_total'] = grouped_df['shots.total'].cumsum()
        df_copy['cumulative_shots_on_percentage'] = (df_copy['cumulative_shots_on'] / df_copy['cumulative_shots_total'])*100
        
        return self.build_role_lineair_regress_graphs(df_copy, "cumulative_shots_on_percentage", "Cumulative Shots on %")
    
    def get_cumulative_passes_success_pc_figures(self, df: DataFrame):
        df_copy = df.copy()
        grouped_df = df_copy.groupby(['role_group', 'type_player', "player_id"])
        
        df_copy['cumulative_passes'] = grouped_df['passes.total'].cumsum()
        df_copy['cumulative_passes_accuracy'] = grouped_df['passes.accuracy'].cumsum()
        df_copy['cumulative_passes_accuracy_percentage'] = (df_copy['cumulative_passes_accuracy'] / df_copy['cumulative_passes'])*100
        df_copy['match_index'] = grouped_df.cumcount()
        
        return self.build_role_lineair_regress_graphs(df_copy, "cumulative_passes_accuracy_percentage", "Passes success %")
    
    def get_cumulative_dribbles_success_pc_figures(self, df: DataFrame):
        df_copy = df.copy()
        
        grouped_df = df_copy.groupby(['role_group', 'type_player', "player_id"])
        
        df_copy['cumulative_passes_attempts'] = grouped_df['dribbles.attempts'].cumsum()
        df_copy['cumulative_dribbles_success'] = grouped_df['dribbles.success'].cumsum()
        df_copy['cumulative_dribbles_success_percentage'] = (df_copy['cumulative_dribbles_success'] / df_copy['cumulative_passes_attempts'])*100
        df_copy['match_index'] = grouped_df.cumcount()
        
        return self.build_role_lineair_regress_graphs(df_copy, "cumulative_dribbles_success_percentage", "Cumulative dribbles success %")
    
    def get_cumulative_duels_won_pc_figures(self, df: DataFrame) -> ttk.Frame:
        df_copy = df.copy()
        
        grouped_df = df_copy.groupby(['role_group', 'type_player', "player_id"])
        
        df_copy['cumulative_duels'] = grouped_df['duels.total'].cumsum()
        df_copy['cumulative_duels_success'] = grouped_df['duels.won'].cumsum()
        df_copy['cumulative_duels_success_percentage'] = (df_copy['cumulative_duels_success'] / df_copy['cumulative_duels'])*100
        df_copy['match_index'] = grouped_df.cumcount()
        
        return self.build_role_lineair_regress_graphs(df_copy, "cumulative_duels_success_percentage", "Cumulative duels won %")

    def get_cumulative_goals_per_90_figures(self, df: DataFrame):
        df_copy = df.copy()
        
        df_copy = df_copy.sort_values("fixture_date")
        
        grouped_df = df_copy.groupby(['role_group', 'type_player', "player_id"])
        
        df_copy['cumulative_minutes'] = grouped_df['games.minutes'].cumsum()
        df_copy['cumulative_goals'] = grouped_df['goals.total'].cumsum()
        df_copy['cumulative_goals_per_1'] = df_copy['cumulative_goals'] / df_copy['cumulative_minutes']
        df_copy['cumulative_goals_per_90'] = df_copy['cumulative_goals_per_1']*90
        df_copy['match_index'] = grouped_df.cumcount()
        
        return self.build_role_lineair_regress_graphs(df_copy, "cumulative_goals_per_90", "Cumulative goals / 90")

    def get_cumulative_shots_per_90_figures(self, df: DataFrame):
        df_copy = df.copy()
        
        grouped_df = df_copy.groupby(['role_group', 'type_player', "player_id"])
        
        df_copy['cumulative_shots'] = grouped_df['goals.total'].cumsum()
        df_copy['cumulative_minutes'] = grouped_df['games.minutes'].cumsum()
        df_copy['cumulative_shots_per_1'] = df_copy['cumulative_shots'] / df_copy['cumulative_minutes']
        df_copy['cumulative_shots_per_90'] = df_copy['cumulative_shots_per_1']*90
        df_copy['match_index'] = grouped_df.cumcount()
        
        return self.build_role_lineair_regress_graphs(df_copy, "cumulative_shots_per_90", "Cumulative shots / 90")
    
    def get_cumulative_shots_on_per_90_figures(self, df: DataFrame):
        df_copy = df.copy()
        
        grouped_df = df_copy.groupby(['role_group', 'type_player', "player_id"])
        
        df_copy['cumulative_shots_on'] = grouped_df['shots.on'].cumsum()
        df_copy['cumulative_minutes'] = grouped_df['games.minutes'].cumsum()
        df_copy['cumulative_shots_on_per_1'] = df_copy['cumulative_shots_on'] / df_copy['cumulative_minutes']
        df_copy['cumulative_shots_on_per_90'] = df_copy['cumulative_shots_on_per_1']*90
        df_copy['match_index'] = grouped_df.cumcount()
        
        return self.build_role_lineair_regress_graphs(df_copy, "cumulative_shots_on_per_90", "Cumulative shots on / 90")
    
    def get_shots_on_pc_growth_figures(self, df: DataFrame):
        df_copy = df.copy()
        
        df_copy['shots_on_pc'] = (df_copy['shots.on'] / df_copy['shots.total']) *100
        
        df_copy["rolling_shots_on_pc"] = (
            df_copy.groupby("player_id")["shots_on_pc"]
                .rolling(window=5, min_periods=1)
                .mean()
                .reset_index(level=0, drop=True)
        )
        
        groups_df = df_copy.groupby(['role_group', 'type_player', 'fixture_date'])["rolling_shots_on_pc"].mean().reset_index()
        filtered_df = groups_df.dropna(subset=["rolling_shots_on_pc"])
        return self.build_role_line_graphs(filtered_df, "rolling_shots_on_pc", "Rolling shots on %")

    def get_shots_on_per_90_growth_figures(self, df: DataFrame):
        df_copy = df.copy()        
        
        df_copy['shots_on_per_90'] = (df_copy['shots.on'] / df_copy['games.minutes'])*90
        
        df_copy["rolling_shots_on_pc"] = (
            df_copy.groupby("player_id")["shots_on_per_90"]
                .rolling(window=5, min_periods=1)
                .mean()
                .reset_index(level=0, drop=True)
        )
        
        groups_df = df_copy.groupby(['role_group', 'type_player', 'fixture_date'])["rolling_shots_on_pc"].mean().reset_index()
        filtered_df = groups_df.dropna(subset=["rolling_shots_on_pc"])
        
        return self.build_role_line_graphs(filtered_df, "rolling_shots_on_pc", "Rolling shots on / 90")
    
    def get_dribbles_success_growth_figures(self, df: DataFrame):
        df_copy = df.copy()
        
        df_copy['dribbles_success'] = (df_copy['dribbles.success'] / df_copy['dribbles.attempts'])*100
        
        df_copy["rolling_dribbles_success"] = (
            df_copy.groupby("player_id")["dribbles_success"]
                .rolling(window=5, min_periods=1)
                .mean()
                .reset_index(level=0, drop=True)
        )
        
        groups_df = df_copy.groupby(['role_group', 'type_player', 'fixture_date'])["rolling_dribbles_success"].mean().reset_index()
        filtered_df = groups_df.dropna(subset=["rolling_dribbles_success"])
        
        return self.build_role_line_graphs(filtered_df, "rolling_dribbles_success", "Rolling Dribbles success %")
    
    def get_passes_success_pc_growth_figures(self, df: DataFrame):
        df_copy = df.copy()
        
        df_copy['passes_success'] = (df_copy['passes.accuracy'] / df_copy['passes.total'])*100
        
        df_copy["rolling_passes_success"] = (
            df_copy.groupby("player_id")["passes_success"]
                .rolling(window=5, min_periods=1)
                .mean()
                .reset_index(level=0, drop=True)
        )
        
        groups_df = df_copy.groupby(['role_group', 'type_player', 'fixture_date'])["rolling_passes_success"].mean().reset_index()
        filtered_df = groups_df.dropna(subset=["rolling_passes_success"])
        
        return self.build_role_line_graphs(filtered_df, "rolling_passes_success", "Rolling passes success %")
    
    def get_duels_won_pc_growth_figures(self, df: DataFrame):
        df_copy = df.copy()
        
        df_copy['duels_won_pc'] = (df_copy['duels.won'] / df_copy['duels.total'])*100
        
        df_copy["rolling_duels_won_pc"] = (
            df_copy.groupby("player_id")["duels_won_pc"]
                .rolling(window=5, min_periods=1)
                .mean()
                .reset_index(level=0, drop=True)
        )
        
        groups_df = df_copy.groupby(['role_group', 'type_player', 'fixture_date'])["rolling_duels_won_pc"].mean().reset_index()
        filtered_df = groups_df.dropna(subset=["rolling_duels_won_pc"])
        
        return self.build_role_line_graphs(filtered_df, "rolling_duels_won_pc", "Rolling Duels won %")
    
    def build_role_line_graphs(self, df: DataFrame, field, ylabel):# -> list:
        roles = df["role_group"].dropna().unique()
        
        graphs = {}
        role_labels = {
            "att": "Attackers",
            "mid": "Midfielders",
            "def": "Defenders"
        }
        for role in roles:
            role_df = df[df["role_group"] == role]
            role_title = role_labels[role].capitalize()
            graphs[role] = self.build_line_graph(role_df, field, role_title, ylabel)
            
        return graphs
    
    def build_line_graph(
        self,
        df: DataFrame,
        y,
        title,
        ylabel,
        xlabel = "Fixture Date",
        x="fixture_date",
        hue="type_player"
    ) -> ttk.Canvas:
        figure = plt.figure(figsize=(5, 3), dpi=100)
        
        sns.lineplot(
            data=df,
            x=x,
            y=y,
            hue=hue,
            marker="o",
            alpha=0.5,
            palette=self.colors,
        )

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tick_params(axis='x', rotation=45)
        plt.xticks(rotation=45)
        
        figure.tight_layout()
        plt.close(figure)
        
        return figure
    
    def build_role_lineair_regress_graphs(self, df, y, axis_labels):
        roles = df["role_group"].dropna().unique()
        
        graphs = {}
        for role in roles:
            df_role = df[df["role_group"] == role]
            
            graphs[role] = self.build_lineair_regress_graph(df_role, y, axis_labels)
        
        return graphs
    
    def build_lineair_regress_graph(self, df, y, axis_labels) -> plt.Figure:
        g = sns.lmplot(
            data=df,
            x="match_index",
            y=y,
            hue="type_player",
            col="role_group",
            height=3,
            aspect=1,
            scatter_kws={"s": 10, "alpha": 0.5},
            ci=None,
            palette=self.colors,
            legend=False
        )

        g.set_axis_labels("Match Index", axis_labels)
        
        role_labels = {
            "att": "Attackers",
            "mid": "Midfielders",
            "def": "Defenders"
        }

        for ax in g.axes.flat:
            role_key = ax.get_title().split(" = ")[-1]
            ax.set_title(role_labels.get(role_key, role_key))

        plt.tight_layout()
        fig = g.figure
        plt.close(fig)
        
        return fig