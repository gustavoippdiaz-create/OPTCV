import streamlit as st
import openai

# Configuración de la página
st.set_page_config(page_title="Optimizador de CV para ATS", page_icon="💼", layout="wide")

# Título de la aplicación
st.title("🚀 Vence a la IA de los Portales de Empleo")
st.subheader("Adapta tu CV técnicamente para pasar los filtros de preselección (ATS)")

# Entrada de la API Key de OpenAI de forma segura en la barra lateral
with st.sidebar:
    st.header("⚙️ Configuración")
    api_key = st.text_input("Introduce tu OpenAI API Key:", type="password")
    st.markdown("[¿Cómo obtener una API Key?](https://platform.openai.com/)")
    st.write("---")
    st.markdown("**Consejo profesional:** Mantén tus CVs de Redes y Mecánica separados en block de notas para usarlos aquí según la oferta.")

# Crear dos columnas para la entrada de datos
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📝 Tu CV Base (Redes o Mecánica)")
    cv_texto = st.text_area(
        "Pega aquí el texto actual de tu currículum:", 
        height=300, 
        placeholder="Ej: Técnico en Administración de Redes... Experiencia en..."
    )

with col2:
    st.markdown("### 🎯 La Oferta de Trabajo")
    oferta_texto = st.text_area(
        "Pega aquí la descripción del empleo del portal web (LinkedIn, Indeed, etc.):", 
        height=300, 
        placeholder="Ej: Buscamos técnico con conocimientos en enrutamiento OSPF, mantenimiento de motores..."
    )

# Botón para procesar
if st.button("🔍 Analizar y Optimizar CV"):
    if not api_key:
        st.error("⚠️ Por favor, introduce tu API Key de OpenAI en la barra lateral izquierda.")
    elif not cv_texto or not oferta_texto:
        st.warning("⚠️ Debes rellenar ambos campos (Tu CV y la Oferta de Trabajo) para poder analizar.")
    else:
        with st.spinner("La IA está analizando los algoritmos de filtrado... Por favor espera."):
            try:
                # Configurar el cliente de OpenAI
                client = openai.OpenAI(api_key=api_key)
                
                instruccion_sistema = (
                    "Eres un reclutador experto y especialista en sistemas ATS. Tu trabajo es desglosar "
                    "las ofertas de empleo, extraer las palabras clave exactas (hard skills y soft skills) "
                    "y modificar el CV del usuario para que haga 'match' perfecto con el algoritmo, sin inventar falsedades."
                )
                
                prompt_usuario = f"""
                Analiza mi CV y la oferta de trabajo.
                
                === MI CV ===
                {cv_texto}
                
                === OFERTA ===
                {oferta_texto}
                
                Devuélveme el resultado estructurado estrictamente con este formato Markdown:
                ## 📊 Diagnóstico de Compatibilidad: [X]%
                
                ### ❌ Palabras clave que te faltan (¡Cruciales para la IA!):
                - [Palabra clave 1]
                - [Palabra clave 2]
                
                ### 🛠️ Tu Perfil Profesional Optimizado:
                [Escribe un extracto/perfil adaptado usando los términos de la oferta]
                
                ### 📈 Ajustes sugeridos para tu Experiencia / Habilidades:
                [Dime cómo reescribir frases de mi experiencia para que coincidan con lo que piden]
                """
                
                # Llamada a la API
                response = client.chat.completions.create(
                    model="gpt-4o-mini", # Usamos mini porque es ultra rápido y muy económico
                    messages=[
                        {"role": "system", "content": instruccion_sistema},
                        {"role": "user", "content": prompt_usuario}
                    ],
                    temperature=0.2
                )
                
                # Mostrar resultados
                st.success("¡Análisis completado con éxito!")
                st.markdown("---")
                st.markdown(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"Ocurrió un error con la API: {e}")