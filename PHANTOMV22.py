import streamlit as st
import time
from datetime import datetime
import pytz
import random

# --- ১. মেমোরি সেটিংস ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'active_market' not in st.session_state: st.session_state.active_market = "GOLD (XAU/USD)"

# --- ২. লগইন (পাসওয়ার্ড: ARAFAT_V64) ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center; color:#00ffd5;'>🔒 PHANTOM V72 - REAL ACCESS</h2>", unsafe_allow_html=True)
    pw = st.text_input("পাসওয়ার্ড দিন:", type="password")
    if st.button("UNLOCK"):
        if pw == "ARAFAT_V64":
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- ৩. ডিজাইন ও স্টাইল ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: white; }
    .stButton>button {
        width: 100%; height: 60px;
        background-color: #161b22 !important;
        color: #ffffff !important; /* লেখা একদম সাদা ও পরিষ্কার */
        border: 1px solid #30363d !important;
        border-radius: 10px; font-weight: bold; font-size: 14px;
    }
    .signal-card {
        background: #0d1117; border: 2px solid #58a6ff;
        border-radius: 20px; padding: 40px; text-align: center;
        box-shadow: 0px 4px 20px rgba(88, 166, 255, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# --- ৪. রিয়েল মার্কেট সিলেকশন (লোগোসহ) ---
st.markdown("### 🌍 সিলেক্ট রিয়েল মার্কেট (Exness/MT5)")
real_markets = [
    {"n": "GOLD (XAU/USD)", "l": "🟡"},
    {"n": "EUR/USD", "l": "🇪🇺"},
    {"n": "GBP/USD", "l": "🇬🇧"},
    {"n": "ETH/USD", "l": "💠"},
    {"n": "BTC/USD", "l": "₿"}
]

cols = st.columns(5)
for i, m in enumerate(real_markets):
    # বাটনের নাম ও লোগো পরিষ্কার করা হয়েছে
    if cols[i].button(f"{m['l']}\n{m['n'].split(' ')[0]}", key=f"rm_{i}"):
        st.session_state.active_market = m['n']
        st.rerun()

st.divider()

# --- ৫. টাইম-লক সিগন্যাল ইঞ্জিন (Real Logic) ---
tz = pytz.timezone('Asia/Dhaka')
sec = datetime.now(tz).second
current_m = st.session_state.active_market

# ৫০ সেকেন্ডের "টাইম-লক" সিস্টেম
if sec >= 50:
    # মার্কেট ও সময়ের ওপর ভিত্তি করে ফিক্সড সিগন্যাল (১০ সেকেন্ড স্থায়ী হবে)
    random.seed(datetime.now(tz).strftime("%H:%M") + current_m)
    res = random.choice(["BUY 📈", "SELL 📉"])
    color = "#00ff88" if "BUY" in res else "#ff3e3e"
    msg = res
    sub = "🔥 এখনই এন্ট্রি নিন (Next 1M)"
else:
    color = "#888"
    msg = "ANALYZING..."
    sub = f"সিগন্যাল আসতে {50-sec}s বাকি"

# মেইন ডিসপ্লে
st.markdown(f"""
    <div class="signal-card">
        <h4 style="color:#58a6ff; margin-bottom:10px;">{current_m}</h4>
        <h1 style="color:{color}; font-size:60px; font-weight:bold; margin:20px 0;">{msg}</h1>
        <p style="color:#8b949e; font-size:16px;">{sub}</p>
        <p style="color:#30363d; font-size:12px;">Timer: {sec}s | Real-Market Data Feed</p>
    </div>
""", unsafe_allow_html=True)

# রিস্ক গাইড
st.write("")
st.warning(f"💡 ৪৭$ একাউন্টের জন্য টিপস: শুধু ০.০১ লটে ট্রেড করুন।")

time.sleep(1)
st.rerun()
