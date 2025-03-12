import pandas as pd

def load_graph_data(file_path: str):
    """
    Carica e valida un file dati per grafici di massa magra.
    """
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith((".xlsx", ".xls")):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Formato non supportato. Usa un file .csv o .xlsx")

    required_columns = ["Titolo", "Date", "Valori", "Obiettivo Min", "Obiettivo Max"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Colonna mancante: '{col}'")

    graph_data = []
    for idx, row in df.iterrows():
        try:
            title = str(row["Titolo"])
            dates = [d.strip() for d in str(row["Date"]).split(";")]
            values = [float(v.strip()) for v in str(row["Valori"]).split(";")]

            if len(dates) != len(values):
                raise ValueError(f"Riga {idx+2}: numero date ≠ numero valori")

            goal_min = float(row["Obiettivo Min"])
            goal_max = float(row["Obiettivo Max"])

            graph_data.append({
                "title": title,
                "dates": dates,
                "values": values,
                "goal_min": goal_min,
                "goal_max": goal_max
            })
        except Exception as e:
            raise ValueError(f"Errore nella riga {idx+2}: {e}")

    return graph_data
