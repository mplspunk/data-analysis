import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf


# Load the dataset and examine the number of observations.
loansData = pd.read_csv('LoanStats3c.csv', skiprows=1, low_memory=False)

len(loansData.index)
# 235631

loansData.info()
# <class 'pandas.core.frame.DataFrame'>
# Int64Index: 235631 entries, 0 to 235630
# Data columns (total 56 columns):
# id                             235631 non-null object
# member_id                      235629 non-null float64
# loan_amnt                      235629 non-null float64
# funded_amnt                    235629 non-null float64
# funded_amnt_inv                235629 non-null float64
# term                           235629 non-null object
# int_rate                       235629 non-null object
# installment                    235629 non-null float64
# grade                          235629 non-null object
# sub_grade                      235629 non-null object
# emp_title                      222393 non-null object
# emp_length                     235629 non-null object
# home_ownership                 235629 non-null object
# annual_inc                     235629 non-null float64
# verification_status            235629 non-null object
# issue_d                        235629 non-null object
# loan_status                    235629 non-null object
# pymnt_plan                     235629 non-null object
# url                            235629 non-null object
# desc                           15279 non-null object
# purpose                        235629 non-null object
# title                          235629 non-null object
# zip_code                       235629 non-null object
# addr_state                     235629 non-null object
# dti                            235629 non-null float64
# delinq_2yrs                    235629 non-null float64
# earliest_cr_line               235629 non-null object
# inq_last_6mths                 235629 non-null float64
# mths_since_last_delinq         119748 non-null float64
# mths_since_last_record         41524 non-null float64
# open_acc                       235629 non-null float64
# pub_rec                        235629 non-null float64
# revol_bal                      235629 non-null float64
# revol_util                     235504 non-null object
# total_acc                      235629 non-null float64
# initial_list_status            235629 non-null object
# out_prncp                      235629 non-null float64
# out_prncp_inv                  235629 non-null float64
# total_pymnt                    235629 non-null float64
# total_pymnt_inv                235629 non-null float64
# total_rec_prncp                235629 non-null float64
# total_rec_int                  235629 non-null float64
# total_rec_late_fee             235629 non-null float64
# recoveries                     235629 non-null float64
# collection_recovery_fee        235629 non-null float64
# last_pymnt_d                   235486 non-null object
# last_pymnt_amnt                235629 non-null float64
# next_pymnt_d                   180601 non-null object
# last_credit_pull_d             235602 non-null object
# collections_12_mths_ex_med     235629 non-null float64
# mths_since_last_major_derog    66478 non-null float64
# policy_code                    235629 non-null float64
# application_type               235629 non-null object
# annual_inc_joint               0 non-null float64
# dti_joint                      0 non-null float64
# verification_status_joint      0 non-null float64
# dtypes: float64(31), object(25)
# memory usage: 102.5+ MB

print "\n"*5

loansData = loansData.drop('annual_inc_joint', axis=1)
loansData = loansData.drop('dti_joint', axis=1)
loansData = loansData.drop('verification_status_joint', axis=1)

# Verify that appropriate columns were dropped.
print loansData.head()

print "\n"*5

# Load a sample/subset of the whole lending data set.
sample_size = int(len(loansData) * .1)
index_list = np.random.choice(loansData.index.tolist(),
                              sample_size, replace=False)
df = loansData.loc[index_list]
len(loansData.index)
# 23563

# Isolate the columns in which we are primarily interested.
df = df[['annual_inc', 'int_rate', 'home_ownership']]
print df.head()

print "\n"*5

df.info()
# <class 'pandas.core.frame.DataFrame'>
# Int64Index: 23563 entries, 174120 to 32940
# Data columns (total 3 columns):
# annual_inc        23563 non-null float64
# int_rate          23563 non-null object
# home_ownership    23563 non-null object
# dtypes: float64(1), object(2)
# memory usage: 736.3+ KB

print "\n"*5

# Remove the '%' sign from the 'int_rate' column.
df['int_rate'] = df['int_rate'].map(lambda x: x.rstrip('%'))
print df.head()

print "\n"*5

# Convert 'int_rate' from object to float.
df['int_rate'] = df.apply(lambda x: pd.Series(x['int_rate']).astype(float)
                          / 100, axis=1)
print df.info()
# <class 'pandas.core.frame.DataFrame'>
# Int64Index: 23563 entries, 174120 to 32940
# Data columns (total 3 columns):
# annual_inc        23563 non-null float64
# int_rate          23563 non-null float64
# home_ownership    23563 non-null object
# dtypes: float64(2), object(1)
# memory usage: 736.3+ KB

print "\n"*5

# Change homeownership to a dummy instead of a categorical.
newColumns = pd.get_dummies(df['home_ownership'])
df = pd.concat([df, newColumns], axis=1)

# Add a column with a constant intercept of 1.0.
df['Intercept'] = float(1.0)
print df.head()

print "\n"*5

# Use income to model interest rates.
model_1 = sm.OLS(df['int_rate'], df[['Intercept', 'annual_inc']])
f1 = model_1.fit()

print 'F1 Summary'
print '-------------'
print f1.summary()

print "\n"*5

# Add home ownership to the model.
model_2 = sm.OLS(df['int_rate'],
                 df[['Intercept', 'annual_inc', 'MORTGAGE', 'OWN', 'RENT']])
f2 = model_2.fit()

print 'F2 Summary'
print '-------------'
print f2.summary()

print "\n"*5

# Add the interaction of home ownership and incomes as a term.
model_3 = smf.ols(formula='int_rate ~ (annual_inc * OWN) + (annual_inc * MORTGAGE) + (annual_inc * RENT)', data=df)
f3 = model_3.fit()

print 'F3 Summary'
print '-------------'
print f3.summary()
