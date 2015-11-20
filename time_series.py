import pandas as pd
import numpy as np 
import statsmodels.api as sm
import matplotlib.pyplot as plt

df = pd.read_csv('LoanStats3c.csv', header=1, low_memory=False)

# Convert string to datetime object in pandas.
df['issue_d_format'] = pd.to_datetime(df['issue_d']) 
dfts = df.set_index('issue_d_format') 
year_month_summary = dfts.groupby(lambda x : x.year * 100 + x.month).count()
loan_count_summary = year_month_summary['issue_d']

# Plot the loan data (loan_count_summary). 
loan_count_summary.plot()
plt.ylabel("Number of Loans")
plt.xlabel("Month")
plt.show()

# Get the differences.
loan_count_sum_diff = loan_count_summary.diff()
plt.plot(loan_count_sum_diff)
plt.show()

#Plot out the autocorrelation (ACF) of the series. 
sm.graphics.tsa.plot_acf(loan_count_summary)
plt.show()

#Plot out the partial autocorrelation (PACF) of the series.
sm.graphics.tsa.plot_pacf(loan_count_summary)
plt.show()