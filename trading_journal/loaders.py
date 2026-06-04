import pandas as pd


REQUIRED_STANDARD_COLUMNS = {
    "date",
    "symbol",
    "side",
    "qty",
    "entry_price",
    "exit_price",
}


BINANCE_FUTURES_COLUMN_MAP = {
    "Date": "date",
    "Symbol": "symbol",
    "Side": "side",
    "Quantity": "qty",
    "Entry Price": "entry_price",
    "Exit Price": "exit_price",
    "Fee": "fee",
}


def load_trades_from_csv(file) -> pd.DataFrame:
    return pd.read_csv(file)


def normalize_standard_columns(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result.columns = [str(column).strip() for column in result.columns]
    return result


def load_binance_futures_csv(file) -> pd.DataFrame:
    raw = pd.read_csv(file)
    normalized = normalize_standard_columns(raw)

    missing = set(BINANCE_FUTURES_COLUMN_MAP) - set(normalized.columns)
    if missing:
        raise ValueError(f"Missing Binance futures columns: {sorted(missing)}")

    result = normalized.rename(columns=BINANCE_FUTURES_COLUMN_MAP)
    result = result[list(BINANCE_FUTURES_COLUMN_MAP.values())]

    result["side"] = result["side"].astype(str).str.lower()
    result["fee"] = result["fee"].fillna(0)

    return result
