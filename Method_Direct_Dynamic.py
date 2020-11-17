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
#create sets for measuring angle#
p = mdb.models['Model-1'].parts['Part-1']
v = p.vertices
verts = v.getSequenceFromMask(mask=('[#2 ]','[#0 #8 ]', ), )
p.Set(vertices=verts, name='angle_measure')
a = mdb.models['Model-1'].rootAssembly
a.regenerate()
#create step#
mdb.models[ModelName].SteadyStateDirectStep(name=SName, previous='Initial', 
    frequencyRange=((MinFreq, MaxFreq, 2, 1.0), ))
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step=SName)
#delete automatic history output request#
del mdb.models[ModelName].historyOutputRequests['H-Output-1']
#create field output requests#
regionDef=mdb.models[ModelName].rootAssembly.sets[TopSetName]
mdb.models[ModelName].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'S', 'LE', 'U', 'V', 'A'), region=regionDef, sectionPoints=DEFAULT, 
    rebar=EXCLUDE)
regionDef=mdb.models['Model-1'].rootAssembly.allInstances['Inst-1'].sets['angle_measure']
mdb.models['Model-1'].FieldOutputRequest(name='free_angle', 
    createStepName='Direct_Dynamic', variables=('COORD', ), 
    region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)
#create BCs#
a = mdb.models[ModelName].rootAssembly
region = a.sets[EncName]
mdb.models[ModelName].DisplacementBC(name='BC-1', createStepName=SName, 
    region=region, u1=0+0j, u2=0+0j, u3=UNSET, ur1=UNSET, ur2=UNSET, 
    ur3=UNSET, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, 
    fieldName='', localCsys=None)
a = mdb.models[ModelName].rootAssembly
region = a.sets[EncName]
mdb.models[ModelName].DisplacementBC(name='BC-2', createStepName=SName, 
    region=region, u1=UNSET, u2=UNSET, u3=VertDisp+0j, ur1=UNSET, ur2=UNSET, 
    ur3=UNSET, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, 
    fieldName='', localCsys=None)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
    predefinedFields=OFF, connectors=OFF)
#create Job#
mdb.Job(name=JobName, model=ModelName, description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=NumCPUs, 
    numDomains=NumCPUs, numGPUs=0)
#create inp file#
mdb.jobs[JobName].writeInput(consistencyChecking=OFF)
