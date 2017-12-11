
def OpenReader(R, filename, pos): #R is the filehandle, a reference
    R.m_value = open(filename, 'r')
    R.m_value.seek(pos)

# reads only 1 character in a file
def Read(filehandle, ch): # filehandle, ch is a reference
    ch.m_value = filehandle.m_value.read(1)

def Close(filehandle):
    filehandle.close()