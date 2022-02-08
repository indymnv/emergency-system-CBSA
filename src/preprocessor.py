import pandas as pd
import numpy as np

def load_data(DATA_URL, DATE_COLUMN):
    data = pd.read_csv(DATA_URL, encoding="latin-1", sep=';')
    data['Fecha'] = pd.to_datetime(data["Fecha"])
    data['mes'] = data[DATE_COLUMN].dt.month_name()
    data['Periodo']=  data['Fecha'].dt.to_period('M')
    data = data.sort_values('Fecha')
    data['int_hour'] = data['Hora del llamado'].str[:2].astype(int) 
    data.rename(columns = {'LATITUDE': 'lat', 'LONGITUDE':'lon'}, inplace = True)
    
    data['lat']=data['lat'].str.replace(",",".", regex = True)
    data['lon']=data['lon'].str.replace(",", ".", regex = True)
    data['lat']=data['lat'].astype(float)
    data['lon']=data['lon'].astype(float)
    return data

def general_line_chart(df):
    
    dft1= pd.DataFrame(df['Fecha'].dt.to_period('M').value_counts().sort_index())
    dft1.columns = ['Total']
    dft1.index = dft1.index.astype(str, copy=False)
    return dft1

def line_chart_by_emergencies(df):
    df['Emergencias_cod_corto'] = df['Tipo de emergencias']
    mapper = {'10.6.1': '10.6',
          '10.2.1': '10.2', 
          '10.5': '10.5',
          '10.0': '10.0',
          '10.4.1': '10.4',
          '10.4.3': '10.4',
          '10.7': '10.7',
          '10.4.2': '10.4',
          '10.1': '10.1',
          '10.6.2': '10.6',
          '10.3.1': '10.3',
          '10.8': '10.8',
          '10.12X10.2.2': '10.2',
          '10.2.2': '10.2',
          '10.12X10.0': '10.0',
          '10.5.1': '10.5',
          '10.12X10.2.1': '10.2',
          '10.9': '10.9',
          '10.10': '10.10'}

    df['Emergencias_cod_corto'] = df['Emergencias_cod_corto'].map(mapper)
    df2 = df.pivot_table(index = 'Periodo', 
            columns = 'Emergencias_cod_corto', 
            fill_value = 0,
            aggfunc = 'count')
    df2 = df2['Tipo de emergencias']
    indices = df2.index
    indices.name = None
    columnas = df2.columns
    columnas.name = None
    valores = df2.values

    df3 = pd.DataFrame(index = indices, columns = columnas, data = valores)
    df3.index = df3.index.astype(str, copy = False)
    return df3
