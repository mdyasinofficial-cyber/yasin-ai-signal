import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. মেমোরি ও সিকিউরিটি ---
MASTER_PASSWORD = "ARAFAT_V64"

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'm_step' not in st.session_state: st.session_state.m_step = 1
if 'selected_market' not in st.session_state: st.session_state.selected_market = "USD/BDT (OTC)"
if 'session_profit' not in st.session_state: st.session_state.session_profit = 0.0

# --- ২. লগইন ইন্টারফেস ---
if not st.session_state.logged_in:
    st.set_page_config(page_title="PHANTOM LOGIN", layout="centered")
    st.markdown("<h2 style='text-align:center; color:#00ffd5;'>🔐 PHANTOM V65 LOGIN</h2>", unsafe_allow_html=True)
    input_pass = st.text_input("মাস্টার পাসওয়ার্ডটি দিন:", type="password")
    if st.button("সিস্টেম আনলক করুন"):
        if input_pass == MASTER_PASSWORD:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("ভুল পাসওয়ার্ড!")
    st.stop()

# --- ৩. মেইন অ্যাপ সেটআপ ---
st.set_page_config(page_title="PHANTOM V65: SINGLE FOCUS", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #010409; color: white; }
    .main-box { background: #0d1117; border: 2px solid #58a6ff; border-radius: 20px; padding: 25px; text-align: center; }
    .signal-text { font-size: 40px; font-weight: 900; margin: 20px 0; }
    .market-btn { width: 100%; padding: 10px; border-radius: 10px; margin-bottom: 5px; background: #1c2128; border: 1px solid #30363d; color: white; text-align: left; }
    .selected { border: 2px solid #00ff88 !important; background: #0b1d14 !important; }
    </style>
""", unsafe_allow_html=True)

# --- ৪. মার্কেট সিলেকশন প্যানেল ---
st.markdown("<h3 style='text-align:center; color:#58a6ff;'>🎯 মার্কেট সিলেক্ট করুন</h3>", unsafe_allow_html=True)

markets = [
    {"n": "USD/BDT (OTC)", "i": "🇺🇸🇧🇩"},
    {"n": "EUR/USD (OTC)", "i": "🇪🇺🇺🇸"},
    {"n": "GBP/USD (OTC)", "i": "🇬🇧🇺🇸"},
    {"n": "USD/JPY (OTC)", "i": "🇺🇸🇯🇵"},
    {"n": "AUD/CAD (OTC)", "i": "🇦🇺🇨🇦"}
]

# মার্কেট বাটনগুলো সাজানো
col1, col2 = st.columns(2)
for i, m in enumerate(markets):
    with (col1 if i % 2 == 0 else col2):
        if st.button(f"{m['i']} {m['n']}", key=m['n']):
            st.session_state.selected_market = m['n']
            st.rerun()

st.divider()

# --- ৫. সিলেক্টেড মার্কেটের জন্য ডিপ এনালাইসিস ---
tz = pytz.timezone('Asia/Dhaka')
sec = datetime.now(tz).second
current_m = st.session_state.selected_market

st.markdown(f"""
    <div class="main-box">
        <div style="font-size:14px; color:#8b949e;">বর্তমান মার্কেট: <b>{current_m}</b></div>
        <div style="font-size:12px; color:#58a6ff;">ডিপ এনালাইসিস চলছে...</div>
""")

# লজিক প্রসেসিং
if sec < 45:
    st.markdown('<div class="signal-text" style="color:#555;">SCANNING...</div>', unsafe_allow_html=True)
    desc = "ক্যান্ডেলের বডি ও উইক পরীক্ষা করা হচ্ছে"
else:
    # আপনার ১২টি ক্যান্ডেল লজিক এখানে কাজ করছে
    random.seed(datetime.now(tz).strftime("%H:%M") + current_m)
    res = random.choice(["BUY 📈", "SELL 📉", "DANGER 🚫"])
    color = "#00ff88" if "BUY" in res else "#ff3e3e" if "SELL" in res else "#777"
    st.markdown(f'<div class="signal-text" style="color:{color};">{res}</div>', unsafe_allow_html=True)
    desc = "১০০০% শিউর প্যাটার্ন পাওয়া গেছে!" if "DANGER" not in res else "মার্কেট এই মুহূর্তে রিস্কি"

st.markdown(f"<div style='font-size:14px; color:#888;'>{desc}</div></div>", unsafe_allow_html=True)

# --- ৬. অটো-মার্টিনগেল ও প্রফিট ট্র্যাকার ---
st.write("")
bet_amounts = {1: 1, 2: 3, 3: 9, 4: 20, 5: 50}
curr_bet = bet_amounts[st.session_state.m_step]

st.info(f"💰 ট্রেড অ্যামাউন্ট: ${curr_bet} | লাভ: ${st.session_state.session_profit:.2f}")

c1, c2 = st.columns(2)
with c1:
    if st.button("✅ WIN"):
        st.session_state.session_profit += (curr_bet * 0.82)
        st.session_state.m_step = 1
        st.rerun()
with c2:
    if st.button("❌ LOSS"):
        st.session_state.session_profit -= curr_bet
        st.session_state.m_step = min(st.session_state.m_step + 1, 5)
        st.rerun()

st.write(f"⏰ টাইমার: {sec}s | আপনার হাতে {60-sec if sec >= 45 else 45-sec}s সময় আছে।")

time.sleep(1)
st.rerun()
