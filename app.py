import streamlit as st
import google.generativeai as genai

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
        with st.spinner("Analizando con Google Gemini..."):
            try:
                # Inicialización limpia
                genai.configure(api_key=api_key)
                
                # Usamos la sintaxis estándar simplificada sin prefijos molestos
                model = genai.GenerativeModel('gemini-1.5-flash')
                
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
                
                response = model.generate_content(prompt)
                
                st.success("¡Análisis completado!")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Ocurrió un error técnico: {e}")
