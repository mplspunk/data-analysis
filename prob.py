import collections
import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt

# read in dataset and count frequencies
x = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 4, 4, 4, 4, 5, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 9, 9]

c = collections.Counter(x)

print c

count_sum = sum(c.values())

# output frequencies for the dataset x
for k,v in c.iteritems():
  print "The frequency of number " + str(k) + " is " + str(float(v) / count_sum)

# create and save a boxplot
plt.boxplot(x)
plt.show()
plt.savefig("boxplot.png")

# create and save a histogram
plt.hist(x, histtype='bar')
plt.show()
plt.savefig("histogram.png")

# create and save a QQ-plot
plt.figure()
test_data = np.random.normal(size=1000)   
graph1 = stats.probplot(test_data, dist="norm", plot=plt)
plt.show()
plt.savefig("qqplot.png")
