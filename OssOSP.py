# MODULE OssOSP
# Author: Timothy Teh

# some ideas for data types
# constants: tuple of 1
# references : list of 1
# records: class
# global variabes : list of 1

import OssOSS as OSS
import OssOSG as OSG

sym = [0]

def declarations(varsize):
    obj = [None] # Pointer to ObjDesc
    first = [None]
    x = OSG.Item()
    tp = [None]
    L = 0
    if sym[0] < OSS.const[0] and sym[0] != OSS.end[0]:
        OSS.Mark("declaration?")

def Module(S):
    # Varsize is a reference
    varsize = [None]
    print "  compiling",
    OSS.Get(sym)
    if sym[0] == OSS.module[0]:
        OSS.Get(sym)
        #OSG.Open()
        if sym[0] == OSS.ident[0]:
            modid = list(OSS.id)
            OSS.Get(sym)
            print ''.join(modid).strip()
        else:
            OSS.Mark("ident?")
        if sym[0] == OSS.semicolon[0]:
            OSS.Get(sym)
        else:
            OSS.Mark(";?")
        declarations(varsize)