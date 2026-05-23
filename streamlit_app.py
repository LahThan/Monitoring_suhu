import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="Lab Environment Monitor",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

audio_html = """
<style>
    #audio-player-container {
        display: none; /* Sembunyikan controls default */
    }
</style>
"""

if 'history' not in st.session_state:
    st.session_state['history'] = pd.DataFrame(columns=["timestamp", "suhu", "kelembapan", "tekanan"])

def get_sensor_data():
    temp = np.random.uniform(22.0, 24.5)
    hum = np.random.uniform(45.0, 55.0)
    press = np.random.uniform(1012.0, 1013.5)
    return {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "suhu": round(temp, 1),
        "kelembapan": round(hum, 1),
        "tekanan": round(press, 1)
    }

st.sidebar.title("⚙️ Pengaturan")
st.sidebar.markdown("---")

st.sidebar.header("🎵 Background Music")

music_url = st.sidebar.text_input(
    "Link Lagu (URL/MP3)", 
    value="https://soundcloud.com/shllw-1/303-pm?utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing"
)

music_title = st.sidebar.text_input("Judul Lagu", value="しゃろう(Sharou)")
music_artist = st.sidebar.text_input("Artist", value="Relaxing Studio")

st.sidebar.markdown("---")

st.title("🧪 Laboratory Monitoring System")
st.markdown("### Kondisi Lingkungan Laboratorium")

col1, col2, col3 = st.columns(3)
data = get_sensor_data()

with col1:
    st.metric("🌡️ Suhu", f"{data['suhu']} °C")
with col2:
    st.metric("💧 Kelembapan", f"{data['kelembapan']} %")
with col3:
    st.metric("⚖️ Tekanan", f"{data['tekanan']} hPa")

st.markdown("### 📈 Grafik Historik")

if st.sidebar.button("🔄 Update Data"):
    new_row = pd.DataFrame([data])
    st.session_state['history'] = pd.concat([st.session_state['history'], new_row], ignore_index=True)
    if len(st.session_state['history']) > 20:
        st.session_state['history'] = st.session_state['history'].tail(20)

if not st.session_state['history'].empty:
    chart = st.session_state['history'].set_index("timestamp")
    st.line_chart(chart)

st.markdown("---")
if data['suhu'] > 26:
    st.error("⚠️ SuhuLAB Tinggi!")
elif data['kelembapan'] < 30:
    st.warning("⚠️ Kelembapan Rendah!")
else:
    st.success("✅ Kondisi Stabil.")

if music_url:
    st.audio(music_url, format='audio/mp3', loop=True, autoplay=True)
    
    st.sidebar.markdown("---")
    st.sidebar.success(f"🎶 Sedang Memutar: {music_title}")
