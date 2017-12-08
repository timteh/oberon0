
# Author: Timothy Teh
# some ideas for data types
# constants: tuple of 1
# references : list of 1
# records: class
# global variabes : list of 1

import OssBB as Oberon
import OssBB as Texts

# "constants"
IdLen = (16,) 
KW = (34,)
# #symbols
null = (0,)
times = (1,)
div = (3,)
mod = (4,)
_and = (5,) 
plus = (6,)
minus = (7,)
_or = (8,)
eql = (9,) 
neq = (10,)
lss = (11,)
geq = (12,)
leq = (13,)
gtr = (14,)
period = (18,)
comma = (19,) 
colon = (20,)
rparen = (22,) 
rbrak = (23,) 
of = (25,)
then = (26,)
do = (27,) 
lparen = (29,)
lbrak = (30,)
_not = (32,)
becomes = (33,)
number = (34,)
ident = (37,) 
semicolon = (38,)
end = (40,)
_else = (41,)
elsif = (42,)
_if = (44,)
_while = (46,)
array = (54,)
record = (55,)
const = (57,)
_type = (58,)
var = (59,)
procedure = (60,)
begin = (61,)
module = (63,)
eof = (64,)

# variables
val = [0]
id = [''] * IdLen[0] #array of char[Idlen]
error = [False]
ch = [' ']
nkw = [0]
errpos = [0]
R = [None]
#W: Texts.Writer;

class keyTabRec:
    sym = 0
    id = "" # technically this should be immutable, copy array?

keyTab =  [keyTabRec() for x in range(KW[0])]

def Mark(msg):
    p = R[0].tell()
    if p > errpos[0]:
        print "  pos " + str(p) + "  " + msg + "\n"
    errpos[0] = p
    error[0] = True

def Get(sym): #sym is a reference
    def Ident():
        i = 0 
        k = 0
        while True:
            # Read in all the characters of the identifier
            if i < IdLen[0]:
                id[i] = ch[0]
                i = i + 1
            Texts.Read(R, ch)
            if ((ch[0] < '0') or (ch[0] > '9')) and ((ch[0].upper() < 'A') or (ch[0].upper() > 'Z')):
                break
        while (k < nkw[0]) and (''.join(id) != keyTab[k].id):
            k = k + 1
        if k < nkw[0]:
            sym[0] = keyTab[k].sym
        else:
            sym[0] = ident[0]

    def Number():
        val[0] = 0
        sym[0] = number[0]
        while True:
            # LONGINT is defined as INT32 in this program -  LONGINT = Oberon.INT32
            # Test to see if adding the next tenth digit will exceed INT32
            if val[0] <= ((2147483647 - ord(ch[0]) + ord('0')) / 10):
                val[0] = 10 * val[0] + (ord(ch[0]) - ord('0'))
            else:
                Mark("number too large")
                val[0] = 0
            Texts.Read(R, ch)
            if (ch[0] < '0') or (ch[0] > '9'):
                break

    def comment():
        Texts.Read(R, ch)
        while True:
            while True:
                while ch[0] == '(':
                    Texts.Read(R, ch)
                    if ch[0] == '*':
                        comment()
                if ch[0] == '*':
                    Texts.Read(R, ch)
                    break
                if ch[0] == '':
                    break
                Texts.Read(R, ch)
            if ch[0] == ')':
                Texts.Read(R, ch)
                break
            if ch[0] == '':
                Mark("comment not terminated")
                break

    # start of Get function proper
    while (ch[0] != '' and ch[0] <= ' '):
        Texts.Read(R, ch)
    if ch[0] == '':
        sym[0] = eof[0]
    else:
        # "switch case" here
        if ch[0] == '&':
            Texts.Read(R, ch)
            sym[0] = _and[0]
        elif ch[0] == '*':
            Texts.Read(R, ch)
            sym[0] = times[0]
        elif ch[0] == '+':
            Texts.Read(R, ch)
            sym[0] = plus[0]
        elif ch[0] == '-':
            Texts.Read(R, ch)
            sym[0] = minus[0]
        elif ch[0] == '=':
            Texts.Read(R, ch)
            sym[0] = eql[0]
        elif ch[0] == '#':
            Texts.Read(R, ch)
            sym[0] = neq[0]
        elif ch[0] == '<':
            Texts.Read(R, ch)
            if ch[0] == '=':
                Texts.Read(R, ch)
                sym[0] = leq[0]
            else:
                sym[0] = lss[0]
        elif ch[0] == '>':
            Texts.Read(R, ch)
            if ch[0] == '=':
                Texts.Read(R, ch)
                sym[0] = geq[0]
            else:
                sym[0] = gtr[0]
        elif ch[0] == ';':
            Texts.Read(R, ch)
            sym[0] = semicolon[0]
        elif ch[0] == ',':
            Texts.Read(R, ch)
            sym[0] = comma[0]
        elif ch[0] == ':':
            Texts.Read(R, ch)
            if ch[0] == '=':
                Texts.Read(R, ch)
                sym[0] = becomes[0]
            else:
                sym[0] = colon[0]
        elif ch[0] == '.':
            Texts.Read(R, ch)
            sym[0] = period[0]
        elif ch[0] == '(':
            Texts.Read(R, ch)
            if ch[0] == '*':
                comment()
                Get(sym)
            else:
                sym[0] = lparen[0]
        elif ch[0] == ')':
            Texts.Read(R, ch)
            sym[0] = rparen[0]
        elif ch[0] == '[':
            Texts.Read(R, ch)
            sym[0] = lbrak[0]
        elif ch[0] == ']':
            Texts.Read(R, ch)
            sym[0] = rbrak[0]
        elif ch[0].isdigit():
            Number()
        elif ch[0].isalpha():
            Ident()
        elif ch[0] == '~':
            Texts.Read(R, ch)
            sym[0] = _not[0]
        else:
            Texts.Read(R, ch)
            sym[0] = null[0]

def Init(filename, pos):
  error[0] = False
  errpos[0] = pos
  Texts.OpenReader(R, filename, pos)
  Texts.Read(R, ch)
  

def EnterKW(sym, name):
    keyTab[nkw[0]].sym = sym[0]
    keyTab[nkw[0]].id = name
    nkw[0]+=1

# BEGIN
error[0] = True
nkw[0] = 0
EnterKW(null, "BY")
EnterKW(do, "DO")
EnterKW(_if, "IF")
EnterKW(null, "IN")
EnterKW(null, "IS")
EnterKW(of, "OF")
EnterKW(_or, "OR")
EnterKW(null, "TO")
EnterKW(end, "END")
EnterKW(null, "FOR")
EnterKW(mod, "MOD")
EnterKW(null, "NIL")
EnterKW(var, "VAR")
EnterKW(null, "CASE")
EnterKW(_else, "ELSE")
EnterKW(null, "EXIT")
EnterKW(then, "THEN")
EnterKW(_type, "TYPE")
EnterKW(null, "WITH")
EnterKW(array, "ARRAY")
EnterKW(begin, "BEGIN")
EnterKW(const, "CONST")
EnterKW(elsif, "ELSIF")
EnterKW(null, "IMPORT")
EnterKW(null, "UNTIL")
EnterKW(_while, "WHILE")
EnterKW(record, "RECORD")
EnterKW(null, "REPEAT")
EnterKW(null, "RETURN")
EnterKW(null, "POINTER")
EnterKW(procedure, "PROCEDURE")
EnterKW(div, "DIV")
EnterKW(null, "LOOP")
EnterKW(module, "MODULE")
# END OssOSS.