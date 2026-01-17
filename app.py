import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import cv2
import numpy as np
import qrcode
import base64
import zipfile
from io import BytesIO
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

# --- 1. DATA MASTER SISWA ---
DATA_SISWA = {
    "ABU KHOROIROH": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=ABU+KHOROIROH&entry.1794922110=H",
    "ADYTIA PRATAMA": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=ADYTIA+PRATAMA&entry.1794922110=H",
    "AHMAD FAIZIN RAMADANI": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=AHMAD+FAIZIN+RAMADANI&entry.1794922110=H",
    "AHMAD FAUZAN": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=AHMAD+FAUZAN&entry.1794922110=H",
    "AHMAD RAMA DANI": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=AHMAD+RAMA+DANI&entry.1794922110=H",
    "AKBAR ARIYAN": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=AKBAR+ARIYAN&entry.1794922110=H",
    "AKBAR DWI SAPUTRA": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=AKBAR+DWI+SAPUTRA&entry.1794922110=H",
    "ALFAREZZAL RADHITYA TOROSI": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=ALFAREZZAL+RADHITYA+TOROSI&entry.1794922110=H",
    "ARMAN SYAIFUL BAHRI": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=ARMAN+SYAIFUL+BAHRI&entry.1794922110=H",
    "BENY KURNIAWAN": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=BENY+KURNIAWAN&entry.1794922110=H",
    "DAVID KURNIAWAN": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=DAVID+KURNIAWAN&entry.1794922110=H",
    "FAHRUL ROZI": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=FAHRUL+ROZI&entry.1794922110=H",
    "FAIDUL BADRI": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=FAIDUL+BADRI&entry.1794922110=H",
    "FIRMAN AFANDI": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=FIRMAN+AFANDI&entry.1794922110=H",
    "ILAN CAHYA": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=ILAN+CAHYA&entry.1794922110=H",
    "JUDIANTO": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=JUDIANTO&entry.1794922110=H",
    "MOH. RAEHAN FIRMANSYAH": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=MOH.+RAEHAN+FIRMANSYAH&entry.1794922110=H",
    "MUHAMMAD FADIL MARSUKI": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=MUHAMMAD+FADIL+MARSUKI&entry.1794922110=H",
    "MUHAMMAD GHUFRON": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=MUHAMMAD+GHUFRON&entry.1794922110=H",
    "MUHAMMAD MALIK WARIYANTO": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=MUHAMMAD+MALIK+WARIYANTO&entry.1794922110=H",
    "MUHAMMAD ROMLI": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=MUHAMMAD+ROMLI&entry.1794922110=H",
    "NARJIYANTO": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=NARJIYANTO&entry.1794922110=H",
    "RIFKA PERADITIYA": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=RIFKA+PERADITIYA&entry.1794922110=H",
    "RIFKI KHAIRUL UMAM": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=RIFKI+KHAIRUL+UMAM&entry.1794922110=H",
    "RIFKI YANTO": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=RIFKI+YANTO&entry.1794922110=H",
    "ZAINAL ARIFIN": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=ZAINAl+ARIFIN&entry.1794922110=H"
}

# --- 2. FUNGSI KEAMANAN ---
@st.cache_resource
def get_cipher(password):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'garam_sekolah_aman_789',
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return Fernet(key)

# --- 3. UI CONFIG ---
st.set_page_config(page_title="Absensi QR Pro", layout="centered")
st.title("📸 Sistem Absensi QR Sekolah")

tab_scan, tab_admin = st.tabs(["📌 Scanner Siswa", "🛠️ Generator Admin"])

# --- 4. TAB SCANNER ---
with tab_scan:
    pwd_scan = st.text_input("Sandi Scanner:", type="password", value="150882", key="sc_pwd")
    st.info("Klik 'Start' dan arahkan kamera ke QR Code. Pilih kamera belakang pada 'Select Device' jika perlu.")

    ctx = webrtc_streamer(
        key="scanner-pro",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"video": {"facingMode": "environment"}, "audio": False},
        async_processing=True,
    )

    if ctx.video_receiver:
        detector = cv2.QRCodeDetector()
        img_frame = ctx.video_receiver.get_frame()
        
        if img_frame:
            img = img_frame.to_ndarray(format="bgr24")
            val, _, _ = detector.detectAndDecode(img)
            
            if val:
                try:
                    cipher = get_cipher(pwd_scan)
                    link_asli = cipher.decrypt(val.encode()).decode()
                    st.success("✅ QR Code Valid!")
                    st.link_button("👉 TEKAN UNTUK ABSEN SEKARANG", link_asli, type="primary", use_container_width=True)
                    st.balloons()
                except:
                    st.error("Sandi salah atau QR tidak dikenal!")

# --- 5. TAB ADMIN ---
with tab_admin:
    st.subheader("Cetak & Kelola QR Code")
    pwd_gen = st.text_input("Konfirmasi Sandi Admin:", type="password", value="150882", key="ad_pwd")
    
    if st.button("🚀 Generate & Siapkan ZIP Semua Siswa"):
        cipher_admin = get_cipher(pwd_gen)
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            cols = st.columns(2)
            for idx, (nama, link) in enumerate(DATA_SISWA.items()):
                token = cipher_admin.encrypt(link.encode()).decode()
                qr = qrcode.make(token)
                img_buffer = BytesIO()
                qr.save(img_buffer, format="PNG")
                
                zip_file.writestr(f"QR_{nama}.png", img_buffer.getvalue())
                
                with cols[idx % 2]:
                    st.image(img_buffer.getvalue(), caption=nama, width=150)
        
        st.success(f"Berhasil membuat {len(DATA_SISWA)} QR Code!")
        st.download_button(
            label="📥 DOWNLOAD SEMUA QR (ZIP)",
            data=zip_buffer.getvalue(),
            file_name="Semua_QR_Siswa.zip",
            mime="application/zip",
            use_container_width=True
        )

st.divider()
st.caption("Aplikasi Absensi Mandiri - Versi Keamanan Tinggi")
