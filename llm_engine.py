import google.generativeai as genai
import streamlit as st

def generate_content(prompt_utama, system_instruction):
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY belum diatur."
        
    genai.configure(api_key=api_key)
    full_prompt = f"[INSTRUKSI SISTEM WAJIB]:\n{system_instruction}\n\n[PERMINTAAN USER]:\n{prompt_utama}"
    
    # Menggunakan model gemini-1.5-flash dengan format yang didukung penuh API key standar
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        try:
            # Fallback jika model flash utama menolak
            model_alt = genai.GenerativeModel('gemini-1.5-pro')
            response_alt = model_alt.generate_content(full_prompt)
            return response_alt.text
        except Exception as err:
            return f"Terjadi kesalahan pada sistem AI: {err}"
