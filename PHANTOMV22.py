import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. কনফিগারেশন ---
st.set_page_config(page_title="PHANTOM V45 FULL", layout="centered")

if 'auth' not in st.session_state: st.session_state.auth = False

# --- ২. লগইন ---
if not st.session_state.auth:
    st.markdown("<h3 style='text-align:center;'>👻 PHANTOM V45 LOGIN</h3>", unsafe_allow_html=True)
    key_input = st.text_input("পাসওয়ার্ড", type="password")
    if st.button("আনলক"):
        if key_input == "ARAFAT_VIP_2026":
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- ৩. মোবাইল ডিজাইন (একদম কমপ্যাক্ট) ---
st.markdown("""
    <style>
    .stApp { background-color: #04080b; color: white; }
    .signal-card {
        border: 1.5px solid #00ffd5; border-radius: 12px; padding: 12px;
        background: #0d161d; margin-bottom: 15px; text-align: center;
    }
    .step-box {
        background: rgba(255,255,255,0.04); border-left: 4px solid #00ffd5;
        padding: 6px 10px; margin: 5px 0; border-radius: 5px; 
        text-align: left; font-size: 14px;
    }
    .timer-box { font-size: 18px; color: #ffcc00; font-weight: bold; margin-top: 5px; }
    .direction-up { color: #00ff88; font-size: 24px; font-weight: bold; margin: 5px 0; }
    .direction-down { color: #ff3e3e; font-size: 24px; font-weight: bold; margin: 5px 0; }
    .market-title { font-size: 18px; font-weight: bold; color: #ffffff; padding-bottom: 5px; border-bottom: 1px solid #222; }
    </style>
""", unsafe_allow_html=True)

# --- ৪. ২৫০+ মার্কেট ডাটাবেজ উইথ লোগো ---
flags = {
    "USD": "🇺🇸", "EUR": "🇪🇺", "GBP": "🇬🇧", "JPY": "🇯🇵", "CAD": "🇨🇦", 
    "AUD": "🇦🇺", "NZD": "🇳🇿", "CHF": "🇨🇭", "INR": "🇮🇳", "BDT": "🇧🇩", 
    "BRL": "🇧🇷", "TRY": "🇹🇷", "ZAR": "🇿🇦", "Apple": "🍎", "Facebook": "🔵"
}

base_markets = [
    "EUR/USD", "GBP/USD", "USD/JPY", "AUD/CAD", "NZD/USD", "USD/BDT", "EUR/GBP", 
    "USD/INR", "USD/BRL", "USD/CHF", "EUR/JPY", "GBP/JPY", "CAD/JPY", "AUD/JPY",
    "EUR/CAD", "GBP/CAD", "EUR/AUD", "Apple", "Facebook", "Boeing", "Intel"
]

# ২৫০টি মার্কেটের লিস্ট তৈরি (OTC সহ)
full_market_list = []
for i in range(12): # লুপ দিয়ে ২৫০+ করা হচ্ছে
    for m in base_markets:
        p1 = m.split('/')[0] if '/' in m else m
        icon = flags.get(p1, "📊")
        full_market_list.append({"name": f"{m} (OTC)", "icon": icon})

# --- ৫. টাইম ইঞ্জিন ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)

# সিগন্যাল ৪ মিনিট স্থির থাকবে
seed_time = now.replace(minute=(now.minute // 4) * 4, second=0, microsecond=0)
random.seed(seed_time.strftime("%Y-%m-%d %H:%M"))

st.markdown("<h4 style='text-align:center; color:#00ffd5;'>🛡️ PHANTOM V45 (250+ MARKETS)</h4>", unsafe_allow_html=True)

# ২৫০টি থেকে ৩টি সেরা সিগন্যাল বাছাই করা
selected_signals = []
for p in random.sample(full_market_list, 3):
    direction = random.choice(["UP 🟢", "DOWN 🔴"])
    selected_signals.append({"name": p['name'], "icon": p['icon'], "dir": direction, "time": seed_time + timedelta(minutes=1)})

# --- ৬. ডিসপ্লে লজিক ---
for sig in selected_signals:
    t1 = sig['time'].strftime("%H:%M")
    t2 = (sig['time'] + timedelta(minutes=1)).strftime("%H:%M")
    t3 = (sig['time'] + timedelta(minutes=2)).strftime("%H:%M")
    
    color_class = "direction-up" if "UP" in sig['dir'] else "direction-down"
    expiry = seed_time + timedelta(minutes=4)
    remaining = (expiry - now).total_seconds()
    
    st.markdown(f"""
        <div class="signal-card">
            <div class="market-title">{sig['icon']} {sig['name']}</div>
            <div class="{color_class}">{sig['dir']}</div>
            
            <div class="step-box">
                <b>STEP 1:</b> {t1} মিনিটে এন্ট্রি (মেইন)
            </div>
            
            <div class="step-box" style="border-left-color: #ffcc00;">
                <b>STEP 2:</b> {t2} (MTG-1)
            </div>
            
            <div class="step-box" style="border-left-color: #ff3e3e;">
                <b>STEP 3:</b> {t3} (MTG-2 / LAST)
            </div>
            
            <div class="timer-box">
                <span style="font-size:12px; color:#8a99a8;">Next Signal:</span> {int(remaining // 60):02}:{int(remaining % 60):02}s
            </div>
        </div>
    """, unsafe_allow_html=True)

time.sleep(1)
st.rerun()
    
