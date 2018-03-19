

import os, sys


a = [51,27,13,56]
b = dict(enumerate(a))
print b

sys.exit(1)


print(sys.prefix)

s = '81b90000100150450000'

print s

print os.path.curdir

for env in os.environ:

    print env , " : ", os.environ.get(env)

"""
print "\\x".join("{:02}".format(ord(c)) for c in s)


#print HexToByte(s)
#print ByteToHex(s)
#print ':'.join('{:02x}'.format(str(x)) for x in 'Hello World!')

print  ":".join("{0:}".format(ord(c)) for c in s)

print ''.join( [ "%02s " % ord( x ) for x in s ] ).strip()

"""