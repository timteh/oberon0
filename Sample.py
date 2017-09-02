# Author: Timothy Teh

# This file executes the compiler by 
# passing the file handle to "source.mod" to it

import compiler

fh = open("source.mod", 'r')

print fh.seek(5)
print fh.read(1)
print fh.read(1)
print fh.read(1)
print fh.read(1)
print fh.read(1)
print fh.tell()
fh.close()