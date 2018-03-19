import sys, os
from hack import Hack, EventHandler
from hooks import *
from inspect import getmembers, isfunction

def sendto(event, ra, s, buf, length, flags, to, tolength):
    data = event.get_process().peek(buf, length)
    print "Send: " + data + "\n"


def mem_write(event, process, str):

    new_str = str.encode("utf-16le")
    new_len = len(new_str)
    new_addr = event.get_process().malloc(new_len)+1
    process.write(new_addr, new_str)
    return new_addr

def set_stack( process, thread, pos, addr):

    bits = thread.get_bits()
    emulation = thread.is_wow64()
    top_of_stack = thread.get_sp()
    if bits == 32 or emulation is True:

        # Write the pointer to the new payload with the old one
        process.write_dword(top_of_stack + pos, addr)

    elif bits == 64:
        thread.set_register("Rdx", new_payload_addr)

def ismatch(str, reg):
    import re
    p = re.compile(reg)
    return p.match(str)

class MyEventHandler(EventHandler):
    apiHooks = {
        'kernel32.dll': [
            ("Sleep", 1)
        ]
    }

def pre_HttpSendRequestW(event):

    proc = event.get_process()
    thread = event.get_thread()

    if proc.get_bits() == 32:
        hRequest, lpszHeaders,dwHeadersLength, lpOptional, dwOptionalLength = thread.read_stack_dwords(6)[1:]
    else:
        context = thread.get_context()
        lpFileName = context['Rcx']
        dwDesiredAccess = context['Rdx']


    if dwHeadersLength != 0:
        headers = process.peek_string(lpszHeaders, fUnicode=True)
        print("Headers %s" % (headers))

    if dwOptionalLength != 0:
        # This is not unicode - see the pointer name (lp vs. lpsz)
        # fUnicode is set to False (default) then
        optional = process.peek_string(lpOptional, fUnicode=False)

        print("Optional %s" % (optional))

def pre_HttpOpenRequestW(event):

    process = event.get_process()

    proc = event.get_process()
    thread = event.get_thread()

    if proc.get_bits() == 32:
        hConnect, lpszVerb,lpszObjectName, lpszVersion, lpszReferer,lplpszAcceptTypes, dwFlags, dwContext = thread.read_stack_dwords(9)[1:]
    else:
        context = thread.get_context()
        hConnect = context['Rcx']
        lpszVerb = context['Rdx']

    verb = process.peek_string(lpszVerb, fUnicode=True)
    if verb is None:
        verb = "GET"

    obj = process.peek_string(lpszObjectName, fUnicode=True)

    print("HttpOpenRequestW")
    print("verb: %s" % verb)
    print("obj : %s" % obj)


# Intercept the API before the actual call is being made to Sleep ('pre' callback)
def pre_Sleep(event):
    thread = event.get_thread()
    process = event.get_process()

    print "Intercepted Sleep call of %d milliseconds"

    # Access first parameter on the stack: EBP + 4
    stack_offset = thread.get_sp() + 4
    # Write the new value at that address (e.g. 0 milliseconds)
    process.write_dword(stack_offset, 0x00)


def pre_InternetConnectW(event ):

    process = event.get_process()
    process.suspend()
    thread = event.get_thread()

    if process.get_bits() == 32:
        hInternet, lpszServerName,nServerPort, lpszUsername, lpszPassword,dwService, dwFlags, dwContext = thread.read_stack_dwords(9)[1:]
    else:
        context = thread.get_context()
        hConnect = context['Rcx']
        lpszVerb = context['Rdx']

    server_name = process.peek_string(lpszServerName, fUnicode=True)
    print server_name
#    if server_name == "naver.com" or server_name == "www.naver.com":
    if ismatch(server_name, ".*naver\.com"):

        # mylogger.log_text(server_name)
        mem_write(event, process, "google.com")
        set_stack( process, thread, 8, new_addr)
        """
        bits = thread.get_bits()
        emulation = thread.is_wow64()

        if bits == 32 or emulation is True:

            # Write the pointer to the new payload with the old one
            process.write_dword(top_of_stack + 8, new_payload_addr)

        elif bits == 64:
            thread.set_register("Rdx", new_payload_addr)
        """
    process.resume()

def pre_ChromeMain():

    process = event.get_process()
    thread = event.get_thread()
    context = thread.get_context()

    a, b, c, d, e, f, g, h, i, j = thread.read_stack_dwords(11)[1:]
    print a
    print b
    print c
    print d
    print e
    print f
    print g
    print h
    print i
    print j

def cb_createfilew(event):

    process = event.get_process()
    process.suspend()
    thread = event.get_thread()

    if process.get_bits() == 32:
        lpFileName, dwDesiredAccess = thread.read_stack_dwords(3)[1:]
    else:
        context = thread.get_context()
        lpFileName = context['Rcx']
        dwDesiredAccess = context['Rdx']

    filename = process.peek_string(lpFileName, fUnicode=True)
    print filename

    if ismatch(filename, ".*\.exe$"):
        new_file = filename.replace('exe','bin')
        new_addr = mem_write(event, process, new_file)
        set_stack( process, thread, 4, new_addr)

    process.resume()
    """
    access = ''
    if dwDesiredAccess & 0x80000000: access += 'R'
    if dwDesiredAccess & 0x40000000: access += 'W'

    processHandle = process.read_pointer( stack+4 )
    print "processHandle " + hex(processHandle)
    BaseAddress = process.read_pointer( stack+8 )
    print "BaseAddress " + hex(BaseAddress)
    Buffer = process.read_pointer( stack+12 )
    print "Buffer " + hex(Buffer)
    NumberOfBytesToWrite = process.read_pointer( stack+16 )
    print "NumberOfBytesToWrite " + hex(NumberOfBytesToWrite)
    NumberOfBytesWritten = process.read_pointer( stack+16 )
    print "NumberOfBytesWritten " + hex(NumberOfBytesWritten)
    print "====================="
    print "virtualQuery - " + windll.kernel32.VirtualQueryEx(int(processHandle), BaseAddress)
    """

def post_CreateFileW(event, retval):


    tid = event.get_tid()
    params = event.hook.get_params(tid)

    print params

def _split_dll_func(str, seq=1):

    if str.find("!") == -1:
        return ("", "")
    else:
        return str.split("!", seq)


#h = Hack(processName="iexplore.exe")
#h = Hack(processName="sleep.exe")
pid = sys.argv[1] if len(sys.argv) > 1 else None
act = sys.argv[2] if len(sys.argv) > 2 else None
print "act:", act

if pid is None:
    print
    print "usage : %s pid [act]" % sys.argv[0]
    sys.exit(-1)

h = Hack(pid=pid)


if not act is None and os.path.exists(act):
    fp = open(act, "r")
    hook_list = []
    for line in fp.readlines():
        print line
        dll, func, callback = _split_dll_func(line,2)

        if not dll is None or not func is None or not callback is None :
            print "1"
            h.add_hook(dll, func, callback)
        else:
            print "2"
            hook_list = [ o for o in getmembers(dll) if isfunction(o[1])]

            print hook_list

else :

    if not act is None :
        dll, func, callback = _split_dll_func(act,2)
        if not dll is None or not func is None or not callback is None :
            print dll, " : ", func, " : ", callback
            h.add_hook(dll, func, callback)
    #h.add_hook("ws2_32.dll", "sendto", sendto)

h.add_hook("kernel32", "CreateFileW", post_CreateFileW)
h.add_hook("kernel32", "CreateFileA", post_CreateFileW)
#h.add_hook("kernel32", "Sleep", pre_Sleep)
#h.add_hook("Wininet", "HttpSendRequestW", pre_HttpSendRequestW)
#h.add_hook("Wininet", "HttpSendRequestA", pre_HttpSendRequestW)
#h.add_hook("Wininet", "HttpOpenRequestW", pre_HttpOpenRequestW)
#h.add_hook("Wininet", "HttpOpenRequestA", pre_HttpOpenRequestW)
#h.add_hook("Wininet", "InternetConnectW", pre_InternetConnectW)

#h.add_hook("C:\\Program Files\\Google\\Chrome\\Application\\64.0.3282.186\\chrome.dll", "GetHandleVerifier", pre_ChromeMain)
#h.add_hook("C:\\Program Files\\Google\\Chrome\\Application\\64.0.3282.186\\chrome_watcher.dll", "WatcherMain", pre_ChromeMain)

h.hook()
h.safe_exit()