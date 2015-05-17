
# coding: utf-8

# ####DataKind Dublin
# 
# ## Volunteer Ireland DataDive Project 2015
# # Initial Import of First Cut of Raw Data
# 
# _Feb 2015_
# 
# Quick & dirty import of raw csv files and write to sqlite3 db
# 
# + [Setup](#Setup)
#     + [Local Functions](#Local-Functions)
#     + [Load Data](#Load Data)    
#    
# 

# # Setup

# In[1]:

## Interactive magics - comment out if running from another script
get_ipython().magic('matplotlib inline')
get_ipython().magic("qtconsole --colors=linux --ConsoleWidget.font_size=12 --ConsoleWidget.font_family='Consolas'")


# In[2]:

from __future__ import division, print_function
from collections import OrderedDict
import unicodedata
import sys
import re
import sqlite3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Set some defaults
pd.set_option('display.mpl_style', 'default')
pd.set_option('display.notebook_repr_html', True)
np.random.seed(0)


# ## Local Functions

# In[3]:

remove_punct_map = dict.fromkeys(i for i in range(sys.maxunicode)
                      if unicodedata.category(chr(i)).startswith('P'))

def snakeycase(s,punctmap=remove_punct_map):
    """ return a string that has been stripped of punctuation, trimmed, lowercased 
        and spaces replaced by underscores .
        e.g. " I'm a Fan, of snakey-strings :) " -> "im_a_fan_of_snakeystrings"
    """
    newstring = s.translate(punctmap)
    return '_'.join(newstring.lower().split())


# ## Load Data

# #### Volunteer Info

# In[4]:

raw_volunteers = pd.read_csv('datadrop_20150325/cleaned_csv/volunteers.csv')
raw_volunteers.rename(columns=lambda x: snakeycase(x), inplace=True)
print(raw_volunteers.shape)
raw_volunteers.head()


# #### Opportunities All Time

# In[5]:

raw_oppsalltime = pd.read_csv('datadrop_20150325/cleaned_csv/opportunites_all_time.csv'
                             ,parse_dates=[9,10,12,13])
raw_oppsalltime.rename(columns=lambda x: snakeycase(x), inplace=True)
print(raw_oppsalltime.shape)
raw_oppsalltime.head()


# #### Opportunities Applied For

# In[6]:

raw_oppsappliedfor = pd.read_csv('datadrop_20150325/cleaned_csv/opportunities_applied_for.csv')
raw_oppsappliedfor.rename(columns=lambda x: snakeycase(x), inplace=True)
print(raw_oppsappliedfor.shape)
raw_oppsappliedfor.head()


# #### Placement Info

# In[7]:

raw_placements = pd.read_csv('datadrop_20150325/cleaned_csv/placements.csv')
raw_placements.rename(columns=lambda x: snakeycase(x), inplace=True)
print(raw_placements.shape)
raw_placements.head()


# ---

# # Quick Tidy and Merge

# In[8]:

df_vol = raw_volunteers.copy()
df_vol.set_index('volunteer_id', inplace=True)
print(df_vol.shape)
df_vol.head(2)


# In[9]:

df_oppsapfr = raw_oppsappliedfor.copy()
df_oppsapfr.set_index('volunteer_opportunity_applied_for_id', inplace=True)
print(df_oppsapfr.shape)
df_oppsapfr.head(2)


# In[10]:

df_oppsaltm = raw_oppsalltime.copy()
df_oppsaltm.set_index('volunteer_opportunity_id', inplace=True)
print(df_oppsaltm.shape)
df_oppsaltm.head(2)


# In[11]:

df_plc = raw_placements.copy()
# df_plc.rename(columns={'volunteer_opportunity_record_id':'volunteer_opportunity_id'}
#               ,inplace=True)
df_plc.set_index('volunteer_opportunity_record_id', inplace=True)
print(df_plc.shape)
df_plc.head(2)


# ## Merge

# ### Merge volunteers with the opportunities they applied to

# In[12]:

df_volsmadeapps = pd.merge(df_vol, df_oppsapfr, how='outer'
                           , left_index=True, right_on='volunteer_volunteer_id')
df_volsmadeapps = df_volsmadeapps.reset_index().set_index('volunteer_volunteer_id')
print(df_volsmadeapps.shape)
df_volsmadeapps.head(2)


# ### Merge opportunities alltime with those that got placed

# In[13]:

df_oppsalltimeplaced = pd.merge(df_oppsaltm, df_plc, how='left', left_index=True, right_index=True)
df_oppsalltimeplaced.index.name = df_oppsaltm.index.name
print(df_oppsalltimeplaced.shape)
df_oppsalltimeplaced.head(2)


# # Write to DB

# In[14]:

cnx = sqlite3.connect('single_database.db')


# ##### The clean separate tables

# In[15]:

df_vol.to_sql('df_vol', con=cnx, if_exists='replace')
df_oppsaltm.to_sql('df_oppsaltm', con=cnx, if_exists='replace')
df_oppsapfr.to_sql('df_oppsapfr', con=cnx, if_exists='replace')
df_plc.to_sql('df_plc', con=cnx, if_exists='replace')


# ##### The merged tables

# In[16]:

df_volsmadeapps.to_sql('df_volsmadeapps', con=cnx, if_exists='replace')
df_oppsalltimeplaced.to_sql('df_oppsalltimeplaced', con=cnx, if_exists='replace')


# ---
# 
# DataKind Dublin 2005
