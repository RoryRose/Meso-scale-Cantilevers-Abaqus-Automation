def InputVarMacro():
    #List of all variables used#
    global d1,d2,d3,d4,h1,h2,r1,r2,t,E,dens,PRat,EncName,TopSetName,CentFreeName,WholePrt,MeshSeedSize,SName,ForceName,JobName,IndentLocName,ModelName,PrtName,InstName,MinFreq,MaxFreq,VertDisp,SName2,SName3,DiskFreeName,EndFreeName
    d1 = 0.0003 #length of cantilever between arc and end block
    d2 = 0.0006 #length of end block
    d3 = 0.0006 #length of cantilever between built in and free end
    d4 = 0.0004 #width of disk arc
    h1 = 0.0002 #width of cantilever
    h2 = 0.001 #width of free end
    r1 = 0.0009 #radius of cantilever arc
    r2 = 0.002 #radius of disc
    t = 0.000125 #thickness of sheet
    E = 200000000000 #material elastic modulus
    dens = 8000 #material density
    PRat = 0.29 #material poissons ratio
    EncName = 'encastre' #name of encarcarate BC set
    TopSetName = 'Cant_top_set' #name of set for top of cantilever surface
    CentFreeName = 'center_of_free_end' #name of set for center of free end (nanoindent location)
    WholePrt = 'Whole-Part' #name of set for the whole part
    MeshSeedSize = 2e-05 #size of mesh seed
    SName = 'nanoindenter' #name of loading step
    ForceName = 'nanoindent' #name of nanoindenter load
    JobName = 'nanoindent' #name of job
    IndentLocName = 'nanoindenter' #name of the set (not created here) for the nanoindenter position
    ModelName = 'Model-1' #name of the model
    PrtName = 'Part-1' #Name of Part
    InstName = 'Inst-1' #Name of Instance
    #Only for direct dynamic analysis#
    MinFreq = 19000 #minimum frequency for the frequency step
    MaxFreq = 20000 #maximum frequency for the frequency step
    VertDisp = 1e-05 #vertical displacement of the built in end
    #Only for static cantilever calibration#
    SName2 = 'disk' #name of loading step  with indent nearer the disk
    SName3 = 'end' #name of loading step with indent nearer the end
    DiskFreeName = 'near_disk' #name of set for the indent nearer the disk side of the tongue (quater of the way along and on center line)
    EndFreeName = 'near_end' #name ofset for the indent nearer the end side of the tongue (three quaters of the way along and on center line)
