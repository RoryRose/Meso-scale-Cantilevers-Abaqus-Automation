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
#delete old mesh#
p = mdb.models[ModelName].parts[PrtName]
c = p.cells
pickedRegions = c.getSequenceFromMask(mask=('[#3ff ]', ), )
p.deleteMesh(regions=pickedRegions)
p = mdb.models[ModelName].parts[PrtName]
c = p.cells
#create new partitions#
pickedCells = c.getSequenceFromMask(mask=('[#41 ]', ), )
e, v, d = p.edges, p.vertices, p.datums
p.PartitionCellByPlanePointNormal(normal=e[60], cells=pickedCells, 
    point=p.InterestingPoint(edge=e[60], rule=MIDDLE))
p = mdb.models[ModelName].parts[PrtName]
c = p.cells
pickedCells = c.getSequenceFromMask(mask=('[#c00 ]', ), )
e1, v1, d1 = p.edges, p.vertices, p.datums
p.PartitionCellByPlanePointNormal(normal=e1[84], cells=pickedCells, 
    point=p.InterestingPoint(edge=e1[84], rule=MIDDLE))
session.viewports['Viewport: 1'].partDisplay.setValues(mesh=ON)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
#create undeformable material#
mdb.models[ModelName].Material(name='Material-2')
mdb.models[ModelName].materials['Material-2'].Density(table=((dens, ), ))
mdb.models[ModelName].materials['Material-2'].Elastic(table=((2e+15, PRat), ))
#delete old section assignment#
del mdb.models[ModelName].parts[PrtName].sectionAssignments[0]
#create new section assignment#
mdb.models[ModelName].HomogeneousSolidSection(name='Section-2', 
    material='Material-2', thickness=None)
p = mdb.models[ModelName].parts[PrtName]
c = p.cells
cells = c.getSequenceFromMask(mask=('[#202f ]', ), )
region = p.Set(cells=cells, name='Undeformable-mat')
p = mdb.models[ModelName].parts[PrtName]
p.SectionAssignment(region=region, sectionName='Section-2', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
p = mdb.models[ModelName].parts[PrtName]
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1fd0 ]', ), )
region = p.Set(cells=cells, name='deformable-mat')
p = mdb.models[ModelName].parts[PrtName]
p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
#generate new mesh#
p = mdb.models[ModelName].parts[PrtName]
p.generateMesh()
elemType1 = mesh.ElemType(elemCode=C3D20R, elemLibrary=STANDARD)
elemType2 = mesh.ElemType(elemCode=C3D15, elemLibrary=STANDARD)
elemType3 = mesh.ElemType(elemCode=C3D10, elemLibrary=STANDARD)
p = mdb.models[ModelName].parts[PrtName]
c = p.cells
cells = c.getSequenceFromMask(mask=('[#3fff ]', ), )
pickedRegions =(cells, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
    elemType3))
#create steps#
a = mdb.models[ModelName].rootAssembly
a.regenerate()
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=ON)
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.00469895, 
    farPlane=0.00712223, width=0.00188493, height=0.000775242, 
    viewOffsetX=0.000207475, viewOffsetY=-0.000125154)
mdb.models[ModelName].StaticStep(name=SName2, previous='Initial')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step=SName2)
mdb.models[ModelName].StaticStep(name=SName, previous=SName2)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step=SName)
mdb.models[ModelName].StaticStep(name=SName3, previous=SName)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step=SName3)
##delete automatically created output requests#
#del mdb.models[ModelName].fieldOutputRequests['F-Output-1']
#del mdb.models[ModelName].historyOutputRequests['H-Output-1']
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step=SName2)
session.viewports['Viewport: 1'].partDisplay.setValues(mesh=OFF)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=OFF)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
p1 = mdb.models[ModelName].parts[PrtName]
session.viewports['Viewport: 1'].setValues(displayedObject=p1)
#create sets#
p = mdb.models[ModelName].parts[PrtName]
v = p.vertices
verts = v.getSequenceFromMask(mask=('[#10000 ]', ), )
p.Set(vertices=verts, name=DiskFreeName)
p = mdb.models[ModelName].parts[PrtName]
v = p.vertices
verts = v.getSequenceFromMask(mask=('[#1 ]', ), )
p.Set(vertices=verts, name=EndFreeName)
a = mdb.models[ModelName].rootAssembly
#regenerate part#
a.regenerate()
session.viewports['Viewport: 1'].setValues(displayedObject=a)
#create history output request#
regionDef=mdb.models[ModelName].rootAssembly.allInstances[InstName].sets[DiskFreeName]
mdb.models[ModelName].HistoryOutputRequest(name='H-Output-1', 
    createStepName=SName2, variables=('U3', ), region=regionDef, 
    sectionPoints=DEFAULT, rebar=EXCLUDE)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step=SName)
regionDef=mdb.models[ModelName].rootAssembly.sets[CentFreeName]
mdb.models[ModelName].HistoryOutputRequest(name='H-Output-2', 
    createStepName=SName, variables=('U3', ), region=regionDef, 
    sectionPoints=DEFAULT, rebar=EXCLUDE)
regionDef=mdb.models[ModelName].rootAssembly.allInstances[InstName].sets[EndFreeName]
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step=SName3)
regionDef=mdb.models[ModelName].rootAssembly.allInstances[InstName].sets[EndFreeName]
mdb.models[ModelName].HistoryOutputRequest(name='H-Output-3', 
    createStepName=SName3, variables=('U3', ), region=regionDef, 
    sectionPoints=DEFAULT, rebar=EXCLUDE)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, connectors=ON, adaptiveMeshConstraints=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step=SName2)
#create forces#
a = mdb.models[ModelName].rootAssembly
region = a.instances[InstName].sets[DiskFreeName]
mdb.models[ModelName].ConcentratedForce(name='Load-1', 
    createStepName=SName2, region=region, cf3=-1.0, 
    distributionType=UNIFORM, field='', localCsys=None)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step=SName)
a = mdb.models[ModelName].rootAssembly
region = a.sets[CentFreeName]
mdb.models[ModelName].ConcentratedForce(name='Load-2', createStepName=SName, 
    region=region, cf3=-1.0, distributionType=UNIFORM, field='', 
    localCsys=None)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step=SName3)
a = mdb.models[ModelName].rootAssembly
region = a.instances[InstName].sets[EndFreeName]
mdb.models[ModelName].ConcentratedForce(name='Load-3', createStepName=SName3, 
    region=region, cf3=-1.0, distributionType=UNIFORM, field='', 
    localCsys=None)
#create BC's#
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step=SName2)
a = mdb.models[ModelName].rootAssembly
region = a.sets[EncName]
mdb.models[ModelName].EncastreBC(name='BC-1', createStepName=SName2, 
    region=region, localCsys=None)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step=SName)
a = mdb.models[ModelName].rootAssembly
region = a.sets[EncName]
mdb.models[ModelName].EncastreBC(name='BC-2', createStepName=SName, 
    region=region, localCsys=None)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step=SName3)
a = mdb.models[ModelName].rootAssembly
region = a.sets[EncName]
mdb.models[ModelName].EncastreBC(name='BC-3', createStepName=SName3, 
    region=region, localCsys=None)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
    predefinedFields=OFF, connectors=OFF)
#create job#
mdb.Job(name=JobName, model=ModelName, description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=NumCPUs, 
    numDomains=NumCPUs, numGPUs=0)
#create inp file#
mdb.jobs[JobName].writeInput(consistencyChecking=OFF)
