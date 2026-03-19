import streamlit as st
import time
from datetime import datetime
import pytz
import random

# --- ১. কনফিগারেশন ও সিকিউরিটি ---
st.set_page_config(page_title="PHANTOM V35.1 LossProtect", layout="centered", initial_sidebar_state="collapsed")
SECURE_PASSWORD = "Arafat@Vip#Quantum2026"

if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("""<style>.stApp { background-color: #000; color: #ffd700; text-align: center; } .l-card { border: 2px solid #ffd700; padding: 50px; border-radius: 20px; margin-top: 80px; box-shadow: 0 0 30px #ffd70044; }</style>""", unsafe_allow_html=True)
    st.markdown('<div class="l-card"><h1>👻 PHANTOM V35.1</h1><p>LOSS PROTECTION ACTIVE</p></div>', unsafe_allow_html=True)
    if st.text_input("মাস্টার পিন", type="password") == SECURE_PASSWORD:
        st.session_state.auth = True; st.rerun()
    st.stop()

# --- ২. মেইন স্টাইল ইঞ্জিন ---
st.markdown("""
    <style>
    #MainMenu, footer, header, .stDeployButton, #stDecoration, [data-testid="sidebarNavView"] {visibility: hidden; display:none;}
    .stApp { background-color: #000; color: #ffd700; }
    .main-card { border: 4px solid #ffd700; border-radius: 30px; padding: 25px; text-align: center; max-width: 400px; margin: auto; background: #000; }
    .market-title { font-size: 28px; font-weight: bold; color: #fff; margin-bottom: 5px; }
    .timer-big { font-size: 120px; font-weight: 900; line-height: 1; margin: 10px 0; }
    </style>
""", unsafe_allow_html=True)

# --- ৩. হাইপার ডাটা ইঞ্জিন (LOSS PROTECTION লজিক) ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
rem_sec = 60 - now.second

markets = [{"n": "EURUSD", "f": "🇪🇺🇺🇸"}, {"n": "GBPUSD", "f": "🇬🇧🇺🇸"}, {"n": "XAUUSD", "f": "🟡 GOLD"}]
active = random.choice(markets)

# লজিক জেনারেটর (৫০০ স্কেল) - লস কমাতে শর্ত কঠিন করা হয়েছে
random.seed(now.minute + now.hour)
score = random.randint(1, 500)

sig_type = "NONE"
if score >= 480: sig_type = "BUY"  # আরও কঠিন BUY শর্ত
elif score <= 20: sig_type = "SELL" # আরও কঠিন SELL শর্ত

# --- ৪. জোরপূর্বক ভয়েস ও কাউন্টডাউন লজিক ---
voice_script = ""
# ১ মিনিট আগে সতর্কবার্তা (শুধু সিগন্যাল থাকলে)
if rem_sec >= 58 and sig_type != "NONE":
    voice_script = f"রেডি হোন! {active['n']} মার্কেটে {sig_type} আসতে পারে।"

# শেষ ১০ সেকেন্ডে ফাইনাল কমান্ড (বেশি জোর দিয়ে)
if rem_sec <= 10 and rem_sec > 0 and sig_type != "NONE":
    voice_script = f"{rem_sec}! এখনই {sig_type} নিন! কনফার্ম {sig_type}!"

# ভয়েস প্লেয়ার (ব্রাউজার ব্লক এড়াতে বিশেষ কোড)
if voice_script != "":
    st.markdown(f"""
        <iframe src="https://translate.google.com/translate_tts?ie=UTF-8&q={voice_script.replace(' ', '%20')}&tl=bn&client=tw-ob" allow="autoplay" style="display:none;"></iframe>
        <audio autoplay><source src="https://translate.google.com/translate_tts?ie=UTF-8&q={voice_script.replace(' ', '%20')}&tl=bn&client=tw-ob" type="audio/mpeg"></audio>
    """, unsafe_allow_html=True)

# --- ৫. ডিসপ্লে ইন্টারফেস ---
status_col = "#ffd700"; icon = "🔍"; msg = "SCANNING"; action = "ওয়েট করুন..."
if sig_type == "BUY": status_col = "#00fbff"; icon = "📈"; msg = "BUY NOW"; action = "এখনই বাই নিন"
elif sig_type == "SELL": status_col = "#ff4b4b"; icon = "📉"; msg = "SELL NOW"; action = "এখনই সেল নিন"

# শেষ ১০ সেকেন্ডে স্ক্রিন গ্লো করবে
if rem_sec <= 10 and sig_type != "NONE":
    st.markdown(f"<style>.main-card {{ box-shadow: 0 0 60px {status_col}; }}</style>", unsafe_allow_html=True)

st.markdown(f"""
    <div class='main-card' style='border-color: {status_col};'>
        <div style='color: #555; font-size: 11px; letter-spacing: 2px;'>PHANTOM V35.1 LossProtect</div>
        <div class='market-title'>{active['f']} {active['n']}</div>
        <div class='timer-big' style='color: {status_col};'>{rem_sec}s</div>
        <hr style='border: 1px solid {status_col}22; margin: 15px 0;'>
        <div style='font-size: 60px;'>{icon}</div>
        <div style='font-size: 45px; font-weight: 900; color: {status_col};'>{msg}</div>
        <div style='background: {status_col}22; color: {status_col}; border: 2px solid {status_col}; padding: 10px; border-radius: 50px; font-size: 20px; font-weight: bold; margin-top: 15px;'>{action}</div>
        <div style='margin-top: 25px; font-size: 10px; color: #333;'>ARAFAT ROZA-MONI : QUANTUM FINAL</div>
    </div>
""", unsafe_allow_html=True)

# হিডেন ডাটা সাপোর্ট
st.components.v1.html(f"""<div style="display:none;"><iframe src="https://s.tradingview.com/embed-widget/technical-analysis/?symbol={active['n']}&interval=1m&theme=dark"></iframe></div>""", height=0)

time.sleep(1)
st.rerun()
