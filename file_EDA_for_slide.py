import time
import pandas as pd
import re
import csv


start = time.time()
launches = pd.read_csv('launches.csv')
notam = pd.read_csv('notams.csv', on_bad_lines='skip', encoding='utf-16', low_memory=False)
polygon = pd.read_csv('polygons.csv')
spaceports = pd.read_csv('spaceports.csv')
vertices = pd.read_csv('vertices.csv')
end = time.time()
print("Read csv with pandas: ", (end-start),"sec")

print(launches.shape)
print(notam.shape)
print(polygon.shape)
print(spaceports.shape)
print(vertices.shape)

print(launches.info())
print(notam.info())
print(polygon.info())
print(spaceports.info())
print(vertices.info())

print(launches.head(5))
print(notam.head(5))
print(polygon.head(5))
print(spaceports.head(5))
print(vertices.head(5))

# print(df1.dtypes)
# print(df4.dtypes)