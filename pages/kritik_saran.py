import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_PENERIMA = st.secrets["EMAIL_PENERIMA"]
EMAIL_PENGIRIM = st.secrets["EMAIL_PENGIRIM"]
EMAIL_APP_PASSWORD = st.secrets["EMAIL_APP_PASSWORD"]
st.set_page_config(page_title="Saran & Kritik", page_icon="💬", layout="centered")

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
[data-testid="stSidebar"] {
    background: #071428 !important;
    border-right: 1px solid rgba(0,212,255,0.15) !important;
}
[data-testid="stSidebarNav"] { display: none !important; }
footer { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    background: rgba(0,212,255,0.15) !important;
    border: 1px solid rgba(0,212,255,0.4) !important;
    border-radius: 8px !important;
}
[data-testid="stSidebarResizeHandle"] { display: none !important; }
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    background: rgba(0,212,255,0.15) !important;
    border: 1px solid rgba(0,212,255,0.4) !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] {
    min-width: 300px !important;
    max-width: 300px !important;
    transform: none !important;
    display: block !important;
}
</style>
""", unsafe_allow_html=True)

st.page_link("streamlit_app.py", label="🔙 Kembali ke Dashboard", use_container_width=False)
st.markdown("## 💬 Saran & Kritik")
st.markdown("Sampaikan saran atau kritik kamu untuk pengembangan aplikasi ini.")
st.divider()

with st.form("form_saran", clear_on_submit=True):
    nama = st.text_input("Nama", placeholder="Nama kamu")
    email_user = st.text_input("Email", placeholder="Email kamu")
    subject = st.text_input("Subject", placeholder="Subjek pesan")
    pesan = st.text_area("Message", placeholder="Tulis saran atau kritik...", height=200)
    kirim = st.form_submit_button("📨 Submit", use_container_width=True)

    if kirim:
        if nama and email_user and subject and pesan:
            try:
                msg = MIMEMultipart()
                msg["From"] = EMAIL_PENGIRIM
                msg["To"] = EMAIL_PENERIMA
                msg["Subject"] = f"[Lab Monitor] {subject}"
                body = f"Nama: {nama}\nEmail: {email_user}\nSubject: {subject}\n\nPesan:\n{pesan}"
                msg.attach(MIMEText(body, "plain"))
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(EMAIL_PENGIRIM, EMAIL_APP_PASSWORD)
                    server.sendmail(EMAIL_PENGIRIM, EMAIL_PENERIMA, msg.as_string())
                st.success("✅ Pesan berhasil terkirim!")
            except Exception as e:
                st.error(f"❌ Gagal kirim: {e}")
        else:
            st.warning("⚠️ Semua field harus diisi!")
