import google.generativeai as genai
import streamlit as st

def generate_content(prompt_utama, system_instruction):
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY belum diatur."
        
    genai.configure(api_key=api_key)
    full_prompt = f"[INSTRUKSI SISTEM WAJIB]:\n{system_instruction}\n\n[PERMINTAAN USER]:\n{prompt_utama}"
    
    # Cari model yang mendukung generateContent secara otomatis dari akun Anda
    try:
        model_terpilih = None
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                model_terpilih = m.name
                break
                
        if not model_terpilih:
            return "Error: Tidak ada model AI yang tersedia untuk API key ini."
            
        model = genai.GenerativeModel(model_terpilih)
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Terjadi kesalahan pada sistem AI: {e}"
