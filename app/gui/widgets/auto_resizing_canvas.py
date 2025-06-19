import ttkbootstrap as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AutoResizingCanvas(ttk.Frame):
    def __init__(self, parent, figure, min_width_in=3):
        super().__init__(parent)

        self.figure = figure
        self.min_width_in = min_width_in
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

        self.bind("<Configure>", self._resize_figure)

    def _resize_figure(self, event):
        dpi = self.figure.get_dpi()
        width = max(self.min_width_in, event.width / dpi)
        height = self.figure.get_figheight()
        self.figure.set_size_inches(width, height)
        self.canvas.draw()