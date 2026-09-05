import google.generativeai as genai
import streamlit as st

def generate_content(prompt_utama, system_instruction):
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY belum diatur di Secrets."
        
    genai.configure(api_key=api_key)
    
    full_prompt = f"[INSTRUKSI SISTEM WAJIB]:\n{system_instruction}\n\n[PERMINTAAN USER]:\n{prompt_utama}"
    
    # Otomatis mencoba model dari yang terbaru sampai versi legacy
    daftar_model = ['gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-pro', 'gemini-1.0-pro']
    
    for nama_model in daftar_model:
        try:
            model = genai.GenerativeModel(nama_model)
            response = model.generate_content(full_prompt)
            return response.text
        except Exception:
            continue
            
    return "Gagal: Token API Anda tidak mendukung model yang tersedia."
