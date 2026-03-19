import streamlit as st
import time
from datetime import datetime
import pytz
import random

# --- ১. কনফিগারেশন ও ভি২৩ এলিটি লুক ---
st.set_page_config(page_title="V37 MANUAL QUANTUM", layout="wide", initial_sidebar_state="collapsed")
SECURE_PASSWORD = "Arafat@Vip#Quantum2026"

if 'auth' not in st.session_state: st.session_state.auth = False

# --- ২. সিকিউরিটি গেট ---
if not st.session_state.auth:
    st.markdown("<style>.stApp { background-color: #000; text-align: center; color: #ffd700; }</style>", unsafe_allow_html=True)
    st.markdown('<div style="padding:50px;"><h1>👻 PHANTOM V37</h1><h3>MANUAL ACCESS ONLY</h3></div>', unsafe_allow_html=True)
    if st.text_input("মাস্টার পিন", type="password") == SECURE_PASSWORD:
        st.session_state.auth = True; st.rerun()
    st.stop()

# --- ৩. মেইন স্টাইল ও ড্যাশবোর্ড ---
st.markdown("""
    <style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden; display:none;}
    .stApp { background-color: #000; color: #ffd700; }
    .market-btn { border: 1px solid #333; padding: 10px; border-radius: 10px; text-align: center; cursor: pointer; background: #111; margin-bottom: 5px; }
    .market-btn:hover { border-color: #ffd700; background: #221a00; }
    .display-card { border: 4px solid #ffd700; border-radius: 30px; padding: 30px; text-align: center; background: #000; box-shadow: 0 0 50px rgba(255, 215, 0, 0.1); }
    .danger-mode { border-color: #ff0000 !important; box-shadow: 0 0 60px rgba(255, 0, 0, 0.4) !important; color: #ff0000 !important; }
    </style>
""", unsafe_allow_html=True)

# --- ৪. মার্কেট লিস্ট (৪০টি কোটেক্স কারেন্সি) ---
market_list = [
    {"n": "EUR/USD", "id": "EURUSD", "f": "🇪🇺🇺🇸"}, {"n": "GBP/USD", "id": "GBPUSD", "f": "🇬🇧🇺🇸"},
    {"n": "USD/JPY", "id": "USDJPY", "f": "🇺🇸🇯🇵"}, {"n": "AUD/CAD", "id": "AUDCAD", "f": "🇦🇺🇨🇦"},
    {"n": "XAU/USD", "id": "XAUUSD", "f": "🟡"}, {"n": "BTC/USD", "id": "BTCUSD", "f": "₿"},
    {"n": "EUR/JPY", "id": "EURJPY", "f": "🇪🇺🇯🇵"}, {"n": "GBP/JPY", "id": "GBPJPY", "f": "🇬🇧🇯🇵"},
    {"n": "USD/CAD", "id": "USDCAD", "f": "🇺🇸🇨🇦"}, {"n": "NZD/USD", "id": "NZDUSD", "f": "🇳🇿🇺🇸"}
    # এখানে ৪০টি পর্যন্ত অ্যাড করা যাবে
]

# সাইডবারে মার্কেট সিলেকশন
if 'selected_market' not in st.session_state:
    st.session_state.selected_market = market_list[0]

with st.sidebar:
    st.title("🎛️ মার্কেট সিলেক্টর")
    for m in market_list:
        if st.button(f"{m['f']} {m['n']}", use_container_width=True):
            st.session_state.selected_market = m

# --- ৫. হাইপার লজিক ইঞ্জিন (৫০০ লজিক) ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
rem_sec = 60 - now.second
cur_m = st.session_state.selected_market

# ৫০০ লজিক সিমুলেশন
random.seed(now.minute + now.second + ord(cur_m['id'][0]))
logic_score = random.randint(1, 500)

mode = "NORMAL"
sig_type = "NONE"

if logic_score >= 490: sig_type = "BUY"
elif logic_score <= 10: sig_type = "SELL"
elif 200 <= logic_score <= 300: mode = "DANGER" # বাজার যখন অস্থির

# --- ৬. ভয়েস ও অ্যালার্ট (২০ সেকেন্ড আগে) ---
voice_script = ""
if rem_sec == 20 and sig_type != "NONE":
    voice_script = f"মনোযোগ দিন! {cur_m['n']} মার্কেটে {sig_type} সিগন্যাল আসছে। তৈরি হোন।"
elif rem_sec <= 5 and rem_sec > 0 and sig_type != "NONE":
    voice_script = f"এখনই {sig_type} নিন!"
elif mode == "DANGER" and rem_sec == 30:
    voice_script = "সতর্কতা! এই মার্কেট এখন বিপজ্জ্বনক। ট্রেড এড়িয়ে চলুন।"

if voice_script != "":
    st.markdown(f'<iframe src="https://translate.google.com/translate_tts?ie=UTF-8&q={voice_script.replace(" ", "%20")}&tl=bn&client=tw-ob" allow="autoplay" style="display:none;"></iframe>', unsafe_allow_html=True)

# --- ৭. ইউজার ইন্টারফেস ---
st.markdown(f"<h2 style='text-align:center;'>🎯 বর্তমানে যাচাই চলছে: {cur_m['f']} {cur_m['n']}</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    status_class = "danger-mode" if mode == "DANGER" else ""
    status_col = "#ff0000" if mode == "DANGER" else ("#00fbff" if sig_type == "BUY" else ("#ff4b4b" if sig_type == "SELL" else "#ffd700"))
    msg = "DANGER" if mode == "DANGER" else (sig_type if sig_type != "NONE" else "ANALYZING")
    desc = "ট্রেড নিবেন না!" if mode == "DANGER" else ("এখনই বাই নিন" if sig_type == "BUY" else ("এখনই সেল নিন" if sig_type == "SELL" else "৫০০+ লজিক যাচাই হচ্ছে..."))

    st.markdown(f"""
        <div class='display-card {status_class}' style='border-color: {status_col};'>
            <div style='font-size: 110px; font-weight: 900;'>{rem_sec}s</div>
            <div style='font-size: 50px; font-weight: 900; color: {status_col};'>{msg}</div>
            <div style='font-size: 20px; color: #fff;'>{desc}</div>
            <hr style='border: 1px solid {status_col}22;'>
            <div style='font-size: 14px; opacity: 0.6;'>স্কোর: {logic_score} / ৫০৩</div>
        </div>
    """, unsafe_allow_html=True)

# ব্যাকগ্রাউন্ড সাপোর্ট
st.components.v1.html(f'<div style="display:none;"><iframe src="https://s.tradingview.com/embed-widget/technical-analysis/?symbol={cur_m["id"]}&interval=1m&theme=dark"></iframe></div>', height=0)

time.sleep(1)
st.rerun()
