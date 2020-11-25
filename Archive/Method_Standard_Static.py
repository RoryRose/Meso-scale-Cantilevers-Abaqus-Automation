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
    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=NumCPUs, 
    numDomains=NumCPUs, numGPUs=0)
#create inp file#
mdb.jobs[JobName].writeInput(consistencyChecking=OFF)
