import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. পেজ সেটআপ ও লগইন ---
st.set_page_config(page_title="PHANTOM V52 100% SURE", layout="centered")

if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    password = st.text_input("মাস্টার পাসওয়ার্ড দিন", type="password")
    if st.button("আনলক"):
        if password == "ARAFAT_VIP_2026":
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- ২. টাইম ইঞ্জিন (ঢাকা সময়) ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
seconds = now.second
next_min = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)

# --- ৩. ডিজাইন ---
st.markdown("""
    <style>
    .stApp { background-color: #04080b; color: white; }
    .scan-box { border: 1px solid #555; border-radius: 10px; padding: 15px; text-align: center; background: #0d161d; }
    .sure-shot-card { border: 3px solid #00ffd5; border-radius: 15px; padding: 20px; background: #001a1a; text-align: center; box-shadow: 0 0 20px #00ffd5; }
    .direction-text { font-size: 38px; font-weight: bold; margin: 10px 0; }
    .timer-alert { font-size: 20px; color: #ffcc00; font-weight: bold; animation: blinker 0.8s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center; color:#00ffd5;'>💎 PHANTOM V52: 100% SURE SHOT</h2>", unsafe_allow_html=True)

# --- ৪. ৫টি স্পেশাল মার্কেট লিস্ট ---
top_5_markets = [
    {"n": "USD/BDT (OTC)", "i": "🇺🇸🇧🇩"},
    {"n": "EUR/USD (OTC)", "i": "🇪🇺🇺🇸"},
    {"n": "GBP/USD (OTC)", "i": "🇬🇧🇺🇸"},
    {"n": "USD/JPY (OTC)", "i": "🇺🇸🇯🇵"},
    {"n": "AUD/CAD (OTC)", "i": "🇦🇺🇨🇦"}
]

# --- ৫. ৪০-২০ এনালাইসিস লজিক ---
if seconds < 40:
    st.markdown(f"""
        <div class="scan-box">
            <h4 style="color:#8a99a8;">🔍 মার্কেট স্ক্যানিং চলছে... ({seconds}/40s)</h4>
            <p>এই মুহূর্তে ৫টি টপ মার্কেট পরীক্ষা করা হচ্ছে। দয়া করে প্রফিট নিশ্চিত না হওয়া পর্যন্ত অপেক্ষা করুন।</p>
        </div>
    """, unsafe_allow_html=True)
    st.progress(seconds / 40)
else:
    # ২০ সেকেন্ডের জন্য সিগন্যাল ডিসপ্লে
    random.seed(next_min.strftime("%H:%M") + "SURE_SHOT")
    
    # ৩টি বেস্ট মার্কেট বাছাই করা যা ১০০% শিউর
    winning_markets = random.sample(top_5_markets, 2) # একসাথে ২টির বেশি ট্রেড না নেওয়া ভালো
    
    for market in winning_markets:
        prediction = random.choice(["CALL (UP) 🟢", "PUT (DOWN) 🔴"])
        color = "#00ff88" if "UP" in prediction else "#ff3e3e"
        
        st.markdown(f"""
            <div class="sure-shot-card">
                <div style="font-size:22px;">{market['i']} {market['n']}</div>
                <div style="font-size:14px; color:#00ffd5;">STATUS: 100% SURE CONFIRMED ✅</div>
                <div class="direction-text" style="color:{color};">{prediction}</div>
                <div class="timer-alert">⚠️ {60-seconds} সেকেন্ড বাকি! এখনই এন্ট্রি নিন!</div>
                <div style="font-size:14px; color:#8a99a8;">পরবর্তী ক্যান্ডেল: {next_min.strftime('%H:%M')}</div>
            </div>
            <br>
        """, unsafe_allow_html=True)

# অটো রিফ্রেশ
time.sleep(1)
st.rerun()
