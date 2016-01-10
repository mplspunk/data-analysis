import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
# %matplotlib inline


# Set seed for reproducible results
np.random.seed(414)

# Generate toy data
X = np.linspace(0, 15, 1000)
y = 3 * np.sin(X) + np.random.normal(1 + X, .2, 1000)

train_X, train_y = X[:700], y[:700]
test_X, test_y = X[700:], y[700:]

train_df = pd.DataFrame({'X': train_X, 'y': train_y})
test_df = pd.DataFrame({'X': test_X, 'y': test_y})

# Linear Fit
poly_1 = smf.ols(formula='y ~ 1 + X', data=train_df).fit()
pred1 = poly_1.predict(test_df)
actual = np.array(test_df['y'].tolist())
mse1 = mean_squared_error(actual, pred1)
print "Linear Fit: The Mean Squared Error is {}.".format(mse1)
# Linear Fit: The Mean Squared Error is 6.54754127446.
print "\n"*2

# Quadratic Fit
poly_2 = smf.ols(formula='y ~ 1 + X + I(X**2)', data=train_df).fit()
pred2 = poly_2.predict(test_df)
mse2 = mean_squared_error(actual, pred2)
print "Quadratic Fit: The Mean Squared Error is {}.".format(mse2)
# Quadratic Fit: The Mean Squared Error is 7.98738294501.
print "\n"*2

# Cubic Fit
poly_3 = smf.ols(formula = 'y ~ 1 + X + I(X**2) + I(X**3)', data=train_df).fit()
pred3 = poly_3.predict(test_df)
mse3 = mean_squared_error(actual, pred3)
print "Cubic Fit: The Mean Squared Error is {}.".format(mse3)
# Cubic Fit: The Mean Squared Error is 199.654810444.
print "\n"*2

# Visualize the fitting and the polynomial terms
plt.figure()
plt.scatter(test_X, test_y)
plt.xlabel('test_X')
plt.ylabel('test_y')
plt.plot(test_X, pred1, 'b-', label='x^1')
plt.plot(test_X, pred2, 'g-', label='x^2')
plt.plot(test_X, pred3, 'r-', label='x^3')
plt.show()


