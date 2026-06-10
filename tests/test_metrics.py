import sys
from io import StringIO
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from trading_journal.loaders import load_binance_futures_csv, load_bybit_csv, load_trades_from_csv
from trading_journal.metrics import (
    calculate_max_drawdown,
    daily_pnl,
    enrich_trades,
    pnl_by_tag,
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


def test_load_trades_from_csv_defaults_missing_tag_to_untagged():
    csv_data = StringIO(
        """date,symbol,side,qty,entry_price,exit_price,fee
2026-05-01,BTCUSDT,long,1,100,110,0
"""
    )

    result = load_trades_from_csv(csv_data)

    assert result.iloc[0]["tag"] == "untagged"


def test_load_trades_from_csv_defaults_empty_tag_to_untagged():
    csv_data = StringIO(
        "date,symbol,side,qty,entry_price,exit_price,fee,tag\n"
        "2026-05-01,BTCUSDT,long,1,100,110,0,\n"
        f"2026-05-02,ETHUSDT,short,1,100,90,0,{'   '}\n"
        "2026-05-03,SOLUSDT,long,1,50,55,0,breakout\n"
    )

    result = load_trades_from_csv(csv_data)

    assert result["tag"].tolist() == ["untagged", "untagged", "breakout"]


def test_pnl_by_tag_groups_and_sorts_pnl():
    df = pd.DataFrame([
        {
            "date": "2026-05-01",
            "symbol": "BTCUSDT",
            "side": "long",
            "qty": 1,
            "entry_price": 100,
            "exit_price": 110,
            "fee": 0,
            "tag": "breakout",
        },
        {
            "date": "2026-05-02",
            "symbol": "ETHUSDT",
            "side": "short",
            "qty": 1,
            "entry_price": 100,
            "exit_price": 95,
            "fee": 0,
            "tag": "breakout",
        },
        {
            "date": "2026-05-03",
            "symbol": "SOLUSDT",
            "side": "long",
            "qty": 1,
            "entry_price": 50,
            "exit_price": 55.555,
            "fee": 0,
            "tag": "scalp",
        },
        {
            "date": "2026-05-04",
            "symbol": "XRPUSDT",
            "side": "long",
            "qty": 1,
            "entry_price": 100,
            "exit_price": 96,
            "fee": 0,
            "tag": "manual",
        },
    ])

    result = pnl_by_tag(df)

    assert result.to_dict("records") == [
        {"tag": "breakout", "pnl": 15.0},
        {"tag": "scalp", "pnl": 5.56},
        {"tag": "manual", "pnl": -4.0},
    ]


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


def test_load_binance_futures_csv():
    csv_data = StringIO(
        """Date,Symbol,Side,Quantity,Entry Price,Exit Price,Fee
2026-05-01,BTCUSDT,LONG,0.1,60000,61200,4
2026-05-02,ETHUSDT,SHORT,1,3100,3000,3
"""
    )

    result = load_binance_futures_csv(csv_data)

    assert list(result.columns) == [
        "date",
        "symbol",
        "side",
        "qty",
        "entry_price",
        "exit_price",
        "fee",
        "tag",
    ]
    assert result.iloc[0]["side"] == "long"
    assert result.iloc[1]["side"] == "short"
    assert result["tag"].tolist() == ["untagged", "untagged"]


def test_load_bybit_csv():
    csv_data = StringIO(
        """Created Time,Contract,Side,Qty,Entry Price,Exit Price,Trading Fee
2026-05-01,BTCUSDT,Buy,0.1,60000,61200,4
2026-05-02,ETHUSDT,Sell,1,3100,3000,3
"""
    )

    result = load_bybit_csv(csv_data)

    assert list(result.columns) == [
        "date",
        "symbol",
        "side",
        "qty",
        "entry_price",
        "exit_price",
        "fee",
        "tag",
    ]
    assert result.iloc[0]["side"] == "long"
    assert result.iloc[1]["side"] == "short"
    assert result["tag"].tolist() == ["untagged", "untagged"]
