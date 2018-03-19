# -*- coding: utf-8 -*-
from winappdbg import System, version, HexDump, win32, Process
import sys, time


"""
for path in sys.path:
    print path

print sys.builtin_module_names
for module in sys.modules:
    print module
"""
def usage():
    print "usage: %s [i/e] [pid] [dll]"
    sys.exit(0)

if len(sys.argv)<3:
    usage()

mod = sys.argv[1]
pid = int(sys.argv[2])
dllname = str(sys.argv[3])

p = Process( pid )

if mod == 'i':
    p.inject_dll(dllname, bWait = False)
elif mod == 'e':
    p.eject_dll(dllname, bWait = False)
else:
    p.test(dllname)
    usage()


