from winappdbg import Debug, EventHandler, System
from winappdbg.win32 import *


class MyEventHandler(EventHandler):
    apiHooks = {
        'kernel32.dll': [
            ("Sleep", 1)
        ]
    }

    # Intercept the API before the actual call is being made to Sleep ('pre' callback)
    def pre_Sleep(self, event, retval, dwMilliseconds):
        thread = event.get_thread()
        process = event.get_process()
        print process
        print "Intercepted Sleep call of %d milliseconds"

        # Access first parameter on the stack: EBP + 4
        stack_offset = thread.get_sp() + 4
        # Write the new value at that address (e.g. 0 milliseconds)
        process.write_dword(stack_offset, 0x00)



def simple_debugger( pid ):

    # Instance a Debug object, passing it the MyEventHandler instance.
    with Debug( MyEventHandler(), bKillOnExit = True ) as debug:

        # Start a new process for debugging.

        debug.attach( pid )

        # Wait for the debugee to finish.
        debug.loop()


# When invoked from the command line,
# the first argument is an executable file,
# and the remaining arguments are passed to the newly created process.
if __name__ == "__main__":
    import sys
    pid = int( sys.argv[1] )
    simple_debugger( pid )