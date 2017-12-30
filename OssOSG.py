# imports
import OssOSS as OSS
import OssRISC as RISC
from Util import *
from struct import *

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
        self.m_a = Variable(0)
        self.m_b = Variable(0)
        self.m_c = 0
        self.m_r = Variable(0)

class ObjDesc:
    def __init__(self):
        self.m_class = 0
        self.m_lev = 0
        self.m_next = None # Pointer to ObjDesc
        self.m_dsc =  None # Pointer to ObjDesc
        self.m_type = None # Pointer to TypeDesc
        self.m_name = 0
        self.m_val = 0

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
entry = Variable(0)
fixlist = Variable(0)
regs = Variable(set())
code = Variable([0]*MAXCODE.getValue())
rel = Variable([0]*MAXREL.getValue())
comname = Variable(NOFCOM.getValue() * [[''] * OSS.IDLEN.getValue()])
comadr = Variable(NOFCOM.getValue() * [0])
mnemo = Variable(54 *[5*['']])

def IncLevel(n):
    INC(curlev, n)

def MakeConstItem(x, Type, val):
    x.m_mode = CONST.getValue()
    x.m_type = Type.m_value
    x.m_a.m_value = val.m_value

def MakeItem(x, y):
    r = Variable(0)
    x.m_mode = y.m_value.m_class
    x.m_type = y.m_value.m_type
    x.m_lev = y.m_value.m_lev
    x.m_a.m_value = y.m_value.m_val
    if y.m_value.m_lev == 0:
        x.m_r.m_value = 0
    elif y.m_value.m_lev == curlev.m_value:
        x.m_r.m_value = FP.getValue()
    else:
        OSS.Mark("level!")
        x.m_r.m_value = 0
    if y.m_value.m_class == PAR.getValue():
        GetReg(r)
        Put(LDW.getValue(), r.m_value, x.m_r.m_value, x.m_a.m_value)
        x.m_mode = VAR.getValue()
        x.m_r.m_value = r.m_value
        x.m_a.m_value = 0

def Field(x,y):
    x.m_a.m_value += y.m_value.m_val
    x.m_type = y.m_value.m_type

def Index(x, y):
    if y.m_type != intType.m_value:
        OSS.Mark("index not integer")
    if y.m_mode == CONST.getValue():
        if y.m_a < 0 or y.m_a >= x.m_type.m_len:
            OSS.Mark("bad index")
            x.m_a.m_value += (y.m_a * x.m_type.m_base.m_size)
    else:
        if y.m_mode != REG.getValue():
            load(y)
        Put(CHKI.getValue(), y.m_r.m_value, 0, x.m_type.m_len)
        Put(MULI.getValue(), y.m_r.m_value, y.m_r.m_value, x.m_type.m_base.m_size)
        if x.m_r.m_value != 0:
            Put(ADD.getValue(), y.m_r.m_value, x.m_r.m_value, y.m_r.m_value)
            EXCL(regs, x.m_r.m_value)
        x.m_r.m_value = y.m_r.m_value
    x.m_type = x.m_type.m_base

def Open():
    curlev.m_value = 0
    pc.m_value = 0
    relx.m_value = 0
    cno.m_value = 0
    regs.m_value = set()

def Close(S, globals):
    Put(POP.getValue(), LNK.getValue(), SP.getValue(), 4)
    Put(RET.getValue(), 0, 0, LNK.getValue())

def GetReg(r):
    i = Variable(0)
    i.m_value = 1
    while i.m_value < FP.getValue() and i.m_value in regs.m_value:
        INC(i)
    INCL(regs, i.m_value)
    r.m_value = i.m_value

def Put(op, a, b, c):
    op = Variable(op)
    if op >= 32:
        DEC(op, 64)
    code.m_value[pc.m_value] = (ASH(ASH(ASH(op.m_value, 5) + a, 5) + b, 16) + (c % 0x10000)) & 0xffffffff
    INC(pc)

def TestRange(x):
    if x >= 0x8000 or x < -0x8000:
        OSS.Mark("value too large")

def Header(size):
    entry.m_value = pc.m_value
    Put(ADDI.getValue(), SP.getValue(), 0, RISC.MEMSIZE.getValue() - size.m_value)
    Put(PSH.getValue(), LNK.getValue(), SP.getValue(), 4)

def Enter(size):
    Put(PSH.getValue(), LNK.getValue(), SP.getValue(), 4)
    Put(PSH.getValue(), FP.getValue(), SP.getValue(), 4)
    Put(ADD.getValue(), FP.getValue(), 0, SP.getValue())
    Put(SUBI.getValue(), SP.getValue(), SP.getValue(), size)

def EnterCmd(name):
    comname.m_value[cno.m_value] = name
    comadr.m_value[cno.m_value] = pc.m_value * 4
    INC(cno)

def Return(size):
    Put(ADD.getValue(), SP.getValue(), 0, FP.getValue())
    Put(POP.getValue(), FP.getValue(), SP.getValue(), 4)
    Put(POP.getValue(), LNK.getValue(), SP.getValue(), size + 4)
    Put(RET.getValue(), 0 , 0, LNK.getValue())

def load(x):
    r = Variable(0)
    if x.m_mode == VAR.getValue():
        if x.m_lev == 0:
            rel.m_value[relx] = SHORT(pc)
            INC(relx)
        GetReg(r)
        Put(LDW.getValue(), r.m_value, x.m_r.m_value, x.m_a.m_value)
        EXCL(regs, x.m_r.m_value)
        x.m_r.m_value = r.m_value
    elif x.m_mode == CONST.getValue():
        if x.m_a.m_value == 0:
            x.m_r.m_value = 0
        else:
            TestRange(x.m_a.m_value)
            GetReg(x.m_r)
            Put(ADDI.getValue(), x.m_r.m_value, 0, x.m_a.m_value)
    x.m_mode = REG.getValue()

def loadBool(x):
    if x.m_type.m_form != BOOLEAN.getValue():
        OSS.Mark("Boolean?")
    load(x)
    x.m_mode = COND.getValue()
    x.m_a.m_value = 0
    x.m_b.m_value = 0
    x.m_c = 1

def PutOp(cd, x, y):
    r = Variable(0)
    if x.m_mode != REG.getValue():
        load(x)
    if x.m_r.m_value == 0:
        GetReg(x.m_r)
        r.m_value = 0
    else:
        r.m_value = x.m_r.m_value
    if y.m_mode == CONST.getValue():
        TestRange(y.m_a.m_value)
        Put(cd + 16, r.m_value, x.m_r.m_value, y.m_a.m_value)
    else:
        if y.m_mode != REG.getValue():
            load(y)
        Put(cd, x.m_r.m_value, r.m_value, y.m_r.m_value)
        EXCL(regs, y.m_r.m_value)

def negated(cond):
    if ODD(cond):
        return (cond - 1)
    else:
        return cond + 1

def merged(L0, L1):
    L2 = Variable(0)
    L3 = Variable(1)
    if L0 != 0:
        L2.m_value = L0
        while True:
            L3.m_value = code.m_value[L2.m_value] % 0x10000
            if L3.m_value == 0:
                break
            L2.m_value = L3.m_value
        code.m_value[L2.m_value] = code.m_value[L2.m_value] - L3.m_value + L1
        return L0
    else:
        return L1

def fix(at, With):
    code.m_value[at] = code.m_value[at] / 0x10000 * 0x10000 + (With % 0x10000)

def FixLink(L):
    L1 = Variable(0)
    while L.m_value != 0:
        L1.m_value = code.m_value[L.m_value] % 0x10000
        fix(L.m_value, pc.m_value - L.m_value)
        L.m_value = L1.m_value

def Op1(op, x):
    t = Variable(0)
    if op == OSS.MINUS.getValue():
        if x.m_type.m_form != INTEGER.getValue():
            OSS.Mark("bad type")
        elif x.m_mode == CONST.getValue():
            x.m_a.m_value = -x.m_a.m_value
        else:
            if x.m_mode == VAR.getValue():
                load(x)
            Put(SUB.getValue(), x.m_r.m_value, 0, x.m_r.m_value)
    elif op == OSS.NOT.getValue():
        if x.m_mode!= COND.getValue():
            loadBool(x)
        x.m_c = negated(x.m_c)
        t.m_value = x.m_a.m_value
        x.m_a.m_value = x.m_b.m_value
        x.m_b.m_value = t.m_value
    elif op == OSS.AND.getValue():
        if x.m_mode != COND.getValue():
            loadBool(x)
        Put(BEQ.getValue() + negated(x.m_c), x.m_r.m_value, 0, x.m_a.m_value)
        EXCL(regs, x.m_r.m_value)
        x.m_a.m_value = pc.m_value - 1
        FixLink(x.m_b)
        x.m_b.m_value = 0
    elif op == OSS.OR.getValue():
        if x.m_mode != COND.getValue():
            loadBool(x)
        Put(BEQ.getValue() + x.m_c, x.m_r.m_value, 0, x.m_b.m_value)
        EXCL(regs, x.m_r.m_value)
        x.m_b.m_value = pc.m_value - 1
        FixLink(x.m_a)
        x.m_a.m_value = 0

def Op2(op, x, y):
    if x.m_type.m_form == INTEGER.getValue() and y.m_type.m_form == INTEGER.getValue():
        if x.m_mode == CONST.getValue() and y.m_mode == CONST.getValue():
            if op == OSS.PLUS.getValue():
                x.m_a.m_value += y.m_a.m_value
            elif op == OSS.MINUS.getValue():
                x.m_a.m_value += y.m_a.m_value
            elif op == OSS.TIMES.getValue():
                x.m_a.m_value = x.m_a.m_value * y.m_a.m_value
            elif op == OSS.DIV.getValue():
                x.m_a.m_value = x.m_a.m_value / y.m_a.m_value
            elif op == OSS.MOD.getValue():
                x.m_a.m_value = x.m_a.m_value % y.m_a.m_value
        else:
            if op == OSS.PLUS.getValue():
                PutOp(ADD.getValue(), x, y)
            elif op == OSS.MINUS.getValue():
                PutOp(SUB.getValue(), x, y)
            elif op == OSS.TIMES.getValue():
                PutOp(MUL.getValue(), x, y)
            elif op == OSS.DIV.getValue():
                PutOp(DIV.getValue(), x, y)
            elif op == OSS.MOD.getValue():
                PutOp(MOD.getValue(), x, y)
            else:
                OSS.Mark("bad type")
    elif x.m_type.m_form == BOOLEAN.getValue() and y.m_type.m_form == BOOLEAN.getValue():
        if y.m_mode != COND.getValue():
            loadBool(y)
        if op == OSS.OR.getValue():
            x.m_a.m_value = y.m_a.m_value
            x.m_b.m_value = merged(y.m_b.m_value, x.m_b.m_value)
            x.m_c = y.m_c
        elif op == OSS.AND.getValue():
            x.m_a.m_value = merged(y.m_a.m_value, x.m_a.m_value)
            x.m_b.m_value = y.m_b.m_value
            x.m_c = y.m_c
    else:
        OSS.Mark("bad type")

def Relation(op, x, y):
    if x.m_type.m_form != INTEGER.getValue() or y.m_type.m_form != INTEGER.getValue():
        OSS.Mark("bad type")
    else:
        if y.m_mode == CONST.getValue() and y.m_a.m_value == 0:
            load(x)
        else:
            PutOp(CMP.getValue(), x ,y)
        x.m_c = op.m_value - OSS.EQL.getValue()
        EXCL(regs, y.m_r.m_value)
    x.m_mode = COND.getValue()
    x.m_type = boolType.m_value
    x.m_a.m_value = 0
    x.m_b.m_value = 0

def Store(x, y):
    r = Variable(0)
    if x.m_type.m_form in {BOOLEAN.getValue(), INTEGER.getValue()} and (x.m_type.m_form == y.m_type.m_form):
        if y.m_mode == COND.getValue():
            Put(BEQ.getValue() + negated(y.m_c), y.m_r.m_value, 0, y.m_a.m_value)
            EXCL(regs, y.m_r.m_value)
            y.m_a.m_value = pc.m_value - 1
            FixLink(y.m_b)
            GetReg(y.m_r)
            Put(ADDI.getValue(), y.m_r.m_value, 0, 1)
            Put(BEQ.getValue(), 0, 0, 2)
            FixLink(y.m_a)
            Put(ADDI.getValue(), y.m_r.m_value, 0, 0)
        elif y.m_mode != REG.getValue():
            load(y)
        if x.m_mode == VAR.getValue():
            if x.m_lev == 0:
                rel.m_value[relx.m_value] = SHORT(pc.m_value)
                INC(relx)
            Put(STW.getValue(), y.m_r.m_value, x.m_r.m_value, x.m_a.m_value)
        else:
            OSS.Mark("illegal assignment")
        EXCL(regs, x.m_r.m_value)
        EXCL(regs, y.m_r.m_value)
    else:
        OSS.Mark("incompatible assignment")

def Parameter(x, ftyp, Class):
    r = Variable(0)
    if x.m_type == ftyp.m_value:
        if Class == PAR.getValue():
            if x.m_mode == VAR.getValue():
                if x.m_a != 0:
                    if x.m_lev == 0:
                        rel.m_value[relx.m_value] = SHORT(pc.m_value)
                        INC(relx)
                    GetReg(r)
                    Put(ADDI.getValue(), r.m_value, x.m_r.m_value, x.m_a.m_value)
                else:
                    r.m_value = x.m_r.m_value
            else:
                OSS.Mark("illegal parameter mode")
            Put(PSH.getValue(), r.m_value, SP.getValue(), 4)
            EXCL(regs, r.m_value)
        else:
            if x.m_mode != REG.getValue():
                load(x)
            Put(PSH.getValue(), x.m_r.m_value, SP.getValue(), 4)
            EXCL(regs, x.m_r.m_value)
    else:
        OSS.Mark("bad parameter type")

def CJump(x):
    if x.m_type.m_form == BOOLEAN.getValue():
        if x.m_mode != COND.getValue():
            loadBool(x)
        Put(BEQ.getValue() + negated(x.m_c), x.m_r.m_value, 0, x.m_a.m_value)
        EXCL(regs, x.m_r.m_value)
        FixLink(x.m_b)
        x.m_a.m_value = pc.m_value - 1
    else:
        OSS.Mark("Boolean?")
        x.m_a.m_value = pc.m_value

def BJump(L):
    Put(BEQ.getValue(), 0, 0, L.m_value - pc.m_value)

def FJump(L):
    Put(BEQ.getValue(), 0, 0, L.m_value)
    L.m_value = pc.m_value - 1

def Call(x):
    Put(BSR.getValue(), 0, 0, x.m_a.m_value - pc.m_value)

def IOCall(x, y):
    z = Item()
    if x.m_a.m_value < 4:
        if y.m_type.m_form != INTEGER.getValue():
            OSS.Mark("Integer?")
    if x.m_a.m_value == 1:
        GetReg(z.m_r)
        z.m_mode = REG.getValue()
        z.m_type = intType.m_value
        Put(RD.getValue(), z.m_r.m_value, 0, 0)
        Store(y, z)
    elif x.m_a.m_value == 2:
        load(y)
        Put(WRD.getValue(), 0, 0, y.m_r.m_value)
        EXCL(regs, y.m_r.m_value)
    elif x.m_a.m_value == 3:
        load(y)
        Put(WRH.getValue(), 0, 0, y.m_r.m_value)
        EXCL(regs, y.m_r.m_value)
    else:
        Put(WRL.getValue(), 0, 0, 0)

def Decode():
    for i in code.m_value:
        if i != 0:
            # Debug
            print unpack('i', pack('I', (i & 0xffffffff)))[0]


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
