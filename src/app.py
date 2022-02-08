import pandas as pd
import numpy as np
import streamlit as st
import plotly.figure_factory as ff
import plotly.express as px
from pathlib import Path
import os
import datetime
import preprocessor

st.title("Sistema de control de emergencias CBSA")

#Config
DATE_COLUMN = 'Fecha'
DATA_URL = os.path.join(os.path.dirname(__file__), '..', 'data', 'emergencias-2021.csv')
#Cantidad de emergencias
# Create a text element and let the reader know the data is loading.
#@st.cache
data_load_state = st.text('cargando data..')

# Load 10,000 rows of data into the dataframe.
data = preprocessor.load_data(DATA_URL, DATE_COLUMN)
data_load_state.text('Data cargada!')

#add calendar dates in side bar
start_date = st.sidebar.date_input(
        "Fecha de inicio",
        datetime.date(2021,1,1)
        )
end_date = st.sidebar.date_input(
        "Fecha de término",
        datetime.date(2023,1,1)
        )

time_step = st.sidebar.slider(label = "Periodo del tiempo en un día",
        min_value = 0,
        max_value = 24,
        value = (0,24))

st.sidebar.write(time_step[0])

df_filtered = data[(data["Fecha"] > pd.to_datetime(start_date)) & (data["Fecha"] < pd.to_datetime(end_date)) & (data['int_hour']>= int(time_step[0])) & (data['int_hour']<= int(time_step[1])) ] 
# Notify the reader that the data was successfully loaded.


col1, col2, col3  = st.columns(3)
col1.metric("Total Emergencias", value = df_filtered.shape[0])
col2.metric("Tiempo Respuesta Promedio (minutos)", value = round(df_filtered["Tiempo respuesta"].median(),2))
col3.metric("Tiempo control Promedio (minutos)", value = round(df_filtered["Tiempo en controlar emergencia"].mean(),2))

if st.checkbox('Mostrar 10 últimas emergencias registradas'):
    st.subheader('Raw data')
    st.write(df_filtered.tail(10))


#Insert line chart with total of emergencies
st.subheader('Cantidad de emergencias por mes')
df2 = preprocessor.general_line_chart(df_filtered)
st.line_chart(df2)

#Insert line chart with total by emergencies
df3 = preprocessor.line_chart_by_emergencies(df_filtered)
st.line_chart(df3)

fig = px.line(df2)
st.write()

st.subheader('Mapa de emergencias')
st.map(df_filtered)


