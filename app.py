import streamlit as st
import qrcode
import cv2
import numpy as np
import base64
from io import BytesIO
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

# --- FUNGSI KEAMANAN ---
def get_cipher(password):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'garam_statis_123',
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return Fernet(key)

# --- DATA LINK SISWA ---
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

# --- SETUP HALAMAN ---
st.set_page_config(page_title="QR Scanner Redmi", layout="wide")

if 'rot' not in st.session_state:
    st.session_state.rot = 0

# --- CSS CUSTOM UNTUK REDMI NOTE 9 ---
st.markdown(f"""
    <style>
    /* Paksa video kamera menjadi lebar penuh */
    video {{
        width: 100% !important;
        height: auto !important;
        border-radius: 12px;
        border: 4px solid #00c853;
        transform: rotate({st.session_state.rot}deg);
    }}
    /* Perbesar tombol 'Ganti Kamera' dan 'Ambil Foto' */
    [data-testid="stCameraInputButton"] {{
        width: 100% !important;
        height: 60px !important;
        font-size: 20px !important;
    }}
    .stButton>button {{
        height: 50px;
        background-color: #f0f2f6;
    }}
    </style>
    """, unsafe_allow_html=True)

st.title("📸 Scanner Absensi")

# Kontrol Rotasi
c1, c2 = st.columns(2)
with c1:
    if st.button("🔄 Putar Tampilan"):
        st.session_state.rot = (st.session_state.rot + 90) % 360
        st.rerun()
with c2:
    if st.button("♻️ Reset"):
        st.session_state.rot = 0
        st.rerun()

st.info("💡 Klik tombol kamera di bawah. Jika kamera depan yang muncul, cari ikon ganti kamera di pojok layar.")

pwd = st.text_input("Sandi (150882):", value="150882", type="password")

# FITUR UTAMA: Kamera Input
# Pada Redmi Note 9, pastikan membuka via Chrome asli
foto = st.camera_input("Scan QR Di Sini")

if foto and pwd:
    try:
        file_bytes = np.asarray(bytearray(foto.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        det = cv2.QRCodeDetector()
        val, _, _ = det.detectAndDecode(img)
        
        if val:
            cipher = get_cipher(pwd)
            link = cipher.decrypt(val.encode()).decode()
            st.success("✅ Berhasil Didekripsi!")
            st.link_button("🔥 BUKA GOOGLE FORM", link)
        else:
            st.error("Gagal membaca QR. Pastikan cahaya terang dan posisi pas.")
    except:
        st.error("Password Salah!")
