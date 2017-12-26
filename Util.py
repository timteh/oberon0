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

def NEW(pointer):
    pointer.m_value = pointer.m_pValue()