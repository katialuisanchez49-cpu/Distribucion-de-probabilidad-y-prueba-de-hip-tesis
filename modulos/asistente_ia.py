import streamlit as st
import numpy as np
from scipy import stats as scipy_stats
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Inicializar cliente de Gemini
cliente = None
try:
    from google import genai
    if GEMINI_API_KEY:
        cliente = genai.Client(api_key=GEMINI_API_KEY)
except Exception:
    cliente = None

PALETA = {
    "principal":  "#c9a84c",
    "medio_alto": "#a8872e",
    "medio":      "#1a2744",
    "suave":      "#243156",
    "fondo":      "#fafaf8"
}

def generar_con_gemini(prompt):
    respuesta = cliente.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt
    )
    return respuesta.text

def analizar_distribucion(resumen):
    variable = resumen['variable']
    n = resumen['n']
    media = resumen['media']
    mediana = resumen['mediana']
    desv = resumen['desv_std']
    sesgo = resumen['sesgo']
    curtosis = resumen['curtosis']
    minimo = resumen['minimo']
    maximo = resumen['maximo']

    respuesta = f"### 📊 Análisis de la variable `{variable}`\n\n"

    respuesta += "**1. ¿La distribución parece normal?**\n"
    if abs(sesgo) < 0.5 and abs(curtosis) < 1:
        respuesta += (f"- La distribución **parece aproximadamente normal**. "
                      f"El sesgo ({sesgo}) es cercano a 0 y la curtosis "
                      f"({curtosis}) es baja, lo que indica una forma "
                      f"simétrica y sin colas extremas.\n\n")
    else:
        respuesta += (f"- La distribución **no parece completamente normal**. "
                      f"El sesgo ({sesgo}) y/o la curtosis ({curtosis}) "
                      f"indican desviaciones de la normalidad.\n\n")

    respuesta += "**2. ¿Hay sesgo? ¿En qué dirección?**\n"
    if abs(sesgo) < 0.5:
        respuesta += "- La distribución es **simétrica**, sin sesgo significativo.\n\n"
    elif sesgo > 0.5:
        respuesta += (f"- Hay un **sesgo positivo** (cola a la derecha) de {sesgo}. "
                      f"Esto indica que hay valores atípicamente altos que "
                      f"jalan la media hacia arriba. La media ({media}) "
                      f"es mayor que la mediana ({mediana}).\n\n")
    else:
        respuesta += (f"- Hay un **sesgo negativo** (cola a la izquierda) de {sesgo}. "
                      f"Esto indica que hay valores atípicamente bajos. "
                      f"La media ({media}) es menor que la mediana ({mediana}).\n\n")

    respuesta += "**3. ¿Qué indica la curtosis?**\n"
    if curtosis > 1:
        respuesta += (f"- La curtosis es **alta ({curtosis})** (leptocúrtica). "
                      f"Los datos tienen colas más pesadas que una distribución "
                      f"normal, con más valores extremos de lo esperado.\n\n")
    elif curtosis < -1:
        respuesta += (f"- La curtosis es **baja ({curtosis})** (platicúrtica). "
                      f"Los datos tienen colas más ligeras, con menos valores "
                      f"extremos que una distribución normal.\n\n")
    else:
        respuesta += (f"- La curtosis ({curtosis}) es **moderada**, "
                      f"similar a una distribución normal estándar.\n\n")

    respuesta += "**4. ¿Qué podemos inferir de los datos?**\n"
    cv = (desv / media * 100) if media != 0 else 0
    respuesta += f"- El coeficiente de variación es **{cv:.2f}%**. "
    if cv < 15:
        respuesta += "Los datos son **poco dispersos** y homogéneos.\n"
    elif cv < 30:
        respuesta += "Los datos tienen una **dispersión moderada**.\n"
    else:
        respuesta += "Los datos son **muy dispersos** y heterogéneos.\n"

    respuesta += (f"- El rango de los datos va de **{minimo}** a **{maximo}**, "
                  f"con una amplitud de {round(maximo - minimo, 4)}.\n")
    respuesta += (f"- Con n={n} datos, "
                  f"{'la muestra es suficientemente grande para aplicar el TCL.' if n >= 30 else 'la muestra es pequeña, se recomienda precaución al hacer inferencias.'}\n")

    return respuesta

def analizar_prueba_z(r, decision_estudiante):
    decision_auto = "Rechazar H0" if r["rechazar"] else "No rechazar H0"
    coincide = decision_estudiante == decision_auto

    respuesta = "### 🧪 Interpretación de la Prueba Z\n\n"

    respuesta += "**1. ¿Se rechaza H0?**\n"
    if r["rechazar"]:
        respuesta += (f"- **Sí, se rechaza H0**. El estadístico Z calculado "
                      f"({r['z_calculado']}) cae en la región de rechazo. "
                      f"El p-value ({r['p_value']}) es menor que α ({r['alpha']}), "
                      f"lo que indica evidencia estadística suficiente para "
                      f"rechazar la hipótesis nula.\n\n")
    else:
        respuesta += (f"- **No se rechaza H0**. El estadístico Z calculado "
                      f"({r['z_calculado']}) NO cae en la región de rechazo. "
                      f"El p-value ({r['p_value']}) es mayor que α ({r['alpha']}), "
                      f"lo que indica que no hay evidencia suficiente para "
                      f"rechazar la hipótesis nula.\n\n")

    respuesta += "**2. ¿Los supuestos son razonables?**\n"
    if r["n"] >= 30:
        respuesta += (f"- Con n={r['n']} observaciones, el **Teorema Central del "
                      f"Límite** garantiza que la distribución muestral es "
                      f"aproximadamente normal. Los supuestos son **razonables**.\n\n")
    else:
        respuesta += (f"- Con n={r['n']} observaciones la muestra es pequeña. "
                      f"Se recomienda verificar normalidad antes de confiar "
                      f"en los resultados.\n\n")

    respuesta += "**3. ¿Qué significa este resultado en términos prácticos?**\n"
    diferencia = abs(r['media_muestral'] - r['mu0'])
    respuesta += (f"- La diferencia entre la media muestral ({r['media_muestral']}) "
                  f"y la media hipotética ({r['mu0']}) es de {round(diferencia, 4)} unidades. ")
    if r["rechazar"]:
        respuesta += ("Esta diferencia es **estadísticamente significativa**, "
                      "lo que sugiere que la población no tiene la media "
                      "propuesta en H0.\n\n")
    else:
        respuesta += ("Esta diferencia **no es estadísticamente significativa**, "
                      "lo que sugiere que la media poblacional podría ser "
                      "compatible con H0.\n\n")

    respuesta += "**4. ¿Qué se recomienda como siguiente paso?**\n"
    if r["rechazar"]:
        respuesta += ("- Se recomienda estimar un **intervalo de confianza** "
                      "para la media poblacional y analizar el tamaño del "
                      "efecto para determinar la relevancia práctica.\n")
    else:
        respuesta += ("- Se recomienda verificar si el tamaño de muestra es "
                      "adecuado mediante un **análisis de potencia estadística** "
                      "y considerar aumentar n si es posible.\n")

    return respuesta, coincide, decision_auto

def modulo_asistente_ia():
    st.header("🤖 Asistente de IA — Gemini")
    st.write("El asistente analiza los resultados estadísticos y genera "
             "una interpretación detallada.")

    # Indicador de estado de la API
    if cliente:
        st.success("✅ Conectado a Gemini API")
    else:
        st.warning("⚠️ Gemini no disponible — usando análisis automático")

    if "df" not in st.session_state or "variable" not in st.session_state:
        st.warning("⚠️ Primero carga los datos en el módulo de Carga de Datos.")
        return

    df = st.session_state["df"]
    variable = st.session_state["variable"]
    datos = df[variable].dropna()

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

    # --- Análisis de distribución ---
    st.subheader("📊 Análisis de Distribución")

    if st.button("🔍 Analizar distribución con IA"):
        with st.spinner("Analizando los datos..."):
            # Intenta con Gemini primero
            if cliente:
                try:
                    prompt = f"""
                    Eres un asistente experto en estadística. Analiza este resumen
                    estadístico y responde en español de forma clara y educativa
                    para un estudiante universitario.

                    Variable: '{variable}'
                    - N: {resumen['n']}
                    - Media: {resumen['media']}
                    - Mediana: {resumen['mediana']}
                    - Desv. estándar: {resumen['desv_std']}
                    - Sesgo: {resumen['sesgo']}
                    - Curtosis: {resumen['curtosis']}
                    - Mínimo: {resumen['minimo']}
                    - Máximo: {resumen['maximo']}

                    Responde:
                    1. ¿La distribución parece normal? ¿Por qué?
                    2. ¿Hay sesgo? ¿En qué dirección?
                    3. ¿Qué indica la curtosis?
                    4. ¿Qué podemos inferir de los datos?
                    Usa viñetas para organizar tu respuesta.
                    """
                    respuesta = generar_con_gemini(prompt)
                    st.info("💡 Respuesta generada por Gemini API")
                except Exception:
                    respuesta = analizar_distribucion(resumen)
                    st.info("💡 Respuesta generada por análisis automático")
            else:
                respuesta = analizar_distribucion(resumen)
                st.info("💡 Respuesta generada por análisis automático")

            st.markdown("#### 💬 Análisis:")
            st.markdown(respuesta)

    st.markdown("---")

    # --- Interpretación de Prueba Z ---
    st.subheader("🧪 Interpretación de Prueba Z")

    if "resultado_z" not in st.session_state:
        st.warning("⚠️ No se encontró resultado de Prueba Z en memoria.")
        st.info("💡 Ve al módulo **Prueba Z**, ejecuta el cálculo y regresa aquí.")
        return
    else:
        r = st.session_state["resultado_z"]

        col1, col2, col3 = st.columns(3)
        col1.metric("Z calculado", r["z_calculado"])
        col2.metric("p-value", r["p_value"])
        col3.metric("Decisión",
                    "Rechazar H0" if r["rechazar"] else "No rechazar H0")

        st.markdown("**¿Cuál fue tu decisión como estudiante?**")
        decision_estudiante = st.radio(
            "Selecciona tu decisión",
            ["Rechazar H0", "No rechazar H0"],
            horizontal=True
        )

        if st.button("🤖 Interpretar prueba Z con IA"):
            with st.spinner("Generando interpretación..."):
                if cliente:
                    try:
                        decision_auto = "Rechazar H0" if r["rechazar"] else "No rechazar H0"
                        prompt_z = f"""
                        Eres un asistente experto en estadística inferencial.
                        Responde en español para un estudiante universitario.

                        Prueba Z realizada:
                        - Media muestral: {r['media_muestral']}
                        - Media hipotética: {r['mu0']}
                        - Sigma: {r['sigma']}
                        - n: {r['n']}
                        - Alpha: {r['alpha']}
                        - Tipo: {r['tipo_prueba']}
                        - Z calculado: {r['z_calculado']}
                        - Z crítico: {r['z_critico']}
                        - p-value: {r['p_value']}
                        - Decisión: {decision_auto}

                        Responde con viñetas:
                        1. ¿Se rechaza H0? Explica.
                        2. ¿Los supuestos son razonables?
                        3. ¿Qué significa en términos prácticos?
                        4. ¿Qué recomiendas como siguiente paso?
                        """
                        respuesta = generar_con_gemini(prompt_z)
                        coincide = decision_estudiante == decision_auto
                        st.info("💡 Respuesta generada por Gemini API")
                    except Exception:
                        respuesta, coincide, decision_auto = analizar_prueba_z(
                            r, decision_estudiante)
                        st.info("💡 Respuesta generada por análisis automático")
                else:
                    respuesta, coincide, decision_auto = analizar_prueba_z(
                        r, decision_estudiante)
                    st.info("💡 Respuesta generada por análisis automático")

                st.markdown("#### 💬 Interpretación:")
                st.markdown(respuesta)

                st.markdown("---")
                st.markdown("#### 🔁 Comparación de decisiones")
                if coincide:
                    st.success(f"✅ Tu decisión **'{decision_estudiante}'** "
                               f"coincide con la decisión automática.")
                else:
                    st.error(f"❌ Tu decisión **'{decision_estudiante}'** "
                             f"NO coincide con la decisión automática "
                             f"**'{decision_auto}'**. Revisa el análisis.")