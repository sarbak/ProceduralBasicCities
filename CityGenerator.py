#==============================================================================
# TODO
# - Roads
# -- Figure out whether to build vertical or horizontal roads
# -- Build appropriately varying length roads
# - Greenspace
# -- Add greenspace without road connection
# 
# Open concerns
# - valuator denies valuation if there is no road connection
# - there is no generate() function
# - the color scheme is not fun
# - some roads override
#==============================================================================






import numpy as np
import matplotlib.pyplot as plt
import os
import random

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

def buildInitialRoad():
    for i in range (0,landSize):
        land[i][25] = 2

def buildNewRoad():
#    bestHor = valuateFor(10,1)

    
    bestVer = valuateFor(1,10)
    buildOnLot(bestVer[1],bestVer[2],1, 10, 2, False)
    
#    if(bestHor[0]>bestVer[0]):
#        buildOnLot(bestHor[1],bestHor[2],10, 1, 2, False)
#    else:
#        buildOnLot(bestVer[1],bestVer[2],1, 10, 2, False)

def build():
    
    lotSizeX = random.randint(3,6)
    lotSizeY = random.randint(3,6)

    maxLot = valuateFor(lotSizeX, lotSizeY)

    buildOnLot(maxLot[1],maxLot[2],lotSizeX, lotSizeY, 1, True)

           
def buildOnLot(mX, mY, lotSizeX, lotSizeY, val, border):
    
    # Build on the land
    for l in range(0,lotSizeX):
        for m in range(0,lotSizeY):

            land[mX+l][mY+m] = val
            
            if(border == True):
                # The borders are half occupied
                land[mX][mY+m] = 0.5
                land[mX+lotSizeX-1][mY+m] = 0.5
                land[mX+l][mY] = 0.5
                land[mX+l][mY+lotSizeY-1] = 0.5
    
def checkForRoad(x,y, lotSizeX,lotSizeY):
    
    roadAccess = False

    for j in range(-1,lotSizeX+1):
       for k in range(-1,lotSizeY+1):
           if(land[x+j][y+k] == 2):
               roadAccess = True
    
    return roadAccess       
            
def valuateFor(lotSizeX, lotSizeY):
    
    buildValue = np.zeros((landSize,landSize))
    
    # Initialize max Value, max X coordinate, max Y coordinate
    mVal = 0
    mX = -1
    mY = -1
    
    # Iterate for every cell
    for j in range(0,landSize-lotSizeX):
       for k in range(0,landSize-lotSizeY):
           
           # Sum up the relative values of the landValues
           for l in range(0,lotSizeX):
               for m in range(0,lotSizeY):

                   # Check if the lot is occupied
                   if(land[j+l][k+m] >= 1):
                        buildValue[j][k] = 0
                   else:
                        buildValue[j][k] += landValue[j+l][k+m]
                   
           # Check if it has access to road
           roadAccess = checkForRoad(j,k,lotSizeX,lotSizeY)
           if(roadAccess == False):
               buildValue[j][k] = 0

           # Keep track of the maximum
           if(buildValue[j][k]>mVal):
               mVal = buildValue[j][k]
               mX = j
               mY = k
    
    return [mVal, mX, mY]




# Key Activities
valuate()
buildInitialRoad()

for j in range (0,4):
    for k in range (0,15):
        build()
    buildNewRoad()

# Visualizing the array
plt.imshow(land,aspect='auto', interpolation='none',
           extent=extents(x) + extents(y), origin='lower')

i = 0
while os.path.exists('{}{:d}.png'.format("city", i)):
    i += 1
plt.savefig('{}{:d}.png'.format("city", i))


