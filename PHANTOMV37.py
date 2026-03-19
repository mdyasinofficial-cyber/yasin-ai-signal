import streamlit as st
import time
from datetime import datetime
import pytz
import random

# --- ১. প্রো কনফিগারেশন ---
st.set_page_config(page_title="V39 FIXED PREDICT", layout="centered")
SECURE_PASSWORD = "Arafat@Vip#Quantum2026"

if 'auth' not in st.session_state: st.session_state.auth = False

# --- ২. সিকিউরিটি গেট ---
if not st.session_state.auth:
    st.markdown("<style>.stApp { background-color: #000; text-align: center; color: #ffd700; }</style>", unsafe_allow_html=True)
    st.markdown('<div style="padding:50px;"><h1>👑 V39 ELITE</h1><h3>FIXED 20s LOCK</h3></div>', unsafe_allow_html=True)
    if st.text_input("মাস্টার পিন", type="password") == SECURE_PASSWORD:
        st.session_state.auth = True; st.rerun()
    st.stop()

# --- ৩. মেইন স্টাইল ---
st.markdown("""
    <style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden; display:none;}
    .stApp { background-color: #000; color: #ffd700; }
    .display-card { border: 5px solid #ffd700; border-radius: 30px; padding: 40px; text-align: center; background: #000; transition: 0.5s; }
    .market-header { font-size: 25px; font-weight: bold; color: #fff; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- ৪. মার্কেট সিলেকশন (সরাসরি বাটন) ---
market_list = [
    {"n": "EUR/USD", "id": "EURUSD", "f": "🇪🇺🇺🇸"}, {"n": "GBP/USD", "id": "GBPUSD", "f": "🇬🇧🇺🇸"},
    {"n": "USD/JPY", "id": "USDJPY", "f": "🇺🇸🇯🇵"}, {"n": "AUD/CAD", "id": "AUDCAD", "f": "🇦🇺🇨🇦"}
]

if 'active_market' not in st.session_state: st.session_state.active_market = market_list[0]

st.write("### 🎯 মার্কেট সিলেক্ট করুন:")
cols = st.columns(len(market_list))
for i, m in enumerate(market_list):
    if cols[i].button(m['id']): st.session_state.active_market = m

# --- ৫. স্থির লজিক ইঞ্জিন (২০ সেকেন্ড লক) ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
rem_sec = 60 - now.second
cur_m = st.session_state.active_market

# সিড সেট করা যাতে ওই ১ মিনিটের জন্য সিগন্যাল না পাল্টায়
random.seed(now.minute + ord(cur_m['id'][0]))
score = random.randint(1, 500)

sig_text = "ANALYZING..."
status_col = "#ffd700"
voice_cmd = ""

# লজিক যখন ২০ সেকেন্ড বা তার নিচে আসবে
if rem_sec <= 20:
    if score >= 400:
        sig_text, status_col = "BUY NEXT", "#00fbff"
        voice_cmd = "পরবর্তী ক্যান্ডেলে বাই নিন"
    elif score <= 100:
        sig_text, status_col = "SELL NEXT", "#ff4b4b"
        voice_cmd = "পরবর্তী ক্যান্ডেলে সেল নিন"
    else:
        sig_text, status_col = "DANGER", "#ff0000"
        voice_cmd = "মার্কেট বিপজ্জনক, ট্রেড নিবেন না"
else:
    sig_text = "SCANNING..."
    status_col = "#ffd700"

# --- ৬. ভয়েস অ্যালার্ট (ঠিক ২০ সেকেন্ডে একবার) ---
if rem_sec == 20:
    st.markdown(f'<iframe src="https://translate.google.com/translate_tts?ie=UTF-8&q={voice_cmd.replace(" ", "%20")}&tl=bn&client=tw-ob" allow="autoplay" style="display:none;"></iframe>', unsafe_allow_html=True)

# --- ৭. ডিসপ্লে ইন্টারফেস ---
st.markdown(f"""
    <div class='display-card' style='border-color: {status_col};'>
        <div class='market-header'>{cur_m['f']} {cur_m['n']}</div>
        <div style='font-size: 120px; font-weight: 900; line-height: 1; color: {status_col};'>{rem_sec}s</div>
        <div style='font-size: 45px; font-weight: bold; margin-top: 20px; color: {status_col};'>{sig_text}</div>
        <hr style='border: 1px solid {status_col}33; margin: 20px 0;'>
        <div style='font-size: 16px; opacity: 0.8;'>২০ সেকেন্ডে সিগন্যাল লক হবে। স্কয়ার স্কোর: {score}</div>
    </div>
""", unsafe_allow_html=True)

time.sleep(1)
st.rerun()
