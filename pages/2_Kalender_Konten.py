import streamlit as st
import sys
import os

# Menambahkan root folder agar bisa import llm_engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from llm_engine import generate_content

st.set_page_config(page_title="Kalender Konten", layout="wide")
st.title("📅 Kalender Konten Humas RS")

# ─── Input Form ───────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    topik = st.text_input(
        "🎯 Fokus Tema / Kampanye",
        "Kampanye Kesehatan Jantung & Preventif"
    )
    target_channel = st.selectbox(
        "📡 Kanal Utama",
        [
            "Semua Kanal",
            "Instagram & Facebook",
            "Website & Blog",
            "LinkedIn & Media Lokal",
            "TikTok & YouTube Shorts",
        ],
    )

with col2:
    durasi = st.radio(
        "📆 Durasi Kalender",
        ["1 Bulan (Bulanan)", "12 Bulan (Tahunan)"],
        horizontal=True,
    )
    bulan_mulai = st.selectbox(
        "Bulan Mulai",
        [
            "Januari", "Februari", "Maret", "April",
            "Mei", "Juni", "Juli", "Agustus",
            "September", "Oktober", "November", "Desember",
        ],
        index=8,  # default September
    )
    tahun = st.number_input("Tahun", min_value=2025, max_value=2035, value=2026)

# ─── Generate ─────────────────────────────────────────────────
if st.button("🚀 Generate Kalender", type="primary"):

    with st.spinner("Sedang menyusun jadwal dan strategi konten..."):

        if "Tahunan" in durasi:
            scope = "12 bulan penuh (1 tahun)"
            extra_instruction = (
                f"Susun untuk 12 bulan berturut-turut mulai dari {bulan_mulai} {tahun}. "
                "Setiap bulan tampilkan 4-6 kegiatan utama berbentuk daftar poin (bullet)."
            )
        else:
            scope = "1 bulan penuh (bulanan)"
            extra_instruction = (
                f"Susun untuk 1 bulan penuh mulai {bulan_mulai} {tahun}. "
                "Tampilkan kegiatan harian dalam bentuk daftar poin (bullet) secara berurutan."
            )

        prompt_user = (
            f"Buatkan kalender konten Humas Rumah Sakit.\n"
            f"- Tema/Kampanye : {topik}\n"
            f"- Kanal target : {target_channel}\n"
            f"- Durasi       : {scope}\n"
            f"- {extra_instruction}\n\n"
            "ATURAN MUTLAK FORMAT OUTPUT:\n"
            "1. DILARANG KERAS menggunakan karakter garis tegak lurus (|) atau tabel markdown apa pun.\n"
            "2. Gunakan heading (###) untuk nama bulan.\n"
            "3. Gunakan bullet list (-) untuk setiap baris jadwal.\n"
            "4. Format baris wajib seperti ini: - **[DD Mmm]** : Judul Konten (Kanal) - Deskripsi singkat.\n"
            "5. Di bagian akhir, berikan 3-5 poin 'Tips Eksekusi'.\n"
        )

        system_msg = (
            "Anda adalah PR & Content Manager Rumah Sakit profesional. "
            "Tugas Anda menyusun kalender konten yang bersih, terstruktur, dan sangat mudah dibaca di layar HP. "
            "Jangan pernah membuat tabel markdown karena akan merusak tampilan di perangkat seluler."
        )

        hasil = generate_content(prompt_user, system_msg)

    # ─── Tampilkan Hasil ──────────────────────────────────────
    st.markdown("---")
    st.subheader("📋 Hasil Kalender Konten")
    
    # Bungkus dalam container dengan markdown bersih agar tampil rapi di HP
    st.markdown(hasil)

    # Tombol download
    st.download_button(
        "⬇️ Download sebagai Markdown",
        data=hasil,
        file_name=f"kalender_konten_{bulan_mulai.lower()}_{tahun}.md",
        mime="text/markdown",
    )
