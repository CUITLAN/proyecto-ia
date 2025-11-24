import streamlit as st
from PIL import Image
import json

st.set_page_config(page_title="Detector de Lunares", page_icon="🌙", layout="centered")

st.title("🌙 Sistema de Detección y Clasificación de Lunares")
st.subheader("Bienvenido")
st.write("Carga una imagen para comenzar el análisis.")

# Estado para manejar pasos de la interfaz
if "imagen_cargada" not in st.session_state:
    st.session_state.imagen_cargada = None

if "resultado" not in st.session_state:
    st.session_state.resultado = None

# Paso 1: Cargar Imagen
st.header("1️⃣ Cargar Imagen")
imagen_file = st.file_uploader("Selecciona una imagen del lunar", type=["jpg", "jpeg", "png"])

if imagen_file:
    st.session_state.imagen_cargada = Image.open(imagen_file)
    st.image(st.session_state.imagen_cargada, caption="Imagen cargada", width=350)

# Botón para iniciar análisis
if st.session_state.imagen_cargada:
    st.header("2️⃣ Iniciar Análisis")
    if st.button("Iniciar"):
        # JSON HARDCODEADO – reemplazar cuando el backend esté listo
        respuesta_backend = {
            "area": 12034,
            "perimetro": 845,
            "circularidad": 0.29,
            "diagnostico": "Nevus Común",
            "confianza": 0.87
        }
        st.session_state.resultado = respuesta_backend

# Mostrar resultado
if st.session_state.resultado:
    st.header("3️⃣ Resultado del Sistema")
    st.success("✔ Clasificación completada")

    st.json(st.session_state.resultado)

    diagnostico = st.session_state.resultado["diagnostico"]
    confianza = st.session_state.resultado["confianza"] * 100

    st.metric(label="Diagnóstico", value=diagnostico)
    st.metric(label="Confianza", value=f"{confianza:.2f} %")
