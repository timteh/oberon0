# Author: Timothy Teh

# some ideas for data types
# constants: tuple of 1
# references : list of 1
# records: class
# global variabes : list of 1

import OssOSS as OSS
import OssBB as BB
import OssOSP as OSP
import OssOSG as OSG
import OssBB as Texts

loaded = [False]

def Compile():
    # Variables
    t = "source.mod" # TODO: To devise a way to pass the file name in future
    loaded[0] = False
    if t is not None:
        OSS.Init(t, 0)
        OSP.Module(0)

def Decode():
    pass

def Load():
    pass

def Exec():
    pass