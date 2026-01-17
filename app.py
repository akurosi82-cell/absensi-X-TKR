import streamlit as st
import cv2
import numpy as np
import base64
from io import BytesIO
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

# --- FUNGSI KEAMANAN (Sama seperti sebelumnya) ---
@st.cache_resource
def get_cipher(password):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'garam_statis_123',
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return Fernet(key)

st.set_page_config(page_title="Scanner QR Belakang", layout="centered")

# --- JAVASCRIPT UNTUK MEMAKSA KAMERA BELAKANG ---
# Script ini mencoba mencari elemen video dan mengatur facingMode ke environment
st.components.v1.html(
    """
    <script>
    const interval = setInterval(() => {
        const videos = window.parent.document.querySelectorAll("video");
        if (videos.length > 0) {
            videos.forEach(video => {
                if (video.srcObject) {
                    const tracks = video.srcObject.getVideoTracks();
                    tracks.forEach(track => {
                        if (track.getConstraints().facingMode !== 'environment') {
                            track.applyConstraints({
                                facingMode: { exact: 'environment' }
                            }).catch(e => {
                                // Jika 'exact' gagal (misal di PC), coba mode environment biasa
                                track.applyConstraints({ facingMode: 'environment' });
                            });
                        }
                    });
                }
            });
        }
    }, 1000);
    </script>
    """,
    height=0,
)

st.title("📸 Scanner Kamera Belakang")

# --- UI INSTRUKSI ---
st.warning("Jika kamera depan masih aktif, klik tombol 'Ganti Kamera' yang muncul di layar jendela kamera Anda.")

pwd = st.text_input("Sandi (150882):", value="150882", type="password")

# Widget Kamera
foto = st.camera_input("Scan QR Code Siswa")

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
            st.error("Gagal dekripsi. Sandi mungkin salah.")
    else:
        st.info("Dekatkan QR Code ke kamera agar fokus.")

# --- BAGIAN ADMIN ---
with st.expander("🛠️ Admin: Cetak QR"):
    st.write("Gunakan bagian ini untuk membuat QR Code terenkripsi.")
    # (Kode generator tetap sama seperti sebelumnya)
