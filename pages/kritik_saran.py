import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_PENERIMA = "fthankrndi@gmail.com"   # ✏️ Email pemilik
EMAIL_PENGIRIM = "kelompok.12.lpk@gmail.com"   # ✏️ Gmail pengirim
EMAIL_APP_PASSWORD = "fhug rnbi aaeg tqua"  # ✏️ Gmail App Password

st.set_page_config(page_title="Saran & Kritik", page_icon="💬", layout="centered")

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
