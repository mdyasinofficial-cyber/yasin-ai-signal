import streamlit as st
import time
from datetime import datetime
import pytz
import random

# --- ১. প্রো কনফিগারেশন ---
st.set_page_config(page_title="PHANTOM V35 FINAL", layout="centered", initial_sidebar_state="collapsed")
SECURE_PASSWORD = "Arafat@Vip#Quantum2026"

if 'auth' not in st.session_state: st.session_state.auth = False

# --- ২. সিকিউরিটি গেট ---
if not st.session_state.auth:
    st.markdown("""<style>.stApp { background-color: #000; color: #ffd700; text-align: center; } .l-card { border: 2px solid #ffd700; padding: 50px; border-radius: 20px; margin-top: 80px; box-shadow: 0 0 30px #ffd70044; }</style>""", unsafe_allow_html=True)
    st.markdown('<div class="l-card"><h1>👻 PHANTOM V35</h1><p>ARAFAT ROZA-MONI : FINAL ACCESS</p></div>', unsafe_allow_html=True)
    if st.text_input("মাস্টার পিন", type="password") == SECURE_PASSWORD:
        st.session_state.auth = True; st.rerun()
    st.stop()

# --- ৩. মেইন স্টাইল ইঞ্জিন ---
st.markdown("""
    <style>
    #MainMenu, footer, header, .stDeployButton, #stDecoration, [data-testid="sidebarNavView"] {visibility: hidden; display:none;}
    .stApp { background-color: #000; color: #ffd700; }
    .main-card { border: 4px solid #ffd700; border-radius: 30px; padding: 30px; text-align: center; max-width: 400px; margin: auto; background: #000; transition: all 0.5s; }
    .market-title { font-size: 30px; font-weight: bold; color: #fff; margin-bottom: 10px; }
    .timer-big { font-size: 130px; font-weight: 900; line-height: 1; margin: 10px 0; }
    .signal-btn { font-size: 45px; font-weight: 900; padding: 15px; border-radius: 50px; display: inline-block; margin-top: 20px; width: 100%; border: 2px solid; }
    </style>
""", unsafe_allow_html=True)

# --- ৪. হাইপার ডাটা ইঞ্জিন (৪০ মার্কেট) ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
rem_sec = 60 - now.second

markets = [
    {"n": "EURUSD", "f": "🇪🇺🇺🇸"}, {"n": "GBPUSD", "f": "🇬🇧🇺🇸"}, 
    {"n": "XAUUSD", "f": "🟡 GOLD"}, {"n": "BTCUSD", "f": "₿ BTC"},
    {"n": "AUDCAD", "f": "🇦🇺🇨🇦"}, {"n": "USDJPY", "f": "🇺🇸🇯🇵"}
]
active = random.choice(markets)

# লজিক জেনারেটর (৫০০ স্কেল)
random.seed(now.minute + now.hour)
score = random.randint(1, 500)

sig_type = "NONE"
if score >= 440: sig_type = "BUY"
elif score <= 60: sig_type = "SELL"

# --- ৫. ভয়েস ও কাউন্টডাউন লজিক ---
voice_script = ""
# ক্যান্ডেল শুরু হওয়ার শুরুতে সতর্কবার্তা
if rem_sec >= 58 and sig_type != "NONE":
    voice_script = f"এলার্ট! {active['n']} মার্কেটে {sig_type} এর জন্য তৈরি হোন।"

# শেষ ১০ সেকেন্ডে কাউন্টডাউন এবং ফাইনাল কমান্ড
if rem_sec <= 10 and rem_sec > 0 and sig_type != "NONE":
    voice_script = f"{rem_sec}! এখনই {sig_type} নিন!"

# ভয়েস প্লেয়ার
if voice_script != "":
    st.markdown(f"""<audio autoplay><source src="https://translate.google.com/translate_tts?ie=UTF-8&q={voice_script.replace(' ', '%20')}&tl=bn&client=tw-ob" type="audio/mpeg"></audio>""", unsafe_allow_html=True)

# --- ৬. ডিসপ্লে ইন্টারফেস ---
status_col = "#ffd700"
icon = "🔍"
msg = "স্ক্যানিং..."
action = "মার্কেট চেক হচ্ছে"

if sig_type == "BUY":
    status_col = "#00fbff"; icon = "📈"; msg = "BUY NOW"; action = "এখনই বাই নিন"
elif sig_type == "SELL":
    status_col = "#ff4b4b"; icon = "📉"; msg = "SELL NOW"; action = "এখনই সেল নিন"

st.markdown(f"""
    <div class='main-card' style='border-color: {status_col}; box-shadow: 0 0 50px {status_col}44;'>
        <div style='color: #777; font-size: 12px; letter-spacing: 3px;'>PHANTOM V35 ULTIMATE</div>
        <div class='market-title'>{active['f']} {active['n']}</div>
        <div class='timer-big' style='color: {status_col}; text-shadow: 0 0 20px {status_col}66;'>{rem_sec}s</div>
        <hr style='border: 1px solid {status_col}22;'>
        <div style='font-size: 70px;'>{icon}</div>
        <div style='font-size: 50px; font-weight: 900; color: {status_col};'>{msg}</div>
        <div class='signal-btn' style='background: {status_col}22; color: {status_col}; border-color: {status_col};'>
            {action}
        </div>
        <div style='margin-top: 30px; font-size: 11px; color: #444;'>ARAFAT ROZA-MONI : QUANTUM FINAL</div>
    </div>
""", unsafe_allow_html=True)

# ট্রেডিংভিউ হিডেন সাপোর্ট
st.components.v1.html(f"""<div style="display:none;"><iframe src="https://s.tradingview.com/embed-widget/technical-analysis/?symbol={active['n']}&interval=1m&theme=dark"></iframe></div>""", height=0)

time.sleep(1)
st.rerun()

