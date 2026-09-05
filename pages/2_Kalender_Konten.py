import streamlit as st
import sys
import os

# Menambahkan root folder agar bisa import llm_engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from llm_engine import generate_content

st.set_page_config(page_title="Kalender Konten", layout="wide")

st.title("📅 Kalender Konten Humas RS")

# Input form untuk kalender
topik = st.text_input("Fokus Tema / Bulan", "Kampanye Kesehatan Jantung & Preventif")
target_channel = st.selectbox("Kanal Utama", ["Semua Kanal", "Instagram & Facebook", "Website & Blog", "LinkedIn & Media Lokal"])

if st.button("Generate Kalender"):
    with st.spinner("Sedang menyusun jadwal dan strategi konten..."):
        prompt_user = f"Buatlah jadwal kalender konten bulanan untuk Rumah Sakit dengan fokus tema: {topik}, target kanal utama: {target_channel}."
        system_msg = "Anda adalah PR Manager Rumah Sakit profesional. Berikan hasil output dalam bentuk uraian poin per tanggal atau ringkasan paragraf yang rapi dan mudah dibaca di layar HP, HINDARI penggunaan tabel markdown mentah (garis vertikal |) agar tidak berantakan."
        
        hasil = generate_content(prompt_user, system_msg)
        
        st.subheader("Hasil Kalender Konten:")
        st.markdown(hasil)
