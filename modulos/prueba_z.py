import streamlit as st
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

PALETA = {
    "principal":  "#c9a84c",
    "medio_alto": "#a8872e",
    "medio":      "#1a2744",
    "suave":      "#243156",
    "fondo":      "#fafaf8"
}

def generar_grafico_z(z_calc, z_crit, tipo_prueba, alpha):
    x = np.linspace(-4, 4, 1000)
    y = stats.norm.pdf(x, 0, 1)

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(x, y, color=PALETA["medio"], lw=2.5,
            label='Distribución Normal ($H_0$)')

    color_r = PALETA["principal"]
    lbl_r = f'Región de Rechazo (α={alpha})'

    if "Bilateral" in tipo_prueba:
        ax.fill_between(x, 0, y, where=(x >= abs(z_crit)),
                        color=color_r, alpha=0.4, label=lbl_r)
        ax.fill_between(x, 0, y, where=(x <= -abs(z_crit)),
                        color=color_r, alpha=0.4)
        ax.axvline(abs(z_crit), color=color_r, lw=1.5, linestyle=":")
        ax.axvline(-abs(z_crit), color=color_r, lw=1.5, linestyle=":")
        ax.text(abs(z_crit), max(y)*0.15, f"±{abs(z_crit):.2f}",
                ha="center", fontsize=9, color=color_r)
    elif "izquierda" in tipo_prueba:
        ax.fill_between(x, 0, y, where=(x <= z_crit),
                        color=color_r, alpha=0.4, label=lbl_r)
        ax.axvline(z_crit, color=color_r, lw=1.5, linestyle=":")
        ax.text(z_crit, max(y)*0.15, f"{z_crit:.2f}",
                ha="center", fontsize=9, color=color_r)
    else:
        ax.fill_between(x, 0, y, where=(x >= z_crit),
                        color=color_r, alpha=0.4, label=lbl_r)
        ax.axvline(z_crit, color=color_r, lw=1.5, linestyle=":")
        ax.text(z_crit, max(y)*0.15, f"{z_crit:.2f}",
                ha="center", fontsize=9, color=color_r)

    # Z calculado — si está dentro del rango visible
    if -4 <= z_calc <= 4:
        ax.axvline(z_calc, color=PALETA["medio_alto"], ls='--',
                   lw=2, label=f'Z calculado ({z_calc:.2f})')
        ax.scatter(z_calc, stats.norm.pdf(z_calc, 0, 1),
                   color=PALETA["medio_alto"], s=100, zorder=5)
        ax.text(z_calc, max(y)*1.04, f"Z={z_calc:.2f}",
                ha="center", fontsize=9, color=PALETA["medio_alto"],
                fontweight="bold")
    else:
        # Z fuera del rango — mostrar flecha en el borde
        lado = 3.7 if z_calc > 0 else -3.7
        direccion = "→" if z_calc > 0 else "←"
        ax.annotate(
            f"Z={z_calc:.2f} {direccion}",
            xy=(lado, max(y)*0.08),
            fontsize=9,
            color=PALETA["medio_alto"],
            fontweight="bold",
            ha="right" if z_calc > 0 else "left",
            bbox=dict(boxstyle="round,pad=0.3",
                      facecolor=PALETA["fondo"],
                      edgecolor=PALETA["medio_alto"],
                      alpha=0.9)
        )
        # Flecha en el borde
        ax.annotate(
            "",
            xy=(3.95 if z_calc > 0 else -3.95, max(y)*0.05),
            xytext=(3.5 if z_calc > 0 else -3.5, max(y)*0.05),
            arrowprops=dict(arrowstyle="->",
                            color=PALETA["medio_alto"], lw=2)
        )
        # Agregar a leyenda manualmente
        from matplotlib.lines import Line2D
        linea = Line2D([0], [0], color=PALETA["medio_alto"],
                       ls='--', lw=2,
                       label=f'Z calculado ({z_calc:.2f}) — fuera de rango')
        ax.legend(handles=ax.get_legend_handles_labels()[0] + [linea],
                  frameon=False, loc='upper right', fontsize=9)

    ax.set_xlim(-4.3, 4.3)
    ax.set_ylim(0, max(y) * 1.2)
    ax.set_title("Visualización de la Prueba Z",
                 color=PALETA["medio"], fontsize=14)
    ax.set_xlabel("Valores Z", fontsize=11)
    ax.set_ylabel("Densidad", fontsize=11)
    ax.legend(frameon=False, loc='upper right', fontsize=9)
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.patch.set_facecolor(PALETA["fondo"])
    ax.set_facecolor(PALETA["fondo"])

    return fig

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
        error_estandar = sigma / np.sqrt(n)
        z_calculado = (media_muestral - mu0) / error_estandar

        if "Bilateral" in tipo_prueba:
            z_critico = stats.norm.ppf(1 - alpha / 2)
            p_value = 2 * (1 - stats.norm.cdf(abs(z_calculado)))
        elif "izquierda" in tipo_prueba:
            z_critico = stats.norm.ppf(alpha)
            p_value = stats.norm.cdf(z_calculado)
        else:
            z_critico = stats.norm.ppf(1 - alpha)
            p_value = 1 - stats.norm.cdf(z_calculado)

        if "Bilateral" in tipo_prueba:
            rechazar = abs(z_calculado) > z_critico
        elif "izquierda" in tipo_prueba:
            rechazar = z_calculado < z_critico
        else:
            rechazar = z_calculado > z_critico

        st.session_state["resultado_z"] = {
            "media_muestral": round(media_muestral, 4),
            "mu0": mu0,
            "sigma": sigma,
            "n": n,
            "alpha": alpha,
            "tipo_prueba": tipo_prueba,
            "z_calculado": round(z_calculado, 4),
            "z_critico": round(z_critico, 4),
            "p_value": round(p_value, 4),
            "rechazar": rechazar
        }

        st.markdown("---")
        st.subheader("Visualización Estadística")
        figura = generar_grafico_z(z_calculado, z_critico, tipo_prueba, alpha)
        st.pyplot(figura)

        st.markdown("---")
        st.subheader("Resultados")
        col5, col6, col7, col8 = st.columns(4)
        col5.metric("Media muestral (x̄)", f"{media_muestral:.4f}")
        col6.metric("Z calculado", f"{z_calculado:.4f}")
        col7.metric("p-value", f"{p_value:.4f}")
        col8.metric("Decisión",
                    "Rechazar H0" if rechazar else "No rechazar H0")

        st.success("✅ ¡Cálculo completado! Ahora puedes ir al Asistente de IA.")