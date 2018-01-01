# A python port of the Oberon-0 compiler, as detailed in Professor Niklaus Wirth's book,
# Compiler Construction - http://www-oldurls.inf.ethz.ch/personal/wirth/CompilerConstruction/index.html
__author__ = "Timothy Teh"
__email__ = "timothytehsw@gmail.com"
__version__ = "0.0.1"

def OpenReader(R, filename, pos): #R is the filehandle, a reference
    R.m_value = open(filename, 'r')
    R.m_value.seek(pos)

# reads only 1 character in a file
def Read(filehandle, ch): # filehandle, ch is a reference
    ch.m_value = filehandle.m_value.read(1)

def Close(filehandle):
    filehandle.close()