import streamlit as st
import random
import time
import base64
from datetime import datetime
import requests
import pytz

JUDUL_APLIKASI = "Lab Environment Monitor"         
SUBJUDUL = "Sistem Monitoring Suhu, Kelembapan & Tekanan"  
NAMA_LABORATORIUM = "Laboratorium Kimia Analitik"  

URL_BACKSOUND = "https://raw.githubusercontent.com/LahThan/Monitoring_suhu/main/backsound.mp3"

AUTOPLAY_MUSIK = True

BATAS_SUHU_MIN = 18.0     
BATAS_SUHU_MAX = 26.0     
BATAS_KELEMBAPAN_MIN = 40 
BATAS_KELEMBAPAN_MAX = 70 
BATAS_TEKANAN_MIN = 990   
BATAS_TEKANAN_MAX = 1020  

# Interval refresh otomatis (detik)
INTERVAL_REFRESH = 5      

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================

st.set_page_config(
    page_title=JUDUL_APLIKASI,
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# STYLING CSS
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');

:root {
    --bg-primary: #040d1a;
    --bg-card: #071428;
    --bg-card2: #0a1f3d;
    --accent-blue: #00d4ff;
    --accent-green: #00ff88;
    --accent-yellow: #ffd700;
    --accent-red: #ff4444;
    --text-main: #e0f0ff;
    --text-dim: #6a8caa;
    --border: rgba(0,212,255,0.2);
    --glow: 0 0 20px rgba(0,212,255,0.3);
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-primary) !important;
    color: var(--text-main) !important;
    font-family: 'Rajdhani', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 0%, #0a1f4d 0%, #040d1a 60%) !important;
}

/* Header */
.header-wrap {
    text-align: center;
    padding: 2rem 0 1rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
}
.header-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.4rem;
    font-weight: 900;
    letter-spacing: 0.12em;
    color: var(--accent-blue);
    text-shadow: 0 0 30px rgba(0,212,255,0.6), 0 0 60px rgba(0,212,255,0.2);
    margin: 0;
}
.header-sub {
    font-size: 1rem;
    color: var(--text-dim);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-top: 0.4rem;
}
.header-lab {
    font-size: 1.1rem;
    color: var(--accent-green);
    font-weight: 600;
    letter-spacing: 0.1em;
    margin-top: 0.3rem;
}

/* Kartu sensor */
.sensor-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.8rem 1.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: var(--glow);
    transition: transform 0.2s;
}
.sensor-card:hover { transform: translateY(-4px); }
.sensor-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, var(--accent-blue), transparent);
}
.sensor-card.warning { border-color: rgba(255,68,68,0.5); box-shadow: 0 0 20px rgba(255,68,68,0.3); }
.sensor-card.warning::before { background: linear-gradient(90deg, transparent, var(--accent-red), transparent); }

.sensor-icon { font-size: 2.4rem; margin-bottom: 0.5rem; }
.sensor-label {
    font-family: 'Orbitron', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    color: var(--text-dim);
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.sensor-value {
    font-family: 'Orbitron', monospace;
    font-size: 2.8rem;
    font-weight: 700;
    line-height: 1;
}
.sensor-unit { font-size: 1rem; opacity: 0.7; }
.sensor-status {
    margin-top: 0.8rem;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    padding: 0.25rem 0.8rem;
    border-radius: 99px;
    display: inline-block;
}
.status-normal { background: rgba(0,255,136,0.15); color: var(--accent-green); border: 1px solid rgba(0,255,136,0.3); }
.status-warning { background: rgba(255,68,68,0.15); color: var(--accent-red); border: 1px solid rgba(255,68,68,0.3); }

/* Info bar */
.info-bar {
    background: var(--bg-card2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
    gap: 1rem;
}
.info-item { text-align: center; }
.info-item-label { font-size: 0.7rem; color: var(--text-dim); letter-spacing: 0.15em; text-transform: uppercase; }
.info-item-value { font-family: 'Orbitron', monospace; font-size: 1rem; color: var(--accent-blue); font-weight: 700; }

/* Footer */
.footer {
    text-align: center;
    padding: 1.5rem 0;
    color: var(--text-dim);
    font-size: 0.8rem;
    border-top: 1px solid var(--border);
    margin-top: 2rem;
    letter-spacing: 0.1em;
}

/* Sembunyikan elemen bawaan streamlit */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* Streamlit metric override */
[data-testid="metric-container"] { display: none; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNGSI BACKSOUND (load dari URL GitHub)
# ============================================================

def embed_audio_from_url(url: str, autoplay: bool = True):
    try:
        response = requests.get(url)
        audio_bytes = response.content
        b64 = base64.b64encode(audio_bytes).decode()
        html = f"""
        <div id="overlay" style="
            position: fixed;
            top: 0; left: 0;
            width: 100vw; height: 100vh;
            background: rgba(4,13,26,0.92);
            z-index: 9999;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        " onclick="startAudio()">
            <div style="
                font-family: 'Orbitron', monospace;
                color: #00d4ff;
                font-size: 1.1rem;
                letter-spacing: 0.2em;
                margin-bottom: 1.5rem;
                text-shadow: 0 0 20px rgba(0,212,255,0.6);
            ">🔬 KLIK UNTUK MEMULAI</div>
            <div style="
                width: 80px; height: 80px;
                border-radius: 50%;
                background: rgba(0,212,255,0.15);
                border: 2px solid #00d4ff;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 2rem;
                box-shadow: 0 0 30px rgba(0,212,255,0.4);
            ">▶</div>
        </div>
        <div style="
            background: rgba(0,212,255,0.07);
            border: 1px solid rgba(0,212,255,0.2);
            border-radius: 12px;
            padding: 0.8rem 1.2rem;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        ">
            <span style="font-size:1.4rem;">🎵</span>
            <span style="font-family:'Rajdhani',sans-serif; color:#6a8caa; font-size:0.85rem; letter-spacing:0.1em;">BACKSOUND</span>
            <audio id="lab-audio" controls loop style="height:32px; flex:1; min-width:200px;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mpeg">
            </audio>
        </div>
        <script>
            function startAudio() {{
                const audio = document.getElementById('lab-audio');
                const overlay = document.getElementById('overlay');
                audio.play();
                overlay.style.display = 'none';
            }}
        </script>
        """
        st.markdown(html, unsafe_allow_html=True)
    except:
        st.warning("⚠️ Gagal memuat backsound. Cek URL di konfigurasi.")


# ============================================================
# SIMULASI DATA SENSOR (ganti dengan data sensor nyata)
# ============================================================

def baca_sensor():
    """Simulasi pembacaan sensor. Ganti fungsi ini dengan data sensor asli."""
    suhu = round(random.uniform(17, 28), 1)
    kelembapan = round(random.uniform(38, 75), 1)
    tekanan = round(random.uniform(985, 1025), 1)
    return suhu, kelembapan, tekanan


def cek_status(nilai, min_val, max_val):
    return "NORMAL" if min_val <= nilai <= max_val else "⚠ PERINGATAN"


def warna_nilai(nilai, min_val, max_val):
    if min_val <= nilai <= max_val:
        return "#00ff88"
    return "#ff4444"


# ============================================================
# RENDER HALAMAN
# ============================================================

# Header
st.markdown(f"""
<div class="header-wrap">
    <div class="header-title">🔬 {JUDUL_APLIKASI}</div>
    <div class="header-sub">{SUBJUDUL}</div>
    <div class="header-lab">{NAMA_LABORATORIUM}</div>
</div>
""", unsafe_allow_html=True)

# Backsound
embed_audio_from_url(URL_BACKSOUND, autoplay=AUTOPLAY_MUSIK)

# Info bar
now = datetime.now(pytz.timezone('Asia/Jakarta'))
st.markdown(f"""
<div class="info-bar">
    <div class="info-item">
        <div class="info-item-label">Tanggal</div>
        <div class="info-item-value">{now.strftime('%d %b %Y')}</div>
    </div>
    <div class="info-item">
        <div class="info-item-label">Waktu</div>
        <div class="info-item-value">{now.strftime('%H:%M:%S')}</div>
    </div>
    <div class="info-item">
        <div class="info-item-label">Refresh</div>
        <div class="info-item-value">Tiap {INTERVAL_REFRESH}s</div>
    </div>
    <div class="info-item">
        <div class="info-item-label">Status Sistem</div>
        <div class="info-item-value" style="color:#00ff88;">● ONLINE</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Baca sensor
suhu, kelembapan, tekanan = baca_sensor()

status_suhu = cek_status(suhu, BATAS_SUHU_MIN, BATAS_SUHU_MAX)
status_kelembapan = cek_status(kelembapan, BATAS_KELEMBAPAN_MIN, BATAS_KELEMBAPAN_MAX)
status_tekanan = cek_status(tekanan, BATAS_TEKANAN_MIN, BATAS_TEKANAN_MAX)

warn_suhu = "warning" if "PERINGATAN" in status_suhu else ""
warn_kelembapan = "warning" if "PERINGATAN" in status_kelembapan else ""
warn_tekanan = "warning" if "PERINGATAN" in status_tekanan else ""

warna_suhu = warna_nilai(suhu, BATAS_SUHU_MIN, BATAS_SUHU_MAX)
warna_kelembapan = warna_nilai(kelembapan, BATAS_KELEMBAPAN_MIN, BATAS_KELEMBAPAN_MAX)
warna_tekanan = warna_nilai(tekanan, BATAS_TEKANAN_MIN, BATAS_TEKANAN_MAX)

kelas_status_suhu = "status-normal" if not warn_suhu else "status-warning"
kelas_status_kelembapan = "status-normal" if not warn_kelembapan else "status-warning"
kelas_status_tekanan = "status-normal" if not warn_tekanan else "status-warning"

# Kartu sensor
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="sensor-card {warn_suhu}">
        <div class="sensor-icon">🌡️</div>
        <div class="sensor-label">Suhu</div>
        <div class="sensor-value" style="color:{warna_suhu};">
            {suhu}<span class="sensor-unit"> °C</span>
        </div>
        <div style="color:{warna_suhu}; font-size:0.75rem; margin-top:0.5rem; opacity:0.7;">
            Normal: {BATAS_SUHU_MIN}–{BATAS_SUHU_MAX} °C
        </div>
        <span class="sensor-status {kelas_status_suhu}">{status_suhu}</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="sensor-card {warn_kelembapan}">
        <div class="sensor-icon">💧</div>
        <div class="sensor-label">Kelembapan</div>
        <div class="sensor-value" style="color:{warna_kelembapan};">
            {kelembapan}<span class="sensor-unit"> %</span>
        </div>
        <div style="color:{warna_kelembapan}; font-size:0.75rem; margin-top:0.5rem; opacity:0.7;">
            Normal: {BATAS_KELEMBAPAN_MIN}–{BATAS_KELEMBAPAN_MAX} %
        </div>
        <span class="sensor-status {kelas_status_kelembapan}">{status_kelembapan}</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="sensor-card {warn_tekanan}">
        <div class="sensor-icon">🔵</div>
        <div class="sensor-label">Tekanan Udara</div>
        <div class="sensor-value" style="color:{warna_tekanan};">
            {tekanan}<span class="sensor-unit"> hPa</span>
        </div>
        <div style="color:{warna_tekanan}; font-size:0.75rem; margin-top:0.5rem; opacity:0.7;">
            Normal: {BATAS_TEKANAN_MIN}–{BATAS_TEKANAN_MAX} hPa
        </div>
        <span class="sensor-status {kelas_status_tekanan}">{status_tekanan}</span>
    </div>
    """, unsafe_allow_html=True)

# Spacer
st.markdown("<br>", unsafe_allow_html=True)

# Ringkasan kondisi
semua_normal = all("PERINGATAN" not in s for s in [status_suhu, status_kelembapan, status_tekanan])
if semua_normal:
    st.markdown("""
    <div style="background:rgba(0,255,136,0.07); border:1px solid rgba(0,255,136,0.25);
    border-radius:12px; padding:1rem 1.5rem; text-align:center; color:#00ff88;
    font-family:'Orbitron',monospace; font-size:0.9rem; letter-spacing:0.15em;">
        ✅ SEMUA PARAMETER DALAM BATAS NORMAL
    </div>
    """, unsafe_allow_html=True)
else:
    sensor_warn = []
    if "PERINGATAN" in status_suhu: sensor_warn.append("Suhu")
    if "PERINGATAN" in status_kelembapan: sensor_warn.append("Kelembapan")
    if "PERINGATAN" in status_tekanan: sensor_warn.append("Tekanan")
    st.markdown(f"""
    <div style="background:rgba(255,68,68,0.07); border:1px solid rgba(255,68,68,0.3);
    border-radius:12px; padding:1rem 1.5rem; text-align:center; color:#ff4444;
    font-family:'Orbitron',monospace; font-size:0.9rem; letter-spacing:0.15em;">
        ⚠️ PERINGATAN: {' · '.join(sensor_warn)} DILUAR BATAS NORMAL
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div class="footer">
    🔬 {NAMA_LABORATORIUM} &nbsp;|&nbsp; {JUDUL_APLIKASI} &nbsp;|&nbsp;
    Diperbarui: {now.strftime('%d/%m/%Y %H:%M:%S')}
</div>
""", unsafe_allow_html=True)

# Auto-refresh
time.sleep(INTERVAL_REFRESH)
st.rerun()
