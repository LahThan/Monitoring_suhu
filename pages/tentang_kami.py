import streamlit as st

# ============================================================
# 🔧 KONFIGURASI — UBAH SESUAI KEBUTUHAN
# ============================================================
NAMA_APLIKASI = "Lab Environment Monitor"          # ✏️ Ganti nama aplikasi
NAMA_LABORATORIUM = "Laboratorium Kimia Analitik"  # ✏️ Ganti nama laboratorium
DESKRIPSI_APLIKASI = "Aplikasi monitoring lingkungan laboratorium berbasis web yang dirancang untuk memantau kondisi suhu, kelembapan, dan tekanan udara secara real-time."  # ✏️ Ganti deskripsi

st.set_page_config(page_title="Tentang Kami", page_icon="👥", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
html, body, [data-testid="stAppViewContainer"] {
    background: #040d1a !important;
    color: #e0f0ff !important;
    font-family: 'Rajdhani', sans-serif !important;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 0%, #0a1f4d 0%, #040d1a 60%) !important;
}
[data-testid="stSidebarNav"] { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
footer { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
.card {
    background: #071428;
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
}
.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, #00d4ff, transparent);
}
.anggota-card {
    background: #0a1f3d;
    border: 1px solid rgba(0,212,255,0.15);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.anggota-no {
    font-family: 'Orbitron', monospace;
    font-size: 1.2rem;
    font-weight: 700;
    color: #00d4ff;
    min-width: 2rem;
    text-align: center;
}
.anggota-nama {
    font-size: 1rem;
    font-weight: 600;
    color: #e0f0ff;
}
.anggota-nim {
    font-size: 0.8rem;
    color: #6a8caa;
    letter-spacing: 0.05em;
}
.info-row {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.5rem 0;
    border-bottom: 1px solid rgba(0,212,255,0.08);
}
.info-label {
    font-size: 0.75rem;
    color: #6a8caa;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    min-width: 120px;
}
.info-value {
    font-size: 0.95rem;
    color: #e0f0ff;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# Tombol kembali
st.page_link("streamlit_app.py", label="🏠 Kembali ke Dashboard Utama", use_container_width=True)
st.markdown("---")

# Header
st.markdown(f"""
<div style="text-align:center; padding:1.5rem 0 1rem;">
    <div style="font-family:'Orbitron',monospace; font-size:1.8rem; font-weight:900; color:#00d4ff;
    text-shadow:0 0 30px rgba(0,212,255,0.6);">👥 Tentang Kami</div>
    <div style="color:#6a8caa; font-size:0.85rem; letter-spacing:0.15em; margin-top:0.3rem;">
    TIM PENGEMBANG APLIKASI</div>
</div>
""", unsafe_allow_html=True)

# Tentang Aplikasi
st.markdown(f"""
<div class="card">
    <div style="font-family:'Orbitron',monospace; font-size:0.8rem; color:#00d4ff; letter-spacing:0.15em; margin-bottom:0.8rem;">
    🔬 TENTANG APLIKASI</div>
    <div style="font-size:1.1rem; font-weight:700; color:#e0f0ff; margin-bottom:0.5rem;">{NAMA_APLIKASI}</div>
    <div style="font-size:0.9rem; color:#6a8caa; line-height:1.6;">{DESKRIPSI_APLIKASI}</div>
</div>
""", unsafe_allow_html=True)

# Fitur utama
st.markdown("""
<div class="card">
    <div style="font-family:'Orbitron',monospace; font-size:0.8rem; color:#00d4ff; letter-spacing:0.15em; margin-bottom:0.8rem;">
    ⚡ FITUR UTAMA</div>
    <div style="font-size:0.9rem; color:#e0f0ff; line-height:2;">
        🌡️ &nbsp;Monitoring suhu real-time<br>
        💧 &nbsp;Monitoring kelembapan real-time<br>
        🔵 &nbsp;Monitoring tekanan udara real-time<br>
        ⚠️ &nbsp;Sistem peringatan otomatis<br>
        📈 &nbsp;Grafik data historis<br>
        ⬇️ &nbsp;Download data CSV<br>
        🔄 &nbsp;Auto refresh setiap 10 detik
    </div>
</div>
""", unsafe_allow_html=True)

# Info tim
st.markdown(f"""
<div class="card">
    <div style="font-family:'Orbitron',monospace; font-size:0.8rem; color:#00d4ff; letter-spacing:0.15em; margin-bottom:1rem;">
    🎓 INFO TIM</div>
    <div class="info-row">
        <div class="info-label">Program Studi</div>
        <div class="info-value">Analisis Kimia</div>
    </div>
    <div class="info-row">
        <div class="info-label">Kelas</div>
        <div class="info-value">1C</div>
    </div>
    <div class="info-row">
        <div class="info-label">Institusi</div>
        <div class="info-value">Politeknik AKA Bogor</div>
    </div>
    <div class="info-row" style="border-bottom:none;">
        <div class="info-label">Laboratorium</div>
        <div class="info-value">{NAMA_LABORATORIUM}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Anggota tim (diurutkan abjad)
st.markdown("""
<div class="card">
    <div style="font-family:'Orbitron',monospace; font-size:0.8rem; color:#00d4ff; letter-spacing:0.15em; margin-bottom:1rem;">
    👤 ANGGOTA TIM</div>
    <div class="anggota-card">
        <div class="anggota-no">01</div>
        <div>
            <div class="anggota-nama">Fanny Aulia Difa Ananda</div>
            <div class="anggota-nim">NIM: 2560628</div>
        </div>
    </div>
    <div class="anggota-card">
        <div class="anggota-no">02</div>
        <div>
            <div class="anggota-nama">Kayla Nadindra Zalfa</div>
            <div class="anggota-nim">NIM: 2560655</div>
        </div>
    </div>
    <div class="anggota-card">
        <div class="anggota-no">03</div>
        <div>
            <div class="anggota-nama">Naisaburi Fathan Kurniadi</div>
            <div class="anggota-nim">NIM: 2560704</div>
        </div>
    </div>
    <div class="anggota-card">
        <div class="anggota-no">04</div>
        <div>
            <div class="anggota-nama">Risa Al Zahra Nugraha</div>
            <div class="anggota-nim">NIM: 2560759</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
