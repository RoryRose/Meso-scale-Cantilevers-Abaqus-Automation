## Saving At End
#save database#
mdb.saveAs(pathName='C:/Users/trin3150/Documents/Abaqus/liltemp/ModelName-2')
#create inp file#
mdb.jobs[JobName].writeInput(consistencyChecking=OFF)