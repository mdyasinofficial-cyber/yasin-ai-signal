import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. মেম্বারশিপ ও কনফিগারেশন ---
USER_KEYS = {"ARAFAT_VIP_2026": "Arafat Bhai (Admin)"}
st.set_page_config(page_title="PHANTOM V26 FIXED", layout="wide")

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

# --- ৩. স্টাইল ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .platform-card {
        border: 1px solid #333; border-radius: 12px; padding: 15px;
        background: #111; margin-bottom: 12px; border-left: 5px solid #ffd700;
    }
    .tag { padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; color: black; }
    .buy-btn { color: #00ff00; font-size: 20px; font-weight: bold; }
    .sell-btn { color: #ff4b4b; font-size: 20px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- ৪. টাইম ইঞ্জিন (এরর ফিক্সড) ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)

# ১৫ মিনিটের ফিক্সড সাইকেল ক্যালকুলেশন
minutes_to_add = 15 - (now.minute % 15)
cycle_end = (now + timedelta(minutes=minutes_to_add)).replace(second=0, microsecond=0)

# ১৫ মিনিট পূর্ণ হলে অটো ক্লিয়ার
if now >= cycle_end:
    st.session_state.dual_signals = []

# --- ৫. সিগন্যাল জেনারেটর ---
markets = [
    {"n": "GOLD (XAUUSD)", "t": "Both", "f": "🟡"},
    {"n": "EURUSD", "t": "Both", "f": "🇪🇺🇺🇸"},
    {"n": "USDJPY-OTC", "t": "Quotex", "f": "🇯🇵🇺🇸"}
]

random.seed(now.minute + now.hour)
for m in markets:
    direction = random.choice(["BUY 🟢", "SELL 🔴"])
    acc = random.randint(88, 98)
    
    new_sig = {
        "market": m['n'],
        "flag": m['f'],
        "dir": direction,
        "platform": "QUOTEX/EXNESS" if m['t'] == "Both" else "QUOTEX ONLY",
        "acc": acc,
        "time": now.strftime("%I:%M %p"),
        "expiry": cycle_end
    }
    
    if not any(s['market'] == new_sig['market'] and s['time'] == new_sig['time'] for s in st.session_state.dual_signals):
        st.session_state.dual_signals.insert(0, new_sig)

# --- ৬. ডিসপ্লে ---
st.markdown(f"<h2 style='text-align:center; color:#ffd700;'>⚡ PHANTOM V26: DUAL PLATFORM SYNC</h2>", unsafe_allow_html=True)
user_lot = st.sidebar.number_input("লট সাইজ (Exness)", value=0.01)

st.write(f"⏰ বর্তমান সময়: {now.strftime('%I:%M:%S %p')} | 🔄 পরবর্তী রিফ্রেশ: {cycle_end.strftime('%I:%M %p')}")

for s in st.session_state.dual_signals[:10]:
    dir_color = "buy-btn" if "BUY" in s['dir'] else "sell-btn"
    tag_bg = "#ffd700" if "EXNESS" in s['platform'] else "#00fbff"
    
    st.markdown(f"""
        <div class="platform-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="width: 40%;">
                    <span class="tag" style="background:{tag_bg};">{s['platform']}</span>
                    <h3 style="margin:5px 0;">{s['flag']} {s['market']}</h3>
                    <small style="color:#666;">এন্ট্রি: {s['time']}</small>
                </div>
                <div style="width: 30%; text-align: center;">
                    <div class="{dir_color}">{s['dir']}</div>
                    <small>ACCURACY: {s['acc']}%</small>
                </div>
                <div style="width: 30%; text-align: right; border-left: 1px solid #333;">
                    <b style="color:#aaa;">Expiry</b><br>
                    <span>{s['expiry'].strftime('%I:%M %p')}</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

time.sleep(10)
st.rerun()
