import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats

# loading the dataset
loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

# remove null value rows
loansData.dropna(inplace=True)

# generate a box plot of the loan amounts requested
loansData.boxplot(column='Amount.Requested')
plt.savefig("boxplot_loans.png")

# generate a histogram of the loan amounts
loansData.hist(column='Amount.Requested')
plt.savefig("histogram_loans.png")

# generate a QQ plot of the loan amounts to test distribution
plt.figure()
graph = stats.probplot(loansData['Amount.Requested'], dist="norm", plot=plt)
plt.savefig("qqplot_loans.png")

print "The 'Amount Funded by Investors' in the loan data is right skewed. The average is about $10,000 and the IQR (middle 50%) is between $6,000 and $16,000. The histogram shows that some observations were $0, indicating that some individuals requested money, but did not receive funding."
print "\n"
print "The 'Amount Requested' in the loan data is also right skewed. The average is about $10,000 and the IQR (middle 50%) is between $6,000 and $17,000 (slightly higher). There were no observations at $0, which intuitively makes sense as no one would request $0 from investors."
print "\n"
print "The QQ plots show that neither set of observations is normally distributed, because the graph curves upward and does not stay close to the line."