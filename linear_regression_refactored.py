import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm


loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

loansData['Interest.Rate'][0:5]
# 81174     8.90%
# 99592    12.12%
# 80059    21.98%
# 15825     9.99%
# 33182    11.71%
# Name: Interest.Rate, dtype: object

# Remove the '%' symbols from the Interest.Rate column.
# scrubInterestRate = loansData['Interest.Rate'].map(lambda x: round(float(x.rstrip('%')) / 100, 4))
scrubInterestRate = [round(float(x.rstrip('%'))/100, 4) for x in loansData['Interest.Rate']]

# Verify that the unwanted characters were stripped from the column.
scrubInterestRate[0:5]
# [0.089, 0.1212, 0.2198, 0.0999, 0.1171]

# Apply changes to the original data set.
loansData['Interest.Rate'] = scrubInterestRate

# Continue with cleaning of other data columns.
loansData['Loan.Length'][0:5]
# 81174    36 months
# 99592    36 months
# 80059    60 months
# 15825    36 months
# 33182    36 months
# Name: Loan.Length, dtype: object

# Remove the word 'months' from the Loan.Length column.
# scrubLoanLength = loansData['Loan.Length'].map(lambda x: int(x.rstrip(' months')))
scrubLoanLength = [x.rstrip(' months') for x in loansData['Loan.Length']]

# Verify that the unwanted words were stripped from the column.
scrubLoanLength[0:5]
# ['36', '36', '60', '36', '36']

# Apply changes to the original data set.
loansData['Loan.Length'] = scrubLoanLength

# Continue with cleaning of other data columns.
loansData['FICO.Range'][0:5]
# 81174    735-739
# 99592    715-719
# 80059    690-694
# 15825    695-699
# 33182    695-699
# Name: FICO.Range, dtype: object

# To get the lower bound on the FICO range, select the first three digits only.
simplifiedFICO = loansData['FICO.Range'].map(lambda x: int(x[:3]))
# 81174    735
# 99592    715
# 80059    690
# 15825    695
# 33182    695

# Apply changes to the original data set.
loansData['FICO.Score'] = simplifiedFICO

# Save the cleaned data to a CSV file.
loansData.to_csv('loansData_clean.csv', header=True, index=False)

# Plot a histogram of FICO scores.
plt.figure()
p = loansData['FICO.Score'].hist()
plt.show()

# Create a scatterplot matrix.
a = pd.scatter_matrix(loansData, alpha=0.05, figsize=(10, 10), diagonal='hist')
plt.show()

# Create a linear regression with two independent variables 
# (FICO Score and Loan Amount) to help determine the dependent 
# variable (Interest Rate).
intrate = loansData['Interest.Rate']
loanamt = loansData['Amount.Requested']
fico = loansData['FICO.Score']

y = np.matrix(intrate).transpose()
x1 = np.matrix(fico).transpose()
x2 = np.matrix(loanamt).transpose()
x = np.column_stack([x1, x2])

X = sm.add_constant(x)
model = sm.OLS(y, X)
f = model.fit()
print f.summary()