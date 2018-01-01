from Util import *
import OssBB as Texts
import OssBB as Oberon

# Constants
MEMSIZE = Constant(4096)
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

# Variables
PC = Variable(0)
IR = Variable(0)
R = Variable(32 * [0])
M = Variable(MEMSIZE.getValue() / 4 * [0])

def Load(code, len):
    i = Variable(0)
    while i.m_value < len:
        M.m_value[i.m_value] = code[i.m_value]
        INC(i)

def Execute(pc0, In):
    R.m_value[31] = 0
    PC.m_value = pc0 / 4
    ScanIndex = 0
    while True:
        R.m_value[0] = 0
        nxt = PC.m_value + 1
        IR.m_value = M.m_value[PC.m_value]
        opc = IR.m_value / 0x4000000 % 0x40
        a = IR.m_value / 0x200000 % 0x20
        b = IR.m_value / 0x10000 % 0x20
        c = IR.m_value % 0x10000
        if opc < ADDI.getValue():
            c = R.m_value[c % 0x20]
        elif c >= 0x8000:
            c -= 0x10000 #sign extension 16 to 32 bit
        if opc == ADD.getValue() or opc == ADDI.getValue():
            R.m_value[a] = R.m_value[b] + c
        elif opc == SUB.getValue() or opc == SUBI.getValue() or opc == CMP.getValue() or opc == CMPI.getValue():
            R.m_value[a] = R.m_value[b] - c
        elif opc == MUL.getValue() or opc == MULI.getValue():
            R.m_value[a] = R.m_value[b] * c
        elif opc == DIV.getValue() or opc == DIVI.getValue():
            R.m_value[a] = R.m_value[b] / c
        elif opc == MOD.getValue() or opc == MODI.getValue():
            R.m_value[a] = R.m_value[b] % c
        elif opc == OR.getValue() or opc == ORI.getValue():
            R.m_value[a] = R.m_value[b] | c
        elif opc == BIC.getValue() or opc == BICI.getValue():
            R.m_value[a] = R.m_value[b] & ~c
        elif opc == XOR.getValue() or opc == XORI.getValue():
            R.m_value[a] = R.m_value[b] ^ c
        elif opc == LSH.getValue() or opc == LSHI.getValue():
            R.m_value[a] = R.m_value[b] << c
        elif opc == ASH1.getValue() or opc == ASHI.getValue():
            R.m_value[a] = R.m_value[b] >> c
        elif opc == CHK.getValue() or opc == CHKI.getValue():
            if R.m_value[a] < 0 or R.m_value[a] >= c:
                print "Trap at {:2}".format(PC.m_value)
                break
        elif opc == LDW.getValue():
            R.m_value[a] = M.m_value[(R.m_value[b] + c) / 4]
        elif opc == LDB.getValue():
            R.m_value[a] = (M.m_value[(R.m_value[b] + c) / 4] << ((R.m_value[b] + c) % 4 * 8) % 0x100)
        elif opc == POP.getValue():
            R.m_value[a] = M.m_value[R.m_value[b] / 4]
            R.m_value[b] += c
        elif opc == STW.getValue():
            M.m_value[(R.m_value[b] + c) / 4] = R.m_value[a]
        elif opc == STB:
            pass # not implemented
        elif opc == PSH.getValue():
            R.m_value[b] -= c
            M.m_value[R.m_value[b] / 4] = R.m_value[a]
        elif opc == BEQ.getValue():
            if R.m_value[a] == R.m_value[b]:
                nxt = PC.m_value + c
        elif opc == BNE.getValue():
            if R.m_value[a] != R.m_value[b]:
                nxt = PC.m_value + c
        elif opc == BLT.getValue():
            if R.m_value[a] < R.m_value[b]:
                nxt = PC.m_value + c
        elif opc == BGE.getValue():
            if R.m_value[a] >= R.m_value[b]:
                nxt = PC.m_value + c
        elif opc == BLE.getValue():
            if R.m_value[a] <= R.m_value[b]:
                nxt = PC.m_value + c
        elif opc == BGT.getValue():
            if R.m_value[a] > R.m_value[b]:
                nxt = PC.m_value + c
        elif opc == BSR.getValue():
            nxt = PC.m_value + c
            R.m_value[31] = (PC.m_value + 1) * 4
        elif opc == JSR.getValue():
            nxt = IR.m_value % 0x4000000
            R.m_value[31] = (PC.m_value + 1) * 4
        elif opc == RET.getValue():
            nxt = R.m_value[c % 0x20] / 4
            if nxt == 0:
                break
        elif opc == RD.getValue():
            R.m_value[a] = int(In[ScanIndex])
            ScanIndex += 1
        elif opc == WRD.getValue():
            print " {:1}".format(R.m_value[c]),
        elif opc == WRH.getValue():
            print " {:x}".format(R.m_value[c]),
        elif opc == WRL.getValue():
            print ""
        PC.m_value = nxt

def State():
    print "PC={:>8}".format(PC.m_value * 4)
    print "SP={:>8}".format(R.m_value[30])
    print "FP={:>8}".format(R.m_value[29])
    print "R1={:>8}".format(R.m_value[1])
    print "R2={:>8}".format(R.m_value[2])
    print "R3={:>8}".format(R.m_value[3])
    print "R4={:>8}".format(R.m_value[4])
