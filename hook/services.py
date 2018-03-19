import os, sys
from time import sleep
from winappdbg import System, win32

def service_type(status):

    ret = ""
    if status & win32.SERVICE_INTERACTIVE_PROCESS:
        ret = "Service type: Win32 GUI ", status
    elif status & win32.SERVICE_WIN32:
        ret = "Service type: Win32 ", status
    elif status & win32.SERVICE_DRIVER:
        ret = "Service type: Driver ", status
    elif status & win32.SERVICE_CONTINUE_PENDING:
        ret = "Current status: RESTARTING... ", status
    elif status & win32.SERVICE_PAUSE_PENDING:
        ret = "Current status: PAUSING... ", status
    elif status & win32.SERVICE_PAUSED:
        ret = "Current status: PAUSED ", status
    elif status & win32.SERVICE_RUNNING:
        ret = "Current status: RUNNING ", status
    elif status & win32.SERVICE_START_PENDING:
        ret = "Current status: STARTING... ", status
    elif status & win32.SERVICE_STOP_PENDING:
        ret = "Current status: STOPPING... ", status
    elif status & win32.SERVICE_STOPPED:
        ret = "Current status: STOPPED ", status

    return ret


def service_list():

    #services = System.get_services()
    services = System.get_active_services()

    for desc in services:

        print "%s : %s\t(%s)" % (desc.ServiceName, desc.DisplayName, service_type(desc.CurrentState))


def main():
    service_list()

if __name__ == '__main__':
    main()