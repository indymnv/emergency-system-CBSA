from email.utils import collapse_rfc2231_value
import pandas as pd
import numpy as np
import streamlit as st
import plotly.figure_factory as ff
import plotly.express as px
from pathlib import Path
import os
import datetime
import preprocessor

st.title("Registro de Emergencias CBSA")

#Config
DATE_COLUMN = 'Fecha'
DATA_URL = os.path.join(os.path.dirname(__file__), '..', 'data', 'cleaned_data.csv')
#Cantidad de emergencias
# Create a text element and let the reader know the data is loading.
#@st.cache

# Load 10,000 rows of data into the dataframe.
data = pd.read_csv(DATA_URL)
data.Fecha = pd.to_datetime(data.Fecha)
data.Hora_del_llamado.fillna(data["Hora_de_primera_respuesta"],inplace=True) #first fill
data.Hora_del_llamado.fillna(data["Hora_de_término_de_la_emergencia"],inplace=True) # second fill 
data["int_hour"] = data.Hora_del_llamado.str[:2].astype(int)
data = data.sort_values('Fecha')

#add calendar dates in side bar
st.sidebar.write("Seleccione los filtros deseados")
start_date = st.sidebar.date_input(
        "Fecha de inicio",
        datetime.date(2020,1,1)
        )
end_date = st.sidebar.date_input(
        "Fecha de término",
        datetime.date(2022,6,1)
        )

time_step = st.sidebar.slider(label = "Periodo del tiempo en un día",
        min_value = 0,
        max_value = 24,
        value = (0,24))

options = st.sidebar.multiselect(
     'Seleccione el tipo de emergencias que quiere visualizar',
     [10.0, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 10.9, 10.12],
     [10.0, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 10.9, 10.12])




df_filtered = data[(data["Fecha"] > pd.to_datetime(start_date)) & (data["Fecha"] < pd.to_datetime(end_date)) 
                        & (data['int_hour']>= int(time_step[0])) & (data['int_hour']<= int(time_step[1])) &
                        (data["Emergencias_cod_corto"].isin(options)) ] 
# Notify the reader that the data was successfully loaded.


col1, col2, col3  = st.columns(3)
col1.metric("Total Emergencias", value = df_filtered.shape[0])
col2.metric("Tiempo Respuesta Promedio (min)", value = round(df_filtered["Tiempo_respuesta"].median(),2))
col3.metric("Tiempo control Promedio (min)", value = round(df_filtered["Tiempo_en_controlar_emergencia"].mean(),2))

if st.checkbox('Mostrar 10 últimas emergencias registradas'):
    st.subheader('Raw data')
    st.write(df_filtered.tail(10))


#Insert line chart with total of emergencies
st.subheader('Cantidad de emergencias por mes')
df2 = preprocessor.general_line_chart(df_filtered)
st.line_chart(df2)

st.subheader('Cantidad de Emergencias por Compañía')
chart_data = df_filtered[['1cia', '2cia', '3cia', '4cia']].sum() 
st.bar_chart(chart_data, use_container_width=True)


#Insert line chart with total by emergencies
st.subheader('Cantidad de emergencias mensual por clasificación')
df3 = preprocessor.line_chart_by_emergencies(df_filtered)
st.line_chart(df3)

#stacked bar chart
st.subheader('Share de emergencias por clasificación')
df_stacked = round(df3[df3.columns].apply(lambda x: x/x.sum(), axis=1)*100,2)
st.bar_chart(df_stacked)

col1, col2 = st.columns(2)
col1.write("Mediana tiempo respuesta (min)")
df_time_respuesta = preprocessor.line_chart_for_time(df_filtered, "Tiempo_respuesta")
col1.line_chart(df_time_respuesta)

col2.write("Mediana Tiempo de control (min)")
df_time_control = preprocessor.line_chart_for_time(df_filtered, "Tiempo_en_controlar_emergencia")
col2.line_chart(df_time_control)

fig = px.line(df2)
st.write()

#st.subheader('Mapa de emergencias')
#st.map(df_filtered)


