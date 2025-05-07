code5 = '''import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

\#parameters
N=100
M=60

\#Beta distribution parameters
a,b=2,3

\#Gaussian distribution parameters
mean\_prior=0.5
var\_prior=0.1
std\_prior=np.sqrt(var\_prior)

\#compute MLE (Max. Likelihood Estimate) of f
f\_mle=M/N

\#define range of f values for plotting
f\_values=np.linspace(0,1,1000)

\#compute priors
beta\_prior=stats.beta(a,b).pdf(f\_values)
gaussian\_prior=stats.norm(mean\_prior,std\_prior).pdf(f\_values)

\#compute likelihood (normalized pmf)
likelihood=stats.binom.pmf(M,N,f\_values)
norm\_likelihood=likelihood/np.max(likelihood) #normalization

\#compute Beta posterior
a\_post=a+M
b\_post=b+(N-M)
beta\_post=stats.beta(a\_post,b\_post).pdf(f\_values)

\#compute Gaussian posterior
var\_post=1/(N/(f\_mle\*(1-f\_mle))+1/(var\_prior))
mean\_post=var\_post\*((N*f\_mle)/(f\_mle*(1-f\_mle))+(mean\_prior/var\_prior))
std\_post=np.sqrt(var\_post)
gaussian\_post=stats.norm(mean\_post,std\_post).pdf(f\_values)

\#plot distributions
plt.figure(figsize=(10,6))
plt.plot(f\_values,norm\_likelihood,label="Likelihood (normalized)",color='blue',linestyle='dashed')
plt.plot(f\_values,beta\_prior,label="Beta prior",color='red',linestyle='dotted')
plt.plot(f\_values,beta\_post,label="Beta posterior",color='brown')
plt.plot(f\_values,gaussian\_prior,label="Gaussian prior",color='green',linestyle='dotted')
plt.plot(f\_values,gaussian\_post,label="Gaussian posterior",color='black')
plt.axvline(f\_mle,color='red',linestyle='dashed',label='MLE')
plt.xlabel('f values')
plt.ylabel('probability')
plt.title('Bayesian Statistics')
plt.grid()
plt.legend()
plt.show()
Code 5
'''
