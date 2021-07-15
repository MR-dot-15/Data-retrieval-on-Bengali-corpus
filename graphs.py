import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sc

data = sc.expon.rvs(scale = 0.3, loc = 0, size = 30)
m = data.mean()
sd = data.std()
data_mod = np.tanh((data-m)/sd)

x = np.arange(0, 1, 0.01)
func = np.tanh((x - m)/sd)

plt.subplot(1,2,1)
plt.scatter(data, np.zeros_like(data), label = 'exponential(0,1)')
plt.plot(x, func, alpha = 0.5, label = 'Classifier tanh')
plt.plot(x, 0.7 * np.ones_like(x),  '--r', alpha = 0.3, label = 'threshold')
plt.scatter(data, data_mod, label = 'classified(0,1)')
plt.xlim(0, 1)
plt.ylim(-1, 1)
plt.grid(True, alpha = 0.2)
plt.legend(loc = 'lower right')

plt.subplot(1,2,2)
plt.scatter(data, np.zeros_like(data), label = 'exponential(0,1)')
plt.plot(x, 0.7 * np.ones_like(x),  '--r', alpha = 0.3, label = 'threshold')
plt.plot( [0.7, 0.7], [-1, 1],'--r', alpha = 0.3)
plt.scatter(np.ones_like(data_mod)/2, data_mod, label = 'classified(0,1)')
plt.grid(False)
plt.xlim(0, 1)
plt.ylim(-1, 1)
plt.legend(loc = 'lower left')

plt.show()