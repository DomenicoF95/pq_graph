from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np


class DiscreteBarWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        category_names = ['Sottopeso', 'Normopeso', 'Sovrappeso',
                  'Obeso', 'Obeso Grave']
        
        results = {
            'BMI': [18.5, 24.9, 29.9, 34.9, 40],
        }

        """ Esaminando la letteratura scientifica, la percentuale di grasso corporeo considerata accettabile 
            (range di normalità) è compresa tra il 10% ed il 18% per gli uomini e 
            tra il 18% ed il 26-28% per le donne.
        """

        """ Il valore ideale della massa magra delle donne sedentarie è del 75% (FM 25%), 
            mentre quella degli uomini è dell'85% (FM 15%); 
            gli atleti e i soggetti sportivi presentano una percentuale di massa magra più alta: 
            per le donne è dell'82-88% (FM 18-12%), mentre per gli uomini è dell'88-92% (FM 12-8%);
        """

        labels = list(results.keys())
        data = np.array(list(results.values()))
        data_cum = data.cumsum(axis=1)
        category_colors = plt.colormaps['YlOrBr'](np.linspace(0.15, 0.85, data.shape[1]))

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.invert_yaxis()
        ax.xaxis.set_visible(False)
        ax.set_xlim(0, np.sum(data, axis=1).max())

        for i, (cat, color) in enumerate(zip(category_names, category_colors)):
            widths = data[:, i]
            starts = data_cum[:, i] - widths
            rects = ax.barh(labels, widths, left=starts, height=0.5, label=cat, color=color)

            r, g, b, _ = color
            text_color = 'white' if r * g * b < 0.5 else 'black'
            ax.bar_label(rects, label_type='center', color=text_color)

        ax.legend(ncols=len(category_names), bbox_to_anchor=(0, 1), loc='lower left', fontsize='small')
        fig.tight_layout()

        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        self.setLayout(layout)
