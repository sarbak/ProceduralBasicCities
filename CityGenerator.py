#==============================================================================
# TODO
# Communicating the buildings
# - Filename to automatically count up
# - No ',' in the last iteration
# - Ability to just let this machine run with it, and generate 10 cities
#
# Open concerns
# - valuator denies valuation if there is no road connection
# - there is no generate() function
# - the color scheme is not fun
# - some roads override
# - land values should be declared on top
#==============================================================================


import numpy as np
import matplotlib.pyplot as plt
import os
import random
import matplotlib.cm as cm

landSize = 100
landLimits = 100
randomSizeFactor = 8
rounds = 20 #10
intensity = 5 #10

codeRoad = 7
codeHighway = 8
codePark = 5
codeBuilding = 2
codeBuffer = 1

# Initializing the array
x = np.linspace(0, landLimits, landSize)
y = np.linspace(0, landLimits, landSize)
land = np.zeros((landSize,landSize))
landValue = np.zeros((landSize,landSize))
landPrint = np.zeros((landSize,landSize))

def fillLot(x,y, lotSizeX,lotSizeY, filled):
    for j in range(0,lotSizeX):
       for k in range(0,lotSizeY):
           if(filled):
               landPrint[x+j][y+k] = 1
           else:
               if(j == 0 or j == (lotSizeX-1) or k == 0 or k == (lotSizeY-1)):
                   landPrint[x+j][y+k] = 2
           

def extents(f):
  delta = f[1] - f[0]
  return [f[0] - delta/2, f[-1] + delta/2]

def valuate():
    for j in range(0,landSize):
        for k in range(0,landSize):
            landValue[j][k] = landSize*2 - (abs(j-landSize/2) + abs(k-landSize/2))

def buildHighway():
    #for i in range (0,landSize):
    #    land[i][int(landSize/2)] = codeHighway
    #    land[i][int(landSize/2)+1] = codeHighway
    #print(0, int(landSize/2), landSize-1, 3, codeHighway)    
    buildOnLot(0, int(landSize/2), landSize-1, 2, codeHighway, False)
    

def buildPark():
    lotSizeX = random.randint(int(randomSizeFactor/2),randomSizeFactor)
    lotSizeY = random.randint(int(randomSizeFactor/2),randomSizeFactor)

    maxLot = valuateFor(lotSizeX, lotSizeY, 'park')

    buildOnLot(maxLot[1],maxLot[2],lotSizeX, lotSizeY, codePark, False)

def buildNewRoad():
    length = random.randint(randomSizeFactor, int(randomSizeFactor*(intensity/2)))
    bestHor = valuateFor(length,1, 'road')   
    bestVer = valuateFor(1,length, 'road')
    #print("best hor and ver", bestHor, bestVer)
    if(max(bestHor[0],bestVer[0])>0):
    
        if(bestHor[0]>bestVer[0]):
            buildOnLot(bestHor[1],bestHor[2],length, 2, codeRoad, False)
        else:
            buildOnLot(bestVer[1],bestVer[2],2, length, codeRoad, False)
    

def build():
    
    lotSizeX = random.randint(max(int(randomSizeFactor/4),6),randomSizeFactor)
    lotSizeY = random.randint(max(int(randomSizeFactor/4),6),randomSizeFactor)

    maxLot = valuateFor(lotSizeX, lotSizeY, 'building')

    buildOnLot(maxLot[1],maxLot[2],lotSizeX, lotSizeY, codeBuilding+(random.randint(0,10)/10), True)

           
def buildOnLot(mX, mY, lotSizeX, lotSizeY, val, buffer):
    
    announceConstruction(mX, mY, lotSizeX, lotSizeY, val, buffer)
    
    # Build on the land
    for l in range(0,lotSizeX):
        for m in range(0,lotSizeY):

            land[mX+l][mY+m] = val
            
            if(buffer == True):
                # The borders are half occupied
                land[mX][mY+m] = codeBuffer
                land[mX+lotSizeX-1][mY+m] = codeBuffer
                land[mX+l][mY] = codeBuffer
                land[mX+l][mY+lotSizeY-1] = codeBuffer
    
    # Prepare the print            
    fill = False
    if(val == codePark):
        fill = True
    if(buffer):
        fillLot(mX+1, mY+1, lotSizeX-2, lotSizeY-2, fill)
    else:
        fillLot(mX, mY, lotSizeX, lotSizeY, fill)

def announceConstruction(mX, mY, lotSizeX, lotSizeY, val, buffer):
    text_file = open("instructions3.txt", "a")
    proportion = 1200 / landSize
    phrase = "{" + str(int(mX*proportion)) + ", " +  str(int((landSize - mY)*proportion)) + ", " + str(int(lotSizeX*proportion)) + ", " + str(int(lotSizeY*proportion)) + ", " + str(val) + "}"
    text_file.write(phrase)
    text_file.write(", ")
#    np.savetxt("instructions.txt", phrase, fmt="%s")
    print(phrase)
    text_file.close()



def checkForRoad(x,y, lotSizeX,lotSizeY):
    
    roadAccess = False

    for j in range(-1,lotSizeX+1):
       for k in range(-1,lotSizeY+1):
           if(x+j >= 0 and x+j<landLimits and y+k >= 0 and y+k < landLimits):
               if(land[x+j][y+k] >= codeRoad):
                   roadAccess = True
    
    return roadAccess       
            
def valuateFor(lotSizeX, lotSizeY, use):
    
    buildValue = np.zeros((landSize,landSize))
    
    # Initialize max Value, max X coordinate, max Y coordinate
    mVal = 0
    mX = -1
    mY = -1
    
    # Iterate for every cell
    for j in range(0,landSize-lotSizeX):
       for k in range(0,landSize-lotSizeY):
           
           
           if(use == 'building'):
           
               # Sum up the relative values of the landValues
               for l in range(0,lotSizeX):
                   for m in range(0,lotSizeY):
    
                       # Check if the lot is occupied
                       if(land[j+l][k+m] >= codeBuilding):
                            buildValue[j][k] = 0
                       else:
                            buildValue[j][k] += landValue[j+l][k+m]
                            
                       
               # Check if it has access to road
               roadAccess = checkForRoad(j,k,lotSizeX,lotSizeY)
               if(roadAccess == False):
                   buildValue[j][k] = 0



           if(use == 'road'):
                                                
               # Discount it if it touches the road too much
               for l in range(0,lotSizeX):
                  for m in range(0,lotSizeY):
    
                      if(land[j+l][k+m] >= codeBuffer):
                          buildValue[j][k] = 0
                      else:
                          if(not checkForRoad(j+l,k+m,1,1)):
                              buildValue[j][k] += landValue[j+l][k+m]
                          
                      # Check if that location touches the road much
               
               roadAccess = checkForRoad(j,k,lotSizeX,lotSizeY)
               if(roadAccess == False):
                  buildValue[j][k] = 0 
           
           if(use == 'park'):
                                                
               for l in range(0,lotSizeX):
                  for m in range(0,lotSizeY):
    
                      if(land[j+l][k+m] >= codeBuffer):
                          buildValue[j][k] = 0
                      else:
                          buildValue[j][k] += landValue[j+l][k+m]
                          

            
           # Keep track of the maximum
           if(buildValue[j][k]>mVal):
                
               mVal = buildValue[j][k]
               mX = j
               mY = k
               
#    if(use == 'road'):
#        print(lotSizeX, lotSizeY, mVal, mX, mY)
    
    return [mVal, mX, mY]







# Key Activities
valuate()
buildHighway()

for j in range (0,rounds):
    for k in range (0,intensity):
        build()
    buildNewRoad()
    buildPark()
    # Visualizing the array
    plt.imshow(land,cmap=cm.hot, aspect='auto', interpolation='none',
           extent=extents(x) + extents(y), origin='lower')
    plt.show()



i = 0
while os.path.exists('{}{:d}.png'.format("city", i)):
    i += 1
plt.savefig('{}{:d}.png'.format("city", i))


