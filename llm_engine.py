import os
import streamlit as st
from google import genai
from google.genai import errors

def generate_content(prompt: str, system_instruction: str = None) -> str:
    """
    Fungsi universal untuk menghasilkan konten menggunakan Google GenAI SDK terbaru.
    """
    api_key = None
    try:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
        elif "GOOGLE_API_KEY" in st.secrets:
            api_key = st.secrets["GOOGLE_API_KEY"]
    except Exception:
        pass
    
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

    if not api_key:
        return "⚠️ Error: API Key Gemini belum dikonfigurasi di Streamlit Secrets."

    try:
        client = genai.Client(api_key=api_key)
        
        config = None
        if system_instruction:
            from google.genai import types
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
            )

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=config
        )
        
        return response.text
        
    except errors.APIError as e:
        return f"⚠️ Terjadi kesalahan pada sistem AI (API Error): {e}"
    except Exception as e:
        return f"⚠️ Terjadi kesalahan sistem: {str(e)}"
