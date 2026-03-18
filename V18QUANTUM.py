import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. প্রো কনফিগারেশন V19 ---
st.set_page_config(page_title="ARAFAT V19 ELITE", layout="wide")

SECURE_PASSWORD = "Arafat@Vip#Quantum2026"

# কাস্টম সিএসএস (সবকিছু এক স্ক্রিনে সাজানোর জন্য)
st.markdown("""
    <style>
    .stApp { background: #000000; color: white; }
    /* চার্ট এবং সিগন্যাল কার্ডের মাঝের গ্যাপ কমানো */
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    
    .signal-card {
        background: #0d1117; 
        border: 3px solid; 
        border-radius: 20px;
        padding: 15px; 
        text-align: center; 
        margin-top: 10px;
    }
    .timer-text {
        font-size: 24px;
        font-weight: bold;
        color: #00d2ff;
        text-shadow: 0 0 10px #00d2ff55;
    }
    .login-box {
        max-width: 400px; margin: 100px auto; padding: 40px;
        background: #161b22; border-radius: 20px; text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- ২. লগইন সিস্টেম ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.title("👑 V19 ELITE")
    pwd = st.text_input("পিন দিন", type="password")
    if st.button("UNLOCK V19 🚀", use_container_width=True):
        if pwd == SECURE_PASSWORD:
            st.session_state.auth = True
            st.rerun()
        else: st.error("ভুল পাসওয়ার্ড!")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- ৩. ৪০টি প্রিমিয়াম মার্কেট ডাটাবেস ---
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
    "💹 MINOR & CROSS": [
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
        {"icon": "🇪🇺🇦🇺", "label": "EUR/AUD", "tv": "FX:EURAUD"},
    ],
    "₿ CRYPTO": [
        {"icon": "₿", "label": "BTC/USDT", "tv": "BINANCE:BTCUSDT"},
        {"icon": "💎", "label": "ETH/USDT", "tv": "BINANCE:ETHUSDT"},
        {"icon": "🚀", "label": "SOL/USDT", "tv": "BINANCE:SOLUSDT"},
        {"icon": "🔶", "label": "BNB/USDT", "tv": "BINANCE:BNBUSDT"},
        {"icon": "🔷", "label": "XRP/USDT", "tv": "BINANCE:XRPUSDT"},
        {"icon": "🐕", "label": "DOGE/USDT", "tv": "BINANCE:DOGEUSDT"},
        {"icon": "🔹", "label": "ADA/USDT", "tv": "BINANCE:ADAUSDT"},
    ],
    "💰 OTC & METALS": [
        {"icon": "🟡", "label": "GOLD (XAU)", "tv": "OANDA:XAUUSD"},
        {"icon": "⚪", "label": "SILVER (XAG)", "tv": "OANDA:XAGUSD"},
        {"icon": "🇧🇷", "label": "USD/BRL (OTC)", "tv": "FX_IDC:USDBRL"},
        {"icon": "🇮🇳", "label": "USD/INR (OTC)", "tv": "FX_IDC:USDINR"},
        {"icon": "🇹🇷", "label": "USD/TRY", "tv": "FX_IDC:USDTRY"},
        {"icon": "🇿🇦", "label": "USD/ZAR", "tv": "FX_IDC:USDZAR"},
        {"icon": "🇲🇽", "label": "USD/MXN", "tv": "FX_IDC:USDMXN"},
        {"icon": "🇸🇬", "label": "USD/SGD", "tv": "FX_IDC:USDSGD"},
        {"icon": "🇭🇰", "label": "USD/HKD", "tv": "FX_IDC:USDHKD"},
        {"icon": "🇩🇰", "label": "USD/DKK", "tv": "FX_IDC:USDDKK"},
        {"icon": "🇸🇪", "label": "USD/SEK", "tv": "FX_IDC:USDSEK"},
        {"icon": "🇳🇴", "label": "USD/NOK", "tv": "FX_IDC:USDNOK"},
    ]
}

# --- ৪. টাইম এবং লজিক ইঞ্জিন ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
sec = now.second
rem_sec = 60 - sec
next_candle = (now + timedelta(minutes=1)).strftime('%I:%M %p')

if 'pair' not in st.session_state:
    st.session_state.pair = markets_db["🌍 FOREX MAJORS"][0]
pair = st.session_state.pair

# ৬০০ লজিক
random.seed(now.minute + now.hour + now.day)
logic_score = random.randint(1, 600)

if logic_score >= 590: 
    sig, col, icon, msg = "NEXT: BUY ⬆️", "#00ff88", "📈", f"ঠিক {next_candle} মিনিটে BUY নিন।"
    play_s = True
elif logic_score <= 10: 
    sig, col, icon, msg = "NEXT: SELL ⬇️", "#ff4b4b", "📉", f"ঠিক {next_candle} মিনিটে SELL নিন।"
    play_s = True
else: 
    sig, col, icon, msg = "RISKY: STOP ✋", "#FFD700", "✋", "লজিক অমিল! এই ক্যান্ডেল বাদ দিন।"
    play_s = False

# অডিও অ্যালার্ট (প্রতি মিনিটের শুরুতে ১ বার)
if play_s and sec < 5:
    st.components.v1.html('<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3"></audio>', height=0)

# --- ৫. মেইন ড্যাশবোর্ড (সাজানো ইন্টারফেস) ---
# উপরে মার্কেট লোগো এবং নাম
st.markdown(f"<h3 style='text-align:center; margin-bottom:0;'>{pair['icon']} {pair['label']} ELITE</h3>", unsafe_allow_html=True)

# ১. চার্ট (মাঝখানে থাকবে)
tv_url = f"https://s.tradingview.com/widgetembed/?symbol={pair['tv']}&interval=1&theme=dark"
st.components.v1.html(f'<iframe src="{tv_url}" width="100%" height="380" frameborder="0"></iframe>', height=380)

# ২. সিগন্যাল কার্ড এবং টাইমার (নিচে এক লাইনে)
st.markdown(f"""
    <div class='signal-card' style='border-color: {col}; box-shadow: 0 0 30px {col}22;'>
        <div style='display: flex; justify-content: space-around; align-items: center;'>
            <div style='text-align: left;'>
                <span class='timer-text'>⏳ {rem_sec}s</span><br>
                <small style='color:#8b949e;'>ক্যান্ডেল শেষ</small>
            </div>
            <div>
                <h2 style='color:{col}; margin:0;'>{icon} {sig}</h2>
                <b style='color:white; font-size:14px;'>{msg}</b>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ৩. সাইডবার (মার্কেট সিলেকশন)
with st.sidebar:
    st.header("👑 VIP MARKETS")
    if st.button("LOGOUT 🔐", use_container_width=True):
        st.session_state.auth = False
        st.rerun()
    st.write("---")
    for cat, pairs in markets_db.items():
        with st.expander(cat):
            for p in pairs:
                if st.button(f"{p['icon']} {p['label']}", key=p['tv'], use_container_width=True):
                    st.session_state.pair = p
                    st.rerun()

# অটো রিফ্রেশ (১ সেকেন্ড পর পর)
time.sleep(1)
st.rerun()


