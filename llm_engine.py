import google.generativeai as genai
import streamlit as st

def generate_content(prompt_utama, system_instruction):
    # Mengambil API key dari secrets Streamlit Cloud
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY belum diatur di Streamlit Secrets."
        
    genai.configure(api_key=api_key)
    
    # Memilih model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    full_prompt = f"""
    [INSTRUKSI SISTEM WAJIB]:
    {system_instruction}
    
    [PERMINTAAN USER]:
    {prompt_utama}
    """
    
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Terjadi kesalahan pada sistem AI: {e}"

