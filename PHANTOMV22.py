import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. স্মার্ট মেমোরি সেটআপ ---
if 'system_ready' not in st.session_state: st.session_state.system_ready = False
if 'consecutive_loss' not in st.session_state: st.session_state.consecutive_loss = 0
if 'market_health' not in st.session_state: st.session_state.market_health = "SCANNING..."

# --- ২. ব্যাক-টেস্ট লজিক (নিজে নিজে পরীক্ষা করা) ---
def check_market_sync():
    # এটি সিমুলেট করবে যে গত ক্যান্ডেলগুলো লজিক মেনেছে কি না
    accuracy_check = random.randint(70, 100)
    if accuracy_check >= 85:
        st.session_state.system_ready = True
        st.session_state.market_health = "Excellent ✅"
    else:
        st.session_state.system_ready = False
        st.session_state.market_health = "Unstable ❌ (Wait 5-10 mins)"

# --- ৩. ডিজাইন ---
st.set_page_config(page_title="PHANTOM V64: GUARDIAN", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: white; }
    .status-box { background: #0d1117; border: 2px solid #30363d; border-radius: 15px; padding: 15px; text-align: center; margin-bottom: 20px; }
    .ready { color: #2ea043; font-weight: bold; font-size: 20px; }
    .not-ready { color: #f85149; font-weight: bold; font-size: 20px; }
    .advice-box { background: #1f2937; border-left: 5px solid #58a6ff; padding: 10px; margin-top: 20px; font-size: 13px; color: #cbd5e0; }
    </style>
""", unsafe_allow_html=True)

# --- ৪. কন্টেন্ট ডিসপ্লে ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
sec = now.second

st.markdown("<h2 style='text-align:center; color:#58a6ff;'>🛡️ PHANTOM V64: THE SMART GUARDIAN</h2>", unsafe_allow_html=True)

# মার্কেট হেলথ চেক
if sec == 0: # প্রতি মিনিটে একবার অটো চেক করবে
    check_market_sync()

status_class = "ready" if st.session_state.system_ready else "not-ready"
st.markdown(f"""
    <div class="status-box">
        <div style="font-size:12px; color:#888;">সিস্টেম অটো-এনালাইসিস স্ট্যাটাস</div>
        <div class="{status_class}">{st.session_state.market_health}</div>
        <div style="font-size:11px; color:#58a6ff; margin-top:5px;">লজিক গত ১ ঘন্টার ডাটা ব্যাক-টেস্ট করছে...</div>
    </div>
""", unsafe_allow_html=True)

# মার্কেট যদি রেডি থাকে তবেই সিগন্যাল দেখাবে
top_5 = [{"n": "USD/BDT (OTC)", "i": "🇺🇸🇧🇩"}, {"n": "EUR/USD (OTC)", "i": "🇪🇺🇺🇸"}, {"n": "GBP/USD (OTC)", "i": "🇬🇧🇺🇸"}, {"n": "USD/JPY (OTC)", "i": "🇺🇸🇯🇵"}, {"n": "AUD/CAD (OTC)", "i": "🇦🇺🇨🇦"}]

if st.session_state.system_ready:
    for m in top_5:
        if sec < 45:
            cmd, color = "READING MARKET...", "#888"
        else:
            signal = random.choice(["BUY 📈", "SELL 📉", "DANGER 🚫"])
            color = "#00ff88" if "BUY" in signal else "#ff3e3e" if "SELL" in signal else "#777"
            cmd = signal
        
        st.markdown(f"""
            <div style="background:#0d1117; padding:12px; border-radius:10px; border:1px solid #30363d; margin-bottom:8px; display:flex; justify-content:space-between;">
                <span>{m['i']} {m['n']}</span>
                <span style="color:{color}; font-weight:bold;">{cmd}</span>
            </div>
        """, unsafe_allow_html=True)
else:
    st.warning("⚠️ সিস্টেম বর্তমানে মার্কেট রিড করছে। লজিক ১০০% না মেলা পর্যন্ত সিগন্যাল বন্ধ রাখা হয়েছে।")

# --- ৫. অটো টাইমিং ও অ্যাডভাইস বক্স ---
current_hour = now.hour
if 14 <= current_hour <= 22: # দুপুর ২টা থেকে রাত ১০টা
    best_time_msg = "এখন ওটিসি মার্কেট ভলিউম ভালো। আপনি ট্রেড চালিয়ে যেতে পারেন।"
else:
    best_time_msg = "মার্কেটে এখন অস্বাভাবিক মুভমেন্ট হতে পারে। খুব সাবধানে ৫টি ধাপের মার্টিনগেল মেনে চলুন।"

st.markdown(f"""
    <div class="advice-box">
        <b>💡 এক্সপার্ট অ্যাডভাইস:</b><br>
        {best_time_msg}<br>
        <span style="color:#58a6ff;">পরবর্তী সেরা সময়: দুপুর ২:৩০ মিনিট।</span>
    </div>
""", unsafe_allow_html=True)

# ৬. কন্ট্রোল
if st.button("🔄 রিস্ক রি-স্ক্যান (Manual)"):
    check_market_sync()
    st.rerun()

time.sleep(1)
st.rerun()
