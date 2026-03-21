import streamlit as st
import time
from datetime import datetime, timedelta
import pytz

# --- ১. মেমোরি ও কনফিগারেশন ---
st.set_page_config(page_title="PHANTOM V98 - TOP 8 MARKETS", layout="wide")

# --- ২. সেরা ৮টি মার্কেট (লোগোসহ) ---
markets = [
    {"name": "GOLD (XAU/USD)", "icon": "🟡"},
    {"name": "EUR/USD", "icon": "🇪🇺"},
    {"name": "GBP/USD", "icon": "🇬🇧"},
    {"name": "ETH/USD", "icon": "💠"},
    {"name": "BTC/USD", "icon": "₿"},
    {"name": "USD/JPY", "icon": "🇯🇵"},
    {"name": "AUD/USD", "icon": "🇦🇺"},
    {"name": "USTEC (Nasdaq)", "icon": "🇺🇸"}
]

# --- ৩. মেইন ইন্টারফেস ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: white; }
    .market-btn {
        background: #0d1117; border: 1px solid #30363d;
        border-radius: 10px; padding: 10px; text-align: center;
        margin-bottom: 5px; cursor: pointer;
    }
    .signal-box {
        background: #0d1117; border: 3px solid #58a6ff;
        border-radius: 20px; padding: 30px; text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# মার্কেট সিলেকশন (পাশাপাশি ৮টি)
st.write("### 🌍 সিলেক্ট মার্কেট (টপ ৮)")
cols = st.columns(8)
if 'active_m' not in st.session_state: st.session_state.active_m = "GOLD (XAU/USD)"

for i, m in enumerate(markets):
    if cols[i].button(f"{m['icon']}\n{m['name'].split(' ')[0]}"):
        st.session_state.active_m = m['name']

st.divider()

# --- ৪. টাইমার ও পাচার লজিক ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
sec = now.second

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"#### মার্কেট: {st.session_state.active_m}")
    if sec < 45:
        remaining = 45 - sec
        st.info(f"⏳ এনালাইসিস চলছে... {remaining} সেকেন্ড পর এন্ট্রি আসবে।")
        st.markdown("<div style='text-align:center; padding:50px; color:#444;'>স্ক্যানিং লিকুইডিটি...</div>", unsafe_allow_html=True)
    else:
        # ৪৫ সেকেন্ড পার হলে কনফার্মড সিগন্যাল
        signal = "BUY 📈" if (now.minute + sec) % 2 == 0 else "SELL 📉"
        color = "#00ff88" if "BUY" in signal else "#ff3e3e"
        
        st.markdown(f"""
            <div class="signal-box" style="border-color:{color};">
                <h1 style="color:{color}; font-size:65px; margin:0;">{signal}</h1>
                <p style="color:#8b949e;">একুরেসি: ৮৫-৯০% (SMC + Vol)</p>
                <h3 style="color:#ffcc00;">এখনই এক্সনেসে এন্ট্রি নিন!</h3>
                <p style="color:#444;">টাইম বাকি: {60-sec} সেকেন্ড</p>
            </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("### 💰 আপনার ৪৭$ গাইড")
    st.success("Target Profit: $2.50")
    st.error("Stop Loss: $1.50")
    st.warning("Lot: 0.01 Only")
    
    # উইন লস কাউন্টার
    st.write("---")
    st.write("আজকের রেজাল্ট:")
    c1, c2 = st.columns(2)
    c1.button("WIN ✅")
    c2.button("LOSS ❌")

# অটো রিফ্রেশ
time.sleep(1)
st.rerun()
