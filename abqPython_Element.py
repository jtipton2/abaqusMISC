#==============================================================================
# IMPORT NECESSARY MODULES
#==============================================================================
# C:\temp>abaqus viewer -noGUI  (this requires a CAE license)
# C:\temp>abaqus python         (this does not require a license)

import numpy as np
import time
from odbAccess import openOdb
from abaqusConstants import *
from multiprocessing import Pool
from contextlib import closing
import os
import sys



#==============================================================================
# OPEN SOLUTION FILE
#==============================================================================
filename = 'Job-3-HIP-SS-Pulse'

odb = openOdb(filename+'.odb',readOnly=True)

allSteps = odb.steps.keys()



#==============================================================================
# CHOOSE SPECIFIC ELEMENT
#==============================================================================
allInstances = (odb.rootAssembly.instances.keys())

odbInstance = odb.rootAssembly.instances[allInstances[-1]]

numElement = 941916

thisElement = odbInstance.ElementSetFromElementLabels(name='fakename', elementLabels=(numElement,))

intPnt = 4



#==============================================================================
# INITIALIZE ARRAY
#==============================================================================
numRows = 0

for i in range(len(allSteps)):
   Frame = odb.steps[allSteps[i]].frames
   numRows = numRows + len(Frame)

thisData = np.zeros((numRows,10))



#==============================================================================
# GET DATA
#==============================================================================
rowNum = 0

for i in range(len(allSteps)):
   Frame = odb.steps[allSteps[i]].frames
   stepTime = odb.steps[allSteps[i]].totalTime
   for j in range(len(Frame)):
      frameTime = stepTime + Frame[j].frameValue
      frameLE = Frame[j].fieldOutputs['LE'].getSubset(position = INTEGRATION_POINT).getSubset(region=thisElement).values[intPnt-1].data
      frameVM = Frame[j].fieldOutputs['S'].getSubset(region=thisElement).values[intPnt-1].mises
      framePEEQ = Frame[j].fieldOutputs['PEEQ'].getSubset(position = INTEGRATION_POINT).getSubset(region=thisElement).values[intPnt-1].data
      thisData[rowNum,0] = frameTime
      thisData[rowNum,1] = i
      thisData[rowNum,2] = frameVM
      thisData[rowNum,3:9] = frameLE
      thisData[rowNum,-1] = framePEEQ
      rowNum = rowNum + 1



#==============================================================================
# SAVE DATA TO FILE
#==============================================================================
headertxt1 = filename + '\n'
headertxt2 = 'Element ' + str(numElement) + ';  Integration Point ' + str(intPnt) + '\n'
headertxt3 = 'Step Names: ' + ' , '.join(allSteps) + '\n\n'
headertxt4 = 'TIME , STEP , MISES , LE11 , LE22 , LE33 , LE12 , LE13 , LE23, PEEQ'
headertxt = headertxt1 + headertxt2 + headertxt3 + headertxt4

np.savetxt(filename+'.csv', thisData, header = headertxt, delimiter = ',')

odb.close()
