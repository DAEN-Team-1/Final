''' DAEN 690 - Capstone Project, Summer 2022
    Team Launch Insight
    Bray, Brensike, Rego, Williamson, Woods
'''

### Load modules ###
import sqlite3
import csv
import math
# from traceback import format_exc
# import time
from datetime import datetime
# import copy
# import itertools
import pandas as pd
import numpy as np
import re

################################################################################
### Import the datasets and Create the indexes for model development ###

launches = pd.read_csv('data/launches_20201027.csv')
notams = pd.read_csv('data/notam_20201027_commas_quotes.csv', on_bad_lines='skip',\
    encoding='utf-16', low_memory=False)

print(notams.shape)

# Convert date/time fields into string datetime format 
launches['LAUNCH_DATE'] = pd.to_datetime(launches['LAUNCH_DATE'], errors = 'coerce').dt.strftime('%Y%m%d%H%M%S')
notams['POSSIBLE_START_DATE'] = pd.to_datetime(notams['POSSIBLE_START_DATE'], errors = 'coerce').dt.strftime('%Y%m%d%H%M%S')
notams['POSSIBLE_END_DATE'] = pd.to_datetime(notams['POSSIBLE_END_DATE'], errors = 'coerce').dt.strftime('%Y%m%d%H%M%S')
# notams['ISSUE_DATE'] = pd.to_datetime(notams['ISSUE_DATE'], errors = 'coerce').dt.strftime('%Y%m%d%H%M%S')
# notams['CANCELED_DATE'] = pd.to_datetime(notams['CANCELED_DATE'], errors = 'coerce').dt.strftime('%Y%m%d%H%M%S')

## Convert dates to numeric
launches['LAUNCH_DATE'] = pd.to_numeric(launches['LAUNCH_DATE'])
notams['POSSIBLE_START_DATE'] = pd.to_numeric(notams['POSSIBLE_START_DATE'])
notams['POSSIBLE_END_DATE'] = pd.to_numeric(notams['POSSIBLE_END_DATE'])

# print(notams.dtypes)
# print(launches.dtypes)

## Set of all launches
i_launch = (set(launches['LAUNCHES_REC_ID']))
# print(i_launch)
## Pick launches to test by reducing the full set to the following...
i_launch = [1,10,50,100,150,200,250,300,350,400,450,500]

## Make the dataset more useable
listNotamDates = pd.DataFrame(notams, columns=['NOTAM_REC_ID','POSSIBLE_START_DATE','POSSIBLE_END_DATE'])
listLaunchDates = pd.DataFrame(launches, columns=['LAUNCHES_REC_ID','LAUNCH_DATE'])

## Convert dataframes to lists because I haven't figured out how to do this with Pandas yet
listNotams = listNotamDates.to_numpy().tolist()
listLaunches = listLaunchDates.to_numpy().tolist()

# print(type(listLaunches))
# print(listNotams)
# print(type(listLaunches))

for i in i_launch:
    j = i-1  ## index value is one less than i
    dtg_check = ([el for el in listNotams if el[1]<=listLaunches[j][1]<=el[2]])
    print(f'LAUNCH_REC_ID {i} had {len(dtg_check)} active NOTAMs at launch time {listLaunches[j][1]}')
    # print(dtg_check)
