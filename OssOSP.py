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

# Global Constants
WORDSIZE = Constant(4)

# Global variables
sym = Variable(0)
topScope = Pointer(OSG.ObjDesc) # Pointer to ObjDesc
universe = Pointer(OSG.ObjDesc) 
guard = Pointer(OSG.ObjDesc) 
testguard = Pointer(OSG.ObjDesc)

def find(obj):
    s = Pointer(OSG.ObjDesc)
    x = Pointer(OSG.ObjDesc)
    s.m_value = topScope.m_value
    # Debugging
    #print ''.join(OSS.id.m_value)
    guard.m_value.m_name = ''.join(OSS.id.m_value)
    while True:
        x.m_value = s.m_value.m_next
        while (x.m_value.m_name != ''.join(OSS.id.m_value)):
            x.m_value = x.m_value.m_next
        if x.m_value != guard.m_value:
            obj.m_value = x.m_value
            break
        if x.m_value == universe.m_value:
            obj.m_value = x.m_value
            OSS.Mark("undef")
            break
        s.m_value = s.m_value.m_dsc

def FindField(obj, List):
    guard.m_value.m_name = ''.join(OSS.id.m_value)
    while List.m_value.m_name != ''.join(OSS.id.m_value):
        List.m_value = List.m_value.m_next
    obj.m_value = List.m_value

def IsParam(obj):
    return ((obj.m_value.m_class == OSG.PAR.getValue()) or (obj.m_value.m_class == OSG.VAR.getValue()) and (obj.m_value.m_val > 0))

def OpenScope():
    s = Pointer(OSG.ObjDesc) # Pointer to ObjDesc
    NEW(s)
    s.m_value.m_class = OSG.HEAD.getValue()
    s.m_value.m_dsc = topScope.m_value
    s.m_value.m_next = guard.m_value
    topScope.m_value = s.m_value

def CloseScope():
    topScope.m_value = topScope.m_value.m_dsc

def selector(x):
    y = OSG.Item()
    obj = Pointer(OSG.ObjDesc)
    while sym.m_value == OSS.LBRAK.getValue() or sym.m_value == OSS.PERIOD.getValue():
        if sym.m_value == OSS.LBRAK.getValue():
            OSS.Get(sym)
            expression(y)
            if x.m_type.m_form == OSG.ARRAY.getValue():
                OSG.Index(x,y)
            else:
                OSS.Mark("not an array")
            if sym.m_value == OSS.RBRAK.getValue():
                OSS.Get(sym)
            else:
                OSS.Mark("]?")
        else:
            OSS.Get(sym)
            if sym.m_value == OSS.IDENT.getValue():
                if x.m_type.m_form == OSG.RECORD.getValue():
                    FindField(obj, x.m_type.m_fields)
                    OSS.Get(sym)
                    if obj.m_value != guard.m_value:
                        OSG.Field(x, obj)
                    else:
                        OSS.Mark("undef")
                else:
                    OSS.Mark("not a record")
            else:
                OSS.Mark("ident?")

def factor(x):
    obj = Pointer(OSG.ObjDesc)
    if sym.m_value < OSS.LPAREN.getValue():
        OSS.Mark("ident?")
        while True:
            OSS.Get(sym)
            if (sym.m_value >= OSS.LPAREN.getValue()):
                break
    if sym.m_value == OSS.IDENT.getValue():
        find(obj)
        OSS.Get(sym)
        OSG.MakeItem(x, obj)
        selector(x)
    elif sym.m_value == OSS.NUMBER.getValue():
        OSG.MakeConstItem(x, OSG.intType, OSS.val)
        OSS.Get(sym)
    elif sym.m_value == OSS.LPAREN.getValue():
        OSS.Get(sym)
        expression(x)
        if sym.m_value == OSS.RPAREN.getValue():
            OSS.Get(sym)
        else:
            OSS.Mark(")?")
    elif sym.m_value == OSS.NOT.getValue():
        OSS.Get(sym)
        factor(x)
        OSG.Op1(OSS.NOT.getValue(), x)
    else:
        OSS.Mark("factor?")
        OSG.MakeItem(x, guard)

def term(x):
    y = OSG.Item()
    op = Variable(0)
    factor(x)
    while sym.m_value >= OSS.TIMES.getValue() and sym.m_value <= OSS.AND.getValue():
        op.m_value = sym.m_value
        OSS.Get(sym)
        if op.m_value == OSS.AND.getValue():
            OSG.Op1(op.m_value, x)
        factor(y)
        OSG.Op2(op.m_value, x, y)

def SimpleExpression(x): #x : OSG.Item
    y = OSG.Item()
    op = Variable(0)
    if sym.m_value == OSS.PLUS.getValue():
        OSS.Get(sym)
        term(x)
    elif sym.m_value == OSS.MINUS.getValue():
        OSS.Get(sym)
        PSG.Op1(OSS.MINUS.getValue(), x)
    else:
        term(x)
    while sym.m_value >= OSS.PLUS.getValue() and sym.m_value <= OSS.OR.getValue():
        op.m_value = sym.m_value
        OSS.Get(sym)
        if op.m_value == OSS.OR.getValue():
            OSG.Op1(op.m_value, x)
        term(y)
        OSG.Op2(op.m_value, x, y)

def expression(x): #x : OSG.Item
    y = OSG.Item()
    op = Variable(0)
    SimpleExpression(x)
    if sym.m_value >= OSS.EQL.getValue() and sym.m_value <= OSS.GTR.getValue():
        op.m_value = sym.m_value
        OSS.Get(sym)
        SimpleExpression(y)
        OSG.Relation(op, x, y)

def parameter(fp):
    x = OSG.Item()
    expression(x)
    if IsParam(fp):
        OSG.Parameter

def StatSequence():
    par = Pointer(OSG.ObjDesc)
    obj = Pointer(OSG.ObjDesc)
    x = OSG.Item()
    y = OSG.Item()
    L = Variable(0)

    def param(x):
        if sym.m_value == OSS.LPAREN.getValue():
            OSS.Get(sym)
        else:
            OSS.Mark(")?")
        expression(x)
        if sym.m_value == OSS.RPAREN.getValue():
            OSS.Get(sym)
        else:
            OSS.Mark(")?")
    # print "calling statsequence"
    while True:
        obj.m_value = guard.m_value
        if sym.m_value < OSS.IDENT.getValue():
            OSS.Mark("statement?")
            while True:
                OSS.Get(sym)
                if sym.m_value >= OSS.IDENT.getValue():
                    break
        if sym.m_value == OSS.IDENT.getValue():
            find(obj)
            OSS.Get(sym)
            OSG.MakeItem(x, obj)
            selector(x)
            if sym.m_value == OSS.BECOMES.getValue():
                OSS.Get(sym)
                expression(y)
                OSG.Store(x, y)
            elif sym.m_value == OSS.EQL.getValue():
                OSS.Mark(":= ?")
                OSS.Get(sym)
                expression(y)
            elif x.m_mode == OSG.PROC.getValue():
                par.m_value = obj.m_value.m_dsc
                if sym.m_value == OSS.LPAREN.getValue():
                    OSS.Get(sym)
                    if sym.m_value == OSS.RPAREN.getValue():
                        OSS.Get(sym)
                    else:
                        while True:
                            parameter(par)
                            if sym.m_value == OSS.COMMA.getValue():
                                OSS.Get(sym)
                            elif sym.m_value == OSS.RPAREN.getValue():
                                OSS.Get(sym)
                                break
                            elif sym.m_value >= OSS.SEMICOLON.getValue():
                                break
                            else:
                                OSS.Mark(") or, ?")
                if obj.m_value.m_val < 0:
                    OSS.Mark("forward call")
                elif ~IsParam(par):
                    OSG.Call(x)
                else:
                    OSS.Mark("too few parameterse")
            elif x.m_mode == OSG.SPROC.getValue():
                if obj.m_value.m_val <= 3:
                    param(y)
                OSG.IOCall(x, y)
            elif obj.m_value.m_class == OSG.TYP.getValue():
                OSS.Mark("illegal assignment")
            else:
                OSS.Mark("statement?")
        elif sym.m_value == OSS.IF.getValue():
            OSS.Get(sym)
            expression(x)
            OSG.CJump(x)
            if sym.m_value == OSS.THEN.getValue():
                OSS.Get(sym)
            else:
                OSS.Mark("THEN?")
            StatSequence()
            L.m_value = 0
            while sym.m_value == OSS.ELSIF.getValue():
                OSS.Get(sym)
                OSG.FJump(L)
                OSG.FixLink(x.m_a)
                expression(x)
                OSG.CJump(x)
                if sym.m_value == OSS.THEN.getValue():
                    OSS.Get(sym)
                else:
                    OSS.Mark("THEN?")
                    StatSequence()
            if sym.m_value == OSS.ELSE.getValue():
                OSS.Get(sym)
                OSG.FJump(L)
                OSG.FixLink(x.m_a)
                StatSequence()
            else:
                OSG.FixLink(x.m_a)

            OSG.FixLink(L)
            if sym.m_value == OSS.END.getValue():
                OSS.Get(sym)
            else:
                OSS.Mark("END?")
        elif sym.m_value == OSS.WHILE.getValue():
            OSS.Get(sym)
            L.m_value = OSG.pc.m_value
            expression(x)
            OSG.CJump(x)
            if sym.m_value == OSS.DO.getValue():
                OSS.Get(sym)
            else:
                OSS.Mark("DO?")
            StatSequence()
            OSG.BJump(L)
            OSG.FixLink(x.m_a)
            if sym.m_value == OSS.END.getValue():
                OSS.Get(sym)
            else:
                OSS.Mark("END?")
        if sym.m_value == OSS.SEMICOLON.getValue():
            OSS.Get(sym)
        elif (sym.m_value >= OSS.SEMICOLON.getValue()) and (sym.m_value < OSS.IF.getValue()) or (sym.m_value >= OSS.ARRAY.getValue()):
            break
        else:
            OSS.Mark("; ?")
    # print "exiting statsequence"

def NewObj(obj, Class):
    new = Pointer(OSG.ObjDesc)
    x = Pointer(OSG.ObjDesc)
    x.m_value = topScope.m_value
    guard.m_value.m_name = ''.join(OSS.id.m_value)
    while x.m_value.m_next.m_name != ''.join(OSS.id.m_value):
        x.m_value = x.m_value.m_next
    if x.m_value.m_next == guard.m_value:
        NEW(new)
        new.m_value.m_name = ''.join(OSS.id.m_value)
        new.m_value.m_class = Class
        new.m_value.m_next = guard.m_value
        x.m_value.m_next = new.m_value
        obj.m_value = new.m_value
    else:
        obj.m_value = x.m_value.m_next
        OSS.Mark("mult def")

def Type(type_):
    obj = Pointer(OSG.ObjDesc)
    first = Pointer(OSG.ObjDesc)
    x = OSG.Item()
    tp = Pointer(OSG.TypeDesc)
    type_.m_value = OSG.intType.m_value
    if sym.m_value != OSS.IDENT.getValue() and sym.m_value < OSS.ARRAY.getValue():
        OSS.Mark("type?")
        while True:
            OSS.Get(sym)
            if sym.m_value == OSS.IDENT.getValue() or sym.m_value >= OSS.ARRAY.getValue():
                break
    if sym.m_value == OSS.IDENT.getValue():
        find(obj)
        OSS.Get(sym)
        if obj.m_value.m_class == OSG.TYP.getValue():
            type_.m_value = obj.m_value.m_type
        else:
            OSS.Mark("type?")
    elif sym.m_value == OSS.ARRAY.getValue():
        OSS.Get(sym)
        expression(x)
        if x.m_mode != OSG.CONST.getValue() or x.m_a.m_value < 0:
            OSS.Mark("bad index")
        if sym.m_value == OSS.OF.getValue():
            OSS.Get(sym)
        else:
            OSS.Mark("OF?")
        Type(tp)
        NEW(type_)
        type_.m_value.m_form = OSG.ARRAY.getValue()
        type_.m_value.m_base = tp.m_value
        type_.m_value.m_len = SHORT(x.m_a.m_value)
        type_.m_value.m_size = SHORT(type_.m_value.m_len * tp.m_value.m_size)
    elif sym.m_value == OSS.RECORD.getValue():
        OSS.Get(sym)
        NEW(type_)
        type_.m_value.m_form = OSG.RECORD.getValue()
        type_.m_value.m_size = 0
        OpenScope()
        while True:
            if sym.m_value == OSS.IDENT.getValue():
                IdentList(OSG.FLD.getValue(), first)
                Type(tp)
                obj.m_value = first.m_value
                while obj.m_value != guard.m_value:
                    obj.m_value.m_type = tp.m_value
                    obj.m_value.m_val = Type.m_value.m_size
                    type_.m_value.m_size += obj.m_value.m_type.m_size
                    obj.m_value = obj.m_value.m_next
            if sym.m_value == OSS.SEMICOLON.getValue():
                OSS.Get(sym)
            elif sym.m_value == OSS.IDENT.getValue():
                OSS.Mark("; ?")
            else:
                break
        type_.m_value.m_fields.m_value = topScope.m_value
        CloseScope()
        if sym.m_value == OSS.END.getValue():
            OSS.Get(sym)
        else:
            OSS.Mark("END?")
    else:
        OSS.Mark("ident?")

def IdentList(Class, first):
    obj = Pointer(OSG.ObjDesc)
    if sym.m_value == OSS.IDENT.getValue():
        NewObj(first, Class)
        OSS.Get(sym)
        while sym.m_value == OSS.COMMA.getValue():
            OSS.Get(sym)
            if sym.m_value == OSS.IDENT.getValue():
                NewObj(obj, Class)
                OSS.Get(sym)
            else:
                OSS.Mark("ident?")
        if sym.m_value == OSS.COLON.getValue():
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
                    obj.m_value.m_val = x.m_a.m_value
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
                    varsize.m_value = varsize.m_value + obj.m_value.m_type.m_size
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

def ProcedureDec1():
    marksize = Constant(8)
    proc = Pointer(OSG.ObjDesc)
    obj  = Pointer(OSG.ObjDesc)
    procid = Variable([''] * OSS.IDLEN.getValue())
    locblksize = Variable(0)
    parblksize = Variable(0)

    def FPSection():
        obj = Pointer(OSG.ObjDesc)
        first = Pointer(OSG.ObjDesc)
        tp = Pointer(OSG.TypeDesc)
        parsize = Variable(0)
        if sym.m_value == OSS.VAR.getValue():
            OSS.Get(sym)
            IdentList(OSG.PAR.getValue(), first)
        else:
            IdentList(OSG.VAR.getValue(), first)
        if sym.m_value == OSS.IDENT.getValue():
            find(obj)
            OSS.Get(sym)
            if obj.m_value.m_class == OSG.TYP.getValue():
                tp.m_value = obj.m_value.m_type
            else:
                OSS.Mark("type?")
                tp.m_value = OSG.intType.m_value
        else:
            OSS.Mark("ident?")
            tp.m_value = OSG.intType.m_value
        if first.m_value.m_class == OSG.VAR.getValue():
            parsize.m_value = WordSize
        obj.m_value = first.m_value
        while obj.m_value != guard.m_value:
            obj.m_value.m_type = tp.m_value
            INC(parblksize, parsize.m_value)
            obj.m_value = obj.m_value.m_next
    
    OSS.Get(sym)
    if sym.m_value == OSS.IDENT.getValue():
        procid.m_value = ''.join(OSS.id.m_value)
        NewObj(proc, OSG.PROC.getValue())
        OSS.Get(sym)
        parblksize.m_value = marksize.getValue()
        OSG.IncLevel(1)
        OpenScope()
        proc.m_value.m_val = -1
        if sym.m_value == OSS.LPAREN.getValue():
            OSS.Get(sym)
            if sym.m_value == OSS.RPAREN.getValue():
                OSS.Get(sym)
            else:
                FPSection()
                while sym.m_value == OSS.SEMICOLON.getValue():
                    OSS.Get(sym)
                    FPSection()
                if sym.m_value == OSS.RPAREN.getValue():
                    OSS.Get(sym)
                else:
                    OSS.Mark(")?")
        elif OSG.curlev.m_value == 1:
            OSG.EnterCmd(procid.m_value)
        obj.m_value = topScope.m_value.m_next
        locblksize.m_value = parblksize.m_value
        while obj.m_value != guard.m_value:
            obj.m_value.m_lev = OSG.curlev.m_value
            if obj.m_value.m_class == OSG.PAR.getValue():
                DEC(locblksize, WORDSIZE.getValue())
            else:
                locblksize.m_value = locblksize.m_value - obj.m_value.m_type.m_size
            obj.m_value.m_val = locblksize.m_value
            obj.m_value = obj.m_value.m_next
        proc.m_value.m_dsc = topScope.m_value.m_next
        if sym.m_value == OSS.SEMICOLON.getValue():
            OSS.Get(sym)
        else: 
            OSS.Mark(";?")
        locblksize.m_value = 0
        declarations(locblksize)
        while sym.m_value == OSS.PROCEDURE.getValue():
            ProcedureDec1()
            if sym.m_value == OSS.SEMICOLON.getValue():
                OSS.Get(sym)
            else:
                OSS.Mark(";?")
        proc.m_value = OSG.pc.m_value
        OSG.Enter(locblksize.m_value)
        if sym.m_value == OSS.BEGIN.getValue():
            OSS.Get(sym)
            StatSequence()
        if sym.m_value == OSS.END.getValue():
            OSS.Get(sym)
        else:
            OSS.Mark("END?")
        if sym.m_value == OSS.IDENT.getValue():
            if procid.m_value != ''.join(OSS.id.m_value):
                OSS.Mark("no match")
            OSS.Get(sym)
        OSG.Return(parblksize.m_value - marksize.getValue())
        CloseScope()
        OSG.IncLevel(-1)

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
            print ''.join(modid)
        else:
            OSS.Mark("ident?")
        if sym.m_value == OSS.SEMICOLON.getValue():
            OSS.Get(sym)
        else:
            OSS.Mark(";?")
        declarations(varsize)
        while sym.m_value == OSS.PROCEDURE.getValue():
            ProcedureDec1()
            if sym.m_value == OSS.SEMICOLON.getValue():
                OSS.Get(sym)
            else:
                OSS.Mark(";?")
        OSG.Header(varsize)
        if sym.m_value == OSS.BEGIN.getValue():
            OSS.Get(sym)
            StatSequence()
        if sym.m_value == OSS.END.getValue():
            OSS.Get(sym)
        else:
            OSS.Mark("END?")
        if sym.m_value == OSS.IDENT.getValue():
            if ''.join(modid) != ''.join(OSS.id.m_value):
                OSS.Mark("no match")
            OSS.Get(sym)
        else:
            OSS.Mark("ident?")
        if sym.m_value != OSS.PERIOD.getValue():
            OSS.Mark(". ?")
        CloseScope()
        #if not OSS.error.m_value:
            #S.s = ''.join(modid)
    OSG.Close(S, varsize)
    print "code generated",
    print OSG.pc.m_value


def enter(cl, n, name, Type):
    obj = Pointer(OSG.ObjDesc) # Pointer to ObjDesc
    NEW(obj)
    obj.m_value.m_class = cl
    obj.m_value.m_val = n
    obj.m_value.m_name = name
    obj.m_value.m_type = Type
    obj.m_value.m_dsc = None
    obj.m_value.m_next = topScope.m_value.m_next
    topScope.m_value.m_next = obj.m_value

# BEGIN
print "Oberon0 Compiler  9.2.95"
NEW(guard)
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