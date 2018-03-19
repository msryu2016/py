### -*- coding: utf-8 -*-
import sys
from winappdbg import Process, HexDump
from winappdbg import Thread, System, win32


def print_threads_and_modules( pid ):

    process = Process(pid)

    print "process %d" % process.get_pid()
    print process.get_command_line()


    print "Threads"
    for thread in process.iter_threads():
        print "\t%d" % thread.get_tid()

    print "Modules"
    bits = process.get_bits()
    for module in process.iter_modules():
        print "\t%s\t%s" % (
            HexDump.address( module.get_base(), bits), module.get_filename()
        )

def process_kill( pid ):
    process = Process( pid )
    print process.get_command_line()
    process.kill()

def process_read(pid, address, length):

    process = Process( pid )
    data = process.read(address, length)

    return data

def show_environment( pid ):
    process = Process( pid )
    environment = process.get_envitonment()

    for variable, value in sorted( environment.iterms()):
        print "%s=%s" % (variable, value)

def print_memory_map( pid ):

    process= Process( pid )
    bits = process.get_bits()

    memoryMap = process.get_memory_map()

    print "Addresss\t Size\t State\t Access\t Type"
    for mbi in memoryMap:
        BaseAddress= HexDump.address(mbi.BaseAddress, bits)
        RegionSize = HexDump.address(mbi.RegionSize, bits)
        # State (free or allocated).
        if mbi.State == win32.MEM_RESERVE:
            State = "Reserved "
        elif mbi.State == win32.MEM_COMMIT:
            State = "Commited "
        elif mbi.State == win32.MEM_FREE:
            State = "Free "
        else:
            State = "Unknown "
        # Page protection bits (R/W/X/G).
        if mbi.State != win32.MEM_COMMIT:
            Protect = " "
        else:
            ## Protect = "0x%.08x" % mbi.Protect
            if mbi.Protect & win32.PAGE_NOACCESS:
                Protect = "--- "
            elif mbi.Protect & win32.PAGE_READONLY:
                Protect = "R-- "
            elif mbi.Protect & win32.PAGE_READWRITE:
                Protect = "RW- "
            elif mbi.Protect & win32.PAGE_WRITECOPY:
                Protect = "RC- "
            elif mbi.Protect & win32.PAGE_EXECUTE:
                Protect = "--X "
            elif mbi.Protect & win32.PAGE_EXECUTE_READ:
                Protect = "R-X "
            elif mbi.Protect & win32.PAGE_EXECUTE_READWRITE:
                Protect = "RWX "
            elif mbi.Protect & win32.PAGE_EXECUTE_WRITECOPY:
                Protect = "RCX "
            else:
                Protect = "??? "
            if mbi.Protect & win32.PAGE_GUARD:
                Protect += "G"
            else:
                Protect += "-"
            if mbi.Protect & win32.PAGE_NOCACHE:
                Protect += "N"
            else:
                Protect += "-"
            if mbi.Protect & win32.PAGE_WRITECOMBINE:
                Protect += "W"
            else:
                Protect += "-"
                Protect += " "
        # Type (file mapping, executable image, or private memory).
        if mbi.Type == win32.MEM_IMAGE:
            Type = "Image "
        elif mbi.Type == win32.MEM_MAPPED:
            Type = "Mapped "
        elif mbi.Type == win32.MEM_PRIVATE:
            Type = "Private "
        elif mbi.Type == 0:
            Type = "Free "
        else:
            Type = "Unknown "

        fmt = "%s\t%s\t%s\t%s\t%s"
        print fmt % ( BaseAddress, RegionSize, State, Protect, Type )

def memory_search(pid, bytes):

    process = Process( pid )

    for address in process.search_bytes( bytes ):
        print HexDump.address( address )

def strings( pid ):

    process = Process ( pid )

    for address, size, data in process.strings():
        print "%s:%s" % ( HexDump.address(address), data)

def freeze_threads( pid ):

    System.request_debug_privileges()

    process= Process( pid )

    process.scan_threads()

    for thread in process.iter_threads():
        thread.suspend()

def unfreeze_threads( pid ):

    System.request_dubug_privileges()

    process = Process( pid )

    process.scan_thread()

    for thread in process.iter_threads():
        thread.resume()

def print_thread_context( tid ):

    System.request_debug_privileges()

    thread = Thread( tid )

    thread.suspend()

    try:
        context = thread.get_context()

    finally:
        thread.resume()

    print
    print CrashDump.dump_registers(context),

def print_thread_disassembly( tid ):
    # Request debug privileges.
    System.request_debug_privileges()
    # Instance a Thread object.
    thread = Thread( tid )
    # Suspend the thread execution.
    thread.suspend()
    # Get the thread’s currently running code.
    try:
        eip = thread.get_pc()
        code = thread.disassemble_around( eip )
        # You can also do this:
        # code = thread.disassemble_around_pc()
        # Or even this:
        # process = thread.get_process()
        # code = process.disassemble_around( eip )
        # Resume the thread execution.
    finally:
        thread.resume()
        # Display the disassembled code.
    print
    print CrashDump.dump_code( code, eip ),

def print_api_address( pid, modName, procName ):
    # Request debug privileges.
    System.request_debug_privileges()
    # Instance a Process object.
    process = Process( pid )
    # Lookup it’s modules.
    process.scan_modules()
    # Get the module.
    module = process.get_module_by_name( modName )
    if not module:
        print "Module not found: %s" % modName
        sys.exit(0)

    # Resolve the requested API function address.
    address = module.resolve( procName )
    # Print the address.
    if address:
        print "%s!%s == 0x%.08x" % ( modName, procName, address )
    else:
        print "Could not resolve %s in module %s" % (procName, modName)

def print_handle_caption():

    system = System()

    for window in system.get_windows():
        handle = HexDump.integer( window.get_handle() )
        caption = window.get_text()

        if not caption in None:
            print "%s\t%s" % (handle, caption)

print_memory_map(int(sys.argv[1]))