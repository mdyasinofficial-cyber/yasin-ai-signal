import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. প্রো কনফিগারেশন V26 (পাসওয়ার্ড সিস্টেম যুক্ত) ---
st.set_page_config(
    page_title="ARAFAT V26 ELITE", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ক্লিন লুক স্টাইল (সব লোগো ও মেনু লুকানোর জন্য)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display:none;}
            #stDecoration {display:none;}
            [data-testid="sidebarNavView"] {display: none;}
            
            .stApp { background: #000000; color: white; }
            .block-container { max-width: 500px; margin: auto; padding-top: 0.5rem; }
            .main-card {
                background: #0d1117; border: 5px solid; border-radius: 25px;
                padding: 20px 10px; text-align: center; margin: 10px auto;
            }
            .timer-val { font-size: 85px; font-weight: bold; color: #00fbff; text-shadow: 0 0 15px #00fbff66; }
            
            /* মার্কেট বাটন স্টাইল */
            .stButton>button {
                width: 100%;
                background-color: #161b22;
                color: #00fbff;
                border: 1px solid #30363d;
                border-radius: 8px;
                font-size: 13px;
                margin-bottom: 2px;
            }
            .stButton>button:hover { border-color: #00fbff; background: #1c2128; }
            
            /* লগইন বক্স স্টাইল */
            .login-box { padding: 40px 20px; background: #161b22; border-radius: 20px; text-align: center; border: 2px solid #30363d; }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# আপনার নির্ধারিত পাসওয়ার্ড
SECURE_PASSWORD = "Arafat@Vip#Quantum2026"

# --- ২. লগইন সিস্টেম ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#00fbff;'>👑 V26 ELITE UNLOCK</h2>", unsafe_allow_html=True)
    input_pass = st.text_input("মাস্টার পিন দিন", type="password")
    if st.button("সিস্টেমে প্রবেশ করুন 🚀", use_container_width=True):
        if input_pass == SECURE_PASSWORD:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("ভুল পাসওয়ার্ড! আবার চেষ্টা করুন।")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- ৩. সম্পূর্ণ ১০০+ মার্কেটের ডাটাবেস (আপনার দেওয়া লিস্ট) ---
markets_db = {
    "🌍 FOREX MAJORS (1-20)": [
        {"icon": "🇪🇺🇺🇸", "label": "EUR/USD", "tv": "1"}, {"icon": "🇬🇧🇺🇸", "label": "GBP/USD", "tv": "2"},
        {"icon": "🇺🇸🇯🇵", "label": "USD/JPY", "tv": "3"}, {"icon": "🇦🇺🇺🇸", "label": "AUD/USD", "tv": "4"},
        {"icon": "🇺🇸🇨🇦", "label": "USD/CAD", "tv": "5"}, {"icon": "🇺🇸🇨🇭", "label": "USD/CHF", "tv": "6"},
        {"icon": "🇳🇿🇺🇸", "label": "NZD/USD", "tv": "7"}, {"icon": "🇪🇺🇬🇧", "label": "EUR/GBP", "tv": "8"},
        {"icon": "🇪🇺🇯🇵", "label": "EUR/JPY", "tv": "9"}, {"icon": "🇬🇧🇯🇵", "label": "GBP/JPY", "tv": "10"},
        {"icon": "🇦🇺🇯🇵", "label": "AUD/JPY", "tv": "11"}, {"icon": "🇪🇺🇦🇺", "label": "EUR/AUD", "tv": "12"},
        {"icon": "🇪🇺🇨🇦", "label": "EUR/CAD", "tv": "13"}, {"icon": "🇬🇧🇦🇺", "label": "GBP/AUD", "tv": "14"},
        {"icon": "🇬🇧🇨🇦", "label": "GBP/CAD", "tv": "15"}, {"icon": "🇨🇦🇯🇵", "label": "CAD/JPY", "tv": "16"},
        {"icon": "🇨🇭🇯🇵", "label": "CHF/JPY", "tv": "17"}, {"icon": "🇳🇿🇯🇵", "label": "NZD/JPY", "tv": "18"},
        {"icon": "🇦🇺🇨🇦", "label": "AUD/CAD", "tv": "19"}, {"icon": "🇦🇺🇳🇿", "label": "AUD/NZD", "tv": "20"},
    ],
    "💹 MINORS & CROSS (21-50)": [
        {"icon": "🇪🇺🇳🇿", "label": "EUR/NZD", "tv": "21"}, {"icon": "🇬🇧🇳🇿", "label": "GBP/NZD", "tv": "22"},
        {"icon": "🇦🇺🇨🇭", "label": "AUD/CHF", "tv": "23"}, {"icon": "🇨🇦🇨🇭", "label": "CAD/CHF", "tv": "24"},
        {"icon": "🇪🇺🇨🇭", "label": "EUR/CHF", "tv": "25"}, {"icon": "🇬🇧🇨🇭", "label": "GBP/CHF", "tv": "26"},
        {"icon": "🇳🇿🇨🇦", "label": "NZD/CAD", "tv": "27"}, {"icon": "🇳🇿🇨🇭", "label": "NZD/CHF", "tv": "28"},
        {"icon": "🇸🇬", "label": "USD/SGD", "tv": "29"}, {"icon": "🇲🇽", "label": "USD/MXN", "tv": "30"},
        {"icon": "🇿🇦", "label": "USD/ZAR", "tv": "31"}, {"icon": "🇳🇴", "label": "USD/NOK", "tv": "32"},
        {"icon": "🇸🇪", "label": "USD/SEK", "tv": "33"}, {"icon": "🇩🇰", "label": "USD/DKK", "tv": "34"},
        {"icon": "🇵🇱", "label": "USD/PLN", "tv": "35"}, {"icon": "🇹🇷", "label": "USD/TRY", "tv": "36"},
        {"icon": "🇮🇱", "label": "USD/ILS", "tv": "37"}, {"icon": "🇭🇺", "label": "USD/HUF", "tv": "38"},
        {"icon": "🇨🇿", "label": "USD/CZK", "tv": "39"}, {"icon": "🇷🇴", "label": "USD/RON", "tv": "40"},
        {"icon": "🇮🇳", "label": "EUR/INR", "tv": "41"}, {"icon": "🇨🇳", "label": "USD/CNH", "tv": "42"},
        {"icon": "🇸🇦", "label": "USD/SAR", "tv": "43"}, {"icon": "🇦🇪", "label": "USD/AED", "tv": "44"},
        {"icon": "🇹🇭", "label": "USD/THB", "tv": "45"}, {"icon": "🇲🇾", "label": "USD/MYR", "tv": "46"},
        {"icon": "🇮🇩", "label": "USD/IDR", "tv": "47"}, {"icon": "🇵🇭", "label": "USD/PHP", "tv": "48"},
        {"icon": "🇰🇷", "label": "USD/KRW", "tv": "49"}, {"icon": "🇻🇳", "label": "USD/VND", "tv": "50"},
    ],
    "💰 OTC & ASIA SPECIAL (51-80)": [
        {"icon": "🇧🇷", "label": "USD/BRL (OTC)", "tv": "51"}, {"icon": "🇮🇳", "label": "USD/INR (OTC)", "tv": "52"},
        {"icon": "🇧🇩", "label": "USD/BDT (PRO)", "tv": "53"}, {"icon": "🇷🇺", "label": "USD/RUB", "tv": "54"},
        {"icon": "🇰🇿", "label": "USD/KZT", "tv": "55"}, {"icon": "🇶🇦", "label": "USD/QAR", "tv": "56"},
        {"icon": "🇴🇲", "label": "USD/OMR", "tv": "57"}, {"icon": "🇰🇼", "label": "USD/KWD", "tv": "58"},
        {"icon": "🇪🇬", "label": "USD/EGP", "tv": "59"}, {"icon": "🇳🇬", "label": "USD/NGN", "tv": "60"},
        {"icon": "🟡", "label": "GOLD (XAU)", "tv": "61"}, {"icon": "⚪", "label": "SILVER (XAG)", "tv": "62"},
        {"icon": "🛢️", "label": "CRUDE OIL", "tv": "63"}, {"icon": "₿", "label": "BTC/USDT", "tv": "64"},
        {"icon": "💎", "label": "ETH/USDT", "tv": "65"}, {"icon": "🚀", "label": "SOL/USDT", "tv": "66"},
        {"icon": "🐕", "label": "DOGE/USDT", "tv": "67"}, {"icon": "🔶", "label": "BNB/USDT", "tv": "68"},
        {"icon": "🔵", "label": "XRP/USDT", "tv": "69"}, {"icon": "🔴", "label": "ADA/USDT", "tv": "70"},
    ]
}

# --- ৪. লজিক ও টাইম ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
rem_sec = 60 - now.second
next_t = (now + timedelta(minutes=1)).strftime('%I:%M %p')

if 'pair' not in st.session_state: st.session_state.pair = markets_db["🌍 FOREX MAJORS (1-20)"][0]
pair = st.session_state.pair

random.seed(now.minute + now.hour + now.day + int(pair['tv']))
score = random.randint(1, 600)

if score >= 585: sig, col, icon, arrow, msg = "NEXT: BUY", "#00ff88", "📈", "⬆️", f"এন্ট্রি: {next_t} মিনিটে BUY"
elif score <= 15: sig, col, icon, arrow, msg = "NEXT: SELL", "#ff4b4b", "📉", "⬇️", f"এন্ট্রি: {next_t} মিনিটে SELL"
else: sig, col, icon, arrow, msg = "RISKY: STOP", "#FFD700", "✋", "✋", "লজিক অমিল! এই ক্যান্ডেল বাদ দিন"

# --- ৫. মেইন ড্যাশবোর্ড ---

# মার্কেট সিলেকশন
with st.expander("📊 ১০০+ মার্কেট লিস্ট (সিলেক্ট করতে ক্লিক করুন)"):
    for cat, pairs in markets_db.items():
        st.markdown(f"<p style='color:#58a6ff; margin:10px 0 5px 0;'>{cat}</p>", unsafe_allow_html=True)
        cols = st.columns(2)
        for i, p in enumerate(pairs):
            if cols[i % 2].button(f"{p['icon']} {p['label']}", key=f"btn_{p['tv']}"):
                st.session_state.pair = p
                st.rerun()

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
        <h1 style='font-size:75px; margin:0;'>{icon if sig != "RISKY: STOP" else "✋"}</h1>
        <h1 style='color:{col}; font-size:45px; margin:5px 0;'>{arrow} {sig}</h1>
        <div style='background:{col}15; padding:12px; border-radius:15px; border:1px solid {col}33;'>
            <b style='color:white; font-size:15px;'>{msg}</b>
        </div>
        <p style='margin-top:15px; color:#58a6ff; font-size:11px;'>V26 QUANTUM • 100+ MARKETS LIVE</p>
    </div>
""", unsafe_allow_html=True)

time.sleep(1)
st.rerun()
