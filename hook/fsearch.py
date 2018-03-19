import os, sys
import pefile
import pprint

def br(msg):
    import pprint

    pp = pprint.PrettyPrinter(indent=4)
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


cnt = len(sys.argv)
if cnt == 2:
    line = sys.argv[1]
    if line.find('!') > 0:
        file, func = line.split("!")
    else :
        file = line
        func = ""
elif cnt>2:
    file = sys.argv[1]
    func = sys.argv[2] if len(sys.argv) > 2 else ""
else:
    print "usage %s file func"
    print "\t\tfile!func"
    sys.exit(0)

if not file.find('.dll') > 0 :
    file += ".dll"


print "%s!%s" % (file, func)
print "isset:", isset(func)

lib = "%s\\Lib" % sys.prefix
win = "%s\\system32" % os.environ.get('SYSTEMROOT')
search_folder = ["", os.path.curdir, lib, win]

for name in search_folder:

    filepath = "%s\\%s" % (name, file)
    if os.path.exists(filepath):
        break;

if not os.path.exists(filepath):
    print file + " not found "
    sys.exit(-1)

print filepath

pe = pefile.PE(filepath)

ep = pe.OPTIONAL_HEADER.AddressOfEntryPoint
ep_ava = ep + pe.OPTIONAL_HEADER.ImageBase

print "EntryPoint:", hex(ep)
print "ImageBase:", hex(ep_ava)

for section in pe.sections:
    print section.Name, hex(section.VirtualAddress), section.SizeOfRawData

print
print "DIRECTORY_ENTRY_IMPORT"
for entry in pe.DIRECTORY_ENTRY_IMPORT:

    for imp in entry.imports:
        if isset(func) :
            """
            func_name = imp.name
            if ismatch(func_name, ".*"+func+".*"):
                print '\t', hex(imp.address), imp.name
            """
            if ismatch(imp.name, ".*"+func+".*"):
                print entry.dll, '\t', hex(imp.address), imp.name
        else:
            print '\t', hex(imp.address), imp.name
"""

print
print "DIRECTORY_ENTRY_EXPORT"
if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
    for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        if isset(func) :
            if ismatch(imp.name, ".*"+func+".*"):
                print hex(pe.OPTIONAL_HEADER.ImageBase + exp.address), exp.name, exp.ordinal
        else:
            print hex(pe.OPTIONAL_HEADER.ImageBase + exp.address), exp.name, exp.ordinal
"""