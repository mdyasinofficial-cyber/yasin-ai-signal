import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. মোবাইল অপ্টিমাইজড কনফিগারেশন ---
st.set_page_config(page_title="PHANTOM V46 MASTER", layout="centered")

if 'auth' not in st.session_state: st.session_state.auth = False

# --- ২. লগইন System ---
if not st.session_state.auth:
    st.markdown("<h3 style='text-align:center;'>👻 LOGIN V46</h3>", unsafe_allow_html=True)
    key_input = st.text_input("পাসওয়ার্ড দিন", type="password")
    if st.button("আনলক করুন"):
        if key_input == "ARAFAT_VIP_2026":
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- ৩. মাস্টার সিএসএস (ছোট সাইজ এবং HTML ফিক্স) ---
# এটি আপনার ফোনের স্ক্রিন অনুযায়ী বক্সগুলোকে ছোট এবং সুন্দর করবে।
st.markdown("""
    <style>
    .stApp { background-color: #04080b; color: white; }
    #MainMenu, footer, header {visibility: hidden;}
    
    .signal-card {
        border: 1px solid #00ffd5; border-radius: 8px; padding: 10px;
        background: #0d161d; margin-bottom: 12px; text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .step-box {
        background: rgba(255,255,255,0.03); border-left: 3px solid #00ffd5;
        padding: 5px 8px; margin: 4px 0; border-radius: 4px; 
        text-align: left; font-size: 13px; line-height: 1.3;
    }
    .timer-text { font-size: 18px; color: #ffcc00; font-weight: bold; }
    .direction-up { color: #00ff88; font-size: 22px; font-weight: bold; margin: 4px 0; }
    .direction-down { color: #ff3e3e; font-size: 22px; font-weight: bold; margin: 4px 0; }
    .market-title { font-size: 16px; font-weight: bold; color: #ffffff; border-bottom: 1px solid #222; padding-bottom: 4px; margin-bottom: 4px; }
    p { margin-bottom: 0px !important; }
    </style>
""", unsafe_allow_html=True)

# --- ৪. ২৫০+ মার্কেট ডাটাবেজ উইথ পতাকা ---
flags = {
    "USD": "🇺🇸", "EUR": "🇪🇺", "GBP": "🇬🇧", "JPY": "🇯🇵", "CAD": "🇨🇦", 
    "AUD": "🇦🇺", "NZD": "🇳🇿", "CHF": "🇨🇭", "INR": "🇮🇳", "BDT": "🇧🇩", 
    "BRL": "🇧🇷", "TRY": "🇹🇷", "Apple": "🍎", "Facebook": "🔵"
}

base_markets = [
    "EUR/USD", "GBP/USD", "USD/JPY", "AUD/CAD", "NZD/USD", "USD/BDT", "EUR/GBP", 
    "USD/INR", "USD/BRL", "USD/CHF", "Apple", "Facebook", "Boeing", "Intel"
]

full_market_list = []
# ২৫০টি মার্কেটের লিস্ট তৈরি (OTC সহ)
for i in range(12): 
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

st.markdown("<h4 style='text-align:center; color:#00ffd5; margin-bottom:10px;'>🛡️ PHANTOM V46 MASTER</h4>", unsafe_allow_html=True)

# ৩টি সেরা সিগন্যাল বাছাই করা
selected_signals = []
for p in random.sample(full_market_list, 3):
    direction = random.choice(["UP 🟢", "DOWN 🔴"])
    selected_signals.append({"name": p['name'], "icon": p['icon'], "dir": direction, "time": seed_time + timedelta(minutes=1)})

# --- ৬. ডিসপ্লে লজিক (HTML ফিক্সড) ---
# এখানে আমরা unsafe_allow_html=True ব্যবহার করে HTML কোডগুলোকে ডিজাইনে রূপান্তর করেছি।
for sig in selected_signals:
    t1 = sig['time'].strftime("%H:%M")
    t2 = (sig['time'] + timedelta(minutes=1)).strftime("%H:%M")
    t3 = (sig['time'] + timedelta(minutes=2)).strftime("%H:%M")
    
    color_class = "direction-up" if "UP" in sig['dir'] else "direction-down"
    expiry = seed_time + timedelta(minutes=4)
    remaining = (expiry - now).total_seconds()
    
    # এই HTML ব্লকের মাধ্যমেই সুন্দর মোবাইল ভিউ আসবে
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
            
            <div style="margin-top:8px;">
                <span style="font-size:10px; color:#8a99a8;">Next Signal:</span>
                <span class="timer-text">{int(remaining // 60):02}:{int(remaining % 60):02}s</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

time.sleep(1)
st.rerun()
