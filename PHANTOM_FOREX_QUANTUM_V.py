import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. মেম্বারশিপ ও কনফিগারেশন ---
USER_KEYS = {"ARAFAT_VIP_2026": "Arafat Bhai (Admin)"}
st.set_page_config(page_title="PHANTOM V19 LOT-CALC", layout="wide")

if 'auth' not in st.session_state: st.session_state.auth = False

# --- ২. লগইন ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center;'>👻 PHANTOM V19</h1>", unsafe_allow_html=True)
    key_input = st.text_input("মাস্টার পাসওয়ার্ড দিন", type="password")
    if st.button("সিস্টেম আনলক করুন"):
        if key_input in USER_KEYS:
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- ৩. ডিজাইন (Lot Calculator UI) ---
st.markdown("""
    <style>
    .stApp { background-color: #010101; color: #ffffff; }
    .calc-card {
        border: 1px solid #333; border-radius: 15px; padding: 20px;
        background: linear-gradient(145deg, #0f0f0f, #1a1a1a);
        margin-bottom: 20px; border-left: 8px solid #ffd700;
    }
    .entry-box { background: #222; padding: 12px; border-radius: 10px; text-align: center; width: 48%; border: 1px solid #444; }
    .profit-text { color: #00ff00; font-size: 14px; font-weight: bold; margin-top: 5px; }
    .loss-text { color: #ff4b4b; font-size: 14px; margin-top: 2px; }
    .lot-input-style { background: #ffd700; color: #000; padding: 5px; border-radius: 5px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- ৪. লট ক্যালকুলেটর ইনপুট ---
st.markdown("<h3 style='text-align:center; color:#ffd700;'>LOT & PROFIT CALCULATOR</h3>", unsafe_allow_html=True)
user_lot = st.number_input("আপনি কত লট কিনতে চান? (Lot Size)", min_value=0.01, max_value=10.0, value=0.01, step=0.01)
st.info(f"আপনার সেট করা লট: {user_lot}। নিচের প্রফিট হিসাব এই লট অনুযায়ী দেখানো হচ্ছে।")

# --- ৫. টাইম ইঞ্জিন ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
e5, e15 = ( (now.minute // 5 + 1) * 5 ), ( (now.minute // 15 + 1) * 15 )

# --- ৬. মার্কেট ডিসপ্লে (আপনার লট অনুযায়ী লাভ/লস) ---
markets = [{"n": "GOLD (XAUUSD)", "f": "🟡"}, {"n": "EURUSD", "f": "🇪🇺🇺🇸"}, {"n": "GBPUSD", "f": "🇬🇧🇺🇸"}]

for m in markets:
    random.seed(now.hour + (now.minute // 5) + ord(m['n'][0]))
    
    # বেস প্রফিট (১ লটের জন্য)
    base_tp5 = random.uniform(10.0, 30.0)
    base_tp15 = random.uniform(40.0, 100.0)
    
    # আপনার লট অনুযায়ী আসল ডলার হিসাব
    actual_tp5 = round(base_tp5 * user_lot, 2)
    actual_sl5 = round(actual_tp5 * 0.4, 2)
    
    actual_tp15 = round(base_tp15 * user_lot, 2)
    actual_sl15 = round(actual_tp15 * 0.4, 2)

    st.markdown(f"""
        <div class="calc-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="width: 30%;">
                    <b style="font-size:18px;">{m['f']} {m['n']}</b><br>
                    <small style="color:#ffd700;">Lot: {user_lot}</small>
                </div>
                <div style="width: 70%; display: flex; justify-content: space-between;">
                    <div class="entry-box">
                        <b style="color:#00fbff;">BUY (৫মি)</b>
                        <div class="profit-text">লাভ: +${actual_tp5}</div>
                        <div class="loss-text">লস: -${actual_sl5}</div>
                    </div>
                    <div class="entry-box">
                        <b style="color:#ffd700;">DUAL (১৫মি)</b>
                        <div class="profit-text">লাভ: +${actual_tp15}</div>
                        <div class="loss-text">লস: -${actual_sl15}</div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

time.sleep(15)
st.rerun()
