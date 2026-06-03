import streamlit as st
import plotly.express as px

from trading_journal.loaders import load_trades_from_csv
from trading_journal.metrics import daily_pnl, enrich_trades, summary_stats, weekly_pnl


st.set_page_config(
    page_title="Trading Journal Lite",
    layout="wide",
)

st.title("Trading Journal Lite")
st.caption("A lightweight local trading journal for CSV-based trade review.")

uploaded_file = st.file_uploader("Upload your trades CSV", type=["csv"])

if uploaded_file is None:
    st.info("Upload a CSV file with columns: date, symbol, side, qty, entry_price, exit_price, fee")
    st.stop()

try:
    raw_df = load_trades_from_csv(uploaded_file)
    trades = enrich_trades(raw_df)
    stats = summary_stats(raw_df)
except Exception as exc:
    st.error(f"Failed to process file: {exc}")
    st.stop()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Net PnL", stats["net_pnl"])
col2.metric("Win Rate", f'{stats["win_rate"]}%')
col3.metric("Avg PnL", stats["avg_pnl"])
col4.metric("Profit Factor", stats["profit_factor"])
col5.metric("Max Drawdown", stats["max_drawdown"])

st.subheader("Equity Curve")
fig = px.line(trades, x="date", y="equity_curve", markers=True)
st.plotly_chart(fig, use_container_width=True)

st.subheader("PnL by Symbol")
symbol_pnl = trades.groupby("symbol", as_index=False)["pnl"].sum()
fig2 = px.bar(symbol_pnl, x="symbol", y="pnl")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Daily PnL")
daily = daily_pnl(raw_df)
fig3 = px.bar(daily, x="date", y="pnl")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Weekly PnL")
weekly = weekly_pnl(raw_df)
fig4 = px.bar(weekly, x="date", y="pnl")
st.plotly_chart(fig4, use_container_width=True)

st.subheader("Trades")
st.dataframe(trades, use_container_width=True)
