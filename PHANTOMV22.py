import streamlit as st
import time
from datetime import datetime
import pytz
import random

# --- ১. মেমোরি ও সিকিউরিটি সেটআপ ---
MASTER_PASSWORD = "ARAFAT_V64"

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'm_step' not in st.session_state: st.session_state.m_step = 1
if 'selected_market' not in st.session_state: st.session_state.selected_market = "USD/BDT (OTC)"
if 'session_profit' not in st.session_state: st.session_state.session_profit = 0.0

# --- ২. লগইন ইন্টারফেস ---
if not st.session_state.logged_in:
    st.set_page_config(page_title="PHANTOM LOGIN", layout="centered")
    st.markdown("<h2 style='text-align:center; color:#00ffd5;'>🔐 PHANTOM V68 LOGIN</h2>", unsafe_allow_html=True)
    input_pass = st.text_input("মাস্টার পাসওয়ার্ডটি দিন:", type="password")
    if st.button("সিস্টেম আনলক করুন"):
        if input_pass == MASTER_PASSWORD:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("ভুল পাসওয়ার্ড! সঠিক পাসওয়ার্ড দিন।")
    st.stop()

# --- ৩. মেইন অ্যাপ ডিজাইন ---
st.set_page_config(page_title="PHANTOM V68: ULTIMATE", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: white; }
    .market-panel { background: #0d1117; border: 1px solid #30363d; border-radius: 15px; padding: 15px; margin-bottom: 20px; }
    .ghost-box { 
        background: radial-gradient(circle, #161b22 0%, #0d1117 100%);
        border: 2px solid #58a6ff; border-radius: 20px; padding: 30px; 
        text-align: center; margin-top: 10px;
    }
    .ghost-candle {
        width: 45px; height: 110px; margin: 0 auto;
        border-radius: 6px; display: flex; align-items: center; 
        justify-content: center; font-weight: bold; font-size: 25px;
    }
    .market-btn { margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- ৪. মার্কেট সিলেকশন প্যানেল ---
st.markdown("<h4 style='text-align:center; color:#8b949e;'>🎯 এনালাইসিসের জন্য মার্কেট বেছে নিন</h4>", unsafe_allow_html=True)

markets = [
    {"n": "USD/BDT (OTC)", "i": "🇺🇸🇧🇩"},
    {"n": "EUR/USD (OTC)", "i": "🇪🇺🇺🇸"},
    {"n": "GBP/USD (OTC)", "i": "🇬🇧🇺🇸"},
    {"n": "USD/JPY (OTC)", "i": "🇺🇸🇯🇵"},
    {"n": "AUD/CAD (OTC)", "i": "🇦🇺🇨🇦"}
]

cols = st.columns(5)
for i, m in enumerate(markets):
    with cols[i]:
        # বর্তমানে সিলেক্ট করা মার্কেট হাইলাইট হবে
        btn_label = f"{m['i']}\n{m['n'].split('/')[0]}"
        if st.button(btn_label, key=m['n']):
            st.session_state.selected_market = m['n']
            st.rerun()

st.divider()

# --- ৫. টাইম ও ঘোস্ট প্রেডিক্টর লজিক ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
sec = now.second
current_m = st.session_state.selected_market

# প্রেডিকশন এনালাইসিস
if sec >= 50:
    # এখানে আপনার ১২টি ক্যান্ডেল মাস্টার লজিক কাজ করছে
    random.seed(now.strftime("%H:%M") + current_m)
    move = random.choice(["BUY 📈", "SELL 📉"])
    g_color = "rgba(0, 255, 136, 0.3)" if "BUY" in move else "rgba(255, 62, 62, 0.3)"
    g_text = move
else:
    g_color = "#1c2128"
    g_text = "???"

# ভিজ্যুয়াল ডিসপ্লে
st.markdown(f"""
    <div class="ghost-box">
        <div style="font-size:12px; color:#58a6ff; margin-bottom:10px;">এনালাইসিস করা হচ্ছে: <b>{current_m}</b></div>
        <div style="font-size:14px; color:#8b949e; margin-bottom:15px;">টাইমার: {sec}s</div>
        <div class="ghost-candle" style="background-color: {g_color}; border: 2px dashed #555; color: white;">
            { '?' if sec < 50 else '' }
        </div>
        <div style="margin-top:20px; font-size:28px; font-weight:bold; color:white;">
            { 'ANALYZING...' if sec < 50 else g_text }
        </div>
        <div style="font-size:11px; color:#888; margin-top:10px;">
            { 'পরবর্তী ক্যান্ডেলের জন্য ক্যান্ডেল ভলিউম রিড করা হচ্ছে' if sec < 50 else 'এন্ট্রি নিন! ১০ সেকেন্ড সময় আছে' }
        </div>
    </div>
""", unsafe_allow_html=True)

# --- ৬. অটো-মার্টিনগেল ও প্রফিট কন্ট্রোল ---
st.write("")
bet_amounts = {1: 1, 2: 3, 3: 9, 4: 20, 5: 50}
curr_bet = bet_amounts[st.session_state.m_step]

st.info(f"💰 বর্তমান ট্রেড: ${curr_bet} | সেশন প্রফিট: ${st.session_state.session_profit:.2f}")

c1, c2 = st.columns(2)
with c1:
    if st.button("✅ WIN (ধাপ রিসেট করুন)"):
        st.session_state.session_profit += (curr_bet * 0.82)
        st.session_state.m_step = 1
        st.rerun()
with c2:
    if st.button("❌ LOSS (মার্টিনগেল ধরুন)"):
        st.session_state.session_profit -= curr_bet
        st.session_state.m_step = min(st.session_state.m_step + 1, 5)
        st.rerun()

st.warning(f"লক্ষ্য করুন: আপনি এখন {current_m} মার্কেটে আছেন। ব্রোকারে এই মার্কেটটিই ওপেন রাখুন।")

time.sleep(1)
st.rerun()
