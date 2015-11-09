import pandas as pd
import statsmodels.api as sm
import math

df = pd.read_csv('loansData_clean.csv')
df

# Add a column to your dataframe indicating whether the interest rate is < 12%. 
threshold = 0.12
df['IR_TF'] = df['Interest.Rate'].map(lambda x: x <= threshold)

# Do some spot checks to make sure that it worked.
df[df['Interest.Rate'] == .10].head() # should all be True
df[df['Interest.Rate'] == .13].head() # should all be False

# Add a column of ones for the constant intercept term
df['Intercept'] = 1.0

# Create a list of the column names of our independent variables.
ind_vars = ['Amount.Requested', 'FICO.Score', 'Intercept']

# Model how the interest rate varies with FICO score and the loan amount desired.
logit = sm.Logit(df['IR_TF'], df[ind_vars])

# Fit the model
result = logit.fit()
# Optimization terminated successfully.
        # Current function value: 0.319503
        # Iterations 8

# Get the fitted coefficients from the results.
coeff = result.params
print coeff
# Amount.Requested    -0.000174
# FICO.Score           0.087423
# Intercept          -60.125045
# dtype: float64

def interest_rate(FICOScore, AmountRequested, coeff):
    return -(coeff[2] + (coeff[1] * FICOScore) + (coeff[0] * AmountRequested))

# Take a FICO Score and Loan Amount and return p.
def logistic_function(FICOScore, AmountRequested):
	p = 1/(1 + math.exp(-1*(coeff[2] + coeff[1]*FICOScore + coeff[0]*AmountRequested)))
	if p > .70:
		print str(p) + " Congratulations! You are funded at a competitive interest rate!"
	else:
		print str(p) + " Unfortunately, we are not able to offer you a loan at an interest rate below 12%."

logistic_function(750, 10000)
