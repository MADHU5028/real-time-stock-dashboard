import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time

st.title("📈 Real-Time Stock Market Dashboard")

stock_list = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
selected_stock = st.selectbox("Select a stock", stock_list)

@st.cache_data
def load_stock_data(symbol):
    stock = yf.Ticker(symbol)
    return stock.history(period="1d", interval="1m")

data = load_stock_data(selected_stock)

data["MA20"] = data["Close"].rolling(20).mean()

def calculate_rsi(series, window=14):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(window).mean()
    loss = -delta.clip(upper=0).rolling(window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

data["RSI"] = calculate_rsi(data["Close"])

fig = go.Figure()
fig.add_trace(go.Scatter(x=data.index, y=data["Close"], name="Close"))
fig.add_trace(go.Scatter(x=data.index, y=data["MA20"], name="MA 20"))

st.plotly_chart(fig)

st.subheader("RSI Indicator")
st.line_chart(data["RSI"])


if st.button("🔄 Refresh Data"):
    st.rerun()

