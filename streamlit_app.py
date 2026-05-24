import streamlit as st
import pandas as pd
import random
import requests
import base64
import time
from datetime import datetime, timezone, timedelta

WIB = timezone(timedelta(hours=7))

# ============================================================
# 🔧 KONFIGURASI — UBAH SESUAI KEBUTUHAN
# ============================================================
JUDUL_APLIKASI = "Lab Environment Monitor"                    # ✏️ Ganti judul
SUBJUDUL = "Sistem Monitoring Suhu, Kelembapan & Tekanan"     # ✏️ Ganti subjudul
NAMA_LABORATORIUM = "Laboratorium Kimia Analitik"             # ✏️ Ganti nama lab
URL_BACKSOUND = "https://raw.githubusercontent.com/LahThan/Monitoring_suhu/main/backsound.mp3"  # ✏️ Ganti URL lagu

BATAS_SUHU_MIN = 18.0       # ✏️ Suhu minimum normal (°C)
BATAS_SUHU_MAX = 26.0       # ✏️ Suhu maksimum normal (°C)
BATAS_KELEMBAPAN_MIN = 40   # ✏️ Kelembapan minimum normal (%)
BATAS_KELEMBAPAN_MAX = 70   # ✏️ Kelembapan maksimum normal (%)
BATAS_TEKANAN_MIN = 990     # ✏️ Tekanan minimum normal (hPa)
BATAS_TEKANAN_MAX = 1020    # ✏️ Tekanan maksimum normal (hPa)

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================
st.set_page_config(
    page_title=JUDUL_APLIKASI,
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

# ============================================================
# CSS
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
    --accent-red: #ff4444;
    --text-main: #e0f0ff;
    --text-dim: #6a8caa;
    --border: rgba(0,212,255,0.2);
}

html, body, [data-testid="stAppViewContainer"] {
    background: #040d1a !important;
    color: #e0f0ff !important;
    font-family: 'Rajdhani', sans-serif !important;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 0%, #0a1f4d 0%, #040d1a 60%) !important;
}
[data-testid="stSidebar"] {
    background: #071428 !important;
    border-right: 1px solid rgba(0,212,255,0.15) !important;
}
.header-wrap {
    text-align: center;
    padding: 1.5rem 0 1rem;
    border-bottom: 1px solid rgba(0,212,255,0.2);
    margin-bottom: 1.5rem;
}
.header-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.2rem;
    font-weight: 900;
    letter-spacing: 0.1em;
    color: #00d4ff;
    text-shadow: 0 0 30px rgba(0,212,255,0.6);
    margin: 0;
}
.header-sub {
    font-size: 0.9rem;
    color: #6a8caa;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-top: 0.3rem;
}
.header-lab {
    font-size: 1.1rem;
    color: #00ff88;
    font-weight: 600;
    letter-spacing: 0.1em;
    margin-top: 0.2rem;
}
.sensor-card {
    background: #071428;
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 16px;
    padding: 1.5rem 1.2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 0 20px rgba(0,212,255,0.15);
}
.sensor-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, #00d4ff, transparent);
}
.sensor-card.warning {
    border-color: rgba(255,68,68,0.5);
    box-shadow: 0 0 20px rgba(255,68,68,0.2);
}
.sensor-card.warning::before {
    background: linear-gradient(90deg, transparent, #ff4444, transparent);
}
.sensor-icon { font-size: 2rem; margin-bottom: 0.4rem; }
.sensor-label {
    font-family: 'Orbitron', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: #6a8caa;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.sensor-value {
    font-family: 'Orbitron', monospace;
    font-size: 2.5rem;
    font-weight: 700;
    line-height: 1;
}
.sensor-unit { font-size: 0.9rem; opacity: 0.7; }
.sensor-status {
    margin-top: 0.6rem;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    padding: 0.2rem 0.7rem;
    border-radius: 99px;
    display: inline-block;
}
.status-normal { background: rgba(0,255,136,0.12); color: #00ff88; border: 1px solid rgba(0,255,136,0.3); }
.status-warning { background: rgba(255,68,68,0.12); color: #ff4444; border: 1px solid rgba(255,68,68,0.3); }
.info-bar {
    background: #0a1f3d;
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 12px;
    padding: 0.8rem 1.2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.2rem;
    flex-wrap: wrap;
    gap: 0.8rem;
}
.info-item { text-align: center; }
.info-item-label { font-size: 0.65rem; color: #6a8caa; letter-spacing: 0.15em; text-transform: uppercase; }
.info-item-value { font-family: 'Orbitron', monospace; font-size: 0.95rem; color: #00d4ff; font-weight: 700; }
.section-title {
    font-family: 'Orbitron', monospace;
    font-size: 0.8rem;
    letter-spacing: 0.2em;
    color: #6a8caa;
    text-transform: uppercase;
    border-left: 3px solid #00d4ff;
    padding-left: 0.8rem;
    margin: 1.5rem 0 1rem;
}
.footer {
    text-align: center;
    padding: 1.2rem 0;
    color: #6a8caa;
    font-size: 0.75rem;
    border-top: 1px solid rgba(0,212,255,0.15);
    margin-top: 2rem;
    letter-spacing: 0.1em;
}
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    background: rgba(0,212,255,0.15) !important;
    border: 1px solid rgba(0,212,255,0.4) !important;
    border-radius: 8px !important;
}
[data-testid="stSidebarResizeHandle"] {
    display: none !important;
    pointer-events: none !important;
}
div[class*="ResizeHandle"] {
    display: none !important;
    pointer-events: none !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["Waktu", "Suhu (°C)", "Kelembapan (%)", "Tekanan (hPa)"]
    )
if "audio_bytes" not in st.session_state:
    try:
        resp = requests.get(URL_BACKSOUND)
        st.session_state.audio_bytes = resp.content
    except:
        st.session_state.audio_bytes = None

# Auto tambah data setiap 10 detik
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = datetime.now(WIB)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:0.8rem 0; border-bottom:1px solid rgba(0,212,255,0.2); margin-bottom:1rem;">
        <div style="font-family:'Orbitron',monospace; font-size:0.9rem; color:#00d4ff; letter-spacing:0.1em;">⚙️ PENGATURAN</div>
    </div>
    """, unsafe_allow_html=True)

    # Auto refresh info
    st.markdown("**🔄 Auto Refresh**")
    st.markdown("""
    <div style="background:rgba(0,212,255,0.07); border:1px solid rgba(0,212,255,0.2);
    border-radius:8px; padding:0.6rem 0.8rem; font-size:0.8rem; color:#00d4ff;">
    ⏱ Data diperbarui otomatis setiap <b>10 detik</b>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("▶ Refresh Sekarang", use_container_width=True, key="btn_refresh"):
        st.rerun()

    st.markdown("---")

    # Pengaturan grafik
    st.markdown("**📊 Tampilan Grafik**")
    max_grafik = st.slider("Jumlah data di grafik", 5, 50, 15)

    st.markdown("---")

    # Download CSV
    st.markdown("**⬇️ Download Data CSV**")
    total = len(st.session_state.data)

    if total > 0:
        jumlah_download = st.number_input(
            "Jumlah data yang didownload",
            min_value=1,
            max_value=total,
            value=min(10, total),
            step=1
        )
        pilihan = st.radio(
            "Pilih rentang data",
            ["Data Terbaru", "Data Terlama", "Semua Data"],
            index=0
        )
        df = st.session_state.data
        if pilihan == "Data Terbaru":
            df_dl = df.tail(int(jumlah_download))
        elif pilihan == "Data Terlama":
            df_dl = df.head(int(jumlah_download))
        else:
            df_dl = df

        now_str = datetime.now(WIB).strftime("%Y%m%d_%H%M%S")
        csv = df_dl.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"⬇️ Download {len(df_dl)} Data (.csv)",
            data=csv,
            file_name=f"lab_data_{now_str}.csv",
            mime="text/csv",
            use_container_width=True,
            key="btn_download"
        )
        st.caption(f"Total data tersimpan: **{total}** record")
    else:
        st.info("Belum ada data. Klik 'Refresh Data Baru' dulu.")

    st.markdown("---")

    # Audio
    st.markdown("**🎵 Backsound**")
    if st.session_state.audio_bytes:
        st.audio(st.session_state.audio_bytes, format="audio/mp3", loop=True)
    else:
        st.warning("Gagal load audio. Cek URL_BACKSOUND.")

# ============================================================
# AUTO REFRESH DATA SETIAP 10 DETIK
# ============================================================
now_data = datetime.now(WIB)
selisih = (now_data - st.session_state.last_refresh).total_seconds()
if selisih >= 10:
    # Ambil nilai terakhir, naik/turun sedikit (realistis)
    if not st.session_state.data.empty:
        last = st.session_state.data.iloc[-1]
        suhu_baru = round(last["Suhu (°C)"] + random.uniform(-0.3, 0.3), 1)
        kelembapan_baru = round(last["Kelembapan (%)"] + random.uniform(-0.5, 0.5), 1)
        tekanan_baru = round(last["Tekanan (hPa)"] + random.uniform(-0.3, 0.3), 1)
        # Batasi supaya tidak keluar range wajar
        suhu_baru = max(17.0, min(30.0, suhu_baru))
        kelembapan_baru = max(35.0, min(80.0, kelembapan_baru))
        tekanan_baru = max(985.0, min(1025.0, tekanan_baru))
    else:
        suhu_baru = round(random.uniform(21, 24), 1)
        kelembapan_baru = round(random.uniform(45, 55), 1)
        tekanan_baru = round(random.uniform(1000, 1010), 1)
    new_row = pd.DataFrame({
        "Waktu": [now_data.strftime("%H:%M:%S")],
        "Suhu (°C)": [suhu_baru],
        "Kelembapan (%)": [kelembapan_baru],
        "Tekanan (hPa)": [tekanan_baru]
    })
    st.session_state.data = pd.concat(
        [st.session_state.data, new_row], ignore_index=True
    )
    st.session_state.last_refresh = now_data

# ============================================================
# HEADER
# ============================================================
st.markdown(f"""
<div class="header-wrap">
    <div class="header-title">🔬 {JUDUL_APLIKASI}</div>
    <div class="header-sub">{SUBJUDUL}</div>
    <div class="header-lab">{NAMA_LABORATORIUM}</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# INFO BAR
# ============================================================
now = datetime.now(WIB)
total_data = len(st.session_state.data)
st.markdown(f"""
<div class="info-bar">
    <div class="info-item">
        <div class="info-item-label">Tanggal</div>
        <div class="info-item-value">{now.strftime('%d %b %Y')}</div>
    </div>
    <div class="info-item">
        <div class="info-item-label">Waktu (WIB)</div>
        <div class="info-item-value">{now.strftime('%H:%M:%S')}</div>
    </div>
    <div class="info-item">
        <div class="info-item-label">Total Data</div>
        <div class="info-item-value">{total_data} Record</div>
    </div>
    <div class="info-item">
        <div class="info-item-label">Status Sistem</div>
        <div class="info-item-value" style="color:#00ff88;">● ONLINE</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# KARTU SENSOR
# ============================================================
if not st.session_state.data.empty:
    latest = st.session_state.data.iloc[-1]
    suhu = latest["Suhu (°C)"]
    kelembapan = latest["Kelembapan (%)"]
    tekanan = latest["Tekanan (hPa)"]
else:
    suhu = kelembapan = tekanan = "-"

def cek(nilai, mn, mx):
    if nilai == "-":
        return "–", "#6a8caa", ""
    if mn <= nilai <= mx:
        return "NORMAL", "#00ff88", "status-normal"
    return "⚠ PERINGATAN", "#ff4444", "status-warning"

st_l, st_w, st_k = cek(suhu, BATAS_SUHU_MIN, BATAS_SUHU_MAX)
kl_l, kl_w, kl_k = cek(kelembapan, BATAS_KELEMBAPAN_MIN, BATAS_KELEMBAPAN_MAX)
tk_l, tk_w, tk_k = cek(tekanan, BATAS_TEKANAN_MIN, BATAS_TEKANAN_MAX)

st.markdown('<div class="section-title">📡 Data Sensor Real-time</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""
    <div class="sensor-card {'warning' if 'PERINGATAN' in st_l else ''}">
        <div class="sensor-icon">🌡️</div>
        <div class="sensor-label">Suhu</div>
        <div class="sensor-value" style="color:{st_w};">{suhu}<span class="sensor-unit"> °C</span></div>
        <div style="color:{st_w}; font-size:0.7rem; margin-top:0.4rem; opacity:0.7;">Normal: {BATAS_SUHU_MIN}–{BATAS_SUHU_MAX} °C</div>
        <span class="sensor-status {st_k}">{st_l}</span>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="sensor-card {'warning' if 'PERINGATAN' in kl_l else ''}">
        <div class="sensor-icon">💧</div>
        <div class="sensor-label">Kelembapan</div>
        <div class="sensor-value" style="color:{kl_w};">{kelembapan}<span class="sensor-unit"> %</span></div>
        <div style="color:{kl_w}; font-size:0.7rem; margin-top:0.4rem; opacity:0.7;">Normal: {BATAS_KELEMBAPAN_MIN}–{BATAS_KELEMBAPAN_MAX} %</div>
        <span class="sensor-status {kl_k}">{kl_l}</span>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="sensor-card {'warning' if 'PERINGATAN' in tk_l else ''}">
        <div class="sensor-icon">🔵</div>
        <div class="sensor-label">Tekanan Udara</div>
        <div class="sensor-value" style="color:{tk_w};">{tekanan}<span class="sensor-unit"> hPa</span></div>
        <div style="color:{tk_w}; font-size:0.7rem; margin-top:0.4rem; opacity:0.7;">Normal: {BATAS_TEKANAN_MIN}–{BATAS_TEKANAN_MAX} hPa</div>
        <span class="sensor-status {tk_k}">{tk_l}</span>
    </div>""", unsafe_allow_html=True)

# ============================================================
# STATUS KESELURUHAN
# ============================================================
st.markdown("")
if suhu == "-":
    st.markdown("""<div style="background:rgba(0,212,255,0.07); border:1px solid rgba(0,212,255,0.2);
    border-radius:12px; padding:1rem; text-align:center; color:#6a8caa;
    font-family:'Orbitron',monospace; font-size:0.8rem; letter-spacing:0.15em;">
    ℹ️ KLIK "REFRESH DATA BARU" DI SIDEBAR UNTUK MULAI MONITORING</div>""", unsafe_allow_html=True)
elif all("PERINGATAN" not in x for x in [st_l, kl_l, tk_l]):
    st.markdown("""<div style="background:rgba(0,255,136,0.07); border:1px solid rgba(0,255,136,0.25);
    border-radius:12px; padding:1rem; text-align:center; color:#00ff88;
    font-family:'Orbitron',monospace; font-size:0.8rem; letter-spacing:0.15em;">
    ✅ SEMUA PARAMETER DALAM BATAS NORMAL</div>""", unsafe_allow_html=True)
else:
    warns = []
    if "PERINGATAN" in st_l: warns.append("Suhu")
    if "PERINGATAN" in kl_l: warns.append("Kelembapan")
    if "PERINGATAN" in tk_l: warns.append("Tekanan")
    st.markdown(f"""<div style="background:rgba(255,68,68,0.07); border:1px solid rgba(255,68,68,0.3);
    border-radius:12px; padding:1rem; text-align:center; color:#ff4444;
    font-family:'Orbitron',monospace; font-size:0.8rem; letter-spacing:0.15em;">
    ⚠️ PERINGATAN: {' · '.join(warns)} DILUAR BATAS NORMAL</div>""", unsafe_allow_html=True)

# ============================================================
# GRAFIK
# ============================================================
if not st.session_state.data.empty:
    st.markdown('<div class="section-title">📈 Grafik Monitoring</div>', unsafe_allow_html=True)
    df_chart = st.session_state.data.tail(max_grafik).set_index("Waktu")
    st.line_chart(df_chart, use_container_width=True, height=300)

# ============================================================
# TABEL DATA
# ============================================================
if not st.session_state.data.empty:
    st.markdown('<div class="section-title">📋 Tabel Data Terbaru</div>', unsafe_allow_html=True)
    st.dataframe(
        st.session_state.data.tail(max_grafik)[::-1].reset_index(drop=True),
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# FOOTER
# ============================================================
st.markdown(f"""
<div class="footer">
    🔬 {NAMA_LABORATORIUM} &nbsp;|&nbsp; {JUDUL_APLIKASI} &nbsp;|&nbsp;
    {now.strftime('%d/%m/%Y %H:%M')} WIB
</div>
""", unsafe_allow_html=True)

# ============================================================
# AUTO RERUN SETIAP 10 DETIK
# ============================================================
time.sleep(10)
st.rerun()
