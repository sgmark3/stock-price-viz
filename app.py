#!/usr/bin/env python
# coding: utf-8

# In[26]:


import numpy as np
import os
import requests
import streamlit as st
import pandas as pd
from datetime import datetime

import plotly.express as px

keycode = str(os.getenv('API_KEY'))

# def load_data(t):
#     url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + t + '&apikey=' + keycode
#     r = requests.get(url)
#     data = r.json()
#     df = pd.DataFrame(data['Time Series (Daily)']).transpose()
#     dates = list(df.index)
#     df['years'] = np.array([int(item.split('-')[0]) for item in dates])
#     df['months'] = np.array([int(item.split('-')[1]) for item in dates])
#     df['days'] = np.array([int(item.split('-')[2]) for item in dates])
#     return df

def load_data(t):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + t + '&interval=1min&apikey=' + keycode
    r = requests.get(url)
    data = r.json()
    df = pd.DataFrame(data['Time Series (1min)']).transpose()
    df['Time of the day'] = [datetime.strptime(entry,"%Y-%m-%d %H:%M:%S") for entry in df.index]
    df = df.rename(columns={'1. open':'Opening price', '2. high':'High', '3. low':'Low', '4. close':'Closing price', '5. volume':'Volume'})
    return df

ticker = st.text_input('Enter stock name here','MSFT')

#Year = st.text_input('Year','2021')

#Month = st.text_input('Month','10')

y_options = ['Opening price', 'High', 'Low', 'Closing price', 'Volume']
             #'6. One day return']

y_axis = st.sidebar.selectbox('Which value do you want to explore', y_options)

df = load_data(ticker)

# dfy = pd.DataFrame(df[df['years'] == int(Year)])
# dfm = pd.DataFrame(dfy[dfy['months'] == int(Month)])

# d = {'1. Opening price':[float(item) for item in dfm['1. open']], '2. High':[float(item) for item in dfm['2. high']],
#     '3. Low':[float(item) for item in dfm['3. low']], '4. Closing price':[float(item) for item in dfm['4. close']],
#     '5. Volume':[float(item) for item in dfm['5. volume']]}

#dff = pd.DataFrame(data=d)

#dff['dates'] = dfm.index 

# returns = round(np.log(dff['4. Closing price']).diff()*100,2)
# returns.dropna(inplace = True)

#d1 = {'dates':list(dfm.index)[1:], '6. one_day_return':returns}

#dr = pd.DataFrame(data=d1)

if y_axis == 'Opening price' or y_axis == 'Closing price':
    if y_axis == 'Opening price':
        st.title('Opening price of ' + ticker)
    else:
        st.title('Closing price of ' + ticker)
elif y_axis == 'High' or y_axis == 'Low':
    st.title(y_axis + 'est price of ' + ticker)
elif y_axis == 'Volume':
    st.title(ticker + ' Trade volume')
#else:
#    st.title('one day percentage log return for ' + ticker)


# # plot the value
# if y_axis == '6. one_day_return':
#    fig = px.line(dr, x='dates',y=y_axis)
# else:
#    fig = px.line(dff, x='dates',y=y_axis)

fig = px.line(df, x='Time of the day',y=y_axis)
st.plotly_chart(fig)
