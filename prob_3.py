# Problem 3: Largest Prime Factor
# The prime factors of 13195 are 5, 7, 13 and 29.
# What is the largest prime factor of the number 600851475143?

n = 600851475143
i = 2
factors = []

while i <= n:
    if n % i == 0:
    	n /= i
    	factors.append(i)
    else:
    	i += 1
 
print "The prime factors are: {}".format(factors)
print "The largest prime factor is: " + str(max(factors))
