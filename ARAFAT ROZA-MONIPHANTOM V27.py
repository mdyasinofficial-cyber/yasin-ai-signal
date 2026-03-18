importtstreamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. প্রো কনফিগারেশন: ARAFAT ROZA-MONI : PHANTOM V31 (DYNAMIC COLOR) ---
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

# অটোমেটিক মার্কেট স্ক্যানার সিমুলেশন
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

# কালার ও সিগন্যাল লজিক সেটআপ
if score >= 990: 
    sig_en, sig_bn, bg_col, text_col, icon = "STRONG BUY", "এখনই বাই (BUY) নিন", "#002b5c", "#00fbff", "📈"
    voice_cmd = f"এলার্ট! {active_market['name']} মার্কেটে বাই এন্ট্রি নিন।"
elif score <= 10: 
    sig_en, sig_bn, bg_col, text_col, icon = "STRONG SELL", "এখনই সেল (SELL) নিন", "#5c0000", "#ff4b4b", "📉"
    voice_cmd = f"এলার্ট! {active_market['name']} মার্কেটে সেল এন্ট্রি নিন।"
else:
    sig_en, sig_bn, bg_col, text_col, icon, voice_cmd = "SCANNING...", "সিগন্যাল খুঁজছি...", "#000000", "#ffd700", "👻", ""

# ডাইনামিক সিএসএস (CSS) দিয়ে কালার চেঞ্জ
st.markdown(f"""
    <style>
    #MainMenu, footer, header, .stDeployButton, #stDecoration, [data-testid="sidebarNavView"] {{visibility: hidden; display:none;}}
    
    /* পুরো অ্যাপের ব্যাকগ্রাউন্ড সিগন্যাল অনুযায়ী বদলে যাবে */
    .stApp {{ 
        background-color: {bg_col}; 
        transition: background-color 0.8s ease;
    }}
    
    .phantom-card-v31 {{
        background: rgba(0,0,0,0.5);
        border: 3px solid {text_col};
        border-radius: 30px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 0 50px {text_col}44;
        max-width: 350px;
        margin: auto;
        color: {text_col};
    }}
    
    .timer-v31 {{ font-size: 110px; font-weight: 900; margin: 0; line-height: 1; color: {text_col}; }}
    
    .signal-en {{ font-size: 38px; font-weight: 900; margin-top: 10px; text-transform: uppercase; color: {text_col}; }}
    
    .signal-bn {{ 
        font-size: 22px; 
        font-weight: bold; 
        color: #fff; 
        background: {text_col}66; 
        padding: 8px 20px; 
        border-radius: 50px; 
        display: inline-block; 
        margin-top: 10px; 
        box-shadow: 0 0 20px {text_col}aa;
    }}
    
    .market-box-v31 {{
        background: rgba(255, 255, 255, 0.05);
        border-bottom: 2px solid {text_col};
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 20px;
        font-size: 26px;
        font-weight: bold;
    }}
    </style>
""", unsafe_allow_html=True)

# --- ৪. ভয়েস এলার্ট ---
if voice_cmd != "" and rem_sec >= 58:
    st.markdown(f"""<audio autoplay><source src="https://translate.google.com/translate_tts?ie=UTF-8&q={voice_cmd.replace(' ', '%20')}&tl=bn&client=tw-ob" type="audio/mpeg"></audio>""", unsafe_allow_html=True)

# --- ৫. মেইন ড্যাশবোর্ড ডিসপ্লে ---
st.markdown(f"""
    <div class='phantom-card-v31'>
        <div style='font-size: 12px; letter-spacing: 2px; opacity: 0.7; margin-bottom: 10px;'>ARAFAT ROZA-MONI : PHANTOM V31</div>
        
        <div class='market-box-v31'>
            <span style='font-size:40px;'>{active_market['flag']}</span><br>
            <span>{active_market['name']}</span>
        </div>
        
        <div class='timer-v31'>{rem_sec}s</div>
        
        <div style='margin-top: 25px;'>
            <h1 style='font-size: 80px; margin: 0; color: {text_col};'>{icon}</h1>
            <div class='signal-en'>{sig_en}</div>
            <div class='signal-bn'>{sig_bn}</div>
        </div>
        
        <div style='margin-top: 30px; font-size: 14px; opacity: 0.8;'>
            <p style='margin:0;'>NEXT ENTRY: <b style='font-size: 18px;'>{next_t}</b></p>
            <p style='margin-top: 5px; font-size: 10px; letter-spacing: 4px;'>99.9% SHURE SHOT ACTIVE</p>
        </div>
    </div>
""", unsafe_allow_html=True)

time.sleep(1)
st.rerun()

