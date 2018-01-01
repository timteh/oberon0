# A python port of the Oberon-0 compiler, as detailed in Professor Niklaus Wirth's book,
# Compiler Construction - http://www-oldurls.inf.ethz.ch/personal/wirth/CompilerConstruction/index.html
__author__ = "Timothy Teh"
__email__ = "timothytehsw@gmail.com"
__version__ = "0.0.1"

import OssBB as Oberon
import OssBB as Texts
from Util import *

# "constants"
IDLEN = Constant(16)
KW = Constant(34)
# #symbols
NULL = Constant(0)
TIMES = Constant(1)
DIV = Constant(3)
MOD = Constant(4)
AND = Constant(5) 
PLUS = Constant(6)
MINUS = Constant(7)
OR = Constant(8)
EQL = Constant(9) 
NEQ = Constant(10)
LSS = Constant(11)
GEQ = Constant(12)
LEQ = Constant(13)
GTR = Constant(14)
PERIOD = Constant(18)
COMMA = Constant(19) 
COLON = Constant(20)
RPAREN = Constant(22) 
RBRAK = Constant(23) 
OF = Constant(25)
THEN = Constant(26)
DO = Constant(27) 
LPAREN = Constant(29)
LBRAK = Constant(30)
NOT = Constant(32)
BECOMES = Constant(33)
NUMBER = Constant(34)
IDENT = Constant(37)
SEMICOLON = Constant(38)
END = Constant(40)
ELSE = Constant(41)
ELSIF = Constant(42)
IF = Constant(44)
WHILE = Constant(46)
ARRAY = Constant(54)
RECORD = Constant(55)
CONST = Constant(57)
TYPE = Constant(58)
VAR = Constant(59)
PROCEDURE = Constant(60)
BEGIN = Constant(61)
MODULE = Constant(63)
EOF = Constant(64)

# variables
val = Variable(0)
id = Variable([''] * IDLEN.getValue()) #array of char[Idlen]
error = Variable(False)
ch = Variable(' ')
nkw = Variable(0)
errpos = Variable(0)
R = Variable(None)
#W: Texts.Writer;

class keyTabRec:
    sym = 0
    id = "" # technically this should be immutable, copy array?

keyTab =  [keyTabRec() for x in range(KW.getValue())]

def Mark(msg):
    p = R.m_value.tell()
    if p > errpos.m_value:
        print "  pos " + str(p) + "  " + msg + "\n"
    errpos.m_value = p
    error.m_value = True

def Get(sym): #sym is a reference
    def Ident():
        i = 0 
        while True:
            # Read in all the characters of the identifier
            if i < IDLEN.getValue():
                id.m_value[i] = ch.m_value
                i = i + 1
            Texts.Read(R, ch)
            if ((ch.m_value < '0') or (ch.m_value > '9')) and ((ch.m_value.upper() < 'A') or (ch.m_value.upper() > 'Z')):
                break
        while i < IDLEN.getValue():
            id.m_value[i] = ''
            i += 1
        k = 0
        while (k < nkw.m_value) and (''.join(id.m_value) != keyTab[k].id):
            k = k + 1
        if k < nkw.m_value:
            sym.m_value = keyTab[k].sym
        else:
            sym.m_value = IDENT.getValue()

    def Number():
        val.m_value = 0
        sym.m_value = NUMBER.getValue()
        while True:
            # LONGINT is defined as INT32 in this program -  LONGINT = Oberon.INT32
            # Test to see if adding the next tenth digit will exceed INT32
            if val.m_value <= ((2147483647 - ord(ch.m_value) + ord('0')) / 10):
                val.m_value = 10 * val.m_value + (ord(ch.m_value) - ord('0'))
            else:
                Mark("number too large")
                val.m_value = 0
            Texts.Read(R, ch)
            if (ch.m_value < '0') or (ch.m_value > '9'):
                break

    def comment():
        Texts.Read(R, ch)
        while True:
            while True:
                while ch.m_value == '(':
                    Texts.Read(R, ch)
                    if ch.m_value == '*':
                        comment()
                if ch.m_value == '*':
                    Texts.Read(R, ch)
                    break
                if ch.m_value == '':
                    break
                Texts.Read(R, ch)
            if ch.m_value == ')':
                Texts.Read(R, ch)
                break
            if ch.m_value == '':
                Mark("comment not terminated")
                break

    # start of Get function proper
    while (ch.m_value != '' and ch.m_value <= ' '):
        Texts.Read(R, ch)
    if ch.m_value == '':
        sym.m_value = EOF.getValue()
    else:
        # "switch case" here
        if ch.m_value == '&':
            Texts.Read(R, ch)
            sym.m_value = AND.getValue()
        elif ch.m_value == '*':
            Texts.Read(R, ch)
            sym.m_value = TIMES.getValue()
        elif ch.m_value == '+':
            Texts.Read(R, ch)
            sym.m_value = PLUS.getValue()
        elif ch.m_value == '-':
            Texts.Read(R, ch)
            sym.m_value = MINUS.getValue()
        elif ch.m_value == '=':
            Texts.Read(R, ch)
            sym.m_value = EQL.getValue()
        elif ch.m_value == '#':
            Texts.Read(R, ch)
            sym.m_value = NEQ.getValue()
        elif ch.m_value == '<':
            Texts.Read(R, ch)
            if ch.m_value == '=':
                Texts.Read(R, ch)
                sym.m_value = LEQ.getValue()
            else:
                sym.m_value = LSS.getValue()
        elif ch.m_value == '>':
            Texts.Read(R, ch)
            if ch.m_value == '=':
                Texts.Read(R, ch)
                sym.m_value = GEQ.getValue()
            else:
                sym.m_value = GTR.getValue()
        elif ch.m_value == ';':
            Texts.Read(R, ch)
            sym.m_value = SEMICOLON.getValue()
        elif ch.m_value == ',':
            Texts.Read(R, ch)
            sym.m_value = COMMA.getValue()
        elif ch.m_value == ':':
            Texts.Read(R, ch)
            if ch.m_value == '=':
                Texts.Read(R, ch)
                sym.m_value = BECOMES.getValue()
            else:
                sym.m_value = COLON.getValue()
        elif ch.m_value == '.':
            Texts.Read(R, ch)
            sym.m_value = PERIOD.getValue()
        elif ch.m_value == '(':
            Texts.Read(R, ch)
            if ch.m_value == '*':
                comment()
                Get(sym)
            else:
                sym.m_value = LPAREN.getValue()
        elif ch.m_value == ')':
            Texts.Read(R, ch)
            sym.m_value = RPAREN.getValue()
        elif ch.m_value == '[':
            Texts.Read(R, ch)
            sym.m_value = LBRAK.getValue()
        elif ch.m_value == ']':
            Texts.Read(R, ch)
            sym.m_value = RBRAK.getValue()
        elif ch.m_value.isdigit():
            Number()
        elif ch.m_value.isalpha():
            Ident()
        elif ch.m_value == '~':
            Texts.Read(R, ch)
            sym.m_value = NOT.getValue()
        else:
            Texts.Read(R, ch)
            sym.m_value = NULL.getValue()

def Init(filename, pos):
  error.m_value = False
  errpos.m_value = pos
  Texts.OpenReader(R, filename, pos)
  Texts.Read(R, ch)
  

def EnterKW(sym, name):
    keyTab[nkw.m_value].sym = sym
    keyTab[nkw.m_value].id = name
    nkw.m_value+=1

# BEGIN
error.m_value = True
nkw.m_value = 0
EnterKW(NULL.getValue(), "BY")
EnterKW(DO.getValue(), "DO")
EnterKW(IF.getValue(), "IF")
EnterKW(NULL.getValue(), "IN")
EnterKW(NULL.getValue(), "IS")
EnterKW(OF.getValue(), "OF")
EnterKW(OR.getValue(), "OR")
EnterKW(NULL.getValue(), "TO")
EnterKW(END.getValue(), "END")
EnterKW(NULL.getValue(), "FOR")
EnterKW(MOD.getValue(), "MOD")
EnterKW(NULL.getValue(), "NIL")
EnterKW(VAR.getValue(), "VAR")
EnterKW(NULL.getValue(), "CASE")
EnterKW(ELSE.getValue(), "ELSE")
EnterKW(NULL.getValue(), "EXIT")
EnterKW(THEN.getValue(), "THEN")
EnterKW(TYPE.getValue(), "TYPE")
EnterKW(NULL.getValue(), "WITH")
EnterKW(ARRAY.getValue(), "ARRAY")
EnterKW(BEGIN.getValue(), "BEGIN")
EnterKW(CONST.getValue(), "CONST")
EnterKW(ELSIF.getValue(), "ELSIF")
EnterKW(NULL.getValue(), "IMPORT")
EnterKW(NULL.getValue(), "UNTIL")
EnterKW(WHILE.getValue(), "WHILE")
EnterKW(RECORD.getValue(), "RECORD")
EnterKW(NULL.getValue(), "REPEAT")
EnterKW(NULL.getValue(), "RETURN")
EnterKW(NULL.getValue(), "POINTER")
EnterKW(PROCEDURE.getValue(), "PROCEDURE")
EnterKW(DIV.getValue(), "DIV")
EnterKW(NULL.getValue(), "LOOP")
EnterKW(MODULE.getValue(), "MODULE")
# END OssOSS.