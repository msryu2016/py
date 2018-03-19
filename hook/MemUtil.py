import sys
import ctypes
from ctypes import *
from ctypes import wintypes
import winappdbg
from winappdbg import System, win32
from privileges import set_privilege

class PROCESSENTRY32(Structure):
    _fields_ = [ ( 'dwSize' , c_uint ) ,
                 ( 'cntUsage' , c_uint) ,
                 ( 'th32ProcessID' , c_uint) ,
                 ( 'th32DefaultHeapID' , c_uint) ,
                 ( 'th32ModuleID' , c_uint) ,
                 ( 'cntThreads' , c_uint) ,
                 ( 'th32ParentProcessID' , c_uint) ,
                 ( 'pcPriClassBase' , c_long) ,
                 ( 'dwFlags' , c_uint) ,
                 ( 'szExeFile' , c_char * 260 ) ,
                 ( 'th32MemoryBase' , c_long) ,
                 ( 'th32AccessKey' , c_long ) ]


class MODULEENTRY32(Structure):
    _fields_ = [ ( 'dwSize' , c_long ) ,
                ( 'th32ModuleID' , c_long ),
                ( 'th32ProcessID' , c_long ),
                ( 'GlblcntUsage' , c_long ),
                ( 'ProccntUsage' , c_long ) ,
                ( 'modBaseAddr' , c_long ) ,
                ( 'modBaseSize' , c_long ) ,
                ( 'hModule' , c_void_p ) ,
                ( 'szModule' , c_char * 256 ),
                ( 'szExePath' , c_char * 260 ) ]

class THREADENTRY32(Structure):
    _fields_ = [
        ('dwSize' , c_long ),
        ('cntUsage' , c_long),
        ('th32ThreadID' , c_long),
        ('th32OwnerProcessID' , c_long),
        ('tpBasePri' , c_long),
        ('tpDeltaPri' , c_long),
        ('dwFlags' , c_long) ]
class LUID(ctypes.Structure):
    _fields_ = [
        ('low_part', wintypes.DWORD),
        ('high_part', wintypes.LONG),
        ]

    def __eq__(self, other):
        return (
            self.high_part == other.high_part and
            self.low_part == other.low_part
            )

    def __ne__(self, other):
        return not (self==other)


SE_PRIVILEGE_ENABLED_BY_DEFAULT = (0x00000001)
SE_PRIVILEGE_ENABLED            = (0x00000002)
SE_PRIVILEGE_REMOVED            = (0x00000004)
SE_PRIVILEGE_USED_FOR_ACCESS    = (0x80000000)

class LUID_AND_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ('LUID', LUID),
        ('attributes', wintypes.DWORD),
        ]

    def is_enabled(self):
        return bool(self.attributes & SE_PRIVILEGE_ENABLED)

    def enable(self):
        self.attributes |= SE_PRIVILEGE_ENABLED

    def get_name(self):
        size = wintypes.DWORD(10240)
        buf = ctypes.create_unicode_buffer(size.value)
        res = ctypes.windll.advapi32.LookupPrivilegeNameW(None, self.LUID, buf, size)
        if res == 0: raise RuntimeError
        return buf[:size.value]

    def __str__(self):
        res = self.get_name()
        if self.is_enabled(): res += ' (enabled)'
        return res

class TOKEN_PRIVILEGES(ctypes.Structure):
    _fields_ = [
        ('count', wintypes.DWORD),
        ('privileges', LUID_AND_ATTRIBUTES*0),
        ]

    def get_array(self):
        array_type = LUID_AND_ATTRIBUTES*self.count
        privileges = ctypes.cast(self.privileges, ctypes.POINTER(array_type)).contents
        return privileges

    def __iter__(self):
        return iter(self.get_array())

PTOKEN_PRIVILEGES = ctypes.POINTER(TOKEN_PRIVILEGES)




class MemUtil:

    PAGE_READWRITE = 0x04
    PROCESS_ALL_ACCESS = ( 0x00F0000 | 0x00100000 | 0xFFF )
    VIRTUAL_MEM = ( 0x1000 | 0x2000 )

    TH32CS_SNAPPROCESS = 2
    STANDARD_RIGHTS_REQUIRED = 0x000F0000
    SYNCHRONIZE = 0x00100000
    PROCESS_ALL_ACCESS = (STANDARD_RIGHTS_REQUIRED | SYNCHRONIZE | 0xFFF)
    TH32CS_SNAPMODULE = 0x00000008
    TH32CS_SNAPMODULE32 = 0x00000010
    TH32CS_SNAPTHREAD = 0x00000004



    def __init__(self, pid):
        self.kernel32 = windll.kernel32
        self.advapi32 = windll.advapi32
        self.getHandle(pid)

    def getHandle(self,pid):
        self.h_process = self.kernel32.OpenProcess( self.PROCESS_ALL_ACCESS, False, int(pid))

        if not self.h_process:
            print "[!] Couldn't get handle to PID: %s" %(pid)
            print "[!] Are you sure %s is a valid PID?" %(pid)
            sys.exit(0)


    def getProc(self):
        return self.h_process

    def write(self, h_process, contents):

        length = len(contents)

        addr = self.kernel32.VirtualAllocEx(h_process, 0, length, self.VIRTUAL_MEM, self.PAGE_READWRITE)
        written = c_int(0)

        self.kernel32.WriteProcessMemory(h_process, addr, contents, length, byref(written))

        return (addr, written)

    def getAddr(self, dll, func):

        h_kernel32 = self.kernel32.GetModuleHandleA(dll)
        h_loadlib = self.kernel32.GetProcAddress(h_kernel32, func)

        return h_loadlib

    def createThread(self, h_process, h_loadlib, addr):

        thread_id = c_ulong(0)

        if not self.kernel32.CreateRemoteThread(h_process, None, 0, h_loadlib, addr, 0, byref(thread_id)):
            print "[!] Failed to inject DLL, exit... %d" % self.kernel32.GetLastError()
            sys.exit(0)

        return thread_id

    def findPE32(self,pid):

        hProcessSnap = c_void_p(0)
        hProcessSnap = self.kernel32.CreateToolhelp32Snapshot( self.TH32CS_SNAPPROCESS , 0 )


        pe32 = PROCESSENTRY32()
        pe32.dwSize = sizeof( PROCESSENTRY32 )
        ret = self.kernel32.Process32First( hProcessSnap , pointer( pe32 ) )

        while ret :
            if pe32.th32ProcessID == long(pid):
                return pe32
            else:
                hProcess = self.kernel32.OpenProcess( self.PROCESS_ALL_ACCESS , 0 , pe32.th32ProcessID )
                ret = self.kernel32.Process32Next( hProcessSnap, pointer(pe32) )

    """
    def findModule(self, pid, module):
        hModuleSnap = c_void_p(0)
        me32 = MODULEENTRY32()
        me32.dwSize = sizeof(MODULEENTRY32)

        print "self.TH32CS_SNAPMODULE:", self.TH32CS_SNAPMODULE
        hModuleSnap = self.kernel32.CreateToolhelp32Snapshot( self.TH32CS_SNAPMODULE32, pid)

        print 'CreateToolhelp32Snapshot() Error on CreateToolhelp32Snapshot[%d]' % self.kernel32.GetLastError()

        ret = self.kernel32.Module32First( hModuleSnap, pointer(me32))

        if ret == 0:
            print 'findModule() Error on Module32First[%d]' % self.kernel32.GetLastError()
            self.kernel32.CloseHandle( hModuleSnap )
            return None

        while ret:
            print me32.szModule
            if module == me32.szModule or module == me32.szExePath:
                return me32

            ret = self.kernel32.Module32Next( hModuleSnap, pointer(me32))
#            print "   MODULE NAME:     %s"%             me32.szModule
#            print "   executable     = %s"%             me32.szExePath

        self.kernel32.CloseHandle( hModuleSnap )

        return me32
    """



    def get_process_token(self):
        """
        Get the current process token
        """

        token = wintypes.HANDLE()
        TOKEN_ALL_ACCESS = 0xf01ff
        res = self.advapi32.OpenProcessToken(self.kernel32.GetCurrentProcess(), TOKEN_ALL_ACCESS, token)
        if not res > 0:
            raise RuntimeError("Couldn't get process token")
        return token

    def get_luid(self, name):
        """
        Get the LUID for the SeCreateSymbolicLinkPrivilege
        """
        luid = LUID()
        res = self.advapi32.LookupPrivilegeValueA(None, name, luid)

        if not res > 0:
            print "LookupPrivilegeValue:", kernel32.GetLastError()
            raise RuntimeError("Couldn't lookup privilege value")
        return luid

    def request_debug_privileges(self, state=True, bIgnoreExceptions = False):
        try:
            self.request_privileges(win32.SE_DEBUG_NAME, state)
            return True
        except Exception, e:
            if not bIgnoreExceptions:
                raise
        return False

    def request_privileges(self, privileges, state=True):
        with win32.OpenProcessToken(win32.GetCurrentProcess(),win32.TOKEN_ADJUST_PRIVILEGES) as hToken:
            NewState = ( (priv, state) for priv in privileges )
            win32.AdjustTokenPrivileges(hToken, NewState)


    def set_privilege(self, name, enable=True):
        """
        Try to assign the privilege to the current process token.
        Return True if the assignment is successful.
        """
        # create a space in memory for a TOKEN_PRIVILEGES structure
        #  with one element
        size = ctypes.sizeof(TOKEN_PRIVILEGES)
        size += ctypes.sizeof(LUID_AND_ATTRIBUTES)
        buffer = ctypes.create_string_buffer(size)
        tp = ctypes.cast(buffer, ctypes.POINTER(TOKEN_PRIVILEGES)).contents
        tp.count = 1
        tp.get_array()[0].LUID = self.get_luid(name)
        tp.get_array()[0].Attributes = SE_PRIVILEGE_ENABLED if enable else 0
        token = get_process_token()
        res = self.advapi32.AdjustTokenPrivileges(token, False, tp, 0, None, None)
        if res == 0:
            print "AdjustTokenPrivileges:", kernel32.GetLastError()
            raise RuntimeError("Error in AdjustTokenPrivileges")

        ERROR_NOT_ALL_ASSIGNED = 1300
        return kernel32.GetLastError() != ERROR_NOT_ALL_ASSIGNED


    @staticmethod
    def inject(pid, dll):

        mu = MemUtil(pid)
        h_process = mu.getProc()
        lib = mu.getAddr("kernel32.dll", "LoadLibraryA")
        addr, written = mu.write(h_process, dll)

        ret = mu.createThread(h_process, lib, addr)

        return ret

    def scan_modules(self, pid, dllname):

        # It would seem easier to clear the snapshot first.
        # But then all open handles would be closed.
        found_bases = set()
        with win32.CreateToolhelp32Snapshot(win32.TH32CS_SNAPMODULE,pid) as hSnapshot:
            me = win32.Module32First(hSnapshot)
            while me is not None:

#                if me32.szModule == name or me32.szExePath :
                print me.szExePath, ">", me.szModule, ">", dllname
                if me.szExePath == dllname or me.szModule == dllname:
                    print me.szExePath
                    return me

                me = win32.Module32Next(hSnapshot)

        return None

    def findModule(self, pid, name):

        me32 = MODULEENTRY32()
        me32.dwSize = sizeof( MODULEENTRY32)

        snapshot = windll.kernel32.CreateToolhelp32Snapshot(win32.TH32CS_SNAPMODULE, pid)

        ret = windll.kernel32.Module32First( snapshot, pointer(me32) )
        if ret == 0:
            print("Error")
            windll.kernel32.CloseHandle(snapshot)
            return None

        while ret :
            if me32.szModule == name or me32.szExePath :
                return me32

            ret = windll.kernel32.Module32Next( snapshot , pointer(me32))
        windll.kernel32.CloseHandle(snapshot)
        return me32


    @staticmethod
    def eject(pid, dll):

        mu = MemUtil(pid)

        set_privilege(win32.SE_DEBUG_NAME)
        pe32 = PROCESSENTRY32()
        pe32.dwSize = sizeof( PROCESSENTRY32 )
        pe32= mu.findPE32(pid)

        if pe32 is None:
            print "[+] Module Not Found"
            sys.exit(-1)
        #h_process = mu.getHandle(pe32.th32ProcessID)
        h_process = mu.getProc()

        me32 = mu.scan_modules(pe32.th32ProcessID, dll)


        if me32 is None :
            print "[+] ME32 Not Found"
            sys.exit(-1)
        lib = mu.getAddr("kernel32.dll", "FreeLibrary")
        ret = mu.createThread(h_process, lib, me32.modBaseAddr)

        return ret

