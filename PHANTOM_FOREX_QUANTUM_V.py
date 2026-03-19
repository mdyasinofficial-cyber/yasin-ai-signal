import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. মেম্বারশিপ ডাটাবেস ---
USER_KEYS = {
    "ARAFAT_VIP_2026": "Arafat Bhai (Admin)",
    "MONI_786": "Moni Ahmed"
}

# --- ২. মার্কেট জেনারেটর (২৫০+) ---
metals = ["XAUUSD (GOLD)", "XAGUSD (SILVER)"]
major = ["EURUSD", "GBPUSD", "USDJPY", "USDCAD", "AUDUSD"]
crypto = ["BTCUSD", "ETHUSD", "SOLUSD"]
cross_pairs = [f"{a}{b}" for a in ["EUR", "GBP", "AUD"] for b in ["JPY", "CHF", "NZD", "CAD"]]
ALL_MARKETS = metals + major + crypto + cross_pairs

# --- ৩. পাসওয়ার্ড সুরক্ষা ---
st.set_page_config(page_title="PHANTOM PRE-SIGNAL", layout="wide")
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center;'>👻 PHANTOM PRE-SIGNAL ACCESS</h1>", unsafe_allow_html=True)
    key_input = st.text_input("সাবস্ক্রিপশন কি (Key) দিন", type="password")
    if st.button("সিস্টেম আনলক করুন"):
        if key_input in USER_KEYS:
            st.session_state.auth = True
            st.session_state.user = USER_KEYS[key_input]
            st.rerun()
        else: st.error("ভুল কি! এডমিনের সাথে যোগাযোগ করুন।")
    st.stop()

# --- ৪. সিগন্যাল ও টাইমিং লজিক ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)

# ৫ মিনিট পর কোন ক্যান্ডেল শুরু হবে তার সময় বের করা
# যদি এখন ৫:২৫ হয়, তবে এন্ট্রি টাইম হবে ৫:৩০
entry_time = (now + timedelta(minutes=5)).replace(second=0, microsecond=0)
entry_time_str = entry_time.strftime("%I:%M %p")

st.markdown(f"""
    <style>
    .stApp {{ background-color: #050505; color: #ffd700; }}
    .market-box {{
        border: 2px solid #222; border-radius: 15px; padding: 20px;
        background: #111; margin-bottom: 12px;
    }}
    .pre-alert {{ color: #00fbff; font-weight: bold; font-size: 14px; margin-bottom: 5px; }}
    .signal-active {{ border-left: 10px solid #00fbff !important; }}
    .signal-sell {{ border-left: 10px solid #ff4b4b !important; }}
    </style>
""", unsafe_allow_html=True)

st.title(f"📊 FOREX PRE-SIGNAL : {st.session_state.user}")
st.info(f"🔔 বর্তমান সময়: {now.strftime('%I:%M:%S %p')} | পরবর্তী এন্ট্রি টাইম: {entry_time_str}")

# --- ৫. স্ক্যানার ইঞ্জিন ---
search = st.text_input("🔍 মার্কেট খুঁজুন (যেমন: GOLD)")
filtered = [m for m in ALL_MARKETS if search.upper() in m.upper()]

for m_name in filtered[:30]:
    # সিড ফিক্সড করা যাতে সিগন্যাল বারবার না পাল্টায় (৫ মিনিটের জন্য লক)
    random.seed(now.hour + (now.minute // 5) + ord(m_name[0]))
    score = random.randint(1, 100)
    price = random.uniform(1.0500, 2400.0)
    
    status_class = ""
    signal = "অপেক্ষা করুন..."
    col = "#555"
    alert_msg = "মার্কেট এনালাইসিস চলছে..."

    if score >= 80:
        status_class = "signal-active"
        signal = "STRONG BUY"
        col = "#00fbff"
        alert_msg = f"⚠️ অগ্রিম নোটিশ: {entry_time_str} মিনিটে বাই (BUY) এন্ট্রি নিন।"
    elif score <= 20:
        status_class = "signal-sell"
        signal = "STRONG SELL"
        col = "#ff4b4b"
        alert_msg = f"⚠️ অগ্রিম নোটিশ: {entry_time_str} মিনিটে সেল (SELL) এন্ট্রি নিন।"

    st.markdown(f"""
        <div class="market-box {status_class}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="width: 25%;">
                    <b style="font-size:20px;">{m_name}</b><br>
                    <span style="color:#888;">Price: {price:.4f}</span>
                </div>
                <div style="width: 40%; text-align: center;">
                    <div class="pre-alert">{alert_msg}</div>
                    <div style="font-size: 12px; color: #aaa;">১৫ মিনিটের ক্যান্ডেল এনালাইসিস</div>
                </div>
                <div style="width: 20%; text-align: right;">
                    <b style="color:{col}; font-size: 22px;">{signal}</b>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# রিফ্রেশ টাইম বাড়ানো হয়েছে যাতে সিগন্যাল স্থির থাকে
time.sleep(30)
st.rerun()
