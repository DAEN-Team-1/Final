import time
import pandas as pd
import re
# Imports
import csv
import pandas as pd
import numpy as np
from datetime import datetime
pd.options.display.max_colwidth = 100000

import seaborn as sns
import matplotlib.pyplot as plt
import plotly as px


start = time.time()

df_notam = pd.read_csv('data/notams.csv', on_bad_lines='skip', encoding='utf-16', low_memory=False)
end = time.time()
print("Read csv with pandas: ", (end-start),"sec")

print(df_notam.shape)

print(df_notam.info())

print(df_notam.head(5))
# Make POSSIBLE_START_DATE, POSSIBLE_END_DATE, ISSUE_DATE, and CANCELED_DATE datetime format
df_notam['POSSIBLE_START_DATE'] = pd.to_datetime(df_notam['POSSIBLE_START_DATE'], errors = 'coerce', format = '%Y/%m/%d %H:%M:%S')
df_notam['POSSIBLE_END_DATE'] = pd.to_datetime(df_notam['POSSIBLE_END_DATE'], errors = 'coerce', format = '%Y/%m/%d %H:%M:%S')
df_notam['ISSUE_DATE'] = pd.to_datetime(df_notam['ISSUE_DATE'], errors = 'coerce', format = '%Y/%m/%d %H:%M:%S')
df_notam['CANCELED_DATE'] = pd.to_datetime(df_notam['CANCELED_DATE'], errors = 'coerce', format = '%Y/%m/%d %H:%M:%S')

# Replace missing POSSIBLE_START_DATE with CANCELED_DATE and vise versa
df_notam.loc[df_notam['CANCELED_DATE'].isna(), 'CANCELED_DATE'] = df_notam.loc[df_notam['CANCELED_DATE'].isna(), 'POSSIBLE_END_DATE']
df_notam.loc[df_notam['POSSIBLE_END_DATE'].isna(), 'POSSIBLE_END_DATE'] = df_notam.loc[df_notam['POSSIBLE_END_DATE'].isna(), 'CANCELED_DATE']

# Drop NOTAMs without POSSIBLE_END_DATE and POSSIBLE_START_DATE
df_notam = df_notam.dropna( how='all', subset=['POSSIBLE_END_DATE', 'POSSIBLE_START_DATE'])

print(df_notam.shape)

## NOTAM by year
plot = sns.histplot(df_notam['POSSIBLE_START_DATE'], bins=8)

print(plot)