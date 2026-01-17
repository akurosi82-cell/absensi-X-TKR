import streamlit as st
import qrcode
import cv2
import numpy as np
import base64
from io import BytesIO
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

# --- KONFIGURASI KEAMANAN ---
def get_cipher(password):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'garam_statis_123',
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return Fernet(key)

# --- DATA LINK SISWA (LENGKAP) ---
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
    "ZAINAl ARIFIN": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=ZAINAl+ARIFIN&entry.1794922110=H"
}

# --- PENGATURAN HALAMAN ---
st.set_page_config(page_title="Absensi QR Terenkripsi", layout="centered")

# Inisialisasi State Rotasi
if 'rotasi' not in st.session_state:
    st.session_state.rotasi = 0

def putar_layar():
    st.session_state.rotasi = (st.session_state.rotasi + 90) % 360

# --- CSS UNTUK TAMPILAN ---
st.markdown(f"""
    <style>
    video {{
        transform: rotate({st.session_state.rotasi}deg);
        border: 4px solid #007bff;
        border-radius: 15px;
        width: 100% !important;
    }}
    .stButton>button {{ width: 100%; font-weight: bold; border-radius: 10px; }}
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Scanner Absensi Sekolah")

tab1, tab2 = st.tabs(["📲 Scanner (Guru)", "🖨️ Download QR (Admin)"])

# --- TAB 1: SCANNER ---
with tab1:
    st.info("Arahkan kamera ke QR Code. Jika miring, klik tombol 'Putar Layar'.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.button("🔄 Putar Layar Kamera", on_click=putar_layar)
    with col_b:
        if st.button("❌ Reset"):
            st.session_state.rotasi = 0
            st.rerun()

    pwd = st.text_input("Password Scan:", value="150882", type="password")
    input_foto = st.camera_input("Ambil Foto QR")

    if input_foto and pwd:
        try:
            # Baca Gambar
            file_bytes = np.asarray(bytearray(input_foto.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, 1)
            
            # Deteksi QR
            det = cv2.QRCodeDetector()
            val, _, _ = det.detectAndDecode(img)
            
            if val:
                cipher = get_cipher(pwd)
                link_asli = cipher.decrypt(val.encode()).decode()
                st.balloons()
                st.success("✅ Terverifikasi!")
                st.link_button("👉 KLIK UNTUK ISI ABSEN", link_asli)
            else:
                st.error("Gagal mendeteksi QR Code. Coba putar layar atau pastikan cahaya cukup.")
        except:
            st.error("❌ Password Salah atau Data Rusak!")

# --- TAB 2: GENERATOR ---
with tab2:
    st.header("Cetak QR Code Siswa")
    st.warning("Gunakan kertas putih dan cetak dengan jelas.")
    
    if st.button("Tampilkan Daftar QR"):
        cipher = get_cipher("150882")
        cols = st.columns(2)
        for i, (nama, url) in enumerate(DATA_SISWA.items()):
            # Enkripsi & Buat QR
            enc = cipher.encrypt(url.encode())
            img_qr = qrcode.make(enc)
            buf = BytesIO()
            img_qr.save(buf, format="PNG")
            
            with cols[i % 2]:
                st.image(buf.getvalue(), caption=nama, use_container_width=True)
                st.download_button(f"Simpan QR {nama}", buf.getvalue(), f"{nama}.png", "image/png")
