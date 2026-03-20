import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. মেম্বারশিপ ও কনফিগারেশন (ফিক্সড) ---
# মোবাইল স্ক্রিনে ফিট করার জন্য layout="centered" রাখা হয়েছে
st.set_page_config(page_title="PHANTOM V46 FIXED", layout="centered")

if 'auth' not in st.session_state: st.session_state.auth = False

# --- ২. লগইন System ---
if not st.session_state.auth:
    st.markdown("<h3 style='text-align:center; color:#00ffd5;'>👻 PHANTOM V46 LOGIN</h3>", unsafe_allow_html=True)
    key_input = st.text_input("মাস্টার পাসওয়ার্ড দিন", type="password")
    if st.button("সিস্টেম আনলক"):
        if key_input == "ARAFAT_VIP_2026": # আপনার পাসওয়ার্ড
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("ভুল পাসওয়ার্ড!")
    st.stop()

# --- ৩. মোবাইল অপ্টিমাইজড সিএসএস (ডিজাইন ফিক্সড) ---
st.markdown("""
    <style>
    .stApp { background-color: #04080b; color: white; }
    /* কোড ব্লক লুকাতে এই অংশটি জরুরি */
    .stCodeBlock { display: none; }
    
    .signal-card {
        border: 1px solid #00ffd5; border-radius: 10px; padding: 12px;
        background: #0d161d; margin-bottom: 12px; text-align: center;
        box-shadow: 0 4px 10px rgba(0,255,213,0.1);
    }
    .step-box {
        background: rgba(255,255,255,0.03); border-left: 3px solid #00ffd5;
        padding: 6px 10px; margin: 5px 0; border-radius: 4px; 
        text-align: left; font-size: 14px; color: #e0e0e0;
    }
    .timer-text { font-size: 18px; color: #ffcc00; font-weight: bold; }
    .direction-up { color: #00ff88; font-size: 24px; font-weight: bold; margin: 5px 0; }
    .direction-down { color: #ff3e3e; font-size: 24px; font-weight: bold; margin: 5px 0; }
    .market-title { font-size: 18px; font-weight: bold; color: #ffffff; border-bottom: 1px solid #222; padding-bottom: 5px; }
    p { margin-bottom: 0px !important; }
    </style>
""", unsafe_allow_html=True)

# --- ৪. টাইম ইঞ্জিন ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)

# সিগন্যাল ৪ মিনিট স্থির থাকবে
seed_time = now.replace(minute=(now.minute // 4) * 4, second=0, microsecond=0)
random.seed(seed_time.strftime("%Y-%m-%d %H:%M"))

st.markdown("<h3 style='text-align:center; color:#00ffd5; margin-bottom:10px;'>🛡️ PHANTOM V46 MASTER</h3>", unsafe_allow_html=True)

# আপনার পছন্দের মার্কেট লিস্ট (লোগোসহ)
pairs = [
    {"n": "EUR/USD (OTC)", "i": "🇪🇺🇺🇸"},
    {"n": "GBP/USD (OTC)", "i": "🇬🇧🇺🇸"},
    {"n": "USD/JPY (OTC)", "i": "🇺🇸🇯🇵"},
    {"n": "USD/BDT (OTC)", "i": "🇺🇸🇧🇩"},
    {"n": "AUD/CAD (OTC)", "i": "🇦🇺🇨🇦"}
]

# ২৫০টি থেকে ৩টি সেরা সিগন্যাল বাছাই করা (সিমুলেশন)
selected_signals = []
for p in random.sample(pairs, 3):
    direction = random.choice(["UP 🟢", "DOWN 🔴"])
    selected_signals.append({"name": p['n'], "icon": p['i'], "dir": direction, "time": seed_time + timedelta(minutes=1)})

# --- ৫. ডিসপ্লে লজিক (HTML ফিক্সড) ---
for sig in selected_signals:
    # টাইম ক্যালকুলেশন
    t1 = sig['time'].strftime("%H:%M")
    t2 = (sig['time'] + timedelta(minutes=1)).strftime("%H:%M")
    t3 = (sig['time'] + timedelta(minutes=2)).strftime("%H:%M")
    
    color_class = "direction-up" if "UP" in sig['dir'] else "direction-down"
    expiry = seed_time + timedelta(minutes=4)
    remaining = (expiry - now).total_seconds()
    
    # !!! এখানেই ভুল হয়েছিল, unsafe_allow_html=True যোগ করা হয়েছে !!!
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

# অটো রিফ্রেশ
time.sleep(1)
st.rerun()
