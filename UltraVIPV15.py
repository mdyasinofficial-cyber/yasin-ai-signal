import streamlit as st
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import pytz
import time

# --- ১. গ্লোবাল কনফিগারেশন এবং স্টাইল ---
st.set_page_config(page_title="ARAFAT ULTRA VIP V15", layout="wide", initial_sidebar_state="collapsed")

# আধুনিক ডার্ক থিম
st.markdown("""
    <style>
    /* মেইন ব্যাকগ্রাউন্ড এবং টেক্সট */
    .stApp { background: #010409; color: #c9d1d9; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
    
    /* কাস্টম মেট্রিক কার্ড */
    .metric-card {
        background: rgba(22, 27, 34, 0.8);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    .metric-title { font-size: 14px; color: #8b949e; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px; }
    .metric-value { font-size: 28px; font-weight: bold; color: #58a6ff; }
    
    /* সিগন্যাল কার্ড (Pro Design) */
    .signal-card {
        background: rgba(13, 17, 23, 0.95);
        border: 2px solid #30363d;
        border-radius: 16px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 0 50px rgba(88, 166, 255, 0.15);
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .signal-card:hover { transform: translateY(-3px); box-shadow: 0 0 60px rgba(88, 166, 255, 0.25); }
    .signal-label { font-size: 16px; color: #8b949e; letter-spacing: 3px; font-weight: bold; text-transform: uppercase; margin-bottom: 10px; }
    .signal-main { font-size: 72px; font-weight: 800; margin: 0; line-height: 1; }
    .signal-status { font-size: 18px; margin-top: 15px; font-weight: 500; color: #c9d1d9; }
    .signal-details { font-size: 14px; color: #8b949e; margin-top: 5px; }
    
    /* মার্কেট লিস্ট বাটন স্টাইল */
    .stButton > button {
        width: 100%; border-radius: 8px; border: 1px solid #30363d;
        background-color: rgba(22, 27, 34, 0.6); color: #c9d1d9;
        text-align: left; padding: 12px 15px; font-size: 15px; font-weight: 500;
        display: flex; align-items: center; justify-content: flex-start; gap: 10px;
    }
    .stButton > button:hover { border-color: #58a6ff; background-color: rgba(88, 166, 255, 0.1); }
    .stButton > button:focus { border-color: #58a6ff; box-shadow: 0 0 10px rgba(88, 166, 255, 0.5); }
    
    /* ক্যান্ডেল টাইমার এবং ক্লক */
    .clock-widget { text-align: center; padding: 10px 0; color: #f08080; }
    .timer-widget { text-align: center; padding: 10px 0; color: #fff; font-size: 20px; font-weight: bold;}
    
    /* এক্সপ্যান্ডার স্টাইল */
    .streamlit-expanderHeader { background-color: rgba(22, 27, 34, 0.6); border: 1px solid #30363d; border-radius: 8px; font-weight: 600; color: #c9d1d9; }
    
    </style>
""", unsafe_allow_html=True)

# --- ২. মার্কেট ডাটাবেস (লোগো এবং টিলিস্ট) ---
markets = {
    "MAJOR FOREX": [
        {"icon": "🇺🇸🇪🇺", "label": "EUR/USD", "ticker": "EURUSD=X"},
        {"icon": "🇺🇸🇬🇧", "label": "GBP/USD", "ticker": "GBPUSD=X"},
        {"icon": "🇺🇸🇯🇵", "label": "USD/JPY", "ticker": "JPY=X"},
        {"icon": "🇺🇸🇨🇦", "label": "USD/CAD", "ticker": "CAD=X"},
        {"icon": "🇺🇸🇦🇺", "label": "AUD/USD", "ticker": "AUDUSD=X"},
        {"icon": "🇺🇸🇨🇭", "label": "USD/CHF", "ticker": "CHF=X"},
        {"icon": "🇺🇸🇳🇿", "label": "NZD/USD", "ticker": "NZDUSD=X"},
    ],
    "MINOR FOREX": [
        {"icon": "🇪🇺🇬🇧", "label": "EUR/GBP", "ticker": "EURGBP=X"},
        {"icon": "🇪🇺🇯🇵", "label": "EUR/JPY", "ticker": "EURJPY=X"},
        {"icon": "🇬🇧🇯🇵", "label": "GBP/JPY", "ticker": "GBPJPY=X"},
        {"icon": "🇪🇺🇨🇦", "label": "EUR/CAD", "ticker": "EURCAD=X"},
        {"icon": "🇬🇧🇨🇦", "label": "GBP/CAD", "ticker": "GBPCAD=X"},
        {"icon": "🇦🇺🇯🇵", "label": "AUD/JPY", "ticker": "AUDJPY=X"},
        {"icon": "🇦🇺🇨🇦", "label": "AUD/CAD", "ticker": "AUDCAD=X"},
        {"icon": "🇨🇦🇯🇵", "label": "CAD/JPY", "ticker": "CADJPY=X"},
        {"icon": "🇺🇸🇧🇩", "label": "USD/BDT", "ticker": "BDT=X"},
    ],
    "METALS & ENERGY": [
        {"icon": "🔥💰", "label": "GOLD (XAU)", "ticker": "GC=F"},
        {"icon": "🥈💰", "label": "SILVER (XAG)", "ticker": "SI=F"},
        {"icon": "🛢️💰", "label": "CRUDE OIL", "ticker": "CL=F"},
        {"icon": "📈💰", "label": "NATURAL GAS", "ticker": "NG=F"},
    ],
    "CRYPTO": [
        {"icon": "₿", "label": "BTC/USDT", "ticker": "BTC-USD"},
        {"icon": "💎", "label": "ETH/USDT", "ticker": "ETH-USD"},
        {"icon": "🚀", "label": "SOL/USDT", "ticker": "SOL-USD"},
        {"icon": "🔶", "label": "BNB/USDT", "ticker": "BNB-USD"},
        {"icon": "🔷", "label": "XRP/USDT", "ticker": "XRP-USD"},
        {"icon": "📉", "label": "ADA/USDT", "ticker": "ADA-USD"},
    ],
    "INDICES": [
        {"icon": "📊", "label": "NASDAQ 100", "ticker": "^IXIC"},
        {"icon": "📈", "label": "S&P 500", "ticker": "^GSPC"},
        {"icon": "🏢", "label": "DOW JONES", "ticker": "^DJI"},
        {"icon": "📉", "label": "VIX INDEX", "ticker": "^VIX"},
    ]
}

# --- ৩. এনালাইসিস ইঞ্জিন (5m Trend + 1m Entry + Candle Action) ---
def get_vip_analysis(symbol):
    try:
        df_1m = yf.download(symbol, period="1d", interval="1m", progress=False)
        df_5m = yf.download(symbol, period="1d", interval="5m", progress=False)

        if len(df_1m) < 30 or len(df_5m) < 10: return None

        if isinstance(df_1m.columns, pd.MultiIndex): df_1m.columns = df_1m.columns.get_level_values(0)
        if isinstance(df_5m.columns, pd.MultiIndex): df_5m.columns = df_5m.columns.get_level_values(0)

        ema9_5m = ta.ema(df_5m['Close'], length=9).iloc[-1]
        ema21_5m = ta.ema(df_5m['Close'], length=21).iloc[-1]
        trend_5m = "UP" if ema9_5m > ema21_5m else "DOWN"

        df_1m['RSI'] = ta.rsi(df_1m['Close'], length=14)
        df_1m['EMA9'] = ta.ema(df_1m['Close'], length=9)

        curr = df_1m.iloc[-1]
        prev = df_1m.iloc[-2]
        body = abs(curr['Close'] - curr['Open'])
        lower_wick = min(curr['Close'], curr['Open']) - curr['Low']
        upper_wick = curr['High'] - max(curr['Close'], curr['Open'])

        signal, color, msg = "WAIT", "#8b949e", "সঠিক সময়ের অপেক্ষা..."

        if trend_5m == "UP":
            if curr['RSI'] < 40:
                if lower_wick > (body * 0.8): signal, color, msg = "BUY ⬆️", "#3fb950", "৫মি ট্রেন্ড বুলিশ, রিভার্সাল কনফার্ম!"
                else: signal, color, msg = "BUY ⬆️", "#238636", "বুলিশ ট্রেন্ড কন্টিনিউশন।"
        elif trend_5m == "DOWN":
            if curr['RSI'] > 60:
                if upper_wick > (body * 0.8): signal, color, msg = "SELL ⬇️", "#f85149", "৫মি ট্রেন্ড বিয়ারিশ, রিভার্সাল কনফার্ম!"
                else: signal, color, msg = "SELL ⬇️", "#da3633", "বিয়ারিশ ট্রেন্ড কন্টিনিউশন।"

        ema_gap = abs(ema9_5m - ema21_5m)
        if ema_gap < (curr['Close'] * 0.00015): signal, color, msg = "RISK", "#d29922", "মার্কেট সাইডওয়েজ, ট্রেড এড়িয়ে চলুন।"

        return signal, color, msg, curr['Close'], curr['RSI'], trend_5m
    except: return None

# --- ৪. ইউজার ইন্টারফেস ---
st.title("👑 ARAFAT ULTRA VIP V15 Pro Dashboard")

if 'selected_pair' not in st.session_state:
    st.session_state.selected_pair = markets["MAJOR FOREX"][0]

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Quotex_logo.png", width=150)
    st.markdown("<h3 style='color:#58a6ff;'>📊 মার্কেট সিলেকশন</h3>", unsafe_allow_html=True)
    
    for category, pairs in markets.items():
        st.markdown(f"<p style='color:#8b949e; margin-bottom: 3px; font-weight:600; text-transform: uppercase; font-size:12px;'>{category}</p>", unsafe_allow_html=True)
        for pair in pairs:
            if st.button(f"{pair['icon']} {pair['label']}", key=pair['ticker']):
                st.session_state.selected_pair = pair
                st.rerun()
    
    st.divider()
    st.markdown("<div class='clock-widget'>Dhaka Clock: " + datetime.now(pytz.timezone('Asia/Dhaka')).strftime('%I:%M:%S %p') + "</div>", unsafe_allow_html=True)

pair = st.session_state.selected_pair
analysis = get_vip_analysis(pair['ticker'])

if analysis:
    prediction, sig_color, msg, price, rsi, trend = analysis
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"<div class='metric-card'><div class='metric-title'>{pair['icon']} SELECTED PAIR</div><div class='metric-value'>{pair['label']}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-card'><div class='metric-title'>🕒 CURRENT PRICE</div><div class='metric-value'>${price:.4f}</div></div>", unsafe_allow_html=True)
        
        now = datetime.now()
        rem_sec = 60 - now.second
        st.markdown(f"<div class='metric-card'><div class='metric-title'>⏳ CANDLE TIMER (1M)</div><div class='timer-widget'>{rem_sec}s</div><div class='metric-title'>NEXT CANDLE PREDICTION</div></div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='signal-card' style='border-color: {sig_color}; box-shadow: 0 0 50px rgba(88, 166, 255, {0.1 if prediction == "WAIT" else 0.3});'>
            <div class='signal-label' style='color:{sig_color if prediction != "WAIT" else "#8b949e"};'>👑 AR VIP PREDICTION</div>
            <h1 class='signal-main' style='color: {sig_color};'>{prediction}</h1>
            <p class='signal-status' style='color:{sig_color if prediction != "WAIT" else "#c9d1d9"};'>{msg}</p>
            <p class='signal-details'>RSI(1m): {rsi:.1f} | 5m TREND: {trend}</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📊 পেশাদার চার্ট এবং ম্যাল্টি-টাইমফ্রেম এনালাইসিস", expanded=True):
        st.markdown("<h4 style='color:#c9d1d9; margin-bottom:15px;'>১ মিনিটের ইন্ট্রাডে চার্ট এবং ইন্ডিকেটর</h4>", unsafe_allow_html=True)
        df_chart = yf.download(pair['ticker'], period="2h", interval="1m", progress=False)
        if isinstance(df_chart.columns, pd.MultiIndex): df_chart.columns = df_chart.columns.get_level_values(0)
        
        fig = go.Figure(data=[go.Candlestick(x=df_chart.index, open=df_chart['Open'], high=df_chart['High'], low=df_chart['Low'], close=df_chart['Close'], increasing_line_color='#3fb950', decreasing_line_color='#f85149', line_width=1)])
        fig.add_trace(go.Scatter(x=df_chart.index, y=ta.ema(df_chart['Close'], length=9), mode='lines', line=dict(color='#ffd900', width=1), name='EMA 9'))
        fig.add_trace(go.Scatter(x=df_chart.index, y=ta.ema(df_chart['Close'], length=21), mode='lines', line=dict(color='#ff4500', width=1), name='EMA 21'))
        
        fig.update_layout(template="plotly_dark", height=450, margin=dict(l=10, r=10, t=20, b=20), xaxis_rangeslider_visible=False, paper_bgcolor='rgba(13, 17, 23, 0.95)', plot_bgcolor='rgba(0,0,0,0)', yaxis=dict(linecolor="#30363d"), xaxis=dict(linecolor="#30363d"))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
else:
    st.error("Error: মার্কেট ডাটা লোড করা যাচ্ছে না। দয়া করে কিছুক্ষণ পর চেষ্টা করুন বা অন্য কোনো মার্কেট সিলেক্ট করুন।")

# অটো-রিফ্রেশ
time.sleep(1)
st.rerun()
