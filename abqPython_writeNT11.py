#
# Get Nodal Temperatures and Write to Text File
# (modified from original by Lianshan Lin, ORNL)
# 
# run this script in Abaqus GUI with command execfile('writeNT11.py')
# write nodeLabel, coordinates, NT11 to an external file
# 

import numpy as np

#dummy odb file Job-2-Temps-Dummy.odb
odbFile = 'Job-2-Temps-Dummy.odb'

#Get number and name of steps
nSteps = session.odbs[odbFile].steps.keys()

for eachStep in nSteps:
  NT11 = session.odbs[odbFile].steps[eachStep].frames[1].fieldOutputs['NT11'].bulkDataBlocks
  numBlocks = len(NT11)
  for ii in range(numBlocks):
    nameBlock = NT11[ii].instance.name
    numNodes = len(NT11[ii].data)
    #labelNode = NT11[ii].nodeLabels
    labelNode = np.arange(1,numNodes+1)
    tempNode = np.concatenate(NT11[ii].data).ravel()
    outData = np.hstack(( np.atleast_2d(labelNode).T , np.atleast_2d(tempNode).T ))
    filename = nameBlock+"_"+eachStep+"-Frame-1-T.txt"
    np.savetxt(filename,outData,fmt = ['%10d','%10.4f'],delimiter=",")
    # Node coordinate export... easy way is to get COORD as an output field
  #end
#end

