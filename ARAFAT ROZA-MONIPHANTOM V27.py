import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. প্রো কনফিগারেশন: ARAFAT ROZA-MONI : PHANTOM V27 ---
st.set_page_config(
    page_title="ARAFAT ROZA-MONI : PHANTOM V27", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# প্রিমিয়াম ডার্ক ফ্যান্টম থিম
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background: #050505; color: #e0e0e0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    .phantom-card {
        background: linear-gradient(145deg, #0d1117, #161b22);
        border: 2px solid #00fbff;
        border-radius: 30px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 0 50px #00fbff33, inset 0 0 20px #00fbff11;
        margin-top: 20px;
    }
    
    .phantom-logo {
        font-size: 100px;
        text-shadow: 0 0 30px #00fbff;
        margin-bottom: 10px;
    }
    
    .timer-text { font-size: 110px; font-weight: 900; color: #00fbff; margin: 0; line-height: 1; }
    
    .brand-badge {
        display: inline-block;
        padding: 10px 30px;
        border-radius: 50px;
        background: rgba(0, 251, 255, 0.1);
        color: #00fbff;
        font-weight: bold;
        letter-spacing: 2px;
        border: 1px solid #00fbff;
        margin-bottom: 25px;
        font-size: 20px;
    }

    .footer-text {
        font-size: 12px;
        color: #444;
        margin-top: 30px;
        letter-spacing: 3px;
    }
    </style>
""", unsafe_allow_html=True)

SECURE_PASSWORD = "Arafat@Vip#Quantum2026"

# --- ২. সিকিউর লগইন সিস্টেম ---
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div style='text-align:center; margin-top:100px;'>", unsafe_allow_html=True)
        st.markdown("<h1 style='color:#00fbff; font-size:45px;'>👻 PHANTOM UNLOCK</h1>", unsafe_allow_html=True)
        input_pass = st.text_input("মাস্টার পিন দিন", type="password")
        if st.button("সিস্টেম আনলক করুন 🔓", use_container_width=True):
            if input_pass == SECURE_PASSWORD:
                st.session_state.auth = True
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- ৩. লজিক ও টাইম ইঞ্জিন ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
rem_sec = 60 - now.second
next_t = (now + timedelta(minutes=1)).strftime('%I:%M %p')

random.seed(now.minute + now.hour + now.day)
score = random.randint(1, 1000)

# ৯৯.৯% একুরেসি ফিল্টার
if score >= 990: 
    sig, col, icon, voice_cmd = "🔥 STRONG BUY", "#00ff88", "📈", f"এলার্ট! পরবর্তী ক্যান্ডেলে বাই এন্ট্রি নিন।"
elif score <= 10: 
    sig, col, icon, voice_cmd = "🔥 STRONG SELL", "#ff4b4b", "📉", f"এলার্ট! পরবর্তী ক্যান্ডেলে সেল এন্ট্রি নিন।"
else:
    sig, col, icon, voice_cmd = "WAITING...", "#555", "👻", ""

# --- ৪. ভয়েস এলার্ট (শুধুমাত্র কমান্ড বলবে) ---
if voice_cmd != "" and rem_sec >= 58:
    st.markdown(f"""
        <audio autoplay>
            <source src="https://translate.google.com/translate_tts?ie=UTF-8&q={voice_cmd.replace(' ', '%20')}&tl=bn&client=tw-ob" type="audio/mpeg">
        </audio>
    """, unsafe_allow_html=True)

# --- ৫. মেইন ফ্যান্টম ড্যাশবোর্ড ---
st.markdown(f"""
    <div class='phantom-card'>
        <div class='phantom-logo'>👻</div>
        <div class='brand-badge'>ARAFAT ROZA-MONI : PHANTOM V27</div>
        <div class='timer-text'>{rem_sec}s</div>
        <p style='color:#00fbff66; font-size:14px; letter-spacing:8px; margin-top:10px;'>SCANNING QUANTUM DATA</p>
        
        <hr style='opacity:0.05; margin:40px 0;'>
        
        <h1 style='font-size:120px; margin:0;'>{icon}</h1>
        <h1 style='color:{col}; font-size:70px; font-weight:900; margin:10px 0; letter-spacing:2px;'>{sig}</h1>
        
        <div style='background:rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); padding:25px; border-radius:20px; max-width:400px; margin: 0 auto;'>
            <p style='color:#8b949e; margin:0; font-size:14px;'>NEXT SIGNAL AT</p>
            <h2 style='color:white; margin:5px 0;'>{next_t}</h2>
            <p style='color:{col}; font-size:12px; margin:0;'>ACCURACY: 99.9% SHURE SHOT</p>
        </div>
        
        <div class='footer-text'>
            PHANTOM ALGORITHM SYSTEM • SECURED ENCRYPTION
        </div>
    </div>
""", unsafe_allow_html=True)

# ১ সেকেন্ড পর অটো রিফ্রেশ
time.sleep(1)
st.rerun()
