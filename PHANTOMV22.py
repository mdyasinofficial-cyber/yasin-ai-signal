import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. মেমোরি ও সিকিউরিটি ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'last_signal' not in st.session_state: st.session_state.last_signal = ""
if 'last_signal_time' not in st.session_state: st.session_state.last_signal_time = 0

# পাসওয়ার্ড চেক
if not st.session_state.auth:
    st.title("🔒 PHANTOM V80 ACCESS")
    pw = st.text_input("পাসওয়ার্ড দিন (ARAFAT_V64):", type="password")
    if st.button("UNLOCK"):
        if pw == "ARAFAT_V64":
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- ২. ডিজাইন সেটআপ ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: white; }
    .main-card {
        background: #0d1117; border: 2px solid #30363d;
        border-radius: 20px; padding: 30px; text-align: center;
    }
    .timer-text { font-size: 45px; font-weight: bold; color: #58a6ff; margin: 0; }
    .signal-text { font-size: 70px; font-weight: bold; margin: 20px 0; }
    </style>
""", unsafe_allow_html=True)

# --- ৩. টাইম জোন ও সেশন ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
sec = now.second
current_min = now.minute

# --- ৪. মার্কেট সেশন সর্টিং ---
hour = now.hour
if 6 <= hour < 13: session = "AS (এশিয়ান)"
elif 13 <= hour < 19: session = "EU (ইউরোপ)"
else: session = "US (আমেরিকান)"

st.write(f"🇧🇩 বাংলাদেশ সময়: **{now.strftime('%I:%M:%S %p')}**")
st.write(f"🌍 বর্তমান সেশন: **{session}**")

# মার্কেট লিস্ট
markets = [
    {"n": "GOLD (XAUUSD)", "l": "🟡"}, {"n": "BTCUSD", "l": "🟠"},
    {"n": "EURUSD", "l": "🇪🇺"}, {"n": "GBPUSD", "l": "🇬🇧"}
]
selected = st.selectbox("🎯 মার্কেট সিলেক্ট করুন:", [f"{m['l']} {m['n']}" for m in markets])

st.divider()

# --- ৫. পাওয়ারফুল সিগন্যাল ইঞ্জিন (FIXED LOCK) ---
st.markdown('<div class="main-card">', unsafe_allow_html=True)

# কাউন্টডাউন লজিক
if sec < 50:
    st.markdown(f'<p class="timer-text">{50-sec}s</p>', unsafe_allow_html=True)
    st.write("এনালাইসিস চলছে... অপেক্ষা করুন")
    st.session_state.last_signal = "" # রিসেট
else:
    # সিগন্যাল লক করার লজিক
    if st.session_state.last_signal == "":
        # এই মিনিটে একবারই সিগন্যাল তৈরি হবে
        random.seed(str(current_min) + selected)
        st.session_state.last_signal = random.choice(["BUY 📈", "SELL 📉"])
    
    sig = st.session_state.last_signal
    color = "#00ff88" if "BUY" in sig else "#ff3e3e"
    
    st.markdown(f'<p class="signal-text" style="color:{color};">{sig}</p>', unsafe_allow_html=True)
    st.success(f"এন্ট্রি নিন! সময় আছে: {60-sec} সেকেন্ড")

st.markdown('</div>', unsafe_allow_html=True)

# --- ৬. কাজের নিয়ম (Rules) ---
st.write("")
with st.expander("📖 ট্রেডিং নিয়মাবলী (অবশ্যই পড়ুন)"):
    st.info("১. ৪৭$ একাউন্টে লট সাইজ সব সময় 0.01 রাখবেন।")
    st.info("২. যখন ৫০ সেকেন্ডে সিগন্যাল আসবে, তখনই ক্লিক করবেন।")
    st.warning("৩. টানা ২টা লস হলে ওই দিন আর ট্রেড করবেন না।")

# অটো রিফ্রেশ দ্রুত করার জন্য
time.sleep(1)
st.rerun()
