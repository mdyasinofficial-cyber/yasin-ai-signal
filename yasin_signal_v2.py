import streamlit as st
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime
import pytz
import time

# --- CONFIG ---
st.set_page_config(page_title="YASIN AI V13 - PREMIUM", layout="wide")

# --- CSS FOR PREMIUM DARK LOOK ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #000000, #020f1a); color: white; }
    .signal-box { 
        padding: 30px; border-radius: 25px; text-align: center; 
        border: 4px solid; background: rgba(0,0,0,0.9);
        box-shadow: 0px 0px 50px rgba(0,255,136,0.1);
        margin-top: 20px;
    }
    .martingale-card {
        background: #121212; padding: 20px; border-radius: 15px;
        border-left: 6px solid #ff4b4b; margin-top: 25px;
    }
    .market-header { color: #00d2ff; font-weight: bold; font-size: 24px; }
    </style>
    """, unsafe_allow_html=True)

# --- ৩৫টি মার্কেটের সম্পূর্ণ লিস্ট (লোগোসহ) ---
markets = {
    # ফরেক্স পেয়ার
    "🇪🇺 EUR/USD": "EURUSD=X", "🇬🇧 GBP/USD": "GBPUSD=X", "🇯🇵 USD/JPY": "JPY=X",
    "🇦🇺 AUD/USD": "AUDUSD=X", "🇨🇦 USD/CAD": "CAD=X", "🇨🇭 USD/CHF": "CHF=X",
    "🇳🇿 NZD/USD": "NZDUSD=X", "🇪🇺 EUR/GBP": "EURGBP=X", "🇪🇺 EUR/JPY": "EURJPY=X",
    "🇬🇧 GBP/JPY": "GBPJPY=X", "🇦🇺 AUD/JPY": "AUDJPY=X", "🇪🇺 EUR/AUD": "EURAUD=X",
    "🇳🇿 NZD/JPY": "NZDJPY=X", "🇬🇧 GBP/CHF": "GBPCHF=X", "🇪🇺 EUR/CAD": "EURCAD=X",
    "🇬🇧 GBP/CAD": "GBPCAD=X", "🇦🇺 AUD/CAD": "AUDCAD=X", "🇨🇦 CAD/JPY": "CADJPY=X",
    
    # ক্রিপ্টোকারেন্সি
    "₿ BTC/USDT": "BTC-USD", "💎 ETH/USDT": "ETH-USD", "🚀 SOL/USDT": "SOL-USD",
    "🔶 BNB/USDT": "BNB-USD", "💠 XRP/USDT": "XRP-USD", "📊 ADA/USDT": "ADA-USD",
    "🐕 DOGE/USDT": "DOGE-USD", "🔴 DOT/USDT": "DOT-USD", "🔵 MATIC/USDT": "MATIC-USD",
    
    # কমোডিটি ও ইনডেক্স
    "🔥 GOLD (XAU)": "GC=F", "🥈 SILVER (XAG)": "SI=F", "🛢️ CRUDE OIL": "CL=F",
    "📉 NASDAQ 100": "^IXIC", "📈 S&P 500": "^GSPC", "🏢 DOW JONES": "^DJI",
    
    # কারেন্সি (লোকাল)
    "🇮🇳 USD/INR": "USDINR=X", "🇧DT USD/BDT": "BDT=X", "🇧🇷 USD/BRL": "USDBRL=X", "🇸🇬 USD/SGD": "USDSGD=X"
}

# --- SIDEBAR CONTROL ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
st.sidebar.markdown("## 💎 YASIN AI VIP PRO")
selected_label = st.sidebar.selectbox("🌐 ৩৫+ প্রিমিয়াম মার্কেট", list(markets.keys()))
ticker = markets[selected_label]
trade_amount = st.sidebar.number_input("ট্রেড এমাউন্ট ($):", min_value=1, value=10)
st.sidebar.write("---")
st.sidebar.info("এটি ১ মিনিটের ক্যান্ডেল এনালাইসিস করে সিগন্যাল দেয়।")

# --- AI LOGIC ENGINE ---
def analyze_market(symbol):
    try:
        # ডাটা ফেচিং
        df = yf.download(symbol, period="1d", interval="1m", progress=False)
        if len(df) < 50: 
            return "DATA ERROR", "#555555", "যথেষ্ট ডাটা পাওয়া যায়নি।", 50, 0
        
        # ইন্ডিকেটর ক্যালকুলেশন
        df['RSI'] = ta.rsi(df['Close'], length=14)
        df['EMA20'] = ta.ema(df['Close'], length=20)
        
        rsi = df['RSI'].iloc[-1]
        price = df['Close'].iloc[-1]
        ema20 = df['EMA20'].iloc[-1]

        # সিগন্যাল লজিক (প্রো লেভেল)
        if 48 < rsi < 52:
            return "WAIT ✋", "#FFD700", "মার্কেট সাইডওয়েজ, ট্রেড করবেন না।", rsi, price
        elif rsi < 30 and price < ema20:
            return "STRONG BUY ⬆️", "#00ff88", "বুলিশ রিভার্সাল আসছে! আপ ট্রেড নিন।", rsi, price
        elif rsi > 70 and price > ema20:
            return "STRONG SELL ⬇️", "#ff4b4b", "বিয়ারিশ রিভার্সাল আসছে! ডাউন ট্রেড নিন।", rsi, price
        elif rsi < 40:
            return "BUY (UP) ⬆️", "#2ecc71", "বুলিশ প্রেসার বাড়ছে।", rsi, price
        else:
            return "SELL (DOWN) ⬇️", "#e74c3c", "বিয়ারিশ প্রেসার বাড়ছে।", rsi, price
    except Exception as e:
        return "ERROR", "#ff4b4b", str(e), 50, 0

# --- MAIN UI ---
prediction, color, status, rsi_val, current_price = analyze_market(ticker)
now = datetime.now(pytz.timezone('Asia/Dhaka'))
seconds = now.second
rem_sec = 60 - seconds

# ডিসপ্লে হেডার
st.markdown(f"<p class='market-header'>{selected_label} | Price: ${current_price:.2f}</p>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    st.markdown(f"#### 🕒 সময়: {now.strftime('%I:%M:%S %p')}")
with c2:
    st.markdown(f"#### ⏳ ক্যান্ডেল শেষ হতে বাকি: `{rem_sec}s`")

# সিগন্যাল টাইমিং লজিক (৪০ সেকেন্ডের পর সিগন্যাল দেখাবে)
if seconds >= 40:
    st.markdown(f"""
        <div class='signal-box' style='border-color: {color};'>
            <p style='color: {color}; letter-spacing: 3px;'><b>YASIN AI V13 VIP SIGNAL</b></p>
            <h1 style='color: {color}; font-size: 80px; margin: 10px 0;'>{prediction}</h1>
            <h3 style='color: white; font-weight: 300;'>{status}</h3>
            <p style='font-size: 14px; opacity: 0.6;'>RSI: {rsi_val:.2f} | Time: {now.hour}:{now.minute + 1}:00</p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
        <div class='signal-box' style='border-color: #333;'>
            <h1 style='font-size: 50px; color: #777;'>ANALYZING... 🛰️</h1>
            <p>পরবর্তী সিগন্যাল ক্যান্ডেল শেষ হওয়ার ২০ সেকেন্ড আগে আসবে।</p>
            <div style='width: 100%; background: #222; border-radius: 10px;'>
                <div style='width: {(seconds/40)*100 if seconds < 40 else 100}%; background: #00d2ff; height: 10px; border-radius: 10px;'></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# লস রিকভারি কার্ড
if "BUY" in prediction or "SELL" in prediction:
    st.markdown(f"""
        <div class='martingale-card'>
            <h4 style='color: #ff4b4b; margin:0;'>🛡️ লস রিকভারি মানি ম্যানেজমেন্ট</h4>
            <p style='margin:10px 0;'>ট্রেড লস হলে <b>মার্টিংগেল (২.৫ গুণ)</b> ব্যবহার করুন।</p>
            <p style='font-size: 18px;'>পরবর্তী ইনভেস্ট: <b>${trade_amount * 2.5}</b></p>
        </div>
    """, unsafe_allow_html=True)

# লাইভ প্রিমিয়াম চার্ট
st.write("---")
with st.expander("📊 লাইভ চার্ট দেখুন", expanded=True):
    df_chart = yf.download(ticker, period="1h", interval="1m", progress=False)
    fig = go.Figure(data=[go.Candlestick(
        x=df_chart.index, open=df_chart['Open'], high=df_chart['High'],
        low=df_chart['Low'], close=df_chart['Close'],
        increasing_line_color='#00ff88', decreasing_line_color='#ff4b4b'
    )])
    fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=400, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

# অটো রিফ্রেশ
time.sleep(1)
st.rerun()
