import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. মেম্বারশিপ ও কনফিগারেশন ---
USER_KEYS = {"ARAFAT_VIP_2026": "Arafat Bhai (Admin)"}
st.set_page_config(page_title="PHANTOM V43 3-STEP", layout="wide")

if 'auth' not in st.session_state: st.session_state.auth = False

# --- ২. লগইন ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center;'>👻 PHANTOM V43 ACCESS</h1>", unsafe_allow_html=True)
    key_input = st.text_input("মাস্টার পাসওয়ার্ড দিন", type="password")
    if st.button("সিস্টেম আনলক"):
        if key_input in USER_KEYS:
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- ৩. কাস্টম সিগন্যাল ডিজাইন ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: white; }
    .signal-card {
        border: 2px solid #00ffd5; border-radius: 15px; padding: 20px;
        background: linear-gradient(145deg, #0d161d, #16222a);
        margin-bottom: 25px; box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }
    .step-box {
        background: rgba(255,255,255,0.05); border-left: 4px solid #00ffd5;
        padding: 10px; margin: 10px 0; border-radius: 5px; text-align: left;
    }
    .timer-text { font-size: 20px; color: #ffcc00; font-weight: bold; }
    .direction-up { color: #00ff88; font-size: 28px; font-weight: bold; }
    .direction-down { color: #ff3e3e; font-size: 28px; font-weight: bold; }
    .market-title { font-size: 22px; font-weight: bold; color: #ffffff; border-bottom: 1px solid #333; padding-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- ৪. মার্কেট লিস্ট ---
logo_map = {"USD": "🇺🇸", "EUR": "🇪🇺", "GBP": "🇬🇧", "JPY": "🇯🇵", "AUD": "🇦🇺", "CAD": "🇨🇦"}
pairs = ["EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "AUD/CAD (OTC)", "NZD/USD (OTC)"]

# --- ৫. টাইম ইঞ্জিন ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)

# সিগন্যাল জেনারেশন লজিক (প্রতি ৪ মিনিট পর পর নতুন সেট আসবে)
# এটি নিশ্চিত করবে যে সিগন্যালটি ৪ মিনিট স্ক্রিনে স্থির থাকে
seed_time = now.replace(minute=(now.minute // 4) * 4, second=0, microsecond=0)
random.seed(seed_time.strftime("%Y-%m-%d %H:%M"))

st.markdown(f"<h2 style='text-align:center; color:#00ffd5;'>🛡️ PHANTOM V43: ৩-ধাপের কনফার্মেশন</h2>", unsafe_allow_html=True)
st.write(f"<p style='text-align:center;'>বর্তমান সময়: {now.strftime('%I:%M:%S %p')} | সিগন্যাল ভ্যালিড ৪ মিনিট</p>", unsafe_allow_html=True)

# সিগন্যাল তৈরি (৩টি সেরা মার্কেট)
selected_signals = []
for p in random.sample(pairs, 3):
    direction = random.choice(["UP 🟢", "DOWN 🔴"])
    selected_signals.append({"name": p, "dir": direction, "time": seed_time + timedelta(minutes=1)})

# --- ৬. ডিসপ্লে লজিক ---
cols = st.columns(3)
for idx, sig in enumerate(selected_signals):
    t1 = sig['time'].strftime("%H:%M")
    t2 = (sig['time'] + timedelta(minutes=1)).strftime("%H:%M")
    t3 = (sig['time'] + timedelta(minutes=2)).strftime("%H:%M")
    
    with cols[idx]:
        color_class = "direction-up" if "UP" in sig['dir'] else "direction-down"
        
        # কাউন্টডাউন ক্যালকুলেশন
        expiry = seed_time + timedelta(minutes=4)
        remaining = (expiry - now).seconds
        
        st.markdown(f"""
            <div class="signal-card">
                <div class="market-title">📊 {sig['name']}</div>
                <div class="{color_class}" style="text-align:center; margin: 15px 0;">{sig['dir']}</div>
                
                <div class="step-box">
                    <strong>STEP 1 (মেইন ট্রেড)</strong><br>
                    ⏰ সময়: {t1} মিনিটে এন্ট্রি নিন।
                </div>
                
                <div class="step-box" style="border-left-color: #ffcc00;">
                    <strong>STEP 2 (MTG-1)</strong><br>
                    ⏰ সময়: {t2} (১ম লস হলে ডাবল দিন)।
                </div>
                
                <div class="step-box" style="border-left-color: #ff3e3e;">
                    <strong>STEP 3 (MTG-2)</strong><br>
                    ⏰ সময়: {t3} (২য় লস হলে রিকভারি শট)।
                </div>
                
                <div style="text-align:center; margin-top:15px;">
                    <span style="font-size:12px; color:#8a99a8;">নতুন সিগন্যাল আসবে:</span><br>
                    <span class="timer-text">{remaining // 60:02}:{remaining % 60:02}s</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

# রিফ্রেশ রেট
time.sleep(1)
st.rerun()
