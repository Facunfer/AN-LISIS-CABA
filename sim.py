import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Cargar los datos
resultados = pd.read_csv(f"https://raw.githubusercontent.com/Facunfer/AN-LISIS-CABA/refs/heads/main/InteractiveSheet_2025-01-03_03_20_37%20-%20Hoja%201%20(1).csv")

# Ordenar las comunas del 1 al 15
resultados = resultados.sort_values(by='seccion_nombre').reset_index(drop=True)

# Configuración de la página de Streamlit
st.set_page_config(page_title="Simulador de Votos LLA", layout="wide")
st.title("Simulador de Votos por Comuna - LLA")

# Inicializar variables para la suma total de votos
suma_votos_simulados = 0

# Crear una fila para cada comuna en el DataFrame
for index, row in resultados.iterrows():
    comuna = row['seccion_nombre']
    votos_generales = row['Votos en Generales']
    votos_ballotage = row['Votos en Ballotage']

    # Crear un cuadro para cada comuna
    with st.container():
        st.markdown(f"### {comuna}")
        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            # Input de porcentaje
            porcentaje_input = st.number_input(f"% en {comuna}", min_value=0.0, max_value=100.0, step=0.1, key=f"porcentaje_{index}")
            votos_equivalentes = int((porcentaje_input / 100) * votos_generales)

        with col2:
            # Input manual de votos (sin límite máximo)
            votos_input = st.number_input(f"Votos simulados en {comuna}", min_value=0, step=1, value=votos_equivalentes, key=f"votos_{index}")  # Sin max_value

        with col3:
            row1, row2 = st.columns([1, 1])
            with row1:
                # Mostrar los votos LLAxVotoGen en Votos Generales
                st.metric(label="Votos Generales", value=f"{row['LLAxVotoGen']:,}")
                st.metric(label="% LLA Generales", value=f"{row['%LLA Gen']:.2f}%")

            with row2:
                # Mostrar los votos LLAxVotoBall en Votos Ballotage
                st.metric(label="Votos Ballotage", value=f"{row['LLAxVotoBall']:,}")
                st.metric(label="% LLA Ballotage", value=f"{row['%LLA Ball']:.2f}%")

        # Sumar los votos simulados
        suma_votos_simulados += votos_input

# Crear los gráficos de medidor
fig1 = go.Figure(go.Indicator(
    mode="gauge+number",
    value=suma_votos_simulados,
    gauge={
        'axis': {'range': [0, resultados['LLAxVotoGen'].sum()]},
        'bar': {'color': "violet"},
    },
    title={'text': f"Votos Generales: {resultados['LLAxVotoGen'].sum():,}"}
))

fig2 = go.Figure(go.Indicator(
    mode="gauge+number",
    value=suma_votos_simulados,
    gauge={
        'axis': {'range': [0, resultados['LLAxVotoBall'].sum()]},
        'bar': {'color': "violet"},
    },
    title={'text': f"Votos Ballotage: {resultados['LLAxVotoBall'].sum():,}"}
))

# Mostrar los gráficos
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.plotly_chart(fig2, use_container_width=True)