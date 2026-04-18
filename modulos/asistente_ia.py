import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

PALETA = {
    "principal":  "#E74C3C",
    "medio_alto": "#F1948A",
    "medio":      "#F5B7B1",
    "suave":      "#FADBD8",
    "fondo":      "#FDEDEC"
}

def modulo_asistente_ia():
    st.header("🤖 Asistente de IA — Gemini")
    st.write("El asistente analiza los resultados estadísticos y te ayuda "
             "a interpretar las decisiones.")

    if "df" not in st.session_state or "variable" not in st.session_state:
        st.warning("⚠️ Primero carga los datos en el módulo de Carga de Datos.")
        return

    df = st.session_state["df"]
    variable = st.session_state["variable"]
    datos = df[variable].dropna()

    # --- Resumen estadístico ---
    resumen = {
        "variable": variable,
        "n": len(datos),
        "media": round(datos.mean(), 4),
        "mediana": round(datos.median(), 4),
        "desv_std": round(datos.std(), 4),
        "sesgo": round(datos.skew(), 4),
        "curtosis": round(datos.kurtosis(), 4),
        "minimo": round(datos.min(), 4),
        "maximo": round(datos.max(), 4)
    }

    # --- Pestaña 1: Análisis de distribución ---
    st.subheader("📊 Análisis de Distribución")
    st.markdown("Presiona el botón para que Gemini analice "
                "la distribución de tus datos.")

    if st.button("🔍 Analizar distribución con IA"):
        prompt_distribucion = f"""
        Eres un asistente experto en estadística. Analiza este resumen estadístico 
        y responde en español de forma clara y educativa para un estudiante universitario.

        Resumen estadístico de la variable '{variable}':
        - Número de datos: {resumen['n']}
        - Media: {resumen['media']}
        - Mediana: {resumen['mediana']}
        - Desviación estándar: {resumen['desv_std']}
        - Sesgo: {resumen['sesgo']}
        - Curtosis: {resumen['curtosis']}
        - Mínimo: {resumen['minimo']}
        - Máximo: {resumen['maximo']}

        Responde estas preguntas:
        1. ¿La distribución parece normal? ¿Por qué?
        2. ¿Hay sesgo? ¿En qué dirección?
        3. ¿Qué indica la curtosis?
        4. ¿Qué podemos inferir de estos datos en general?

        Sé conciso pero completo. Usa viñetas para organizar tu respuesta.
        """

        with st.spinner("Gemini está analizando los datos..."):
            try:
                modelo = genai.GenerativeModel("gemini-1.5-flash")
                respuesta = modelo.generate_content(prompt_distribucion)
                st.markdown("#### 💬 Respuesta de Gemini:")
                st.markdown(respuesta.text)
            except Exception as e:
                st.error(f"Error al conectar con Gemini: {e}")

    st.markdown("---")

    # --- Pestaña 2: Análisis de prueba Z ---
    st.subheader("🧪 Interpretación de Prueba Z")

    if "resultado_z" not in st.session_state:
        st.info("💡 Primero ejecuta la Prueba Z en el módulo correspondiente.")
    else:
        r = st.session_state["resultado_z"]

        st.markdown("**Resumen de la prueba realizada:**")
        col1, col2, col3 = st.columns(3)
        col1.metric("Z calculado", r["z_calculado"])
        col2.metric("p-value", r["p_value"])
        col3.metric("Decisión", 
                    "Rechazar H0" if r["rechazar"] else "No rechazar H0")

        st.markdown("**¿Cuál fue tu decisión como estudiante?**")
        decision_estudiante = st.radio(
            "Selecciona tu decisión:",
            ["Rechazar H0", "No rechazar H0"],
            horizontal=True
        )

        if st.button("🤖 Interpretar prueba Z con IA"):
            decision_auto = "Rechazar H0" if r["rechazar"] else "No rechazar H0"
            coincide = decision_estudiante == decision_auto

            prompt_z = f"""
            Eres un asistente experto en estadística inferencial. 
            Responde en español de forma clara para un estudiante universitario.

            Se realizó una prueba Z con los siguientes parámetros:
            - Media muestral (x̄): {r['media_muestral']}
            - Media hipotética (μ0): {r['mu0']}
            - Desviación estándar poblacional (σ): {r['sigma']}
            - Tamaño de muestra (n): {r['n']}
            - Nivel de significancia (α): {r['alpha']}
            - Tipo de prueba: {r['tipo_prueba']}
            - Estadístico Z calculado: {r['z_calculado']}
            - Valor crítico Z: {r['z_critico']}
            - p-value: {r['p_value']}
            - Decisión automática: {decision_auto}

            Responde:
            1. ¿Se rechaza H0? Explica la decisión detalladamente.
            2. ¿Los supuestos de la prueba Z son razonables con n={r['n']}?
            3. ¿Qué significa este resultado en términos prácticos?
            4. ¿Qué recomendarías como siguiente paso estadístico?

            Sé conciso pero completo. Usa viñetas para organizar tu respuesta.
            """

            with st.spinner("Gemini está interpretando la prueba Z..."):
                try:
                    modelo = genai.GenerativeModel("gemini-1.5-flash")
                    respuesta = modelo.generate_content(prompt_z)

                    st.markdown("#### 💬 Respuesta de Gemini:")
                    st.markdown(respuesta.text)

                    st.markdown("---")
                    st.markdown("#### 🔁 Comparación de decisiones")
                    if coincide:
                        st.success(f"✅ Tu decisión **'{decision_estudiante}'** "
                                   f"coincide con la decisión automática.")
                    else:
                        st.error(f"❌ Tu decisión **'{decision_estudiante}'** "
                                 f"NO coincide con la decisión automática "
                                 f"**'{decision_auto}'**. Revisa el análisis.")
                except Exception as e:
                    st.error(f"Error al conectar con Gemini: {e}")
