from Util import *

# "constants"
HEAD = Constant(0)
VAR = Constant(1)
CONST = Constant(3)
TYP = Constant(5)
SPROC = Constant(7)

class Item:
    def __init__(self):
        self.m_mode = 0
        self.m_lev = 0
        self.m_type = None# Pointer to TypeDesc
        self.m_a = 0
        self.m_b = 0
        self.m_c = 0
        self.m_d = 0

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
        self.m_fields = None # Pointer to ObjDesc
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
regs = Variable(None)

def Open():
    curlev.m_value = 0
    pc.m_value = 0
    relx.m_value = 0
    cno.m_value = 0
    regs.m_value = set()