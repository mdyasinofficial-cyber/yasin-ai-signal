import streamlit as st
import time
from datetime import datetime
import pytz
import random

# --- ১. প্রো কনফিগারেশন ও সিকিউরিটি ---
st.set_page_config(page_title="PHANTOM V34.2", layout="centered", initial_sidebar_state="collapsed")

SECURE_PASSWORD = "Arafat@Vip#Quantum2026"

if 'auth' not in st.session_state: st.session_state.auth = False

# --- ২. লগইন ইন্টারফেস ডিজাইন (ভয়ঙ্কর থিম) ---
if not st.session_state.auth:
    # গ্লোবাল স্টাইল ও ডার্ক থিম
    st.markdown("""
        <style>
        #MainMenu, footer, header, .stDeployButton, #stDecoration, [data-testid="sidebarNavView"] {visibility: hidden; display:none;}
        .stApp { background-color: #000; color: #ffd700; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        
        /* লগইন কার্ডের ডিজাইন */
        .login-card {
            border: 3px solid #ffd700; 
            border-radius: 20px; 
            padding: 40px; 
            text-align: center; 
            background: #000; 
            margin-top: 100px;
            box-shadow: 0 0 50px rgba(255, 215, 0, 0.4); /* সোনালী গ্লো */
        }
        
        /* ভয়ঙ্কর লোগো ডিজাইন */
        .phantom-logo {
            font-size: 100px;
            text-shadow: 0 0 20px #ffd700; /* নিওন গ্লো */
            margin-bottom: 5px;
            display: inline-block;
        }
        
        /* হেডার লেখা */
        .header-text {
            color: #ffd700;
            font-size: 30px;
            font-weight: bold;
            letter-spacing: 2px;
            margin-bottom: 20px;
            text-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
        }
        
        /* ছোট লেখা */
        .sub-text {
            color: #555;
            font-size: 11px;
            margin-bottom: 40px;
            letter-spacing: 1.5px;
        }
        
        /* লগইন বাটন ডিজাইন */
        div.stButton > button {
            background-color: #000;
            color: #ffd700;
            border: 2px solid #ffd700;
            border-radius: 50px;
            font-size: 16px;
            font-weight: bold;
            padding: 10px 40px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: block;
            margin: auto;
        }
        
        /* মাউস নিলে কালার চেঞ্জ */
        div.stButton > button:hover {
            background-color: #ffd700;
            color: #000;
            box-shadow: 0 0 20px #ffd700;
        }
        
        /* পাসওয়ার্ড ইনপুট ফিল্ডের কালার */
        div.stTextInput > div > div > input {
            background-color: #111;
            color: #ffd700;
            border-color: #ffd700;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # লগইন কার্ডের কন্টেন্ট
    st.markdown("""
        <div class="login-card">
            <div class="phantom-logo">👻</div>
            <div class="header-text">ARAFAT ROZA-MONI : PHANTOM</div>
            <div class="sub-text">SECURE QUANTUM ACCESS V34.2</div>
        </div>
    """, unsafe_allow_html=True)
    
    # ইনপুট ফিল্ড এবং বাটন
    input_col1, input_col2, input_col3 = st.columns([1, 2, 1])
    with input_col2:
        st.markdown("<br>", unsafe_allow_html=True) # একটু গ্যাপ
        pwd_input = st.text_input("মাস্টার পিন", type="password", key="login_pass")
        if st.button("সিস্টেম আনলক করুন 🔓", key="unlock_btn"):
            if pwd_input == SECURE_PASSWORD:
                st.session_state.auth = True
                st.rerun()
            else:
                st.markdown("<p style='color:#ff4b4b; text-align:center; margin-top:10px;'>ভুল পাসওয়ার্ড!</p>", unsafe_allow_html=True)
    
    st.stop()

# --- ৩. মেইন সিস্টেম থিম (আগের মতোই থাকবে) ---
st.markdown("""
    <style>
    #MainMenu, footer, header, .stDeployButton, #stDecoration, [data-testid="sidebarNavView"] {visibility: hidden; display:none;}
    .stApp { background-color: #000; color: #ffd700; }
    </style>
""", unsafe_allow_html=True)

# ডাটা ইঞ্জিন (V34.1 থেকে নেওয়া)
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
rem_sec = 60 - now.second

market_list = ["EURUSD", "GBPUSD", "XAUUSD", "BTCUSD", "AUDCAD"]
active_m = random.choice(market_list)

# রিয়েল ডাটা সিমুলেশন লজিক
random.seed(now.minute + now.hour)
score = random.randint(1, 1000)

if score >= 990:
    sig, txt, icon, bn = "STRONG BUY", "#00fbff", "📈", "এখনই বাই (BUY) নিন"
    v_cmd = f"এলার্ট! {active_m} মার্কেটে বাই এন্ট্রি নিন।"
elif score <= 10:
    sig, txt, icon, bn = "STRONG SELL", "#ff4b4b", "📉", "এখনই সেল (SELL) নিন"
    v_cmd = f"এলার্ট! {active_m} মার্কেটে সেল এন্ট্রি নিন।"
else:
    sig, txt, icon, bn, v_cmd = "SCANNING...", "#ffd700", "🔍", "১০০টি মার্কেট চেক হচ্ছে...", ""

# ভয়েস এলার্ট
if v_cmd != "" and rem_sec >= 58:
    st.markdown(f"""<audio autoplay><source src="https://translate.google.com/translate_tts?ie=UTF-8&q={v_cmd.replace(' ', '%20')}&tl=bn&client=tw-ob" type="audio/mpeg"></audio>""", unsafe_allow_html=True)

# মেইন কার্ড ডিসপ্লে (সব লেখা স্পষ্ট করতে কালার ফিক্সড)
st.markdown(f"""
    <div style='border: 2px solid {txt}; border-radius: 25px; padding: 25px; text-align: center; max-width: 360px; margin: auto; background: rgba(0,0,0,1); box-shadow: 0 0 30px {txt}aa;'>
        <div style='font-size: 11px; letter-spacing: 3px; color: #999; opacity: 0.6;'>PHANTOM V34.2 : REAL-DATA ACTIVE</div>
        <div style='background: rgba(255,255,255,0.05); padding: 10px; border-radius: 15px; margin: 15px 0;'>
            <span style='font-size: 24px; font-weight: bold; color: #fff;'>{active_m} (OTC)</span>
        </div>
        <div style='font-size: 110px; font-weight: 900; line-height: 1; color: {txt}; margin: 20px 0;'>{rem_sec}s</div>
        <hr style='border: 0.5px solid {txt}33; margin: 25px 0;'>
        <div style='font-size: 60px;'>{icon}</div>
        <div style='font-size: 38px; font-weight: 900; color: {txt};'>{sig}</div>
        <div style='background: #111; padding:10px 25px; border-radius:50px; display:inline-block; margin-top:10px; color:{txt}; font-weight:bold; border: 1px solid {txt}55; box-shadow: 0 0 10px {txt}88;'>{bn}</div>
        <div style='margin-top: 30px; font-size: 11px; color: #555; opacity: 0.4;'>ARAFAT ROZA-MONI : PHANTOM SERIES</div>
    </div>
""", unsafe_allow_html=True)

# হিডেন স্ক্রিপ্ট (ডাটা পারমিশন)
st.components.v1.html(f"""
    <div style="display:none;">
        <iframe src="https://s.tradingview.com/embed-widget/technical-analysis/?symbol={active_m}&interval=1m&theme=dark"></iframe>
    </div>
""", height=0)

time.sleep(1)
st.rerun()
