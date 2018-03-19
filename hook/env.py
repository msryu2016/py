import os, sys


print sys.prefix
print os.path.curdir

for env in os.environ:

    print env , " : ", os.environ.get(env)