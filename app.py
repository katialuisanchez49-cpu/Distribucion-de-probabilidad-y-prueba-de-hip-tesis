import streamlit as st
from modulos.carga_datos import modulo_carga_datos
from modulos.visualizacion import modulo_visualizacion
from modulos.prueba_z import modulo_prueba_z
from modulos.asistente_ia import modulo_asistente_ia

st.set_page_config(
    page_title="Análisis Estadístico",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
/* ── Botones ── */
div.stButton > button {
    background-color: #c9a84c;
    color: #1a2744;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-size: 15px;
    font-weight: 700;
    transition: 0.3s;
    width: 100%;
}
div.stButton > button:hover {
    background-color: #a8872e;
    color: #ffffff;
}

/* ── Inputs ── */
div[data-baseweb="input"] input,
div[data-baseweb="select"] {
    border-radius: 8px !important;
    border: 1.5px solid #c9a84c !important;
    background-color: #fafaf8 !important;
    color: #1a2744 !important;
    padding: 6px 12px !important;
}

/* ── Métricas ── */
div[data-testid="metric-container"] {
    background-color: #1a2744;
    border: 1.5px solid #c9a84c;
    border-radius: 10px;
    padding: 12px 16px;
    text-align: center;
    color: #ffffff !important;
}
div[data-testid="metric-container"] label {
    color: #c9a84c !important;
    font-weight: 600;
}
div[data-testid="metric-container"] div {
    color: #ffffff !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #1a2744;
}
section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* ── Pestañas sidebar ── */
section[data-testid="stSidebar"] div[data-baseweb="radio"] label {
    display: block;
    background-color: #243156;
    border: 1.5px solid #c9a84c;
    border-radius: 10px;
    padding: 10px 16px;
    margin: 6px 0;
    font-size: 15px;
    font-weight: 500;
    color: #ffffff !important;
    cursor: pointer;
    transition: 0.2s;
}
section[data-testid="stSidebar"] div[data-baseweb="radio"] label:hover {
    background-color: #c9a84c;
    color: #1a2744 !important;
}

/* ── Encabezados sombreados ── */
h1 {
    background-color: #1a2744;
    border-left: 5px solid #c9a84c;
    border-radius: 6px;
    padding: 10px 18px;
    color: #ffffff !important;
    font-size: 1.9rem;
}
h2 {
    background-color: rgba(26, 39, 68, 0.85);
    border-left: 4px solid #c9a84c;
    border-radius: 6px;
    padding: 8px 14px;
    color: #ffffff !important;
}
h3 {
    background-color: rgba(26, 39, 68, 0.6);
    border-left: 3px solid #c9a84c;
    border-radius: 6px;
    padding: 6px 12px;
    color: #ffffff !important;
}

/* ── Pestañas internas ── */
div[data-baseweb="tab-list"] button {
    background-color: #1a2744 !important;
    color: #ffffff !important;
    border-radius: 8px 8px 0 0 !important;
    font-weight: 500 !important;
    border: 1px solid #c9a84c !important;
    margin-right: 4px !important;
}
div[data-baseweb="tab-list"] button[aria-selected="true"] {
    background-color: #c9a84c !important;
    color: #1a2744 !important;
    border-color: #c9a84c !important;
    font-weight: 700 !important;
}
div[data-baseweb="tab-list"] button:hover {
    background-color: #c9a84c !important;
    color: #1a2744 !important;
}

/* ── Espaciado ── */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──
st.sidebar.markdown("""
<div style='text-align:center; padding: 10px 0 5px;'>
    <span style='font-size:40px;'>📊</span>
    <p style='color:#c9a84c; font-weight:700; font-size:16px; margin:4px 0;'>
        Análisis Estadístico
    </p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<p style='color:#c9a84c; font-weight:700; "
    "font-size:13px; margin-bottom:4px; letter-spacing:1px;'>NAVEGACIÓN</p>",
    unsafe_allow_html=True
)

modulo = st.sidebar.radio("Modulos", [
    "📂  Carga de Datos",
    "📊  Visualización",
    "🧪  Prueba Z",
    "🤖  Asistente IA"
], label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='font-size:12px; color:#ffffff; padding: 4px 0;'>
    <p style='margin:2px 0; color:#c9a84c;'>📘 Probabilidad y Estadística</p>
    <p style='margin:2px 0;'>🐍 Python · Streamlit · Gemini</p>
</div>
""", unsafe_allow_html=True)

# ── Módulos ──

st.title("📊 Aplicación de Probabilidad y Estadística")
st.markdown("---")

if modulo == "📂  Carga de Datos":
    modulo_carga_datos()
elif modulo == "📊  Visualización":
    modulo_visualizacion()
elif modulo == "🧪  Prueba Z":
    modulo_prueba_z()
elif modulo == "🤖  Asistente IA":
    modulo_asistente_ia()