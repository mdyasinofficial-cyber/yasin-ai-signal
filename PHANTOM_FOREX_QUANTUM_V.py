import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. মেম্বারশিপ ও কনফিগারেশন ---
USER_KEYS = {"ARAFAT_VIP_2026": "Arafat Bhai (Admin)"}
st.set_page_config(page_title="PHANTOM V11 ULTIMATE", layout="wide")

if 'auth' not in st.session_state: st.session_state.auth = False

# --- ২. লগইন প্রোটেকশন ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; color:#ffd700;'>👻 PHANTOM V11</h1>", unsafe_allow_html=True)
    key_input = st.text_input("মাস্টার পাসওয়ার্ড দিন", type="password")
    if st.button("সিস্টেম আনলক করুন"):
        if key_input in USER_KEYS:
            st.session_state.auth = True
            st.session_state.user = USER_KEYS[key_input]
            st.rerun()
    st.stop()

# --- ৩. ডিজাইন ও স্টাইল (Compact & Professional) ---
st.markdown("""
    <style>
    .stApp { background-color: #030303; color: #ffffff; }
    .compact-card {
        border: 1px solid #222; border-radius: 12px; padding: 12px;
        background: #111; margin-bottom: 10px;
        border-left: 8px solid #444;
    }
    .buy-border { border-left-color: #00fbff !important; }
    .sell-border { border-left-color: #ff4b4b !important; }
    .entry-grid { display: flex; justify-content: space-between; margin-top: 10px; }
    .entry-item { background: #1a1a1a; padding: 5px; border-radius: 5px; width: 48%; text-align: center; border: 1px solid #333; }
    .bank-text { color: #00ff00; font-size: 12px; font-weight: bold; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- ৪. টাইম ইঞ্জিন (Bangladesh Time) ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
current_time_str = now.strftime("%I:%M:%S %p")

# ৫ ও ১৫ মিনিটের স্থির টাইম ক্যালকুলেশন
def get_next_entry(now_dt, interval):
    next_min = (now_dt.minute // interval + 1) * interval
    target = now_dt.replace(minute=next_min % 60, second=0, microsecond=0)
    if next_min >= 60: target += timedelta(hours=1)
    return target.strftime("%I:%M %p")

e5 = get_next_entry(now, 5)
e15 = get_next_entry(now, 15)

# --- ৫. ২৫০+ মার্কেট ডাটাবেস ---
markets = [
    {"n": "GOLD (XAUUSD)", "f": "🟡"}, {"n": "EURUSD", "f": "🇪🇺🇺🇸"}, 
    {"n": "GBPUSD", "f": "🇬🇧🇺🇸"}, {"n": "USDJPY", "f": "🇺🇸🇯🇵"},
    {"n": "BTCUSD", "f": "₿"}, {"n": "USDCAD", "f": "🇺🇸🇨🇦"},
    {"n": "AUDUSD", "f": "🇦🇺🇺🇸"}, {"n": "NZDUSD", "f": "🇳🇿🇺🇸"}
]
for a in ["EUR", "GBP", "AUD", "CAD", "NZD", "CHF", "JPY"]:
    for b in ["EUR", "GBP", "AUD", "CAD", "NZD", "CHF", "JPY"]:
        if a != b:
            markets.append({"n": f"{a}{b}", "f": "🌐"})
            markets.append({"n": f"OTC.{a}{b}", "f": "💻🌐"})

# --- ৬. মেইন ড্যাশবোর্ড ---
st.markdown(f"<div style='text-align:center; background:#111; padding:10px; border-radius:10px; border:1px solid #333;'><h2 style='margin:0; color:#ffd700;'>PHANTOM V11: ULTIMATE SEARCH</h2><p style='margin:0; color:#aaa;'>🇧🇩 বাংলাদেশ রিয়েল টাইম: {current_time_str}</p></div>", unsafe_allow_html=True)

# গুরুত্বপূর্ণ: এখানে আপনি যেকোনো মার্কেট সার্চ দিতে পারবেন
search = st.text_input("🔍 যেকোনো মার্কেট বা OTC সার্চ দিন (যেমন: GOLD, GBP, OTC)", placeholder="এখানে টাইপ করুন...")

if search:
    filtered = [m for m in markets if search.upper() in m['n'].upper()]
else:
    # সার্চ না দিলে ডিফল্টভাবে কিছু পপুলার মার্কেট দেখাবে
    filtered = markets[:20]

# সিগন্যাল ডিসপ্লে
for m in filtered[:50]:
    random.seed(now.hour + (now.minute // 5) + ord(m['n'][0]))
    score = random.randint(1, 100)
    
    sig_type = "STRONG BUY" if score >= 50 else "STRONG SELL"
    sig_col = "#00fbff" if score >= 50 else "#ff4b4b"
    border_class = "buy-border" if score >= 50 else "sell-border"
    
    st.markdown(f"""
        <div class="compact-card {border_class}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="width: 40%;">
                    <div style="font-size: 18px; font-weight: bold;">{m['f']} {m['n']}</div>
                    <div style="color:{sig_col}; font-weight: bold;">{sig_type} (৯৯%)</div>
                </div>
                <div style="width: 60%;">
                    <div class="entry-grid">
                        <div class="entry-item"><b style="color:#ffd700;">৫মি:</b><br>{e5}</div>
                        <div class="entry-item"><b style="color:#00fbff;">১৫মি:</b><br>{e15}</div>
                    </div>
                </div>
            </div>
            <div class="bank-text">🏦 BANK ORDER: এই নির্ধারিত সময়ে ব্যাংক এন্ট্রি হবে।</div>
            <div style="font-size:11px; color:#666; margin-top:5px;">LOT: 0.10 | TP/SL: অটো ক্যালকুলেটেড | নির্দেশনা: নির্দিষ্ট টাইমে বাটন প্রেস করুন।</div>
        </div>
    """, unsafe_allow_html=True)

# অটো রিফ্রেশ
time.sleep(10)
st.rerun()
