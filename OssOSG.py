from Util import *

# "constants"
HEAD = Constant(0)
VAR = Constant(1)
CONST = Constant(3)
TYP = Constant(5)
SPROC = Constant(7)

class Item:
    m_mode = 0
    m_lev = 0
    m_type = 0 # Pointer to TypeDesc
    m_a = 0
    m_b = 0
    m_c = 0
    m_d = 0

class ObjDesc:
    m_class = 0
    m_lev = 0
    m_next = 0 # Pointer to ObjDesc
    m_dsc = 0 # Pointer to ObjDesc
    m_type = 0 # Pointer to TypeDesc
    m_name = 0
    val = 0

class TypeDesc:
    m_form = 0
    m_fields = 0 # Pointer to ObjDesc
    m_base = 0 # Pointer to TypeDesc
    m_size = 0
    m_len = 0

# Global variables
intType  = Variable(None) #pointer to TypeDesc
boolType = Variable(None) #pointer to TypeDesc
curlev = Variable(0)
pc = Variable(0)
relx = Variable(0)
cno = Variable(0)
regs = Variable(None)

def Open():
    curlev.m_value = 0
    pc.m_value = 0
    relx.m_value = 0
    cno.m_value = 0
    regs.m_value = set()