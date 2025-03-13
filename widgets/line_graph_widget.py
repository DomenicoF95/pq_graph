# widgets/line_graph_widget.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from line_graph import create_line_plot

class LineGraphWidget(QWidget):
    def __init__(self, title, date_labels, values, goal_min, goal_max, width=8, height=6):
        super().__init__()
        layout = QVBoxLayout(self)

        fig, _ = create_line_plot(title, date_labels, values, goal_min, goal_max)
        canvas = FigureCanvas(fig)
        toolbar = NavigationToolbar2QT(canvas, self)

        layout.addWidget(toolbar)
        layout.addWidget(canvas)
