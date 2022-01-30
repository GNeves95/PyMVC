from sys import platform

from enum import Enum

class OpSys(Enum):
	Windows = 1
	Linux = 2
	Mac = 3
	Unknown = 4

opSys = None

if platform == "linux" or platform == "linux2":
    opSys = OpSys.Linux
elif platform == "darwin":
    opSys = OpSys.Mac
elif platform == "win32":
    opSys = OpSys.Windows
else:
	opSys = OpSys.Unknown