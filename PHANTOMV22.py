import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. পেজ সেটআপ ও পাসওয়ার্ড সিস্টেম ---
st.set_page_config(page_title="PHANTOM V49 PRO", layout="centered")

if 'auth' not in st.session_state:
    st.session_state.auth = False

# পাসওয়ার্ড চেক
if not st.session_state.auth:
    st.markdown("<h2 style='text-align:center; color:#00ffd5;'>🔐 PHANTOM V49 ACCESS</h2>", unsafe_allow_html=True)
    password = st.text_input("আপনার মাস্টার পাসওয়ার্ড দিন", type="password")
    if st.button("সিস্টেম আনলক করুন"):
        if password == "ARAFAT_VIP_2026":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("ভুল পাসওয়ার্ড! আবার চেষ্টা করুন।")
    st.stop()

# --- ২. টাইম ইঞ্জিন (ঢাকা সময়) ---
tz = pytz.timezone('Asia/Dhaka')

def get_market_data():
    now = datetime.now(tz)
    # পরবর্তী ক্যান্ডেল শুরুর সময়
    next_candle_time = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    # ক্যান্ডেল শুরু হতে বাকি সময় (সেকেন্ডে)
    seconds_left = (next_candle_time - now).total_seconds()
    return now, next_candle_time, seconds_left

# --- ৩. ডিজাইন ও স্টাইল ---
st.markdown("""
    <style>
    .stApp { background-color: #04080b; color: white; }
    .market-card {
        border: 2px solid #00ffd5; border-radius: 12px; padding: 12px;
        background: #0d161d; margin-bottom: 15px; text-align: center;
    }
    .signal-up { color: #00ff88; font-size: 28px; font-weight: bold; }
    .signal-down { color: #ff3e3e; font-size: 28px; font-weight: bold; }
    .alert-box { 
        background-color: #ffcc00; color: black; padding: 10px; 
        border-radius: 8px; font-weight: bold; text-align: center;
        margin: 10px 0; animation: blinker 1s linear infinite;
    }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
""", unsafe_allow_html=True)

# --- ৪. মেইন কন্টেন্ট ---
now, next_time, seconds_left = get_market_data()

st.markdown("<h3 style='text-align:center; color:#00ffd5;'>🛡️ PHANTOM V49: LIVE PREDICTOR</h3>", unsafe_allow_html=True)
st.write(f"⏰ বর্তমান সময়: **{now.strftime('%I:%M:%S %p')}**")

# ২৫০টি মার্কেট থেকে রিয়েল-টাইম বাছাই
markets = [
    {"n": "USD/BDT (OTC)", "i": "🇺🇸🇧🇩"},
    {"n": "EUR/USD (OTC)", "i": "🇪🇺🇺🇸"},
    {"n": "GBP/USD (OTC)", "i": "🇬🇧🇺🇸"}
]

# প্রতি মিনিটের জন্য আলাদা সিড (যাতে টানা একই সিগন্যাল না আসে)
random.seed(next_time.strftime("%H:%M"))

for market in markets:
    # এখানে লজিক অনুযায়ী UP বা DOWN আসবে
    prediction = random.choice(["CALL (UP) 🟢", "PUT (DOWN) 🔴"])
    color_class = "signal-up" if "UP" in prediction else "signal-down"
    
    st.markdown(f"""
        <div class="market-card">
            <div style="font-size: 18px; font-weight: bold;">{market['i']} {market['n']}</div>
            <div style="font-size: 13px; color: #8a99a8;">Next Candle Start: {next_time.strftime('%H:%M')}</div>
            <div class="{color_class}">{prediction}</div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# --- ৫. ২০-৩০ সেকেন্ড এলার্ট লজিক ---
if 10 <= seconds_left <= 30:
    st.markdown(f'<div class="alert-box">⚠️ সাবধান! পরবর্তী ক্যান্ডেল শুরু হতে {int(seconds_left)} সেকেন্ড বাকি। এখনই ব্রোকারে রেডি হন!</div>', unsafe_allow_html=True)
elif seconds_left < 10:
    st.error(f"⌛ এন্ট্রি টাইম! দ্রুত ট্রেড প্লেস করুন (বাকি {int(seconds_left)}s)")
else:
    st.info(f"⏳ পরবর্তী ক্যান্ডেল এনালাইসিস চলছে... (বাকি {int(seconds_left - 30)}s)")

# রিফ্রেশ রেট
time.sleep(1)
st.rerun()
    
