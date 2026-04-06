import streamlit as st
import pandas as pd
import numpy as np

def modulo_carga_datos():
    st.header("Carga de Datos")
    st.write("Sube un archivo CSV o genera datos sintéticos para comenzar.")

    opcion = st.radio("¿Cómo deseas cargar los datos?", 
                      ["Subir archivo CSV", "Generar datos sintéticos"])

    df = None

    if opcion == "Subir archivo CSV":
        archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])
        if archivo is not None:
            df = pd.read_csv(archivo)
            st.success("✅ Archivo cargado correctamente")
            st.dataframe(df.head(10))

    elif opcion == "Generar datos sintéticos":
        st.subheader("Parámetros de generación")

        col1, col2, col3 = st.columns(3)
        with col1:
            n = st.number_input("Número de datos (n)", 
                                min_value=30, max_value=10000, value=100)
        with col2:
            media = st.number_input("Media", value=50.0)
        with col3:
            desv = st.number_input("Desviación estándar", 
                                   min_value=0.1, value=10.0)

        if st.button("Generar datos"):
            datos = np.random.normal(loc=media, scale=desv, size=int(n))
            df = pd.DataFrame({"valor": datos})
            st.success(f"Se generaron {int(n)} datos sintéticos")
            st.dataframe(df.head(10))

    if df is not None:
        st.subheader("Selección de variable")
        columnas = df.columns.tolist()
        variable = st.selectbox("Selecciona la variable a analizar", columnas)
        st.session_state["df"] = df
        st.session_state["variable"] = variable
        st.info(f"Variable seleccionada: **{variable}**")

    return df
