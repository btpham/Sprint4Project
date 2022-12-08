#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import streamlit as st
import plotly.express as px


# ## Project requirements
# 
# 1. project structure
#     - README.md
#     - app.py
#     - <name_of_your_dataset>.csv
#     - notebooks
#          - EDA.ipynb
#     - .streamlit
#     - config.toml 
# 
# 2. web accessibility through the browser
#     - use Streamlit and Render
#     
# 3. contains at least one of each of the following:
#     - at least one header with text (st.header)
#     - at least one histogram
#     - at least one scatterplot

# In[2]:


data =  pd.read_csv('vehicles_us.csv')


# In[3]:


# convert model_year, cylinders, odometer, and is_4wd from floating to integers

data['cylinders'] = data['cylinders'].fillna(0).astype(int)
data['odometer'] = data['odometer'].fillna(0).astype(int)
data['is_4wd'] = data['is_4wd'].fillna(0).astype(int)


# convert date_posted to date_time

data['date_posted'] = pd.to_datetime(data['date_posted'], format = '%Y-%m-%d')


# In[4]:


# creating title for page

st.header("Pricing Analysis")


# In[5]:


# create options for histogram elements by creating selectbox
list_for_hist = ['is_4wd','model','condition']
choice_for_hist = st.selectbox('Choose Options', list_for_hist)

# create histogram using plotly-express
fig1 = px.histogram(data, x = 'price', color = choice_for_hist)
fig1.update_layout(
title = '<b>Price Analysis -- {}</b>'.format(choice_for_hist))

# embedding into streamlit
st.plotly_chart(fig1)


# In[7]:


# create distribution for scatterplot
list_for_scatter = ['model', 'condition', 'odometer']
choice_for_scatter = st.selectbox('Choose Factors: ',list_for_scatter)

# create scatterplot using plotly-express
fig2 = px.scatter(data,x = choice_for_scatter, y = 'price')
fig2.update_layout(
title = '<b>Price based on {}</b>'.format(choice_for_scatter))
st.plotly_chart(fig2)


# In[ ]:




