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
    pass

def EXCL(Set, element):
    Set.m_value.discard(element)

def INCL(Set, element):
    Set.m_value.add(element)

def ASH(var, shiftPos):
    var = var << shiftPos

def DEC(operand, decrement = None):
    if decrement is None:
        operand.m_value -= 1
    else:
        operand.m_value -= decrement