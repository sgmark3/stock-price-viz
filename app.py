#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


#@st.cache()
def load_data(t):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=' + t + '&apikey=VW9MMPY6I13TVX8J'
    r = requests.get(url)
    data_monthly = r.json()
    df = pd.DataFrame(data_monthly['Monthly Time Series'])
    return df

y_options = ['1. open', '4. close', '3. low', '2. high', '5. volume']

# Allow use to choose
y_axis = st.sidebar.selectbox('Which value do you want to explore', y_options)

ticker = 'GOOGL'

# Read in the cereal data
dft = load_data(ticker).transpose()

d = {'1. open':[float(item) for item in dft['1. open']], '2. high':[float(item) for item in dft['2. high']],
    '3. low':[float(item) for item in dft['3. low']], '4. close':[float(item) for item in dft['4. close']],
    '5. volume':[float(item) for item in dft['5. volume']]}

df = pd.DataFrame(data=d) 

df['date'] = dft.index

st.title('Closing price of ' + ticker)


# plot the value
fig = px.line(df,
                x='date',
                y=y_axis)

st.plotly_chart(fig)

