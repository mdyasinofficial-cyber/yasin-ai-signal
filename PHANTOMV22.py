import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. মেম্বারশিপ ও কনফিগারেশন ---
USER_KEYS = {"ARAFAT_VIP_2026": "Arafat Bhai (Admin)"}
st.set_page_config(page_title="PHANTOM V35 PRO", layout="wide")

if 'auth' not in st.session_state: 
    st.session_state.auth = False

# --- ২. লগইন সিস্টেম ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center;'>👻 PHANTOM V35</h1>", unsafe_allow_html=True)
    key = st.text_input("মাস্টার পাসওয়ার্ড দিন", type="password")
    if st.button("সিস্টেম আনলক"):
        if key in USER_KEYS:
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- ৩. আল্ট্রা প্রফেশনাল ডিজাইন (CSS Error-Free) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: white; }
    .location-tag { 
        background: #ffd700; color: black; padding: 2px 10px; 
        border-radius: 5px; font-weight: bold; font-size: 11px; margin-bottom: 5px; display: inline-block;
    }
    .best-card {
        border: 2px solid #00ff00; border-radius: 15px; padding: 15px;
        background: linear-gradient(145deg, #0a140a, #000);
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.2); text-align: center; margin-bottom: 15px;
    }
    .buy-text { color: #00ff00; font-size: 30px; font-weight: bold; }
    .sell-text { color: #ff4b4b; font-size: 30px; font-weight: bold; }
    .market-header { font-size: 20px; font-weight: bold; margin: 5px 0; color: #fff; }
    .scan-box { border: 1px dashed #444; padding: 30px; text-align: center; border-radius: 15px; color: #888; }
    </style>
""", unsafe_allow_html=True)

# --- ৪. ২৫০ মার্কেট ডা
