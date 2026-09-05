import streamlit as st
from llm_engine import generate_content

st.set_page_config(page_title="Kalender Konten", page_icon="📅", layout="wide")
st.title("📅 Generator Kalender Humas & Marketing")

bulan = st.text_input("Bulan & Tahun", placeholder="September 2026")
fokus = st.text_input("Fokus Kampanye", placeholder="Edukasi Layanan CT Scan")

if st.button("Generate Kalender"):
    with st.spinner("Memproses playbook operasional harian..."):
        prompt = f"Buat kalender konten untuk bulan: {bulan}, fokus: {fokus}."
        system_instruction = """
        Buat jadwal operasional PR dan Marketing. 
        OUTPUT WAJIB 1 TABEL MARKDOWN dengan kolom:
        | ☐ | Tanggal & Momen | Program / Konten | Sub-Spesialis | Kanal | Detail Action (jam + langkah) | PIC | KPI / Target | Budget | ⚡ |
        
        - Detail Action harus berbasis jam (misal: "08.00 posting").
        - Kolom ⚡ diisi prioritas (⚡, ⚡⚡).
        - Masukkan aktivitas setoran harian/mingguan admin dan follow-up.
        Dilarang memberikan teks pengantar atau penutup. Langsung berikan tabelnya.
        """
        hasil = generate_content(prompt, system_instruction)
        st.markdown(hasil)
