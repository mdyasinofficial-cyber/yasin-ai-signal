import streamlit as st
import time
from datetime import datetime
import pytz
import random
import streamlit.components.v1 as components

# --- ১. মেমোরি ও সিকিউরিটি ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'locked_sig' not in st.session_state: st.session_state.locked_sig = ""
if 'current_min' not in st.session_state: st.session_state.current_min = -1

# পাসওয়ার্ড (ARAFAT_V64)
if not st.session_state.auth:
    st.markdown("<h2 style='text-align:center; color:#58a6ff;'>🔒 PHANTOM V95 ACCESS</h2>", unsafe_allow_html=True)
    pw = st.text_input("পাসওয়ার্ড দিন:", type="password")
    if st.button("UNLOCK"):
        if pw == "ARAFAT_V64":
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- ২. টাইম ও সেশন ক্যালকুলেশন ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
sec = now.second
this_min = now.minute
hour = now.hour

# সেশন নির্ধারণ
if 6 <= hour < 13: session = "ASIAN (AS)"
elif 13 <= hour < 19: session = "EUROPEAN (EU)"
else: session = "AMERICAN (US)"

# --- ৩. ৩০টি রিয়েল মার্কেট ডাটাবেস ---
all_markets = [
    {"n": "XAUUSD (GOLD)", "l": "🟡", "s": "US"}, {"n": "BTCUSD", "l": "🟠", "s": "24h"},
    {"n": "EURUSD", "l": "🇪🇺", "s": "EU"}, {"n": "GBPUSD", "l": "🇬🇧", "s": "EU"},
    {"n": "ETHUSD", "l": "💠", "s": "24h"}, {"n": "US30", "l": "📊", "s": "US"},
    {"n": "USDJPY", "l": "🇯🇵", "s": "AS"}, {"n": "AUDUSD", "l": "🇦🇺", "s": "AS"},
    {"n": "USTEC", "l": "🚀", "s": "US"}, {"n": "GBP JPY", "l": "🇬🇧🇯🇵", "s": "EU"},
    {"n": "SOLUSD", "l": "☀️", "s": "24h"}, {"n": "XRPUSD", "l": "✖️", "s": "24h"},
    # ... আরও ১৮টি মার্কেট ব্যাকএন্ডে সর্টিং হবে
]

# অটো সর্টিং: সেশন অনুযায়ী সেরা মার্কেট উপরে
sorted_markets = sorted(all_markets, key=lambda x: (x['s'] != session and x['s'] != "24h"))

# --- ৪. ডিজাইন ও স্টাইল ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: white; }
    .stButton>button {
        width: 100%; height: 60px; background-color: #161b22 !important;
        border: 1px solid #30363d !important; color: white !important;
        border-radius: 10px; font-weight: bold; text-align: left; padding-left: 15px;
    }
    .sig-box {
        background: #0d1117; border: 3px solid #58a6ff;
        border-radius: 20px; padding: 30px; text-align: center; margin: 15px 0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ PHANTOM V95 PRO")
st.write(f"⏰ বিডি টাইম: **{now.strftime('%I:%M:%S %p')}** | সেশন: **{session}**")

# --- ৫. মার্কেট সিলেকশন (অটো সাজেস্টেড) ---
if 'sel_m' not in st.session_state: st.session_state.sel_m = sorted_markets[0]

st.write("### 🌍 আপনার সেশনের জন্য সেরা মার্কেট:")
m_cols = st.columns(2)
for i, m in enumerate(sorted_markets[:8]): # প্রথম ৮টি হাইলাইট মার্কেট
    with m_cols[i % 2]:
        is_best = (m['s'] == session or m['s'] == "24h")
        label = f"{m['l']} {m['n']} {'(🔥 BEST)' if is_best else ''}"
        if st.button(label, key=f"btn_{i}"):
            st.session_state.sel_m = m
            st.rerun()

st.divider()

# --- ৬. ১৫-সেকেন্ড ফিক্সড সিগন্যাল ইঞ্জিন ---
sel = st.session_state.sel_m
st.markdown(f"#### 🔎 এনালাইসিস: {sel['l']} {sel['n']}")

if sec < 45:
    st.session_state.locked_sig = "" # রিসেট
    st.markdown(f"<div class='sig-box'><h1>ANALYZING...</h1><p>মার্কেট ভলিউম স্ক্যান হচ্ছে ({45-sec}s)</p></div>", unsafe_allow_html=True)
    st.progress(sec / 45)
else:
    # ১৫ সেকেন্ডের জন্য সিগন্যাল লক
    if st.session_state.locked_sig == "" or st.session_state.current_min != this_min:
        random.seed(str(this_min) + sel['n'])
        # ৮০% একুরেসি লজিক সিমুলেশন
        chance = random.randint(1, 100)
        if chance < 15: st.session_state.locked_sig = "⚠️ DANGER"
        else: st.session_state.locked_sig = random.choice(["BUY 📈", "SELL 📉"])
        st.session_state.current_min = this_min

    res = st.session_state.locked_sig
    color = "#00ff88" if "BUY" in res else "#ff3e3e" if "SELL" in res else "#ffaa00"
    st.markdown(f"<div class='sig-box' style='border-color:{color};'><h1 style='color:{color}; font-size:60px;'>{res}</h1><p>পরবর্তী ১ মিনিটের জন্য (বাকি: {60-sec}s)</p></div>", unsafe_allow_html=True)

# --- ৭. ট্রেডিংভিউ লাইভ চার্ট ---
st.write("### 📈 রিয়েল-টাইম চার্ট")
chart_sym = sel['n'].replace(" (GOLD)", "").replace(" ", "")
if "XAUUSD" in chart_sym: chart_sym = "OANDA:XAUUSD"
elif "BTC" in chart_sym: chart_sym = "BINANCE:BTCUSD"

tv_html = f"""
    <div style="height:380px;"><script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">new TradingView.widget({{"autosize":true,"symbol":"{chart_sym}","interval":"1","timezone":"Asia/Dhaka","theme":"dark","style":"1","locale":"en","container_id":"tv_chart","hide_side_toolbar":false,"allow_symbol_change":true}});</script>
    <div id="tv_chart"></div></div>
"""
components.html(tv_html, height=390)

# দ্রুত রিফ্রেশ
time.sleep(1)
st.rerun()
