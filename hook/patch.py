from winappdbg import Process, System, Thread, win32
import os, sys, time
from winappdbg.process import _ProcessContainer
from winappdbg.module import Module, _ModuleContainer
from winappdbg.breakpoint import CodeBreakpoint
from winappdbg.util import PathOperations
from winappdbg.event import EventHandler, NoEvent
from winappdbg.textio import HexInput, HexOutput, HexDump, CrashDump, DebugLog
import winappdbg
from winappdbg import Thread, HexDump, CrashDump, System, Process
import struct
from ctypes import *

#/merge:.rdata=.text.


PAGE_NOACCESS          = 0x01
PAGE_READONLY          = 0x02
PAGE_READWRITE         = 0x04
PAGE_WRITECOPY         = 0x08
PAGE_EXECUTE           = 0x10
PAGE_EXECUTE_READ      = 0x20
PAGE_EXECUTE_READWRITE = 0x40
PAGE_EXECUTE_WRITECOPY = 0x80
PAGE_GUARD            = 0x100
PAGE_NOCACHE          = 0x200
PAGE_WRITECOMBINE     = 0x400
MEM_COMMIT           = 0x1000
MEM_RESERVE          = 0x2000
MEM_DECOMMIT         = 0x4000
MEM_RELEASE          = 0x8000
MEM_FREE            = 0x10000
MEM_PRIVATE         = 0x20000
MEM_MAPPED          = 0x40000
MEM_RESET           = 0x80000
MEM_TOP_DOWN       = 0x100000
MEM_WRITE_WATCH    = 0x200000
MEM_PHYSICAL       = 0x400000
MEM_LARGE_PAGES  = 0x20000000
MEM_4MB_PAGES    = 0x80000000
SEC_FILE           = 0x800000
SEC_IMAGE         = 0x1000000
SEC_RESERVE       = 0x4000000
SEC_COMMIT        = 0x8000000
SEC_NOCACHE      = 0x10000000
SEC_LARGE_PAGES  = 0x80000000
MEM_IMAGE         = SEC_IMAGE
WRITE_WATCH_FLAG_RESET = 0x01
FILE_MAP_ALL_ACCESS = 0xF001F

def br(msg):
    import pprint

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(msg)

    return False

def _split_dll_func(str):

    if str.find("!") == -1:
        return ("", "")
    else:
        return str.split("!", 1)

def ismatch(str, reg):
    import re
    try:
        p = re.compile(reg)
        it = p.match(str)
    except:
        return False
    return it



def strhex(s):
    l=[]
    for i in range(0, len(s), 2):
        l.append( '\\x%s' % s[i:i+2] )

    return ''.join(l)

def show_disassemble(pid, addr, size, Flag=True):

    x = int(addr, 16)

    process = Process( pid )

    if Flag == True:
        code = process.disassemble(x, size*8)
    else:
        data   = process.read(x, size*8)
        code = process.disassemble_string(x, data)


    s = ''
    for line in code:
        print CrashDump.dump_code_line(line, bShowDump = True, dwDumpWidth=16)
        s += CrashDump.dump_shell_line(line)

    return s


def read_string(pid, addr):

    x = int( addr, 16)
    process = Process( pid )

#    print "get_main_module:", process.get_main_module()
#    print "get_peb:", hex(process.get_peb().ImageBaseAddress)
    print "read: ", x

    print
    print "string :"
    read = process.peek_string(x)

    print read
    print HexDump.hexadecimal(read, '\\x')

def write_string(pid, addr, value):

    x = int( addr, 16)
    process = Process( pid )
    process.write(x, value+'\x0a')

def write_double(pid, addr, value):

    x = int( addr, 16)
    process = Process( pid )
    process.write_double(x, value)


def alloc_string(pid, addr, value):

    x = int( addr, 16)
    process = Process( pid )

    lpNewAddr = process.malloc(len(value)+1)

    newval = value + '\x0a'
    print HexDump.hexadecimal(newval, '\\x')

    try:
        process.write(lpNewAddr, newval)
    except Exception, e:
        process.free(lpNewAddr)
        raise

    print "lpNewAddr:", hex(lpNewAddr)

    read = process.peek_string(lpNewAddr)
    print read
    print HexDump.hexadecimal(read, '\\x')

    return lpNewAddr

def push_addr(pid, addr, value):

    x = int( addr, 16)
    process = Process( pid )

    code = '\x68' + struct.pack('<L', int(value, 16))
    print "code:", code
    print "addr:", x

    try:
        process.write(x, code)
    except Exception, e:
        raise

    print "string :"
    read = process.peek_string(x)



def hex_string(pid, addr, size, flag=1):

    x = int(addr, 16)

    process = Process( pid )

    data   = process.read(x, size*8)
    #hexdump = HexDump.printable( data )

    if flag == 3:
        print HexDump.hexblock_dword( data, address = True, width = 16 )
    elif flag == 2:
        print HexDump.hexblock_word( data, address = True, width = 16 )
    else:
        print HexDump.hexblock( data, address = True, width = 16 )


def proces_info(pid, addr=""):

    x = int( addr, 16)
    process = Process( pid )

    print "get_arch:", process.get_arch()
    print "get_bits:", process.get_bits()
#    print "get_main_module:", process.get_main_module()


    print "get_command_line:", process.get_command_line()
    print "get_image_name:", (process.get_image_name())
    print "get_image_base:", hex(process.get_image_base())
    print "get_peb:", hex(process.get_peb().ImageBaseAddress)
    print "get_peb_address:", hex(process.get_peb_address())
    print "get_entry_point:", hex(process.get_entry_point())

def search_string(pid, func, size):

    process = Process(pid)

    print "get_image_base:", hex(process.get_image_base())
    print "get_main_module:", process.get_main_module()

    dosheader = process.read(process.get_image_base(), 100)
    print ''.join( [ "%02X " % ord( x ) for x in dosheader ] ).strip()



    sys.exit(0)
    search_dll, search_func = _split_dll_func(func)
    print search_dll, ":", search_func
    if search_dll is None or search_func is None :
        print "%s not found!" % arg
        sys.exit(-1)

    dict = {}
    for file, file_addr in process.get_modules():
        if ismatch(file, ".*"+search_dll+"$") or ismatch(file, ".*"+search_dll+".dll$"):
            print file," : ", hex(file_addr) , " (", file_addr,")"


    return ""

def do_bp(process, address):

    x = int( address, 16)
    hProcess = process.get_handle()
    # store the original byte
    old_protect = c_ulong(0)
    #h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    windll.kernel32.VirtualProtectEx(hProcess, x, 1, PAGE_EXECUTE_READWRITE, byref(old_protect))

    try:
        process.write(x, '\xcc')
    except Exception,e:
        print e


def set_bp(pid, func,size):

    process = Process(pid)

    search_dll, search_func = _split_dll_func(func)
    print search_dll, ":", search_func
    if search_dll is None or search_func is None :
        print "%s not found!" % arg
        sys.exit(-1)

    dict = {}
    for file, file_addr in process.get_modules():

        if ismatch(file, ".*"+search_dll+"$") or ismatch(file, ".*"+search_dll+".dll$"):

            module = Module(file_addr, process=process, fileName=file)
            module.get_symbols()
            print file, "!", file_addr, " > ", search_dll, " > ", search_func
            for func, addr, _ in module.iter_symbols():

                if ismatch(func, search_func+".*"):
                    dict[hex(addr)] = func
                    print "%s : [%s] %s" % (hex(addr), addr, func)

    print "len", len(dict)
    if len(dict)==1:
        break_addr, break_func = dict.items()[0]
        print " : ", break_addr, "", break_func
        do_bp(process, break_addr)
    else:
        i = 0
        for key in dict.keys():
            print "%d : %s!%s" % (i, key, dict[key])
            i+=1

        number = int(raw_input("What is your Number? "))
        print
        break_addr, break_func = dict.items()[number]
        print break_func, ":", break_addr


        if do_bp(process, break_addr[:-1]) == True:
            print_breakpoints()

def set_bbp(pid, func,size):

    process = Process(pid)

    if do_bp(process, func) == True:
        print_breakpoints()




def print_breakpoints():

    print
    print "break pointer :"
    for key in breakpoints.keys():
        print key, ":", breakpoints[key]

"""
    print
    for env in process.get_environment():
        print env, "=", process.get_environment()[env]

    print
    print "get_environment_block:", process.get_environment_block()
    for envb in process.get_environment_variables():
        print envb[0], "=", envb[1]
"""

"""
patch.py l 3552 01101000
patch.py rs 3552 0x1102100
patch.py wa 3552 0x1102100 "abcdefg: %d > %d"
patch.py ps 3552 0x01101015 0x200000
patch.py rs 3552 0x200000

patch.py ws 3552 0x200000 "A: %d > %d"
"""

def usage(sys):
    script = sys.argv[0]
    print
    print "%s l [assembly list]  <pid> addr size"  % os.path.basename(script)

    print "  \ts   [search           <pid> dll func"
    print "  \tb   [break            <pid> dll func"
    print "  \tbb   [break with addr <pid> addr func"
    print "  \ti   [info]            <pid> addr size"
    print "  \th  [hex]              <pid> addr size"
    print "  \ths [hex string]       <pid> addr size"
    print "  \thw [hex word]         <pid> addr size"
    print "  \thd [hex doubleword]   <pid> addr size"

    print "  \trs [read string]      <pid> addr "
    print "  \tws [write string]     <pid> addr string"
    print "  \twa [write alloc]      <pid> addr string"
    print "  \tps [push value]       <pid> addr value"

    print
    sys.exit(-1)


def main():

    import sys

    if len(sys.argv) < 3:
        usage(sys)

    command = sys.argv[1].lower()
    pid = int(sys.argv[2])
    func = sys.argv[2] if len(sys.argv) > 2 else ""
    addr = sys.argv[3] if len(sys.argv) > 3 else hex(Process(pid).get_entry_point())
    print "addr:", addr, ""
    size = sys.argv[4] if len(sys.argv) > 4 else 10

    if command == 'l' or command=='ll':
        Flag = False
        if command == 'll' :
            Flag = True

        str = show_disassemble(pid, addr, int(size), Flag)
        print
        hex_string(pid, addr, int(size))
        print
        print strhex(str)

        process = Process(pid)
        for tid in process.iter_thread_ids():
            print tid

    elif command == 'i':
        proces_info(pid, addr)
    elif command == 'rs':
        read_string(pid, addr)
    elif command == 'ws':
        write_string(pid, addr, size)
        print read_string(pid, addr)
    elif command == 'wa':
        alloc_string(pid, addr, size)
    elif command == 'ps':
        push_addr(pid, addr, size)
    elif command == 'h':
        hex_string(pid, addr, int(size), 1)
        print
        hex_string(pid, addr, int(size), 2)
        print
        hex_string(pid, addr, int(size), 3)
    elif command == 'hs':
        hex_string(pid, addr, int(size), 1)
    elif command == 'hw':
        hex_string(pid, addr, int(size), 2)
    elif command == 'hd':
        hex_string(pid, addr, int(size), 3)
    elif command == 's':
        address = search_string(pid, addr, int(size))
        #print "bp :", hex(address), " : ", address
        #show_disassemble(pid, address, 10)
        #hex_string(pid, address, 10, 1)
    elif command == 'b':
        set_bp(pid, addr, int(size))
    elif command == 'bb':
        debug = winappdbg.Debug( )
        debug.attach(pid)
        debug.break_at(pid, addr)


       #
        #show_disassemble(pid, addr, 10, 1)

if __name__ == '__main__':
    main()