# -*- coding: utf-8 -*-
import os, sys, time
from hack import Hack, print_thread
import winapputil
from winappdbg import Thread, HexDump, CrashDump, System, Process
"""
Hack.change_window_title("c:\windows\system32\cmd.exe", "Changed Notepad.exe")
time.sleep(1)
Hack.change_window_title("Changed Notepad.exe", "c:\windows\system32\cmd.exe")

# Winsock sockaddr structure.
class sockaddr(ctypes.Structure):
    _fields_ = [
        ("sa_family", ctypes.c_ushort),
        ("sa_data", ctypes.c_char * 14),
    ]

def sendto(event, ra, s, buf, length, flags, to, tolength):
    p = event.get_process()
    data = p.peek(buf, length)
    to_struct = p.read_structure(to, sockaddr)
    print "BUFFER DATA: " + repr(data) + "\n"
    print "ACCESSING SPECIFIC STRUCTURE sa_data field:", repr(to_struct.sa_data)
    print "PEEKING WHOLE STRUCTURE DATA:", repr(p.peek(to, tolength))


def sendto(event, ra, s, buf, length, flags, to, tolength):
    p = event.get_process()
    data = p.peek(buf, length)
    to_struct = p.read_structure(to, sockaddr)
    print "BUFFER DATA: " + repr(data) + "\n"
    print "ACCESSING SPECIFIC STRUCTURE sa_data field:", repr(to_struct.sa_data)
    print "PEEKING WHOLE STRUCTURE DATA:", repr(p.peek(to, tolength))

"""

"""
(
       LPCTSTR               lpFileName,
       DWORD                 dwDesiredAccess,
       DWORD                 dwShareMode,
  opt_ LPSECURITY_ATTRIBUTES lpSecurityAttributes,
       DWORD                 dwCreationDisposition,
       DWORD                 dwFlagsAndAttributes,
  opt_ HANDLE                hTemplateFile
)

int sendto(
         SOCKET                s,
   const char                  *buf,
         int                   len,
         int                   flags,
         const struct sockaddr *to,
         int                   tolen
);


    # Get the vararg parameters.
    count      = lpFmt.replace( '%%', '%' ).count( '%' )
    thread     = event.get_thread()
    if process.get_bits() == 32:
        parameters = thread.read_stack_dwords( count, offset = 3 )
    else:
        parameters = thread.read_stack_qwords( count, offset = 3 )

    # Show a message to the user.
    showparams = ", ".join( [ hex(x) for x in parameters ] )
    print "wsprintf( %r, %s );" % ( lpFmt, showparams )

def CreateFileA(event, ra, lpFileName, dwDesiredAccess,dwShareMode, lpSecurityAttributes, dwCreationDisposition,dwFlagsAndAttributes, hTemplateFile):
    #data = event.get_process().peek(buf, length)

    process = event.get_process()
    myFileName = process.peek_string(lpFileName, fUnicode=True)





    print "ra: " + str(ra) + "\n"
    print "lpFileName: " + str(myFileName) + "\n"
    print "event: " + str(event) + "\n"
    print "dwDesiredAccess: " + str(dwDesiredAccess) + "\n"
    print "dwShareMode: " + str(dwShareMode) + "\n"

    lpFileName = "C:\Users\psi\Documents\a1.txt"
    myFileName = process.peek_string(lpFileName, fUnicode=True)
    print "lpFileName: " + str(myFileName) + "\n"


h = Hack("notepad.exe")
h.add_hook("kernel32.dll", "CreateFileA", CreateFileA)
h.add_hook("kernel32.dll", "CreateFileW", CreateFileA)
h.hook()
h.safe_exit()
"""

"""
BOOL HttpSendRequest(hRequest,lpszHeaders,dwHeadersLength,lpOptional,dwOptionalLength):

HINTERNET HttpOpenRequest(
   HINTERNET hConnect,
   LPCTSTR   lpszVerb,
   LPCTSTR   lpszObjectName,
   LPCTSTR   lpszVersion,
   LPCTSTR   lpszReferer,
   LPCTSTR   *lplpszAcceptTypes,
   DWORD     dwFlags,
   DWORD_PTR dwContext
);

"""
def pre_HttpSendRequestW(event, ra, hRequest, lpszHeaders, dwHeadersLength, lpOptional, dwOptionalLength):
    #data = event.get_process().peek(buf, length)

    process = event.get_process()
    print "pid:" , str(event.get_pid())
    print(winapputil.utils.get_line())

    if dwHeadersLength != 0:
        print("HttpSendRequestW")
        print winapputil.utils.get_line()
        headers = process.peek_string(lpszHeaders, fUnicode=True)
        print headers

    if dwOptionalLength != 0:
        print winapputil.utils.get_line()
        optional = process.peek_string(lpOptional, fUnicode=False)
        print "Optional %s" % (optional)

    print(winapputil.utils.get_line())

def pre_HttpOpenRequest(event, ra, hConnect, lpszVerb,lpszObjectName, lpszVersion, lpszReferer,lplpszAcceptTypes, dwFlags, dwContext):
        process = event.get_process()

        verb = process.peek_string(lpszVerb, fUnicode=True)
        if verb is None:
            verb = "GET"

        obj = process.peek_string(lpszObjectName, fUnicode=True)

        #contents = process.read(buf, amount)
        #print("%s" % str(contents))

        print(winapputil.utils.get_line())
        print("HttpOpenRequestW")
        print("verb: %s" % verb)
        print("obj : %s" % obj)
        print(winapputil.utils.get_line())

results = {'instr' : {}, 'filehandle' : {}, 'urls' : [], 'procs' : [], 'wmi' : []}
stats = { 'str' : 0, 'url' : 0, 'filew' : 0, 'filer' : 0, 'wmi' : 0, 'proc' : 0 }

def pre_writeprocessmemory(event):

    thread = event.get_thread()
    proc = event.get_process()

    if proc.get_bits() == 32:
        hProc, lpBase, lpBuffer, nSize = thread.read_stack_dwords(5)[1:]
    else:
        context = thread.get_context()
        hProc = context['Rcx']
        lpBase = context['Rdx']
        lpBuffer = context['R8']
        nSize = context['R9']

    print "_in writeprocessmemory:", hex(lpBase)
    print context

"""
HANDLE WINAPI CreateRemoteThread(
  _In_  HANDLE                 hProcess,
  _In_  LPSECURITY_ATTRIBUTES  lpThreadAttributes,
  _In_  SIZE_T                 dwStackSize,
  _In_  LPTHREAD_START_ROUTINE lpStartAddress,
  _In_  LPVOID                 lpParameter,
  _In_  DWORD                  dwCreationFlags,
  _Out_ LPDWORD                lpThreadId
);
"""
def pre_CreateRemoteThread(event):

    thread = event.get_thread()
    print thread
    proc = event.get_process()
    print "in pre_CreateRemoteThread"
    if proc.get_bits() == 32:
        hProc, lpThread, dwStack, lpAddr, lpParam, dwFlag, lpTid = thread.read_stack_dwords(7)[1:]
        print thread.read_stack_dwords(7)[1:]
    else:
        context = thread.get_context()

        print context

def pre_createprocess(event):
    pass


def pre_createfilew(event):
    process = event.get_process()
    thread = event.get_thread()

    address = thread.read_stack_dwords(1)[0]

    process.suspend()

    emulation = thread.is_wow64()
    bits = thread.get_bits()

    if bits == 32 or emulation is True:

        lpFileName, dwDesiredAccess = thread.read_stack_dwords(3)[1:]

#        logstring = "Return Address %s" % HexDump.address(return_address, bits)
#        print logstring

        #process.write_dword(top_of_stack+((bits/8)*1), 0)
    else:
        context = thread.get_context()
        lpFileName = context['Rcx']
        dwDesiredAccess = context['Rdx']

    filename = process.peek_string(lpFileName, fUnicode=True)
    print "filename:" +filename
    str = "1.txt"
    print filename.find(str)
    replacename = "c:\\tmp\\2.txt"
    if filename.find(str) > 0 :
        filelen = len(replacename)

        fileaddr = event.get_process().malloc(filelen)
        process.write(fileaddr, replacename)
        top_of_stack = thread.get_sp()


        print "address read_word:", process.read_dword(lpFileName)
        print process.peek_string(lpFileName, fUnicode=True)
        print "read_word:", process.read_dword(fileaddr)
        print process.peek_string(fileaddr)
        bits = thread.get_bits()
        emulation = thread.is_wow64()
        print "fileaddr: %s" % hex(fileaddr)
        r = process.write_dword(top_of_stack+4, fileaddr)
        print "read_word:", process.read_dword(fileaddr)
        print "return : ", r
    else :
        print "not found"
#    if bits ==32 or emulation is True:



#    filename = process.peek_string(lpFileName, fUnicode=True)
#    addr = module.get_base()
#    print "addr :" % hex(addr)
    #addr = module.lpBaseOfDll + func
#    process.write(addr, len(filename))

    process.resume()


    """

    access = ''
    if dwDesiredAccess & 0x80000000: access += 'R'
    if dwDesiredAccess & 0x40000000: access += 'W'


    if access is not '' and '\\\\' not in filename[:2]: # Exclude PIPE and WMIDataDevice
        if 'W' in access:
            print('Opened file handle (access: %s):%s' % (access, filename))
        elif not writes_only:
            print('Opened file handle (access: %s):%s' % (access, filename))

        if results['filehandle'].has_key(filename):
            results['filehandle'][filename].append(access)
        else:
            results['filehandle'][filename] = []
            results['filehandle'][filename].append(access)

        if 'W' in access:
            stats['filew'] += 1
        else:
            stats['filer'] += 1
    """

def dump_thread_range(thread):

    thread.suspend()

    # Get the thread's currently running code.
    try:
        eip  = thread.get_pc()
        code = thread.disassemble_around( eip )

        # You can also do this:
        # code = thread.disassemble_around_pc()

        # Or even this:
        # process = thread.get_process()
        # code    = process.disassemble_around( eip )

    # Resume the thread execution.
    finally:
        thread.resume()

    return (code, eip)

def pre_InternetConnectW(event):

    process = event.get_process()
    process.suspend()
    thread = event.get_thread()

    if process.get_bits() == 32:
        hInternet, lpszServerName,nServerPort, lpszUsername, lpszPassword,dwService, dwFlags, dwContext = thread.read_stack_dwords(9)[1:]
    else:
        context = thread.get_context()
        hProc = context['Rcx']
        lpBase = context['Rdx']
        lpBuffer = context['R8']
        nSize = context['R9']

    server_name = process.peek_string(lpszServerName, fUnicode=True)
    print "server_name:", server_name

    if server_name == "naver.com" or server_name == "www.naver.com":

        new_server_name = "google.com".encode("utf-16le")
        print new_server_name
        payload_length = len(new_server_name)

        new_payload_addr = event.get_process().malloc(payload_length)

        process.write(new_payload_addr, new_server_name)
        top_of_stack = thread.get_sp()

        bits = thread.get_bits()
        emulation = thread.is_wow64()

        if bits ==32 or emulation is True:
            process.write_dword(top_of_stack+8, new_payload_addr)
        elif bits == 64:
            thread.set_register("Rdx", new_payload_addr)

    process.resume()

# Tell the user a module was loaded.
def print_module_load(self, event):
    mod  = event.get_module()
    base = mod.get_base()
    name = mod.get_filename()
    if not name:
        name = ''
    msg = "Loaded module (%s) %s"
    msg = msg % (HexDump.address(base), name)
    print msg

def pre_Sleep(event):
    thread = event.get_thread()
    process = event.get_process()

    print "Intercepted Sleep call of %d milliseconds"
    print_module_load(event)
    code, eip = dump_thread_range(thread)

    print CrashDump.dump_code( code, eip )

    n = 10000

#kernel32!start+0xd52c6

    # Access first parameter on the stack: EBP + 4
    stack_offset = thread.get_sp() + 4
    # Write the new value at that address (e.g. 0 milliseconds)
    process.write_dword(stack_offset, n)

global f, file
file="c:\\python\\hook\\1.cfg"
print file
f = open(file)

#h = Hack(processName="notepad.exe")
h = Hack(pid=sys.argv[1])
#h.add_hook('kernel32', "CreateFileW", pre_createfilew)
#h.add_hook('kernel32', 'WriteProcessMemory', pre_writeprocessmemory)
#h.add_hook('kernel32', 'CreateRemoteThread', pre_CreateRemoteThread)
#h.add_hook('kernel32', 'CreateProcessInternalW', pre_createprocess);
h.add_hook('kernel32', 'Sleep', pre_Sleep);
#h.add_hook('wininet', 'InternetConnectW', pre_InternetConnectW);
#h.add_hook("wininet", "HttpOpenRequest", pre_HttpOpenRequest)

h.hook()
f.close()
h.safe_exit()