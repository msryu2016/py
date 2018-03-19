import winappdbg
import argparse
from winappdbg import win32


from winappdbg.win32 import *

def print_drivers( fFullPath = False ):

    # Determine if we have 32 bit or 64 bit pointers.
    if sizeof(SIZE_T) == sizeof(DWORD):
        fmt = "%.08x\t%s"
        hdr = "%-8s\t%s"
    else:
        fmt = "%.016x\t%s"
        hdr = "%-16s\t%s"

    # Get the list of loaded device drivers.
    ImageBaseList = EnumDeviceDrivers()
    print "Device drivers found: %d" % len(ImageBaseList)
    print
    print hdr % ("Image base", "File name")

    # For each device driver...
    for ImageBase in ImageBaseList:

        # Get the device driver filename.
        if fFullPath:
            DriverName = GetDeviceDriverFileName(ImageBase)
        else:
            DriverName = GetDeviceDriverBaseName(ImageBase)

        # Print the device driver image base and filename.
        print fmt % (ImageBase, DriverName)

def print_modules( pid ):

    # Determine if we have 32 bit or 64 bit pointers.
    if sizeof(SIZE_T) == sizeof(DWORD):
        fmt = "%.8x    %.8x    %s"
        hdr = "%-8s    %-8s    %s"
    else:
        fmt = "%.16x    %.16x    %s"
        hdr = "%-16s    %-16s    %s"

    # Print a banner.
    print "Modules for process %d:" % pid
    print
    print hdr % ("Address", "Size", "Path")

    # Create a snapshot of the process, only take the heap list.
    hSnapshot = CreateToolhelp32Snapshot( TH32CS_SNAPMODULE, pid )

    # Enumerate the modules.
    module = Module32First( hSnapshot )
    while module is not None:

        # Print the module address, size and pathname.
        print fmt % ( module.modBaseAddr,
                      module.modBaseSize,
                      module.szExePath )

        # Next module in the process.
        module = Module32Next( hSnapshot )

    # No need to call CloseHandle, the handle is closed automatically when it goes out of scope.
    return


def main():

#    print_drivers(True)


    parser = argparse.ArgumentParser(description="WinAppDbg stuff.")
    parser.add_argument("-r", "--run", help="path to application")

    args = parser.parse_args()

    if win32.PathFileExists(args.run) is True:

        debug = winappdbg.Debug()

        try :
            my_process = debug.execv([args.run])

            print "Attached to %d -%s " % (my_process.get_pid(), my_process.get_filename())

            print_modules(my_process.get_pid())


            debug.loop()
        finally:
            debug.stop()
            print "debugger stopped"

    else:
        print "%s not found." % (args.run)


if __name__ == "__main__":
    main()