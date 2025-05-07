code6 = '''import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

x=np.array(\[1,2,3,4,5,6,7,8,9,10])
y=np.array(\[3,4,5,6,7,8,10,14,19,20])
data={'x'\:x,'y'\:y}
df=pd.DataFrame(data)

x\_bar=np.mean(x)
y\_bar=np.mean(y)
n=len(x)
confidence=0.90

s\_xx=np.sum((x-x\_bar)\*\*2)
s\_yy=np.sum((y-y\_bar)\*\*2)
s\_xy=np.sum((x-x\_bar)*(y-y\_bar))
b1=s\_xy/s\_xx
b0=y\_bar-b1*x\_bar

df\['y\_pred']=b1\*df\['x']+b0
e=y-df\['y\_pred']

data1={'x'\:x,'y'\:y,'x-x\_bar'\:x-x\_bar,'y-y\_bar'\:y-y\_bar,'(x-x\_bar)^2':(x-x\_bar)\*\*2,'(y-y\_bar)^2':(y-y\_bar)**2,'(x-x\_bar)(y-y\_bar)':(x-x\_bar)\*(y-y\_bar),'y\_fitted'\:df,'e'\:e,'e^2'\:e**2}
df1=pd.DataFrame(data1)
print(df1)

errors=np.array(e)
sum\_e=np.sum(e)
sum\_e2=np.sum(e\*\*2)
se=np.sqrt(sum\_e2/n-2) #std. error
se\_b=se/np.sqrt(s\_xx) #std. error for slope

t\_critical=stats.t.ppf((1+confidence)/2,df=n-2)

lower\_ci=b1-t\_critical*se\_b
upper\_ci=b1+t\_critical*se\_b

sum\_y=np.sum(y)
R\_sq=1-(sum\_e/sum\_y) #correlation coefficient
print("correlation coeff:",R\_sq)

plt.errorbar(x,y,yerr=np.abs(errors),fmt='o',label='data points with error bars',capsize=5)
plt.plot(x,df\['y\_pred'],label='Regression Line')
plt.fill\_between(x,b0+lower\_ci*x,b0+upper\_ci*x,color='red',alpha=0.2,label='90% confidence interval')
plt.title('Least Square Fitting')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid()
plt.show()
Code 6
'''
