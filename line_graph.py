from matplotlib.figure import Figure
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime

def create_line_plot(
    title: str,
    date_labels: list[str],
    values: list[float],
    goal_min: float,
    goal_max: float
):
    dates = [datetime.strptime(d, "%Y-%m-%d") for d in date_labels]
    mean_value = np.mean(values)

    fig = Figure(figsize=(9, 4))
    ax = fig.add_subplot(111)

    # LINEA DEI DATI
    ax.plot(dates, values, marker='o', linestyle='-', color='teal', label='Massa Magra (%)')

    # 1. Valori accanto ai punti
    for i, value in enumerate(values):
        ax.annotate(f"{value:.1f}%", (dates[i], value), textcoords="offset points", xytext=(0, 8),
                    ha='center', fontsize=9, color='black')

    # 2. Linea media
    ax.axhline(mean_value, color='orange', linestyle='--', linewidth=1.5, label=f"Media: {mean_value:.1f}%")

    # 3. Range obiettivo
    ax.axhspan(goal_min, goal_max, color='green', alpha=0.1, label=f"Obiettivo: {goal_min}-{goal_max}%")

    # Asse X formattato con date
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    fig.autofmt_xdate()

    ax.set_title(title)
    ax.set_ylabel("Percentuale (%)")
    ax.grid(True)
    ax.legend(loc='upper left')

    return fig, ax
