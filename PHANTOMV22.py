import streamlit as st
import time
from datetime import datetime
import pytz
import random

# --- ১. মেমোরি ও সিকিউরিটি ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'selected_market' not in st.session_state: st.session_state.selected_market = "USD/BDT (OTC)"
if 'm_step' not in st.session_state: st.session_state.m_step = 1
if 'session_profit' not in st.session_state: st.session_state.session_profit = 0.0

# --- ২. লগইন ইন্টারফেস ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center; color:#00ffd5;'>🔐 PHANTOM V71</h2>", unsafe_allow_html=True)
    pw = st.text_input("পাসওয়ার্ড দিন:", type="password", key="login_pw")
    if st.button("আনলক করুন", key="unlock_btn"):
        if pw == "ARAFAT_V64":
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- ৩. মেইন ডিজাইন ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: white; }
    .ghost-box { 
        background: #0d1117; border: 2px solid #58a6ff; 
        border-radius: 15px; padding: 20px; text-align: center; 
    }
    .candle { 
        width: 40px; height: 100px; margin: 10px auto; 
        border: 2px dashed #555; border-radius: 5px; 
    }
    /* বাটন স্টাইল */
    .stButton>button {
        width: 100%;
        background-color: #21262d !important;
        color: white !important;
        border: 1px solid #30363d !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- ৪. মার্কেট সিলেকশন (লোগোসহ) ---
st.markdown("### 🎯 মার্কেট বেছে নিন:")
markets = [
    {"n": "USD/BDT (OTC)", "l": "🇺🇸🇧🇩"},
    {"n": "EUR/USD (OTC)", "l": "🇪🇺🇺🇸"},
    {"n": "GBP/USD (OTC)", "l": "🇬🇧🇺🇸"},
    {"n": "USD/JPY (OTC)", "l": "🇺🇸🇯🇵"},
    {"n": "AUD/CAD (OTC)", "l": "🇦🇺🇨🇦"}
]

cols = st.columns(5)
for i, m in enumerate(markets):
    # লোগো এবং নাম একসাথে বাটনে দেওয়া হয়েছে
    btn_text = f"{m['l']}\n{m['n'].split('/')[0]}"
    if cols[i].button(btn_text, key=f"m_btn_{i}"):
        st.session_state.selected_market = m['n']
        st.rerun()

st.divider()

# --- ৫. টাইম ও সিগন্যাল ইঞ্জিন ---
tz = pytz.timezone('Asia/Dhaka')
sec = datetime.now(tz).second
current_m = st.session_state.selected_market

if sec >= 50:
    random.seed(datetime.now(tz).strftime("%H:%M") + current_m)
    res = random.choice(["BUY 📈", "SELL 📉"])
    bg = "rgba(0, 255, 136, 0.3)" if "BUY" in res else "rgba(255, 62, 62, 0.3)"
    txt_color = "#00ff88" if "BUY" in res else "#ff3e3e"
    msg = res
else:
    bg = "#1c2128"
    txt_color = "#888"
    msg = "ANALYZING..."

# ডিজাইন প্রদর্শন
st.markdown(f"""
    <div class="ghost-box">
        <p style="color:#58a6ff; font-size:16px; font-weight:bold;">{current_m}</p>
        <p style="color:#888; font-size:12px;">টাইমার: {sec}s</p>
        <div class="candle" style="background-color: {bg};"></div>
        <h2 style="color:{txt_color}; font-weight:bold;">{msg}</h2>
        <p style="font-size:11px; color:#555;">ক্যান্ডেল শেষ হওয়ার ১০ সেকেন্ড আগে সিগন্যাল আসবে</p>
    </div>
""", unsafe_allow_html=True)

# --- ৬. মার্টিনগেল প্যানেল ---
st.write("")
amounts = {1: 1, 2: 3, 3: 9, 4: 20, 5: 50}
curr = amounts[st.session_state.m_step]

st.info(f"💰 বর্তমান ট্রেড: ${curr} | সেশন প্রফিট: ${st.session_state.session_profit:.2f}")

c1, c2 = st.columns(2)
if c1.button("✅ WIN", key="win_btn"):
    st.session_state.session_profit += (curr * 0.82)
    st.session_state.m_step = 1
    st.rerun()
if c2.button("❌ LOSS", key="loss_btn"):
    st.session_state.session_profit -= curr
    st.session_state.m_step = min(st.session_state.m_step + 1, 5)
    st.rerun()

time.sleep(1)
st.rerun()
    
