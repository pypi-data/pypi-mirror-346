code7 = '''import numpy as np
import matplotlib.pyplot as plt
x=np.array(\[1,2,3,4,5,6,7,8,9,10])
y=np.array(\[3,4,5,6,7,8,10,14,19,20])
m=len(x)

\#initial guess
theta0=0
theta1=0

\#hyperparameters
alpha=0.01
epochs=20 #no of iterations

\#store cost history for potting
cost\_history=\[]
error\_sq=0

\#gradient descent iterations
for \_ in range(epochs):
pred=theta0+theta1\*x
error=pred-y
error\_sq+=np.sum(error\*\*2) #a+=y means a=a+b

\#compute gradients
grad0=np.sum(error)/m
grad1=np.sum(error\*x)/m

\#update parameters
theta0-=alpha*grad0 #a-=b means a=a-b
theta1-=alpha*grad1

\#cost function
cost=np.sum(error\*\*2)/(2\*m)
cost\_history.append(cost)

print("final parameters: theta0=",theta0,"theta1=",theta1)

y\_pred=theta0+theta1\*x

x\_design=np.vstack((np.ones(m),x)).T #correlation matrix of regression parameters
sigma\_sq=error\_sq/(m-2) #residual(e) variance

\#covariance matrix of parameters
xtx\_inv=np.linalg.inv(x\_design.T\@x\_design) #@=matrix multiplication
cov\_matrix=sigma\_sq\*xtx\_inv

\#correlation matrix
std\_dev=np.sqrt(np.diag(cov\_matrix))
corr\_matrix=cov\_matrix/np.outer(std\_dev,std\_dev)

print("covariance matrix=\n",cov\_matrix)
print("correlation matrix=\n",corr\_matrix)

plt.scatter(x,y,color='green',label='observed data')
plt.plot(x,y\_pred,color='blue',label='Gradient Descent')
plt.plot(x,df\['y\_pred'],label='Least Square Fitting') #comparing with least square fitting
plt.xlabel('x')
plt.ylabel('y')
plt.title('Linear Regression using Gradient Descent')
plt.legend()
plt.grid()
plt.show()

\#plot cost convergence
plt.plot(cost\_history)
plt.xlabel('epochs (iterations)')
plt.ylabel('cost (MSE)')
plt.title('Convergence of Gradient Descent')
plt.grid()
plt.show()code 7
'''
