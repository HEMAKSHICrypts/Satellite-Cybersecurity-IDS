import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import time
import requests

# Page config
st.set_page_config(
    page_title="Satellite Defense Dashboard",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0a0f1e;
    }
    .attack-alert {
        background-color: #ff000020;
        border-left: 4px solid #ff0000;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .normal-alert {
        background-color: #00ff0020;
        border-left: 4px solid #00ff00;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛰️ AI-Powered Satellite Defense System")
st.caption("Real-time Anomaly Detection | Adaptive Cyber Defense")

# Sidebar
with st.sidebar:
    st.header("🎮 System Controls")
    self_healing = st.toggle("🛡️ Self-Healing Mode", value=True)
    security_level = st.select_slider("🔒 Security Level", ["LOW", "MEDIUM", "HIGH", "MAXIMUM"], value="MEDIUM")
    st.divider()
    
    # Check satellite health
    try:
        health = requests.get('http://localhost:5000/health', timeout=2)
        if health.status_code == 200:
            st.success("🟢 Satellite: ONLINE")
        else:
            st.error("🔴 Satellite: OFFLINE")
    except:
        st.error("🔴 Satellite: OFFLINE (Start satellite.py first)")

# Main metrics
col1, col2, col3, col4 = st.columns(4)
current_risk = random.uniform(-0.8, 0.2)

def get_risk_level(score):
    if score < -0.6:
        return "🚨 CRITICAL", "#ff0000"
    elif score < -0.4:
        return "⚠️ HIGH", "#ff6600"
    elif score < -0.2:
        return "📊 MEDIUM", "#ffcc00"
    else:
        return "✅ LOW", "#00ff00"

risk_text, risk_color = get_risk_level(current_risk)

col1.metric("📊 Current Risk Score", f"{current_risk:.2f}")
col2.metric("🚨 Risk Level", risk_text)
col3.metric("🌍 Active Threats", "3")
col4.metric("⚡ Commands/Min", "142")

# Anomaly chart
st.subheader("📈 Anomaly Detection Timeline")
timeline_data = pd.DataFrame({
    "timestamp": pd.date_range(start="2024-01-01 00:00:00", periods=100, freq="1min"),
    "anomaly_score": [random.uniform(-1, 0.5) for _ in range(100)],
})

fig = px.line(timeline_data, x="timestamp", y="anomaly_score", title="Real-time Anomaly Score")
fig.add_hline(y=-0.6, line_dash="dash", line_color="red", annotation_text="CRITICAL")
fig.add_hline(y=-0.4, line_dash="dash", line_color="orange", annotation_text="HIGH")
fig.update_layout(plot_bgcolor="#0f1422", paper_bgcolor="#0f1422", font_color="#e0e0e0")
st.plotly_chart(fig, use_container_width=True)

# Live command feed
st.subheader("📡 Live Command Feed")
commands = [
    {"time": "10:00:32", "cmd": "CAPTURE_IMAGE", "origin": "INDIA", "verdict": "✅ NORMAL", "score": -0.12},
    {"time": "10:00:45", "cmd": "TRANSMIT_DATA", "origin": "INDIA", "verdict": "✅ NORMAL", "score": -0.08},
    {"time": "10:01:28", "cmd": "ROTATE", "origin": "UNKNOWN", "verdict": "🚨 ATTACK", "score": -0.72},
]

for cmd in commands:
    if "ATTACK" in cmd["verdict"]:
        st.markdown(f'<div class="attack-alert">🕒 {cmd["time"]} | {cmd["cmd"]} | 🌍 {cmd["origin"]} | {cmd["verdict"]} | Score: {cmd["score"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="normal-alert">🕒 {cmd["time"]} | {cmd["cmd"]} | 🌍 {cmd["origin"]} | {cmd["verdict"]} | Score: {cmd["score"]}</div>', unsafe_allow_html=True)

st.caption("🔄 Dashboard auto-refreshes every 10 seconds")
time.sleep(10)
st.rerun()