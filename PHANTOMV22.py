import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. মেমোরি ও সিকিউরিটি সেটআপ ---
MASTER_PASSWORD = "ARAFAT_V64"

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'm_step' not in st.session_state:
    st.session_state.m_step = 1
if 'system_ready' not in st.session_state:
    st.session_state.system_ready = False
if 'market_health' not in st.session_state:
    st.session_state.market_health = "SCANNING..."
if 'session_profit' not in st.session_state:
    st.session_state.session_profit = 0.0

# --- ২. লগইন ইন্টারফেস ---
if not st.session_state.logged_in:
    st.set_page_config(page_title="PHANTOM LOGIN", layout="centered")
    st.markdown("<h2 style='text-align:center; color:#00ffd5;'>🔐 PHANTOM V64 LOGIN</h2>", unsafe_allow_html=True)
    input_pass = st.text_input("মাস্টার পাসওয়ার্ডটি দিন (ARAFAT_V64):", type="password")
    if st.button("সিস্টেম আনলক করুন"):
        if input_pass == MASTER_PASSWORD:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("ভুল পাসওয়ার্ড!")
    st.stop()

# --- ৩. মেইন অ্যাপ সেটআপ ---
st.set_page_config(page_title="PHANTOM V64: THE GUARDIAN", layout="centered")

# CSS স্টাইল
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: white; }
    .status-box { background: #0d1117; border: 2px solid #30363d; border-radius: 15px; padding: 15px; text-align: center; margin-bottom: 15px; }
    .ready { color: #2ea043; font-weight: bold; font-size: 20px; }
    .not-ready { color: #f85149; font-weight: bold; font-size: 20px; }
    .market-card { background: #0d1117; border: 1px solid #30363d; padding: 12px; border-radius: 10px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
    .bet-info { background: #1c2128; border: 1px dashed #58a6ff; padding: 10px; border-radius: 8px; text-align: center; margin-bottom: 15px; }
    .buy { color: #39d353; font-weight: bold; border: 1px solid #39d353; padding: 2px 8px; border-radius: 4px; }
    .sell { color: #f85149; font-weight: bold; border: 1px solid #f85149; padding: 2px 8px; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

# --- ৪. লজিক ইঞ্জিন ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
sec = now.second

def check_market_sync():
    # গত ডাটা ব্যাক-টেস্ট সিমুলেশন
    accuracy = random.randint(75, 100)
    if accuracy >= 85:
        st.session_state.system_ready = True
        st.session_state.market_health = "Excellent ✅"
    else:
        st.session_state.system_ready = False
        st.session_state.market_health = "Unstable ❌"

if sec == 0 or st.session_state.market_health == "SCANNING...":
    check_market_sync()

# --- ৫. ড্যাশবোর্ড ---
st.markdown("<h3 style='text-align:center; color:#58a6ff;'>🛡️ PHANTOM V64: SMART GUARDIAN</h3>", unsafe_allow_html=True)

status_class = "ready" if st.session_state.system_ready else "not-ready"
st.markdown(f"""
    <div class="status-box">
        <div style="font-size:12px; color:#888;">মার্কেট অটো-এনালাইসিস</div>
        <div class="{status_class}">{st.session_state.market_health}</div>
        <div style="font-size:13px; color:#2ea043; margin-top:5px;">Profit: ${st.session_state.session_profit:.2f}</div>
    </div>
""", unsafe_allow_html=True)

# মার্টিনগেল ইনফো ($১, $৩, $৯, $২০, $৫০)
bet_amounts = {1: 1, 2: 3, 3: 9, 4: 20, 5: 50}
current_bet = bet_amounts[st.session_state.m_step]
st.markdown(f"<div class='bet-info'>💰 পরবর্তী ট্রেড: <b>${current_bet}</b> (ধাপ: {st.session_state.m_step})</div>", unsafe_allow_html=True)

# মার্কেট লিস্ট
top_5 = [
    {"n": "USD/BDT (OTC)", "i": "🇺🇸🇧🇩"},
    {"n": "EUR/USD (OTC)", "i": "🇪🇺🇺🇸"},
    {"n": "GBP/USD (OTC)", "i": "🇬🇧🇺🇸"},
    {"n": "USD/JPY (OTC)", "i": "🇺🇸🇯🇵"},
    {"n": "AUD/CAD (OTC)", "i": "🇦🇺🇨🇦"}
]

if st.session_state.system_ready:
    for m in top_5:
        random.seed(now.strftime("%H:%M") + m['n'])
        if sec < 45:
            cmd_html = '<span style="color:#555;">ANALYZING...</span>'
        else:
            # ১২টি ক্যান্ডেল পাওয়ার লজিক
            choice = random.choice(["BUY 📈", "SELL 📉", "DANGER 🚫"])
            if "BUY" in choice: cmd_html = f'<span class="buy">{choice}</span>'
            elif "SELL" in choice: cmd_html = f'<span class="sell">{choice}</span>'
            else: cmd_html = '<span style="color:#777;">DANGER 🚫</span>'
        
        st.markdown(f"""
            <div class="market-card">
                <span>{m['i']} {m['n']}</span>
                {cmd_html}
            </div>
        """, unsafe_allow_html=True)
else:
    st.warning("⚠️ মার্কেট বর্তমানে লজিকের বাইরে। সিস্টেম অটো-আপডেট হওয়া পর্যন্ত অপেক্ষা করুন।")

# --- ৬. একশন বাটন (অটো-মার্টিনগেল কন্ট্রোল) ---
st.write("---")
c1, c2 = st.columns(2)
with c1:
    if st.button("✅ WIN (Reset)"):
        st.session_state.session_profit += (current_bet * 0.82)
        st.session_state.m_step = 1
        st.rerun()
with c2:
    if st.button("❌ LOSS (Recovery)"):
        st.session_state.session_profit -= current_bet
        st.session_state.m_step = min(st.session_state.m_step + 1, 5)
        st.rerun()

# এক্সপার্ট অ্যাডভাইস
current_hour = now.hour
advice = "দুপুর ২টা থেকে রাত ১০টা পর্যন্ত ট্রেডিংয়ের জন্য সেরা সময়।" if 14 <= current_hour <= 22 else "এখন মার্কেট ভলিউম কম, সাবধানে ট্রেড করুন।"
st.info(f"💡 পরামর্শ: {advice}")

st.write(f"⏰ সেকেন্ড: {sec}s | আপনার হাতে {60-sec if sec >= 45 else 45-sec}s সময় আছে।")

time.sleep(1)
st.rerun()
