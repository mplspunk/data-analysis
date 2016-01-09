from bs4 import BeautifulSoup
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import statsmodels.api as sm


# Import UN webpage for scraping
url = "http://web.archive.org/web/20110514112442/\
http://unstats.un.org/unsd/demographic/products/socind/education.htm"

# Get the content
r = requests.get(url)

# Pass the results to Beautiful Soup
soup = BeautifulSoup(r.content)

# Check for desired table(s)
for row in soup('table'):
    print(row)

# Run script in a wrapper
if r.ok:
    # Put content in the parsing structure
    soup = BeautifulSoup(r.content)

    # Find all table rows within the appropriate table
    A = soup('table')[6]('table')[2].findAll('tr')
    A = A[4:-1]
	
	# Define and find each record, add to dataRows
    dataRows = []
    for row in A:
        record = [x.string for x in row.findAll('td', {'align': 'right'})]
        record.insert(0, row.findAll('td')[0].string)
        dataRows.append(record)

	# Create column names for dataRows
    colNames = ['Country', 'Year', 'Total', 'Men', 'Women']

	# Read into a pandas dataframe
    dfUNData = pd.DataFrame(dataRows, columns=colNames)

	# Write data to CSV file
    dfUNData.to_csv('un_data.csv', encoding='utf-8', index=False)
else:
    print r.status_code

# Examine a histogram of male education
plt.figure()
(dfUNData['Men'].astype(int)).hist()
plt.title('Male School Life Expentancy')
plt.xlabel('Age')
plt.ylabel('Count')
plt.show()

# Examine a histogram of female education
plt.close()
plt.figure()
(dfUNData['Women'].astype(int)).hist()
plt.title('Women School Life Expentancy')
plt.xlabel('Age')
plt.ylabel('Count')
plt.show()

# Print summary statistics by gender
print "The mean age for men is: "
print (dfUNData['Men'].astype(int)).mean()
print "\n"

print "The median age for men is: "
print (dfUNData['Men'].astype(int)).median()
print "\n"

print "The mean age for women is: "
print (dfUNData['Women'].astype(int)).mean()
print "\n"

print "The median age for women is: "
print (dfUNData['Women'].astype(int)).median()
print "\n"

# The UN Education Dataset
# The mean and median school life expectancy for women is greater than the mean
# and median school life expectancy of men (i.e., girls appear to stay in
# school longer than boys). This seems somewhat counterintuitive to stories 
# about gender and education in developing countries, where it is routine for
# families to invest more in the education of sons than daughters. However,
# this is data across 182 countries, including many countries like the U.S., 
# where women stay in school longer than men. Although some countries, such 
# as Afghanistan or Chad, clearly show educational bias for male children when
# looking at the country-level data in this dataset.

# Import World Bank data on GDP
data = pd.read_csv('ny.gdp.mktp.cd_indicator_en_csv_v2.csv', skiprows=3)
data.head()

# Read into a pandas dataframe
dfGDPData = pd.DataFrame(data, columns=['Country Code', '1999', '2000', '2001', 
    '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010'])

# Remove scientific notation on GDP figures
pd.set_option('display.float_format', lambda x: '%.3f' % x)
dfGDPData.head()

# Remove rows/countries that are completely missing data
dfGDPData = dfGDPData.dropna(thresh=11)

# Eliminate the few remaining NaN values
dfGDPData = dfGDPData.dropna()

# Since there is variation in the country names between the UN Education 
# Dataset and the World Bank GDP Dataset, we will use the country code to 
# merge the datasets together. In order to do this, we will need to scrape 
# a third dataframe that has UN country codes.

# Import UN code page
url = "http://unstats.un.org/unsd/methods/m49/m49alpha.htm"

# Get the content
r = requests.get(url)

# Pass the results to Beautiful Soup
soup = BeautifulSoup(r.content)

# Run script in a wrapper
if r.ok:
    # Put content in the parsing structure
    soup = BeautifulSoup(r.content)

   # Find all table rows within the appropriate table
    A = soup('table')[3]('table')[2].findAll('tr')
    A = A[1:]

    # Define and find each record, add to dataRows
    dataRows = []
    for row in A:
        record = [x.string for x in row.findAll('p')]
        dataRows.append(record)

    # Create column names for dataRows
    colNames = ['NumericalCode', 'Country', 'ISOCode']

    # Read into a pandas dataframe
    dfUNCodes = pd.DataFrame(dataRows, columns=colNames)

    # Clean up the dataframe
    dfUNCodes.dropna(inplace=True)
    dfUNCodes['NumericalCode'] = dfUNCodes.apply(
        lambda x: x['NumericalCode'].rstrip(), axis=1)
    dfUNCodes['Country'] = dfUNCodes.apply(
        lambda x: x['Country'].rstrip(), axis=1)
    dfUNCodes['ISOCode'] = dfUNCodes.apply(
        lambda x: x['ISOCode'].lstrip(), axis=1)
    dfUNCodes['ISOCode'] = dfUNCodes.apply(
        lambda x: x['ISOCode'].rstrip(), axis=1)

    # Write data to CSV file
    dfUNCodes.to_csv('un_codes.csv', encoding='utf-8', index=False)
else:
    print r.status_code

# Merge UN education dataframe and UN country codes dataframe on country name
dfUN_merged = pd.merge(dfUNData, dfUNCodes, on='Country', how='inner')

# Rename columns so the dataframe columns align
dfGDPData.columns = dfGDPData.columns.str.replace('Country Code', 'ISOCode')

# Merge updated UN data with the World Bank dataframe on the country code
dfAll_merged = pd.merge(dfUN_merged, dfGDPData, on='ISOCode', how='inner')

# Verify data types are compatible for running regression
dfAll_merged.info()
# <class 'pandas.core.frame.DataFrame'>
# Int64Index: 162 entries, 0 to 161
# Data columns (total 19 columns):
# Country          162 non-null object
# Year             162 non-null object
# Total            162 non-null object
# Men              162 non-null object
# Women            162 non-null object
# NumericalCode    162 non-null object
# ISOCode          162 non-null object
# 1999             162 non-null float64
# 2000             162 non-null float64
# 2001             162 non-null float64
# 2002             162 non-null float64
# 2003             162 non-null float64
# 2004             162 non-null float64
# 2005             162 non-null float64
# 2006             162 non-null float64
# 2007             162 non-null float64
# 2008             162 non-null float64
# 2009             162 non-null float64
# 2010             162 non-null float64
# dtypes: float64(12), object(7)
# memory usage: 25.3+ KB

# Convert 'Men', 'Women', and 'Total' to floats
dfAll_merged[['Men', 'Women', 'Total']] = dfAll_merged[['Men', 'Women', 'Total']].astype(float)

# Do a log-transform of the GDP to get a scale that can be used to compare
years = (['1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', 
        '2007', '2008', '2009', '2010'])

for year in years:
    dfAll_merged[year + 'L'] = dfAll_merged[year].apply(lambda x: np.log(x))


# Create a linear model with log GDP (dependent) and education (independent)
loggdp = dfAll_merged[['1999L', '2000L', '2001L', '2002L', '2003L', '2004L', 
        '2005L', '2006L', '2007L', '2008L', '2009L', '2010L']].mean(axis=1)
education = dfAll_merged['Total']

y = np.matrix(loggdp).transpose()
x = np.matrix(education).transpose()

X = sm.add_constant(x)
model = sm.OLS(y,X)
results = model.fit()
print results.summary()


