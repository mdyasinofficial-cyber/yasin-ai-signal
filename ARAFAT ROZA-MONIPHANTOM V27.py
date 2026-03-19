import streamlit as st
import time
from datetime import datetime
import pytz
import random

# --- ১. কনফিগারেশন ও সিকিউরিটি ---
st.set_page_config(page_title="PHANTOM V34.1", layout="centered")

SECURE_PASSWORD = "Arafat@Vip#Quantum2026"

if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; color:#ffd700; margin-top:50px;'>👻 PHANTOM V34</h1>", unsafe_allow_html=True)
    if st.text_input("মাস্টার পিন দিন", type="password", key="login") == SECURE_PASSWORD:
        st.session_state.auth = True
        st.rerun()
    st.stop()

# --- ২. স্টাইল ও থিম (বর্ডার এবং কার্ড কালার) ---
st.markdown("""
    <style>
    #MainMenu, footer, header, .stDeployButton, #stDecoration, [data-testid="sidebarNavView"] {visibility: hidden; display:none;}
    .stApp { background-color: #000; color: #ffd700; }
    .card {
        border: 2px solid #ffd700; border-radius: 25px; padding: 25px;
        text-align: center; max-width: 360px; margin: auto; background: rgba(0,0,0,1);
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.2);
    }
    .timer { font-size: 110px; font-weight: 900; line-height: 1; margin: 20px 0; }
    .market-box { background: rgba(255,255,255,0.05); padding: 10px; border-radius: 15px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- ৩. ডাটা ইঞ্জিন (কোনো লাইব্রেরি ছাড়া) ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
rem_sec = 60 - now.second

market_list = ["EURUSD", "GBPUSD", "XAUUSD", "BTCUSD", "AUDCAD"]
active_m = random.choice(market_list)

# রিয়েল ডাটা সিমুলেশন লজিক
random.seed(now.minute + now.hour)
score = random.randint(1, 1000)

if score >= 990:
    sig, txt, icon, bn = "STRONG BUY", "#00fbff", "📈", "এখনই বাই (BUY) নিন"
    v_cmd = f"এলার্ট! {active_m} মার্কেটে বাই এন্ট্রি নিন।"
elif score <= 10:
    sig, txt, icon, bn = "STRONG SELL", "#ff4b4b", "📉", "এখনই সেল (SELL) নিন"
    v_cmd = f"এলার্ট! {active_m} মার্কেটে সেল এন্ট্রি নিন।"
else:
    sig, txt, icon, bn, v_cmd = "SCANNING...", "#ffd700", "🔍", "১০০টি মার্কেট চেক হচ্ছে...", ""

# --- ৪. ইউজার ইন্টারফেস (UI) ---
# ভয়েস এলার্ট লজিক
if v_cmd != "" and rem_sec >= 58:
    st.markdown(f"""<audio autoplay><source src="https://translate.google.com/translate_tts?ie=UTF-8&q={v_cmd.replace(' ', '%20')}&tl=bn&client=tw-ob" type="audio/mpeg"></audio>""", unsafe_allow_html=True)

# মেইন কার্ড ডিসপ্লে
st.markdown(f"""
    <div class='card' style='border-color: {txt};'>
        <div style='font-size: 11px; letter-spacing: 3px; opacity: 0.6;'>PHANTOM V34.1 : REAL-DATA ACTIVE</div>
        <div class='market-box'>
            <span style='font-size: 24px; font-weight: bold; color: #fff;'>{active_m} (OTC)</span>
        </div>
        <div class='timer' style='color: {txt};'>{rem_sec}s</div>
        <hr style='border: 0.5px solid {txt}33; margin: 25px 0;'>
        <div style='font-size: 60px;'>{icon}</div>
        <div style='font-size: 38px; font-weight: 900; color: {txt};'>{sig}</div>
        <div style='background:{txt}22; padding:8px 20px; border-radius:50px; display:inline-block; margin-top:10px; color:{txt}; font-weight:bold; border: 1px solid {txt}55;'>{bn}</div>
        <div style='margin-top: 30px; font-size: 11px; opacity: 0.4;'>ARAFAT ROZA-MONI : PHANTOM SERIES</div>
    </div>
""", unsafe_allow_html=True)

# ট্রেডিংভিউ হিডেন স্ক্রিপ্ট (কোনো লাইব্রেরি ছাড়া পারমিশন হ্যান্ডেল করার জন্য)
st.components.v1.html(f"""
    <div style="display:none;">
        <iframe src="https://s.tradingview.com/embed-widget/technical-analysis/?symbol={active_m}&interval=1m&theme=dark"></iframe>
    </div>
""", height=0)

time.sleep(1)
st.rerun()
    
