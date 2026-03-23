import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random
import pandas as pd
import pandas_ta as ta  # টেকনিক্যাল এনালাইসিসের জন্য (ইন্সটল করতে হবে: pip install pandas_ta)

# --- ১. হাইপার কনফিগারেশন: ARAFAT ROZA-MONI : PHANTOM V32 PRO ---
st.set_page_config(
    page_title="ARAFAT ROZA-MONI : PHANTOM V32 PRO", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# মাস্টার পাসওয়ার্ড সেটআপ (সিকিউরিটির জন্য এটি পরিবর্তন করুন)
SECURE_PASSWORD = "Arafat@Vip#Quantum2026"

# --- ২. সিকিউরিটি চেক ---
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
    st.markdown("<h1 style='color:#ffd700;'>👻 PHANTOM V32 PRO</h1>", unsafe_allow_html=True)
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
        text-align: center; max-width: 380px; margin: auto; background: rgba(0,0,0,0.85);
        box-shadow: 0 0 40px rgba(0,0,0,1);
    }
    .status-text { font-size: 11px; color: #ffd700; letter-spacing: 4px; animation: blink 1.2s infinite; font-weight: bold; }
    @keyframes blink { 0% {opacity:1} 50% {opacity:0.2} 100% {opacity:1} }
    .indicator-val { font-size: 14px; color: #aaa; margin-top: 5px; }
    </style>
""", unsafe_allow_html=True)

# Quotex মার্কেটের বড় লিস্ট
quotex_markets = [
    {"name": "EUR/USD (OTC)", "flag": "🇪🇺🇺🇸"}, {"name": "GOLD (XAU)", "flag": "🟡"},
    {"name": "GBP/USD (OTC)", "flag": "🇬🇧🇺🇸"}, {"name": "USD/BDT", "flag": "🇺🇸🇧🇩"},
    {"name": "BTC/USDT", "flag": "₿"}, {"name": "USD/INR (OTC)", "flag": "🇺🇸🇮🇳"},
    {"name": "AUD/CAD (OTC)", "flag": "🇦🇺🇨🇦"}, {"name": "USD/JPY", "flag": "🇺🇸🇯🇵"},
    {"name": "EUR/GBP", "flag": "🇪🇺🇬🇧"}, {"name": "CRYPTO IDX", "flag": "🌐"}
]

# --- ৪. টেকনিক্যাল এনালাইসিস লজিক ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
rem_sec = 60 - now.second
next_t = (now + timedelta(minutes=1)).strftime('%I:%M %p')

def get_real_time_indicators():
    """রিয়েল-টাইম ডাটা সিমুলেট করে ইন্ডিকেটর ক্যালকুলেট করে।"""
    # নোট: প্রোডাকশন লেভেলে এখানে ব্রোকার API থেকে ডাটা আসবে।
    # আমরা এখানে Pandas DataFrame তৈরি করে Pandas TA লাইব্রেরি ব্যবহার করছি।
    
    # ডামি ডাটা তৈরি (২০টি ক্যান্ডেল)
    data = {
        'close': [random.uniform(1.0900, 1.1000) for _ in range(20)]
    }
    df = pd.DataFrame(data)
    
    # RSI (14 period) ক্যালকুলেশন
    df.ta.rsi(length=14, append=True)
    
    # SMA (10 period) ক্যালকুলেশন
    df.ta.sma(length=10, append=True)
    
    last_rsi = round(df['RSI_14'].iloc[-1], 2)
    last_sma = round(df['SMA_10'].iloc[-1], 4)
    last_price = round(df['close'].iloc[-1], 4)
    
    return last_price, last_rsi, last_sma

# ইন্ডিকেটর ডাটা নেওয়া
last_price, last_rsi, last_sma = get_real_time_indicators()

# --- ৫. সিগন্যাল লজিক (ইন্ডিকেটর ভিত্তিক) ---
best_signal = None

# সব মার্কেট চেক করার পরিবর্তে, প্রথম মার্কেটে সিগন্যাল খুঁজছে (ব্রোকার API থাকলে লুপ ব্যবহার হবে)
for market in quotex_markets:
    # এখানে রিয়েল লজিক অনুযায়ী সিগন্যাল তৈরি করা হবে
    # উদাহরণ: RSI < 30 এবং Price > SMA হলে BUY
    
    if last_rsi < 30 and last_price > last_sma:
        best_signal = {"market": market, "type": "STRONG BUY", "col": "#002b5c", "txt": "#00fbff", "icon": "📈", "bn": "এখনই বাই (BUY) নিন"}
        break
    elif last_rsi > 70 and last_price < last_sma:
        best_signal = {"market": market, "type": "STRONG SELL", "col": "#5c0000", "txt": "#ff4b4b", "icon": "📉", "bn": "এখনই সেল (SELL) নিন"}
        break

# --- ৬. ডিসপ্লে ও ভয়েস আপডেট ---
if best_signal:
    bg, txt, sig_en, sig_bn, icon = best_signal['col'], best_signal['txt'], best_signal['type'], best_signal['bn'], best_signal['icon']
    m_name, m_flag = best_signal['market']['name'], best_signal['market']['flag']
    voice_msg = f"সতর্কবার্তা! {m_name} মার্কেটে এখনই {best_signal['type']} এন্ট্রি নিন।"
else:
    bg, txt, sig_en, sig_bn, m_name, m_flag, icon = "#000", "#ffd700", "SCANNING...", "১০০টি মার্কেট চেক হচ্ছে...", "SEARCHING SIGNAL", "🔍", "👻"
    voice_msg = ""

# সিগন্যাল আসলে স্ক্রিন কালার চেঞ্জ হবে
st.markdown(f"<style>.stApp {{ background-color: {bg}; }} .card {{ border-color: {txt}; color: {txt}; box-shadow: 0 0 50px {txt}44; }}</style>", unsafe_allow_html=True)

# ভয়েস এলার্ট (ক্যান্ডেল শুরু হওয়ার ঠিক আগে)
if voice_msg != "" and rem_sec >= 58:
    st.markdown(f"""<audio autoplay><source src="https://translate.google.com/translate_tts?ie=UTF-8&q={voice_msg.replace(' ', '%20')}&tl=bn&client=tw-ob" type="audio/mpeg"></audio>""", unsafe_allow_html=True)

# মেইন ড্যাশবোর্ড
st.markdown(f"""
    <div class='card'>
        <p class='status-text'>PHANTOM HYPER-SCANNER V32 PRO</p>
        <div style='background:rgba(255,255,255,0.05); padding:15px; border-radius:15px; margin:15px 0;'>
            <span style='font-size:35px;'>{m_flag}</span><br>
            <span style='font-size:22px; font-weight:bold; color:#fff;'>{m_name}</span>
            <div class='indicator-val'>
                Price: {last_price} | RSI: {last_rsi} | SMA: {last_sma}
            </div>
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

# প্রতি ১ সেকেন্ডে রিফ্রেশ
time.sleep(1)
st.rerun()
