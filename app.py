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

# --- 1. CONFIG & DATA ---
SANDI_UTAMA = "150882"
DATA_SISWA = {
    "ABU KHOROIROH": "https://docs.google.com/forms/d/e/1FAIpQLSdUe2J9tSsCngKuJEqJLNACrnb2oGqQ5yKCR5N7i1iSyZWpcA/viewform?usp=pp_url&entry.1937004703=ABU+KHOROIROH&entry.1794922110=H",
    # ... (tambahkan data siswa lainnya di sini)
}

# --- 2. FUNGSI KEAMANAN ---
@st.cache_resource
def get_cipher(password):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'garam_xtkr_v4',
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return Fernet(key)

# --- 3. UI STYLE & UKURAN KAMERA ---
st.set_page_config(page_title="Scanner Besar X TKR", layout="centered")

st.markdown("""
    <style>
    /* Mengatur ukuran kotak kamera agar lebih besar */
    div[data-testid="stCameraInput"] {
        width: 100% !important;
        max-width: 600px !important; /* Sesuaikan lebar maksimal */
        margin: auto;
        border: 4px solid #1E88E5;
        border-radius: 20px;
        padding: 5px;
    }
    
    /* Mengatur preview video di dalam kotak agar lebih tinggi */
    div[data-testid="stCameraInput"] video {
        border-radius: 15px;
        min-height: 400px; /* Menambah tinggi tampilan kamera */
        object-fit: cover; /* Agar video memenuhi kotak */
    }

    /* Memperbesar tombol di dalam kamera */
    button[data-testid="stBaseButton-secondary"] {
        height: 50px !important;
        font-size: 18px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📸 Presensi QR X TKR")

tab_scan, tab_admin = st.tabs(["📌 SCAN SEKARANG", "🛠️ ADMIN"])

# --- 4. TAB SCANNER ---
with tab_scan:
    st.write("### Gunakan Kamera Belakang")
    st.info("Posisikan QR Code tepat di tengah layar kamera di bawah.")
    
    # Widget Kamera (Sekarang Tampil Lebih Besar karena CSS di atas)
    img_file = st.camera_input("Scanner Aktif")

    if img_file:
        file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(img)
        
        if data:
            try:
                cipher = get_cipher(SANDI_UTAMA)
                link = cipher.decrypt(data.encode()).decode()
                st.success("✅ Terdeteksi!")
                st.link_button("🔥 KLIK UNTUK KIRIM ABSEN", link, type="primary", use_container_width=True)
                st.balloons()
            except:
                st.error("QR Code tidak cocok.")
        else:
            st.warning("⚠️ QR tidak terbaca. Coba dekati objek atau bersihkan lensa.")

# --- 5. TAB ADMIN ---
with tab_admin:
    st.subheader("Menu Admin")
    pwd = st.text_input("Sandi Admin:", type="password", value=SANDI_UTAMA)
    
    if st.button("Download Semua QR (ZIP)"):
        if pwd == SANDI_UTAMA:
            zip_buf = BytesIO()
            with zipfile.ZipFile(zip_buf, "a", zipfile.ZIP_DEFLATED) as zf:
                for nama, url in DATA_SISWA.items():
                    encrypted = get_cipher(SANDI_UTAMA).encrypt(url.encode()).decode()
                    qr_img = qrcode.make(encrypted)
                    img_io = BytesIO()
                    qr_img.save(img_io, format="PNG")
                    zf.writestr(f"QR_{nama}.png", img_io.getvalue())
            
            st.download_button("📥 DOWNLOAD ZIP", zip_buf.getvalue(), "QR_XTKR.zip", "application/zip")
