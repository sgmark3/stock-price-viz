#!/usr/bin/env python
# coding: utf-8

# In[26]:


import numpy as np
import os
import requests
import streamlit as st
import pandas as pd
import plotly.express as px

keycode = str(os.getenv('API_KEY'))

def load_data(t):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + t + '&apikey=' + keycode
    r = requests.get(url)
    data = r.json()
    df = pd.DataFrame(data['Time Series (Daily)']).transpose()
    dates = list(df.index)
    df['years'] = np.array([int(item.split('-')[0]) for item in dates])
    df['months'] = np.array([int(item.split('-')[1]) for item in dates])
    df['days'] = np.array([int(item.split('-')[2]) for item in dates])
    return df

ticker = st.text_input('Enter stock name here','MSFT')

Year = st.text_input('Year','2021')

Month = st.text_input('Month','10')

y_options = ['4. close', '1. open', '3. low', '2. high', '5. volume', 'one_day_return']

y_axis = st.sidebar.selectbox('Which value do you want to explore', y_options)

df = load_data(ticker)

dfy = pd.DataFrame(df[df['years'] == int(Year)])
dfm = pd.DataFrame(dfy[dfy['months'] == int(Month)])

d = {'1. open':[float(item) for item in dfm['1. open']], '2. high':[float(item) for item in dfm['2. high']],
    '3. low':[float(item) for item in dfm['3. low']], '4. close':[float(item) for item in dfm['4. close']],
    '5. volume':[float(item) for item in dfm['5. volume']]}

dff = pd.DataFrame(data=d)

dff['dates'] = dfm.index 

returns = round(np.log(dff['4. close']).diff()*100,2)
returns.dropna(inplace = True)

d1 = {'dates':list(dfm.index)[1:], 'one_day_return':returns}

dr = pd.DataFrame(data=d1)

if y_axis == '1. open' or y_axis == '4. close':
   if y_axis == '1. open':
      st.title('opening price of ' + ticker)
   else:
      st.title('closing price of ' + ticker)
elif y_axis == '2. high' or y_axis == '3. low':
   st.title(y_axis.split('.')[1] + 'est price of ' + ticker)
elif y_axis == '5. volume':
   st.title(ticker + ' trade volume')
else:
   st.title('one day percentage log return for ' + ticker)


# plot the value
if y_axis == 'one_day_return':
   fig = px.line(dr, x='dates',y=y_axis)
else:
   fig = px.line(dff, x='dates',y=y_axis)

st.plotly_chart(fig)

