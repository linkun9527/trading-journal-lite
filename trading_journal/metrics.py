import pandas as pd


def calculate_pnl(row: pd.Series) -> float:
    side = str(row["side"]).lower()
    qty = float(row["qty"])
    entry = float(row["entry_price"])
    exit_ = float(row["exit_price"])
    fee = float(row.get("fee", 0))

    if side == "long":
        return (exit_ - entry) * qty - fee

    if side == "short":
        return (entry - exit_) * qty - fee

    raise ValueError(f"Unsupported side: {side}")


def enrich_trades(df: pd.DataFrame) -> pd.DataFrame:
    required = {"date", "symbol", "side", "qty", "entry_price", "exit_price"}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    result = df.copy()
    result["date"] = pd.to_datetime(result["date"])
    result["fee"] = result.get("fee", 0)
    result["pnl"] = result.apply(calculate_pnl, axis=1)
    result["equity_curve"] = result["pnl"].cumsum()

    return result


def summary_stats(df: pd.DataFrame) -> dict:
    enriched = enrich_trades(df)

    total_trades = len(enriched)
    wins = enriched[enriched["pnl"] > 0]
    losses = enriched[enriched["pnl"] < 0]

    gross_profit = wins["pnl"].sum()
    gross_loss = abs(losses["pnl"].sum())

    return {
        "total_trades": total_trades,
        "net_pnl": round(enriched["pnl"].sum(), 2),
        "win_rate": round(len(wins) / total_trades * 100, 2) if total_trades else 0,
        "avg_pnl": round(enriched["pnl"].mean(), 2) if total_trades else 0,
        "profit_factor": round(gross_profit / gross_loss, 2) if gross_loss else None,
        "best_trade": round(enriched["pnl"].max(), 2) if total_trades else 0,
        "worst_trade": round(enriched["pnl"].min(), 2) if total_trades else 0,
    }
