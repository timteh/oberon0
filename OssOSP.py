# MODULE OssOSP
# Author: Timothy Teh

# some ideas for data types
# constants: tuple of 1
# references : Variable class from util module, or a class itself
# records: class
# global variabes : Variable() class

import OssOSS as OSS
import OssOSG as OSG
from Util import *

# Global variables
sym = Variable(0)
topScope = Pointer(OSG.ObjDesc) # Pointer to ObjDesc
universe = Pointer(OSG.ObjDesc) 
guard = Pointer(OSG.ObjDesc) 
testguard = Pointer(OSG.ObjDesc)

def NewObj(obj, Class):
    new = Pointer(OSG.ObjDesc)
    x = Pointer(OSG.ObjDesc)
    x.m_value = topScope.m_value
    guard.m_value.m_name = OSS.id.m_value
    while x.m_value.m_next.m_name != OSS.id.m_value:
        x.m_value = x.m_value.m_next
        if x.m_value.m_next == guard.m_value:
            NEW(new)
            new.m_value.m_name = OSS.id.m_value
            new.m_value.m_class = Class
            new.m_value.m_next = guard.m_value
            x.m_value.m_next = new.m_value
            obj.m_value = new.m_value
        else:
            obj.m_value = x.m_value.m_next
            OSS.Mark("mult def")

def OpenScope():
    s = Pointer(OSG.ObjDesc) # Pointer to ObjDesc
    NEW(s)
    s.m_value.m_class = OSG.HEAD.getValue()
    s.m_value.m_dsc = topScope.m_value
    s.m_value.m_next = guard.m_value
    topScope.m_value = s.m_value

def expression(item):
    pass

def Type(Type):
    pass

def IdentList(Class, first):
    obj = OSG.ObjDesc()
    if sym == OSS.IDENT.getValue():
        NewObj(first, Class)
        OSS.Get(sym)
        while sym == OSS.COMMA.getValue():
            OSS.Get(sym)
            if sym == OSS.IDENT.getValue():
                NewObj(obj, Class)
                OSS.Get(sym)
            else:
                OSS.Mark("ident?")
        if sym == OSS.COLON.getValue():
            OSS.Get(sym)
        else:
            OSS.Mark(":?")

def declarations(varsize):
    obj = Pointer(OSG.ObjDesc)  # Reference Pointer to ObjDesc
    first = Pointer(OSG.Item) # Pointer to ObjDesc
    x = OSG.Item() # x is a reference 
    tp = Pointer(OSG.TypeDesc) # Pointer to TypeDesc
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
                while obj.m_value != guard.m_value:
                    obj.m_value.m_type = tp.m_value
                    obj.m_value.m_lev = OSG.curlev.m_value
                    varsize.m_value = varsize.m_value + obj.m_type.m_size
                    obj.m_value.m_val -= varsize.m_value
                    obj.m_value = obj.m_value.m_next
                if sym.m_value == OSS.SEMICOLON.getValue():
                    OSS.Get(sym)
                else:
                    OSS.Mark("; ?")
        if sym.m_value >= OSS.CONST.getValue() and sym.m_value <= OSS.VAR.getValue():
            OSS.Mark("; ?")
        else:
            break

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
NEW(guard)
guard.m_value.m_class = OSG.VAR.getValue()
guard.m_value.m_type = OSG.intType
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