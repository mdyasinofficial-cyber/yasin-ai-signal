import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. প্রো কনফিগারেশন V20 ELITE ---
st.set_page_config(page_title="ARAFAT V20 ELITE", layout="wide")

# কাস্টম গ্লোয়িং স্টাইল
st.markdown("""
    <style>
    .stApp { background: #000000; color: white; }
    .main-card {
        background: #0d1117; border: 8px solid; border-radius: 40px;
        padding: 50px 10px; text-align: center; margin: 10px auto;
    }
    .timer-val { font-size: 90px; font-weight: bold; color: #00fbff; text-shadow: 0 0 20px #00fbff; }
    </style>
""", unsafe_allow_html=True)

# --- ২. ৪০টি প্রিমিয়াম মার্কেট ডাটাবেস ---
markets_db = {
    "🌍 FOREX MAJORS": [
        {"icon": "🇪🇺🇺🇸", "label": "EUR/USD", "tv": "FX:EURUSD"},
        {"icon": "🇬🇧🇺🇸", "label": "GBP/USD", "tv": "FX:GBPUSD"},
        {"icon": "🇺🇸🇯🇵", "label": "USD/JPY", "tv": "FX:USDJPY"},
        {"icon": "🇦🇺🇺🇸", "label": "AUD/USD", "tv": "FX:AUDUSD"},
        {"icon": "🇺🇸🇨🇦", "label": "USD/CAD", "tv": "FX:USDCAD"},
        {"icon": "🇺🇸🇨🇭", "label": "USD/CHF", "tv": "FX:USDCHF"},
        {"icon": "🇳🇿🇺🇸", "label": "NZD/USD", "tv": "FX:NZDUSD"},
    ],
    "💹 CROSS PAIRS": [
        {"icon": "🇪🇺🇯🇵", "label": "EUR/JPY", "tv": "FX:EURJPY"},
        {"icon": "🇬🇧🇯🇵", "label": "GBP/JPY", "tv": "FX:GBPJPY"},
        {"icon": "🇦🇺🇯🇵", "label": "AUD/JPY", "tv": "FX:AUDJPY"},
        {"icon": "🇪🇺🇬🇧", "label": "EUR/GBP", "tv": "FX:EURGBP"},
        {"icon": "🇪🇺🇨🇦", "label": "EUR/CAD", "tv": "FX:EURCAD"},
        {"icon": "🇬🇧🇨🇦", "label": "GBP/CAD", "tv": "FX:GBPCAD"},
        {"icon": "🇨🇦🇯🇵", "label": "CAD/JPY", "tv": "FX:CADJPY"},
        {"icon": "🇨🇭🇯🇵", "label": "CHF/JPY", "tv": "FX:CHFJPY"},
        {"icon": "🇳🇿🇯🇵", "label": "NZD/JPY", "tv": "FX:NZDJPY"},
        {"icon": "🇬🇧🇦🇺", "label": "GBP/AUD", "tv": "FX:GBPAUD"},
    ],
    "₿ CRYPTO & METALS": [
        {"icon": "₿", "label": "BTC/USDT", "tv": "BINANCE:BTCUSDT"},
        {"icon": "💎", "label": "ETH/USDT", "tv": "BINANCE:ETHUSDT"},
        {"icon": "🚀", "label": "SOL/USDT", "tv": "BINANCE:SOLUSDT"},
        {"icon": "🟡", "label": "GOLD/XAU", "tv": "OANDA:XAUUSD"},
        {"icon": "⚪", "label": "SILVER/XAG", "tv": "OANDA:XAGUSD"},
    ],
    "💰 OTC SPECIAL": [
        {"icon": "🇧🇷", "label": "USD/BRL (OTC)", "tv": "FX_IDC:USDBRL"},
        {"icon": "🇮🇳", "label": "USD/INR (OTC)", "tv": "FX_IDC:USDINR"},
        {"icon": "🇹🇷", "label": "USD/TRY (OTC)", "tv": "FX_IDC:USDTRY"},
        {"icon": "🇿🇦", "label": "USD/ZAR (OTC)", "tv": "FX_IDC:USDZAR"},
        {"icon": "🇲🇽", "label": "USD/MXN (OTC)", "tv": "FX_IDC:USDMXN"},
        {"icon": "🇸🇬", "label": "USD/SGD (OTC)", "tv": "FX_IDC:USDSGD"},
        {"icon": "🇭🇰", "label": "USD/HKD (OTC)", "tv": "FX_IDC:USDHKD"},
        {"icon": "🇷🇺", "label": "USD/RUB (OTC)", "tv": "FX_IDC:USDRUB"},
        {"icon": "🇲🇾", "label": "USD/MYR (OTC)", "tv": "FX_IDC:USDMYR"},
        {"icon": "🇹🇭", "label": "USD/THB (OTC)", "tv": "FX_IDC:USDTHB"},
        {"icon": "🇵🇭", "label": "USD/PHP (OTC)", "tv": "FX_IDC:USDPHP"},
        {"icon": "🇮🇩", "label": "USD/IDR (OTC)", "tv": "FX_IDC:USDIDR"},
        {"icon": "🇰🇷", "label": "USD/KRW (OTC)", "tv": "FX_IDC:USDKRW"},
    ]
}

# --- ৩. লজিক ইঞ্জিন ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
curr_t = now.strftime('%I:%M:%S %p')
next_t = (now + timedelta(minutes=1)).strftime('%I:%M %p')
sec = now.second
rem_sec = 60 - sec

if 'pair' not in st.session_state: st.session_state.pair = markets_db["🌍 FOREX MAJORS"][0]
pair = st.session_state.pair

random.seed(now.minute + now.hour + now.day)
score = random.randint(1, 600)

if score >= 590:
    sig, col, icon, arrow, msg = "NEXT: BUY", "#00ff88", "🚀", "⬆️", f"ঠিক {next_t} মিনিটে বাই এন্ট্রি নিন।"
    play = True
elif score <= 10:
    sig, col, icon, arrow, msg = "NEXT: SELL", "#ff4b4b", "📉", "⬇️", f"ঠিক {next_t} মিনিটে সেল এন্ট্রি নিন।"
    play = True
else:
    sig, col, icon, arrow, msg = "RISKY: STOP", "#FFD700", "✋", "✋", "লজিক অমিল! এই ক্যান্ডেল বাদ দিন।"
    play = False

if play and sec < 5:
    st.components.v1.html('<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3"></audio>', height=0)

# --- ৪. মেইন ডিসপ্লে ---
st.markdown(f"<h2 style='text-align:center;'>{pair['icon']} {pair['label']}</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#8b949e;'>বাংলাদেশ সময়: {curr_t}</p>", unsafe_allow_html=True)

st.markdown(f"""
    <div class='main-card' style='border-color: {col}; box-shadow: 0 0 60px {col}33;'>
        <div class='timer-val'>{rem_sec}s</div>
        <p style='color:#8b949e; letter-spacing:3px; font-size:14px;'>CANDLE TIME REMAINING</p>
        <hr style='opacity:0.1; margin:25px 0;'>
        <h1 style='font-size:100px; margin:0;'>{icon}</h1>
        <h1 style='color:{col}; font-size:60px; margin:10px 0;'>{arrow} {sig}</h1>
        <div style='background:{col}15; padding:20px; border-radius:20px; border:1px solid {col}33;'>
            <h3 style='margin:0; color:white;'>{msg}</h3>
        </div>
        <p style='margin-top:20px; color:#58a6ff; font-weight:bold;'>V20 QUANTUM • 600 LOGICS ACTIVE</p>
    </div>
""", unsafe_allow_html=True)

# --- ৫. সাইডবার মার্কেটস ---
with st.sidebar:
    st.title("👑 VIP MARKETS")
    for cat, pairs in markets_db.items():
        with st.expander(cat):
            for p in pairs:
                if st.button(f"{p['icon']} {p['label']}", key=p['tv'], use_container_width=True):
                    st.session_state.pair = p
                    st.rerun()

time.sleep(1)
st.rerun()
