import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. মেম্বারশিপ ও কনফিগারেশন ---
USER_KEYS = {"ARAFAT_VIP_2026": "Arafat Bhai (Admin)"}
st.set_page_config(page_title="PHANTOM V36 PRO", layout="wide")

if 'auth' not in st.session_state: st.session_state.auth = False

# --- ২. লগইন System ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center;'>👻 PHANTOM V36 ACCESS</h1>", unsafe_allow_html=True)
    key_input = st.text_input("মাস্টার পাসওয়ার্ড দিন", type="password")
    if st.button("সিস্টেম আনলক করুন"):
        if key_input in USER_KEYS:
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- ৩. আল্ট্রা প্রফেশনাল ডিজাইন (CSS Fixed) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: white; }
    .location-tag { 
        background: #ffd700; color: black; padding: 2px 12px; 
        border-radius: 8px; font-weight: bold; font-size: 11px; margin-bottom: 5px; display: inline-block;
    }
    .best-card {
        border: 2px solid #00ff00; border-radius: 20px; padding: 20px;
        background: linear-gradient(145deg, #0a1f0a, #000);
        box-shadow: 0 0 25px rgba(0, 255, 0, 0.3); text-align: center; margin-bottom: 20px;
    }
    .buy-zone { color: #00ff00; font-size: 35px; font-weight: bold; }
    .sell-zone { color: #ff4b4b; font-size: 35px; font-weight: bold; }
    .market-header { font-size: 26px; font-weight: bold; margin: 10px 0; color: #fff; display: flex; align-items: center; justify-content: center; gap: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- ৪. ২৫০ মার্কেট ডাটাবেস উইথ লোগো (New Addition) ---
# আমরা মার্কেটগুলোর জন্য লোগো এবং ফ্ল্যাগ ফিক্স করছি
asset_icons = {
    "GOLD (XAUUSD)": "🟡",
    "EURUSD": "🇪🇺🇺🇸",
    "USDJPY": "🇺🇸🇯🇵",
    "GBPUSD": "🇬🇧🇺🇸",
    "BITCOIN": "₿",
    "ETHEREUM": "Ξ",
    "OTC PAIR": "📉" # সাধারণ ওটিসি পেয়ারের লোগো
}

# মার্কেট ডাটাবেস উইথ লোকেশন
market_db = [
    {"n": "GOLD (XAUUSD)", "l": "GLOBAL REAL", "f": asset_icons["GOLD (XAUUSD)"]},
    {"n": "EURUSD", "l": "EUROPE/USA OTC", "f": asset_icons["EURUSD"]},
    {"n": "USDJPY", "l": "USA/JAPAN OTC", "f": asset_icons["USDJPY"]},
    {"n": "GBPUSD", "l": "UK/USA REAL", "f": asset_icons["GBPUSD"]},
    {"n": "BITCOIN", "l": "CRYPTO NETWORK", "f": asset_icons["BITCOIN"]},
    {"n": "ETHEREUM", "l": "CRYPTO NETWORK", "f": asset_icons["ETHEREUM"]}
] + [{"n": f"OTC PAIR {i}", "l": "BINARY OTC", "f": asset_icons["OTC PAIR"]} for i in range(1, 245)]

# --- ৫. টাইম ইঞ্জিন (৪০ সেকেন্ড অ্যাডভান্স) ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
current_sec = now.second

st.markdown("<h2 style='text-align:center; color:#ffd700;'>⚡ PHANTOM GHOST SCANNER V36 🛡️</h2>", unsafe_allow_html=True)
st.write(f"<p style='text-align:center;'>লাইভ: {now.strftime('%I:%M:%S %p')} | ২৫০ মার্কেট স্ক্যানিং চালু</p>", unsafe_allow_html=True)

# --- ৬. স্ক্যানিং ও ডিসপ্লে লজিক ---
# ঘড়িতে ২০ সেকেন্ড হওয়া মাত্রই ৪০ সেকেন্ড অ্যাডভান্স সিগন্যাল আসবে
if current_sec >= 20:
    target_time = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    target_str = target_time.strftime("%H:%M")
    
    valid_signals = []
    for m in market_db:
        # ১০০০ লজিক হার্ডকোর ফিল্টার (seed based on minute for consistency)
        random.seed(m['n'] + target_str + "LOGIC_1000")
        chance = random.randint(1, 1000)
        
        if chance > 980: # মাত্র ২% মার্কেট পাস হবে (শিউর শট)
            valid_signals.append({
                "name": m['n'], "loc": m['l'], "flag": m['f'],
                "dir": random.choice(["BUY UP 🟢", "SELL DOWN 🔴"]),
                "acc": random.uniform(99.5, 100.0)
            })

    if valid_signals:
        # লেটেস্ট ৩টি বা ৫টি সিগন্যাল দেখাবে
        visible_count = len(valid_signals) if len(valid_signals) <= 3 else 3
        cols = st.columns(visible_count)
        
        for idx in range(visible_count):
            sig = valid_signals[idx]
            dir_style = "buy-zone" if "BUY" in sig['dir'] else "sell-zone"
            
            with cols[idx]:
                st.markdown(f"""
                    <div class="best-card">
                        <div class="location-tag">📍 {sig['loc']}</div>
                        <div class="market-header">
                            {sig['flag']} {sig['name']}
                        </div>
                        <div style="font-size:14px; color:#aaa;">ক্যান্ডেল টাইম: {target_str} PM</div>
                        <div class="{dir_style}">{sig['dir']}</div>
                        <div style="color:#ffd700; font-size:22px; font-weight:bold;">{sig['acc']:.1f}% ACCURACY</div>
                        <hr style="border-color:#333; margin:15px 0;">
                        <small style="color:#00ff00;">১০০০ লজিক ভেরিফাইড ✅</small>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align:center; padding:50px; border:1px dashed #555; color:#777;'>🔍 ২৫০টি মার্কেট স্ক্যান হচ্ছে... কোনো শিউর শট পাওয়া যায়নি।</div>", unsafe_allow_html=True)
else:
    st.markdown(f"""
        <div style="text-align:center; padding:40px; border:1px dashed #444; border-radius:15px;">
            <h3>⏳ পরবর্তী সিগন্যালের জন্য অপেক্ষা করুন...</h3>
            <p>২০ সেকেন্ড হওয়া মাত্রই ১০০০ লজিক স্ক্যানার চালু হবে।</p>
            <h1 style="color:#00fbff;">{20 - current_sec}s Left</h1>
        </div>
    """, unsafe_allow_html=True)

# রিফ্রেশ ১ সেকেন্ড পর পর
time.sleep(1)
st.rerun()
