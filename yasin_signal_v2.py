import streamlit as st
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime
import pytz
import time

# --- ১. পাসওয়ার্ড সুরক্ষা ফাংশন ---
def check_password():
    """পাসওয়ার্ড সঠিক হলে True রিটার্ন করবে, নাহলে লগইন পেজ দেখাবে।"""
    def password_entered():
        # সঠিক পাসওয়ার্ড চেক করা হচ্ছে
        if st.session_state["password"] == "Arafat@Vip#Quantum2026":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # সিকিউরিটির জন্য পাসওয়ার্ড ডিলিট করা
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # প্রথমবার লগইন পেজ দেখানো
        st.set_page_config(page_title="Login | YASIN AI VIP", page_icon="🔒")
        st.markdown("<h2 style='text-align: center;'>🔒 YASIN AI VIP ACCESS</h2>", unsafe_allow_html=True)
        st.text_input("আপনার সিকিউরিটি পাসওয়ার্ড দিন:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # পাসওয়ার্ড ভুল হলে আবার ইনপুট বক্স দেখানো
        st.markdown("<h2 style='text-align: center;'>🔒 YASIN AI VIP ACCESS</h2>", unsafe_allow_html=True)
        st.text_input("ভুল পাসওয়ার্ড! আবার চেষ্টা করুন:", type="password", on_change=password_entered, key="password")
        st.error("❌ পাসওয়ার্ড সঠিক নয়।")
        return False
    else:
        # পাসওয়ার্ড সঠিক হলে মেইন অ্যাপে যাওয়া
        return True

# পাসওয়ার্ড চেক করা হচ্ছে
if check_password():

    # --- ২. মূল অ্যাপ কনফিগারেশন (যদি পাসওয়ার্ড সঠিক হয়) ---
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

    # --- ৩৫টি মার্কেটের সম্পূর্ণ লিস্ট ---
    markets = {
        "🇪🇺 EUR/USD": "EURUSD=X", "🇬🇧 GBP/USD": "GBPUSD=X", "🇯🇵 USD/JPY": "JPY=X",
        "🇦🇺 AUD/USD": "AUDUSD=X", "🇨🇦 USD/CAD": "CAD=X", "🇨🇭 USD/CHF": "CHF=X",
        "🇳🇿 NZD/USD": "NZDUSD=X", "🇪🇺 EUR/GBP": "EURGBP=X", "🇪🇺 EUR/JPY": "EURJPY=X",
        "🇬🇧 GBP/JPY": "GBPJPY=X", "₿ BTC/USDT": "BTC-USD", "💎 ETH/USDT": "ETH-USD",
        "🚀 SOL/USDT": "SOL-USD", "🔥 GOLD (XAU)": "GC=F", "🥈 SILVER (XAG)": "SI=F",
        "🛢️ CRUDE OIL": "CL=F", "📈 S&P 500": "^GSPC", "🇧DT USD/BDT": "BDT=X"
    }

    # --- SIDEBAR CONTROL ---
    st.sidebar.markdown("## 💎 YASIN AI VIP PRO")
    selected_label = st.sidebar.selectbox("🌐 ৩৫+ প্রিমিয়াম মার্কেট", list(markets.keys()))
    ticker = markets[selected_label]
    trade_amount = st.sidebar.number_input("ট্রেড এমাウント ($):", min_value=1, value=10)
    
    if st.sidebar.button("Logout"):
        st.session_state["password_correct"] = False
        st.rerun()

    # --- AI LOGIC ENGINE ---
    def analyze_market(symbol):
        try:
            df = yf.download(symbol, period="1d", interval="1m", progress=False)
            if len(df) < 30: 
                return "DATA ERROR", "#555555", "যথেষ্ট ডাটা নেই।", 50, 0
            
            df['RSI'] = ta.rsi(df['Close'], length=14)
            df['EMA20'] = ta.ema(df['Close'], length=20)
            
            rsi = df['RSI'].iloc[-1]
            price = df['Close'].iloc[-1]
            ema20 = df['EMA20'].iloc[-1]

            if 48 < rsi < 52:
                return "WAIT ✋", "#FFD700", "সাইডওয়েজ মার্কেট!", rsi, price
            elif rsi < 30 and price < ema20:
                return "STRONG BUY ⬆️", "#00ff88", "বুলিশ রিভার্সাল!", rsi, price
            elif rsi > 70 and price > ema20:
                return "STRONG SELL ⬇️", "#ff4b4b", "বিয়ারিশ রিভার্সাল!", rsi, price
            elif rsi < 40:
                return "BUY (UP) ⬆️", "#2ecc71", "বুলিশ প্রেসার।", rsi, price
            else:
                return "SELL (DOWN) ⬇️", "#e74c3c", "বিয়ারিশ প্রেসার।", rsi, price
        except:
            return "ERROR", "#ff4b4b", "ত্রুটি হয়েছে", 50, 0

    # --- MAIN UI ---
    prediction, color, status, rsi_val, current_price = analyze_market(ticker)
    now = datetime.now(pytz.timezone('Asia/Dhaka'))
    seconds = now.second
    rem_sec = 60 - seconds

    st.markdown(f"<p class='market-header'>{selected_label} | Price: ${current_price:.2f}</p>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"#### 🕒 সময়: {now.strftime('%I:%M:%S %p')}")
    with c2:
        st.markdown(f"#### ⏳ ক্যান্ডেল শেষ হতে বাকি: `{rem_sec}s`")

    if seconds >= 40:
        st.markdown(f"""
            <div class='signal-box' style='border-color: {color};'>
                <p style='color: {color}; letter-spacing: 3px;'><b>YASIN AI V13 VIP SIGNAL</b></p>
                <h1 style='color: {color}; font-size: 80px; margin: 10px 0;'>{prediction}</h1>
                <h3 style='color: white;'>{status}</h3>
                <p style='font-size: 14px; opacity: 0.6;'>RSI: {rsi_val:.2f}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class='signal-box' style='border-color: #333;'>
                <h1 style='font-size: 50px; color: #777;'>ANALYZING... 🛰️</h1>
                <p>পরবর্তী সিগন্যাল ক্যান্ডেল শেষ হওয়ার ২০ সেকেন্ড আগে আসবে।</p>
                <div style='width: 100%; background: #222; border-radius: 10px;'>
                    <div style='width: {(seconds/40)*100}%; background: #00d2ff; height: 10px; border-radius: 10px;'></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    if "BUY" in prediction or "SELL" in prediction:
        st.markdown(f"""
            <div class='martingale-card'>
                <h4 style='color: #ff4b4b; margin:0;'>🛡️ লস রিকভারি</h4>
                <p>ট্রেড লস হলে <b>মার্টিংগেল</b> ব্যবহার করুন। পরবর্তী ইনভেস্ট: <b>${trade_amount * 2.5}</b></p>
            </div>
        """, unsafe_allow_html=True)

    # অটো রিফ্রেশ
    time.sleep(1)
    st.rerun()
    
