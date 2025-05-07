code1 = '''import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

# Settings

M = 10000  # Number of samples
sample\_sizes = \[5, 50, 500]  # Sample sizes to evaluate
distribution\_funcs = {
'Normal': lambda size: np.random.normal(loc=0, scale=1, size=size),
'Binomial': lambda size: np.random.binomial(n=10, p=0.5, size=size),
'Poisson': lambda size: np.random.poisson(lam=3, size=size),
'Cauchy': lambda size: np.random.standard\_cauchy(size=size)
}

# Plotting individual plots for each distribution

for name, dist\_func in distribution\_funcs.items():
plt.figure(figsize=(10, 6))
plt.title(f"Distribution of Sample Means - {name}")
for N in sample\_sizes:
data = dist\_func((M, N))
sample\_means = np.mean(data, axis=1)

```
    sns.histplot(sample_means, kde=True, stat="density", bins=50, label=f"N={N}")

    if name != 'Cauchy':
        mu, std = np.mean(sample_means), np.std(sample_means)
        x = np.linspace(mu - 4*std, mu + 4*std, 1000)
        plt.plot(x, norm.pdf(x, mu, std), 'r-', lw=2)

plt.xlabel("Mean")
plt.ylabel("Density")
plt.legend()
plt.tight_layout()
plt.show()
```
'''
