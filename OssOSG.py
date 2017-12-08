
class Item:
    mode = 0
    lev = 0
    _type = [None]
    a = 0
    b = 0
    c = 0
    d = 0

class ObjDesc:
    _class = 0
    lev = 0
    _next = [None]
    _dsc = [None]
    name = [None]
    val = 0

class TypeDesc:
    form = 0
    fields = [None]
    base = [None]
    size = 0
    len = 0