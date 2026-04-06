import streamlit as st
from modulos.carga_datos import modulo_carga_datos

st.set_page_config(page_title="Análisis Estadístico", 
                   page_icon="📊", layout="wide")

st.title("📊 Aplicación de Probabilidad y Estadística")
st.markdown("---")

modulo_carga_datos()