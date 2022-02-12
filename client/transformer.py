import numpy as np
import pandas as pd
import os

DATA_URL = os.path.join(os.path.dirname(__file__), '..', 'data', 'emergencias-2021.csv')

df = pd.read_csv(DATA_URL, encoding = 'latin-1', sep = ';')

df['json'] = df.to_json(orient='records', lines = True).splitlines()

dfjson = df['json']
print(dfjson.head())

np.savetxt(r'../emergency-system-CBSA/data/output.txt', dfjson.values, fmt='%s')
