import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

st.set_page_config(
    page_title="Lab Environment Monitor",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_sensor_data():
    now = datetime.now()
    temp = np.random.uniform(22.0, 24.5)
    hum = np.random.uniform(45.0, 55.0)
    press = np.random.uniform(1012.0, 1013.5)
    return {
        "timestamp": now.strftime("%H:%M:%S"),
        "suhu": round(temp, 1),
        "kelembapan": round(hum, 1),
        "tekanan": round(press, 1)
    }

if 'history' not in st.session_state:
    st.session_state['history'] = pd.DataFrame(columns=["timestamp", "suhu", "kelembapan", "tekanan"])

st.markdown("""
    <style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.title("⚙️ Pengaturan")
st.sidebar.markdown("---")

st.sidebar.header("🎵 Background Music")
st.sidebar.info("Browsers mungkin memblokir putar otomatis. Gunakan tombol play di bawah.")

music_file_url = st.sidebar.text_input(
    "Masukkan Link Lagu (URL/MP3)", 
    value="https://soundcloud.com/sweet-medicine/sweet-medicine-dreamin?in=lofi-hip-hop-music/sets/lofi-lofi&utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing" 
)

music_title_input = st.sidebar.text_input("Judul Lagu Saat Ini", value="Lo-Fi Study Beat")
music_artist_input = st.sidebar.text_input("Nama Artist", value="Unknown Artist")

if music_file_url:
    st.sidebar.markdown(f"**Sekarang Memutar:** {music_title_input} - {music_artist_input}")
    st.sidebar.audio(music_file_url, format='audio/mp3', loop=True, autoplay=False)
else:
    st.sidebar.warning("Masukkan link lagu terlebih dahulu.")

refresh_data = st.sidebar.button("🔄 Update Data Sekarang")

st.title("🧪 Laboratory Monitoring System")
st.markdown("### Kondisi Lingkungan Laboratorium")

col1, col2, col3 = st.columns(3)

current_data = get_sensor_data()

with col1:
    st.metric(
        label="🌡️ Suhu (Temperature)",
        value=f"{current_data['suhu']} °C",
        delta="Normal" if 20 <= current_data['suhu'] <= 26 else "Waspada"
    )

with col2:
    st.metric(
        label="💧 Kelembapan (Humidity)",
        value=f"{current_data['kelembapan']} %",
        delta="Normal" if 40 <= current_data['kelembapan'] <= 60 else "Waspada"
    )

with col3:
    st.metric(
        label="⚖️ Tekanan (Pressure)",
        value=f"{current_data['tekanan']} hPa",
        delta="-0.5 hPa" # Contoh simulasi delta
    )

st.markdown("### 📈 Grafik Historik Sensor")

if refresh_data:
    new_row = pd.DataFrame([current_data])
    st.session_state['history'] = pd.concat([st.session_state['history'], new_row], ignore_index=True)
    
    if len(st.session_state['history']) > 20:
        st.session_state['history'] = st.session_state['history'].tail(20)

if not st.session_state['history'].empty:
    chart_data = st.session_state['history'].set_index("timestamp")
    st.line_chart(chart_data)
else:
    st.write("Tekan tombol **Update Data Sekarang** di sidebar untuk melihat grafik bergerak.")

st.markdown("---")
if current_data['suhu'] > 26:
    st.error("⚠️ PERINGATAN: Suhu laboratorium terlalu tinggi!")
elif current_data['kelembapan'] < 30:
    st.warning("⚠️ PERINGATAN: Kelembapan terlalu rendah!")
else:
    st.success("✅ Kondisi Laboratorium Stabil.")
