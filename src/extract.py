import pandas as pd

CAMINHO = "data/raw/"


def extrair_dados():
    return {
        "train": pd.read_csv(CAMINHO + "train.csv", parse_dates=["date"]),
        "stores": pd.read_csv(CAMINHO + "stores.csv"),
        "transactions": pd.read_csv(CAMINHO + "transactions.csv", parse_dates=["date"]),
        "oil": pd.read_csv(CAMINHO + "oil.csv", parse_dates=["date"]),
        "holidays": pd.read_csv(CAMINHO + "holidays_events.csv", parse_dates=["date"]),
    }


if __name__ == "__main__":
    dados = extrair_dados()
    for nome, df in dados.items():
        print(f"{nome}: {df.shape[0]:,} linhas")