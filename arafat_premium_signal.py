import streamlit as st
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime
import pytz
import time

# --- ১. পাসওয়ার্ড প্রোটেকশন ফাংশন ---
def check_password():
    if "password_correct" not in st.session_state:
        st.markdown("""
            <style>
            .login-box {
                padding: 40px; border-radius: 20px; background: #121212;
                border: 2px solid #00d2ff; text-align: center; margin-top: 50px;
            }
            .stTextInput>div>div>input {
                background-color: #1a1a1a; color: white; border: 1px solid #00d2ff;
            }
            </style>
            <div class='login-box'>
                <h2 style='color: #00d2ff; font-family: sans-serif;'>👑 ARAFAT PREMIUM VIP LOGIN</h2>
                <p style='color: #888;'>আপনার সিকিউরিটি কি (Key) প্রদান করুন</p>
            </div>
            """, unsafe_allow_html=True)
        
        password = st.text_input("পাসওয়ার্ড:", type="password", placeholder="এখানে লিখুন...")
        if st.button("Login Now"):
            if password == "Arafat@Vip#Quantum2026":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ ভুল পাসওয়ার্ড! সঠিক পাসওয়ার্ড দিয়ে চেষ্টা করুন।")
        return False
    return True

# পাসওয়ার্ড সঠিক হলে মূল অ্যাপ লোড হবে
if check_password():
    # --- ২. কনফিগারেশন ---
    st.set_page_config(page_title="ARAFAT VIP SIGNAL V13", layout="wide")

    # --- CSS স্টাইল (প্রিমিয়াম ডার্ক মোড) ---
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(to bottom, #000000, #020f1a); color: white; }
        .signal-box { 
            padding: 30px; border-radius: 25px; text-align: center; 
            border: 4px solid; background: rgba(0,0,0,0.9);
            box-shadow: 0px 0px 50px rgba(0,255,136,0.2);
            margin-top: 20px;
        }
        .martingale-card {
            background: #0a0a0a; padding: 20px; border-radius: 15px;
            border-left: 6px solid #ff4b4b; margin-top: 25px;
            box-shadow: 5px 5px 15px rgba(0,0,0,0.5);
        }
        .market-header { 
            color: #00d2ff; font-weight: bold; font-size: 28px; 
            text-align: center; text-transform: uppercase; letter-spacing: 2px;
        }
        </style>
        """, unsafe_allow_html=True)

    # --- ৩৫টি মার্কেটের লিস্ট (লোগোসহ) ---
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
        # লোকাল কারেন্সি
        "🇮🇳 USD/INR": "USDINR=X", "🇧🇩 USD/BDT": "BDT=X"
    }

    # --- সাইডবার কন্ট্রোল ---
    st.sidebar.markdown("<h1 style='color: #00d2ff; text-align: center;'>👑 ARAFAT VIP</h1>", unsafe_allow_html=True)
    st.sidebar.write("---")
    selected_label = st.sidebar.selectbox("🎯 মার্কেট সিলেক্ট করুন", list(markets.keys()))
    ticker = markets[selected_label]
    trade_amount = st.sidebar.number_input("ট্রেড অ্যামাউন্ট ($):", min_value=1, value=10)
    st.sidebar.write("---")
    st.sidebar.success("সিগন্যাল পাওয়ার পর দ্রুত ট্রেড প্লেস করুন।")

    # --- এনালাইসিস ইঞ্জিন ---
    def analyze_market(symbol):
        try:
            df = yf.download(symbol, period="1d", interval="1m", progress=False)
            if len(df) < 30: return "ERROR", "#555", "লোডিং হচ্ছে...", 50, 0
            
            df['RSI'] = ta.rsi(df['Close'], length=14)
            df['EMA20'] = ta.ema(df['Close'], length=20)
            
            rsi = df['RSI'].iloc[-1]
            price = df['Close'].iloc[-1]
            ema20 = df['EMA20'].iloc[-1]

            # প্রিমিয়াম সিগন্যাল লজিক
            if rsi < 32 and price < ema20:
                return "STRONG BUY ⬆️", "#00ff88", "বুলিশ রিভার্সাল কনফার্ম! আপ ট্রেড নিন।", rsi, price
            elif rsi > 68 and price > ema20:
                return "STRONG SELL ⬇️", "#ff4b4b", "বিয়ারিশ রিভার্সাল কনফার্ম! ডাউন ট্রেড নিন।", rsi, price
            elif rsi < 45:
                return "BUY ⬆️", "#2ecc71", "মার্কেট ঊর্ধ্বমুখী ট্রেন্ডে আছে।", rsi, price
            elif rsi > 55:
                return "SELL ⬇️", "#e74c3c", "মার্কেট নিম্নমুখী ট্রেন্ডে আছে।", rsi, price
            else:
                return "WAIT ✋", "#FFD700", "মার্কেট সাইডওয়েজ, সিগন্যালের অপেক্ষা করুন।", rsi, price
        except:
            return "ERROR", "#ff4b4b", "ডাটা পাওয়া যাচ্ছে না", 50, 0

    # --- মেইন ডিসপ্লে আপডেট ---
    prediction, color, status, rsi_val, current_price = analyze_market(ticker)
    now = datetime.now(pytz.timezone('Asia/Dhaka'))
    seconds = now.second
    rem_sec = 60 - seconds

    st.markdown(f"<p class='market-header'>{selected_label} | LIVE PRICE: ${current_price:.2f}</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1: st.markdown(f"#### 🕒 সময়: {now.strftime('%I:%M:%S %p')}")
    with col2: st.markdown(f"#### ⏳ ক্যান্ডেল শেষ হতে: `{rem_sec}s` বাকি")

    # সিগন্যাল টাইমিং (ক্যান্ডেল শেষ হওয়ার ২০ সেকেন্ড আগে)
    if seconds >= 40:
        st.markdown(f"""
            <div class='signal-box' style='border-color: {color};'>
                <p style='color: {color}; letter-spacing: 3px; font-weight: bold;'>👑 ARAFAT PREMIUM VIP V13</p>
                <h1 style='color: {color}; font-size: 80px; margin: 10px 0;'>{prediction}</h1>
                <h3 style='color: white; font-weight: 300;'>{status}</h3>
                <p style='font-size: 14px; opacity: 0.6;'>RSI: {rsi_val:.2f} | Time: {now.hour}:{now.minute + 1}:00</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class='signal-box' style='border-color: #333;'>
                <h1 style='font-size: 50px; color: #777;'>ANALYZING... 🛰️</h1>
                <p>পরবর্তী সিগন্যাল ২০ সেকেন্ডের মধ্যে আসছে...</p>
                <div style='width: 100%; background: #222; border-radius: 10px; height: 12px; margin-top: 15px;'>
                    <div style='width: {(seconds/40)*100}%; background: linear-gradient(to right, #00d2ff, #00ff88); height: 12px; border-radius: 10px;'></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # লস রিকভারি কার্ড
    if "BUY" in prediction or "SELL" in prediction:
        st.markdown(f"""
            <div class='martingale-card'>
                <h4 style='color: #ff4b4b; margin:0;'>🛡️ লস রিকভারি স্ট্রেটেজি</h4>
                <p style='margin:5px 0;'>ট্রেড লস হলে <b>মার্টিংগেল (২.৫ গুণ)</b> ব্যবহার করুন।</p>
                <p style='font-size: 20px;'>পরবর্তী ইনভেস্ট: <b style='color: #00ff88;'>${trade_amount * 2.5}</b></p>
            </div>
        """, unsafe_allow_html=True)

    # চার্ট ডিসপ্লে
    st.write("---")
    with st.expander("📊 লাইভ ক্যান্ডেলস্টিক চার্ট", expanded=True):
        df_chart = yf.download(ticker, period="1h", interval="1m", progress=False)
        fig = go.Figure(data=[go.Candlestick(
            x=df_chart.index, open=df_chart['Open'], high=df_chart['High'],
            low=df_chart['Low'], close=df_chart['Close'],
            increasing_line_color='#00ff88', decreasing_line_color='#ff4b4b'
        )])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=450, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

    # ১ সেকেন্ড পর পর অটো রিফ্রেশ
    time.sleep(1)
    st.rerun()
