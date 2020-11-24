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
import csv
import time
# from datetime import datetime

# from matplotlib import pyplot as plt
#set working directory#
AbqFDir = r"C:\Users\trin3150\Documents\Abaqus\liltemp" #directory location for abaqus to use (best if local)
os.chdir(AbqFDir)
filename = 'VariablesCSV.csv' #must be placed into the working directory of abaqus (AbqFDir)
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    NumOfColumns = len(header_row)
    NumOfTests = int(NumOfColumns-1)
    # print(NumOfTests)

for i in range(1,NumOfTests):
    print("\nData column = %d" % i)
    with open(filename) as f:
        reader = csv.reader(f)
        variables, values = [], []
        for row in reader:
            # print(row)
            
            current_var = row[0]
            print(current_var)
            # variables.append(current_var)
            
            test_val = row[i]
            print(test_val)
            if len(test_val) > 0:
                if isinstance(test_val, float):
                    current_value = float(test_val)
                    exec("%s = %f" % (current_var,current_value))
                elif isinstance(test_val, str):
                    current_value = test_val
                    exec("%s = %s" % (current_var,current_value))
                    # values.append(current_value)
                elif isinstance(test_val, int):
                    current_value = test_val
                    exec("%s = %d" % (current_var,current_value))
                else:
                    exec("%s = %s" % (current_var,''))
            else:
                exec("%s = %s" % (current_var,''))
    #initialise session#
    mdb.Model(name=ModelName, modelType=STANDARD_EXPLICIT)
    session.viewports['Viewport: 1'].setValues(displayedObject=None)
    s = mdb.models[ModelName].ConstrainedSketch(name=ModelName, sheetSize=0.006)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.sketchOptions.setValues(decimalPlaces=4)
    s.setPrimaryObject(option=STANDALONE)
    #create sketch#
    s.ConstructionLine(point1=(-0.000275, 0.0), point2=(0.0, 0.0))
    s.HorizontalConstraint(entity=g[2], addUndoState=False)
    s.Line(point1=(0.001, 0.0), point2=(0.001, 0.000500000040978193))
    s.VerticalConstraint(entity=g[3], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[2], entity2=g[3], addUndoState=False)
    s.CoincidentConstraint(entity1=v[0], entity2=g[2], addUndoState=False)
    s.Line(point1=(0.001, 0.000500000040978193), point2=(0.000199999946542084, 
        0.000500000040978193))
    s.HorizontalConstraint(entity=g[4], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
    s.Line(point1=(0.000199999946542084, 0.000500000040978193), point2=(
        0.000199999946542086, 0.000299999978020787))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[4], entity2=g[5], addUndoState=False)
    s.Line(point1=(0.000199999946542086, 0.000299999978020787), point2=(
        -0.000199999946542084, 0.000299999978020786))
    s.HorizontalConstraint(entity=g[6], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[5], entity2=g[6], addUndoState=False)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.00432733, 
        farPlane=0.00510076, width=0.0044371, height=0.00238451, 
        cameraPosition=(0.000222518, -0.000264382, 0.00471405), cameraTarget=(
        0.000222518, -0.000264382, 0))
    s.Line(point1=(-0.0006, 0.0005), point2=(-0.0006, 0.000900000050477684))
    s.VerticalConstraint(entity=g[7], addUndoState=False)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.00446327, 
        farPlane=0.00496482, width=0.00254243, height=0.00136631, 
        cameraPosition=(0.000816576, -7.76535e-005, 0.00471405), cameraTarget=(
        0.000816576, -7.76535e-005, 0))
    s.CoincidentConstraint(entity1=v[0], entity2=g[2])
    s.CoincidentConstraint(entity1=v[0], entity2=g[2])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.00430264, 
        farPlane=0.00512545, width=0.00472032, height=0.00253671, 
        cameraPosition=(0.00169525, -0.0002707, 0.00471405), cameraTarget=(
        0.00169525, -0.0002707, 0))
    s.ArcByStartEndTangent(point1=(-0.000199999946542084, 0.000299999978020786), 
        point2=(-0.0006, 0.0005), entity=g[6])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.00418711, 
        farPlane=0.00524098, width=0.00604588, height=0.00324907, 
        cameraPosition=(0.00227586, -0.000336939, 0.00471405), cameraTarget=(
        0.00227586, -0.000336939, 0))
    s.ObliqueDimension(vertex1=v[0], vertex2=v[1], textPoint=(0.00150307640433311, 
        0.000271040771622211), value=h2/2)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.00418711, 
        farPlane=0.00524098, width=0.00534214, height=0.00287088, 
        cameraPosition=(0.0021428, -0.000269356, 0.00471405), cameraTarget=(
        0.0021428, -0.000269356, 0))
    s.ObliqueDimension(vertex1=v[1], vertex2=v[2], textPoint=(0.000699343276210129, 
        0.000803338829427958), value=d2)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.00439284, 
        farPlane=0.00503525, width=0.00325641, height=0.00175, cameraPosition=(
        0.00121375, -6.2817e-005, 0.00471405), cameraTarget=(0.00121375, 
        -6.2817e-005, 0))
    s.DistanceDimension(entity1=v[3], entity2=g[2], textPoint=(
        0.000447663362137973, 0.000127766688819975), value=h1/2)
    s.ObliqueDimension(vertex1=v[3], vertex2=v[4], textPoint=(5.98803162574768e-05, 
        0.00025412073591724), value=d1)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.00449064, 
        farPlane=0.00493745, width=0.00226492, height=0.00121717, 
        cameraPosition=(0.000547788, 0.00012291, 0.00471405), cameraTarget=(
        0.000547788, 0.00012291, 0))
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(0.000257903, 
        0.000124375, 0.00471405), cameraTarget=(0.000257903, 0.000124375, 0))
    s.DistanceDimension(entity1=v[5], entity2=g[2], textPoint=(
        -0.000490404781885445, 3.7224919651635e-05), value=h3/2)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.00451665, 
        farPlane=0.00491145, width=0.00226492, height=0.00121717, 
        cameraPosition=(0.000194848, 7.78864e-005, 0.00471405), cameraTarget=(
        0.000194848, 7.78864e-005, 0))
    s.DistanceDimension(entity1=g[7], entity2=g[5], textPoint=(
        -0.000194330961676314, 0.0004374721320346), value=d3)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.00449065, 
        farPlane=0.00493745, width=0.00226492, height=0.00121717, 
        cameraPosition=(0.0001934, 7.74268e-005, 0.00471405), cameraTarget=(
        0.0001934, 7.74268e-005, 0))
    s.FixedConstraint(entity=v[5])
    session.viewports['Viewport: 1'].view.setValues(width=0.00240949, 
        height=0.00129486, cameraPosition=(0.000164645, 6.88886e-005, 
        0.00471405), cameraTarget=(0.000164645, 6.88886e-005, 0))
    s.copyMirror(mirrorLine=g[2], objectList=(g[3], g[4], g[5], g[6], g[8], g[7]))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.00452849, 
        farPlane=0.00489961, width=0.00212902, height=0.00114414, 
        cameraPosition=(0.00011629, 6.14514e-005, 0.00471405), cameraTarget=(
        0.00011629, 6.14514e-005, 0))
    s.delete(objectList=(c[27], ))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.00444508, 
        farPlane=0.00498302, width=0.00308612, height=0.00165849, 
        cameraPosition=(0.000404486, -7.53105e-007, 0.00471405), cameraTarget=(
        0.000404486, -7.53105e-007, 0))
    s.Arc3Points(point1=(-0.000499999971191242, 0.000600000050477684), point2=(
        -0.000499999971191242, -0.000600000050477684), point3=(-0.000775, 0.0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.0051597, 
            farPlane=0.00523016, width=0.000231577, height=0.000150995, 
            cameraPosition=(-0.000437469, 0.000592363, 0.00519493), cameraTarget=(
            -0.000437469, 0.000592363, 0))
    s.CoincidentConstraint(entity1=v[16], entity2=v[6])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.00510653, 
        farPlane=0.00528333, width=0.000581073, height=0.000378878, 
        cameraPosition=(-0.000318599, -0.000388514, 0.00519493), cameraTarget=(
        -0.000318599, -0.000388514, 0))
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(-0.000324365, 
        -0.000537245, 0.00519493), cameraTarget=(-0.000324365, -0.000537245, 
        0))
    s.CoincidentConstraint(entity1=v[14], entity2=v[17])
    s.DistanceDimension(entity1=v[18], entity2=g[7], textPoint=(
            -0.000617911980953068, -6.11209543421865e-06), value=d4)
    s.RadialDimension(curve=g[15], textPoint=(-0.000789811310824007, 
        0.000176487024873495), radius=r2)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.00493921, 
        farPlane=0.0053339, width=0.00129724, height=0.000845841, 
        cameraPosition=(-0.000360502, 6.41261e-006, 0.00513656), cameraTarget=(
        -0.000360502, 6.41261e-006, 0))
    s.CoincidentConstraint(entity1=v[18], entity2=g[2])
    #extrude sketch#
    p = mdb.models[ModelName].Part(name=PrtName, dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models[ModelName].parts[PrtName]
    
    p.BaseSolidExtrude(sketch=s, depth=t)
    s.unsetPrimaryObject()
    p = mdb.models[ModelName].parts[PrtName]
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models[ModelName].sketches[ModelName]
    #create partitions#
    p = mdb.models[ModelName].parts[PrtName]
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    e, v1, d1 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(normal=e[10], cells=pickedCells, 
        point=p.InterestingPoint(edge=e[10], rule=MIDDLE))
    p = mdb.models[ModelName].parts[PrtName]
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#3 ]', ), )
    e1, v2, d2 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(normal=e1[27], cells=pickedCells, 
        point=p.InterestingPoint(edge=e1[27], rule=MIDDLE))
    p = mdb.models[ModelName].parts[PrtName]
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#9 ]', ), )
    e, v1, d1 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(normal=e[21], cells=pickedCells, 
        point=p.InterestingPoint(edge=e[41], rule=MIDDLE))
    p = mdb.models[ModelName].parts[PrtName]
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#f ]', ), )
    f = p.faces
    p.PartitionCellByExtendFace(extendFace=f[31], cells=pickedCells)
    p = mdb.models[ModelName].parts[PrtName]
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#a8 ]', ), )
    f1 = p.faces
    p.PartitionCellByExtendFace(extendFace=f1[29], cells=pickedCells)
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
        engineeringFeatures=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    #assign material#
    mdb.models[ModelName].Material(name='Material-1')
    mdb.models[ModelName].materials['Material-1'].Density(table=((dens, ), ))
    mdb.models[ModelName].materials['Material-1'].Elastic(table=((E, 
        PRat), ))
    #section part#
    mdb.models[ModelName].HomogeneousSolidSection(name='Section-1', 
        material='Material-1', thickness=None)
    del mdb.models[ModelName].sections['Section-1']
    mdb.models[ModelName].HomogeneousSolidSection(name='Section-1', 
        material='Material-1', thickness=None)
    a = mdb.models[ModelName].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
    #create assembly#
    a = mdb.models[ModelName].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models[ModelName].parts[PrtName]
    a.Instance(name=InstName, part=p, dependent=ON)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.00449812, 
        farPlane=0.00733091, width=0.00257805, height=0.00212468, 
        cameraPosition=(-0.0037457, 0.00262778, 0.00409448), cameraUpVector=(
        -0.17802, 0.407271, -0.895789), cameraTarget=(-0.000287169, 
        3.21561e-005, 1.49071e-005))
    #create useful sets#
    a = mdb.models[ModelName].rootAssembly
    f1 = a.instances[InstName].faces
    faces1 = f1.getSequenceFromMask(mask=('[#0 #1004 ]', ), )
    a.Set(faces=faces1, name=EncName)
    a = mdb.models[ModelName].rootAssembly
    v1 = a.instances[InstName].vertices
    verts1 = v1.getSequenceFromMask(mask=('[#8000000 ]', ), )
    a.Set(vertices=verts1, name=CentFreeName)
    a = mdb.models[ModelName].rootAssembly
    c1 = a.instances[InstName].cells
    cells1 = c1.getSequenceFromMask(mask=('[#3ff ]', ), )
    a.Set(cells=cells1, name='whole_prt')
    a = mdb.models[ModelName].rootAssembly
    f1 = a.instances[InstName].faces
    faces1 = f1.getSequenceFromMask(mask=('[#50048 ]', ), )
    a.Set(faces=faces1, name=TopSetName)
    p1 = mdb.models[ModelName].parts[PrtName]
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p = mdb.models[ModelName].parts[PrtName]
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#3ff ]', ), )
    region = p.Set(cells=cells, name=WholePrt)
    #section part#
    p = mdb.models[ModelName].parts[PrtName]
    p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
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
    p.seedPart(size=MeshSeedSize, deviationFactor=0.1, minSizeFactor=0.1)
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
    mdb.models[ModelName].StaticStep(name=SName, previous='Initial')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step=SName)
    #regenerate part#
    a.regenerate()
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    #create history output request#
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step=SName)
    regionDef=mdb.models[ModelName].rootAssembly.sets[CentFreeName]
    mdb.models[ModelName].HistoryOutputRequest(name='H-Output-2', 
        createStepName=SName, variables=('U3', ), region=regionDef, 
        sectionPoints=DEFAULT, rebar=EXCLUDE)
    #create forces#
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step=SName)
    a = mdb.models[ModelName].rootAssembly
    region = a.sets[CentFreeName]
    mdb.models[ModelName].ConcentratedForce(name='Load-2', createStepName=SName, 
        region=region, cf3=-1.0, distributionType=UNIFORM, field='', 
        localCsys=None)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step=SName)
    #create BCs#
    a = mdb.models[ModelName].rootAssembly
    region = a.sets[EncName]
    mdb.models[ModelName].EncastreBC(name='BC-2', createStepName=SName, 
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
    #run job#
    mdb.jobs[JobName].submit(consistencyChecking=OFF)#mdb.jobs['Job'+str(d[i])].submit(consistencyChecking=OFF)
    #wait for job to finish#
    mdb.jobs[JobName].waitForCompletion()#mdb.jobs['Job'+str(d[i])].waitForCompletion()
    
    #create xy data#
    a = mdb.models[ModelName].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.mdbData.summary()
    o3 = session.openOdb(
        name=ODBName+JobName+'.odb')
    session.viewports['Viewport: 1'].setValues(displayedObject=o3)
    odb = session.odbs[JobName+'.odb']#odb = session.odbs[ODBName+JobName+'.odb']
    xy1 = session.XYDataFromHistory(name='Data-1', odb=odb, 
        outputVariableName='Spatial displacement: U3 at Node 7 in NSET CENTER_OF_FREE_END', 
        steps=(SName, ), )
    c1 = session.Curve(xyData=xy1)
    #create output .rpt file#
    x0 = session.xyDataObjects['Data-1']
    session.writeXYReport(fileName=RPTName+'.rpt', xyData=(x0))
    time.sleep(2)# -*- coding: mbcs -*-
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
import csv
import time
# from datetime import datetime

# from matplotlib import pyplot as plt
#set working directory#
AbqFDir = r"C:\Users\trin3150\Documents\Abaqus\liltemp" #directory location for abaqus to use (best if local)
os.chdir(AbqFDir)
filename = 'VariablesCSV.csv' #must be placed into the working directory of abaqus (AbqFDir)
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    NumOfColumns = len(header_row)
    NumOfTests = int(NumOfColumns-1)
    # print(NumOfTests)

for i in range(1,NumOfTests):
    print("\nData column = %d" % i)
    with open(filename) as f:
        reader = csv.reader(f)
        variables, values = [], []
        for row in reader:
            # print(row)
            
            current_var = row[0]
            print(current_var)
            # variables.append(current_var)
            
            test_val = row[i]
            print(test_val)
            if len(test_val) > 0:
                if isinstance(test_val, float):
                    current_value = float(test_val)
                    exec("%s = %f" % (current_var,current_value))
                elif isinstance(test_val, str):
                    current_value = test_val
                    exec("%s = %s" % (current_var,current_value))
                    # values.append(current_value)
                elif isinstance(test_val, int):
                    current_value = test_val
                    exec("%s = %d" % (current_var,current_value))
                else:
                    exec("%s = %s" % (current_var,''))
            else:
                exec("%s = %s" % (current_var,''))
    #initialise session#
    mdb.Model(name=ModelName, modelType=STANDARD_EXPLICIT)
    session.viewports['Viewport: 1'].setValues(displayedObject=None)
    s = mdb.models[ModelName].ConstrainedSketch(name=ModelName, sheetSize=0.006)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    #create sketch#
    s.sketchOptions.setValues(decimalPlaces=4)
    s.setPrimaryObject(option=STANDALONE)
    s.Line(point1=(-0.0003, 0.0002), point2=(0.0, 0.0002))
    s.HorizontalConstraint(entity=g[2], addUndoState=False)
    s.Line(point1=(0.0, 0.0002), point2=(0.0, 0.0004))
    s.VerticalConstraint(entity=g[3], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[2], entity2=g[3], addUndoState=False)
    s.Line(point1=(0.0, 0.0004), point2=(0.0003, 
        0.0004))
    s.HorizontalConstraint(entity=g[4], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
    s.Line(point1=(0.0003, 0.0004), point2=(
        0.0003, -0.0002))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[4], entity2=g[5], addUndoState=False)
    s.Line(point1=(0.0003, -0.0002), point2=(0.0, 
        -0.0002))
    s.HorizontalConstraint(entity=g[6], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[5], entity2=g[6], addUndoState=False)
    s.Line(point1=(0.0, -0.0002), point2=(0.0, 
        -7.5e-05))
    s.VerticalConstraint(entity=g[7], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[6], entity2=g[7], addUndoState=False)
    s.Line(point1=(0.0, -7.5e-05), point2=(-0.0003, 
        -7.5e-05))
    s.HorizontalConstraint(entity=g[8], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[7], entity2=g[8], addUndoState=False)
    s.Arc3Points(point1=(-0.0003, 0.0002), point2=(-0.0005, 0.00035), point3=(
        -0.000425, 0.00025))
    s.Arc3Points(point1=(-0.0003, -7.5e-05), point2=(
        -0.0005, -0.0002), point3=(-0.000425, -0.0001))
    s.Line(point1=(-0.0005, 0.00035), point2=(-0.0005, 0.0007))
    s.VerticalConstraint(entity=g[11], addUndoState=False)
    s.Line(point1=(-0.0005, -0.0002), point2=(-0.0005, -0.0005))
    s.VerticalConstraint(entity=g[12], addUndoState=False)
    s.Arc3Points(point1=(-0.0005, -0.0005), point2=(-0.0005, 
        0.0007), point3=(-0.000775, 0.0))
    s.ConstructionLine(point1=(0.0, 0.0), point2=(5e-05, 0.0))
    s.HorizontalConstraint(entity=g[14], addUndoState=False)
    s.SymmetryConstraint(entity1=g[4], entity2=g[6], symmetryAxis=g[14])
    s.SymmetryConstraint(entity1=g[2], entity2=g[8], symmetryAxis=g[14])
    s.SymmetryConstraint(entity1=g[9], entity2=g[10], symmetryAxis=g[14])
    s.SymmetryConstraint(entity1=v[13], entity2=v[12], symmetryAxis=g[14])
    s.ObliqueDimension(vertex1=v[3], vertex2=v[4], textPoint=(0.0004, 
        1.4e-05), value=h2)
    s.ObliqueDimension(vertex1=v[4], vertex2=v[5], textPoint=(0.00012, 
        -0.0005), value=d2)
    s.DistanceDimension(entity1=g[2], entity2=g[8], textPoint=(
        -0.00013, -3.4e-06), value=d1)
    s.DistanceDimension(entity1=g[11], entity2=g[3], textPoint=(6e-07, 0.0), 
        value=d3)
    s.DistanceDimension(entity1=v[14], entity2=g[12], textPoint=(
        -0.00068, -0.0002), value=d4)
    s.RadialDimension(curve=g[13], textPoint=(-0.0008, 
        0.0007), radius=r2)
    s.TangentConstraint(entity1=g[9], entity2=g[2])
    s.RadialDimension(curve=g[9], textPoint=(-0.0005, 
        0.0003), radius=r1)
    s.dragEntity(entity=v[9], points=((-0.00106096395802383, 0.000567404644683332), 
        (-0.00105, 0.000575), (-0.0008, 0.000375), (-0.000625, 0.00025), (
        -0.00055, 0.000225)))
    s.dragEntity(entity=v[11], points=((-0.001136249659634, -0.000296156967864238), 
        (-0.001125, -0.0003), (-0.000725, -0.000125), (-0.000575, -7.5e-05), (
        -0.00055, -7.5e-05)))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.00436022, 
        farPlane=0.00506787, width=0.00263219, height=0.00225061, 
        cameraPosition=(0.000328496, 0.000331514, 0.00471405), cameraTarget=(
        0.000328496, 0.000331514, 0))
    s.undo()
    s.undo()
    s.undo()
    s.ObliqueDimension(vertex1=v[0], vertex2=v[1], textPoint=(
        -0.00037, 0.0003), value=d1)
    s.RadialDimension(curve=g[9], textPoint=(-0.0006, 
        0.0004), radius=r1)
    s.dragEntity(entity=v[9], points=((-0.000970904952102452, 
        0.000316688240342015), (-0.000975, 0.000325), (-0.000775, 0.0002), (
        -0.000675, 0.00015), (-0.00065, 0.00015)))
    s.dragEntity(entity=v[11], points=((-0.000897071345175977, 
        -0.000221790082393968), (-0.0009, -0.000225), (-0.000675, -0.00015), (
        -0.000625, -0.000125)))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.00405714, 
        farPlane=0.00537095, width=0.00431811, height=0.00369213, 
        cameraPosition=(0.000859323, 0.000700032, 0.00471405), cameraTarget=(
        0.000859323, 0.000700032, 0))
    #extrude sketch#
    p = mdb.models[ModelName].Part(name=PrtName, dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models[ModelName].parts[PrtName]
    
    p.BaseSolidExtrude(sketch=s, depth=t)
    s.unsetPrimaryObject()
    p = mdb.models[ModelName].parts[PrtName]
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models[ModelName].sketches[ModelName]
    #create partitions#
    p = mdb.models[ModelName].parts[PrtName]
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    e, v1, d1 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(normal=e[10], cells=pickedCells, 
        point=p.InterestingPoint(edge=e[10], rule=MIDDLE))
    p = mdb.models[ModelName].parts[PrtName]
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#3 ]', ), )
    e1, v2, d2 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(normal=e1[27], cells=pickedCells, 
        point=p.InterestingPoint(edge=e1[27], rule=MIDDLE))
    p = mdb.models[ModelName].parts[PrtName]
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#9 ]', ), )
    e, v1, d1 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(normal=e[21], cells=pickedCells, 
        point=p.InterestingPoint(edge=e[41], rule=MIDDLE))
    p = mdb.models[ModelName].parts[PrtName]
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#f ]', ), )
    f = p.faces
    p.PartitionCellByExtendFace(extendFace=f[31], cells=pickedCells)
    p = mdb.models[ModelName].parts[PrtName]
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#a8 ]', ), )
    f1 = p.faces
    p.PartitionCellByExtendFace(extendFace=f1[29], cells=pickedCells)
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
        engineeringFeatures=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    #assign material#
    mdb.models[ModelName].Material(name='Material-1')
    mdb.models[ModelName].materials['Material-1'].Density(table=((dens, ), ))
    mdb.models[ModelName].materials['Material-1'].Elastic(table=((E, 
        PRat), ))
    #section part#
    mdb.models[ModelName].HomogeneousSolidSection(name='Section-1', 
        material='Material-1', thickness=None)
    del mdb.models[ModelName].sections['Section-1']
    mdb.models[ModelName].HomogeneousSolidSection(name='Section-1', 
        material='Material-1', thickness=None)
    a = mdb.models[ModelName].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
    #create assembly#
    a = mdb.models[ModelName].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models[ModelName].parts[PrtName]
    a.Instance(name=InstName, part=p, dependent=ON)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.00449812, 
        farPlane=0.00733091, width=0.00257805, height=0.00212468, 
        cameraPosition=(-0.0037457, 0.00262778, 0.00409448), cameraUpVector=(
        -0.17802, 0.407271, -0.895789), cameraTarget=(-0.000287169, 
        3.21561e-005, 1.49071e-005))
    #create useful sets#
    a = mdb.models[ModelName].rootAssembly
    f1 = a.instances[InstName].faces
    faces1 = f1.getSequenceFromMask(mask=('[#0 #1004 ]', ), )
    a.Set(faces=faces1, name=EncName)
    a = mdb.models[ModelName].rootAssembly
    v1 = a.instances[InstName].vertices
    verts1 = v1.getSequenceFromMask(mask=('[#8000000 ]', ), )
    a.Set(vertices=verts1, name=CentFreeName)
    a = mdb.models[ModelName].rootAssembly
    c1 = a.instances[InstName].cells
    cells1 = c1.getSequenceFromMask(mask=('[#3ff ]', ), )
    a.Set(cells=cells1, name='whole_prt')
    a = mdb.models[ModelName].rootAssembly
    f1 = a.instances[InstName].faces
    faces1 = f1.getSequenceFromMask(mask=('[#50048 ]', ), )
    a.Set(faces=faces1, name=TopSetName)
    p1 = mdb.models[ModelName].parts[PrtName]
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p = mdb.models[ModelName].parts[PrtName]
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#3ff ]', ), )
    region = p.Set(cells=cells, name=WholePrt)
    #section part#
    p = mdb.models[ModelName].parts[PrtName]
    p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
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
    p.seedPart(size=MeshSeedSize, deviationFactor=0.1, minSizeFactor=0.1)
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
    mdb.models[ModelName].StaticStep(name=SName, previous='Initial')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step=SName)
    #regenerate part#
    a.regenerate()
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    #create history output request#
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step=SName)
    regionDef=mdb.models[ModelName].rootAssembly.sets[CentFreeName]
    mdb.models[ModelName].HistoryOutputRequest(name='H-Output-2', 
        createStepName=SName, variables=('U3', ), region=regionDef, 
        sectionPoints=DEFAULT, rebar=EXCLUDE)
    #create forces#
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step=SName)
    a = mdb.models[ModelName].rootAssembly
    region = a.sets[CentFreeName]
    mdb.models[ModelName].ConcentratedForce(name='Load-2', createStepName=SName, 
        region=region, cf3=-1.0, distributionType=UNIFORM, field='', 
        localCsys=None)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step=SName)
    #create BCs#
    a = mdb.models[ModelName].rootAssembly
    region = a.sets[EncName]
    mdb.models[ModelName].EncastreBC(name='BC-2', createStepName=SName, 
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
    #run job#
    mdb.jobs[JobName].submit(consistencyChecking=OFF)#mdb.jobs['Job'+str(d[i])].submit(consistencyChecking=OFF)
    #wait for job to finish#
    mdb.jobs[JobName].waitForCompletion()#mdb.jobs['Job'+str(d[i])].waitForCompletion()
    
    #create xy data#
    a = mdb.models[ModelName].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.mdbData.summary()
    o3 = session.openOdb(
        name=ODBName+JobName+'.odb')
    session.viewports['Viewport: 1'].setValues(displayedObject=o3)
    odb = session.odbs[JobName+'.odb']#odb = session.odbs[ODBName+JobName+'.odb']
    xy1 = session.XYDataFromHistory(name='Data-1', odb=odb, 
        outputVariableName='Spatial displacement: U3 at Node 7 in NSET CENTER_OF_FREE_END', 
        steps=(SName, ), )
    c1 = session.Curve(xyData=xy1)
    #create output .rpt file#
    x0 = session.xyDataObjects['Data-1']
    session.writeXYReport(fileName=RPTName+'.rpt', xyData=(x0))
    time.sleep(2)