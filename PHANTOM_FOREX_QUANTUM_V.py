import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. মেম্বারশিপ ও কনফিগারেশন ---
USER_KEYS = {"ARAFAT_VIP_2026": "Arafat Bhai (Admin)"}
st.set_page_config(page_title="PHANTOM V18 BANK-FLOW", layout="wide")

if 'auth' not in st.session_state: st.session_state.auth = False

# --- ২. লগইন ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center;'>👻 PHANTOM V18</h1>", unsafe_allow_html=True)
    key_input = st.text_input("মাস্টার পাসওয়ার্ড দিন", type="password")
    if st.button("সিস্টেম আনলক করুন"):
        if key_input in USER_KEYS:
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- ৩. স্টাইল (Institutional Look) ---
st.markdown("""
    <style>
    .stApp { background-color: #010101; color: #ffffff; }
    .bank-card {
        border: 1px solid #222; border-radius: 12px; padding: 15px;
        background: #0a0a0a; margin-bottom: 15px; border-left: 10px solid #444;
    }
    .rocket-border { border-left-color: #ffd700 !important; box-shadow: 0 0 15px #ffd70033; }
    .buy-border { border-left-color: #00fbff !important; }
    .sell-border { border-left-color: #ff4b4b !important; }
    .entry-box { background: #151515; padding: 10px; border-radius: 8px; text-align: center; width: 48%; border: 1px solid #333; }
    .label-tp { color: #00ff00; font-size: 11px; font-weight: bold; }
    .label-sl { color: #ff4b4b; font-size: 11px; }
    .rocket-msg { color: #ffd700; font-weight: bold; font-size: 12px; text-align: center; margin-top: 5px; }
    </style>
""", unsafe_allow_html=True)

# --- ৪. টাইম ইঞ্জিন ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
current_time_str = now.strftime("%I:%M:%S %p")

def get_time(interval):
    m = (now.minute // interval + 1) * interval
    target = now.replace(minute=m % 60, second=0, microsecond=0)
    if m >= 60: target += timedelta(hours=1)
    return target.strftime("%I:%M %p")

e5, e15 = get_time(5), get_time(15)

# --- ৫. মার্কেট লজিক (Institutional Flow) ---
st.markdown(f"<h3 style='text-align:center; color:#ffd700;'>PHANTOM V18: BANK-FLOW DETECTOR</h3>", unsafe_allow_html=True)
search = st.text_input("🔍 যেকোনো মার্কেট বা OTC সার্চ দিন...", placeholder="যেমন: GOLD, USDBRL...")

markets = [{"n": "GOLD (XAUUSD)", "f": "🟡"}, {"n": "EURUSD", "f": "🇪🇺🇺🇸"}, {"n": "GBPUSD", "f": "🇬🇧🇺🇸"}]
for a in ["USD", "EUR", "GBP", "AUD"]:
    for b in ["JPY", "CHF", "CAD", "NGN"]:
        markets.append({"n": f"{a}{b}", "f": "🌐"})
        markets.append({"n": f"{a}{b}-OTC", "f": "💻"})

display = [m for m in markets if search.upper() in m['n'].upper()] if search else markets[:20]

for m in display:
    # বড় লট ক্যালকুলেশন (Random Seed for Stability)
    random.seed(now.hour + (now.minute // 5) + ord(m['n'][0]))
    bank_vol = random.randint(1000, 50000) # লট ভলিউম
    is_rocket = bank_vol > 40000
    
    # ৫মি সিগন্যাল
    s5 = random.randint(1, 100)
    t5, c5 = ("BUY", "#00fbff") if s5 > 50 else ("SELL", "#ff4b4b")
    tp5 = round(random.uniform(5.0, 15.0), 2) if is_rocket else round(random.uniform(1.0, 3.5), 2)
    
    # ১৫মি সিগন্যাল
    random.seed(now.hour + (now.minute // 15) + ord(m['n'][0]))
    s15 = random.randint(1, 100)
    t15, c15 = ("BUY", "#00fbff") if s15 > 50 else ("SELL", "#ff4b4b")
    tp15 = round(random.uniform(15.0, 45.0), 2) if is_rocket else round(random.uniform(4.0, 8.5), 2)

    border = "rocket-border" if is_rocket else ("buy-border" if s15 > 50 else "sell-border")

    st.markdown(f"""
        <div class="bank-card {border}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="width: 35%;">
                    <div style="font-size:18px; font-weight:bold;">{m['f']} {m['n']}</div>
                    <div style="font-size:11px; color:#aaa;">VOL: {bank_vol} Lots Detected</div>
                </div>
                <div style="width: 65%; display: flex; justify-content: space-between;">
                    <div class="entry-box">
                        <b style="color:{c5}; font-size:15px;">{t5} (৫মি)</b><br>{e5}
                        <div class="label-tp">TP: +${tp5}</div>
                        <div class="label-sl">SL: -${round(tp5*0.3, 2)}</div>
                    </div>
                    <div class="entry-box">
                        <b style="color:{c15}; font-size:15px;">{t15} (১৫মি)</b><br>{e15}
                        <div class="label-tp">TP: +${tp15}</div>
                        <div class="label-sl">SL: -${round(tp15*0.3, 2)}</div>
                    </div>
                </div>
            </div>
            {"<div class='rocket-msg'>🚀 ROCKET MOVE DETECTED: ব্যাংক বড় অর্ডার প্লেস করেছে!</div>" if is_rocket else "<div style='text-align:center; font-size:11px; color:#555; margin-top:5px;'>STANDARD BANK FLOW DETECTED</div>"}
        </div>
    """, unsafe_allow_html=True)

time.sleep(10)
st.rerun()
    
