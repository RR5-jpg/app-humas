import streamlit as st
import sys
import os

# Menambahkan root folder agar bisa import llm_engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from llm_engine import generate_content

# ─── KONFIGURASI HALAMAN ───
st.set_page_config(page_title="Event Planner Kesehatan", page_icon="📋", layout="wide")
st.title("📋 Event & Logistic Detailer — Kesehatan")
st.caption("Generator rencana kegiatan, rundown, alur peserta, dan logistik event kesehatan secara otomatis.")

# ─── INPUT SECTION ───
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📌 Detail Event")
    nama_event = st.text_input("Nama Event", placeholder="Booth CFD Cek Jagoan")
    
    col_a, col_b = st.columns(2)
    with col_a:
        jenis_event = st.selectbox("Jenis Event", [
            "Booth CFD (Car Free Day)",
            "Penyuluhan / Seminar Kesehatan",
            "Screening Massal",
            "Bakti Sosial",
            "Health Fair / Pameran Kesehatan",
            "Posyandu / Posbindu",
            "Senam + Cek Kesehatan",
            "Lainnya"
        ])
        jumlah_peserta = st.number_input("Estimasi Peserta", min_value=10, max_value=2000, value=50, step=10)
    with col_b:
        durasi = st.selectbox("Durasi Kegiatan", [
            "2 jam", "3 jam", "4 jam", "5 jam", "6 jam", "Full day (8 jam)"
        ])
        target_audience = st.multiselect(
            "Target Peserta",
            ["Umum / Semua Usia", "Lansia", "Remaja / Mahasiswa",
             "Ibu & Anak", "Pekerja Kantoran", "Komunitas Olahraga"],
            default=["Umum / Semua Usia"]
        )

with col_right:
    st.subheader("🩺 Layanan & Fokus")
    kebutuhan_medis = st.multiselect(
        "Layanan Medis",
        ["Cek Tekanan Darah (Tensi)",
         "Cek Gula Darah Sewaktu (GDS)",
         "Cek Kolesterol",
         "Cek Asam Urat",
         "Pengukuran BB/TB & IMT",
         "Konsultasi Dokter",
         "HRV / Stress Screening",
         "Edukasi Gizi",
         "Edukasi PHBS",
         "Pemeriksaan Mata",
         "Vaksinasi"],
        default=["Cek Tekanan Darah (Tensi)", "Cek Gula Darah Sewaktu (GDS)", "Edukasi PHBS"]
    )
    
    st.subheader("🎯 Tujuan Utama")
    tujuan = st.text_area(
        "Apa goal utama event ini?",
        placeholder="Contoh: Meningkatkan awareness deteksi dini PTM, branding produk kesehatan, edukasi gaya hidup sehat...",
        height=80
    )

# ─── OPSI TAMBAHAN ───
with st.expander("⚙️ Opsi Tambahan (Opsional)"):
    col_x, col_y, col_z = st.columns(3)
    with col_x:
        ada_games = st.checkbox("Sertakan ide games/aktivitas interaktif", value=True)
        ada_souvenir = st.checkbox("Sertakan rekomendasi souvenir/giveaway", value=True)
    with col_y:
        jumlah_tim = st.number_input("Jumlah Tim/Panitia Tersedia", min_value=2, max_value=50, value=8)
        ada_senam = st.checkbox("Ada sesi senam/olahraga bersama", value=False)
    with col_z:
        tema_khusus = st.text_input("Tema/Fokus Khusus (opsional)", placeholder="Contoh: Hari Diabetes Sedunia")
        budget_hint = st.selectbox("Indikasi Budget", ["Terbatas / Minimalis", "Menengah", "Cukup Fleksibel"])

# ─── GENERATE ───
st.divider()

if st.button("🚀 Generate Rencana Lengkap", type="primary", use_container_width=True):
    if not nama_event.strip():
        st.warning("⚠️ Mohon isi **Nama Event** terlebih dahulu.")
    else:
        with st.spinner("Menyusun rencana kegiatan, rundown, dan logistik..."):
            
            prompt = f"""
Nama Event    : {nama_event}
Jenis         : {jenis_event}
Peserta       : {jumlah_peserta} orang
Durasi        : {durasi}
Target        : {', '.join(target_audience)}
Layanan Medis : {', '.join(kebutuhan_medis)}
Tujuan Utama  : {tujuan if tujuan.strip() else 'Edukasi & screening kesehatan umum'}
Tim Tersedia  : {jumlah_tim} orang
Tema Khusus   : {tema_khusus if tema_khusus.strip() else 'Tidak ada'}
Budget        : {budget_hint}
Games/Aktivitas: {'Ya' if ada_games else 'Tidak perlu'}
Souvenir      : {'Ya' if ada_souvenir else 'Tidak perlu'}
Senam Bersama : {'Ya' if ada_senam else 'Tidak'}
"""

            system_instruction = """
Kamu adalah Event Planner profesional khusus event kesehatan masyarakat Indonesia.
Berdasarkan data input, buatkan RENCANA LENGKAP dalam format Markdown dengan struktur berikut:

## 1. 💡 IDE & KONSEP KEGIATAN
- Berikan 3-5 ide aktivitas utama yang relevan dengan jenis event dan target peserta.
- Jelaskan singkat mengapa aktivitas tersebut cocok.

## 2. 🗓️ RUNDOWN / SUSUNAN ACARA
Gunakan daftar poin (bullet list) terstruktur, DILARANG menggunakan tabel markdown garis vertikal (|).
Format:
- **[Waktu]** : **[Nama Kegiatan]** — Deskripsi/PIC/Keterangan singkat.

## 3. 🚶 ALUR PESERTA (PARTICIPANT JOURNEY)
Buat alur langkah demi langkah menggunakan numbered list:
1. Datang & Registrasi...
2. Skrining Awal...
dst.

## 4. 👥 PEMBAGIAN TIM & TUGAS
Gunakan daftar poin terstruktur, DILARANG menggunakan tabel markdown.
Format:
- **[Peran / Divisi]** ([Jumlah] orang) : Tugas utama meliputi...

## 5. 🏥 LOGISTIK — ALAT MEDIS & BAHAN HABIS PAKAI
Gunakan daftar poin terstruktur dengan kalkulasi jumlah yang realistis (cadangan 15-20%):
- **[Nama Item]** : [Jumlah] [Satuan] — (Keterangan)

## 6. 📦 LOGISTIK — NON-MEDIS, PROMOSI & ATK
Gunakan daftar poin terstruktur:
- **[Nama Item]** : [Jumlah] [Satuan] — (Keterangan)

## 7. ⚠️ ANTISIPASI & TIPS LAPANGAN
- 3-5 poin singkat potensi masalah dan solusinya.

ATURAN MUTLAK:
- DILARANG KERAS menggunakan karakter garis tegak lurus (|) atau tabel markdown apa pun agar tampilan di HP tidak hancur.
- Gunakan bahasa Indonesia yang ringkas dan actionable.
"""

            hasil = generate_content(prompt, system_instruction)
            st.markdown(hasil)

        # Tombol download hasil
        st.divider()
        st.download_button(
            label="📥 Download Rencana (Markdown)",
            data=hasil,
            file_name=f"rencana_{nama_event.replace(' ', '_').lower()}.md",
            mime="text/markdown"
        )
