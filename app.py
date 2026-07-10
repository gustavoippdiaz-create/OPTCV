import streamlit as st
import requests
import json

# Configuración de la página
st.set_page_config(page_title="Optimizador de CV para ATS", page_icon="💼", layout="wide")

st.title("🚀 Vence a la IA de los Portales de Empleo")
st.subheader("Adapta tu CV técnicamente para pasar los filtros de preselección (ATS)")

# Entrada de la API Key de Google
with st.sidebar:
    st.header("⚙️ Configuración")
    api_key = st.text_input("Introduce tu Google Gemini API Key:", type="password")
    st.markdown("[👉 Consigue tu API Key GRATIS aquí](https://aistudio.google.com/)")
    st.write("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📝 Tu CV Base (Redes o Mecánica)")
    cv_texto = st.text_area("Pega aquí el texto actual de tu currículum:", height=300)

with col2:
    st.markdown("### 🎯 La Oferta de Trabajo")
    oferta_texto = st.text_area("Pega aquí la descripción del empleo:", height=300)

if st.button("🔍 Analizar y Optimizar CV"):
    if not api_key:
        st.error("⚠️ Por favor, introduce tu API Key de Google en la barra lateral.")
    elif not cv_texto or not oferta_texto:
        st.warning("⚠️ Debes rellenar ambos campos.")
    else:
        with st.spinner("Analizando con Google Gemini mediante conexión directa..."):
            try:
                # Usamos la API estable v1 de Google saltándonos las librerías antiguas de Streamlit
                url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
                
                prompt = f"""
                Actúa como experto en reclutamiento y sistemas ATS. Analiza mi CV y la oferta de trabajo para optimizarlo sin mentir.
                
                === MI CV ===
                {cv_texto}
                
                === OFERTA ===
                {oferta_texto}
                
                Devuélveme el resultado estructurado en Markdown con:
                ## 📊 Diagnóstico de Compatibilidad: [X]%
                ### ❌ Palabras clave que te faltan:
                ### 🛠️ Tu Perfil Profesional Optimizado:
                ### 📈 Ajustes sugeridos para tu Experiencia / Habilidades:
                """
                
                payload = {
                    "contents": [
                        {
                            "parts": [
                                {"text": prompt}
                            ]
                        }
                    ]
                }
                
                headers = {'Content-Type': 'application/json'}
                
                response = requests.post(url, headers=headers, data=json.dumps(payload))
                
                if response.status_code == 200:
                    response_data = response.json()
                    texto_ia = response_data['candidates'][0]['content']['parts'][0]['text']
                    st.success("¡Análisis completado!")
                    st.markdown("---")
                    st.markdown(texto_ia)
                else:
                    st.error(f"Error del servidor de Google (Código {response.status_code}): {response.text}")
                
            except Exception as e:
                st.error(f"Ocurrió un error técnico: {e}")
