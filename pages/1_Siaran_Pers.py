import streamlit as st
from llm_engine import generate_content

st.set_page_config(page_title="Siaran Pers", page_icon="📰", layout="wide")
st.title("📰 Generator Siaran Pers Resmi")

with st.form("pr_form"):
    tema = st.text_input("Tema/Judul Kegiatan", placeholder="Sinergi RSPUR dan Jasa Raharja")
    tanggal_lokasi = st.text_input("Lokasi dan Tanggal", placeholder="BANDA ACEH, ...")
    komitmen = st.text_area("Poin-poin Komitmen (pisahkan dengan koma/baris baru)")
    hadirin = st.text_area("Daftar Hadir (Pisahkan Manajemen RS dan Mitra)")
    
    submit = st.form_submit_button("Generate Dokumen")

if submit and tema:
    with st.spinner("Menyusun siaran pers..."):
        prompt = f"Tema: {tema}\nLokasi/Tanggal: {tanggal_lokasi}\nKomitmen: {komitmen}\nHadirin: {hadirin}"
        system_instruction = """
        Tulis Siaran Media Resmi untuk Rumah Sakit.
        STRUKTUR WAJIB:
        1. Header: "HUMAS RSPUR | Rumah Sakit Pertamedika Ummi Rosnati | SIARAN MEDIA RESMI"
        2. Judul Besar (Kapital)
        3. Lokasi (huruf kapital) - Paragraf pembuka.
        4. Poin-poin komitmen (gunakan numbered list).
        5. "PROSESI PENANDATANGANAN/KEGIATAN DIHADIRI OLEH:" beserta daftarnya terbagi atas Manajemen RSPUR dan Pihak Mitra.
        6. Paragraf penutup (call-to-action).
        7. Footer: "Disusun oleh: HUMAS RSPUR"
        Gaya bahasa formal dan jurnalistik. Tanpa narasi basa-basi.
        """
        hasil = generate_content(prompt, system_instruction)
        st.markdown(hasil)
