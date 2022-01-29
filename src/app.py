import pandas as pd
import numpy as np
import streamlit as st
import plotly.figure_factory as ff
import plotly.express as px
from pathlib import Path
import os

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



# Create a text element and let the reader know the data is loading.
data_load_state = st.text('cargando data..')
# Load 10,000 rows of data into the dataframe.
data = load_data()

# Notify the reader that the data was successfully loaded.

data_load_state.text('Data cargada!')

if st.checkbox('Mostrar data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Cantidad de emergencias por mes')
dft1 = data['mes'].value_counts()
st.line_chart(dft1)

fig = px.line(dft1)
st.write()

st.text('Mapa de emergencias')
st.map(data)


