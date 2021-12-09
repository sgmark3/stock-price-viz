import numpy as np
import os
import requests
import streamlit as st
import pandas as pd
from datetime import datetime

import plotly.express as px

keycode = str(os.getenv('API_KEY'))

def load_data(t):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + t + '&interval=1min&apikey=' + keycode
    r = requests.get(url)
    data = r.json()
    df = pd.DataFrame(data['Time Series (1min)']).transpose()
    df['Time of the day'] = [datetime.strptime(entry,"%Y-%m-%d %H:%M:%S") for entry in df.index]
    df = df.rename(columns={'1. open':'Opening price', '2. high':'High', '3. low':'Low', '4. close':'Closing price', '5. volume':'Volume'})
    return df

ticker = st.text_input('Enter stock name here','MSFT')

y_options = ['Opening price', 'High', 'Low', 'Closing price', 'Volume']
             #'6. One day return']
y_axis = st.sidebar.selectbox('Which value do you want to explore', y_options)

df = load_data(ticker)

if y_axis == 'Opening price' or y_axis == 'Closing price':
    if y_axis == 'Opening price':
        st.title('Opening price of ' + ticker)
    else:
        st.title('Closing price of ' + ticker)
elif y_axis == 'High' or y_axis == 'Low':
    st.title(y_axis + 'est price of ' + ticker)
elif y_axis == 'Volume':
    st.title(ticker + ' Trade volume')

fig = px.line(df, x='Time of the day',y=y_axis)
st.plotly_chart(fig)
