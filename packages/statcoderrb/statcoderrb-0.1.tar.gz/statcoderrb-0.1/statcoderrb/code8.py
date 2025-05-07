code8 = '''import numpy as np
import matplotlib.pyplot as plt

def sigmoid(z):
return 1/(1+np.exp(-z))

x=np.random.uniform(-1000,1000,20)
y=sigmoid(x)

theta0=0
theta1=0

\#hyperparameters
alpha=0.001
epochs=1000
m=len(x)

\#store loss history
loss\_history=\[]

\#Gradient Descent for Logistic Regression
for \_ in range(epochs):
z=theta0+theta1\*x
pred=sigmoid(z)

epsilon=1e-9 #to avoid log(0)
loss=-np.mean(y\*np.log(pred+epsilon)+(1-y)\*np.log(1-pred+epsilon))
loss\_history.append(loss)

\#gradients
error=pred-y
grad0=np.mean(error)
grad1=np.mean(error\*x)

\#update parameters
theta0-=alpha*grad0
theta1-=alpha*grad1

\#final parameters
print(f"\nFinal parameters:\ntheta0={theta0:.4f},theta1={theta1:.4f}")

\#plot decision boundary (sigmoid curve)
x\_plot=np.linspace(-1000,1000,500)
z\_plot=sigmoid(theta0+theta1\*x\_plot)

plt.scatter(x,y,color='blue',label='data')
plt.plot(x\_plot,z\_plot,color='green',label='Logistic Regression')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Logistic Regression')
plt.legend()
plt.grid()
plt.show()

\#plot loss convergence
plt.plot(loss\_history)
plt.xlabel('epochs')
plt.ylabel('loss')
plt.title('Loss Convergence')
plt.grid()
plt.show()
Code 8
'''
