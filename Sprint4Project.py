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

# In[3]:


# Fill in missing values: 'model_year' and 'cylinders'
grouped_by_model = data.groupby('model').agg({'model_year': 'median', 'cylinders': 'median'})
for model in data['model'].unique():
    data.loc[(data['model'] == model) & (data['model_year'].isna()), 'model_year'] =         grouped_by_model.loc[grouped_by_model.index == model, 'model_year'][0]
    data.loc[(data['model'] == model) & (data['cylinders'].isna()), 'cylinders'] =         grouped_by_model.loc[grouped_by_model.index == model, 'cylinders'][0]

data.isna().sum()
data.info()


# In[4]:


# Fill in missing values: 'cylinder' to median of cylinder by model year
data['cylinders'] = data['cylinders'].fillna(data.groupby('model').agg({'cylinders':'median'}).to_dict)

# Check that cylinders show 0 missing values
data.isna().sum()


# In[5]:


# Missing Values 'is_4wd'
data['is_4wd'] = data['is_4wd'].fillna(0)
data['is_4wd'] = data['is_4wd'].astype(bool)

# Check that is_4wd shows 0 missing values
data.isna().sum()


# In[6]:


# Missing Values: paint_color to 'unknown'
data['paint_color'] = data['paint_color'].fillna('unknown')


# In[7]:


# Missing Values: convert odometer to mean by model_year and paint color to 'unknown'
grouped_by_condition = data.groupby('condition').agg({'odometer': 'mean'})
for condition in data['condition'].unique():
    data.loc[(data['condition'] == condition) & (data['odometer'].isna()), 'odometer'] =         grouped_by_condition.loc[grouped_by_condition.index == condition, 'odometer'][0]
    
# Check that odometer shows 0 missing values
data.isna().sum()


# In[8]:


# Format Change: convert date_posted to date_time
data['date_posted'] = pd.to_datetime(data['date_posted'], format = '%Y-%m-%d')


# In[9]:


# Remove Duplicates:
data = data.drop_duplicates(subset = None, keep = 'first')


# In[10]:


data.info()


# In[11]:


data['odometer'] = pd.to_numeric(data['odometer'])


# In[12]:


# creating title for page

st.header("Model Comparison and Pricing Analysis")


# In[13]:


# create histogram using plotly-express to compare 2 models for is_4wd
fig1 = px.histogram(data, x = 'is_4wd', color='model')
fig1.update_layout(
title = '<b>Count -- {}</b>'.format('Has 4 Wheel Drive'))

# embedding into streamlit
st.plotly_chart(fig1)


# In[14]:


# create histogram using plotly-express to compare 2 models for color
fig2 = px.histogram(data, x = 'paint_color', color='model')
fig2.update_layout(
title = '<b>Count -- {}</b>'.format('Paint Color'))

# embedding into streamlit
st.plotly_chart(fig2)


# In[15]:


# create histogram using plotly-express to compare 2 models for condition
fig3 = px.histogram(data, x = 'condition', color='model')
fig3.update_layout(
title = '<b>Count -- {}</b>'.format('Condition'))

# embedding into streamlit
st.plotly_chart(fig3)


# In[16]:


# create distribution for scatterplot
list_for_scatter = ['model', 'condition', 'odometer']
choice_for_scatter = st.selectbox('Choose Factors: ',list_for_scatter)

# create scatterplot using plotly-express
fig4 = px.scatter(data,x = choice_for_scatter, y = 'price')
fig4.update_layout(
title = '<b>Price based on {}</b>'.format(choice_for_scatter))
st.plotly_chart(fig4)

