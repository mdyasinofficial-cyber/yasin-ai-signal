import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. কনফিগারেশন ---
st.set_page_config(
    page_title="ARAFAT ROZA-MONI : PHANTOM V31", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- ২. লজিক ও টাইম ইঞ্জিন ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
rem_sec = 60 - now.second
next_t = (now + timedelta(minutes=1)).strftime('%I:%M %p')

# মার্কেট লিস্ট
market_list = [
    {"name": "EUR/USD", "flag": "🇪🇺🇺🇸"},
    {"name": "GOLD (XAU)", "flag": "🟡"},
    {"name": "USD/BDT (OTC)", "flag": "🇧🇩🇺🇸"},
    {"name": "GBP/JPY", "flag": "🇬🇧🇯🇵"},
    {"name": "USD/INR (OTC)", "flag": "🇮🇳🇺🇸"}
]

random.seed(now.minute + now.hour)
active_market = random.choice(market_list)
score = random.randint(1, 1000)

# কালার ও সিগন্যাল লজিক
if score >= 990: 
    sig_en, sig_bn, bg_col, text_col, icon = "STRONG BUY", "এখনই বাই (BUY) নিন", "#002b5c", "#00fbff", "📈"
    voice_cmd = f"এলার্ট! {active_market['name']} মার্কেটে বাই এন্ট্রি নিন।"
elif score <= 10: 
    sig_en, sig_bn, bg_col, text_col, icon = "STRONG SELL", "এখনই সেল (SELL) নিন", "#5c0000", "#ff4b4b", "📉"
    voice_cmd = f"এলার্ট! {active_market['name']} মার্কেটে সেল এন্ট্রি নিন।"
else:
    sig_en, sig_bn, bg_col, text_col, icon, voice_cmd = "SCANNING...", "সিগন্যাল খুঁজছি...", "#000000", "#ffd700", "👻", ""

# ডাইনামিক স্টাইল
st.markdown(f"""
    <style>
    #MainMenu, footer, header, .stDeployButton, #stDecoration, [data-testid="sidebarNavView"] {{visibility: hidden; display:none;}}
    .stApp {{ background-color: {bg_col}; transition: background-color 0.8s ease; }}
    .phantom-card {{
        background: rgba(0,0,0,0.6);
        border: 2px solid {text_col};
        border-radius: 25px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 40px {text_col}33;
        max-width: 350px;
        margin: auto;
        color: {text_col};
    }}
    .timer {{ font-size: 100px; font-weight: 900; margin: 0; line-height: 1; }}
    .signal-bn {{ 
        font-size: 20px; font-weight: bold; color: #fff; background: {text_col}66; 
        padding: 5px 15px; border-radius: 50px; display: inline-block; margin-top: 5px; 
    }}
    </style>
""", unsafe_allow_html=True)

# লগইন চেক (পাসওয়ার্ড ছাড়া সরাসরি দেখার জন্য চাইলে সরাতে পারেন)
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    if st.text_input("মাস্টার পিন", type="password") == "Arafat@Vip#Quantum2026":
        st.session_state.auth = True
        st.rerun()
    st.stop()

# ভয়েস এলার্ট
if voice_cmd != "" and rem_sec >= 58:
    st.markdown(f"""<audio autoplay><source src="https://translate.google.com/translate_tts?ie=UTF-8&q={voice_cmd.replace(' ', '%20')}&tl=bn&client=tw-ob" type="audio/mpeg"></audio>""", unsafe_allow_html=True)

# মেইন ডিসপ্লে
st.markdown(f"""
    <div class='phantom-card'>
        <div style='font-size: 10px; letter-spacing: 2px; opacity: 0.6;'>ARAFAT ROZA-MONI : PHANTOM V31</div>
        <div style='padding: 10px; font-size: 22px; font-weight: bold; border-bottom: 1px solid {text_col}33;'>
            {active_market['flag']} {active_market['name']}
        </div>
        <div class='timer'>{rem_sec}s</div>
        <div style='margin-top: 15px;'>
            <h1 style='font-size: 60px; margin: 0; color: {text_col};'>{icon}</h1>
            <div style='font-size: 30px; font-weight: 900;'>{sig_en}</div>
            <div class='signal-bn'>{sig_bn}</div>
        </div>
        <div style='margin-top: 20px; font-size: 12px; opacity: 0.7;'>
            NEXT: {next_t} | 99.9% SHOT
        </div>
    </div>
""", unsafe_allow_html=True)

time.sleep(1)
st.rerun()
    
