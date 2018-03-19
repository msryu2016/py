import sys
from ctypes import *
from my_debugger_defines import *
#from win32 import *
import win32

kernel32 = windll.kernel32


class debugger():

    def __init__(self):
        self.h_process = None
        self.pid =None
        self.debugger_active =False
        self.h_thread = None
        self.context = None
        self.breakpoints = {}

    def load(self, path_to_exe):
        #
        creation_flags = CREATE_NEW_CONSOLE

        startupinfo = STARTUPINFO()
        process_information = PROCESS_INFORMATION()

        startupinfo.dwFlags = 0x1
        startupinfo.wShowWindow = 0x0


        startupinfo.cb = sizeof(startupinfo)


        if kernel32.CreateProcessA(path_to_exe,
                                    None,
                                    None,
                                    None,
                                    None,
                                    creation_flags,
                                    None,
                                    None,
                                    byref(startupinfo),
                                    byref(process_information)):
            print "[*] We have successfully launched the process!"
            print "[*] PID : %d" % process_information.dwProcessId

        else:
            print "[*] Error : 0x%08x." % kernel32.GetLastError()

    def request_privileges(self, state, *privileges):

        try:
            with win32.OpenProcessToken(win32.GetCurrentProcess(),
                win32.TOKEN_ADJUST_PRIVILEGES) as hToken:
                NewState = ( (priv, state) for priv in privileges )
                win32.AdjustTokenPrivileges(hToken, NewState)
        except Exception, e:
            print e
            return False

        return True

    def open_process(self, pid):

        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        return h_process

    def mquery(self, lpaddress):

        h_process = self.open_process(self.pid)
        mbi = MEMORY_BASIC_INFORMATION()
        sysinfo = SYSTEM_INFO()
        kernel32.GetSystemInfo(byref(sysinfo))
        kernel32.VirtualQueryEx(h_process, lpaddress, byref(mbi), sizeof(mbi))
        return MemoryBasicInformation(mbi)


    def mprotect(self, lpaddress, size, prot):
        h_process = self.open_process(self.pid)
        flOldProtect = DWORD(0)
        kernel32.VirtualProtectEx(h_process, lpaddress, size, prot, flOldProtect)
        return flOldProtect

    def attach(self,pid):

        print "win32.SE_DEBUG_NAME:SeDebugPrivilege", win32.SE_DEBUG_NAME
        #self.request_privileges(True, win32.SE_DEBUG_NAME)
        self.h_process = self.open_process(pid)

        if kernel32.DebugActiveProcess(pid):
            self.debugger_active = True
            print "act:", self.debugger_active
            self.pid = int(pid)
        else:
            print kernel32.GetLastError()
            print "[*] Unable to attach to the process."
            sys.exit(-1)



    def run(self):

        while self.debugger_active == True:
            self.get_debug_event()

    def get_debug_event(self):

        debug_event    = DEBUG_EVENT()
        continue_status = DBG_CONTINUE

        if kernel32.WaitForDebugEvent(byref(debug_event),100):
            # grab various information with regards to the current exception.
            self.h_thread          = self.open_thread(debug_event.dwThreadId)
            self.context           = self.get_thread_context(h_thread=self.h_thread)
            self.debug_event       = debug_event


            print "Event Code: %d Thread ID: %d" % \
                (debug_event.dwDebugEventCode,debug_event.dwThreadId)

            if debug_event.dwDebugEventCode == EXCEPTION_DEBUG_EVENT:
                self.exception = debug_event.u.Exception.ExceptionRecord.ExceptionCode
                self.exception_address = debug_event.u.Exception.ExceptionRecord.ExceptionAddress

                # call the internal handler for the exception event that just occured.
                if self.exception == EXCEPTION_ACCESS_VIOLATION:
                    print "Access Violation Detected."
                elif self.exception == EXCEPTION_BREAKPOINT:
                    continue_status = self.exception_handler_breakpoint()
                elif self.exception == EXCEPTION_GUARD_PAGE:
                    print "Guard Page Access Detected."
                elif self.exception == EXCEPTION_SINGLE_STEP:
                    self.exception_handler_single_step()

            kernel32.ContinueDebugEvent(debug_event.dwProcessId, debug_event.dwThreadId, continue_status)


    def exception_handler_breakpoint(self):
        print "[*] inside the breakpoint handler."
        print "Exception Address : 0x%08x" % self.exception_address

        return DBG_CONTINUE


    def detach(self):

        if kernel32.DebugActiveProcessStop(self.pid):
            print "[*] Finished deubggin. Exiting..."
            return True
        else:
            print "Threr was an error"
            return False

    def open_thread(self, thread_id):

        h_thread = kernel32.OpenThread(THREAD_ALL_ACCESS, None, thread_id)

        if h_thread is not None:
            return h_thread

        else:
            print "[*] Could not obtain a valid thread handle."
            return False

    def enumerate_threads(self):
        thread_entry = THREADENTRY32()
        thread_list = []

        snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, self.pid)

        if snapshot is not None:
            thread_entry.dwSize = sizeof(thread_entry)
            success = kernel32.Thread32First(snapshot, byref(thread_entry))

            while success:
                if thread_entry.th32OwnerProcessID == self.pid:
                    thread_list.append(thread_entry.th32ThreadID)
                success = kernel32.Thread32Next(snapshot, byref(thread_entry))

            kernel32.CloseHandle(snapshot)
            return thread_list
        else:
            return False


    def get_thread_context(self, thread_id=None, h_thread=None):
        context = CONTEXT()
        context.ContextFlags = CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS


        if not h_thread:
            self.open_thread(thread_id)

        h_thread = self.open_thread(thread_id)

        if kernel32.GetThreadContext(h_thread, byref(context)):
            kernel32.CloseHandle(h_thread)
            return context
        else:
            return False


    def read_process_memory(self, address, length):

        data = ""
        read_buf = create_string_buffer(length)
        count = c_ulong(0)

        if not kernel32.ReadProcessMemory(self.h_process, address, read_buf, length, byref(count)):
            return False
        else:
            data += read_buf.raw
            return data

    def write_process_memory(self, address, data):



        count = c_ulong(0)
        length = len(data)

        c_data = c_char_p(data[count.value:])

        if not kernel32.WriteProcessMemory(self.h_process, address,c_data, length, byref(count)):
            return False
        else:
            return True

    def bp_set(self, address):
        print "[*] Setting breakpoint at: 0x%08x" % address
        if not self.breakpoints.has_key(address):

            # store the original byte
            old_protect = c_ulong(0)
            kernel32.VirtualProtectEx(self.h_process, address, 1, PAGE_EXECUTE_READWRITE, byref(old_protect))

            original_byte = self.read_process_memory(address, 1)
            if original_byte != False:

                # write the INT3 opcode
                if self.write_process_memory(address, "\xCC"):

                    # register the breakpoint in our internal list
                    self.breakpoints[address] = (original_byte)
                    return True
            else:
                return False

    def func_resolve(self, dll, function):
        print dll, " : ", function
        handle = kernel32.GetModuleHandleA(dll)
        address = kernel32.GetProcAddress(handle, function)
        print hex(address)
        #kernel32.CloseHandle(handle)

        return address
