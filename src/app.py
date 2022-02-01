import pandas as pd
import numpy as np
import streamlit as st
import plotly.figure_factory as ff
import plotly.express as px
from pathlib import Path
import os
import datetime

st.title("Sistema de control de emergencias CBSA")

#Config
DATE_COLUMN = 'Fecha'
DATA_URL = os.path.join(os.path.dirname(__file__), '..', 'data', 'emergencias-2021.csv')

@st.cache
def load_data():
    data = pd.read_csv(DATA_URL, encoding="latin-1", sep=';')
    data['Fecha'] = pd.to_datetime(data["Fecha"])
    data['mes'] = data[DATE_COLUMN].dt.month_name()
    data['periodo']=  pd.to_datetime(data["Fecha"],format='%Y%m')
    data = data.sort_values('Fecha')

    data.rename(columns = {'LATITUDE': 'lat', 'LONGITUDE':'lon'}, inplace = True)
    
    data['lat']=data['lat'].str.replace(",",".", regex = True)
    data['lon']=data['lon'].str.replace(",", ".", regex = True)
    data['lat']=data['lat'].astype(float)
    data['lon']=data['lon'].astype(float)
    return data

#Cantidad de emergencias
# Create a text element and let the reader know the data is loading.
data_load_state = st.text('cargando data..')
# Load 10,000 rows of data into the dataframe.
data = load_data()
data_load_state.text('Data cargada!')


start_date = st.sidebar.date_input(
        "Fecha de inicio",
        datetime.date(2021,1,1)
        )
end_date = st.sidebar.date_input(
        "Fecha de término",
        datetime.date(2023,1,1)
        )

df_filtered = data[(data["Fecha"] > pd.to_datetime(start_date)) & (data["Fecha"] < pd.to_datetime(end_date))] 
# Notify the reader that the data was successfully loaded.


col1, col2, col3  = st.columns(3)
col1.metric("Total Emergencias", value = df_filtered.shape[0])
col2.metric("Tiempo Respuesta Promedio (minutos)", value = round(df_filtered["Tiempo respuesta"].median(),2))
col3.metric("Tiempo control Promedio (minutos)", value = round(df_filtered["Tiempo en controlar emergencia"].mean(),2))

if st.checkbox('Mostrar 10 últimas emergencias registradas'):
    st.subheader('Raw data')
    st.write(df_filtered.tail(10))

st.subheader('Cantidad de emergencias por mes')
dft1= pd.DataFrame(df_filtered['Fecha'].dt.to_period('M').value_counts().sort_index())
dft1.columns = ['Total']
dft1.index = dft1.index.astype(str, copy=False)
st.line_chart(dft1)

fig = px.line(dft1)
st.write()

st.text('Mapa de emergencias')
st.map(df_filtered)


