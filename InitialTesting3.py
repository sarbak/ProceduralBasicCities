import numpy as np
import matplotlib.pyplot as plt
import os

landSize = 50
landLimits = 100

# Initializing the array
x = np.linspace(0, landLimits, landSize)
y = np.linspace(0, landLimits, landSize)
land = np.zeros((landSize,landSize))
landValue = np.zeros((landSize,landSize))

def extents(f):
  delta = f[1] - f[0]
  return [f[0] - delta/2, f[-1] + delta/2]

def valuate():
    for j in range(0,landSize):
        for k in range(0,landSize):
            landValue[j][k] = landSize*2 - (abs(j-landSize/2) + abs(k-landSize/2))

def road():
    for i in range (0,landSize):
        land[i][25] = -1

def build():
    
    lotSize = 3
    buildValue = np.zeros((landSize,landSize))

    # Initialize max Value, max X coordinate, max Y coordinate
    mVal = 0
    mX = -1
    mY = -1
    
    # Iterate for every cell
    for j in range(0,landSize-lotSize):
       for k in range(0,landSize-lotSize):
           
           # Sum up the relative values of the landValues
           for l in range(0,lotSize):
               for m in range(0,lotSize):
                   buildValue[j][k] += landValue[j+l][k+m]
                   
                   # Keep track of the maximum
                   if(buildValue[j][k]>mVal):
                       mVal = buildValue[j][k]
                       mX = j
                       mY = k
    
    
    
    print(mVal, mX, mY)


#==============================================================================
# TODOS
# - Sum up neighbor values - DONE
# - Pick the highest spot, print its coordinates - DONE
# - Put road into a function - DONE
# - Build onto that location, on data
# - Do not build on the road
# - Factor in the benefit of the road
# - Let the lot size change by x and y
# - Give random lot sizes
# - Make sure you understand columns and rows
# 
#==============================================================================

#print(landValue)

# Adding a new road

valuate()
road()
build()

# Visualizing the array
plt.imshow(land,aspect='auto', interpolation='none',
           extent=extents(x) + extents(y), origin='lower')

i = 0
while os.path.exists('{}{:d}.png'.format("city", i)):
    i += 1
plt.savefig('{}{:d}.png'.format("city", i))


