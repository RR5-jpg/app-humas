import os
import streamlit as st

def generate_content(prompt: str, system_instruction: str = None) -> str:
    """
    Fungsi universal dengan proteksi ganda (fallback SDK) untuk menghindari error import.
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

    # Coba gunakan SDK google-genai terbaru
    try:
        from google import genai
        from google.genai import errors
        
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
        
    except ImportError:
        pass # Lanjut ke fallback jika google-genai tidak ada
    except Exception as e:
        # Jika gagal dengan SDK baru, coba fallback ke google.generativeai lama
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            
            full_prompt = prompt
            if system_instruction:
                full_prompt = f"[INSTRUKSI SISTEM]:\n{system_instruction}\n\n[PROMPT]:\n{prompt}"
                
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(full_prompt)
            return response.text
        except Exception as e_old:
            return f"⚠️ Terjadi kesalahan pada sistem AI: {e_old}"

    # Fallback permanen jika block di atas tembus
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        full_prompt = prompt
        if system_instruction:
            full_prompt = f"[INSTRUKSI SISTEM]:\n{system_instruction}\n\n[PROMPT]:\n{prompt}"
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e2:
        return f"⚠️ Gagal memuat engine AI: {e2}"
