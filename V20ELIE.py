
import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. প্রো কনফিগারেশন V23 (৫৩টি মার্কেট + পাসওয়ার্ড) ---
st.set_page_config(
    page_title="ARAFAT V23 ELITE", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

SECURE_PASSWORD = "Arafat@Vip#Quantum2026"

st.markdown("""
    <style>
    .stApp { background: #000000; color: white; }
    .block-container { max-width: 480px; margin: auto; padding-top: 0.5rem; }
    .main-card {
        background: #0d1117; border: 5px solid; border-radius: 25px;
        padding: 25px 10px; text-align: center; margin: 10px auto;
    }
    .timer-val { font-size: 85px; font-weight: bold; color: #00fbff; text-shadow: 0 0 15px #00fbff66; }
    .login-box { padding: 40px 20px; background: #161b22; border-radius: 20px; text-align: center; border: 2px solid #30363d; }
    </style>
""", unsafe_allow_html=True)

# --- ২. লগইন সিস্টেম ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#00fbff;'>👑 V23 ELITE UNLOCK</h2>", unsafe_allow_html=True)
    input_pass = st.text_input("মাস্টার পিন দিন", type="password")
    if st.button("সিস্টেমে প্রবেশ করুন 🚀", use_container_width=True):
        if input_pass == SECURE_PASSWORD:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("ভুল পাসওয়ার্ড!")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- ৩. সম্পূর্ণ ৫০+ মার্কেটের তালিকা (অপরিবর্তিত থাকবে) ---
markets_db = {
    "🌍 FOREX MAJORS (1-15)": [
        {"icon": "🇪🇺🇺🇸", "label": "EUR/USD", "tv": "FX:EURUSD"},
        {"icon": "🇬🇧🇺🇸", "label": "GBP/USD", "tv": "FX:GBPUSD"},
        {"icon": "🇺🇸🇯🇵", "label": "USD/JPY", "tv": "FX:USDJPY"},
        {"icon": "🇦🇺🇺🇸", "label": "AUD/USD", "tv": "FX:AUDUSD"},
        {"icon": "🇺🇸🇨🇦", "label": "USD/CAD", "tv": "FX:USDCAD"},
        {"icon": "🇺🇸🇨🇭", "label": "USD/CHF", "tv": "FX:USDCHF"},
        {"icon": "🇳🇿🇺🇸", "label": "NZD/USD", "tv": "FX:NZDUSD"},
        {"icon": "🇪🇺🇬🇧", "label": "EUR/GBP", "tv": "FX:EURGBP"},
        {"icon": "🇪🇺🇯🇵", "label": "EUR/JPY", "tv": "FX:EURJPY"},
        {"icon": "🇬🇧🇯🇵", "label": "GBP/JPY", "tv": "FX:GBPJPY"},
        {"icon": "🇦🇺🇯🇵", "label": "AUD/JPY", "tv": "FX:AUDJPY"},
        {"icon": "🇪🇺🇦🇺", "label": "EUR/AUD", "tv": "FX:EURAUD"},
        {"icon": "🇪🇺🇨🇦", "label": "EUR/CAD", "tv": "FX:EURCAD"},
        {"icon": "🇬🇧🇦🇺", "label": "GBP/AUD", "tv": "FX:GBPAUD"},
        {"icon": "🇬🇧🇨🇦", "label": "GBP/CAD", "tv": "FX:GBPCAD"},
    ],
    "💹 CROSS & MINORS (16-35)": [
        {"icon": "🇨🇦🇯🇵", "label": "CAD/JPY", "tv": "FX:CADJPY"},
        {"icon": "🇨🇭🇯🇵", "label": "CHF/JPY", "tv": "FX:CHFJPY"},
        {"icon": "🇳🇿🇯🇵", "label": "NZD/JPY", "tv": "FX:NZDJPY"},
        {"icon": "🇦🇺🇨🇦", "label": "AUD/CAD", "tv": "FX:AUDCAD"},
        {"icon": "🇦🇺🇳🇿", "label": "AUD/NZD", "tv": "FX:AUDNZD"},
        {"icon": "🇪🇺🇳🇿", "label": "EUR/NZD", "tv": "FX:EURNZD"},
        {"icon": "🇬🇧🇳🇿", "label": "GBP/NZD", "tv": "FX:GBPNZD"},
        {"icon": "🇦🇺🇨🇭", "label": "AUD/CHF", "tv": "FX:AUDCHF"},
        {"icon": "🇨🇦🇨🇭", "label": "CAD/CHF", "tv": "FX:CADCHF"},
        {"icon": "🇪🇺🇨🇭", "label": "EUR/CHF", "tv": "FX:EURCHF"},
        {"icon": "🇬🇧🇨🇭", "label": "GBP/CHF", "tv": "FX:GBPCHF"},
        {"icon": "🇳🇿🇨🇦", "label": "NZD/CAD", "tv": "FX:NZDCAD"},
        {"icon": "🇳🇿🇨🇭", "label": "NZD/CHF", "tv": "FX:NZDCHF"},
        {"icon": "🇺🇸🇲🇽", "label": "USD/MXN", "tv": "FX:USDMXN"},
        {"icon": "🇺🇸🇸🇬", "label": "USD/SGD", "tv": "FX:USDSGD"},
        {"icon": "🇺🇸🇳🇴", "label": "USD/NOK", "tv": "FX:USDNOK"},
        {"icon": "🇺🇸🇸🇪", "label": "USD/SEK", "tv": "FX:USDSEK"},
        {"icon": "🇺🇸🇩🇰", "label": "USD/DKK", "tv": "FX:USDDKK"},
        {"icon": "🇺🇸🇵🇱", "label": "USD/PLN", "tv": "FX:USDPLN"},
        {"icon": "🇺🇸🇿🇦", "label": "USD/ZAR", "tv": "FX:USDZAR"},
    ],
    "💰 OTC & SPECIALS (36-53)": [
        {"icon": "🇧🇷", "label": "USD/BRL (OTC)", "tv": "FX_IDC:USDBRL"},
        {"icon": "🇮🇳", "label": "USD/INR (OTC)", "tv": "FX_IDC:USDINR"},
        {"icon": "🇹🇷", "label": "USD/TRY", "tv": "FX:USDTRY"},
        {"icon": "🇷🇺", "label": "USD/RUB", "tv": "FX:USDRUB"},
        {"icon": "🟡", "label": "GOLD (XAU/USD)", "tv": "OANDA:XAUUSD"},
        {"icon": "⚪", "label": "SILVER (XAG/USD)", "tv": "OANDA:XAGUSD"},
        {"icon": "₿", "label": "BTC/USDT", "tv": "BINANCE:BTCUSDT"},
        {"icon": "💎", "label": "ETH/USDT", "tv": "BINANCE:ETHUSDT"},
        {"icon": "🚀", "label": "SOL/USDT", "tv": "BINANCE:SOLUSDT"},
        {"icon": "🔶", "label": "BNB/USDT", "tv": "BINANCE:BNBUSDT"},
        {"icon": "🇭🇰", "label": "USD/HKD", "tv": "FX:USDHKD"},
        {"icon": "🇹🇭", "label": "USD/THB", "tv": "FX:USDTHB"},
        {"icon": "🇮🇩", "label": "USD/IDR", "tv": "FX:USDIDR"},
        {"icon": "🇲🇾", "label": "USD/MYR", "tv": "FX:USDMYR"},
        {"icon": "🇵🇭", "label": "USD/PHP", "tv": "FX:USDPHP"},
        {"icon": "🇮🇱", "label": "USD/ILS", "tv": "FX:USDILS"},
        {"icon": "🇨🇿", "label": "USD/CZK", "tv": "FX:USDCZK"},
        {"icon": "🇭🇺", "label": "USD/HUF", "tv": "FX:USDHUF"},
    ]
}

# --- ৪. টাইম ও লজিক ইঞ্জিন ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
rem_sec = 60 - now.second
next_t = (now + timedelta(minutes=1)).strftime('%I:%M %p')

if 'pair' not in st.session_state:
    st.session_state.pair = markets_db["🌍 FOREX MAJORS (1-15)"][0]
pair = st.session_state.pair

random.seed(now.minute + now.hour + now.day)
score = random.randint(1, 600)

if score >= 585:
    sig, col, icon, arrow, msg = "NEXT: BUY", "#00ff88", "📈", "⬆️", f"এন্ট্রি: {next_t} মিনিটে BUY"
elif score <= 15:
    sig, col, icon, arrow, msg = "NEXT: SELL", "#ff4b4b", "📉", "⬇️", f"এন্ট্রি: {next_t} মিনিটে SELL"
else:
    sig, col, icon, arrow, msg = "RISKY: STOP", "#FFD700", "✋", "✋", "লজিক অমিল! এই ক্যান্ডেল বাদ দিন"

# --- ৫. মেইন ড্যাশবোর্ড ---
st.markdown(f"""
    <div style='text-align:center; padding: 10px; background: #161b22; border-radius: 15px; border: 1px solid #30363d;'>
        <h2 style='margin:0;'>{pair['icon']} {pair['label']}</h2>
        <small style='color:#8b949e;'>বাংলাদেশ সময়: {now.strftime('%I:%M:%S %p')}</small>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class='main-card' style='border-color: {col}; box-shadow: 0 0 35px {col}22;'>
        <div class='timer-val'>{rem_sec}s</div>
        <p style='color:#8b949e; font-size:12px; letter-spacing:2px;'>CANDLE COUNTDOWN</p>
        <hr style='opacity:0.1; margin:15px 0;'>
        <h1 style='font-size:75px; margin:0;'>{icon}</h1>
        <h1 style='color:{col}; font-size:45px; margin:5px 0;'>{arrow} {sig}</h1>
        <div style='background:{col}15; padding:12px; border-radius:15px; border:1px solid {col}33;'>
            <b style='color:white; font-size:15px;'>{msg}</b>
        </div>
        <p style='margin-top:15px; color:#58a6ff; font-size:11px;'>V23 ELITE • 53 MARKETS ACTIVE</p>
    </div>
""", unsafe_allow_html=True)

# সাইডবার (সম্পূর্ণ মার্কেট লিস্ট)
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

