import streamlit as st
import time
from datetime import datetime
import pytz
import random

# --- ১. মেম্বারশিপ ও কনফিগারেশন ---
USER_KEYS = {"ARAFAT_VIP_2026": "Arafat Bhai (Admin)"}
st.set_page_config(page_title="PHANTOM V22 RADAR", layout="wide")

if 'auth' not in st.session_state: st.session_state.auth = False

# --- ২. লগইন ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center;'>👻 PHANTOM V22</h1>", unsafe_allow_html=True)
    key_input = st.text_input("মাস্টার পাসওয়ার্ড দিন", type="password")
    if st.button("সিস্টেম আনলক করুন"):
        if key_input in USER_KEYS:
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- ৩. রাডার ডিজাইন (UI) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: white; }
    .radar-container {
        border: 2px dashed #ffd700; border-radius: 20px; padding: 25px;
        text-align: center; background: radial-gradient(circle, #1a1a00, #000);
        box-shadow: 0 0 20px #ffd70033; margin-bottom: 20px;
    }
    .alert-button {
        background: #ffd700; color: black; padding: 10px 20px;
        border-radius: 50px; font-weight: bold; font-size: 20px;
        display: inline-block; cursor: pointer; animation: pulse 1s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.7); }
        70% { transform: scale(1.05); box-shadow: 0 0 0 15px rgba(255, 215, 0, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 215, 0, 0); }
    }
    .status-box { font-size: 14px; color: #aaa; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- ৪. সাইডবার সেটিংস ---
st.sidebar.header("⚙️ একাউন্ট সেটিংস")
user_lot = st.sidebar.number_input("আপনার লট সাইজ", value=0.01, step=0.01)

# --- ৫. লাইভ রাডার ইঞ্জিন ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)

# ব্যাংক অর্ডার ডিটেকশন সিমুলেশন
random.seed(now.second)
bank_detect = random.choice([True, False, False, False]) # মাঝে মাঝে ব্যাংক মুভমেন্ট দেখাবে

st.markdown("""
    <div class="radar-container">
        <h2 style="color:#ffd700;">📡 LIVE BANK RADAR</h2>
""", unsafe_allow_html=True)

if bank_detect:
    market_name = random.choice(["EURUSD", "GOLD", "GBPUSD"])
    action = random.choice(["BUY", "SELL"])
    color = "#00ff00" if action == "BUY" else "#ff4b4b"
    
    st.markdown(f"""
        <div class="alert-button">🚨 BANK {action} ORDER DETECTED!</div>
        <div style="font-size: 24px; margin-top:15px; color:{color}; font-weight:bold;">
            {market_name} রকেটের মতো {"উপরে" if action == "BUY" else "নিচে"} যাচ্ছে!
        </div>
        <div class="status-box">প্রাইস জোন: {random.uniform(1.08500, 1.08900):.5f} | ভলিউম: {random.randint(50000, 100000)} লট</div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div style="font-size: 18px; color:#555;">স্ক্যানিং হচ্ছে... ব্যাংক অর্ডারের জন্য অপেক্ষা করুন...</div>
        <div class="status-box">মার্কেট এখন রিটেইল ট্রেডারদের দখলে।</div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# --- ৬. নিয়মিত সিগন্যাল ডিসপ্লে ---
st.markdown("### 📊 বর্তমান মার্কেট কন্ডিশন")
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
        <div style="background:#111; padding:15px; border-radius:10px; border-left:5px solid #00fbff;">
            <b>EURUSD (৫মি)</b><br>
            <span style="color:#00ff00;">TP: +${round(15.0 * user_lot * 10, 2)}</span> | 
            <span style="color:#ff4b4b;">SL: -${round(6.0 * user_lot * 10, 2)}</span>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div style="background:#111; padding:15px; border-radius:10px; border-left:5px solid #ffd700;">
            <b>GOLD (১৫মি)</b><br>
            <span style="color:#00ff00;">TP: +${round(45.0 * user_lot * 10, 2)}</span> | 
            <span style="color:#ff4b4b;">SL: -${round(18.0 * user_lot * 10, 2)}</span>
        </div>
    """, unsafe_allow_html=True)

time.sleep(5) # ৫ সেকেন্ড পর পর অটো রিফ্রেশ হবে ব্যাংক মুভমেন্ট ধরার জন্য
st.rerun()
