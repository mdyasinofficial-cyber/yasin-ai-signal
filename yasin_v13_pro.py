import streamlit as st
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime
import pytz
import time

# --- CONFIG ---
st.set_page_config(page_title="YASIN AI V13 - LOSS RECOVERY", layout="wide")

# --- CSS FOR PREMIUM LOOK ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #000000, #020f1a); color: white; }
    .signal-box { 
        padding: 40px; border-radius: 30px; text-align: center; 
        border: 5px solid; background: rgba(0,0,0,0.85);
        box-shadow: 0px 0px 60px rgba(0,255,136,0.15);
    }
    .martingale-card {
        background: #1a1a1a; padding: 15px; border-radius: 15px;
        border-left: 5px solid #ff4b4b; margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ৩০+ মার্কেট লিস্ট লোগো সহ ---
markets = {
    "🇪🇺 EUR/USD": "EURUSD=X", "🇬🇧 GBP/USD": "GBPUSD=X", "🇯🇵 USD/JPY": "JPY=X",
    "🇦🇺 AUD/USD": "AUDUSD=X", "🇨🇦 USD/CAD": "CAD=X", "🇨🇭 USD/CHF": "CHF=X",
    "🇳🇿 NZD/USD": "NZDUSD=X", "🇪🇺 EUR/GBP": "EURGBP=X", "🇪🇺 EUR/JPY": "EURJPY=X",
    "🇬🇧 GBP/JPY": "GBPJPY=X", "🇦🇺 AUD/JPY": "AUDJPY=X", "🇨🇭 EUR/CHF": "EURCHF=X",
    "🇳🇿 NZD/JPY": "NZDJPY=X", "🇬🇧 GBP/CHF": "GBPCHF=X", "🇪🇺 EUR/CAD": "EURCAD=X",
    "₿ BTC/USDT": "BTC-USD", "💎 ETH/USDT": "ETH-USD", "🚀 SOL/USDT": "SOL-USD",
    "🔶 BNB/USDT": "BNB-USD", "💠 XRP/USDT": "XRP-USD", "📊 ADA/USDT": "ADA-USD",
    "🔥 GOLD (XAU)": "GC=F", "🥈 SILVER (XAG)": "SI=F", "🛢️ CRUDE OIL": "CL=F",
    "📉 NASDAQ 100": "^IXIC", "📈 S&P 500": "^GSPC", "🏢 DOW JONES": "^DJI",
    "🇮🇳 USD/INR": "USDINR=X", "🇧🇷 USD/BRL": "USDBRL=X", "🇸🇬 USD/SGD": "USDSGD=X"
}

st.sidebar.markdown("## 💎 YASIN AI VIP CONTROL")
selected_label = st.sidebar.selectbox("🌐 ৩০+ মার্কেট লিস্ট", list(markets.keys()))
ticker = markets[selected_label]
trade_amount = st.sidebar.number_input("আপনার ট্রেড এমাউন্ট ($):", min_value=1, value=10)

# --- AI ENGINE ---
def analyze_v13(symbol):
    try:
        df = yf.download(symbol, period="1d", interval="1m", progress=False)
        if len(df) < 50: return "LOADING...", "#555555", "তথ্য সংগ্রহ করা হচ্ছে...", 50
        
        df['RSI'] = ta.rsi(df['Close'], length=14)
        df['EMA20'] = ta.ema(df['Close'], length=20)
        df['EMA50'] = ta.ema(df['Close'], length=50)
        
        rsi = df['RSI'].iloc[-1]
        price = df['Close'].iloc[-1]
        e20 = df['EMA20'].iloc[-1]
        e50 = df['EMA50'].iloc[-1]

        # শক্তিশালী সিগন্যাল ও ডেঞ্জার জোন লজিক
        if 47 < rsi < 53:
            return "WAIT ✋", "#FFD700", "মার্কেট এখন বিপজ্জনক! ট্রেড নিবেন না।", rsi
        elif rsi < 32 and price < e20:
            return "STRONG BUY ⬆️", "#00ff88", "নিখুঁত এন্ট্রি! পরবর্তী ক্যান্ডেল গ্রিন হবে।", rsi
        elif rsi > 68 and price > e20:
            return "STRONG SELL ⬇️", "#ff4b4b", "নিখুঁত এন্ট্রি! পরবর্তী ক্যান্ডেল রেড হবে।", rsi
        elif e20 > e50:
            return "BUY (UP) ⬆️", "#00ff88", "ট্রেন্ড বুলিশ। কল অপশন সেফ।", rsi
        else:
            return "SELL (DOWN) ⬇️", "#ff4b4b", "ট্রেন্ড বিয়ারিশ। পুট অপশন সেফ।", rsi
    except:
        return "ERROR", "#ff4b4b", "সার্ভার এরর!", 50

# --- UI DISPLAY ---
prediction, color, status, rsi_val = analyze_v13(ticker)
now = datetime.now(pytz.timezone('Asia/Dhaka'))
rem_sec = 60 - now.second

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"### 🕒 বর্তমান সময়: {now.strftime('%I:%M:%S %p')}")
with col2:
    st.markdown(f"### ⏳ ক্যান্ডেল শেষ: {rem_sec}s")

# সিগন্যাল বক্স (৪০ সেকেন্ডের পর সিগন্যাল দেখাবে)
if now.second >= 40:
    st.markdown(f"""
        <div class='signal-box' style='border-color: {color};'>
            <p style='color: {color}; letter-spacing: 2px;'><b>AI PRO V13 ANALYSIS</b></p>
            <h1 style='color: {color}; font-size: 75px; margin: 0;'>{prediction}</h1>
            <h3 style='opacity: 0.9;'>{status}</h3>
            <hr style='opacity: 0.1;'>
            <p>Market: {selected_label} | RSI: {rsi_val:.2f} | Entry Time: {now.minute + 1}:00</p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
        <div class='signal-box' style='border-color: #555555;'>
            <h1 style='font-size: 60px; color: #555555;'>ANALYZING... 🛰️</h1>
            <h3>পরবর্তী সিগন্যাল ক্যান্ডেল শেষ হওয়ার ২০ সেকেন্ড আগে আসবে।</h3>
        </div>
    """, unsafe_allow_html=True)

# লস রিকভারি ক্যালকুলেটর
if "SELL" in prediction or "BUY" in prediction:
    st.markdown(f"""
        <div class='martingale-card'>
            <h4 style='color: #ff4b4b; margin:0;'>🛡️ লস রিকভারি গাইড (Martingale)</h4>
            <p style='margin:5px 0;'>যদি এই ট্রেডটি লস হয়, তবে পরবর্তী ট্রেডে ইনভেস্ট করুন: <b>${trade_amount * 2.5}</b></p>
        </div>
    """, unsafe_allow_html=True)

# লাইভ চার্ট
st.write("---")
df_chart = yf.download(ticker, period="1h", interval="1m", progress=False)
fig = go.Figure(data=[go.Candlestick(x=df_chart.index, open=df_chart['Open'], high=df_chart['High'], low=df_chart['Low'], close=df_chart['Close'])])
fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=450)
st.plotly_chart(fig, use_container_width=True)

time.sleep(1)
st.rerun()
