import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

PALETA = {
    "principal":  "#c9a84c",
    "medio_alto": "#a8872e",
    "medio":      "#1a2744",
    "suave":      "#243156",
    "fondo":      "#fafaf8"
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

    st.markdown("""
    <style>
        .viz-tabs [data-baseweb="tab-list"] button {
            background-color: #EAFAF1;
            color: #1E8449;
            font-weight: bold;
            border-radius: 8px 8px 0 0;
        }
        .viz-tabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            background-color: #27AE60;
            color: white;
        }
        .viz-tabs [data-baseweb="tab-list"] button:hover {
            background-color: #A9DFBF;
            color: white;
        }
        .viz-tabs [data-baseweb="tab"] {
            background-color: #F9FFFC;
            border-radius: 0 0 8px 8px;
            padding: 15px;
            margin-bottom: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

    tab_estadisticas, tab_graficas, tab_analisis = st.tabs([
        "Estadísticas Descriptivas", "Gráficas", "Análisis Automático"
    ])

    with tab_estadisticas:
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
        tipo_grafica = st.multiselect(
            "Selecciona las gráficas a mostrar",
            ["Histograma + KDE", "Boxplot", "QQ-Plot"],
            default=["Histograma + KDE", "Boxplot"]
        )

        if "Histograma + KDE" in tipo_grafica:
            st.markdown("#### Histograma con KDE")
            fig, ax = plt.subplots(figsize=(6, 3))
            sns.histplot(datos, kde=True, ax=ax,
                        color="#c9a84c", edgecolor="white")
            ax.lines[0].set_color("#1a2744")
            ax.lines[0].set_linewidth(2.5)
            ax.set_title(f"Histograma + KDE de {variable}",
                         fontsize=13, fontweight="bold")
            ax.set_xlabel(variable, fontsize=11)
            ax.set_ylabel("Frecuencia", fontsize=11)
            ax.set_facecolor("#FFFFFF")
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.grid(axis="y", linestyle="--", alpha=0.3)
            fig.patch.set_facecolor("#FFFFFF")
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

        if "Boxplot" in tipo_grafica:
            st.markdown("#### Boxplot")
            fig, ax = plt.subplots(figsize=(6, 3))
            sns.boxplot(x=datos, ax=ax,
                        color="#fafaf8",
                        boxprops=dict(edgecolor="#1a2744"),
                        whiskerprops=dict(color="#1a2744"),
                        capprops=dict(color="#1a2744"),
                        medianprops=dict(color="#c9a84c", linewidth=2.5))
            ax.set_title(f"Boxplot de {variable}",
                         fontsize=13, fontweight="bold")
            ax.set_xlabel(variable, fontsize=11)
            ax.set_facecolor("#FFFFFF")
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            fig.patch.set_facecolor("#FFFFFF")
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

        if "QQ-Plot" in tipo_grafica:
            st.markdown("#### QQ-Plot (Normalidad)")
            fig, ax = plt.subplots(figsize=(5, 3))
            stats.probplot(datos, dist="norm", plot=ax)
            ax.get_lines()[0].set(color="#c9a84c", markersize=4, alpha=0.7)
            ax.get_lines()[1].set(color="#1a2744", linewidth=2)
            ax.set_title(f"QQ-Plot de {variable}",
                         fontsize=13, fontweight="bold")
            ax.set_facecolor("#FFFFFF")
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.grid(axis="both", linestyle="--", alpha=0.3)
            fig.patch.set_facecolor("#FFFFFF")
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

        # --- Distribución Normal con valores Z ---
        st.markdown("---")
        st.subheader("📉 Distribución Normal Estándar")
        st.write("Esta gráfica muestra cómo se distribuyen los datos "
                 "estandarizados (valores Z).")

        fig, ax = plt.subplots(figsize=(8, 3.5))
        z_datos = (datos - datos.mean()) / datos.std()
        x = np.linspace(-4, 4, 1000)
        y = stats.norm.pdf(x)

        ax.plot(x, y, color="#2C2C2C", linewidth=2.5,
                label="Distribución normal teórica", zorder=3)
        ax.fill_between(x, y, color=PALETA["fondo"], alpha=0.6, zorder=1)

        ax.hist(z_datos, bins=30, density=True,
                color=PALETA["medio_alto"], alpha=0.5,
                edgecolor="white", label="Datos estandarizados", zorder=2)

        ax.axvline(0, color=PALETA["principal"], linewidth=2,
                   linestyle="--", label="Media (Z = 0)")

        for val, etiqueta in [
            (-3, "-3σ"), (-2, "-2σ"), (-1, "-1σ"),
            (1, "+1σ"), (2, "+2σ"), (3, "+3σ")
        ]:
            ax.axvline(val, color=PALETA["medio"], linewidth=1,
                       linestyle=":", alpha=0.8)
            ax.text(val, max(y)*1.05, etiqueta, ha="center",
                    fontsize=9, color=PALETA["principal"])

        ax.text(0, max(y)*0.6, f"x̄ = {datos.mean():.2f}",
                ha="center", fontsize=10, color=PALETA["principal"],
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.3",
                          facecolor=PALETA["suave"], alpha=0.9))

        ax.set_title("Distribución Normal Estándar con valores Z",
                     fontsize=13, fontweight="bold", pad=12)
        ax.set_xlabel("Valores Z (desviaciones estándar)", fontsize=11)
        ax.set_ylabel("Densidad", fontsize=11)
        ax.set_xlim(-4.2, 4.2)
        ax.set_ylim(0, max(y) * 1.2)
        ax.legend(loc="upper right", fontsize=10,
                  framealpha=0.9, edgecolor=PALETA["medio"])
        ax.set_facecolor("#FFFFFF")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        fig.patch.set_facecolor("#FFFFFF")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with tab_analisis:
        sesgo = datos.skew()
        curtosis = datos.kurtosis()

        _, p_normalidad = stats.shapiro(datos[:5000])
        if p_normalidad > 0.05:
            st.success("✅ La distribución **parece normal** "
                       "(Shapiro-Wilk p > 0.05)")
        else:
            st.error("❌ La distribución **NO parece normal** "
                     "(Shapiro-Wilk p ≤ 0.05)")

        if abs(sesgo) < 0.5:
            st.info(f"📐 Sesgo = {sesgo:.4f} → Distribución **simétrica**")
        elif sesgo > 0:
            st.warning(f"📐 Sesgo = {sesgo:.4f} → Sesgo **positivo** "
                       f"(cola a la derecha)")
        else:
            st.warning(f"📐 Sesgo = {sesgo:.4f} → Sesgo **negativo** "
                       f"(cola a la izquierda)")

        Q1 = datos.quantile(0.25)
        Q3 = datos.quantile(0.75)
        IQR = Q3 - Q1
        outliers = datos[(datos < Q1 - 1.5 * IQR) | (datos > Q3 + 1.5 * IQR)]
        if len(outliers) > 0:
            st.warning(f"⚠️ Se detectaron **{len(outliers)} outliers** "
                       f"en los datos.")
        else:
            st.success("✅ No se detectaron outliers significativos.")