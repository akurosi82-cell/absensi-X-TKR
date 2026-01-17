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

# --- PENGATURAN STATE ---
if 'rotasi' not in st.session_state:
    st.session_state.rotasi = 0

# --- UI DAN CSS ---
st.set_page_config(page_title="Scanner QR Sekolah", layout="wide")

st.markdown(f"""
    <style>
    /* Membuat video kamera lebar dan merespons rotasi */
    video {{
        width: 100% !important;
        max-width: 600px;
        height: auto !important;
        border: 5px solid #007bff;
        border-radius: 20px;
        transform: rotate({st.session_state.rotasi}deg);
        transition: transform 0.3s ease;
        margin-bottom: 20px;
    }}
    /* Menghilangkan label default kamera */
    div[data-testid="stCameraInput"] > label {{
        display: none;
    }}
    .stButton>button {{ width: 100%; height: 50px; border-radius: 12px; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Scanner Absensi")

tab1, tab2 = st.tabs(["📲 Scanner", "🖨️ Cetak QR"])

with tab1:
    # Kontrol Kamera
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Putar Tampilan"):
            st.session_state.rotasi = (st.session_state.rotasi + 90) % 360
            st.rerun()
    with col2:
        if st.button("♻️ Reset Kamera"):
            st.session_state.rotasi = 0
            st.rerun()
            
    st.write("Jika kamera salah (depan/belakang), gunakan pengaturan browser Anda.")
    
    pwd = st.text_input("Password (150882):", value="150882", type="password")
    
    # Komponen Kamera Utama
    foto = st.camera_input("Ambil Foto QR")

    if foto and pwd:
        try:
            file_bytes = np.asarray(bytearray(foto.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, 1)
            det = cv2.QRCodeDetector()
            val, _, _ = det.detectAndDecode(img)
            
            if val:
                cipher = get_cipher(pwd)
                link = cipher.decrypt(val.encode()).decode()
                st.balloons()
                st.success("✅ Berhasil!")
                st.link_button("👉 BUKA FORM GOOGLE", link)
            else:
                st.error("Gagal mendeteksi QR. Coba putar atau perbaiki pencahayaan.")
        except:
            st.error("❌ Password salah atau data QR tidak valid!")

with tab2:
    st.header("Generator QR")
    if st.button("Tampilkan QR Siswa"):
        cipher = get_cipher("150882")
        cols = st.columns(2)
        for i, (nama, url) in enumerate(DATA_SISWA.items()):
            enc = cipher.encrypt(url.encode())
            qr_img = qrcode.make(enc)
            buf = BytesIO()
            qr_img.save(buf, format="PNG")
            with cols[i % 2]:
                st.image(buf.getvalue(), caption=nama, use_container_width=True)
                st.download_button(f"Unduh {nama}", buf.getvalue(), f"{nama}.png")
