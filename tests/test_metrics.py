import pandas as pd

from trading_journal.metrics import enrich_trades, summary_stats


def test_enrich_trades_calculates_long_pnl():
    df = pd.DataFrame([
        {
            "date": "2026-05-01",
            "symbol": "BTCUSDT",
            "side": "long",
            "qty": 1,
            "entry_price": 100,
            "exit_price": 110,
            "fee": 1,
        }
    ])

    result = enrich_trades(df)

    assert result.iloc[0]["pnl"] == 9


def test_enrich_trades_calculates_short_pnl():
    df = pd.DataFrame([
        {
            "date": "2026-05-01",
            "symbol": "BTCUSDT",
            "side": "short",
            "qty": 1,
            "entry_price": 100,
            "exit_price": 90,
            "fee": 1,
        }
    ])

    result = enrich_trades(df)

    assert result.iloc[0]["pnl"] == 9


def test_summary_stats():
    df = pd.DataFrame([
        {
            "date": "2026-05-01",
            "symbol": "BTCUSDT",
            "side": "long",
            "qty": 1,
            "entry_price": 100,
            "exit_price": 110,
            "fee": 0,
        },
        {
            "date": "2026-05-02",
            "symbol": "ETHUSDT",
            "side": "long",
            "qty": 1,
            "entry_price": 100,
            "exit_price": 95,
            "fee": 0,
        },
    ])

    stats = summary_stats(df)

    assert stats["total_trades"] == 2
    assert stats["net_pnl"] == 5
    assert stats["win_rate"] == 50.0
