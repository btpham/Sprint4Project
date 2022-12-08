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
data.info()


# ## Data Cleanup - missing values, duplicates, change type
# 1. Convert missing values for cylinders to the median of all non-missing cylinder values
# 2. Convert missing values for odometer to the mean of all non-missing odometer values
# 3. Convert missing 'is_4wd' (either 0 - no, or 1 - yes) to median non-missing is_4wd values
# 4. Convert missing paint_color to 'unknown' string

# # Having some issues with converting missing values in 'is_4wd' to boolean - see errors below

# In[3]:


# Missing Values: convert model_year, cylinders, odometer, and is_4wd to more suitable values

data['cylinders'] = data['cylinders'].fillna(data['cylinders'].median())
data['odometer'] = data['odometer'].fillna(data['odometer'].mean())
data['is_4wd'] = data['is_4wd'].fillna(data['is_4wd'].a.bool())
data['model_year'] = data['model_year'].fillna(data['model_year'].median())
data['paint_color'] = data['paint_color'].fillna('unknown')


# <b> There was a reviewer comment to adjust model_year, but I don't really use it in my graphs, so I decided not to modify it. </b>

# In[ ]:


# Format Change: convert date_posted to date_time
data['date_posted'] = pd.to_datetime(data['date_posted'], format = '%Y-%m-%d')


# In[ ]:


# Remove Duplicates:
data = data.drop_duplicates(subset = None, keep = 'first')


# In[ ]:


data.info()


# In[ ]:


# creating title for page

st.header("Pricing Analysis")


# In[ ]:


# create options for histogram elements by creating selectbox
list_for_hist = ['is_4wd','model','condition']
choice_for_hist = st.selectbox('Choose Options', list_for_hist)

# create histogram using plotly-express
fig1 = px.histogram(data, x ="price", color = choice_for_hist)
fig1.update_layout(
title = '<b>Price Analysis -- {}</b>'.format(choice_for_hist))

# embedding into streamlit
st.plotly_chart(fig1)


# In[ ]:


# create distribution for scatterplot
list_for_scatter = ['model', 'condition', 'odometer']
choice_for_scatter = st.selectbox('Choose Factors: ',list_for_scatter)

# create scatterplot using plotly-express
fig2 = px.scatter(data,x = choice_for_scatter, y = 'price')
fig2.update_layout(
title = '<b>Price based on {}</b>'.format(choice_for_scatter))
st.plotly_chart(fig2)


# In[ ]:





# In[ ]:




