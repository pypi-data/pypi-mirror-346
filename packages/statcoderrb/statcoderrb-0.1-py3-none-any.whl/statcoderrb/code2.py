code2 = '''import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Helper function to compute and plot joint probability

def plot\_joint\_prob(ax, xi, yi, title):
data = pd.DataFrame({'x': xi, 'y': yi})
x\_probs = data\['x'].value\_counts(normalize=True).sort\_index()
y\_probs = data\['y'].value\_counts(normalize=True).sort\_index()
joint\_probs = pd.DataFrame(np.outer(x\_probs, y\_probs), index=x\_probs.index, columns=y\_probs.index)

```
sns.heatmap(joint_probs, ax=ax, annot=True, fmt=".4f", cmap="Reds", cbar=True)
ax.set_title(title)
ax.set_xlabel("Y")
ax.set_ylabel("X")
```

# Set up plot grid

fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle("Joint Probability Distribution Graph", fontsize=16)

# 1. Theoretical distribution

xi = \[1, 2, 3, 4, 5, 6]
yi = \[1, 2, 3, 4, 5, 6]
plot\_joint\_prob(axes\[0, 0], xi, yi, "Theoretical Distribution")

# 2. Manual data

xi = \[1,2,3,2,4,5,2,3,4,2,6,7,5,8,2,4,5,6,7,9,5,3,4,2,4]
yi = \[9,8,7,9,7,5,4,8,9,5,4,7,6,9,6,7,3,5,7,9,5,8,6,7,4]
plot\_joint\_prob(axes\[0, 1], xi, yi, "Manual Distribution")

# 3. Random small sample

xi = np.random.randint(1, 7, 10)
yi = np.random.randint(1, 7, 10)
plot\_joint\_prob(axes\[1, 0], xi, yi, "Random Small Sample")

# 4. Random large sample

xi = np.random.randint(1, 7, 10000)
yi = np.random.randint(1, 7, 10000)
plot\_joint\_prob(axes\[1, 1], xi, yi, "Random Large Sample")

# Show the plot

# plt.tight\_layout(rect=\[0, 0, 1, 0.95])

plt.show()
Code 2
'''
