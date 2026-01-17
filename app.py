import streamlit as st
import cv2
import numpy as np
import qrcode
import base64
import zipfile
from io import BytesIO
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

# --- 1. KONFIGURASI & DATA ---
SANDI_UTAMA = "150882"
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
        salt=b'garam_xtkr_v3',
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return Fernet(key)

# --- 3. UI STYLE ---
st.set_page_config(page_title="Scanner Otomatis X TKR", layout="centered")

# CSS untuk membuat tampilan fokus pada kamera
st.markdown(f"""
    <style>
    div[data-testid="stCameraInput"] {{ border: 5px solid #28a745; border-radius: 20px; }}
    .stButton>button {{ background-color: #28a745; color: white; font-weight: bold; border-radius: 10px; }}
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ Scanner Presensi X TKR")

tab_scan, tab_admin = st.tabs(["📸 SCAN QR", "⚙️ ADMIN"])

# --- 4. SCANNER (PROSES INSTAN) ---
with tab_scan:
    st.info("Sandi Otomatis: " + SANDI_UTAMA)
    # Gunakan kunci statis agar siswa tidak perlu mengetik
    cipher = get_cipher(SANDI_UTAMA)
    
    # Widget kamera
    img_file = st.camera_input("Arahkan QR ke Kotak di Bawah")

    if img_file:
        # Mengolah gambar secara instan setelah tombol ditekan
        file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
        opencv_img = cv2.imdecode(file_bytes, 1)
        
        # Deteksi QR
        detector = cv2.QRCodeDetector()
        decoded_text, points, _ = detector.detectAndDecode(opencv_img)
        
        if decoded_text:
            try:
                # Dekripsi link
                final_link = cipher.decrypt(decoded_text.encode()).decode()
                st.success("✅ BERHASIL TERDETEKSI!")
                st.balloons()
                # Langsung tampilkan tombol absen besar
                st.link_button("🔥 KLIK DI SINI UNTUK KIRIM ABSEN", final_link, use_container_width=True, type="primary")
            except:
                st.error("❌ QR Code tidak cocok dengan sistem ini.")
        else:
            st.error("⚠️ QR Tidak Terdeteksi. Pastikan cahaya terang dan gambar fokus.")

# --- 5. ADMIN (ZIP GENERATOR) ---
with tab_admin:
    st.subheader("Cetak QR Baru")
    admin_pwd = st.text_input("Sandi Admin:", type="password", value=SANDI_UTAMA)
    
    if st.button("📦 Download Semua QR (ZIP)"):
        if admin_pwd == SANDI_UTAMA:
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
                for nama, link in DATA_SISWA.items():
                    # Buat QR Terenkripsi
                    token = get_cipher(SANDI_UTAMA).encrypt(link.encode()).decode()
                    qr_img = qrcode.make(token)
                    img_io = BytesIO()
                    qr_img.save(img_io, format="PNG")
                    zip_file.writestr(f"QR_{nama}.png", img_io.getvalue())
            
            st.download_button(
                label="📥 UNDUH SEKARANG",
                data=zip_buffer.getvalue(),
                file_name="QR_Siswa_XTKR.zip",
                mime="application/zip",
                use_container_width=True
            )
        else:
            st.error("Sandi Admin Salah!")

st.divider()
st.caption("Gunakan Kamera Belakang untuk hasil terbaik.")
