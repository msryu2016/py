import os, sys
import pprint, re
import inspect, pprint

def br(msg, _indent=4):

    if inspect.isclass(msg):
        dir(msg)
    else:
        pp = pprint.PrettyPrinter(indent=_indent)
        pp.pprint(msg)

    return False

def ismatch(str, reg):
    import re
    try:
        p = re.compile(reg)
        it = p.match(str)
    except:
        return False
    return it

def isset(str, isempty=True):
    try:
        str
    except NameError:
        return False

    if isempty == True:
        if str is None or str == "":
            return False
    return True


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

def dir_file_search(sdir,redir,recat):
    out = list()
    for root,dirnames, filenames in os.walk(sdir):
        for filename in filenames:
            re1 = redir.match(filename)
            if not re1 is None:
                filepath =os.path.join(root, filename)
                f = open(filepath, 'r')
                for line in f.readlines():
                    re2 = recat.match(line)
                    if not re2 is None:
                        #print line.replace('\n', '')
                        #sys.stdout.write(line)
                        out.append(line)
    return out