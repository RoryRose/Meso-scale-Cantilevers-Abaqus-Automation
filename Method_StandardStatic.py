# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__
#set names
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior

## Importing User Variables ##

import InputVarMacro
InputVarMacro.InputVarMacro()

# import csv
# filename = 'VariablesCSV.csv'
# with open(filename) as f:
#     reader = csv.reader(f)
#     header_row = next(reader)
#     print(header_row)

# import csv
# with open('VariablesCSV.csv', newline='') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         print(row['first_name'], row['last_name'])



## Generating Model ##

import Assembly_JG_V2_Cantilever
Assembly_JG_V2_Cantilever.Assembly_JG_V2_Cantilever()

## Method Specficic Step ##
a = mdb.models[ModelName].rootAssembly
a.regenerate()
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=ON)
#create step#
mdb.models[ModelName].StaticStep(name=SName, previous='Initial')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step=SName)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, connectors=ON, adaptiveMeshConstraints=OFF)
a = mdb.models[ModelName].rootAssembly
#create force#
region = a.sets[CentFreeName]
mdb.models[ModelName].ConcentratedForce(name=ForceName, 
    createStepName=SName, region=region, cf3=-1.0, 
    distributionType=UNIFORM, field='', localCsys=None)
a = mdb.models[ModelName].rootAssembly
#create BCs#
region = a.sets[EncName]
mdb.models[ModelName].EncastreBC(name='BC-1', createStepName=SName, 
    region=region, localCsys=None)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
    predefinedFields=OFF, connectors=OFF, adaptiveMeshConstraints=ON)
#delete auto-generated output requests#
del mdb.models[ModelName].fieldOutputRequests['F-Output-1']
del mdb.models[ModelName].historyOutputRequests['H-Output-1']
#create history output request for displacement at the nanoindenter#
regionDef=mdb.models[ModelName].rootAssembly.sets[CentFreeName]
mdb.models[ModelName].HistoryOutputRequest(name='H-Output-1', 
    createStepName=SName, variables=('U3', ), region=regionDef, 
    sectionPoints=DEFAULT, rebar=EXCLUDE)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=OFF)
#create job#
mdb.Job(name=JobName, model=ModelName, description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
    numGPUs=0)
