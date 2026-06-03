import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from trading_journal.metrics import (
    calculate_max_drawdown,
    daily_pnl,
    enrich_trades,
    summary_stats,
    weekly_pnl,
)


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


def test_calculate_max_drawdown():
    equity_curve = pd.Series([10, 15, 5, 20, 12])

    assert calculate_max_drawdown(equity_curve) == -10



def test_daily_pnl():
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
            "date": "2026-05-01",
            "symbol": "ETHUSDT",
            "side": "long",
            "qty": 1,
            "entry_price": 100,
            "exit_price": 95,
            "fee": 0,
        },
        {
            "date": "2026-05-02",
            "symbol": "SOLUSDT",
            "side": "short",
            "qty": 1,
            "entry_price": 50,
            "exit_price": 45,
            "fee": 0,
        },
    ])

    result = daily_pnl(df)

    assert len(result) == 2
    assert result.iloc[0]["pnl"] == 5
    assert result.iloc[1]["pnl"] == 5


def test_weekly_pnl():
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

    result = weekly_pnl(df)

    assert len(result) == 1
    assert result.iloc[0]["pnl"] == 5
