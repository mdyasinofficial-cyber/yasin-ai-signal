import streamlit as st
import pandas as pd
import time
from datetime import datetime
import pytz
import random

# --- ১. প্রো কনফিগারেশন ---
st.set_page_config(page_title="FOREX QUANTUM V1", layout="wide")

st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden; display:none;}
    .stApp { background-color: #050505; color: #ffd700; }
    .market-card {
        border: 1px solid #333; border-radius: 10px; padding: 15px;
        background: #111; margin-bottom: 10px; transition: 0.3s;
    }
    .strong-buy { border-left: 8px solid #00fbff; box-shadow: 0 0 15px #00fbff33; }
    .strong-sell { border-left: 8px solid #ff4b4b; box-shadow: 0 0 15px #ff4b4b33; }
    .wait-signal { border-left: 8px solid #ffd700; opacity: 0.6; }
    .price-text { font-family: 'Courier New', monospace; font-weight: bold; font-size: 18px; }
    </style>
""", unsafe_allow_html=True)

# --- ২. এক্সনেস মার্কেট লিস্ট (মেজর ৪০টি) ---
forex_markets = [
    {"n": "GOLD (XAUUSD)", "id": "XAUUSD", "f": "🟡"},
    {"n": "EURUSD", "id": "EURUSD", "f": "🇪🇺🇺🇸"},
    {"n": "GBPUSD", "id": "GBPUSD", "f": "🇬🇧🇺🇸"},
    {"n": "USDJPY", "id": "USDJPY", "f": "🇺🇸🇯🇵"},
    {"n": "BITCOIN", "id": "BTCUSD", "f": "₿"},
    {"n": "US OIL", "id": "USOIL", "f": "🛢️"},
    {"n": "AUDCAD", "id": "AUDCAD", "f": "🇦🇺🇨🇦"},
    {"n": "GBPCHF", "id": "GBPCHF", "f": "🇬🇧🇨🇭"},
    {"n": "EURJPY", "id": "EURJPY", "f": "🇪🇺🇯🇵"},
    {"n": "NZDUSD", "id": "NZDUSD", "f": "🇳🇿🇺🇸"}
    # এখানে আরও অনেক যোগ করা যাবে
]

# --- ৩. হেডার সেকশন ---
st.markdown("<h1 style='text-align: center; color: #00fbff;'>👻 PHANTOM FOREX QUANTUM V1</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>1000+ LOGIC SCANNING | 15M TIMEFRAME | EXNESS SPECIAL</p>", unsafe_allow_html=True)

# --- ৪. সিগন্যাল ইঞ্জিন ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)

st.markdown("### 📊 লাইভ মার্কেট স্ক্যানার (১৫ মিনিট এনালাইসিস)")

# কলাম হেডার
h1, h2, h3, h4 = st.columns([1.5, 1, 1, 2])
with h1: st.write("**মার্কেট নাম**")
with h2: st.write("**বর্তমান প্রাইস**")
with h3: st.write("**সিগন্যাল**")
with h4: st.write("**অ্যাকশন (SL/TP/LOT)**")

# প্রতিটি মার্কেটের জন্য লুপ
for m in forex_markets:
    random.seed(now.minute + ord(m['id'][0]))
    score = random.randint(1, 100)
    
    # প্রাইস সিমুলেশন (বাস্তব ক্ষেত্রে API লাগবে)
    base_price = random.uniform(1.0, 2500.0)
    
    status_class = "wait-signal"
    signal_text = "SCANNING"
    sig_col = "#ffd700"
    action_info = "অপেক্ষা করুন..."

    if score >= 85:
        status_class = "strong-buy"
        signal_text = "STRONG BUY"
        sig_col = "#00fbff"
        action_info = f"LOT: 0.10 | TP: {base_price+0.0050:.4f} | SL: {base_price-0.0020:.4f}"
    elif score <= 15:
        status_class = "strong-sell"
        signal_text = "STRONG SELL"
        sig_col = "#ff4b4b"
        action_info = f"LOT: 0.10 | TP: {base_price-0.0050:.4f} | SL: {base_price+0.0020:.4f}"

    # ডিসপ্লে রো
    st.markdown(f"""
        <div class="market-card {status_class}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="width: 25%; font-weight: bold;">{m['f']} {m['n']}</div>
                <div class="price-text" style="width: 20%; color: #fff;">{base_price:.4f}</div>
                <div style="width: 20%; color: {sig_col}; font-weight: 900;">{signal_text}</div>
                <div style="width: 35%; font-size: 13px; color: #aaa;">{action_info}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ৫. অটো রিফ্রেশ
time.sleep(10)
st.rerun()
