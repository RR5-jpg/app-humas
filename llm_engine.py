import google.generativeai as genai
import streamlit as st

def generate_content(prompt_utama, system_instruction):
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY belum diatur."
        
    genai.configure(api_key=api_key)
    full_prompt = f"[INSTRUKSI SISTEM WAJIB]:\n{system_instruction}\n\n[PERMINTAAN USER]:\n{prompt_utama}"
    
    # Menggunakan model standar gemini-pro yang pasti kompatibel dengan API key baru
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Terjadi kesalahan pada sistem AI: {e}"
