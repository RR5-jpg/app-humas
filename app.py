import streamlit as st

st.set_page_config(
    page_title="Humas & Marketing RSPUR",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Sistem Informasi Humas & Marketing")
st.markdown("Selamat datang di panel otomatisasi operasional RSPUR.")

st.info("""
**Silakan pilih modul di *sidebar* sebelah kiri:**
1. **Siaran Pers:** Untuk generate draft rilis media.
2. **Kalender Konten:** Untuk menyusun playbook harian pemasaran.
3. **Event Planner:** Untuk merinci kebutuhan logistik medis/non-medis.

*Aplikasi ini dirancang modular. Anda bisa menambahkan fitur baru kapan saja.*
""")
