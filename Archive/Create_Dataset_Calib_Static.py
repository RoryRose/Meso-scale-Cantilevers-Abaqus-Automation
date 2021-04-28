odb = session.odbs[ODBName]
xy0 = session.XYDataFromHistory(name='Data-1', odb=odb, 
    outputVariableName='Spatial displacement: U3 at Node 3 in NSET NEAR_END', 
    steps=('end', ), )
c0 = session.Curve(xyData=xy0)
xy1 = session.XYDataFromHistory(name='Data-2', odb=odb, 
    outputVariableName='Spatial displacement: U3 at Node 7 in NSET CENTER_OF_FREE_END', 
    steps=('nanoindenter', ), )
c1 = session.Curve(xyData=xy1)
xy2 = session.XYDataFromHistory(name='Data-3', odb=odb, 
    outputVariableName='Spatial displacement: U3 at Node 17 in NSET NEAR_DISK', 
    steps=('disk', ), )
c2 = session.Curve(xyData=xy2)
x0 = session.xyDataObjects['Data-1']
x1 = session.xyDataObjects['Data-2']
x2 = session.xyDataObjects['Data-3']
session.writeXYReport(fileName=RPTName+'.rpt', xyData=(x0, x1, x2))