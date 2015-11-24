import sqlite3 as lite
import pandas as pd

# Connect to the database. The `connect()` method returns a connection object.
con = lite.connect('getting_started.db')

# Take user parameters
month = raw_input("Please enter the name of the month to analyze: ")

# Check for and remove existing tables before executing.
with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS cities;")
    cur.execute("DROP TABLE IF EXISTS weather;")
    cur.execute("CREATE TABLE cities(name text, state text);")
    cur.execute("""
        CREATE TABLE weather (
            city text, year integer, 
            warm_month text, cold_month text, 
            average_high integer);""")

# Insert data into the two tables
cities = ((
    'New York City', 'NY'), 
    ('Boston', 'MA'), 
    ('Chicago', 'IL'), 
    ('Miami', 'FL'), 
    ('Dallas', 'TX'), 
    ('Seattle', 'WA'), 
    ('Portland', 'OR'), 
    ('San Francisco', 'CA'), 
    ('Los Angeles', 'CA'))

weather = (
    ('New York City', 2013, 'July', 'January', 62), 
    ('Boston', 2013, 'July', 'January', 59), 
    ('Chicago', 2013, 'July', 'January', 59), 
    ('Miami', 2013, 'August', 'January', 84), 
    ('Dallas', 2013, 'July', 'January', 77), 
    ('Seattle', 2013, 'July', 'January', 61), 
    ('Portland', 2013, 'July', 'December', 63), 
    ('San Francisco', 2013, 'September', 'December', 64), 
    ('Los Angeles', 2013, 'September', 'December', 75))

# Inserting rows by passing tuples to `execute()`
with con:
    cur = con.cursor()
    cur.executemany("INSERT INTO cities VALUES(?,?)", cities)
    cur.executemany("INSERT INTO weather VALUES(?,?,?,?,?)", weather)

# Join the data together and load into a pandas dataframe
with con:
    cur = con.cursor()
    cur.execute("""
        SELECT name, state, average_high 
        FROM cities 
        INNER JOIN weather 
        ON name = city 
        WHERE warm_month=?""", (month,))

rows = cur.fetchall()
df = pd.DataFrame(rows)

# Print out the resulting city and state in a full sentence
print "The cities that are warmest in {0} are: ".format(month)

city_list = []
for i in df.index:
    city_list.append(df.ix[i, 0] + ',' + df.ix[i, 1])

print ", ".join(city_list)
