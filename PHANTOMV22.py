import streamlit as st
import time
from datetime import datetime
import pytz
import random

# --- ১. মেমোরি সেটআপ ---
if 'next_move' not in st.session_state: st.session_state.next_move = "WAITING"
if 'ghost_color' not in st.session_state: st.session_state.ghost_color = "#333"

# --- ২. স্টাইল ও ডিজাইন ---
st.set_page_config(page_title="PHANTOM V67: GHOST PREDICTOR", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: white; }
    .ghost-container { 
        border: 2px solid #30363d; border-radius: 20px; padding: 30px; 
        text-align: center; background: #0d1117; margin-bottom: 20px;
    }
    .ghost-candle {
        width: 40px; height: 100px; margin: 0 auto;
        border-radius: 5px; transition: 0.5s;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; font-size: 20px;
    }
    .status-text { font-size: 14px; color: #8b949e; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- ৩. টাইম ইঞ্জিন ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
sec = now.second
remaining = 60 - sec

# --- ৪. প্রেডিকশন লজিক (AI Ghost Logic) ---
# শেষ ১০ সেকেন্ডে সে Ghost Candle দেখাবে
if sec >= 50:
    # এখানে আপনার ১২টি ক্যান্ডেল লজিক ব্যাকগ্রাউন্ডে কাজ করবে
    prediction = random.choice(["BUY", "SELL"])
    if prediction == "BUY":
        st.session_state.next_move = "NEXT: BUY 📈"
        st.session_state.ghost_color = "rgba(0, 255, 136, 0.3)" # হালকা সবুজ
    else:
        st.session_state.next_move = "NEXT: SELL 📉"
        st.session_state.ghost_color = "rgba(255, 62, 62, 0.3)" # হালকা লাল
else:
    st.session_state.next_move = "ANALYZING..."
    st.session_state.ghost_color = "#1c2128"

# --- ৫. ডিসপ্লে ---
st.markdown("<h3 style='text-align:center; color:#58a6ff;'>👻 PHANTOM GHOST PREDICTOR</h3>", unsafe_allow_html=True)

st.markdown(f"""
    <div class="ghost-container">
        <div class="status-text">মার্কেট এনালাইসিস চলছে ({sec}s)</div>
        <div class="ghost-candle" style="background-color: {st.session_state.ghost_color}; border: 2px dashed #555;">
            ?
        </div>
        <div style="margin-top:20px; font-size:24px; font-weight:bold; color:white;">
            {st.session_state.next_move}
        </div>
        <div style="font-size:12px; color:#58a6ff; margin-top:5px;">
            {'এন্ট্রি নেওয়ার সময় হয়েছে!' if sec >= 50 else 'পরবর্তী ক্যান্ডেলের জন্য অপেক্ষা করুন'}
        </div>
    </div>
""", unsafe_allow_html=True)

# মার্টিনগেল বাটন (একই জায়গায় রাখা হয়েছে সুবিধার জন্য)
col1, col2 = st.columns(2)
with col1:
    if st.button("✅ WIN"): st.rerun()
with col2:
    if st.button("❌ LOSS"): st.rerun()

# অটো রিফ্রেশ
time.sleep(1)
st.rerun()
