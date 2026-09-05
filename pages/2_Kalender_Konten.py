import streamlit as st
import sys
import os

# Menambahkan root folder agar bisa import llm_engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from llm_engine import generate_content

st.set_page_config(page_title="Kalender Konten", layout="wide")
st.title("📅 Kalender Konten Humas RS")
st.caption("Generator jadwal dan strategi konten media sosial serta publikasi rumah sakit secara otomatis.")

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
st.divider()

if st.button("🚀 Generate Kalender", type="primary", use_container_width=True):

    with st.spinner("Sedang menyusun jadwal dan strategi konten secara komprehensif..."):

        if "Tahunan" in durasi:
            scope = "12 bulan penuh (1 tahun)"
            extra_instruction = (
                f"Susun untuk 12 bulan berturut-turut mulai dari {bulan_mulai} {tahun}. "
                "Setiap bulan tampilkan 4-6 kegiatan utama berbentuk daftar poin (bullet) lengkap dengan PIC dan target."
            )
        else:
            scope = "1 bulan penuh (bulanan)"
            extra_instruction = (
                f"Susun untuk 1 bulan penuh mulai {bulan_mulai} {tahun}. "
                "Tampilkan kegiatan harian dalam bentuk daftar poin (bullet) secara berurutan dari tanggal 1 hingga akhir bulan."
            )

        prompt_user = (
            f"Buatkan kalender konten Humas Rumah Sakit secara lengkap dan detail.\n"
            f"- Tema/Kampanye : {topik}\n"
            f"- Kanal target : {target_channel}\n"
            f"- Durasi       : {scope}\n"
            f"- {extra_instruction}\n\n"
            "ATURAN MUTLAK FORMAT OUTPUT:\n"
            "1. DILARANG KERAS menggunakan karakter garis tegak lurus (|) atau tabel markdown apa pun agar tidak pecah di HP.\n"
            "2. Gunakan heading (###) untuk nama bulan.\n"
            "3. Gunakan bullet list (-) untuk setiap baris jadwal.\n"
            "4. Format baris wajib seperti ini: - **[DD Mmm]** : Judul Konten — Kanal — Deskripsi singkat & PIC.\n"
            "5. Di bagian akhir, berikan 3-5 poin 'Tips Eksekusi dan Evaluasi Kampenyekita'.\n"
        )

        system_msg = (
            "Anda adalah PR & Content Manager Rumah Sakit profesional dengan pengalaman lebih dari 10 tahun. "
            "Tugas Anda menyusun kalender konten yang sangat mendalam, terstruktur rapi, kronologis, dan nyaman dibaca di layar perangkat seluler. "
            "Jangan pernah menggunakan tabel markdown."
        )

        hasil = generate_content(prompt_user, system_msg)

    # ─── Tampilkan Hasil ──────────────────────────────────────
    st.markdown("---")
    st.subheader("📋 Hasil Kalender Konten")
    st.markdown(hasil)

    # Tombol download
    st.divider()
    st.download_button(
        "⬇️ Download sebagai Markdown",
        data=hasil,
        file_name=f"kalender_konten_{bulan_mulai.lower()}_{tahun}.md",
        mime="text/markdown",
    )
