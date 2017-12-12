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
topScope = Variable(None) # Pointer to ObjDesc
universe = Variable(None)
guard = Variable(None)

def NewObj(obj, _class):
    x = topScope.m_value
    guard.m_value.m_name = OSS.id.m_value
    while x.m_next.name != OSS.id.m_value:
        x = x.m_next
        if x.m_next == guard.m_value:
            new = OSG.ObjDesc()
            new.name = OSS.id.m_value
            new.m_class = _class
            new.m_next = guard.m_value
            x.m_next = new
            obj.m_value = new
        else:
            obj.m_value = x.m_next
            OSS.Mark("mult def")

def OpenScope():
    s = OSG.ObjDesc() # Pointer to ObjDesc
    s.m_class = OSG.HEAD.getValue
    s.m_dsc = topScope.m_value
    s.m_next = guard.m_value
    topScope.m_value = s

def expression(item):
    pass

def Type(Type):
    pass

def declarations(varsize):
    obj = Variable(None)  # Reference Pointer to ObjDesc
    first = Variable(None) # Pointer to ObjDesc
    x = OSG.Item() # x is a reference 
    tp = Variable(None) # Pointer to TypeDesc
    L = Variable(0)
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
                if x.m_mode == OSG.CONST.getValue():
                    obj.m_value.m_val = x.m_a
                    obj.m_value.m_type = x.m_type
                else:
                    OSS.Mark("expression not constant")
                if sym.m_value == OSS.SEMICOLON.getValue():
                    OSS.Get(sym)
                else:
                    OSS.Mark(";?")
        if sym.m_value == OSS.TYPE.getValue():
                OSS.Get(sym)
                while sym.m_value == OSS.IDENT.getValue():
                    NewObj(obj, OSG.TYP.getValue())
                    OSS.Get(Sym)
                    if sym.m_value == OSS.EQL.getValue():
                        OSS.Get(sym)
                    else:
                        OSS.Mark("=?")
                    Type(obj.m_value.m_type)
                    if sym.m_value == OSS.SEMICOLON.getValue():
                        OSS.Get(sym)
                    else:
                        OSS.Mark(";?")
        if sym.m_value == OSS.VAR.getValue():
            OSS.Get(sym)           
            while sym.m_value == OSS.IDENT.getValue():
                IdentList(OSG.VAR.getValue(), first)
                Type(tp)
                obj.m_value = first.m_value
                #while obj.m_value != guard.m_value:
                    #obj.m_value.m_type = 


def Module(S):
    # Varsize is a reference
    varsize = Variable(None)
    print "  compiling",
    OSS.Get(sym)
    if sym.m_value == OSS.MODULE.getValue():
        OSS.Get(sym)
        OSG.Open()
        OpenScope()
        varsize.m_value = 0
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

def enter(cl, n, name, Type):
    obj = OSG.ObjDesc() # Pointer to ObjDesc
    obj.m_class = cl
    obj.m_val = n
    obj.m_name = name
    obj.m_type = Type
    obj.m_dsc = None
    obj.m_next = topScope.m_value.m_next
    topScope.m_value.m_next = obj

# BEGIN
print "Oberon0 Compiler  9.2.95"
guard.m_value = OSG.ObjDesc()
guard.m_value.m_class = OSG.VAR.getValue()
guard.m_value.m_type = OSG.intType.m_value
guard.m_value.m_val = 0
topScope.m_value = None
OpenScope()
enter(OSG.TYP.getValue(), 1, "BOOLEAN", OSG.boolType.m_value)
enter(OSG.TYP.getValue(), 2, "INTEGER", OSG.intType.m_value)
enter(OSG.CONST.getValue(), 1, "TRUE", OSG.boolType.m_value)
enter(OSG.CONST.getValue(), 0, "FALSE", OSG.boolType.m_value)
enter(OSG.SPROC.getValue(), 1, "Read", None)
enter(OSG.SPROC.getValue(), 2, "Write", None)
enter(OSG.SPROC.getValue(), 3, "WriteHex", None)
enter(OSG.SPROC.getValue(), 4, "WriteLn", None)
universe.m_value = topScope.m_value
# END OssOSP