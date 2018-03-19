from winappdbg import Debug, EventHandler, System
from winappdbg.win32 import *
import json

class MyEventHandler(EventHandler):
    """
    This is the event handler class.
    """

    def load_dll(self, event):
        """
        This function is called when a new DLL is loaded.
        """

        # do something with the event object
        module = event.get_module()
        #print dir(module)
        logstring = "\nLoaded DLL:\nName: %s\nFilename: %s\nBase Addr: %s" % \
            (module.get_name(), module.get_filename(), hex(module.get_base()))
        #print logstring
        print "symbols:", json.dumps(module.get_symbols())


    def create_process(self, event):
        process  = event.get_process()
        pid      = event.get_pid()
        # pid    = process.get_pid()
        filename = process.get_filename()

        print("CreateProcess %d - %s" % (pid, filename))

    def exit_process(self, event):
        process  = event.get_process()
        pid      = event.get_pid()
        # pid    = process.get_pid()
        filename = process.get_filename()

        print("ExitProcess %d - %s" % (pid, filename))

    def create_thread(self, event):
        process  = event.get_process()
        thread   = event.get_thread()

        tid  = thread.get_tid()
        name = thread.get_name()

        print("CreateThread %d - %s" % (tid, name))

    def exit_thread(self, event):
        process  = event.get_process()
        thread   = event.get_thread()

        tid  = thread.get_tid()
        name = thread.get_name()

        print("ExitThread %d - %s" % (tid, name))



def simple_debugger( pid ):

    # Instance a Debug object, passing it the MyEventHandler instance.
    with Debug( MyEventHandler(), bKillOnExit = False ) as debug:

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