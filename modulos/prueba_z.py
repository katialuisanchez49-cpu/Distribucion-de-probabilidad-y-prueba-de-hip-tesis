import streamlit as st
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

PALETA = {
    "principal":  "#E74C3C",
    "medio_alto": "#F1948A",
    "medio":      "#F5B7B1",
    "suave":      "#FADBD8",
    "fondo":      "#FDEDEC"
}

def modulo_prueba_z():
    st.header("Prueba de Hipótesis Z")

    if "df" not in st.session_state or "variable" not in st.session_state:
        st.warning("⚠️ Primero debes cargar los datos en el módulo de Carga de Datos.")
        return

    df = st.session_state["df"]
    variable = st.session_state["variable"]
    datos = df[variable].dropna()
    n = len(datos)
    media_muestral = datos.mean()

    st.subheader("Parámetros de la prueba")

    col1, col2 = st.columns(2)
    with col1:
        mu0 = st.number_input("Media hipotética (H0: μ =)", value=0.0)
        sigma = st.number_input(
            "Desviación estándar poblacional (σ)",
            min_value=0.01, value=float(round(datos.std(), 4))
        )
    with col2:
        alpha = st.selectbox("Nivel de significancia (α)", 
                             [0.01, 0.05, 0.10], index=1)
        tipo_prueba = st.selectbox("Tipo de prueba", [
            "Bilateral (H1: μ ≠ μ0)",
            "Cola izquierda (H1: μ < μ0)",
            "Cola derecha (H1: μ > μ0)"
        ])

    st.markdown("---")
    st.subheader("Hipótesis")
    col3, col4 = st.columns(2)
    with col3:
        st.info(f"**H0:** μ = {mu0}")
    with col4:
        if "Bilateral" in tipo_prueba:
            st.warning(f"**H1:** μ ≠ {mu0}")
        elif "izquierda" in tipo_prueba:
            st.warning(f"**H1:** μ < {mu0}")
        else:
            st.warning(f"**H1:** μ > {mu0}")

    if st.button("Calcular Prueba Z"):

        # --- Cálculo del estadístico Z ---
        error_estandar = sigma / np.sqrt(n)
        z_calculado = (media_muestral - mu0) / error_estandar

        # --- Valor crítico y p-value ---
        if "Bilateral" in tipo_prueba:
            z_critico = stats.norm.ppf(1 - alpha / 2)
            p_value = 2 * (1 - stats.norm.cdf(abs(z_calculado)))
        elif "izquierda" in tipo_prueba:
            z_critico = stats.norm.ppf(alpha)
            p_value = stats.norm.cdf(z_calculado)
        else:
            z_critico = stats.norm.ppf(1 - alpha)
            p_value = 1 - stats.norm.cdf(z_calculado)

        # --- Decisión ---
        if "Bilateral" in tipo_prueba:
            rechazar = abs(z_calculado) > z_critico
        elif "izquierda" in tipo_prueba:
            rechazar = z_calculado < z_critico
        else:
            rechazar = z_calculado > z_critico

        # --- Resultados numéricos ---
        st.markdown("---")
        st.subheader("Resultados")
        col5, col6, col7, col8 = st.columns(4)
        col5.metric("Media muestral (x̄)", f"{media_muestral:.4f}")
        col6.metric("Z calculado", f"{z_calculado:.4f}")