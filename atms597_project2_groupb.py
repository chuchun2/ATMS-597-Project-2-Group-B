# -*- coding: utf-8 -*-
"""ATMS597_Project2_GroupB.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13NGsTHGeGN8HBkUxM3lWcmp3eVrueUv9
"""

#needed to make web requests
import requests

#store the data we get as a dataframe
import pandas as pd

#convert the response as a structured json
import json

#mathematical operations on lists
import numpy as np

#parse the datetimes we get from NOAA
from datetime import datetime

#import time for sleeping
import time

#add the access token you got from NOAA
Token = 'XTuPxqfWBGOmcsWJFcfFhDxqITHYTGOJ'

#Academy 2 NE, SD Airport station
station_id = 'GHCND:USC00390043'

import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

start_date = '1899-01-01'
end_date = '2020-01-01'

start_year = int(start_date[0:4])
end_year = int(end_date[0:4])

#initialize lists to store data
dates_mintemp = []
dates_maxtemp = []
min_temps = []
max_temps = []
prcp = []

#for each year from 1899-2019 ...
for year in range(start_year, end_year):
    year = str(year)
    print('working on year '+year)
    
    #make the api call
    r = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMIN&datatypeid=TMAX&limit=1000&stationid='+station_id+'&startdate='+year+'-01-01&enddate='+year+'-12-31', headers={'token':Token})
    #load the api response as a json
    #print(r.text)
    d = json.loads(r.text)    

    #get all items in the response which are max&min temperature readings
    maxtemps = [item for item in d['results'] if item['datatype']=='TMAX']
    mintemps = [item for item in d['results'] if item['datatype']=='TMIN']
    #get the date field from all average temperature readings
    dates_maxtemp += [item['date'] for item in maxtemps]
    dates_mintemp += [item['date'] for item in mintemps]
    #get the actual average temperature from all average temperature readings
    max_temps += [item['value'] for item in maxtemps]
    min_temps += [item['value'] for item in mintemps]
    time.sleep(0.2) # API max 5 requests per second

#initialize dataframe
df_temp_min = pd.DataFrame()
df_temp_max = pd.DataFrame()
df_temp_avg = pd.DataFrame()

#populate date and min and max temperature fields (convert string date to datetime)
df_temp_min['date'] = [datetime.strptime(d, "%Y-%m-%dT%H:%M:%S") for d in dates_mintemp]
df_temp_min['minTemp'] = [float(v)/10.0 * 1.8 + 32 for v in min_temps]  # Celsius to Fahrenheit

df_temp_max['date'] = [datetime.strptime(d, "%Y-%m-%dT%H:%M:%S") for d in dates_maxtemp]
df_temp_max['maxTemp'] = [float(v)/10.0 * 1.8 + 32 for v in max_temps]  # Celsius to Fahrenheit

df_temp_avg['date'] = [datetime.strptime(d, "%Y-%m-%dT%H:%M:%S") for d in dates_maxtemp]
df_temp_avg['avgTemp'] = (df_temp_min['minTemp'] + df_temp_max['maxTemp'])/2

df_temp_avg = df_temp_avg.dropna()  # Remove missing values
df_temp_avg

plt.figure(figsize=(30,10))
plt.plot(df_temp_avg.date,df_temp_avg.avgTemp,'.')
plt.show()

df_temp_avg = df_temp_avg.set_index(['date'])
df_temp_avg

ltm = df_temp_avg.avgTemp.mean()
 ltm

#ask users what frequency do they want
freq = input("Enter annual, monthly, or weekly: ")

if freq == 'annual':
  df_temp_freq = df_temp_avg.resample('Y').mean()
  t_range = pd.date_range(start_date, end_date, freq='5Y')
  x_ticks_lbs = t_range.strftime('%Y').astype(int)
  fig_wide = 22
elif freq == 'monthly':
  df_temp_freq = df_temp_avg.resample('M').mean()
  t_range = pd.date_range(start_date, end_date, freq='60M')
  x_ticks_lbs = t_range.strftime('%Y%m').astype(int)
  fig_wide = 22*12
elif freq == 'weekly':
  df_temp_freq = df_temp_avg.resample('W').mean()
  t_range = pd.date_range(start_date, end_date, freq='261W')  
  x_ticks_lbs = t_range.strftime('%Y%m').astype(int)
  fig_wide = 22*12
else:
  print('Only support annual, monthly, or weekly.')

df_temp_freq

df_temp_freq['Normalized'] = (df_temp_freq.avgTemp - ltm)/df_temp_freq.avgTemp.std()

df_temp_freq.isnull().sum()  # Check if there are missing values

df_temp_freq = df_temp_freq.dropna()  # Remove missing values
df_temp_freq

temps_normed = df_temp_freq.Normalized.values
temps_normed

elements = len(df_temp_freq)

x_lbls = np.arange(elements)
y_vals = np.full(elements, 300)  # Return a new array of given shape and type, filled with fill_value.

my_cmap = plt.cm.coolwarm #choose colormap to use for bars
norm = Normalize(vmin=0, vmax=1.)

fig=plt.figure(figsize=(fig_wide,5))
plt.axis('tight')

#Plot warming stripes.
plt.bar(x_lbls, y_vals, color = my_cmap(norm(temps_normed)), width=1.0, bottom=-100, edgecolor = "none")

#Plot temperature timeseries. Comment out to only plot stripes
plt.plot(x_lbls,df_temp_freq.avgTemp,'k.-',ms=10.)

#Setting for the xticks
if freq == 'annual':
  x_ticks = np.arange(elements, step=5)
elif freq == 'monthly':
  x_ticks = np.arange(elements, step=60)
elif freq == 'weekly':
  x_ticks = np.arange(elements, step=261)
  
plt.xticks(x_ticks,x_ticks_lbs)
plt.ylim(min(df_temp_freq.avgTemp)-5, max(df_temp_freq.avgTemp)+5)
plt.show()

plt.tight_layout()

