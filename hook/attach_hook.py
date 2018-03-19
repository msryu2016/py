import winappdbg
from winappdbg import Thread, HexDump, CrashDump, System, Process
import inspect
import os, sys, time, signal
import pprint
import warnings
import pefile

__websites__ = [
    "https://www.github.com/SirFroweey/",
    "https://pypi.python.org/pypi/hackManager",
    "https://www.github.com/SirFroweey/hackManager"
]
__info__ = "Memory hacking software"
__author__ = "SirFroweey (a.k.a Froweey)"
__version__ = "2.5.0"
__date__ = "06/16/2017"

# This project was created using winappdbg.
# Check out http://winappdbg.sourceforge.net/doc/v1.4/tutorial/ for more details.

def print_thread_disassembly( tid ):

    # Request debug privileges.
    System.request_debug_privileges()

    # Instance a Thread object.
    thread = Thread( tid )

    # Suspend the thread execution.
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

    # Display the disassembled code.
    print
    print CrashDump.dump_code( code, eip ),


def print_modules( pid ):

    # Instance a Process object.
    process = Process( pid )
    print "Process %d" % process.get_pid()

    # ...and the modules in the process.
    print "Modules:"
    bits = process.get_bits()
    for module in process.iter_modules():
        print "\t%s\t%s" % (
            HexDump.address( module.get_base(), bits ),
            module.get_filename()
        )


def print_thread(title, thread):

    tid = thread.get_tid()
    eip     = thread.get_pc()
    context = thread.get_context()
    handle = thread.get_handle()
    code    = thread.disassemble_around( eip )

    print("%s %s - %s " % (title, HexDump.integer( tid ), handle))
    print CrashDump.dump_registers( context )
    print CrashDump.dump_code( code, eip ),


def print_event(event):
    code = HexDump.integer( event.get_event_code() )
    name = event.get_event_name()
    desc = event.get_event_description()
    if code in desc:
        print
        print "%s: %s" % (name, desc)
    else:
        print
        print "%s (%s): %s" % (name, code, desc)

def getSize_FromPE(PE_data):
# Performs basic lookup to find the end of an EXE, based upon the
# size of PE sections. Same algorithm is used to find EXE overlay
# FYI: This will miss any overlay data, such as RAR SFX archives, etc
    try:
        pe = pefile.PE(data=PE_data)
        return pe.sections[-1].PointerToRawData + pe.sections[-1].SizeOfRawData
    except:
        return 0

class BasicEventHandler(winappdbg.EventHandler):
    """EventHandler for our winappdbg debugger."""
    def __init__(self, hook_dict):
        winappdbg.EventHandler.__init__(self)
        self.hooks = hook_dict
    def load_dll(self, event):
        pid = event.get_pid()
        module = event.get_module()
        for dict_module_name in list(self.hooks.keys()):
            if isinstance(dict_module_name, int):
                # Internal function hooks.
                dict_module_function, signatures = self.hooks.get(dict_module_name)[0]
                event.debug.hook_function(pid, dict_module_name, dict_module_function, signature = signatures)
            else:
                # External DLL function hooks.
                values = self.hooks.get(dict_module_name)
                for entry in values:
                    dict_module_function_name, dict_module_function = entry
                    if module.match_name(dict_module_name):
                        event.debug.hook_function(
                            pid,
                            module.resolve(dict_module_function_name),
                            dict_module_function,
                            paramCount = len(inspect.getargspec(dict_module_function)[0])-2
                        )

dll_dict = {}

class EventHandler(winappdbg.EventHandler):
    """
    Event handler class.
    event: https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/event.py
    """


    def __init__(self, hook_dict):
        winappdbg.EventHandler.__init__(self)
        self.hooks = hook_dict
        self.pp = pprint.PrettyPrinter(indent=4)


    def create_process(self, event):
        process = event.get_process()
        pid = event.get_pid()
        filename = process.get_filename()
        print("create_process %d - %s" % (pid, filename))


        bits = process.get_bits()
        for module in process.iter_modules():
            dll_dict[HexDump.address( module.get_base(), bits )] = module.get_filename()


            print "\t%s\t%s" % (
                HexDump.address( module.get_base(), bits ),
                module.get_filename()
            )

            PE_header = process.read(module.get_base(), 0x64)

            dosheader = PE_header[:64]
            print ":", dosheader, ":"
            print ''.join( [ "%02X " % ord( x ) for x in dosheader ] ).strip()

            pe = pefile.PE(data = PE_header)

            size = pe.sections[-1].PointerToRawData + pe.sections[-1].SizeOfRawData
            print "size:", size

            if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
                for entry in pe.DIRECTORY_ENTRY_IMPORT:
                    for imp in entry.imports:
                        print '\t', hex(imp.address), imp.name
                    print entry.dll


    def exit_process(self, event):
        process = event.get_process()
        pid = event.get_pid()
        filename = process.get_filename()
        print("exit_process %d - %s" % (pid, filename))

    def create_thread(self, event):
        process = event.get_process()
        thread = event.get_thread()
        context = thread.get_context()
        eip     = thread.get_pc()
        tid = event.get_tid()

        filename = process.get_filename()
        print "process:%s" % filename
#        pid = event.get_pid()

        start = event.get_start_address()
        if start:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                start = event.get_process().get_label_at_address(start)
            print "Started thread %d at %s" % (tid, start)
        else:
            print "Attached to thread %d" % tid


        print CrashDump.dump_registers( context )

        #print_thread('asm', thread)

        """
        top_of_stack = thread.get_sp()
        print "stack"
        print CrashDump.dump_registers( top_of_stack )
        """
        #print print_event(event)
        #print "eip:", hex(eip)
        #print_module_load( event )
        #thread.kill()
        #print "thread kill"
        #print_thread("create_thread", thread)
        #event.debug.start_tracing( event.get_tid() )

        #print "context:", context

    def exit_thread(self, event):
        thread = event.get_thread()
        eip     = thread.get_pc()
        tid = event.get_tid()
        pid = event.get_pid()
        print("exit_thread %d > %d" % (pid, tid))
        print "eip:", hex(eip)

        #print_thread("exit_thread", thread)
        #event.debug.start_tracing( event.get_tid() )

    # Single step events go here.
    def single_step( self, event ):

        # Show the user where we're running.
        thread = event.get_thread()
        pc     = thread.get_pc()
        code   = thread.disassemble( pc, 0x10 ) [0]
        bits   = event.get_process().get_bits()
        print "%s: %s" % ( HexDump.address(code[0], bits), code[2].lower() )

    def load_dll(self, event):
        module = event.get_module()
        proc = event.get_process()
        pid = event.get_pid()
        thread = event.get_thread()
#        print "baseofdll:", module.lpBaseOfDll
#        print "baseofdll+func:", module.lpBaseOfDll + func
        def bp(name, func, callback):

            if module.match_name(name):
                if isinstance(func, long):
                    addr = module.lpBaseOfDll + func
                else:
                    addr = module.resolve(func)


                try:
                    if addr:
                        event.debug.break_at(pid, addr, callback)
                    else:
                        print("Couldn't resolve or address not belong to module:%s!%s" % (name,func))
                except Exception, e:
                    print e
                    print("Could not break at : %s!%s." % (name, func))

        for name in list(self.hooks.keys()):
            func, sig = self.hooks.get(name)[0]
            #print pid, ':', name, ':', func, ':', sig
            bp(name, func, sig)

class Hack(object):
    """Base class utilized to make hack development for any type of game/software easy."""

    def __init__(self, processName=None, pid=None, run=None):
        """
        process_name = 'Notepad'
        i = Hack(process_name).
        # If no process is supplied, then you do:
        i = Hack().find_process()
        print i.running
        # to get a list the currently running processes.

        :processName: (string) exact process name.
        """

        self.module_base_dict = {}
        self.name = processName
        self.threads = {}
        self.hwnd = None
        self.hook_dict = {}
        self.base_address = None
        self.last_address = None
        self.running = []
        if processName is not None:
            self.find_process(processName)
        if pid is not None :
            self.find_pid(pid)
        if run is not None:
            pass

        self.get_base_address()

    def __repr__(self):
        return "<Hack instance: %s>" %str(self.name)

    def set_last_address(self):
        self.last_address = self.module_base_dict.get(
            self.module_base_dict.keys()[::-1][0]
        )

    def add_hook(self, module_name, function_name, function_handle):
        """
        Add hook to an external DLL function.
        :param module_name: (string) module name (i.e: 'ws2_32.dll')
        :param function_name: (string) function name (i.e: 'send')
        :param function_handle: (string) function event callback (i.e.: 'mycallback')
        """
        key = self.hook_dict.get(module_name)
        if key is not None:
            key.append((function_name, function_handle))
        else:
            self.hook_dict[module_name] = [(function_name, function_handle)]

    def add_internal_hook(self, address, function_handle, signature=()):
        """
        Add hook to an internal function.
        :param address: (int/hex) Memory address of internal functin.
        :param function_handle: callback function.
        :param signature: byte-code signature used to find function.
        """
        self.hook_dict[address] = [(function_handle, signature)]

    def hook(self):
        if self.hwnd is None:
            raise ValueError, "You need to specify the process name, i.e.: Hack('process_name.exe').hook()"

        if len(self.hook_dict.keys()) == 0:
            raise ValueError, "You need to call Hack().add_hook() first! You currently haven't added any hooks!"
        #debug = winappdbg.Debug( BasicEventHandler(self.hook_dict) )
        self.debug = winappdbg.Debug( EventHandler(self.hook_dict) )
        try:
            self.debug.attach(self.hwnd.get_pid())
            #self.debug.interactive()
            self.debug.loop()
        finally:
            self.debug.stop()

    def wait(self, add_time):
        self.debug = winappdbg.Debug( )
        try:
            self.debug.attach(self.hwnd.get_pid())
            #System.set_kill_on_exit_mode(True)

            maxTime = time.time() + add_time

            while self.debug and time.time() < maxTime:
                try:
                    self.debug.wait(1000)
                    print time.time()
                except WindowsError, e:
                    continue
                    raise


                try:
                    self.debug.dispatch()
                finally:
                    self.debug.cont()
        except Exception, e:
            print e
            pass

    def get_threads(self):
        """
        Get running thread list.
        You can call .suspend(), .resume(), .kill(), .name(), \
        .set_name(), .is_hidden(), .set_process(), etc.
        Check out http://winappdbg.sourceforge.net/doc/v1.4/reference/winappdbg.system.Thread-class.html for more info.
        """
        process = self.hwnd
        for thread in process.iter_threads():
            self.threads[str(thread.get_tid())] = thread

    @classmethod
    def change_window_title(cls, title, new_title):
        """
        Change the specified window's title to the new_title. \
        (title, new_title).

        This is a class-method.

        i.e.: Hack.change_window_title('Cheat Engine 6.1', 'Undetected CE')
        """
        try:
            _window = winappdbg.System.find_window(windowName=title)
        except:
            _window = None

        if _window:
            _window.set_text(new_title)
            return _window

        return False

    def find_pid(self, pid=None):

        process = Process(int(pid))
        self.hwnd = process

    def find_process(self, processName=None):
        """
        If a processName is not passed, then it will return the list of running processes.
        Do NOT call this method(function) directly. It is called by the __init__ class method.
        If you want to list all running process do the following:
        ins = Hack()
        print ins.running

        :processName: (string) Window title or process name.
        """
        system = winappdbg.System()
        for process in system:
            if process.get_filename() is not None:
                name = process.get_filename().split("\\")[-1]
                if processName is None:
                    self.running.append((name, process.get_pid()))
                else:
                    if name == processName:
                        self.hwnd = process
                        break;

    def get_base_address(self):
        """
        Get our processes base_address & its DLL's base_addresses too. \
        Then store it in the module_base_dict global variable.
        """
        process = self.hwnd
        if process is None:
            raise ValueError, "Could not find process."
        bits = process.get_bits()
        for module in process.iter_modules():
            if module.get_filename().split("\\")[-1] == self.name:
                self.base_address = module.get_base()
                #self.base_address = winappdbg.HexDump.address( module.get_base(), bits )
            else:
                module_name = os.path.basename(module.get_filename())
                self.module_base_dict[module_name] = module.get_base()
        try:
            self.set_last_address()
        except IndexError, e:
            pass

    def read(self, address, length):
        """
        Read process memory. (memory_adress, data_length). \
        i.e.: (0x40000000, 4)
        """
        process = self.hwnd
        data = process.read( address, length )
        label = process.get_label_at_address( address )
        return (data, label)

    def read_char(self, address):
        return (self.hwnd.read_char(address),
                self.hwnd.get_label_at_address(address))

    def read_int(self, address):
        return (self.hwnd.read_int(address),
                self.hwnd.get_label_at_address(address))

    def read_uint(self, address):
        return (self.hwnd.read_uint(address),
                self.hwnd.get_label_at_address(address))

    def read_float(self, address):
        return (self.hwnd.read_float(address),
                self.hwnd.get_label_at_address(address))

    def read_double(self, address):
        return (self.hwnd.read_double(address),
                self.hwnd.get_label_at_address(address))

    def read_pointer(self, address):
        return (self.hwnd.read_pointer(address),
                self.hwnd.get_label_at_address(address))

    def read_dword(self, address):
        return (self.hwnd.read_dword(address),
                self.hwnd.get_label_at_address(address))

    def read_qword(self, address):
        return (self.hwnd.read_qword(address),
                self.hwnd.get_label_at_address(address))

    def read_structure(self, address):
        return (self.hwnd.read_structure(address),
                self.hwnd.get_label_at_address(address))

    def read_string(self, address, charLength):
        return (self.hwnd.read_string(address, charLength),
                self.hwnd.get_label_at_address(address))

    def write(self, address, data):
        "Write to process memory. (memory_address, data2write)"""
        process = self.hwnd
        written = process.write( address, data )
        return written

    def write_char(self, address, data):
        "Write to process memory. (memory_address, data2write)"""
        process = self.hwnd
        written = process.write_char( address, data )
        return written

    def write_int(self, address, data):
        "Write to process memory. (memory_address, data2write)"""
        process = self.hwnd
        written = process.write_int( address, data )
        return written

    def write_uint(self, address, data):
        "Write to process memory. (memory_address, data2write)"""
        process = self.hwnd
        written = process.write_uint( address, data )
        return written

    def write_float(self, address, data):
        "Write to process memory. (memory_address, data2write)"""
        process = self.hwnd
        written = process.write_float( address, data )
        return written

    def write_double(self, address, data):
        "Write to process memory. (memory_address, data2write)"""
        process = self.hwnd
        written = process.write_double( address, data )
        return written

    def write_pointer(self, address, data):
        "Write to process memory. (memory_address, data2write)"""
        process = self.hwnd
        written = process.write_pointer( address, data )
        return written

    def write_dword(self, address, data):
        "Write to process memory. (memory_address, data2write)"""
        process = self.hwnd
        written = process.write_dword( address, data )
        return written

    def write_qword(self, address, data):
        "Write to process memory. (memory_address, data2write)"""
        process = self.hwnd
        written = process.write_qword( address, data )
        return written

    def search(self, _bytes, minAddr, maxAddr):
        """
        Search minAddr through maxAddr for _bytes. (_bytes, minAddr, maxAddr).
        Returns a generator iterable containing memory addresses.
        """
        return self.hwnd.search_bytes(_bytes, minAddr, maxAddr)

    def address_from_label(self, name):
        """Returns the memory address(es) that match the label name. (name)"""
        return self.hwnd.resolve_label(name)

    def load_dll(self, filename):
        """Inject filename.dll into our process. (filename)"""
        process = self.hwnd
        process.inject_dll( filename )
        return True

    def safe_exit(self):
        self.hwnd.close_handle()
        return True


pid = sys.argv[1] if len(sys.argv) > 1 else None

if pid is None:
    print
    print "usage : %s pid [act]" % sys.argv[0]

def post_CreateFileW(event, a):


    tid = event.get_tid()
    params = event.hook.get_params(tid)

    print "in post_CreateFileW"
    print params

    print
    print
    print "=" * 30


h = Hack(pid=pid)
print "pid :", pid
h.add_hook("kernel32", "CreateFileW", post_CreateFileW)
h.add_hook("kernel32", "CreateFileA", post_CreateFileW)
#h.add_hook("kernel32", "Sleep", pre_Sleep)
#h.add_hook("Wininet", "HttpOpenRequestA", pre_HttpOpenRequestW)
#h.add_hook("Wininet", "InternetConnectW", pre_InternetConnectW)


h.hook()
h.safe_exit()