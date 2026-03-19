import streamlit as st
import time
from datetime import datetime
import pytz
import random

# --- ১. হাইপার কনফিগারেশন ও সিকিউরিটি ---
st.set_page_config(page_title="PHANTOM V34.4", layout="centered", initial_sidebar_state="collapsed")

SECURE_PASSWORD = "Arafat@Vip#Quantum2026"

if 'auth' not in st.session_state: st.session_state.auth = False

# লগইন ইন্টারফেস
if not st.session_state.auth:
    st.markdown("""<style>.stApp { background-color: #000; color: #ffd700; text-align: center; } .login-box { border: 2px solid #ffd700; padding: 40px; border-radius: 20px; margin-top: 50px; box-shadow: 0 0 30px #ffd70044; }</style>""", unsafe_allow_html=True)
    st.markdown('<div class="login-box"><div style="font-size:80px;">👻</div><h2>PHANTOM V34.4</h2><p style="color:#555;">HYPER-SIGNAL ACTIVE</p></div>', unsafe_allow_html=True)
    pwd_input = st.text_input("মাস্টার পিন", type="password")
    if st.button("আনলক করুন 🔓"):
        if pwd_input == SECURE_PASSWORD:
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- ২. মেইন ডিসপ্লে স্টাইল ---
st.markdown("""<style>.stApp { background-color: #000; color: #ffd700; } .card { border: 3px solid #ffd700; border-radius: 25px; padding: 25px; text-align: center; max-width: 380px; margin: auto; background: #000; }</style>""", unsafe_allow_html=True)

# --- ৩. হাইপার-সিগন্যাল ইঞ্জিন (আপনার দেওয়া লজিক অনুযায়ী) ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
rem_sec = 60 - now.second

# ৪০টি টপ মার্কেট লিস্ট
markets = ["EURUSD", "GBPUSD", "XAUUSD", "BTCUSD", "AUDCAD", "USDJPY", "EURJPY", "GBPJPY", "USDCAD", "EURAUD"]
active_m = random.choice(markets)

# লজিক শিথিল করা হয়েছে যাতে ঘনঘন সিগন্যাল আসে (৫০০ স্কেল)
random.seed(now.minute + now.second)
score = random.randint(1, 500)

# এখন ৪৫০ হলেই সিগন্যাল দিবে (বেশি সিগন্যাল পাওয়ার জন্য)
if score >= 450: 
    sig, txt, icon, bn = "STRONG BUY", "#00fbff", "📈", "বাই (BUY) এন্ট্রি নিন"
    v_cmd = f"এলার্ট! {active_m} মার্কেটে বাই এন্ট্রি নিন।"
elif score <= 50:
    sig, txt, icon, bn = "STRONG SELL", "#ff4b4b", "📉", "সেল (SELL) এন্ট্রি নিন"
    v_cmd = f"এলার্ট! {active_m} মার্কেটে সেল এন্ট্রি নিন।"
else:
    sig, txt, icon, bn, v_cmd = "SCANNING", "#ffd700", "🔍", "মার্কেট স্ক্যান হচ্ছে...", ""

# ভয়েস এলার্ট (সিগন্যাল আসার ঠিক আগে)
if v_cmd != "" and rem_sec >= 58:
    st.markdown(f"""<audio autoplay><source src="https://translate.google.com/translate_tts?ie=UTF-8&q={v_cmd.replace(' ', '%20')}&tl=bn&client=tw-ob" type="audio/mpeg"></audio>""", unsafe_allow_html=True)

# ডিসপ্লে কার্ড
st.markdown(f"""
    <div class='card' style='border-color: {txt}; box-shadow: 0 0 40px {txt}33;'>
        <div style='font-size: 11px; letter-spacing: 2px; color: #777;'>PHANTOM HYPER-SIGNAL V34.4</div>
        <div style='margin: 15px 0; font-size: 26px; font-weight: bold; color: #fff;'>{active_m} (OTC)</div>
        <div style='font-size: 110px; font-weight: 900; line-height: 1; color: {txt};'>{rem_sec}s</div>
        <hr style='border: 0.5px solid {txt}33; margin: 25px 0;'>
        <div style='font-size: 60px;'>{icon}</div>
        <div style='font-size: 40px; font-weight: 900; color: {txt};'>{sig}</div>
        <div style='background: {txt}22; padding: 10px 30px; border-radius: 50px; display: inline-block; margin-top: 15px; color: {txt}; font-weight: bold; border: 1px solid {txt}55;'>{bn}</div>
        <div style='margin-top: 30px; font-size: 10px; opacity: 0.4;'>ARAFAT ROZA-MONI : QUANTUM SERIES</div>
    </div>
""", unsafe_allow_html=True)

# আপনার দেওয়া সেই হিডেন পারমিশন লজিক
st.components.v1.html(f"""<div style="display:none;"><iframe src="https://s.tradingview.com/embed-widget/technical-analysis/?symbol={active_m}&interval=1m&theme=dark"></iframe></div>""", height=0)

time.sleep(1)
st.rerun()
