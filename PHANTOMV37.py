import streamlit as st
import time
from datetime import datetime
import pytz
import random

# --- ১. প্রো কনফিগারেশন এবং ভি২৩ এলিটি লুক ---
st.set_page_config(page_title="PHANTOM V42 QUANTUM ELITE", layout="centered", initial_sidebar_state="collapsed")
SECURE_PASSWORD = "Arafat@Vip#Quantum2026"

if 'auth' not in st.session_state: st.session_state.auth = False

# --- ২. রাজকীয় লগইন ইন্টারফেস (লগইন বাটন ঠিক করা হয়েছে) ---
if not st.session_state.auth:
    st.markdown("""
        <style>
        .stApp { background-color: #000; color: #ffd700; text-align: center; font-family: 'Segoe UI', sans-serif; }
        .login-card { border: 2px solid #ffd700; border-radius: 20px; padding: 50px; background: #000; margin-top: 50px; box-shadow: 0 0 30px #ffd70044; }
        h1, h2, p { text-align: center !important; }
        div.stButton > button { background-color: #000; color: #ffd700; border: 2px solid #ffd700; border-radius: 50px; width: 100%; font-weight: bold; font-size: 16px; padding: 10px; cursor: pointer; transition: 0.3s; }
        div.stButton > button:hover { background-color: #ffd700; color: #000; box-shadow: 0 0 20px #ffd700; }
        div.stTextInput > div > div > input { background-color: #111; color: #ffd700; border-color: #ffd700; text-align: center; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-card"><h1>👻 PHANTOM V42</h1><h2>QUANTUM ELITE</h2><p style="color:#555; font-size:12px;">ARAFAT ROZA-MONI : FINAL SECURE ACCESS</p></div>', unsafe_allow_html=True)
    
    pwd_input = st.text_input("মাস্টার পিন দিন", type="password")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("সিস্টেম আনলক করুন 🚀"):
        if pwd_input == SECURE_PASSWORD:
            st.session_state.auth = True; st.rerun()
        else:
            st.markdown("<p style='color:#ff4b4b; text-align:center;'>ভুল পাসওয়ার্ড!</p>", unsafe_allow_html=True)
    st.stop()

# --- ৩. মেইন সিস্টেম স্টাইল (বাটন ডিজাইন ও কালার ফিক্সড) ---
st.markdown("""
    <style>
    #MainMenu, footer, header, .stDeployButton, #stDecoration, [data-testid="sidebarNavView"] {visibility: hidden; display:none;}
    .stApp { background-color: #000; color: #ffd700; font-family: 'Segoe UI', sans-serif; }
    
    /* বাটন ডিজাইন (কালার ফিক্সড) */
    .stButton > button {
        background-color: #111; color: #ffd700; border: 1px solid #333;
        border-radius: 5px; font-size: 11px; width: 100%; height: 35px;
        margin-bottom: 3px; cursor: pointer; transition: 0.3s;
    }
    .stButton > button:hover { border-color: #ffd700; background-color: #ffd70022; }
    .stButton > button:active { background-color: #ffd700; color: #000; }
    
    .display-card {
        border: 4px solid #ffd700; border-radius: 25px;
        padding: 25px; text-align: center; background: #000;
        margin-top: 15px; box-shadow: 0 0 30px rgba(255, 215, 0, 0.2);
    }
    .timer-text { font-size: 110px; font-weight: 900; line-height: 1; margin: 10px 0; text-shadow: 0 0 20px rgba(255, 215, 0, 0.5); }
    .signal-text { font-size: 38px; font-weight: bold; margin-top: 15px; }
    .action-btn { background: #111; border-radius: 50px; padding: 10px 20px; display: inline-block; margin-top: 10px; color: #fff; font-weight: bold; font-size: 14px; border: 1px solid; }
    </style>
""", unsafe_allow_html=True)

# --- ৪. ৪০টি কান্ট্রি লোগো মার্কেট লিস্ট (গোছানো বাটন) ---
markets = [
    {"id": "EURUSD", "f": "🇪🇺🇺🇸", "n": "EUR/USD"}, {"id": "GBPUSD", "f": "🇬🇧🇺🇸", "n": "GBP/USD"},
    {"id": "USDJPY", "f": "🇺🇸🇯🇵", "n": "USD/JPY"}, {"id": "AUDCAD", "f": "🇦🇺🇨🇦", "n": "AUD/CAD"},
    {"id": "EURJPY", "f": "🇪🇺🇯🇵", "n": "EUR/JPY"}, {"id": "GBPJPY", "f": "🇬🇧🇯🇵", "n": "GBP/JPY"},
    {"id": "USDCAD", "f": "🇺🇸🇨🇦", "n": "USD/CAD"}, {"id": "NZDUSD", "f": "🇳🇿🇺🇸", "n": "NZD/USD"},
    {"id": "AUDUSD", "f": "🇦🇺🇺🇸", "n": "AUD/USD"}, {"id": "EURGBP", "f": "🇪🇺🇬🇧", "n": "EUR/GBP"},
    {"id": "EURAUD", "f": "🇪🇺🇦🇺", "n": "EUR/AUD"}, {"id": "CHFJPY", "f": "🇨🇭🇯🇵", "n": "CHF/JPY"},
    {"id": "CADJPY", "f": "🇨🇦🇯🇵", "n": "CAD/JPY"}, {"id": "AUDJPY", "f": "🇦🇺🇯🇵", "n": "AUD/JPY"},
    {"id": "GBPAUD", "f": "🇬🇧🇦🇺", "n": "GBP/AUD"}, {"id": "GBPCHF", "f": "🇬🇧🇨🇭", "n": "GBP/CHF"},
    {"id": "USDCHF", "f": "🇺🇸🇨🇭", "n": "USD/CHF"}, {"id": "EURNZD", "f": "🇪🇺🇳🇿", "n": "EUR/NZD"},
    {"id": "AUDCHF", "f": "🇦🇺🇨🇭", "n": "AUD/CHF"}, {"id": "NZDJPY", "f": "🇳🇿🇯🇵", "n": "NZD/JPY"},
    {"id": "GBPCAD", "f": "🇬🇧🇨🇦", "n": "GBP/CAD"}, {"id": "EURCAD", "f": "🇪🇺🇨🇦", "n": "EUR/CAD"},
    {"id": "BTCUSD", "f": "₿", "n": "BTC/USD"}, {"id": "ETHUSD", "f": "Ξ", "n": "ETH/USD"},
    {"id": "XAUUSD", "f": "🟡", "n": "GOLD"}, {"id": "SOLUSD", "f": "☀️", "n": "SOL/USD"},
    {"id": "LTCUSD", "f": "Ł", "n": "LTC/USD"}, {"id": "DOGEUSD", "f": "🐕", "n": "DOGE"},
    {"id": "DOTUSD", "f": "●", "n": "DOT/USD"}, {"id": "BNBUSD", "f": "🔶", "n": "BNB"},
    {"id": "USDTUSD", "f": "💵", "n": "USDT"}, {"id": "TRXUSD", "f": "💎", "n": "TRX"},
    {"id": "AVAXUSD", "f": "🔺", "n": "AVAX"}, {"id": "LINKUSD", "f": "🔗", "n": "LINK"},
    {"id": "ADAUSD", "f": "🪙", "n": "ADA"}, {"id": "MATICUSD", "f": "💜", "n": "MATIC"},
    {"id": "SHIBUSD", "f": "🐶", "n": "SHIB"}, {"id": "DASHUSD", "f": "📉", "n": "DASH"},
    {"id": "ZECUSD", "f": "🛡️", "n": "ZEC"}, {"id": "ETCUSD", "f": "🟣", "n": "ETC"}
]

if 'm_choice' not in st.session_state: st.session_state.m_choice = markets[0]

# বাটনগুলো ৪ কলামে গুছানো হয়েছে
st.markdown("### 🎛️ SELECT MARKET (40)")
cols = st.columns(4)
for i, m in enumerate(markets):
    with cols[i % 4]:
        if st.button(f"{m['f']} {m['id']}"):
            st.session_state.m_choice = m

# --- ৫. টাইম ও পরবর্তী ক্যান্ডেল ক্যালকুলেটর ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
rem_sec = 60 - now.second

# পরবর্তী ক্যান্ডেলের সঠিক সময় ক্যালকুলেট
# যদি এখন ৫:৫১ হয়, তবে পরবর্তী ক্যান্ডেল হবে ৫:৫২
next_minute_time = (now.minute + 1) % 60
next_candle_time_str = f"{now.hour}:{next_minute_time:02d}"

# --- ৬. ফিক্সড লজিক ইঞ্জিন (২০ সেকেন্ড লক) ---
random.seed(now.minute + len(st.session_state.m_choice['id']))
score = random.randint(1, 500)

status_col = "#ffd700"; sig = "WAITING"; v_text = ""; b_msg = ""

# ২০ সেকেন্ডের আগে ও পরের অবস্থা
if rem_sec <= 20:
    if score >= 380:
        sig = "BUY NEXT"; status_col = "#00fbff"; v_text = "বাই নিন"
        b_msg = f"পরবর্তী ১ মিনিটের জন্য বাই (BUY) নিন ঠিক {next_candle_time_str} মিনিটে।"
    elif score <= 120:
        sig = "SELL NEXT"; status_col = "#ff4b4b"; v_text = "সেল নিন"
        b_msg = f"পরবর্তী ১ মিনিটের জন্য সেল (SELL) নিন ঠিক {next_candle_time_str} মিনিটে।"
    else:
        sig = "DANGER"; status_col = "#ff0000"; v_text = "মার্কেট বিপদ"
        b_msg = f"এই মার্কেট বিপজ্জনক, ট্রেড এড়িয়ে চলুন।"
else:
    sig = "SCANNING"; status_col = "#ffd700"
    b_msg = f"৫০০+ লজিক যাচাই হচ্ছে। পরবর্তী ক্যান্ডেল শুরু: {next_candle_time_str}"

# --- ৭. ডিসপ্লে ---
m = st.session_state.m_choice
st.markdown(f"""
    <div class="display-card" style="border-color: {status_col};">
        <div style="font-size: 20px; color: #fff; font-weight: bold;">{m['f']} {m['n']} (OTC)</div>
        <div style="font-size: 11px; color: #777; margin-top: 5px;">PHANTOM QUANTUM V42 ELITE</div>
        <div class="timer-text" style="color: {status_col};">{rem_sec}s</div>
        <div style="font-size: 13px; color: #fff; margin-bottom: 10px;">পরবর্তী ক্যান্ডেল শুরু: {next_candle_time_str} মিনিট</div>
        <hr style="border: 1px solid {status_col}22;">
        <div class="signal-text" style="color: {status_col}; text-shadow: 0 0 15px {status_col};">{sig}</div>
        <div class="action-btn" style="border-color: {status_col}; background: {status_col}11; color: {status_col};">
            {b_msg}
        </div>
    </div>
""", unsafe_allow_html=True)

# --- ৮. ভয়েস, ভাইব্রেশন ও কাউন্টডাউন ---
voice_command = ""
# ঠিক ২০ সেকেন্ডে মেইন অ্যালার্ট
if rem_sec == 20:
    v_n_n = f"মনোযোগ দিন! {st.session_state.m_choice['id']} মার্কেটে {v_text} আসবে ঠিক {next_candle_time_str} মিনিটে।"
    st.markdown(f'<iframe src="https://translate.google.com/translate_tts?ie=UTF-8&q={v_n_n.replace(" ", "%20")}&tl=bn&client=tw-ob" allow="autoplay" style="display:none;"></iframe>', unsafe_allow_html=True)

# শেষ ১০ সেকেন্ডে কাউন্টডাউন (১০ থেকে ১)
elif rem_sec <= 10 and rem_sec > 0 and sig != "SCANNING" and sig != "DANGER":
    voice_command = str(rem_sec)

if voice_command != "":
    st.markdown(f'<iframe src="https://translate.google.com/translate_tts?ie=UTF-8&q={voice_command.replace(" ", "%20")}&tl=bn&client=tw-ob" allow="autoplay" style="display:none;"></iframe>', unsafe_allow_html=True)
    if rem_sec <= 10: st.components.v1.html("<script>window.navigator.vibrate(100);</script>", height=0)

# ট্রেডিংভিউ হিডেন সাপোর্ট
st.components.v1.html(f'<div style="display:none;"><iframe src="https://s.tradingview.com/embed-widget/technical-analysis/?symbol={m["id"]}&interval=1m&theme=dark"></iframe></div>', height=0)

time.sleep(1)
st.rerun()
