# A python port of the Oberon-0 compiler, as detailed in Professor Niklaus Wirth's book,
# Compiler Construction - http://www-oldurls.inf.ethz.ch/personal/wirth/CompilerConstruction/index.html
__author__ = "Timothy Teh"
__email__ = "timothytehsw@gmail.com"
__version__ = "0.0.1"

# Define a class to handle variables
class Variable:
    def __init__(self, initialValue):
        self.m_value = initialValue

class Pointer:
    def __init__(self, initialValue):
        self.m_pValue = initialValue
        self.m_value = None

class Constant:
    def __init__(self, value):
        self.__const = value
    def getValue(self):
        return self.__const

# Predeclared procedures of component pascal
def NEW(pointer):
    pointer.m_value = pointer.m_pValue()

def INC(var, increment = None):
    if increment is None:
        var.m_value += 1
    else:
        var.m_value += increment

def SHORT(var):
    return var

def EXCL(Set, element):
    Set.m_value.discard(element)

def INCL(Set, element):
    Set.m_value.add(element)

def ASH(var, shiftPos):
    var = var << shiftPos
    return var

def DEC(operand, decrement = None):
    if decrement is None:
        operand.m_value -= 1
    else:
        operand.m_value -= decrement

def ODD(var):
    if (var % 2) == 0:
        return False
    else:
        return True