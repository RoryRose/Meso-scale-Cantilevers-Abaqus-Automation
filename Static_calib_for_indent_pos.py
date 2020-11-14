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
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
pickedRegions = c.getSequenceFromMask(mask=('[#3ff ]', ), )
p.deleteMesh(regions=pickedRegions)
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
pickedCells = c.getSequenceFromMask(mask=('[#41 ]', ), )
e, v, d = p.edges, p.vertices, p.datums
p.PartitionCellByPlanePointNormal(normal=e[60], cells=pickedCells, 
    point=p.InterestingPoint(edge=e[60], rule=MIDDLE))
p = mdb.models['Model-1'].parts['Part-1']
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
p = mdb.models['Model-1'].parts['Part-1']
p.generateMesh()
elemType1 = mesh.ElemType(elemCode=C3D20R, elemLibrary=STANDARD)
elemType2 = mesh.ElemType(elemCode=C3D15, elemLibrary=STANDARD)
elemType3 = mesh.ElemType(elemCode=C3D10, elemLibrary=STANDARD)
p = mdb.models['Model-1'].parts['Part-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#3fff ]', ), )
pickedRegions =(cells, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
    elemType3))
a = mdb.models['Model-1'].rootAssembly
a.regenerate()
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=ON)
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.00469895, 
    farPlane=0.00712223, width=0.00188493, height=0.000775242, 
    viewOffsetX=0.000207475, viewOffsetY=-0.000125154)
mdb.models['Model-1'].StaticStep(name='near_disk', previous='Initial')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='near_disk')
mdb.models['Model-1'].StaticStep(name='middle', previous='near_disk')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='middle')
mdb.models['Model-1'].StaticStep(name='end', previous='middle')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='end')
del mdb.models['Model-1'].fieldOutputRequests['F-Output-1']
del mdb.models['Model-1'].historyOutputRequests['H-Output-1']
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='near_disk')
session.viewports['Viewport: 1'].partDisplay.setValues(mesh=OFF)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=OFF)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
p1 = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p1)
p = mdb.models['Model-1'].parts['Part-1']
v = p.vertices
verts = v.getSequenceFromMask(mask=('[#10000 ]', ), )
p.Set(vertices=verts, name='near-disk-node')
p = mdb.models['Model-1'].parts['Part-1']
v = p.vertices
verts = v.getSequenceFromMask(mask=('[#1 ]', ), )
p.Set(vertices=verts, name='near-end-node')
a = mdb.models['Model-1'].rootAssembly
a.regenerate()
session.viewports['Viewport: 1'].setValues(displayedObject=a)
regionDef=mdb.models['Model-1'].rootAssembly.allInstances['Part-1-1'].sets['near-disk-node']
mdb.models['Model-1'].HistoryOutputRequest(name='H-Output-1', 
    createStepName='near_disk', variables=('U3', ), region=regionDef, 
    sectionPoints=DEFAULT, rebar=EXCLUDE)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='middle')
regionDef=mdb.models['Model-1'].rootAssembly.sets['center_of_free_end']
mdb.models['Model-1'].HistoryOutputRequest(name='H-Output-2', 
    createStepName='middle', variables=('U3', ), region=regionDef, 
    sectionPoints=DEFAULT, rebar=EXCLUDE)
regionDef=mdb.models['Model-1'].rootAssembly.sets['center_of_free_end']
mdb.models['Model-1'].HistoryOutputRequest(name='H-Output-3', 
    createStepName='middle', variables=('U3', ), region=regionDef, 
    sectionPoints=DEFAULT, rebar=EXCLUDE)
del mdb.models['Model-1'].historyOutputRequests['H-Output-3']
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='end')
regionDef=mdb.models['Model-1'].rootAssembly.allInstances['Part-1-1'].sets['near-end-node']
mdb.models['Model-1'].HistoryOutputRequest(name='H-Output-3', 
    createStepName='end', variables=('U3', ), region=regionDef, 
    sectionPoints=DEFAULT, rebar=EXCLUDE)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, connectors=ON, adaptiveMeshConstraints=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='near_disk')
a = mdb.models['Model-1'].rootAssembly
region = a.instances['Part-1-1'].sets['near-disk-node']
mdb.models['Model-1'].ConcentratedForce(name='Load-1', 
    createStepName='near_disk', region=region, cf3=-1.0, 
    distributionType=UNIFORM, field='', localCsys=None)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='middle')
a = mdb.models['Model-1'].rootAssembly
region = a.sets['center_of_free_end']
mdb.models['Model-1'].ConcentratedForce(name='Load-2', createStepName='middle', 
    region=region, cf3=-1.0, distributionType=UNIFORM, field='', 
    localCsys=None)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='end')
a = mdb.models['Model-1'].rootAssembly
region = a.instances['Part-1-1'].sets['near-end-node']
mdb.models['Model-1'].ConcentratedForce(name='Load-3', createStepName='end', 
    region=region, cf3=-1.0, distributionType=UNIFORM, field='', 
    localCsys=None)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='near_disk')
a = mdb.models['Model-1'].rootAssembly
region = a.sets['encastre']
mdb.models['Model-1'].EncastreBC(name='BC-1', createStepName='near_disk', 
    region=region, localCsys=None)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='middle')
a = mdb.models['Model-1'].rootAssembly
region = a.sets['encastre']
mdb.models['Model-1'].EncastreBC(name='BC-2', createStepName='middle', 
    region=region, localCsys=None)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='end')
a = mdb.models['Model-1'].rootAssembly
region = a.sets['encastre']
mdb.models['Model-1'].EncastreBC(name='BC-3', createStepName='end', 
    region=region, localCsys=None)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
    predefinedFields=OFF, connectors=OFF)
mdb.Job(name='Job-1', model='Model-1', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
    numGPUs=0)