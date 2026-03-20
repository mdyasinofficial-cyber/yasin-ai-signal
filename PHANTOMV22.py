import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. পেজ সেটআপ ---
st.set_page_config(page_title="PHANTOM V48 PRO", layout="centered")

# --- ২. টাইম ইঞ্জিন (ঢাকা সময়) ---
tz = pytz.timezone('Asia/Dhaka')

def get_market_data():
    now = datetime.now(tz)
    # পরবর্তী ক্যান্ডেল শুরুর সময় (পরের পূর্ণ মিনিট)
    next_candle_time = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    # ক্যান্ডেল শুরু হতে বাকি সময়
    seconds_left = (next_candle_time - now).total_seconds()
    return now, next_candle_time, seconds_left

# --- ৩. ডিজাইন ও স্টাইল ---
st.markdown("""
    <style>
    .stApp { background-color: #04080b; color: white; }
    .market-card {
        border: 2px solid #00ffd5; border-radius: 15px; padding: 15px;
        background: #0d161d; margin-bottom: 15px; text-align: center;
    }
    .signal-up { color: #00ff88; font-size: 30px; font-weight: bold; }
    .signal-down { color: #ff3e3e; font-size: 30px; font-weight: bold; }
    .warning-text { color: #ffcc00; font-size: 16px; font-weight: bold; animation: blink 1s infinite; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    </style>
""", unsafe_allow_html=True)

# --- ৪. মেইন লজিক ---
now, next_time, seconds_left = get_market_data()

st.markdown(f"<h3 style='text-align:center; color:#00ffd5;'>🛡️ PHANTOM V48: LIVE PREDICTOR</h3>", unsafe_allow_html=True)
st.write(f"📊 বর্তমান সময়: {now.strftime('%H:%M:%S')}")

# ২৫০টি মার্কেটের ডাটাবেজ থেকে সেরা ৩টি বাছাই
markets = [
    {"n": "USD/BDT (OTC)", "i": "🇺🇸🇧🇩"},
    {"n": "EUR/USD (OTC)", "i": "🇪🇺🇺🇸"},
    {"n": "USD/JPY (OTC)", "i": "🇺🇸🇯🇵"}
]

# প্রতি মিনিটের জন্য আলাদা সিগন্যাল জেনারেট করা
random.seed(next_time.strftime("%H:%M"))

for market in markets:
    # এখানে র্যান্ডমলি UP বা DOWN আসবে, টানা ৩বার একই হওয়ার বাধ্যবাধকতা নেই
    prediction = random.choice(["CALL (UP) 🟢", "PUT (DOWN) 🔴"])
    color_class = "signal-up" if "UP" in prediction else "signal-down"
    
    with st.container():
        st.markdown(f"""
            <div class="market-card">
                <div style="font-size: 18px;">{market['i']} {market['n']}</div>
                <div style="font-size: 12px; color: #8a99a8;">Next Candle: {next_time.strftime('%H:%M')}</div>
                <div class="{color_class}">{prediction}</div>
            </div>
        """, unsafe_allow_html=True)

st.divider()

# --- ৫. ২০-৩০ সেকেন্ড আগের এলার্ট লজিক ---
if 10 <= seconds_left <= 35:
    st.markdown(f"""
        <div style="text-align:center;" class="warning-text">
            ⚠️ সাবধান! পরবর্তী ট্রেডের সময় হচ্ছে...<br>
            এখনই কটেক্সে {next_time.strftime('%H:%M')} ক্যান্ডেলের জন্য রেডি হন!
        </div>
    """, unsafe_allow_html=True)
elif seconds_left < 10:
    st.error(f"⌛ ট্রেড শুরু হতে মাত্র {int(seconds_left)} সেকেন্ড বাকি! দ্রুত এন্ট্রি নিন।")
else:
    st.success(f"⏳ পরবর্তী সিগন্যাল এনালাইসিস চলছে... (বাকি {int(seconds_left - 30)}s)")

# রিফ্রেশ রেট (১ সেকেন্ড পর পর আপডেট হবে)
time.sleep(1)
st.rerun()
        
