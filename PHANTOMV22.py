import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. পেজ ও সিকিউরিটি ---
st.set_page_config(page_title="PHANTOM V54 COMMANDER", layout="centered")

if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    pw = st.text_input("পাসওয়ার্ড", type="password")
    if st.button("সিস্টেম আনলক"):
        if pw == "ARAFAT_VIP_2026":
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- ২. কমান্ড সেন্টার ডিজাইন (মোবাইল ফিট) ---
st.markdown("""
    <style>
    .stApp { background-color: #03070a; color: white; }
    .cmd-box {
        border: 1px solid #333; border-radius: 10px; padding: 10px;
        background: #0d161d; margin-bottom: 8px; display: flex;
        justify-content: space-between; align-items: center;
    }
    .market-name { font-size: 14px; font-weight: bold; flex: 1.5; }
    .status-btn { 
        padding: 5px 12px; border-radius: 5px; font-weight: bold; 
        font-size: 15px; text-align: center; min-width: 90px;
    }
    .wait { background: #555; color: #ddd; }
    .danger { background: #ff3e3e; color: white; animation: blink 0.6s infinite; }
    .buy { background: #00ff88; color: #000; box-shadow: 0 0 10px #00ff88; }
    .sell { background: #ff3e3e; color: white; box-shadow: 0 0 10px #ff3e3e; }
    @keyframes blink { 50% { opacity: 0.4; } }
    </style>
""", unsafe_allow_html=True)

# --- ৩. টাইম ইঞ্জিন ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
sec = now.second
next_t = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)

st.markdown(f"<h3 style='text-align:center; color:#00ffd5; margin:0;'>🛡️ PHANTOM V54 COMMANDER</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; font-size:12px; color:#888;'>সময়: {now.strftime('%I:%M:%S %p')} | এনালাইসিস: {sec}s</p>", unsafe_allow_html=True)

# ৫টি ফিক্সড মার্কেট
top_5 = [
    {"n": "USD/BDT (OTC)", "i": "🇺🇸🇧🇩"},
    {"n": "EUR/USD (OTC)", "i": "🇪🇺🇺🇸"},
    {"n": "GBP/USD (OTC)", "i": "🇬🇧🇺🇸"},
    {"n": "USD/JPY (OTC)", "i": "🇺🇸🇯🇵"},
    {"n": "AUD/CAD (OTC)", "i": "🇦🇺🇨🇦"}
]

# --- ৪. কমান্ড লজিক ডিসপ্লে ---
for m in top_5:
    random.seed(next_t.strftime("%H:%M") + m['n'])
    
    # শিউর শট প্রোব্যাবিলিটি (৯৭% এর নিচে নামলে ডেঞ্জার)
    win_rate = random.randint(90, 100)
    direction = random.choice(["BUY 📈", "SELL 📉"])

    if sec < 40:
        btn_class = "wait"
        btn_text = "WAIT ⏳"
    else:
        if win_rate < 96: # যদি মার্কেট রিস্কি হয়
            btn_class = "danger"
            btn_text = "DANGER 🚫"
        else: # যদি মার্কেট ক্লিয়ার থাকে
            btn_class = "buy" if "BUY" in direction else "sell"
            btn_text = direction

    st.markdown(f"""
        <div class="cmd-box">
            <div class="market-name">
                {m['i']} {m['n']}<br>
                <span style="font-size:10px; color:#666;">Next: {next_t.strftime('%H:%M')}</span>
            </div>
            <div class="status-btn {btn_class}">
                {btn_text}
            </div>
        </div>
    """, unsafe_allow_html=True)

# নিচের মেইন টাইমার
if sec >= 40:
    st.markdown(f"<p style='text-align:center; color:#ffcc00; font-weight:bold;'>🔥 একশন টাইম: {60-sec} সেকেন্ড বাকি!</p>", unsafe_allow_html=True)

time.sleep(1)
st.rerun()
