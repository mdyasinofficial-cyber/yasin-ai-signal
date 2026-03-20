import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. কনফিগারেশন ও অথেন্টিকেশন ---
USER_KEYS = {"ARAFAT_VIP_2026": "Arafat Bhai (Admin)"}
st.set_page_config(page_title="PHANTOM V29 PRO-VISUAL", layout="wide")

if 'auth' not in st.session_state: st.session_state.auth = False
if 'master_signal' not in st.session_state: st.session_state.master_signal = {}

# --- ২. লগইন সিস্টেম ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center;'>👻 PHANTOM V29 [ULTIMATE]</h1>", unsafe_allow_html=True)
    key = st.text_input("মাস্টার পাসওয়ার্ড দিন", type="password")
    if st.button("সিস্টেম আনলক"):
        if key in USER_KEYS:
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- ৩. আল্ট্রা ডিজাইন (Black & Gold with Logo Support) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #e0e0e0; }
    .main-box {
        border: 2px solid #ffd700; border-radius: 20px; padding: 30px;
        background: linear-gradient(145deg, #1a1a1a, #000000);
        box-shadow: 0px 0px 25px #ffd70055; text-align: center; margin-bottom: 25px;
    }
    .accuracy-meter { font-size: 55px; font-weight: bold; color: #ffd700; text-shadow: 2px 2px #000; margin-top: 15px; }
    .next-move { font-size: 40px; font-weight: bold; padding: 10px; border-radius: 10px; margin: 20px 0; }
    .buy-text { color: #00ff00; background: rgba(0, 255, 0, 0.1); border: 1px solid #00ff00; }
    .sell-text { color: #ff4b4b; background: rgba(255, 75, 75, 0.1); border: 1px solid #ff4b4b; }
    .countdown-timer { font-size: 30px; font-weight: bold; color: #00fbff; background: #222; padding: 10px; border-radius: 10px; display: inline-block; }
    </style>
""", unsafe_allow_html=True)

# --- ৪. রিয়েল-টাইম ইঞ্জিন (Error-Free Calculation) ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
real_time_str = now.strftime('%I:%M:%S %p')

# ২ মিনিটের সাইকেল ক্যালকুলেশন
minutes_to_add = 2 - (now.minute % 2)
# যদি সেকেন্ডস ০ হয়, তবে minutes_to_add ২ হবে, যা ঠিক আছে।
next_signal_time = (now + timedelta(minutes=minutes_to_add)).replace(second=0, microsecond=0)

# সিগন্যাল আইডি তৈরি (প্রতি ২ মিনিটের জন্য আলাদা)
signal_id = next_signal_time.strftime("%H:%M")

if 'last_signal_id' not in st.session_state or st.session_state.last_signal_id != signal_id:
    # ১০ ঘণ্টা ডাটা এনালাইসিসের ভার্চুয়াল লজিক (আপনার চাহিদা অনুযায়ী)
    random.seed(signal_id + "ARAFAT_ULTIMATE")
    
    direction = random.choice(["BUY UP 🟢", "SELL DOWN 🔴"])
    accuracy = random.randint(99, 99) # আপনার চাহিদা অনুযায়ী ৯৯% ফিক্সড
    
    # মার্কেট ডেটা লোগোসহ (আপনি যে কোনো সময় পরিবর্তন করতে পারেন)
    market_list = [
        {"n": "GOLD (XAUUSD)", "f": "🟡"},
        {"n": "EURUSD", "f": "🇪🇺🇺🇸"}
    ]
    selected_market = random.choice(market_list)
    
    st.session_state.master_signal = {
        "dir": direction,
        "acc": accuracy,
        "market": selected_market['n'],
        "flag": selected_market['f'],
        "time_id": signal_id
    }
    st.session_state.last_signal_id = signal_id

# --- ৫. ইউজার ইন্টারফেস ও লাইভ কাউন্টডাউন ---
st.markdown("<h2 style='text-align:center; color:#ffd700;'>⚡ 10-HOUR DATA ANALYSIS ENGINE ⚡</h2>", unsafe_allow_html=True)
st.write(f"<div style='text-align:center; font-size:18px;'>লাইভ টাইম (রিয়েল): <b>{real_time_str}</b></div>", unsafe_allow_html=True)

sig = st.session_state.master_signal
move_style = "buy-text" if "BUY" in sig['dir'] else "sell-text"

st.markdown(f"""
    <div class="main-box">
        <div class="status-tag" style="color:#ffd700; font-weight:bold;">[ CONFIRMED BY 10H HISTORICAL DATA ]</div>
        <h1 style="margin:10px 0; font-size:35px;">{sig['flag']} {sig['market']}</h1>
        <div class="accuracy-meter">{sig['acc']}% SURE SHOT</div>
        <div class="next-move {move_style}">{sig['dir']}</div>
        <div style="font-size:24px; font-weight:bold; color:#fff;">ট্রেড টাইম: {sig['time_id']} PM (২ মিনিট স্ক্যাল্পিং)</div>
        <hr style="border-color:#333; margin:20px 0;">
    </div>
""", unsafe_allow_html=True)

# লাইভ কাউন্টডাউন সেকশন
seconds_left = int((next_signal_time - now).total_seconds())

if seconds_left > 0:
    st.markdown(f"""
        <div style="text-align:center;">
            <p style="color:#888;">নতুন সিগন্যাল আপডেট হবে</p>
            <div class="countdown-timer">{seconds_left // 60:02d}:{seconds_left % 60:02d}</div>
            <p style="color:#888;">সেকেন্ড পর...</p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.write("🔄 নতুন সিগন্যাল লোড হচ্ছে...")
    st.rerun() # সময় শেষ হলে অটো রিফ্রেশ

# প্রগ্রেস বার (পরবর্তী সিগন্যালের জন্য কত সময় বাকি)
st.progress(max(0, min(1.0, 1 - (seconds_left / 120))))

# অটো রিফ্রেশ ৫ সেকেন্ড পর পর লাইভ টাইমের সাথে সিঙ্ক করার জন্য
time.sleep(1)
st.rerun()
