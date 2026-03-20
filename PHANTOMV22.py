import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. পেজ সেটআপ ---
st.set_page_config(page_title="PHANTOM V47", layout="centered")

# --- ২. লগইন ---
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.title("👻 PHANTOM V47")
    key = st.text_input("পাসওয়ার্ড দিন", type="password")
    if st.button("আনলক"):
        if key == "ARAFAT_VIP_2026":
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- ৩. টাইম ইঞ্জিন ---
tz = pytz.timezone('Asia/Dhaka')
now = datetime.now(tz)
seed_time = now.replace(minute=(now.minute // 4) * 4, second=0, microsecond=0)
random.seed(seed_time.strftime("%Y-%m-%d %H:%M"))

st.subheader("🛡️ PHANTOM V47 MASTER SCANNER")
st.write(f"সময়: {now.strftime('%I:%M:%S %p')}")
st.divider()

# মার্কেট ডাটা
pairs = [
    {"n": "USD/BDT (OTC)", "i": "🇺🇸🇧🇩"},
    {"n": "EUR/USD (OTC)", "i": "🇪🇺🇺🇸"},
    {"n": "USD/JPY (OTC)", "i": "🇺🇸🇯🇵"},
    {"n": "GBP/USD (OTC)", "i": "🇬🇧🇺🇸"}
]

# ৪ মিনিটের জন্য ৩টি সিগন্যাল
selected = random.sample(pairs, 3)

# --- ৪. ডিসপ্লে (কোডিং ছাড়া সরাসরি ডিজাইন) ---
for sig in selected:
    # টাইম ক্যালকুলেশন
    t1 = (seed_time + timedelta(minutes=1)).strftime("%H:%M")
    t2 = (seed_time + timedelta(minutes=2)).strftime("%H:%M")
    t3 = (seed_time + timedelta(minutes=3)).strftime("%H:%M")
    
    direction = random.choice(["UP 🟢", "DOWN 🔴"])
    
    # কন্টেইনার দিয়ে ডিজাইন
    with st.container(border=True):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"### {sig['i']} {sig['n']}")
        with col2:
            st.markdown(f"## {direction}")
        
        # ৩টি ধাপ
        st.info(f"**STEP 1 (Main):** {t1} মিনিটে এন্ট্রি নিন")
        st.warning(f"**STEP 2 (MTG-1):** {t2} (লস হলে ডাবল)")
        st.error(f"**STEP 3 (MTG-2):** {t3} (শেষ রিকভারি শট)")
        
        # টাইমার
        expiry = seed_time + timedelta(minutes=4)
        rem = int((expiry - now).total_seconds())
        st.write(f"⏳ নতুন সিগন্যাল আসবে: {rem // 60:02}:{rem % 60:02}s")

# অটো রিফ্রেশ
time.sleep(1)
st.rerun()
