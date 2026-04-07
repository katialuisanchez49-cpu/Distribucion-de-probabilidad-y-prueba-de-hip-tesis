import streamlit as st
from modulos.carga_datos import modulo_carga_datos
from modulos.visualizacion import modulo_visualizacion

st.set_page_config(page_title="Análisis Estadístico",
                   page_icon="📊", layout="wide")

st.title("📊 Aplicación de Probabilidad y Estadística")
st.markdown("---")

st.sidebar.title("🧭 Navegación")
modulo = st.sidebar.radio("Selecciona un módulo", [
    "📂 Carga de Datos",
    "📊 Visualización"
])

if modulo == "📂 Carga de Datos":
    modulo_carga_datos()
elif modulo == "📊 Visualización":
    modulo_visualizacion()