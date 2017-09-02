
def OpenReader(R, filename, pos): #R is the filehandle, a reference
    R[0] = open(filename, 'r')
    R[0].seek(pos)

# reads only 1 character in a file
def Read(filehandle, ch): # ch is a reference
    ch[0] = filehandle.read(1)

def Close(filehandle):
    filehandle.close()