import numpy as np
import shipCalculator as sc
import matplotlib.pyplot as plt
from scipy.integrate import simps

def f(x):
    return (0.05*x**2 + 0.1*x)

x = np.array([0,1,2,3,4])
y = f(x)

f1 = plt.figure()
plt.plot(x,y)
a2= simps(y,x)
print(a2)
plt.show()