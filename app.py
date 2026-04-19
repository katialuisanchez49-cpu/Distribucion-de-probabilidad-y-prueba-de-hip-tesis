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
/* ── Fuentes ── */
* { font-family: serif !important; }
h1, h2 { font-family: Georgia, serif !important; }

/* ── Fondo general ── */
.main { background-color: #fafaf8 !important; }
.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
    background-color: #fafaf8 !important;
}

/* ── Ocultar sidebar ── */
section[data-testid="stSidebar"] { display: none; }

/* ── Tabs ── */
div[data-baseweb="tab-list"] {
    background-color: #fdf6e3 !important;
    border-bottom: 2px solid #c9a84c !important;
    padding: 6px 12px !important;
    gap: 4px !important;
}
div[data-baseweb="tab-list"] button {
    background-color: #fafaf8 !important;
    color: #1a2744 !important;
    border: 1.5px solid #c9a84c !important;
    border-radius: 8px 8px 0 0 !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    padding: 8px 18px !important;
    transition: 0.2s !important;
}
div[data-baseweb="tab-list"] button[aria-selected="true"] {
    background-color: #c9a84c !important;
    color: #1a2744 !important;
    font-weight: 700 !important;
}
div[data-baseweb="tab-list"] button:hover {
    background-color: #fdf0d0 !important;
    color: #1a2744 !important;
}
div[data-baseweb="tab-panel"] {
    background-color: #fafaf8 !important;
    border: 1px solid #e8d5a3 !important;
    border-top: none !important;
    padding: 1.5rem !important;
}

/* ── Botones principales ── */
div.stButton > button {
    background-color: #c9a84c !important;
    color: #1a2744 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 8px 20px !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    transition: 0.3s !important;
    width: 100% !important;
}
div.stButton > button:hover {
    background-color: #a8872e !important;
    color: #ffffff !important;
}

/* ── File uploader ── */
div[data-testid="stFileUploader"] {
    background-color: #fdf6e3 !important;
    border: 2px dashed #c9a84c !important;
    border-radius: 10px !important;
    padding: 12px !important;
}
div[data-testid="stFileUploader"] * {
    color: #1a2744 !important;
    background-color: transparent !important;
}
div[data-testid="stFileUploadDropzone"] {
    background-color: #fdf6e3 !important;
}
button[data-testid="baseButton-secondary"] {
    background-color: #fafaf8 !important;
    color: #1a2744 !important;
    border: 1.5px solid #c9a84c !important;
    border-radius: 6px !important;
    width: auto !important;
}

/* ── Inputs y selects ── */
div[data-baseweb="input"] input,
div[data-baseweb="select"] {
    border-radius: 8px !important;
    border: 1.5px solid #c9a84c !important;
    background-color: #fafaf8 !important;
    color: #1a2744 !important;
}

/* ── Métricas ── */
div[data-testid="metric-container"] {
    background-color: #fdf6e3 !important;
    border: 1.5px solid #c9a84c !important;
    border-radius: 10px !important;
    padding: 12px 16px !important;
    text-align: center !important;
}
div[data-testid="metric-container"] label {
    color: #a8872e !important;
    font-weight: 600 !important;
}
div[data-testid="metric-container"] div {
    color: #1a2744 !important;
}

/* ── Encabezados ── */
h1 {
    color: #a8872e !important;
    font-size: 1.8rem !important;
    font-family: Georgia, serif !important;
    border-bottom: 2px solid #c9a84c !important;
    padding-bottom: 8px !important;
    background: none !important;
}
h2 {
    color: #a8872e !important;
    font-family: Georgia, serif !important;
    border-bottom: 1.5px solid #e8d5a3 !important;
    padding-bottom: 6px !important;
    background: none !important;
}
h3 {
    color: #1a2744 !important;
    font-family: sans-serif !important;
    font-weight: 600 !important;
    border-bottom: 1px solid #e8d5a3 !important;
    padding-bottom: 4px !important;
    background: none !important;
}

/* ── Alertas sin azul ── */
div[data-testid="stInfo"],
div[data-baseweb="notification"] {
    background-color: #fdf6e3 !important;
    color: #1a2744 !important;
    border-left: 4px solid #c9a84c !important;
}
div[data-testid="stSuccess"] {
    background-color: #f6fff6 !important;
    color: #1a2744 !important;
}
div[data-testid="stWarning"] {
    background-color: #fffbf0 !important;
    color: #1a2744 !important;
}
div[data-testid="stError"] {
    background-color: #fff5f5 !important;
    color: #1a2744 !important;
}
/* ── Number input botones ── */
div[data-baseweb="input"] {
    background-color: #fafaf8 !important;
    border: 1.5px solid #c9a84c !important;
    border-radius: 8px !important;
}
button[data-testid="stNumberInputStepDown"],
button[data-testid="stNumberInputStepUp"] {
    background-color: #c9a84c !important;
    color: #1a2744 !important;
    border: none !important;
}
button[data-testid="stNumberInputStepDown"]:hover,
button[data-testid="stNumberInputStepUp"]:hover {
    background-color: #a8872e !important;
}
/* ── Fix botón upload ── */
div[data-testid="stFileUploader"] button span {
    display: none !important;
}
div[data-testid="stFileUploader"] button::after {
    content: "Subir archivo" !important;
    color: #1a2744 !important;
    font-family: sans-serif !important;
    font-size: 14px !important;
}
div[data-testid="stFileUploader"] button {
    background-color: #fafaf8 !important;
    border: 1.5px solid #c9a84c !important;
    border-radius: 6px !important;
    padding: 6px 16px !important;
    width: auto !important;
}
/* ── Radio buttons ── */
div[data-baseweb="radio"] input {
    accent-color: #c9a84c !important;
}

/* ── Selectbox ── */
div[data-baseweb="select"] * {
    background-color: #fafaf8 !important;
    color: #1a2744 !important;
}

/* ── Spinner ── */
div[data-testid="stSpinner"] {
    color: #c9a84c !important;
}

/* ── Dataframe ── */
div[data-testid="stDataFrame"] {
    border: 1px solid #e8d5a3 !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Header superior ──
st.markdown("""
<div style='padding:16px 24px; display:flex; align-items:center;
     gap:12px; border-bottom: 3px solid #c9a84c;
     background-color:#fafaf8; width:100%; box-sizing:border-box;
     margin-top: 0;'>
    <span style='font-size:30px;'>📊</span>
    <div style='flex:1;'>
        <p style='color:#a8872e; font-family:Georgia,serif;
           font-size:35px; font-weight:700; margin:0; line-height:1.4;'>
            Aplicación de Probabilidad y Estadística
        </p>
        <p style='color:#c9a84c; font-family:sans-serif;
           font-size:12px; margin:0;'>
            Python · Streamlit · Gemini
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
# ── Navegación como tabs ──
tab1, tab2, tab3, tab4 = st.tabs([
    "📂  Carga de Datos",
    "📊  Visualización",
    "🧪  Prueba Z",
    "🤖  Asistente IA"
])

with tab1:
    modulo_carga_datos()
with tab2:
    modulo_visualizacion()
with tab3:
    modulo_prueba_z()
with tab4:
    modulo_asistente_ia()