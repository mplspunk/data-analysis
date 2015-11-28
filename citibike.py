import requests
from pandas.io.json import json_normalize
import pandas as pd
import sqlite3 as lite
import time
from dateutil.parser import parse
import collections
import matplotlib.pyplot as plt
import datetime


r = requests.get('http://www.citibikenyc.com/stations/json')

# Convert the data into a pandas data frame
df = json_normalize(r.json()['stationBeanList'])

con = lite.connect('citi_bike.db')
cur = con.cursor()

# Create a SQL table to store the reference data
with con:
    cur.execute('CREATE TABLE citibike_reference (id INT PRIMARY KEY, ' 
    	'totalDocks INT, city TEXT, altitude INT, stAddress2 TEXT, '
    	'longitude NUMERIC, postalCode TEXT, testStation TEXT, '
    	'stAddress1 TEXT, stationName TEXT, landMark TEXT, latitude NUMERIC, '
    	'location TEXT )')

# Insert reference data in the SQL table
sql = '''INSERT INTO citibike_reference (id, totalDocks, city, altitude, 
	stAddress2, longitude, postalCode, testStation, stAddress1, stationName, 
	landMark, latitude, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)'''

# For loop to populate values in the database
with con:
    for station in r.json()['stationBeanList']:
        # id, totalDocks, city, altitude, stAddress2, longitude, postalCode, 
        # testStation, stAddress1, stationName, landMark, latitude, location)
        cur.execute(sql,(
        	station['id'],
        	station['totalDocks'],
        	station['city'],
        	station['altitude'],
        	station['stAddress2'],
        	station['longitude'],
        	station['postalCode'],
        	station['testStation'],
        	station['stAddress1'],
        	station['stationName'],
        	station['landMark'],
        	station['latitude'],
        	station['location'])
        )

# Extract the column from the dataframe and put into a list
station_ids = df['id'].tolist() 

# Add the '_' to the station name and also add the data type for SQLite
station_ids = ['_' + str(x) + ' INT' for x in station_ids]

# Create the table - concatentate the string and join all the station ids 
# (now with '_' and 'INT' added)
with con:
    cur.execute('CREATE TABLE available_bikes ( execution_time INT, ' +  
    	', '.join(station_ids) + ');')

# Take the string and parse it into a Python datetime object
exec_time = parse(r.json()['executionTime'])

# Create an entry for the execution time by inserting it into the database
with con:
    cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime('%s'),))

# Create defaultdict to store available bikes by station
id_bikes = collections.defaultdict(int)

# Loop through the stations in the station list
for station in r.json()['stationBeanList']:
    id_bikes[station['id']] = station['availableBikes']

# Iterate through the defaultdict to update the values in the database
with con:
    for k, v in id_bikes.iteritems():
        cur.execute("UPDATE available_bikes SET _" + 
        	str(k) + " = " + 
        	str(v) + " WHERE execution_time = " + 
        	exec_time.strftime('%s') + ";")

# Update available bikes iteratively every minute for an hour
for i in range(60):
    exec_time = parse(r.json()['executionTime']).strftime("%s")

    cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time,))

    for station in r.json()['stationBeanList']:
        cur.execute("UPDATE available_bikes SET _%d = %d WHERE execution_time = %s" % (station['id'], station['availableBikes'], exec_time))
    con.commit()

    time.sleep(60)

con.close()


# Set up access to the SQL database
con = lite.connect('citi_bike.db')
cur = con.cursor()

# Load the data into a pandas dataframe
df = pd.read_sql_query("SELECT * FROM available_bikes ORDER BY execution_time",con,index_col='execution_time')

# Process each column and calculate the change each minute
hour_change = collections.defaultdict(int)
for col in df.columns:
    station_vals = df[col].tolist()
    station_id = col[1:]  # trim the "_"
    station_change = 0
    for k,v in enumerate(station_vals):
        if k < len(station_vals) - 1:
            station_change += abs(station_vals[k] - station_vals[k+1])
    hour_change[int(station_id)] = station_change  # convert the station id back to integer

# Find the key with the greatest value
def keywithmaxval(d):
    return max(d, key=lambda k: d[k])

# Assign the max key to max_station
max_station = keywithmaxval(hour_change)

# Query sqlite for reference information
cur.execute("SELECT id, stationname, latitude, longitude FROM citibike_reference WHERE id = ?", (max_station,))
data = cur.fetchone()
print("The most active station is station id %s at %s latitude: %s longitude: %s " % data)
print("With %d bicycles coming and going in the hour between %s and %s" % (
    hour_change[max_station],
    datetime.datetime.fromtimestamp(int(df.index[0])).strftime('%Y-%m-%dT%H:%M:%S'),
    datetime.datetime.fromtimestamp(int(df.index[-1])).strftime('%Y-%m-%dT%H:%M:%S'),
))

# Visually inspect to ensure the results print correctly
plt.bar(hour_change.keys(), hour_change.values())
plt.show()
