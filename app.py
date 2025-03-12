import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox
)
from PyQt6.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

from bmi_graph import survey
from line_graph import create_line_plot
from data_loader import load_graph_data

# Dati (puoi anche spostarli in un file separato se vuoi)
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

# Widget contenente i grafici
class SurveyGraphWidget(FigureCanvas):
    def __init__(self):
        fig, ax = survey(results, category_names)
        super().__init__(fig)


class LineGraphWidget(QWidget):
    def __init__(self, title, date_labels, values, goal_min, goal_max):
        super().__init__()
        layout = QVBoxLayout(self)

        fig, _ = create_line_plot(title, date_labels, values, goal_min, goal_max)
        canvas = FigureCanvas(fig)
        toolbar = NavigationToolbar2QT(canvas, self)

        layout.addWidget(toolbar)
        layout.addWidget(canvas)

# Main Window
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monitoraggio Dati")
        self.layout = QVBoxLayout(self)
        
        title = QLabel("📝 Valori di Riferimento BMI")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.layout.addWidget(title)

        self.layout.addWidget(SurveyGraphWidget())

        # Bottone per caricare file
        self.load_button = QPushButton("Carica file dati (.csv / .xlsx)")
        self.load_button.clicked.connect(self.load_file)
        self.layout.addWidget(self.load_button)

        self.graph_widgets = []

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleziona file", "", "File CSV (*.csv);;File Excel (*.xlsx *.xls)"
        )

        if not file_path:
            return  # Utente ha annullato

        try:
            grafici = load_graph_data(file_path)

            # Rimuove eventuali grafici già mostrati
            for widget in self.graph_widgets:
                self.layout.removeWidget(widget)
                widget.setParent(None)
            self.graph_widgets.clear()

            # Aggiunge i nuovi grafici
            for g in grafici:
                widget = LineGraphWidget(
                    g["title"], g["dates"], g["values"], g["goal_min"], g["goal_max"]
                )
                self.layout.addWidget(widget)
                self.graph_widgets.append(widget)

        except Exception as e:
            QMessageBox.critical(self, "Errore nel file", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
