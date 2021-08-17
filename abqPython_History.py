#
# IMPORT MODULES
#
import numpy as np
import time
from odbAccess import openOdb
from abaqusConstants import *
from contextlib import closing
import os
import sys

#
# OPEN ODB AND GET INFO
#
filename = 'Job-3-HIP-SS-Pulse.odb'

odb = openOdb(filename,readOnly=True)

i = 0

allSteps = odb.steps.keys()

thisStep = odb.steps.keys()[i]

allEnergy = odb.steps[thisStep].historyRegions['Assembly ASSEMBLY'].historyOutputs.keys()

#
# GET TOTAL ARRAY SIZE
#
totLength = 0

for i in range(len(allSteps)):
   thisStep = odb.steps.keys()[i]
   thisEnergy = odb.steps[thisStep].historyRegions['Assembly ASSEMBLY'].historyOutputs.keys()[5]
   thisEnergyData = odb.steps[thisStep].historyRegions['Assembly ASSEMBLY'].historyOutputs[thisEnergy].data
   totLength = totLength + len(thisEnergyData)

#
# GET ENERGY HISTORIES
#
allHistory = np.zeros((totLength,len(allEnergy)+2))
rowStart = 0
for i in range(len(allSteps)):
   thisStep = odb.steps.keys()[i]
   # Get energy from each step and concatenate
   for j in range(len(allEnergy)):
      thisEnergy = odb.steps[thisStep].historyRegions['Assembly ASSEMBLY'].historyOutputs.keys()[j]
      thisEnergyData = odb.steps[thisStep].historyRegions['Assembly ASSEMBLY'].historyOutputs[thisEnergy].data
      lenStep = len(thisEnergyData)
      rowEnd = rowStart + lenStep
      allHistory[rowStart:rowEnd,j+2] = np.asarray(thisEnergyData,dtype=('float'))[:,1]
   # Get step numbers
   allHistory[rowStart:rowEnd,1] = i+1
   # Get time values using last energy
   thisEnergy = odb.steps[thisStep].historyRegions['Assembly ASSEMBLY'].historyOutputs.keys()[j]
   thisEnergyData = odb.steps[thisStep].historyRegions['Assembly ASSEMBLY'].historyOutputs[thisEnergy].data
   lenStep = len(thisEnergyData)
   rowEnd = rowStart + lenStep
   allHistory[rowStart:rowEnd,0] = np.asarray(thisEnergyData,dtype=('float'))[:,0]
   # Advance to next block of time values
   rowStart = rowEnd

#
# SAVE FILE FOR LATER ANALYSIS
#
# np.savez_compressed(filename, allHistory=allHistory, allSteps=allSteps, allEnergy=allEnergy)

headertxt = ' , '.join(allSteps) + '\n\n' + 'TIME , STEP , ' + ' , '.join(allEnergy)

np.savetxt(filename+'.csv', allHistory, header = headertxt, delimiter = ',')

odb.close()
