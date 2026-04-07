import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
PALETA = {
    "principal":   "#E74C3C",
    "medio_alto":  "#F1948A",
    "medio":       "#F5B7B1",
    "suave":       "#FADBD8",
    "fondo":       "#FDEDEC"
}

def modulo_visualizacion():
    st.header("📊 Visualización de Distribuciones")

    if "df" not in st.session_state or "variable" not in st.session_state:
        st.warning("⚠️ Primero debes cargar los datos en el módulo anterior.")
        return

    df = st.session_state["df"]
    variable = st.session_state["variable"]
    datos = df[variable].dropna()

    st.subheader(f"Variable analizada: `{variable}`")

    # CSS personalizado para las pestañas en visualización
    st.markdown("""
    <style>
        .viz-tabs [data-baseweb="tab-list"] button {
            background-color: #e8f4f8;
            color: #006d77;
            font-weight: bold;
            border-radius: 8px 8px 0 0;
        }
        .viz-tabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            background-color: #006d77;
            color: white;
        }
        .viz-tabs [data-baseweb="tab-list"] button:hover {
            background-color: #83c5be;
            color: white;
        }
        .viz-tabs [data-baseweb="tab"] {
            background-color: #f7f9fb;
            border-radius: 0 0 8px 8px;
            padding: 15px;
            margin-bottom: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Crear pestañas para las secciones
    tab_estadisticas, tab_graficas, tab_analisis = st.tabs(["Estadísticas Descriptivas", "Gráficas", "Análisis Automático"])

    with tab_estadisticas:
        # --- Estadísticas básicas ---
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Media", f"{datos.mean():.4f}")
        col2.metric("Mediana", f"{datos.median():.4f}")
        col3.metric("Desv. Estándar", f"{datos.std():.4f}")
        col4.metric("N", f"{len(datos)}")

        col5, col6, col7, col8 = st.columns(4)
        col5.metric("Mínimo", f"{datos.min():.4f}")
        col6.metric("Máximo", f"{datos.max():.4f}")
        col7.metric("Sesgo", f"{datos.skew():.4f}")
        col8.metric("Curtosis", f"{datos.kurtosis():.4f}")

    with tab_graficas:
        # --- Gráficas ---
        tipo_grafica = st.multiselect(
            "Selecciona las gráficas a mostrar",
            ["Histograma + KDE", "Boxplot", "QQ-Plot"],
            default=["Histograma + KDE", "Boxplot"]
        )

        if "Histograma + KDE" in tipo_grafica:
            st.markdown("#### Histograma con KDE")
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.histplot(datos, kde=True, ax=ax, color="#F1948a", 
                         edgecolor="white")
            ax.set_title(f"Histograma + KDE de {variable}")
            ax.set_xlabel(variable)
            ax.set_ylabel("Frecuencia")
            ax.lines[0].set_color("#E74C3C")
            st.pyplot(fig)
            plt.close()

        if "Boxplot" in tipo_grafica:
            st.markdown("#### Boxplot")
            fig, ax = plt.subplots(figsize=(8, 3))
            sns.boxplot(x=datos, ax=ax, color="#fadbd8")
            ax.set_title(f"Boxplot de {variable}")
            ax.set_xlabel(variable)
            st.pyplot(fig)
            plt.close()

        if "QQ-Plot" in tipo_grafica:
            st.markdown("#### QQ-Plot (Normalidad)")
            fig, ax = plt.subplots(figsize=(6, 4))
            stats.probplot(datos, dist="norm", plot=ax)
            ax.set_title(f"QQ-Plot de {variable}")
            st.pyplot(fig)
            plt.close()

    with tab_analisis:
        # --- Análisis automático ---
        sesgo = datos.skew()
        curtosis = datos.kurtosis()

        # ¿Normal?
        _, p_normalidad = stats.shapiro(datos[:5000])
        if p_normalidad > 0.05:
            st.success("La distribución **parece normal** (Shapiro-Wilk p > 0.05)")
        else:
            st.error("La distribución **NO parece normal** (Shapiro-Wilk p ≤ 0.05)")

        # ¿Sesgo?
        if abs(sesgo) < 0.5:
            st.info(f"📐 Sesgo = {sesgo:.4f} → Distribución **simétrica**")
        elif sesgo > 0:
            st.warning(f"📐 Sesgo = {sesgo:.4f} → Sesgo **positivo** (cola a la derecha)")
        else:
            st.warning(f"📐 Sesgo = {sesgo:.4f} → Sesgo **negativo** (cola a la izquierda)")

        # ¿Outliers?
        Q1 = datos.quantile(0.25)
        Q3 = datos.quantile(0.75)
        IQR = Q3 - Q1
        outliers = datos[(datos < Q1 - 1.5 * IQR) | (datos > Q3 + 1.5 * IQR)]