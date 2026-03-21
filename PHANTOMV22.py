import streamlit as st
import time
from datetime import datetime
import pytz
import streamlit.components.v1 as components

# --- ১. পাসওয়ার্ড প্রটেকশন (ARAFAT_V64) ---
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h2 style='text-align:center; color:#58a6ff;'>🔒 PHANTOM V78 ACCESS</h2>", unsafe_allow_html=True)
    pw = st.text_input("পাসওয়ার্ড দিন:", type="password")
    if st.button("UNLOCK"):
        if pw == "ARAFAT_V64":
            st.session_state.auth = True
            st.rerun()
        else: st.error("ভুল পাসওয়ার্ড!")
    st.stop()

# --- ২. সেশন লজিক ও মার্কেট লিস্ট ---
tz = pytz.timezone('Asia/Dhaka')
bd_now = datetime.now(tz)
hour = bd_now.hour

# সেশন নির্ধারণ
if 6 <= hour < 13: current_s = "AS" # এশিয়ান
elif 13 <= hour < 19: current_s = "EU" # ইউরোপ
else: current_s = "US" # আমেরিকান

all_markets = [
    {"n": "GOLD (XAUUSD)", "l": "🟡", "s": "US"}, {"n": "BTCUSD", "l": "🟠", "s": "24h"},
    {"n": "EURUSD", "l": "🇪🇺", "s": "EU"}, {"n": "GBPUSD", "l": "🇬🇧", "s": "EU"},
    {"n": "USDJPY", "l": "🇯🇵", "s": "AS"}, {"n": "AUDUSD", "l": "🇦🇺", "s": "AS"},
    {"n": "US30", "l": "📊", "s": "US"}, {"n": "ETHUSD", "l": "💠", "s": "24h"}
]

# অটো সর্টিং: সেরা মার্কেটগুলো উপরে আসবে
sorted_markets = sorted(all_markets, key=lambda x: (x['s'] != current_s and x['s'] != "24h"))

# --- ৩. ডিজাইন ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: white; }
    .stButton>button {
        width: 100%; height: 70px;
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        color: white !important; border-radius: 12px;
        text-align: left; padding-left: 15px;
    }
    .best-tag { color: #00ff88; font-size: 11px; font-weight: bold; }
    .sig-box {
        background: #0d1117; border: 2px solid #58a6ff;
        border-radius: 15px; padding: 25px; text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 PHANTOM V78 PRO")
st.write(f"⏰ বিডি টাইম: **{bd_now.strftime('%I:%M %p')}** | সেশন: **{current_s}**")

# --- ৪. মার্কেট ডিসপ্লে (স্মার্ট বাটন) ---
if 'active_m' not in st.session_state: st.session_state.active_m = sorted_markets[0]

st.write("### 🌍 আপনার জন্য সেরা মার্কেটগুলো:")
cols = st.columns(2)
for i, m in enumerate(sorted_markets):
    with cols[i % 2]:
        is_best = (m['s'] == current_s or m['s'] == "24h")
        tag = "🔥 BEST NOW" if is_best else "⏳ WAIT"
        btn_label = f"{m['l']} {m['n']}\n{tag}"
        
        if st.button(btn_label, key=f"m_{i}"):
            st.session_state.active_m = m
            st.rerun()

st.divider()

# --- ৫. সিগন্যাল ও চার্ট ---
sel = st.session_state.active_m
sec = bd_now.second

st.markdown(f"#### এনালাইসিস চলছে: {sel['l']} {sel['n']}")

if sec >= 50:
    res = "BUY 📈" if (bd_now.minute + sec) % 2 == 0 else "SELL 📉"
    color = "#00ff88" if "BUY" in res else "#ff3e3e"
    st.markdown(f"<div class='sig-box' style='border-color:{color};'><h1 style='color:{color};'>{res}</h1><p>এন্ট্রি নিন ১ মিনিটের জন্য</p></div>", unsafe_allow_html=True)
else:
    st.markdown(f"<div class='sig-box'><h1>ANALYZING...</h1><p>পরবর্তী ক্যান্ডেল স্ক্যান হচ্ছে ({50-sec}s)</p></div>", unsafe_allow_html=True)

# ট্রেডিংভিউ চার্ট (অটোমেটিক আপডেট)
st.write("### 📈 লাইভ রিয়েল চার্ট")
chart_sym = sel['n'].replace("US30", "DJI").replace("GOLD (XAUUSD)", "XAUUSD")
tradingview_html = f"""
    <div style="height:350px;"><script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">new TradingView.widget({{"autosize": true,"symbol": "{chart_sym}","interval": "1","timezone": "Asia/Dhaka","theme": "dark","style": "1","locale": "en","container_id": "tv_chart"}});
    </script><div id="tv_chart"></div></div>
"""
components.html(tradingview_html, height=360)

time.sleep(1)
st.rerun()
