import streamlit as st
import random
import pygame

APP_TITLE = "🌡️ Monitoring Suhu Laboratorium"
MUSIC_FILE = "backsound.mp3"  

pygame.mixer.init()

def play_music():
    try:
        pygame.mixer.music.load(MUSIC_FILE)
        pygame.mixer.music.play(-1) 
    except Exception as e:
        st.error(f"Gagal memutar musik: {e}")

def stop_music():
    pygame.mixer.music.stop()

st.title(APP_TITLE)

suhu_data = [random.uniform(20, 30) for _ in range(20)]
current_temp = suhu_data[-1]

st.metric(label="Suhu Saat Ini (°C)", value=f"{current_temp:.2f}")
st.line_chart(suhu_data)

if current_temp < 22:
    st.success("✅ Suhu rendah, aman")
elif 22 <= current_temp <= 28:
    st.info("ℹ️ Suhu normal")
else:
    st.warning("⚠️ Suhu tinggi, perlu perhatian!")

st.subheader("🎵 Backsound")
col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ Play Lagu"):
        play_music()
with col2:
    if st.button("⏸️ Stop Lagu"):
        stop_music()
