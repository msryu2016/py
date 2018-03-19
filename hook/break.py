from winappdbg import Process, System, Thread, win32
import os, sys, time
from winappdbg.process import _ProcessContainer
from winappdbg.module import Module, _ModuleContainer
from ctypes import *
import winappdbg



def main():

    pid = int(sys.argv[1])
    addr = sys.argv[2]
    debug = winappdbg.Debug( winappdbg.EventHandler() )

    try:
        debug.attach( pid )
        #debug.break_at(pid, addr)
        #debug.interactive()
        #self.debug.loop()
    finally:
        debug.stop()

if __name__ == '__main__':
    main()