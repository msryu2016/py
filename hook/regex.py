import os,re

def ismatch(str, reg):
    import re
    p = re.compile(reg)
    return p.match(str)


str = "c:\temp\1.txt"
#str = "c:\temp\2.exe"
reg = ".+\.txt$"

"""

p = re.compile(reg)
m = p.match( str )
if m:
    print('Match found: ', m.group())
else:
    print('No match')
"""

if ismatch(str, reg):
    print('Match found: ', str)
else:
    print('No match')


server_name ="naver.com"
server_name ="daum.com"
if ismatch(server_name, ".*naver\.com"):
    print('Match found: ', server_name)
else:
    print('No match')