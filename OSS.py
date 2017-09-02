#some ideas for data types
# constants: tuple of 1
# references : list of 1
# records: class
# global variabes : list of 1

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
R = None
#W: Texts.Writer;

class keyTabRec:
    sym = 0
    id = "" # technically this should be immutable, copy array?

keyTab =  [keyTabRec() for x in range(KW[0])]

def Mark(msg):
    p = R.tell()
    if p > errpos[0]:
        print "  pos " + str(p) + "  " + msg + "\n"
    errpos[0] = p
    error[0] = True

def Get(sym): #sym is a reference
    def Ident():
        i = 0 
        k = 0
        while True:
            if i < IdLen[0]:
                id[i] = ch[0]
                i = i + 1
            ch[0] = R.read(1)
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
            #LONGINT is defined as INT32 in this program -  LONGINT = Oberon.INT32
            if val[0] <= ((2147483647 - ord(ch[0]) + ord('0')) / 10):
                val[0] = 10 * val[0] + (ord(ch[0]) - ord('0'))
            else:
                Mark("number too large")
                val[0] = 0
            if (ch[0] < '0') or (ch[0] > '9'):
                break

        PROCEDURE Number;
    BEGIN val := 0; sym := number;
      REPEAT
        IF val <= (2147483647 - ORD(ch) + ORD("0")) DIV 10 THEN
          val := 10 * val + (ORD(ch) - ORD("0"))
        ELSE Mark("number too large"); val := 0
        END ;
        Texts.Read(R, ch)
      UNTIL (ch < "0") OR (ch > "9")
    END Number;

def Init(filename, pos):
  error[0] = False
  errpos[0] = pos
  R = open(filename, r)
  R.seek(pos)
  ch[0] = R.read(1)
  

def EnterKW(sym, name):
    keyTab[nkw[0]].sym = sym
    keyTab[nkw[0]].id = name
    nkw[0]+=1

# BEGIN
nkw[0] = 0
EnterKW(null[0], "BY")
EnterKW(do[0], "DO")
EnterKW(_if[0], "IF")
EnterKW(null[0], "IN")
EnterKW(null[0], "IS")
EnterKW(of[0], "OF")
EnterKW(_or[0], "OR")
EnterKW(null[0], "TO")
EnterKW(end[0], "END")
EnterKW(null[0], "FOR")
EnterKW(mod[0], "MOD")
EnterKW(null[0], "NIL")
EnterKW(var[0], "VAR")
EnterKW(null[0], "CASE")
EnterKW(_else[0], "ELSE")
EnterKW(null[0], "EXIT")
EnterKW(then[0], "THEN")
EnterKW(_type[0], "TYPE")
EnterKW(null[0], "WITH")
EnterKW(array[0], "ARRAY")
EnterKW(begin[0], "BEGIN")
EnterKW(const[0], "CONST")
EnterKW(elsif[0], "ELSIF")
EnterKW(null[0], "IMPORT")
EnterKW(null[0], "UNTIL")
EnterKW(_while[0], "WHILE")
EnterKW(record[0], "RECORD")
EnterKW(null[0], "REPEAT")
EnterKW(null[0], "RETURN")
EnterKW(null[0], "POINTER")
EnterKW(procedure[0], "PROCEDURE")
EnterKW(div[0], "DIV")
EnterKW(null[0], "LOOP")
EnterKW(module[0], "MODULE")
# END OssOSS.