import winappdbg
import argparse
from winappdbg import win32


from winappdbg.win32 import *


def main():

#    print_drivers(True)


    parser = argparse.ArgumentParser(description="WinAppDbg stuff.")
    parser.add_argument("-p", "--pid", help="process id")

    args = parser.parse_args()

    args.pid = long(args.pid)
    if (args.pid):
        system = winappdbg.System()

        # Get all pids
        pids = system.get_process_ids()
        print pids
        if args.pid in pids:
            # pid exists

            # Create a Debug object
            debug = winappdbg.Debug()

            try:
                # Attach to pid
                # attach: https://github.com/MarioVilas/winappdbg/blob/master/winappdbg/debug.py#L219
                my_process = debug.attach(int(args.pid))

                print "Attached to %d - %s" % (my_process.get_pid(),
                                               my_process.get_filename())

                # Keep debugging until the debugger stops
                debug.loop()

            finally:
                # Stop the debugger
                debug.stop()
                print "Debugger stopped."

        else:
            print "pid %d not found." % (args.pid)

        exit()

    else:
        print "%s not found." % (args.pid)


if __name__ == "__main__":
    main()