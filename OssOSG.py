from Util import *

# "constants"
HEAD = Constant(0)
VAR = Constant(1)
CONST = Constant(3)
TYP = Constant(5)
SPROC = Constant(7)

class Item:
    mode = 0
    lev = 0
    _type = 0 # Pointer to TypeDesc
    a = 0
    b = 0
    c = 0
    d = 0

class ObjDesc:
    _class = 0
    lev = 0
    _next = 0 # Pointer to ObjDesc
    dsc = 0 # Pointer to ObjDesc
    _type = 0 # Pointer to TypeDesc
    name = 0
    val = 0

class TypeDesc:
    form = 0
    fields = 0 # Pointer to ObjDesc
    base = 0 # Pointer to TypeDesc
    size = 0
    len = 0

# Global variables
intType  = [None] #pointer to TypeDesc
boolType = [None] #pointer to TypeDesc
curlev = [0]
pc = [0]
relx = [0]
cno = [0]
regs = [None]

def Open():
    curlev[0] = 0
    pc[0] = 0
    relx[0] = 0
    cno[0] = 0
    regs[0] = set()