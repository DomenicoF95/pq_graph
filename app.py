import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QStackedWidget, QFileDialog, QLabel, QHBoxLayout, QMessageBox, QScrollArea, QSizePolicy
from PyQt6.QtCore import Qt
from widgets.discrete_bar_widget import DiscreteBarWidget
from widgets.line_graph_widget import LineGraphWidget
from data_loader import load_graph_data


class WizardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Report Wizard")
        self.setMinimumSize(1100, 700)

        # -----------------------
        # WIDGET CENTRALE
        # -----------------------
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # LAYOUT PRINCIPALE VERTICALE (menu + grafico sopra, pulsanti sotto)
        main_layout = QVBoxLayout(main_widget)

        # -----------------------
        # ZONA SUPERIORE: MENU + GRAFICO
        # -----------------------
        top_layout = QHBoxLayout()

        # 🟦 MENU LATERALE SCORRIBILE
        self.menu_layout = QVBoxLayout()
        self.menu_buttons = []

        menu_container = QWidget()
        menu_container.setLayout(self.menu_layout)

        menu_scroll = QScrollArea()
        menu_scroll.setWidgetResizable(True)
        menu_scroll.setWidget(menu_container)
        menu_scroll.setFixedWidth(200)

        top_layout.addWidget(menu_scroll)

        # 🟩 STACK DEI GRAFICI
        self.graph_stack = QStackedWidget()
        top_layout.addWidget(self.graph_stack)

        main_layout.addLayout(top_layout)

        # -----------------------
        # BOTTOM BAR: PULSANTI
        # -----------------------
        bottom_bar = QHBoxLayout()
        self.btn_load = QPushButton("📂 Carica File (.csv / .xsls)")
        self.btn_prev = QPushButton("← Indietro")
        self.btn_next = QPushButton("Avanti →")
        self.status = QLabel()

        bottom_bar.addWidget(self.btn_load)
        bottom_bar.addStretch()
        bottom_bar.addWidget(self.btn_prev)
        bottom_bar.addWidget(self.btn_next)
        bottom_bar.addWidget(self.status)

        main_layout.addLayout(bottom_bar)

        # -----------------------
        # AZIONI
        # -----------------------
        self.btn_load.clicked.connect(self.load_file)
        self.btn_prev.clicked.connect(self.prev_graph)
        self.btn_next.clicked.connect(self.next_graph)

        self.graph_widgets = []
        self.current_index = 0

        self.add_fixed_step()

    def add_fixed_step(self):
        widget = DiscreteBarWidget()
        self.graph_stack.addWidget(widget)
        self.graph_widgets.append(widget)
        self.add_menu_button("BMI")
        self.graph_stack.setCurrentIndex(0)
        self.update_status()

    def add_menu_button(self, label):
        btn = QPushButton(label)
        btn.setCheckable(True)
        btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        index = len(self.menu_buttons)
        btn.clicked.connect(lambda: self.go_to_step(index))
        self.menu_layout.addWidget(btn)
        self.menu_buttons.append(btn)

    def go_to_step(self, index):
        self.current_index = index
        self.graph_stack.setCurrentIndex(index)
        self.update_status()

    def update_status(self):
        self.status.setText(f"Step {self.current_index + 1} di {len(self.graph_widgets)}")
        for i, btn in enumerate(self.menu_buttons):
            btn.setChecked(i == self.current_index)

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleziona file", "", "File CSV (*.csv);;File Excel (*.xlsx *.xls)"
        )
        if not file_path:
            return

        try:
            grafici = load_graph_data(file_path)

            # Rimuove step grafici (eccetto primo)
            while self.graph_stack.count() > 1:
                w = self.graph_stack.widget(1)
                self.graph_stack.removeWidget(w)
                w.deleteLater()
            self.graph_widgets = self.graph_widgets[:1]

            # Rimuove i pulsanti extra (eccetto primo)
            while len(self.menu_buttons) > 1:
                btn = self.menu_buttons.pop()
                btn.deleteLater()

            # Aggiungi nuovi grafici e pulsanti
            for g in grafici:
                widget = LineGraphWidget(
                    g["title"], g["dates"], g["values"], g["goal_min"], g["goal_max"],
                    width=8, height=6
                )
                self.graph_stack.addWidget(widget)
                self.graph_widgets.append(widget)
                self.add_menu_button(g["title"])

            self.go_to_step(0)

        except Exception as e:
            QMessageBox.critical(self, "Errore", str(e))

    def next_graph(self):
        if self.current_index < len(self.graph_widgets) - 1:
            self.go_to_step(self.current_index + 1)

    def prev_graph(self):
        if self.current_index > 0:
            self.go_to_step(self.current_index - 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WizardWindow()
    win.show()
    sys.exit(app.exec())
