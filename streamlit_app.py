import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="Lab Environment Monitor",
    page_icon="🧪",
    layout="wide"
)

st.markdown("""
    <style>
    .stAudio {
        display: none !important;
    }
    div[data-testid="stAudio"] {
        display: none !important;
        height: 0 !important;
    }
    .music-info {
        background-color: #1E1E1E;
        padding: 10px;
        border-radius: 8px;
        color: #00FF00;
        font-family: monospace;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'history' not in st.session_state:
    st.session_state['history'] = pd.DataFrame(columns=["timestamp", "suhu", "kelembapan", "tekanan"])
if 'music_playing' not in st.session_state:
    st.session_state['music_playing'] = False

def get_sensor_data():
    return {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "suhu": round(np.random.uniform(22.0, 24.5), 1),
        "kelembapan": round(np.random.uniform(45.0, 55.0), 1),
        "tekanan": round(np.random.uniform(1012.0, 1013.5), 1)
    }

st.sidebar.title("⚙️ Pengaturan")
st.sidebar.markdown("---")

st.sidebar.header("🎵 Background Music")

music_url = st.sidebar.text_input(
    "Link Lagu (URL MP3)", 
    value="https://files.freemusicarchive.org/田野%20-%20Lofi%20Study%20Beat/田野%20-%2001%20-%20Lofi%20Study%20Beat.mp3"
)

music_title = st.sidebar.text_input("Judul Lagu", value="Lo-Fi Chill Beat")
music_artist = st.sidebar.text_input("Artist", value="Studio Mix")

st.sidebar.markdown("---")

st.title("🧪 Laboratorium Monitoring")
st.markdown("### Lingkungan Laboratorium")

col1, col2, col3 = st.columns(3)
data = get_sensor_data()

with col1:
    st.metric("🌡️ Suhu", f"{data['suhu']} °C", delta="Normal" if data['suhu'] < 25 else "High")
with col2:
    st.metric("💧 Kelembapan", f"{data['kelembapan']} %", delta="Normal")
with col3:
    st.metric("⚖️ Tekanan", f"{data['tekanan']} hPa")

st.markdown("### 📈 Grafik Historik")

btn_update = st.button("🔄 Update Data")

if btn_update:
    new_row = pd.DataFrame([data])
    st.session_state['history'] = pd.concat([st.session_state['history'], new_row], ignore_index=True)
    if len(st.session_state['history']) > 20:
        st.session_state['history'] = st.session_state['history'].tail(20)

if not st.session_state['history'].empty:
    chart = st.session_state['history'].set_index("timestamp")
    st.line_chart(chart)

st.markdown("---")
if data['suhu'] > 26:
    st.error("⚠️ PERINGATAN: Suhu Tinggi!")
else:
    st.success("✅ Kondisi Stabil")

if music_url:
    try:
        st.audio(music_url, format='audio/mp3', loop=True, autoplay=True)
    except:
        pass
    
    st.markdown(f"""
    <div class="music-info">
        🎶 SEDANG MEMUTAR: {music_title} <br>
        🎤 Artist: {music_artist} <br>
        🔁 Mode: LOOP (Berulang)
    </div>
    """, unsafe_allow_html=True)
    
    col_play1, col_play2 = st.columns([1, 4])
    with col_play1:
        st.markdown("**Jika/autoplay diblokir browser:**")
    with col_play2:
        if st.button("▶️ KLIK UNTUK MULAI MUSIK"):
            st.audio(music_url, format='audio/mp3', loop=True, autoplay=True)
            st.rerun()

elif music_url == "":
    st.sidebar.warning("Masukkan link lagu di kolom pengaturan!")
