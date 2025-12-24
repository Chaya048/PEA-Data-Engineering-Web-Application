import streamlit as st
import requests
import json
import pandas as pd

# select a file from the list
files = requests.get('http://localhost:5000/api/files')
files = json.loads(files.text)
selected_file = st.sidebar.selectbox('Select File', options=files)

# select a meterID
meters = requests.get(f'http://localhost:5000/api/data/{selected_file}')
meters = json.loads(meters.text)
selected_meter = st.sidebar.selectbox('Select MeterID', options=meters)

# display the data
data = requests.get(f'http://localhost:5000/api/data/{selected_file}/{selected_meter}')
data = json.loads(data.text)
df = pd.DataFrame(data)
df['DateTime'] = pd.to_datetime(df['DateTime'])
df.set_index('DateTime', inplace=True)

# select a day
days = sorted(list(set(df.index.date)))
selected_start_day = st.sidebar.selectbox('Start date', options=days)
selected_end_day = st.sidebar.selectbox('End date', options=days)    
df = df[(df.index.date >= selected_start_day) & (df.index.date <= selected_end_day)]

table, stats, chart = st.tabs(['Data', 'Statistics', 'Line chart'])
with table:
    st.dataframe(df)
with stats:
    st.write(df.describe())
with chart:
    st.line_chart(df['kwh'])
