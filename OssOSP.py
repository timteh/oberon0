# MODULE OssOSP
# Author: Timothy Teh

# some ideas for data types
# constants: tuple of 1
# references : list of 1
# records: class
# global variabes : list of 1

import OssOSS as OSS
import OssOSG as OSG
from Util import *

# Global variables
sym = Variable(0)
topScope = [None] # Pointer to ObjDesc
universe = [None]
guard = [None]

def NewObj(obj, _class):
    x = topScope[0]
    guard[0].name = OSS.id.m_value
    while x._next.name != OSS.id.m_value:
        x = x._next
        if x._next == guard[0]:
            new = OSG.ObjDesc()
            new.name = OSS.id.m_value
            new._class = _class
            new._next = guard[0]
            x._next = new
            obj[0] = new
        else:
            obj[0] = x._next
            OSS.Mark("mult def")

def OpenScope():
    s = OSG.ObjDesc() # Pointer to ObjDesc
    s._class = OSG.HEAD.getValue
    s.dsc = topScope[0]
    s._next = guard[0]
    topScope[0] = s

def declarations(varsize):
    obj = [None]  # Reference Pointer to ObjDesc
    first = [None] # Pointer to ObjDesc
    x = [OSG.Item()] # x is a reference 
    tp = [None] # Pointer to TypeDesc
    L = 0
    if sym.m_value < OSS.CONST.getValue() and sym.m_value != OSS.END.getValue():
        OSS.Mark("declaration?")
        while True:
            OSS.Get(sym)
            if (sym.m_value >= OSS.CONST.getValue() or sym.m_value == OSS.END.getValue()):
                break
    while True:
        if sym.m_value == OSS.CONST.getValue():
            OSS.Get(sym)
            while sym.m_value == OSS.IDENT.getValue():
                NewObj(obj, OSG.CONST.getValue())
                OSS.Get(sym)
                if sym.m_value == OSS.EQL.getValue():
                    OSS.Get(sym)
                else:
                    OSS.Mark("=?")                    
                expression(x)
                
def Module(S):
    # Varsize is a reference
    varsize = [None]
    print "  compiling",
    OSS.Get(sym)
    if sym.m_value == OSS.MODULE.getValue():
        OSS.Get(sym)
        OSG.Open()
        OpenScope()
        varsize[0] = 0
        if sym.m_value == OSS.IDENT.getValue():
            modid = list(OSS.id.m_value)
            OSS.Get(sym)
            print ''.join(modid).strip()
        else:
            OSS.Mark("ident?")
        if sym.m_value == OSS.SEMICOLON.getValue():
            OSS.Get(sym)
        else:
            OSS.Mark(";?")
        declarations(varsize)

def enter(cl, n, name, _type):
    obj = OSG.ObjDesc() # Pointer to ObjDesc
    obj._class = cl
    obj.val = n
    obj.name = name
    obj._type = _type
    obj.dsc = None
    global topScope
    obj._next = topScope[0]._next
    topScope[0]._next = obj

# BEGIN
print "Oberon0 Compiler  9.2.95"
guard[0] = OSG.ObjDesc()
guard[0]._class = OSG.VAR.getValue()
guard[0]._type = OSG.intType
guard[0].val = 0
topScope[0] = None
OpenScope()
enter(OSG.TYP.getValue(), 1, "BOOLEAN", OSG.boolType[0])
enter(OSG.TYP.getValue(), 2, "INTEGER", OSG.intType[0])
enter(OSG.CONST.getValue(), 1, "TRUE", OSG.boolType[0])
enter(OSG.CONST.getValue(), 0, "FALSE", OSG.boolType[0])
enter(OSG.SPROC.getValue(), 1, "Read", None)
enter(OSG.SPROC.getValue(), 2, "Write", None)
enter(OSG.SPROC.getValue(), 3, "WriteHex", None)
enter(OSG.SPROC.getValue(), 4, "WriteLn", None)
universe[0] = topScope[0]
# END OssOSP