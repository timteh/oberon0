# imports
import OssOSS as OSS
from Util import *

# "constants"
MAXCODE = Constant(1000)
MAXREL = Constant(200)
NOFCOM = Constant(16)

HEAD = Constant(0)
VAR = Constant(1)
PAR = Constant(2)
CONST = Constant(3)
FLD = Constant(4)
TYP = Constant(5)
PROC = Constant(6)
SPROC = Constant(7)
REG = Constant(10)
COND = Constant(11)
BOOLEAN = Constant(0)
INTEGER = Constant(1)
ARRAY = Constant(2)
RECORD = Constant(3)

# ISA
ADD = Constant(0)
SUB = Constant(1)
MUL = Constant(2)
DIV = Constant(3)
MOD = Constant(4)
CMP = Constant(5)
OR = Constant(8)
AND = Constant(9)
BIC = Constant(10)
XOR = Constant(11)
LSH = Constant(12)
ASH1 = Constant(13)
CHK = Constant(14)
ADDI = Constant(16)
SUBI = Constant(17)
MULI = Constant(18)
DIVI = Constant(19)
MODI = Constant(20)
CMPI = Constant(21)
ORI = Constant(24)
ANDI = Constant(25)
BICI = Constant(26)
XORI = Constant(27)
LSHI = Constant(28)
ASHI = Constant(29)
CHKI = Constant(30)
LDW = Constant(32)
LDB = Constant(33)
POP = Constant(34)
STW = Constant(36)
STB = Constant(37)
PSH = Constant(38)
BEQ = Constant(40)
BNE = Constant(41)
BLT = Constant(42)
BGE = Constant(43)
BLE = Constant(44)
BGT = Constant(45)
BSR = Constant(46)
JSR = Constant(48)
RET = Constant(49)
RD = Constant(50)
WRD = Constant(51)
WRH = Constant(52)
WRL = Constant(53)
FP = Constant(29)
SP = Constant(30)
LNK = Constant(31)

class Item:
    def __init__(self):
        self.m_mode = 0
        self.m_lev = 0
        self.m_type = None# Pointer to TypeDesc
        self.m_a = 0
        self.m_b = 0
        self.m_c = 0
        self.m_r = 0

class ObjDesc:
    def __init__(self):
        self.m_class = 0
        self.m_lev = 0
        self.m_next = None # Pointer to ObjDesc
        self.m_dsc =  None # Pointer to ObjDesc
        self.m_type = None # Pointer to TypeDesc
        self.m_name = 0
        self.val = 0

class TypeDesc:
    def __init__(self):    
        self.m_form = 0
        self.m_fields = Pointer(ObjDesc) # Pointer to ObjDesc
        self.m_base = None # Pointer to TypeDesc
        self.m_size = 0
        self.m_len = 0

# Global variables
intType  = Pointer(TypeDesc) #pointer to TypeDesc
boolType = Pointer(TypeDesc) #pointer to TypeDesc
curlev = Variable(0)
pc = Variable(0)
relx = Variable(0)
cno = Variable(0)
regs = Variable(set())
code = Variable([0]*MAXCODE.getValue())
rel = Variable([0]*MAXREL.getValue())
comname = Variable(NOFCOM.getValue() * [[''] * OSS.IDLEN.getValue()])
comadr = Variable(NOFCOM.getValue() * [0])
mnemo = Variable(54 *[5*['']])

def MakeConstItem(x, type, val):
    x.m_mode = CONST.getValue()
    x.m_type = typ.m_value
    x.m_a = val.m_value

def MakeItem(x, y):
    r = Variable(0)
    x.m_mode = y.m_value.m_class
    x.m_type = y.m_value.m_type
    x.m_lev = y.m_value.m_lev
    x.m_a = y.m_value.m_val
    if y.m_value.m_lev == 0:
        x.m_r = 0
    elif y.m_value.m_lev == curlev.m_value:
        x.m_r = FP.getValue()
    else:
        OSS.Mark("level!")
        x.m_r = 0
    if y.m_value.m_class == PAR.getValue():
        GetReg(r)
        Put(LDW.getValue(), r.m_value, x.m_r, x.m_a)
        x.m_mode = VAR.getValue()
        x.m_r = r.m_value
        x.m_a = 0

def Field(x,y):
    x.m_a += y.m_value.m_val
    x.m_type = y.m_value.m_type

def Index(x, y):
    if y.m_type != intType.m_value:
        OSS.Mark("index not integer")
    if y.m_mode == CONST.getValue():
        if y.m_a < 0 or y.m_a >= x.m_type.m_len:
            OSS.Mark("bad index")
            x.m_a += (y.m_a * x.m_type.m_base.m_size)
    else:
        if y.m_mode != REG.getValue():
            load(y)
        Put(CHKI.getValue(), y.m_r, 0, x.m_type.m_len)
        Put(MULI.getValue(), y.m_r, y.m_r, x.m_type.m_base.m_size)
        if x.m_r != 0:
            Put(ADD.getValue(), y.mr, x.m_r, y.m_r)
            EXCL(regs, x.m_r)
        x.m_r = y.m_r
    x.m_type = x.m_type.m_base

def Open():
    curlev.m_value = 0
    pc.m_value = 0
    relx.m_value = 0
    cno.m_value = 0
    regs.m_value = set()

def GetReg(r):
    i = Variable(0)
    i.m_value = 1
    while i.m_value < FP.getValue() and i.m_value in regs.m_value:
        INC(i)
    INCL(regs, i.m_value)
    r.m_value = i.m_value

def Put(op, a, b, c):
    localop = Variable(op)
    if op >= 32:
        DEC(localop, 64)
    code.m_value[pc.m_value] = ASH(ASH(ASH(localop, 5) + a, 5) + b, 16) + (c % 0x10000)
    INC(pc)

def TestRange(x):
    if x >= 0x8000 or x < -0x8000:
        OSS.Mark("value too large")

def load(x):
    r = Variable(0)
    if x.m_mode == VAR.getValue():
        if x.m_lev == 0:
            rel.m_value[relx] = SHORT(pc)
            INC(relx)
        GetReg(r)
        Put(LDW.getValue(), r.m_value, x.m_r, x.m_a)
        EXCL(regs, x.m_r)
        x.m_r = r.m_value
    elif x.m_mode == CONST.getValue():
        if x.m_a == 0:
            x.m_r = 0
        else:
            TestRange(x.m_a)
            localr = Variable(0)
            GetReg(localr)
            x.m_r = localr
            Put(ADDI.getValue(), x.m_r, 0, x.m_a)
    x.m_mode = REG.getValue()

def loadBool(x):
    if x.m_type.m_form != BOOLEAN.getValue():
        OSS.Mark("Boolean?")
    load(x)
    x.m_mode = COND.getValue()
    x.m_a = 0
    x.m_b = 0
    x.m_c = 1

def Op1(op, x):
    t = Variable(0)
    if op == OSS.MINUS.getValue():
        if x.m_type.m_form != INTEGER.getValue():
            OSS.Mark("bad type")
        elif x.m_mode == CONST.getValue():
            x.m_a = -x.m_a
        else:
            if x.m_mode == VAR.getValue():
                load(x)
            Put(SUB.getValue(), x.m_r, 0, x.m_r)
    elif op == OSS.NOT.getValue():
        if x.m_mode!= COND.getValue():
            loadBool(x)
        x.m_c = negated(x.m_c)
        t.m_value = x.m_a
        x.m_a = x.m_b
        x.m_b = t.m_value

def Relation(op, x, y):
    if x.m_type.m_form != INTEGER.getValue() or y.m_type.m_form != INTEGER.getValue():
        OSS.Mark("bad type")
    else:
        if y.m_mode == CONST.getValue() and y.m_a == 0:
            load(x)
        else:
            PutOp(CMP.getValue(), x ,y)
        x.m_c = op.m_value - OSS.EQL.getValue()
        EXCL(regs, y.m_r)
    x.m_mode = COND.getValue()
    x.m_type = boolType.m_value
    x.m_a = 0
    x.m_b = 0

NEW(boolType)        
boolType.m_value.m_form = BOOLEAN.getValue()
boolType.m_value.m_size = 4
NEW(intType)
intType.m_value.m_form = INTEGER.getValue()
intType.m_value.m_size = 4
mnemo.m_value[ADD.getValue()] = "add "
mnemo.m_value[SUB.getValue()] = "sub "
mnemo.m_value[MUL.getValue()] = "mul "
mnemo.m_value[DIV.getValue()] = "DIV "
mnemo.m_value[MOD.getValue()] = "MOD "
mnemo.m_value[CMP.getValue()] = "CMP "
mnemo.m_value[OR.getValue()]  = "OR  "
mnemo.m_value[AND.getValue()] = "AND "
mnemo.m_value[BIC.getValue()] = "BIC "
mnemo.m_value[XOR.getValue()] = "XOR "
mnemo.m_value[LSH.getValue()] = "LSH "
mnemo.m_value[ASH1.getValue()] = "ASH "
mnemo.m_value[CHK.getValue()] = "CHK "
mnemo.m_value[ADDI.getValue()] = "ADDI"
mnemo.m_value[SUBI.getValue()] = "SUBI"
mnemo.m_value[MULI.getValue()] = "MULI"
mnemo.m_value[DIVI.getValue()] = "DIVI"
mnemo.m_value[MODI.getValue()] = "CMPI"
mnemo.m_value[CMPI.getValue()] = "MODI"
mnemo.m_value[ORI.getValue()]  = "ORI "
mnemo.m_value[ANDI.getValue()] = "ANDI"
mnemo.m_value[BICI.getValue()] = "BICI"
mnemo.m_value[XORI.getValue()] = "XORI"
mnemo.m_value[LSHI.getValue()] = "LSHI"
mnemo.m_value[ASHI.getValue()] = "ASHI"
mnemo.m_value[CHKI.getValue()] = "CHKI"
mnemo.m_value[LDW.getValue()] = "ldw "
mnemo.m_value[LDB.getValue()] = "LDB "
mnemo.m_value[POP.getValue()] = "POP "
mnemo.m_value[STW.getValue()] = "STW "
mnemo.m_value[STB.getValue()] = "STB "
mnemo.m_value[PSH.getValue()] = "PSH "
mnemo.m_value[BEQ.getValue()] = "BEQ "
mnemo.m_value[BNE.getValue()] = "BNE "
mnemo.m_value[BLT.getValue()] = "BLT "
mnemo.m_value[BGE.getValue()] = "BGE "
mnemo.m_value[BLE.getValue()] = "BLE "
mnemo.m_value[BGT.getValue()] = "BGT "
mnemo.m_value[BSR.getValue()] = "BSR "
mnemo.m_value[JSR.getValue()] = "JSR "
mnemo.m_value[RET.getValue()] = "RET "
mnemo.m_value[RD.getValue()]  = "READ"
mnemo.m_value[WRD.getValue()] = "WRD "
mnemo.m_value[WRH.getValue()] = "WRH "
mnemo.m_value[WRL.getValue()] = "WRL "
