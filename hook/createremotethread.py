from MemUtil import MemUtil
import os, sys
#0x7754f7e8L

import ctypes
from ctypes import *
from ctypes import wintypes


PAGE_READWRITE = 0x04
PROCESS_ALL_ACCESS = ( 0x00F0000 | 0x00100000 | 0xFFF )
VIRTUAL_MEM = ( 0x1000 | 0x2000 )


addr = 0x015d0000L

kernel32 = windll.kernel32

pid = sys.argv[1]

h_kernel32 = kernel32.GetModuleHandleA('kernel32.dll')
h_loadlib = kernel32.GetProcAddress(h_kernel32, 'LoadLibraryEx')

h_process = kernel32.OpenProcess( PROCESS_ALL_ACCESS, False, int(pid))


thread_id = c_ulong(0)
if not kernel32.CreateRemoteThread(h_process, None, 0, h_loadlib, addr, 0, byref(thread_id)):
    print "[!] Failed to inject DLL, exit... %d" % self.kernel32.GetLastError()
    sys.exit(0)

print "0x%08x" % addr
print "%s" % thread_id
print "done"

#mu = MemUtil(pid)
#h_process = mu.getProc()
#lib = mu.getAddr("C:\\Program Files\\Google\\Chrome\\Application\\64.0.3282.186\\chrome.dll", "GetHandleVerifier")
#addr, written = mu.write(h_process, dll)

#ret = mu.createThread(h_process, lib, None)