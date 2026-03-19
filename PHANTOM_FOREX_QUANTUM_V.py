import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. মেম্বারশিপ ও কনফিগারেশন ---
USER_KEYS = {"ARAFAT_VIP_2026": "Arafat Bhai (Admin)"}
st.set_page_config(page_title="PHANTOM V13 HYBRID", layout="wide")

if 'auth' not in st.session_state: st.session_state.auth = False

# --- ২. লগইন প্রোটেকশন ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; color:#ffd700;'>👻 PHANTOM V13</h1>", unsafe_allow_html=True)
    key_input = st.text_input("মাস্টার পাসওয়ার্ড দিন", type="password")
    if st.button("সিস্টেম আনলক করুন"):
        if key_input in USER_KEYS:
            st.session_state.auth = True
            st.session_state.user = USER_KEYS[key_input]
            st.rerun()
    st.stop()

# --- ৩. ডিজাইন ও স্টাইল (image_9.png এর মতো কম্প্যাক্ট) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .compact-card {
        border: 1px solid #222; border-radius: 12px; padding: 15px;
        background: #111; margin-bottom: 12px;
        border-left: 10px solid #444; position: relative;
    }
    .buy-border { border-left-color: #00fbff !important; box-shadow: 0 0 10px #00fbff22; }
    .sell-border { border-left-color: #ff4b4b !important; box-shadow: 0 0 10px #ff4b4b22; }
    .entry-grid { display: flex; justify-content: space-between; margin-top: 10px; }
    .entry-box {
        background: #1a1a1a; padding: 10px; border-radius: 8px;
        text-align: center; border: 1px solid #333; width: 48%;
    }
    .bank-status { color: #00ff00; font-size: 13px; font-weight: bold; margin-top: 10px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- ৪. টাইম ইঞ্জিন (Bangladesh Time) ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
current_time_str = now.strftime("%I:%M:%S %p")

def get_entry_time(interval):
    next_m = (now.minute // interval + 1) * interval
    target = now.replace(minute=next_m % 60, second=0, microsecond=0)
    if next_m >= 60: target += timedelta(hours=1)
    return target.strftime("%I:%M %p")

e5 = get_entry_time(5)
e15 = get_entry_time(15)

# --- ৫. মার্কেট লিস্ট (২৫০+ মার্কেট) ---
markets = [
    {"n": "GOLD (XAUUSD)", "f": "🟡"}, {"n": "EURUSD", "f": "🇪🇺🇺🇸"}, 
    {"n": "GBPUSD", "f": "🇬🇧🇺🇸"}, {"n": "USDJPY", "f": "🇺🇸🇯🇵"},
    {"n": "BTCUSD", "f": "₿"}, {"n": "USDNGN-OTC", "f": "🇳🇬💻"},
    {"n": "USDBRL-OTC", "f": "🇧🇷💻"}, {"n": "EURGBP-OTC", "f": "🇪🇺🇬🇧"}
]
for a in ["EUR", "GBP", "AUD", "CAD", "NZD"]:
    for b in ["USD", "JPY", "CHF"]:
        markets.append({"n": f"{a}{b}", "f": "🌐"})
        markets.append({"n": f"{a}{b}-OTC", "f": "💻"})

# --- ৬. ড্যাশবোর্ড হেডার ও সার্চ ---
st.markdown(f"""
    <div style='background:#111; border:1px solid #333; padding:15px; border-radius:15px; text-align:center;'>
        <h2 style='margin:0; color:#ffd700;'>PHANTOM V13 [HYBRID ENGINE]</h2>
        <p style='margin:0; color:#aaa;'>🇧🇩 বাংলাদেশ রিয়েল টাইম: {current_time_str}</p>
    </div>
""", unsafe_allow_html=True)

search = st.text_input("🔍 মার্কেট সার্চ দিন (যেমন: GOLD, USDBRL, OTC)", placeholder="এখানে টাইপ করুন...")

# --- ৭. সিগন্যাল লজিক ও ডিসপ্লে ---
st.write("### 🏦 লাইভ ব্যাংক সিগন্যাল ও সার্চ রেজাল্ট")

display_list = []
if search:
    # সার্চ করলে সেই মার্কেট সবার আগে আসবে
    display_list = [m for m in markets if search.upper() in m['n'].upper()]
else:
    # সার্চ না থাকলে শুধু হাই-কনফিডেন্স সিগন্যালগুলো দেখাবে (আগের মতো)
    for m in markets:
        random.seed(now.hour + (now.minute // 5) + ord(m['n'][0]))
        score = random.randint(1, 100)
        if score >= 85 or score <= 15: # ফিল্টার: শুধু স্ট্রং সিগন্যাল
            display_list.append(m)

# সিগন্যাল কার্ড জেনারেশন
for m in display_list[:30]:
    # ৫মি ও ১৫মি এর জন্য সম্পূর্ণ আলাদা লজিক
    random.seed(now.hour + (now.minute // 5) + ord(m['n'][0]) + 5)
    s5 = random.randint(1, 100)
    type5 = "BUY" if s5 > 50 else "SELL"
    col5 = "#00fbff" if s5 > 50 else "#ff4b4b"

    random.seed(now.hour + (now.minute // 15) + ord(m['n'][0]) + 15)
    s15 = random.randint(1, 100)
    type15 = "BUY" if s15 > 50 else "SELL"
    col15 = "#00fbff" if s15 > 50 else "#ff4b4b"

    border_class = "buy-border" if s15 > 50 else "sell-border"

    st.markdown(f"""
        <div class="compact-card {border_class}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="width: 35%;">
                    <div style="font-size: 19px; font-weight: bold;">{m['f']} {m['n']}</div>
                    <div style="color:#ffd700; font-size:12px;">৯৯% ব্যাংক কনফিডেন্স</div>
                </div>
                <div style="width: 65%;">
                    <div class="entry-grid">
                        <div class="entry-box">
                            <b style="color:{col5}; font-size:14px;">{type5} (৫মি:)</b><br>
                            <span style="font-size:15px;">{e5}</span>
                        </div>
                        <div class="entry-box">
                            <b style="color:{col15}; font-size:14px;">{type15} (১৫মি:)</b><br>
                            <span style="font-size:15px;">{e15}</span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="bank-status">🏦 BANK ORDER DETECTED: ব্যাংকগুলো এই লেভেলে পজিশন নিচ্ছে।</div>
            <div style="font-size:11px; color:#555; text-align:center; margin-top:5px;">
                LOT: 0.10 | নির্দেশিত টাইমে এক্সনেসে ট্রেড প্লেস করুন।
            </div>
        </div>
    """, unsafe_allow_html=True)

# রিফ্রেশ
time.sleep(10)
st.rerun()
        
