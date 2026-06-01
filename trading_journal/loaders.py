import pandas as pd


def load_trades_from_csv(file) -> pd.DataFrame:
    return pd.read_csv(file)
