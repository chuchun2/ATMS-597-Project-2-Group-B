# -*- coding: utf-8 -*-
"""ATMS597_Project2_GroupB.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yiVAR4tb9kZ4w1cskozzF47-TBuYidrE
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

import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

#add the access token you got from NOAA
Token = 'szwPaVkJgTghjaaDSujrPMpbRilnUVva'

# Academy 2 NE, SD Airport station
station_id = 'GHCND:USC00390043'

dates_temp = []
temps = []

start_date = '1899-01-01'
end_date = '2020-01-01'

start_year = int(start_date[0:4])
end_year = int(end_date[0:4])

for year in range(start_year, end_year):
    year = str(year)
    print('working on year '+year)
    
    #make the api call
    r = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMAX&limit=1000&stationid='+station_id+'&startdate='+year+'-01-01&&enddate='+year+'-12-31', headers={'token':Token})
    #load the api response as a json
    #print(r.text)
    d = json.loads(r.text)
    #get all items in the response which are average temperature readings
    max_temps = [item for item in d['results'] if item['datatype']=='TMAX']
    #get the date field from all average temperature readings
    dates_temp += [item['date'] for item in max_temps]
    #get the actual average temperature from all average temperature readings
    temps += [item['value'] for item in max_temps]

df_temp = pd.DataFrame()

#populate date and average temperature fields (cast string date to datetime and convert temperature from tenths of Celsius to Fahrenheit)
df_temp['date'] = [datetime.strptime(d, "%Y-%m-%dT%H:%M:%S") for d in dates_temp]
df_temp['avgTemp'] = [float(v)/10.0*1.8 + 32 for v in temps]

df_temp = df_temp.dropna()

df_temp

plt.figure(figsize=(30,10))
plt.plot(df_temp.date,df_temp.maxTemp,'.')
plt.show()

df_temp = df_temp.set_index(['date'])
df_temp

df_temp_mon = df_temp.resample('Y').max()
df_temp_mon

df_temp_mon['Normalized'] = (df_temp_mon.avgTemp-df_temp_mon.avgTemp.min())/(df_temp_mon.avgTemp.max()-df_temp_mon.avgTemp.min())

df_temp_mon

temps_normed = df_temp_mon.Normalized.values

years = np.arange(1899,2020)
years

elements = len(df_temp_mon)

x_lbls = np.arange(elements)
y_vals = temps_normed / (len(df_temp_mon) - 1)
y_vals2 = np.full(elements, 1)
bar_wd  = 1

my_cmap = plt.cm.coolwarm #choose colormap to use for bars
norm = Normalize(vmin=0, vmax=1.)

def colorval(num):
    return my_cmap(norm(num))

fig=plt.figure(figsize=(22,5))
#plt.axis('off')
plt.axis('tight')

#Plot warming stripes. Change y_vals2 to y_vals to plot stripes under the line only.
plt.bar(x_lbls, y_vals2, color = list(map(colorval, temps_normed)), width=1.0, edgecolor = "none")
#plt.colorbar()
plt.plot(x_lbls,temps_normed,'k.-',ms=10.)
#Plot temperature timeseries. Comment out to only plot stripes
#plt.plot((x_lbls + 0.5), y_vals - 0.002, color='black', linewidth=2)

plt.xticks( x_lbls + bar_wd, x_lbls)

plt.ylim(0, 1)
fig.subplots_adjust(bottom = 0)
fig.subplots_adjust(top = 1)
fig.subplots_adjust(right = 1)
fig.subplots_adjust(left = 0)
plt.show()
