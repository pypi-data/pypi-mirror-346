code3 = '''import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set up figure and axes

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle("Joint Probability Distribution for Normal Variables", fontsize=16)

# Sample sizes and titles

samples = \[10, 400, 1000]
titles = \["Small Sample (10)", "Medium Sample (400)", "Large Sample (1000)"]

# Loop over each sample size

for i in range(3):
np.random.seed(42)
x = np.random.normal(0, 1, samples\[i])
y = np.random.normal(0, 1, samples\[i])
data = pd.DataFrame({'x': x, 'y': y})

```
# Plot KDE + scatter
sns.kdeplot(data=data, x='x', y='y', ax=axes[i], cmap="Reds", fill=True, levels=30, cbar=True, thresh=0)
axes[i].scatter(x, y, color='blue', alpha=0.5, s=5)
axes[i].set_title(titles[i])
axes[i].grid(True)
```

# plt.tight\_layout(rect=\[0, 0, 1, 0.93])

plt.show()
Code 3
'''
