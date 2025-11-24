import streamlit as st
from PIL import Image
import requests
import json

st.set_page_config(page_title="Detector de Lunares", page_icon="🌙", layout="centered")

st.title("🌙 Sistema de Detección y Clasificación de Lunares")
st.subheader("Bienvenido")
st.write("Carga una imagen para comenzar el análisis.")

if "imagen_cargada" not in st.session_state:
    st.session_state.imagen_cargada = None

if "resultado" not in st.session_state:
    st.session_state.resultado = None

# 1️⃣ CARGAR IMAGEN
st.header("1️⃣ Cargar Imagen")
imagen_file = st.file_uploader("Selecciona una imagen del lunar", type=["jpg", "jpeg", "png"])

if imagen_file:
    st.session_state.imagen_cargada = imagen_file
    img = Image.open(imagen_file)
    st.image(img, caption="Imagen cargada", width=350)

# 2️⃣ ENVIAR A BACKEND
if st.session_state.imagen_cargada:
    st.header("2️⃣ Iniciar Análisis")

    if st.button("Iniciar análisis"):
        with st.spinner("Procesando imagen, por favor espera..."):
            try:
                backend_url = "http://localhost:8000/analizar"

                files = {
                    "file": (imagen_file.name, imagen_file, imagen_file.type)
                }

                response = requests.post(backend_url, files=files)

                if response.status_code == 200:
                    st.session_state.resultado = response.json()
                else:
                    st.error("Error al comunicarse con el backend.")
            except Exception as e:
                st.error(f"Error: {str(e)}")


# 3️⃣ MOSTRAR RESULTADO
if st.session_state.resultado:
    r = st.session_state.resultado

    st.header("3️⃣ Resultado del Sistema")
    st.success("✔ Clasificación completada")

    # Mostrar JSON completo
    st.json(r)

    # CARD ELEGANTE
    st.subheader("🟦 Diagnóstico")

    diagnostico = r.get("diagnostico", "N/A")
    tipo = r.get("tipo_detectado", "N/A")
    confianza = r.get("confianza_riesgo", "N/A")

    st.markdown(
        f"""
        <div style="
            background-color:#f5f5f5;
            padding:20px;
            border-radius:12px;
            border-left: 8px solid {'#ff4d4d' if diagnostico=='MALIGNO' else '#4caf50'};
        ">
            <h3>Diagnóstico: <b>{diagnostico}</b></h3>
            <h4>Tipo detectado: {tipo}</h4>
            <h4>Confianza del sistema: {confianza}</h4>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Datos técnicos
    st.subheader("📊 Datos Técnicos")
    datos = r.get("datos_tecnicos", {})

    col1, col2, col3 = st.columns(3)

    col1.metric("Área", datos.get("Area", "N/A"))
    col2.metric("Asimetría", datos.get("Asimetria", "N/A"))
    col3.metric("Color STD", datos.get("Color", "N/A"))
