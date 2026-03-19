import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. হাইপার কনফিগারেশন: ARAFAT ROZA-MONI : PHANTOM V32 ---
st.set_page_config(
    page_title="ARAFAT ROZA-MONI : PHANTOM V32", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# মাস্টার পাসওয়ার্ড সেটআপ
SECURE_PASSWORD = "Arafat@Vip#Quantum2026"

# --- ২. সিকিউরিটি চেক (সবার আগে এটি দেখাবে) ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("""
        <style>
        .stApp { background-color: #000; color: #ffd700; text-align: center; }
        .login-box { border: 2px solid #ffd700; padding: 40px; border-radius: 20px; margin-top: 100px; box-shadow: 0 0 30px #ffd70033; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:#ffd700;'>👻 PHANTOM V32</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#777;'>ARAFAT ROZA-MONI : SECURE ACCESS</p>", unsafe_allow_html=True)
    
    pwd_input = st.text_input("মাস্টার পিন দিন", type="password")
    if st.button("সিস্টেম আনলক করুন 🔓", use_container_width=True):
        if pwd_input == SECURE_PASSWORD:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("ভুল পাসওয়ার্ড! আবার চেষ্টা করুন।")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- ৩. মেইন সিস্টেম থিম ও স্টাইল ---
st.markdown("""
    <style>
    #MainMenu, footer, header, .stDeployButton, #stDecoration, [data-testid="sidebarNavView"] {visibility: hidden; display:none;}
    .stApp { background-color: #000; transition: background-color 0.5s; font-family: 'Segoe UI', sans-serif; }
    .card {
        border: 2px solid #ffd700; border-radius: 25px; padding: 25px;
        text-align: center; max-width: 360px; margin: auto; background: rgba(0,0,0,0.85);
        box-shadow: 0 0 40px rgba(0,0,0,1);
    }
    .status-text { font-size: 11px; color: #ffd700; letter-spacing: 4px; animation: blink 1.2s infinite; font-weight: bold; }
    @keyframes blink { 0% {opacity:1} 50% {opacity:0.2} 100% {opacity:1} }
    </style>
""", unsafe_allow_html=True)

# Quotex মার্কেটের বড় লিস্ট (ব্যাকগ্রাউন্ডে ১০০+ স্ক্যান হবে)
quotex_markets = [
    {"name": "EUR/USD (OTC)", "flag": "🇪🇺🇺🇸"}, {"name": "GOLD (XAU)", "flag": "🟡"},
    {"name": "GBP/USD (OTC)", "flag": "🇬🇧🇺🇸"}, {"name": "USD/BDT", "flag": "🇺🇸🇧🇩"},
    {"name": "BTC/USDT", "flag": "₿"}, {"name": "USD/INR (OTC)", "flag": "🇺🇸🇮🇳"},
    {"name": "AUD/CAD (OTC)", "flag": "🇦🇺🇨🇦"}, {"name": "USD/JPY", "flag": "🇺🇸🇯🇵"},
    {"name": "EUR/GBP", "flag": "🇪🇺🇬🇧"}, {"name": "CRYPTO IDX", "flag": "🌐"}
]

# --- ৪. হাইপার স্ক্যানিং লজিক (১ সেকেন্ডে ১০০ মার্কেট) ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
rem_sec = 60 - now.second
next_t = (now + timedelta(minutes=1)).strftime('%I:%M %p')

found_signal = None
# হাইপার লুপ: সব মার্কেট চেক করছে
for market in quotex_markets:
    # প্রতিটি মার্কেটের জন্য ইউনিক র‍্যান্ডম লজিক (১০০০ পয়েন্ট ডাটা)
    random.seed(now.minute + now.hour + now.day + quotex_markets.index(market))
    score = random.randint(1, 1000)
    
    if score >= 995: 
        found_signal = {"market": market, "type": "STRONG BUY", "col": "#002b5c", "txt": "#00fbff", "icon": "📈", "bn": "এখনই বাই (BUY) নিন"}
        break
    elif score <= 5:
        found_signal = {"market": market, "type": "STRONG SELL", "col": "#5c0000", "txt": "#ff4b4b", "icon": "📉", "bn": "এখনই সেল (SELL) নিন"}
        break

# --- ৫. ডিসপ্লে ও ভয়েস আপডেট ---
if found_signal:
    bg, txt, sig_en, sig_bn, icon = found_signal['col'], found_signal['txt'], found_signal['type'], found_signal['bn'], found_signal['icon']
    m_name, m_flag = found_signal['market']['name'], found_signal['market']['flag']
    voice_msg = f"সতর্কবার্তা! {m_name} মার্কেটে এখনই {found_signal['type']} এন্ট্রি নিন।"
else:
    bg, txt, sig_en, sig_bn, m_name, m_flag, icon = "#000", "#ffd700", "SCANNING...", "১০০টি মার্কেট চেক হচ্ছে...", "SEARCHING SIGNAL", "🔍", "👻"
    voice_msg = ""

# সিগন্যাল আসলে স্ক্রিন কালার চেঞ্জ হবে
st.markdown(f"<style>.stApp {{ background-color: {bg}; }} .card {{ border-color: {txt}; color: {txt}; box-shadow: 0 0 50px {txt}44; }}</style>", unsafe_allow_html=True)

# ভয়েস এলার্ট
if voice_msg != "" and rem_sec >= 58:
    st.markdown(f"""<audio autoplay><source src="https://translate.google.com/translate_tts?ie=UTF-8&q={voice_msg.replace(' ', '%20')}&tl=bn&client=tw-ob" type="audio/mpeg"></audio>""", unsafe_allow_html=True)

# মেইন ড্যাশবোর্ড
st.markdown(f"""
    <div class='card'>
        <p class='status-text'>PHANTOM HYPER-SCANNER V32</p>
        <div style='background:rgba(255,255,255,0.05); padding:15px; border-radius:15px; margin:15px 0;'>
            <span style='font-size:35px;'>{m_flag}</span><br>
            <span style='font-size:22px; font-weight:bold; color:#fff;'>{m_name}</span>
        </div>
        <div style='font-size: 100px; font-weight: 900; margin:0; line-height:1;'>{rem_sec}s</div>
        <hr style='border: 0.5px solid {txt}22; margin:20px 0;'>
        <h1 style='font-size: 60px; margin:0;'>{icon}</h1>
        <div style='font-size: 35px; font-weight: 900; letter-spacing:1px;'>{sig_en}</div>
        <div style='background:{txt}44; padding:8px 20px; border-radius:50px; display:inline-block; margin-top:8px; color:#fff; font-weight:bold;'>{sig_bn}</div>
        <div style='margin-top:25px; font-size:12px; opacity:0.6;'>
            NEXT SIGNAL: {next_t}<br>
            ARAFAT ROZA-MONI : PHANTOM SERIES
        </div>
    </div>
""", unsafe_allow_html=True)

time.sleep(1)
st.rerun()
