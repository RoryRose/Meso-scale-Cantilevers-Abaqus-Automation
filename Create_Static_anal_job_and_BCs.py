#import#
from abaqus import *
from abaqusConstants import *
import __main__
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
a = mdb.models['Model-1'].rootAssembly
a.regenerate()
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=ON)
#create step#
mdb.models['Model-1'].StaticStep(name=SName, previous='Initial')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step=SName)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, connectors=ON, adaptiveMeshConstraints=OFF)
a = mdb.models['Model-1'].rootAssembly
#create force#
region = a.sets[IndentLocName]
mdb.models['Model-1'].ConcentratedForce(name=ForceName, 
    createStepName=SName, region=region, cf3=-1.0, 
    distributionType=UNIFORM, field='', localCsys=None)
a = mdb.models['Model-1'].rootAssembly
#create BCs#
region = a.sets[EncName]
mdb.models['Model-1'].EncastreBC(name='BC-1', createStepName=SName, 
    region=region, localCsys=None)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
    predefinedFields=OFF, connectors=OFF, adaptiveMeshConstraints=ON)
#delete auto-generated output requests#
del mdb.models['Model-1'].fieldOutputRequests['F-Output-1']
del mdb.models['Model-1'].historyOutputRequests['H-Output-1']
#create history output request for displacement at the nanoindenter#
regionDef=mdb.models['Model-1'].rootAssembly.sets[IndentLocName]
mdb.models['Model-1'].HistoryOutputRequest(name='H-Output-1', 
    createStepName=SName, variables=('U3', ), region=regionDef, 
    sectionPoints=DEFAULT, rebar=EXCLUDE)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=OFF)
#create job#
mdb.Job(name=JobName, model='Model-1', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
    numGPUs=0)