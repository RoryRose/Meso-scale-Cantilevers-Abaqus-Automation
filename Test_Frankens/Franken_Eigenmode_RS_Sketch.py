# -*- coding: mbcs -*-
# Do not delete the following import lines
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
import csv
import time
#set working directory#
AbqFDir = r"C:\Users\trin3150\Documents\Abaqus\liltemp" #directory location for abaqus to use (best if local)
os.chdir(AbqFDir)
filename = 'VariablesCSV.csv' #must be placed into the working directory of abaqus (AbqFDir)
#read the variables csv file#
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    NumOfColumns = len(header_row)
    NumOfTests = int(NumOfColumns-1)
    # print(NumOfTests)
#create variables from the csv file#
for i in range(1,NumOfTests+1):
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
    #initialise session - create new model and sketch#
    #new model created for each variable set in the csv file#
    mdb.Model(name=ModelName, modelType=STANDARD_EXPLICIT)
    session.viewports['Viewport: 1'].setValues(displayedObject=None)
    s = mdb.models[ModelName].ConstrainedSketch(name=ModelName, sheetSize=0.006)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.sketchOptions.setValues(decimalPlaces=4)
    s.setPrimaryObject(option=STANDALONE)
    #create constrained sketch starting from lines then adding dimensions and lines#
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
    s.Line(point1=(-0.0006, 0.0005), point2=(-0.0006, 0.000900000050477684))
    s.VerticalConstraint(entity=g[7], addUndoState=False)
    s.CoincidentConstraint(entity1=v[0], entity2=g[2])
    s.CoincidentConstraint(entity1=v[0], entity2=g[2])
    s.ArcByStartEndTangent(point1=(-0.000199999946542084, 0.000299999978020786), 
        point2=(-0.0006, 0.0005), entity=g[6])
    s.ObliqueDimension(vertex1=v[0], vertex2=v[1], textPoint=(0.00150307640433311, 
        0.000271040771622211), value=h2/2)
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
    s.DistanceDimension(entity1=v[5], entity2=g[2], textPoint=(
        -0.000490404781885445, 3.7224919651635e-05), value=h3/2)
    s.DistanceDimension(entity1=g[7], entity2=g[5], textPoint=(
        -0.000194330961676314, 0.0004374721320346), value=d3)
    s.FixedConstraint(entity=v[5])
    s.copyMirror(mirrorLine=g[2], objectList=(g[3], g[4], g[5], g[6], g[8], g[7]))
    s.delete(objectList=(c[27], ))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.00444508, 
        farPlane=0.00498302, width=0.00308612, height=0.00165849, 
        cameraPosition=(0.000404486, -7.53105e-007, 0.00471405), cameraTarget=(
        0.000404486, -7.53105e-007, 0))
    s.Arc3Points(point1=(-0.000499999971191242, 0.000600000050477684), point2=(
        -0.000499999971191242, -0.000600000050477684), point3=(-0.000775, 0.0))
    s.CoincidentConstraint(entity1=v[16], entity2=v[6])
    s.CoincidentConstraint(entity1=v[14], entity2=v[17])
    s.DistanceDimension(entity1=v[18], entity2=g[7], textPoint=(
            -0.000617911980953068, -6.11209543421865e-06), value=d4)
    s.RadialDimension(curve=g[15], textPoint=(-0.000789811310824007, 
        0.000176487024873495), radius=r2)
    s.CoincidentConstraint(entity1=v[18], entity2=g[2])
    #extrude sketch to create part
    p = mdb.models[ModelName].Part(name=PrtName, dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models[ModelName].parts[PrtName]
    
    p.BaseSolidExtrude(sketch=s, depth=t)
    s.unsetPrimaryObject()
    p = mdb.models[ModelName].parts[PrtName]
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models[ModelName].sketches[ModelName]
    #create the material from the imputted variable parameters#
    mdb.models[ModelName].Material(name='Material-1')
    mdb.models[ModelName].materials['Material-1'].Density(table=((dens, ), ))
    mdb.models[ModelName].materials['Material-1'].Elastic(table=((E, 
        PRat), ))    
    #create partitions for defining the nodal sets later to allow them to be defined by geometry rather than node number#
    #one partition along the beam and 5 accross the cantilever#
    #partitions defined by point and normal or extending face to make sure no nodes referenced explicitly#
    p1 = mdb.models[ModelName].parts[PrtName]
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p = mdb.models[ModelName].parts[PrtName]
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    e, v1, d1 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(normal=e[31], cells=pickedCells, 
        point=p.InterestingPoint(edge=e[31], rule=MIDDLE))
    p = mdb.models[ModelName].parts[PrtName]
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    e1, v2, d2 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(normal=e1[42], cells=pickedCells, 
        point=p.InterestingPoint(edge=e1[42], rule=MIDDLE))
    p = mdb.models[ModelName].parts[PrtName]
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#4 ]', ), )
    e, v1, d1 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(normal=e[17], cells=pickedCells, 
        point=p.InterestingPoint(edge=e[17], rule=MIDDLE))
    p = mdb.models[ModelName].parts[PrtName]
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    e1, v2, d2 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(normal=e1[39], cells=pickedCells, 
        point=p.InterestingPoint(edge=e1[59], rule=MIDDLE))
    p = mdb.models[ModelName].parts[PrtName]
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1f ]', ), )
    e, v1, d1 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(point=v1[37], normal=e[54], 
        cells=pickedCells)
    p = mdb.models[ModelName].parts[PrtName]
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#300 ]', ), )
    f = p.faces
    p.PartitionCellByExtendFace(extendFace=f[45], cells=pickedCells)
    p = mdb.models[ModelName].parts[PrtName]
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#b8a ]', ), )
    f1 = p.faces
    p.PartitionCellByExtendFace(extendFace=f1[55], cells=pickedCells)    
    #section whole part to be material 1#
    mdb.models[ModelName].HomogeneousSolidSection(name='Section-1', 
        material='Material-1', thickness=None)
    a = mdb.models[ModelName].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
    #create assembly from the part#
    a = mdb.models[ModelName].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models[ModelName].parts[PrtName]
    a.Instance(name=InstName, part=p, dependent=ON)
    #create useful sets#
    #sets created for: BC set on edge of disk, center of free end, top surface of the cantilever, whole part, sets for measuring angle#
    p1 = mdb.models[ModelName].parts[PrtName]
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p = mdb.models[ModelName].rootAssembly
    f = p.instances[InstName].faces
    faces = f.getSequenceFromMask(mask=('[#0 #4000004 ]', ), )
    p.Set(faces=faces, name=EncName)
    v = p.instances[InstName].vertices
    verts = v.getSequenceFromMask(mask=('[#10000000 ]', ), )
    p.Set(vertices=verts, name=CentFreeName)
    c = p.instances[InstName].cells
    cells = c.getSequenceFromMask(mask=('[#3fff ]', ), )
    p.Set(cells=cells, name='whole_prt')
    f = p.instances[InstName].faces
    faces = f.getSequenceFromMask(mask=('[#210 #22 ]', ), )
    p.Set(faces=faces, name=TopSetName)
    v = p.instances[InstName].vertices
    verts = v.getSequenceFromMask(mask=('[#80000000 ]', ), )
    p.Set(vertices=verts, name=EndFreeName)
    v = p.instances[InstName].vertices
    verts = v.getSequenceFromMask(mask=('[#200 ]', ), )
    p.Set(vertices=verts, name=DiskFreeName)
    c = p.instances[InstName].cells
    #section part#
    p = mdb.models[ModelName].parts[PrtName]
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#3fff ]', ), )
    region = p.Set(cells=cells, name='whole_part')
    p = mdb.models[ModelName].parts[PrtName]
    p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    #generate new mesh#
    #medial axis algorithm used to stop mesh errors when doing parametric analysis at the expense of computing time#
    #elements changed to be C3D20R#
    p = mdb.models[ModelName].parts[PrtName]
    p.seedPart(size=MeshSeedSize, deviationFactor=0.1, minSizeFactor=0.1)
    c = p.cells
    pickedRegions = c.getSequenceFromMask(mask=('[#3fff ]', ), )
    p.setMeshControls(regions=pickedRegions, algorithm=MEDIAL_AXIS)    
    p.generateMesh()
    elemType1 = mesh.ElemType(elemCode=C3D20R, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=C3D15, elemLibrary=STANDARD)
    elemType3 = mesh.ElemType(elemCode=C3D10, elemLibrary=STANDARD)

    cells = c.getSequenceFromMask(mask=('[#3fff ]', ), )
    pickedRegions =(cells, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
        elemType3))
    #create frequency step#
    mdb.models[ModelName].FrequencyStep(name=SName, previous='Initial', 
        numEigen=1)
    #create BCs#
    #encaster the edje of the disk#
    a = mdb.models[ModelName].rootAssembly
    region = a.sets[EncName]
    mdb.models[ModelName].EncastreBC(name='BC-1', createStepName=SName, 
        region=region, localCsys=None)
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
    #run job#
    mdb.jobs[JobName].submit(consistencyChecking=OFF)
    #wait for job to finish#
    mdb.jobs[JobName].waitForCompletion()
    #create xy data of the eigenfrequency for the whole model and save the data to a .rpt file#
    a = mdb.models[ModelName].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.mdbData.summary()
    o3 = session.openOdb(
        name=ODBName+JobName+'.odb')
    session.viewports['Viewport: 1'].setValues(displayedObject=o3)
    odb = session.odbs[JobName+'.odb']#odb = session.odbs[ODBName+JobName+'.odb']
    xy1 = session.XYDataFromHistory(name='Eigenfreq', odb=odb, 
        outputVariableName='Eigenfrequency: EIGFREQ for Whole Model', steps=(
        SName, ), )
    x0 = session.xyDataObjects['Eigenfreq']
    session.writeXYReport(fileName='rpt_eigenmode_'+JobName+'.rpt', xyData=(x0))
    #sleep for 2s to allow some time to prevent crashes#
    time.sleep(2)

