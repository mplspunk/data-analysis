import requests
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import pandas as pd


r = requests.get('http://www.citibikenyc.com/stations/json')

# Get a list of the keys
r.json().keys()
# [u'executionTime', u'stationBeanList']

# Examine the format of both keys
r.json()['executionTime']
r.json()['stationBeanList']

# Use 'length' to get the # of bike docks
len(r.json()['stationBeanList'])
# 511

# Run a loop to test that you have all the fields
key_list = []  # unique list of keys for each station listing
for station in r.json()['stationBeanList']:
    for k in station.keys():
        if k not in key_list:
            key_list.append(k)

print key_list
# [u'availableDocks',
# u'totalDocks',
# u'city',
# u'altitude',
# u'stAddress2',
# u'longitude',
# u'lastCommunicationTime',
# u'postalCode',
# u'statusValue',
# u'testStation',
# u'stAddress1',
# u'stationName',
# u'landMark',
# u'latitude',
# u'statusKey',
# u'availableBikes',
# u'id',
# u'location']

# Convert the data into a pandas data frame
df = json_normalize(r.json()['stationBeanList'])

print df.info()
# <class 'pandas.core.frame.DataFrame'>
# Int64Index: 511 entries, 0 to 510
# Data columns (total 18 columns):
# altitude                 511 non-null object
# availableBikes           511 non-null int64
# availableDocks           511 non-null int64
# city                     511 non-null object
# id                       511 non-null int64
# landMark                 511 non-null object
# lastCommunicationTime    511 non-null object
# latitude                 511 non-null float64
# location                 511 non-null object
# longitude                511 non-null float64
# postalCode               511 non-null object
# stAddress1               511 non-null object
# stAddress2               511 non-null object
# stationName              511 non-null object
# statusKey                511 non-null int64
# statusValue              511 non-null object
# testStation              511 non-null bool
# totalDocks               511 non-null int64
# dtypes: bool(1), float64(2), int64(5), object(10)
# memory usage: 72.4+ KB

print df.head()

# Look at the range of available bikes
df['availableBikes'].hist()
plt.show()

# Look at the range of total docks
df['totalDocks'].hist()
plt.show()

# The distribution of available bikes is right-skewed, with values from 
# 0 - 60. Most of the distribution is between 0 and 15. The distribution 
# of total docks is approximately normal, with values from 0 - ~66.

print "\n"

test = df[df['testStation'] == True]
print "There are {} test stations in the dataset.".format(len(test))
print "\n"

service = df[df['statusValue'] == 'In Service']
print "There are {} stations that are in service.".format(len(service))
print "\n"

no_service = df[df['statusValue'] == 'Not In Service']
print "There are {} stations that are not in service.".format(len(no_service))
print "\n"

print "The mean number of docks is {}.".format(df['totalDocks'].mean())
print "\n"

print "The median number of docks is {}.".format(df['totalDocks'].median())
print "\n"

service.median()
# There is no difference in median for total docks and in service docks
