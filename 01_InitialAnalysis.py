
# coding: utf-8

# # Initial analysis
# 
# Trying to answer question 1
# 

# # Setup

# In[2]:

## Interactive magics - comment out if running from another script
get_ipython().magic('matplotlib inline')
get_ipython().magic("qtconsole --colors=linux --ConsoleWidget.font_size=12 --ConsoleWidget.font_family='Consolas'")


# In[3]:

import sqlite3
import numpy as np
import pandas as pd
import seaborn as sns

pd.set_option('display.mpl_style', 'default')
pd.set_option('display.notebook_repr_html', True)
np.random.seed(0)


# In[4]:

cnx = sqlite3.connect('data/volunteerireland_datadive2015.db')


# ## Load Data

# In[7]:

dfv = pd.read_sql('select * from vi_merged', cnx, index_col='index')
print(dfv.shape)
dfv.head()


# In[8]:

dfoppsaltm = pd.read_sql('select * from dfoppsaltm', cnx, index_col='index')
print(dfoppsaltm.shape)
dfoppsaltm.head()


# In[9]:

dforgs = pd.read_sql('select * from dforgs', cnx, index_col='index')
print(dforgs.shape)
dforgs.head()


# In[29]:

dfoppsapfr = pd.read_sql('select * from dfoppsapfr', cnx, index_col='index'
                        ,parse_dates=['apfr_volunteer_opportunity_applied_for_created_date'])
print(dfoppsapfr.shape)
dfoppsapfr.head()


# In[63]:

dfplc = pd.read_sql('select * from dfplc', cnx, index_col='index'
                   ,parse_dates=['plc_place_volunteer_created_date'
                                ,'plc_volunteer_opportunity_created_date'])
print(dfplc.shape)
dfplc.head()


# In[12]:

dfvol = pd.read_sql('select * from dfvol', cnx, index_col='index')
print(dfvol.shape)
dfvol.head()


# ---

# ### Count unique vols who applied

# In[20]:

print(dfv.groupby('vol_id_apfr').size().shape[0])
ax = dfv.groupby('vol_id_apfr').size().plot(kind='box'
                ,showfliers=False, showmeans=True, vert=False)


# ### Count unique vols who applied by year

# In[59]:

dfv_app = pd.merge(dfv, dfoppsapfr
                   ,how='left', left_on='apfr_id', right_on='apfr_id')


# In[60]:

dfv_app['app_year'] = dfv_app['apfr_volunteer_opportunity_applied_for_created_date'].apply(
            lambda x: x.year)
dfv_app.groupby(['vol_id_apfr','app_year']).size().unstack().count()


# In[68]:

ax = dfv_app.groupby(['vol_id_apfr','app_year']).size().unstack().plot(
            kind='box', showfliers=False, showmeans=True, figsize=(12, 6))
ax.set_title('Distribution of count of applications per volunteer per year')


# ---

# ### Count unique vols who placed

# In[55]:

print(dfv.groupby('vol_id_plc').size().shape[0])
ax = dfv.groupby('vol_id_plc').size().plot(kind='box'
                ,showfliers=False, showmeans=True, vert=False)


# ### Count unique vols who placed by year

# In[65]:

dfv_plc = pd.merge(dfv, dfplc
                   ,how='left', left_on='plc_id', right_on='plc_id')


# In[66]:

dfv_plc['app_year'] = dfv_plc['plc_place_volunteer_created_date'].apply(
            lambda x: x.year)
dfv_plc.groupby(['vol_id_plc','app_year']).size().unstack().count()


# In[69]:

ax = dfv_plc.groupby(['vol_id_plc','app_year']).size().unstack().plot(
            kind='box', showfliers=False, showmeans=True, figsize=(12, 6))
ax.set_title('Distribution of count of placements per volunteer per year')


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



