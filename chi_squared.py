import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import collections


# Load the reduced version of the Lending Club Dataset
loansData = pd.read_csv(
	'https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

# Drop null rows
loansData.dropna(inplace=True)

freq = collections.Counter(loansData['Open.CREDIT.Lines'])

# Visually examine the data
plt.figure()
plt.bar(freq.keys(), freq.values(), width=1)
plt.show()

# Perform the chi-squared test and print the result
chi, p = stats.chisquare(freq.values())
print (p, chi)
print "The p-value is {} and the chi-squared test result is {}.".format(p, chi)
