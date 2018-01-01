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
M = Variable(MEMSIZE.getValue()/4*[0])

def Load(code, len):
    i = Variable(0)
    while i.m_value < len:
        M.m_value[i.m_value] = code[i.m_value]
        INC(i)

def Execute(pc0, In):
    pass

def State():
    print "PC={:>8}".format(PC.m_value * 4)
    print "SP={:>8}".format(R.m_value[30] * 4)
    print "FP={:>8}".format(R.m_value[29] * 4)
    print "R1={:>8}".format(R.m_value[1] * 4)
    print "R2={:>8}".format(R.m_value[2] * 4)
    print "R3={:>8}".format(R.m_value[3] * 4)
    print "R4={:>8}".format(R.m_value[4] * 4)
