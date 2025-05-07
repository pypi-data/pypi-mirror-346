code4 = '''import numpy as np
from scipy.stats import binom
import matplotlib.pyplot as plt

def toss\_coin(n,q):
tosses=np.random.binomial(1,q,n)
return tosses

def binomial\_test(n,observed\_tosses,q\_expected=0.5,alpha=0.05):
observed\_heads=np.sum(observed\_tosses)
prob\_left=binom.cdf(observed\_heads,n,q\_expected)
prob\_right=1-binom.cdf(observed\_heads-1,n,q\_expected)
p\_value=2\*min(prob\_left,prob\_right)
reject\_null=p\_value\<alpha
return reject\_null,p\_value,observed\_heads

\#Parameters
n=100
q=0.5

observed\_tosses=toss\_coin(n,q) #Simulate tossing a coin

\#Perform the Binomial test
p\_value,reject\_null,observed\_heads=binomial\_test(n,observed\_tosses,q\_expected=0.5,alpha=0.05)

\#Output results
print("p\_value=",p\_value)
print("observed\_heads=",observed\_heads)

if reject\_null:
print("Reject null hypothesis (0.5): the observed result is significantly different from 0.5")
else:
print("Fail to reject null hypothesis (0.5): the observed result is not significantly different from 0.5")

\#Plot te distribution of heads (Binomial)
x=np.arange(0,n+1)
pmf=binom.pmf(x,n,q)

plt.plot(x,pmf,label="Expected distribution",color='blue')
plt.vlines(observed\_heads,0,binom.pmf(observed\_heads,n,q),color='red',label="Observed heads")
plt.xlabel("Number of heads")
plt.ylabel("Probability mass function")
plt.title("Binomial Test for Coin Tosses")
plt.legend()
plt.show()
Code 4
'''
