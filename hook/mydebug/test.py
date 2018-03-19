import sys
import my_debugger

debugger= my_debugger.debugger()

#debugger.load(r'c:\windows\system32\calc.exe')

pid= int(sys.argv[1])

debugger.attach(pid)

printf_address= debugger.func_resolve("msvcrt.dll", "printf")

debugger.bp_set(printf_address)

debugger.run()


debugger.detach()