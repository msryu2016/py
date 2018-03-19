# -*- coding: utf-8 -*-
import optparse
import os, sys
import datetime
import pefile
from util import *
"""
dest : 변수이름, argument 가 저장될 변수이름
help : option 에 대한 help message
help message 안에서 사용할 수 있는 변수들, 대체로 %로 시작한다.
%default
%prog
metavar : help message 에서 argument 를 표현할 때 쓰임
default : dest 에 대한 default 값을 표현한다. 이것보다는 parser.set_defaults(my_dest=True) 를 사용하는 것이 좀 더 명확하다.
action : store 가 default 이다.
store : argument 를 저장
store_true : option 이 설정되면 그것을 true 로 저장
store_false : option 이 설정되면 그것을 false 로 저장
store_const : constant value 를 저장
append : argument 를 list 에 append
count : counter 를 하나 증가시킴
callback : 특정 callback function 을 호출
type
int
float
string
complex
choice
"""


def search_file(file, prefix=[]):

    if file.find('.dll') == -1:
        file = "%s.dll" % (file)

    if len(prefix) == 0:
        search_folder = [
            "",
            os.path.curdir,
            "%s\\Lib" % sys.prefix,
            "%s\\system32" % os.environ.get('SYSTEMROOT')]

    for folder in search_folder:
        filepath ="%s\\%s" % (folder, file)
        if os.path.exists(filepath):
            break

    if not os.path.exists(filepath):
        print file + " not found "
        sys.exit(-1)

    return filepath

def parsePE(file):
    pe = pefile.PE(file)

    ep = pe.OPTIONAL_HEADER.AddressOfEntryPoint
    ep_ava = ep + pe.OPTIONAL_HEADER.ImageBase
    print "EntryPoint:", hex(ep)
    print "ImageBase:", hex(ep_ava)

    return (pe, ep, ep_ava)

def search_import(pe, func):
    out = dir()

    for imp in pe.DIRECTORY_ENTRY_IMPORT:
        print "imp:", dir(imp)
        line = {}
        if isset(func) :
            if ismatch(imp.name, ".*"+func+".*"):
                #line = {'addr':hex(imp.address), 'name':imp.name}
                #print entry.dll, '\t', hex(imp.address), imp.name
                print
        else:
            #line = {'addr':hex(imp.address), 'name':imp.name}
            print '\t', imp.name

        out[entry.dll] = line

    return out

def print_function(pots, show=False):

    for key, pot in pots.items():
        if len(pot) > 0 :
            print key, " : ", pot.addr, " : ", pot.name

usage = "usage: %prog [options] arg"
"default=True, "
parser = optparse.OptionParser(usage=usage, version="%prog 1.0")
parser.add_option('-d', '--dll', dest='dll', type='string', help="Search DLL", metavar="DLL")
parser.add_option('-f', '--function', dest='function', type="string", help='Search Function in DLL', metavar="FUNCTION")
parser.add_option('-s', '--save', dest='save', type="string", help='save function', metavar="FILENAME")
#parser.add_option('-e', dest='export',action='store', Help='search entry_export')
#parser.set_defaults(export=False)

(options, args) = parser.parse_args()

if(options.dll == None):
    parser.print_help()
    sys.exit(2)

dllname = options.dll
funcname = options.function
savename = options.save
#export = options.export
print 'function:', funcname
def main():

    filepath = search_file(dllname)
    print
    print "Your choice to file:", filepath
    print

    pe, ep, ep_ava = parsePE(filepath)

    is_save = False
    if savename is not None:
        is_save =True
        fp = open(savename, "a+")

        print
    print "DIRECTORY_ENTRY_IMPORT"
    for entry in pe.DIRECTORY_ENTRY_IMPORT:

        for imp in entry.imports:
            if isset(funcname) :
                if ismatch(imp.name, ".*"+funcname+".*"):
                    print hex(imp.address), " ", imp.name, " : ", entry.dll

                    if is_save == True:
                        skin = """
def pre_%s(event):
    # %s : %s

    tid = event.get_tid()
    params = event.hook.get_params(tid)
    host_name = event.get_process().peak_string(params[0])
    process = event.get_process()

    sub_key = event.get_process().peek_string(params[1])

    proc = event.get_process()
    thread = event.get_thread()

    if proc.get_bits() == 32:
       a, b, c, d = thread.read_stack_dwords(9)
    else:
        context = thread.get_context()
        Rcx = context['Rcx']
        Rdx = context['Rdx']

    \"\"\"
    # Access first parameter on the stack: EBP + 4
    stack_offset = thread.get_sp() + 4
    # Write the new value at that address (e.g. 0 milliseconds)
    process.write_dword(stack_offset, 0x00)

    server_name = process.peek_string(lpszServerName, fUnicode=True)
    print server_name
    if ismatch(server_name, ".*naver\.com"):

        # mylogger.log_text(server_name)
        mem_write(event, process, "google.com")
        set_stack( process, thread, 8, new_addr)
                \"\"\"
                        """
                        line = skin % (imp.name, imp.name, hex(imp.address))
                        fp.write(line)
            else:
                print hex(imp.address), " ", imp.name, " : ", entry.dll



    if is_save == True:
        fp.close()


"""
    if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
        for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
            if isset(funcname) :
                if ismatch(imp.name, ".*"+funcname+".*"):
                    print hex(pe.OPTIONAL_HEADER.ImageBase + exp.address), exp.name, exp.ordinal
            else:
                print hex(pe.OPTIONAL_HEADER.ImageBase + exp.address), exp.name, exp.ordinal
"""




if __name__ == '__main__':
    main()