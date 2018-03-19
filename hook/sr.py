# -*- coding: utf-8 -*-
import sys, time
from hack import Hack, print_thread
import winapputil
from winappdbg import Thread, HexDump, CrashDump, System, Process

def pre_suspend(event):
    process = event.get_process()
    print "pre_suspend"
    process.suspend()

def pre_resume(event):
    process = event.get_process()
    print "pre_resume"
    process.resume()

h = Hack(pid=sys.argv[1])


h.wait(int(sys.argv[2]))


#h.add_hook('kernel32', "CreateFileW", func)
#h.add_hook('kernel32', 'WriteProcessMemory', func)
#h.add_hook('kernel32', 'CreateRemoteThread', pre_CreateRemoteThread)
#h.add_hook('kernel32', 'CreateProcessInternalW', pre_createprocess);
#h.add_hook('kernel32', 'Sleep', pre_Sleep);
#h.add_hook('wininet', 'InternetConnectW', pre_InternetConnectW);
#h.add_hook("wininet", "HttpOpenRequest", pre_HttpOpenRequest)


h.safe_exit()