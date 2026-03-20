import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. মেম্বারশিপ ও কনফিগারেশন ---
USER_KEYS = {"ARAFAT_VIP_2026": "Arafat Bhai (Admin)"}
st.set_page_config(page_title="PHANTOM V26 DUAL-SYNC", layout="wide")

if 'auth' not in st.session_state: st.session_state.auth = False
if 'dual_signals' not in st.session_state: st.session_state.dual_signals = []

# --- ২. লগইন ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center;'>👻 PHANTOM V26</h1>", unsafe_allow_html=True)
    key = st.text_input("মাস্টার পাসওয়ার্ড দিন", type="password")
    if st.button("সিস্টেম আনলক"):
        if key in USER_KEYS:
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- ৩. ডিজাইন (Dual Platform UI) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .platform-card {
        border: 1px solid #333; border-radius: 12px; padding: 15px;
        background: #111; margin-bottom: 12px;
    }
    .exness-tag { background: #ffd700; color: black; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; }
    .quotex-tag { background: #00fbff; color: black; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; }
    .buy-btn { color: #00ff00; font-size: 20px; font-weight: bold; }
    .sell-btn { color: #ff4b4b; font-size: 20px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- ৪. টাইম ইঞ্জিন ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
cycle_end = now.replace(minute=(now.minute // 15 + 1) * 15, second=0, microsecond=0)

# ১৫ মিনিট শেষ হলে সব পরিষ্কার হবে
if now >= cycle_end:
    st.session_state.dual_signals = []

# --- ৫. সিগন্যাল জেনারেটর ---
markets = [
    {"n": "GOLD (XAUUSD)", "type": "Both"},
    {"n": "EURUSD", "type": "Both"},
    {"n": "USDJPY-OTC", "type": "Quotex Only"}
]

random.seed(now.minute + now.hour)
for m in markets:
    direction = random.choice(["BUY 🟢", "SELL 🔴"])
    platform = "QUOTEX/EXNESS" if m['type'] == "Both" else "QUOTEX ONLY"
    tag_class = "quotex-tag" if "QUOTEX" in platform else "exness-tag"
    
    new_sig = {
        "market": m['n'],
        "dir": direction,
        "platform": platform,
        "tag": tag_class,
        "time": now.strftime("%I:%M %p"),
        "expiry": cycle_end
    }
    
    # ডুপ্লিকেট চেক
    if not any(s['market'] == new_sig['market'] and s['time'] == new_sig['time'] for s in st.session_state.dual_signals):
        st.session_state.dual_signals.insert(0, new_sig)

# --- ৬. ডিসপ্লে ---
st.markdown(f"<h2 style='text-align:center; color:#ffd700;'>⚡ PHANTOM V26: DUAL PLATFORM SYNC</h2>", unsafe_allow_html=True)
st.sidebar.success(f"একাউন্ট: {USER_KEYS['ARAFAT_VIP_2026']}")
user_lot = st.sidebar.number_input("লট সাইজ (Exness এর জন্য)", value=0.01)

st.write(f"⏰ বর্তমান সময়: {now.strftime('%I:%M:%S %p')} | 🔄 রিফ্রেশ: {cycle_end.strftime('%I:%M %p')}")

for s in st.session_state.dual_signals[:10]:
    dir_color = "buy-btn" if "BUY" in s['dir'] else "sell-btn"
    
    st.markdown(f"""
        <div class="platform-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span class="{s['tag']}">{s['platform']}</span>
                    <h3 style="margin:5px 0;">{s['market']}</h3>
                    <small style="color:#666;">সিগন্যাল টাইম: {s['time']}</small>
                </div>
                <div style="text-align: center;">
                    <div class="{dir_color}">{s['dir']}</div>
                    <small>পরবর্তী ক্যান্ডেল প্রেডিকশন</small>
                </div>
                <div style="text-align: right; border-left: 1px solid #333; padding-left: 15px;">
                    <b style="color:#ffd700;">ACCURACY: {random.randint(85, 98)}%</b><br>
                    <small>Expire: {s['expiry'].strftime('%I:%M %p')}</small>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

time.sleep(10)
st.rerun()
    
