from numpy import linspace
from scipy.fft import fft, fftfreq
import numpy as np
import matplotlib.pyplot as plt

N = 600
x = linspace(1, N, N)
y = np.sin(np.pi*x/10) * (600 - x) ** 4
yf = fft(y)

plt.plot(y)
plt.show()

plt.figure()
plt.plot(np.abs(yf[0:N//2]), linewidth=0.3)
plt.show()
