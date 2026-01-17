import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, WebRtcMode
import cv2
import numpy as np
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

# --- FUNGSI KEAMANAN ---
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

# --- LOGIKA SCANNER ---
class QRScanner(VideoTransformerBase):
    def __init__(self):
        self.detector = cv2.QRCodeDetector()
        self.last_val = None

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        val, _, _ = self.detector.detectAndDecode(img)
        
        if val:
            self.last_val = val
        return img

st.title("🛡️ Scanner Absensi Pro")
pwd = st.text_input("Sandi Sistem:", value="150882", type="password")

st.info("Klik 'START' lalu pilih kamera belakang pada menu 'Select Device' di bawah layar video.")

# --- KOMPONEN KAMERA ---
ctx = webrtc_streamer(
    key="qr-scanner",
    mode=WebRtcMode.SENDRECV,
    video_transformer_factory=QRScanner,
    # Memaksa preferensi kamera belakang pada HP
    media_stream_constraints={"video": {"facingMode": "environment"}, "audio": False},
    async_processing=True,
)

# --- PROSES HASIL SCAN ---
if ctx.video_transformer:
    hasil_qr = ctx.video_transformer.last_val
    if hasil_qr:
        try:
            cipher = get_cipher(pwd)
            link_asli = cipher.decrypt(hasil_qr.encode()).decode()
            
            st.success("✅ QR Terdeteksi!")
            st.link_button("🚀 KLIK UNTUK ABSEN", link_asli, type="primary", use_container_width=True)
            
            # Reset hasil agar tidak looping terus menerus
            ctx.video_transformer.last_val = None
        except:
            st.error("Gagal dekripsi. Pastikan sandi benar.")
