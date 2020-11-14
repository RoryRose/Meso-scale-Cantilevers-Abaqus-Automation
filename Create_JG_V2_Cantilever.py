# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

def JG_CantV2_Test_1():
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
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=0.005)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.sketchOptions.setValues(decimalPlaces=4)
    s.setPrimaryObject(option=STANDALONE)
    s.Line(point1=(-0.0003, 0.0002), point2=(0.0, 0.0002))
    s.HorizontalConstraint(entity=g[2], addUndoState=False)
    s.Line(point1=(0.0, 0.0002), point2=(0.0, 0.00040000000949949))
    s.VerticalConstraint(entity=g[3], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[2], entity2=g[3], addUndoState=False)
    s.Line(point1=(0.0, 0.00040000000949949), point2=(0.000299999978020787, 
        0.00040000000949949))
    s.HorizontalConstraint(entity=g[4], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
    s.Line(point1=(0.000299999978020787, 0.00040000000949949), point2=(
        0.000299999978020786, -0.000199999946542084))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[4], entity2=g[5], addUndoState=False)
    s.Line(point1=(0.000299999978020786, -0.000199999946542084), point2=(0.0, 
        -0.000199999946542086))
    s.HorizontalConstraint(entity=g[6], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[5], entity2=g[6], addUndoState=False)
    s.Line(point1=(0.0, -0.000199999946542086), point2=(0.0, 
        -7.50000527128577e-05))
    s.VerticalConstraint(entity=g[7], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[6], entity2=g[7], addUndoState=False)
    s.Line(point1=(0.0, -7.50000527128577e-05), point2=(-0.000299999978020787, 
        -7.50000527128591e-05))
    s.HorizontalConstraint(entity=g[8], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[7], entity2=g[8], addUndoState=False)
    s.Arc3Points(point1=(-0.0003, 0.0002), point2=(-0.0005, 0.00035), point3=(
        -0.000425, 0.00025))
    s.Arc3Points(point1=(-0.000299999978020787, -7.50000527128591e-05), point2=(
        -0.0005, -0.0002), point3=(-0.000425, -0.0001))
    s.Line(point1=(-0.0005, 0.00035), point2=(-0.0005, 0.000699999987520278))
    s.VerticalConstraint(entity=g[11], addUndoState=False)
    s.Line(point1=(-0.0005, -0.0002), point2=(-0.0005, -0.000500000040978193))
    s.VerticalConstraint(entity=g[12], addUndoState=False)
    s.Arc3Points(point1=(-0.0005, -0.000500000040978193), point2=(-0.0005, 
        0.000699999987520278), point3=(-0.000775, 0.0))
    s.ConstructionLine(point1=(0.0, 0.0), point2=(4.99999575316906e-05, 0.0))
    s.HorizontalConstraint(entity=g[14], addUndoState=False)
    s.SymmetryConstraint(entity1=g[4], entity2=g[6], symmetryAxis=g[14])
    s.SymmetryConstraint(entity1=g[2], entity2=g[8], symmetryAxis=g[14])
    s.SymmetryConstraint(entity1=g[9], entity2=g[10], symmetryAxis=g[14])
    s.SymmetryConstraint(entity1=v[13], entity2=v[12], symmetryAxis=g[14])
    s.ObliqueDimension(vertex1=v[3], vertex2=v[4], textPoint=(0.000384744140319526, 
        1.46774691529572e-05), value=0.001)
    s.ObliqueDimension(vertex1=v[4], vertex2=v[5], textPoint=(0.000154574634507298, 
        -0.000504677416756749), value=6e-07)
    s.undo()
    s.ObliqueDimension(vertex1=v[4], vertex2=v[5], textPoint=(0.000122982659377158, 
        -0.000495645101182163), value=0.0006)
    s.DistanceDimension(entity1=g[2], entity2=g[8], textPoint=(
        -0.000136522052343935, -3.38704558089376e-06), value=0.0002)
    s.DistanceDimension(entity1=g[11], entity2=g[3], textPoint=(6e-07, 0.0), 
        value=0.0006)
    s.DistanceDimension(entity1=v[14], entity2=g[12], textPoint=(
        -0.000687123625539243, -0.000208870915230364), value=0.0004)
    s.RadialDimension(curve=g[13], textPoint=(-0.000829287222586572, 
        0.000719193543773144), radius=0.002)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.00413596, 
        farPlane=0.00529213, width=0.00379994, height=0.00324907, 
        cameraPosition=(0.000622389, 0.000417702, 0.00471405), cameraTarget=(
        0.000622389, 0.000417702, 0))
    s.TangentConstraint(entity1=g[9], entity2=g[2])
    s.RadialDimension(curve=g[9], textPoint=(-0.000515078252647072, 
        0.000361105136107653), radius=0.0018)
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
        -0.000375258561689407, 0.00035329454112798), value=0.0003)
    s.RadialDimension(curve=g[9], textPoint=(-0.00061322923284024, 
        0.000385238672606647), radius=0.0009)
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
    p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['Part-1']
    p.BaseSolidExtrude(sketch=s, depth=0.000125)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['Part-1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']
    p = mdb.models['Model-1'].parts['Part-1']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    e, v1, d1 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(normal=e[10], cells=pickedCells, 
        point=p.InterestingPoint(edge=e[10], rule=MIDDLE))
    p = mdb.models['Model-1'].parts['Part-1']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#3 ]', ), )
    e1, v2, d2 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(normal=e1[27], cells=pickedCells, 
        point=p.InterestingPoint(edge=e1[27], rule=MIDDLE))
    p = mdb.models['Model-1'].parts['Part-1']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#9 ]', ), )
    e, v1, d1 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(normal=e[21], cells=pickedCells, 
        point=p.InterestingPoint(edge=e[41], rule=MIDDLE))
    p = mdb.models['Model-1'].parts['Part-1']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#f ]', ), )
    f = p.faces
    p.PartitionCellByExtendFace(extendFace=f[31], cells=pickedCells)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.00463493, 
        farPlane=0.0071823, width=0.00265646, height=0.0021893, 
        cameraPosition=(-0.00346862, 0.002082, 0.00459946), cameraUpVector=(
        -0.165887, 0.572168, -0.803184), cameraTarget=(-0.000287169, 
        3.21562e-005, 1.49071e-005))
    p = mdb.models['Model-1'].parts['Part-1']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#a8 ]', ), )
    f1 = p.faces
    p.PartitionCellByExtendFace(extendFace=f1[29], cells=pickedCells)
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
        engineeringFeatures=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    mdb.models['Model-1'].Material(name='Material-1')
    mdb.models['Model-1'].materials['Material-1'].Density(table=((8000.0, ), ))
    mdb.models['Model-1'].materials['Material-1'].Elastic(table=((200000000000.0, 
        0.29), ))
    mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', 
        material='Material-1', thickness=None)
    del mdb.models['Model-1'].sections['Section-1']
    mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', 
        material='Material-1', thickness=None)
    a = mdb.models['Model-1'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
    a = mdb.models['Model-1'].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models['Model-1'].parts['Part-1']
    a.Instance(name='Part-1-1', part=p, dependent=ON)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.00449812, 
        farPlane=0.00733091, width=0.00257805, height=0.00212468, 
        cameraPosition=(-0.0037457, 0.00262778, 0.00409448), cameraUpVector=(
        -0.17802, 0.407271, -0.895789), cameraTarget=(-0.000287169, 
        3.21561e-005, 1.49071e-005))
    a = mdb.models['Model-1'].rootAssembly
    f1 = a.instances['Part-1-1'].faces
    faces1 = f1.getSequenceFromMask(mask=('[#0 #1004 ]', ), )
    a.Set(faces=faces1, name='encastre')
    a = mdb.models['Model-1'].rootAssembly
    v1 = a.instances['Part-1-1'].vertices
    verts1 = v1.getSequenceFromMask(mask=('[#8000000 ]', ), )
    a.Set(vertices=verts1, name='center of tongue')
    a = mdb.models['Model-1'].rootAssembly
    c1 = a.instances['Part-1-1'].cells
    cells1 = c1.getSequenceFromMask(mask=('[#3ff ]', ), )
    a.Set(cells=cells1, name='whole_prt')
    a = mdb.models['Model-1'].rootAssembly
    f1 = a.instances['Part-1-1'].faces
    faces1 = f1.getSequenceFromMask(mask=('[#50048 ]', ), )
    a.Set(faces=faces1, name='Cant_top_set')
    p1 = mdb.models['Model-1'].parts['Part-1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p = mdb.models['Model-1'].parts['Part-1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#3ff ]', ), )
    region = p.Set(cells=cells, name='whole_prt')
    p = mdb.models['Model-1'].parts['Part-1']
    p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)


