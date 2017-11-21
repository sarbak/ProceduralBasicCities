import numpy as np
import matplotlib.pyplot as plt
import os

landSize = 50
landLimits = 100

def extents(f):
  delta = f[1] - f[0]
  return [f[0] - delta/2, f[-1] + delta/2]

# Initializing the array
x = np.linspace(0, landLimits, landSize)
y = np.linspace(0, landLimits, landSize)
data = np.zeros((landSize,landSize))

# Adding a new road
for i in range (0,landSize):
    data[i][25] = -1

# Visualizing the array
plt.imshow(data,aspect='auto', interpolation='none',
           extent=extents(x) + extents(y), origin='lower')

i = 0
while os.path.exists('{}{:d}.png'.format("city", i)):
    i += 1
plt.savefig('{}{:d}.png'.format("city", i))






#==============================================================================
# TODO
# - Add an initial road - DONE
# - Pull out size and limits as a separate variable - DONE
# - Make it save py.png next to each other - DONE
# - New Github
# 
#==============================================================================
