''' DAEN 690 - Capstone Project, Summer 2022
    Team Launch Insight
    Bray, Brensike, Rego, Williamson, Woods

    Use this code to get the unique NOTAM count from results csv file
'''

import csv
import pandas as pd
import numpy as np

df_results = pd.read_csv('data/LAUNCHES_REC_ID_DISCOVERED.csv')

print(df_results['DISCOVERED'])

count = 0

print(df_results['DISCOVERED'])

new_set = []
for index, row in df_results.iterrows():
	count += row['DISCOVERED'].count(",") + 1
	r = row['DISCOVERED'].replace(" ","")
	r = r.replace("[","")
	r = r.replace("]","")

	new_set.extend(r.split(','))

print(count)

new_set = set(new_set)
print(new_set)
print(len(new_set))
