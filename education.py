from bs4 import BeautifulSoup
import csv
import matplotlib.pyplot as plt
import pandas as pd
import requests


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




# Convert to log and perform a regression on education (y/dependant variable)
# and relationship to country's GDP (x/independent variable).
# https://github.com/FrankRuns/Thinkful/blob/master/Unit3/EducationAndWealth/education.py









