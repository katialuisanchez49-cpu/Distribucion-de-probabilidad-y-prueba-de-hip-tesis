import streamlit as st
from modulos.carga_datos import modulo_carga_datos
from modulos.visualizacion import modulo_visualizacion
from modulos.prueba_z import modulo_prueba_z

st.set_page_config(page_title="Análisis Estadístico",
                   page_icon="📃", layout="wide")

st.title("Aplicación de Probabilidad y Estadística")
st.markdown("---")

st.sidebar.title("Navegación")
modulo = st.sidebar.radio("Selecciona un módulo", [
    "Carga de Datos",
    "Visualización",
    "Prueba Z"
])

if modulo == "Carga de Datos":
    modulo_carga_datos()
elif modulo == "Visualización":
    modulo_visualizacion()
elif modulo == "Prueba Z":
    modulo_prueba_z()

# CSS personalizado para estilizar las pestañas
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab-list"] button {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #31333f;
        font-weight: bold;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #ff4b4b;
        color: white;
    }
    .stTabs [data-baseweb="tab-list"] button:hover {
        background-color: #e0e2e6;
        color: #31333f;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"]:hover {
        background-color: #ff4b4b;
        color: white;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        border-radius: 0 0 4px 4px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)
