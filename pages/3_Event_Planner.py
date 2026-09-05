import streamlit as st
from llm_engine import generate_content

st.set_page_config(page_title="Event Planner", page_icon="📋", layout="wide")
st.title("📋 Event & Logistic Detailer")

nama_event = st.text_input("Nama Event", placeholder="Booth CFD Cek Jagoan")
jumlah_peserta = st.number_input("Estimasi Peserta", min_value=10, value=50, step=10)
kebutuhan = st.text_input("Layanan Medis", placeholder="Tensi, GDS, Edukasi")

if st.button("Generate Logistik"):
    with st.spinner("Menghitung rasio logistik..."):
        prompt = f"Event: {nama_event}\nPeserta: {jumlah_peserta} orang\nLayanan: {kebutuhan}"
        system_instruction = """
        Breakdown logistik event kesehatan. Berikan dalam 2 tabel markdown terpisah.
        TABEL 1: "A. Alat Medis & Bahan Habis Pakai" (No | Item | Jumlah | Keterangan).
        TABEL 2: "B. Perlengkapan Non-Medis, Promosi & ATK" (No | Item | Jumlah | Keterangan).
        Kalkulasikan jumlah barang medis sesuai jumlah peserta + cadangan.
        Tanpa basa-basi, langsung tabel.
        """
        hasil = generate_content(prompt, system_instruction)
        st.markdown(hasil)
