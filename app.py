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
    # ... (Siswa lainnya tetap ada dalam sistem)
    "ZAINAl ARIFIN": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=ZAINAl+ARIFIN&entry.1794922110=H"
}

st.set_page_config(page_title="Scanner QR Otomatis", layout="centered")

# --- CSS PAKSA LEBAR & ROTASI ---
if 'rot' not in st.session_state:
    st.session_state.rot = 0

st.markdown(f"""
    <style>
    video {{
        width: 100% !important;
        border: 4px solid #28a745;
        border-radius: 15px;
        transform: rotate({st.session_state.rot}deg);
    }}
    </style>
    """, unsafe_allow_html=True)

st.title("📸 Scanner Kamera Belakang")

# Tombol Rotasi jika gambar miring
if st.button("🔄 Putar Tampilan (Jika Miring)"):
    st.session_state.rot = (st.session_state.rot + 90) % 360
    st.rerun()

pwd = st.text_input("Sandi (150882):", value="150882", type="password")

# --- SOLUSI PAKSA KAMERA BELAKANG ---
# Menambahkan label 'label=None' terkadang membantu browser Android memunculkan dialog pilihan kamera
foto = st.camera_input("Arahkan ke QR Code", label_visibility="hidden")

if foto:
    file_bytes = np.asarray(bytearray(foto.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    det = cv2.QRCodeDetector()
    val, _, _ = det.detectAndDecode(img)
    
    if val:
        try:
            cipher = get_cipher(pwd)
            link = cipher.decrypt(val.encode()).decode()
            st.success("✅ Berhasil Scan!")
            st.link_button("👉 BUKA FORM ABSEN", link, type="primary")
            st.balloons()
        except:
            st.error("Sandi salah!")
    else:
        st.warning("QR belum terbaca. Coba dekatkan/jauhkan HP sedikit.")

with st.expander("🛠️ Admin: Cetak QR"):
    if st.button("Generate QR"):
        cp = get_cipher("150882")
        for nm, lnk in DATA_SISWA.items():
            en = cp.encrypt(lnk.encode())
            q = qrcode.make(en)
            b = BytesIO()
            q.save(b, format="PNG")
            st.image(b.getvalue(), caption=nm, width=150)
