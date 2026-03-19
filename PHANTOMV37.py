import streamlit as st
import time
from datetime import datetime
import pytz
import random

# --- ১. প্রো কনফিগারেশন ---
st.set_page_config(page_title="V41.1 COUNTDOWN", layout="centered")

st.markdown("""
    <style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden; display:none;}
    .stApp { background-color: #000; color: #ffd700; }
    .stButton > button {
        background-color: #111; color: #ffd700; border: 1px solid #333;
        border-radius: 5px; font-size: 10px; width: 100%; height: 32px;
    }
    .display-card {
        border: 4px solid #ffd700; border-radius: 20px;
        padding: 20px; text-align: center; background: #000;
    }
    </style>
""", unsafe_allow_html=True)

# --- ২. ৪০টি মার্কেট লিস্ট ---
markets = [
    "EURUSD", "GBPUSD", "USDJPY", "AUDCAD", "EURJPY", "GBPJPY", "USDCAD", "NZDUSD",
    "AUDUSD", "EURGBP", "EURAUD", "CHFJPY", "CADJPY", "AUDJPY", "GBPAUD", "GBPCHF",
    "USDCHF", "EURNZD", "AUDCHF", "NZDJPY", "GBPCAD", "Eurchf", "CADCHF", "EURCAD",
    "BTCUSD", "ETHUSD", "XAUUSD", "XAGUSD", "SOLUSD", "LTCUSD", "BNBUSD", "ADAUSD",
    "USDTUSD", "DOGEUSD", "DOTUSD", "AVAXUSD", "MATICUSD", "SHIBUSD", "TRXUSD", "LINKUSD"
]

if 'm_choice' not in st.session_state: st.session_state.m_choice = "EURUSD"

st.markdown("### 🎛️ SELECT MARKET (40)")
cols = st.columns(4)
for i, m in enumerate(markets):
    if cols[i % 4].button(m): st.session_state.m_choice = m

# --- ৩. টাইম ও লজিক ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
rem_sec = 60 - now.second

random.seed(now.minute + len(st.session_state.m_choice))
score = random.randint(1, 500)

status_col = "#ffd700"; sig = "WAITING"; v_text = ""

if rem_sec <= 20:
    if score >= 380:
        sig = "BUY NEXT"; status_col = "#00fbff"; v_text = "বাই নিন"
    elif score <= 120:
        sig = "SELL NEXT"; status_col = "#ff4b4b"; v_text = "সেল নিন"
    else:
        sig = "DANGER"; status_col = "#ff0000"; v_text = "বিপদ"
else:
    sig = "SCANNING"; status_col = "#ffd700"

# --- ৪. ডিসপ্লে ---
st.markdown(f"""
    <div class="display-card" style="border-color: {status_col};">
        <div style="font-size: 18px; color: #fff;">{st.session_state.m_choice} (OTC)</div>
        <div style="font-size: 110px; font-weight: 900; color: {status_col}; line-height:1;">{rem_sec}s</div>
        <div style="font-size: 40px; font-weight: bold; color: {status_col};">{sig}</div>
    </div>
""", unsafe_allow_html=True)

# --- ৫. স্মার্ট ভয়েস ও কাউন্টডাউন সিস্টেম ---
voice_command = ""

# ঠিক ২০ সেকেন্ডে মেইন অ্যালার্ট
if rem_sec == 20:
    voice_command = f"পরবর্তী ক্যান্ডেলে {v_text} এর জন্য তৈরি হোন।"

# শেষ ১০ সেকেন্ডে কাউন্টডাউন (১০ থেকে ১)
elif rem_sec <= 10 and rem_sec > 0 and sig != "SCANNING" and sig != "DANGER":
    voice_command = str(rem_sec)

# ভয়েস প্লেয়ার
if voice_command != "":
    st.markdown(f'<iframe src="https://translate.google.com/translate_tts?ie=UTF-8&q={voice_command.replace(" ", "%20")}&tl=bn&client=tw-ob" allow="autoplay" style="display:none;"></iframe>', unsafe_allow_html=True)
    if rem_sec <= 10: # শেষ ১০ সেকেন্ডে ভাইব্রেশন
        st.components.v1.html("<script>window.navigator.vibrate(100);</script>", height=0)

time.sleep(1)
st.rerun()
