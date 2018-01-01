# Author: Timothy Teh

# This file executes the compiler by 
# passing the file handle to "source.mod" to it

import OssCompiler
# import OssOSS required to close the file
import OssOSS
import OssRISC

# Test compiler
OssCompiler.Compile()
OssCompiler.Decode()
OssCompiler.Load()
OssRISC.State()

# Execute the code
OssCompiler.Exec("Multiply 5 5")
OssCompiler.Exec("Divide 9 5")
OssCompiler.Exec("BinSearch 9 2 3 4 5 6 7 8 9 10 2")

#close the OSS file handle as stated above
OssOSS.R.m_value.close()
