import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import random

# --- ১. মেম্বারশিপ ও কনফিগারেশন ---
USER_KEYS = {"ARAFAT_VIP_2026": "Arafat Bhai (Admin)"}
st.set_page_config(page_title="PHANTOM V34 LOCATION TRACKER", layout="wide")

if 'auth' not in st.session_state: st.session_state.auth = False

# --- ২. লগইন ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center;'>👻 PHANTOM V34</h1>", unsafe_allow_html=True)
    key = st.text_input("মাস্টার পাসওয়ার্ড দিন", type="password")
    if st.button("সিস্টেম আনলক"):
        if key in USER_KEYS:
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- ৩. আল্ট্রা প্রফেশনাল ডিজাইন ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: white; }
    .location-tag { 
        background: #ffd700; color: black; padding: 2px 10px; 
        border-radius: 5px; font-weight: bold; font-size: 12px; margin-bottom: 5px;
    }
    .best-card {
        border: 2px solid #00ff00; border-radius: 20px; padding: 20px;
        background: linear-gradient(145deg, #0a140a, #000);
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.2); text-align: center;
    }
    .buy-text { color: #00ff00; font-size: 35px; font-weight: bold; }
    .sell-text { color: #ff4b4b; font-size: 35px; font-weight: bold; }
    
