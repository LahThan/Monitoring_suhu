# app.py
import streamlit as st
import random
import io

# --- Bagian yang bisa diubah ---
APP_TITLE = "🌡️ Monitoring Suhu Laboratorium"   # Ubah judul di sini
DEFAULT_MUSIC_GITHUB_RAW = ""                  # Masukkan GitHub raw URL mp3 jika mau
# -------------------------------

st.set_page_config(page_title=APP_TITLE, layout="wide")
st.title(APP_TITLE)

# ---------------- Monitoring Suhu (contoh) ----------------
st.header("📡 Monitoring Suhu")
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
# ---------------------------------------------------------

st.markdown("---")
st.header("🎵 Backsound (pilih salah satu cara)")

# Opsi A: Upload file langsung lewat UI (paling mudah untuk testing)
uploaded_file = st.file_uploader("Upload file lagu (mp3/wav)", type=["mp3","wav"])
if uploaded_file is not None:
    st.audio(uploaded_file)

# Opsi B: Pakai file dari GitHub (raw URL)
st.write("Atau masukkan GitHub raw URL file audio (contoh: https://raw.githubusercontent.com/LahThan/Monitoring_suhu/refs/heads/main/backsound.mp3)")
music_url = st.text_input("GitHub raw URL", value=DEFAULT_MUSIC_GITHUB_RAW)
if music_url:
    st.audio(music_url)

# Opsi C: Autoplay (browser mungkin blokir autoplay)
autoplay = st.checkbox("Coba autoplay (browser mungkin memblokir)")
if music_url and autoplay:
    audio_html = f"""
    <audio controls autoplay loop>
      <source src="{music_url}" type="audio/mpeg">
      Your browser does not support the audio element.
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

st.caption("Ubah **APP_TITLE** dan **DEFAULT_MUSIC_GITHUB_RAW** di bagian atas untuk menyesuaikan judul dan lagu default.")
