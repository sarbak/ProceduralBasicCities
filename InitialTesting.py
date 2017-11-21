import numpy as np
import matplotlib.pyplot as plt

landSize = 50
landLimits = 100

def extents(f):
  delta = f[1] - f[0]
  return [f[0] - delta/2, f[-1] + delta/2]

x = np.linspace(0, landLimits, landSize)
y = np.linspace(0, landLimits, landSize)
data = np.zeros((landSize,landSize))


for x in range (0,landSize):
    data[25][x] = 1

print(data) 

plt.imshow(data, cmap=plt.cm.BuPu_r,aspect='auto', interpolation='none',
           extent=extents(x) + extents(y), origin='lower')
plt.savefig('py.png')


#==============================================================================
# TODO
# - Add an initial road
# - Pull out size and limits as a separate variable
# - Make it save py.png next to each other
# 
#==============================================================================
