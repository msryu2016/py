from winappdbg import Process, System, Thread, win32
import os, sys, time

def print_thread_context( tid ):

    # Request debug privileges.
    System.request_debug_privileges()

    # Instance a Thread object.
    thread = Thread( tid )

    # Suspend the thread execution.
    thread.suspend()

    # Get the thread context.
    try:
        context = thread.get_context()

    # Resume the thread execution.
    finally:
        thread.resume()

    # Display the thread context.
    print
    print CrashDump.dump_registers( context ),

def freeze_threads( pid, _tid=None ):
    System.request_debug_privileges()

    process = Process(pid)
    process.scan_threads()

    tmp = _tid.split(',')
    print tmp, ":", type(tmp), ":", len(tmp)

    for thread in process.iter_threads():
        tid = thread.get_tid()
        _tid = int(tid)
        if _tid is None or _tid == 0 :
            thread.suspend()
            print tid, " suspend()"
        else:
            if len(tmp)>1:
                for s in tmp:
                    if tid == int(s):
                        print tid, " suspend()"
                        thread.suspend()
            else:
                if tid == _tid:
                    print tid, " suspend()"
                    thread.suspend()

def unfreeze_thread( pid, _tid=None ):
    System.request_debug_privileges()

    process = Process(pid)
    process.scan_threads()

    tmp = _tid.split(',')
    print tmp, ":", type(tmp), ":", len(tmp)

    for thread in process.iter_threads():
        tid = thread.get_tid()
        _tid = int(tid)
        if _tid is None or _tid == 0:
            thread.resume()
            print tid, " resume()"
        else:
            if len(tmp)>1:
                for s in tmp:
                    if tid == int(s):
                        print tid, " resume()"
                        thread.resume()


def kill_thread( pid, kill_tid=None ):
    System.request_debug_privileges()

    process = Process(pid)
    process.scan_threads()
    tmp = kill_tid.split(',')
    print tmp, ":", type(tmp), ":", len(tmp)

    for thread in process.iter_threads():
        thread.suspend()
        tid = thread.get_tid()

        try:
            if kill_tid is None or kill_tid == 0:
                hThread = thread.get_handle()
                win32.CloseHandle(hThread)
                win32.TerminateThread(hThread, -999)
            else:
                if len(tmp)>1:
                    for s in tmp:
                        if tid == int(s):
                            print "kill > ", pid, " > ", tid, " > ", kill_tid
                            hThread = thread.get_handle()

                            #win32.CloseHandle(hThread)
                            win32.TerminateThread(hThread, -999)
        except Exception, e:
            print e
            pass
        thread.resume()

def list_thread( pid ):
    System.request_debug_privileges()

    process = Process(pid)
    process.scan_threads()

    list=[]
    for thread in process.iter_threads():
        tid = thread.get_tid()
        list.append(str(tid))
        try:
            print_thread_context( tid )
        except:
            pass
    pid_line = ','.join(list)
    print pid_line

    return pid_line

def usage(sys):
    script = sys.argv[0]
    print "%s f <pid> freeze a process "  % script
    print "%s u <pid> unfreeze a process "  % script
    print "%s l <pid> list process "  % script
    print "%s k <pid> <tid>kill a process "  % script
    print "%s d <pid> daemon"  % script
if __name__ == '__main__':

    import sys

    if len(sys.argv) < 3:
        usage(sys)
        sys.exit(-1)

    command = sys.argv[1].lower()
    pid = int(sys.argv[2])

    if command  == 'f':
        tid = sys.argv[3]
        freeze_threads(pid, tid)
    elif command == 'u':
        tid = sys.argv[3]
        unfreeze_thread(pid, tid)
    elif command == 'l':
        pid_line = list_thread(pid)

        fp = open("freeze_thread_list.txt", "a+")
        fp.write(pid_line+"\n")
        fp.close()
    elif command == 'k':
        tid = sys.argv[3]
        kill_thread(pid, tid)
    elif command == 'd':
        orig_pid_line = list_thread(pid)

        while True:

            pid_line = list_thread(pid)

#            kill_line = set(orig_pid_line) - (pid_line)
            print "orig:", orig_pid_line
            print "new :", pid_line
            set_list= list(set(orig_pid_line.split(',')).intersection(set(pid_line.split(','))))

            if len(set_list)>0:
                kill_thread(pid, ','.join(list(set(pid_line.split(','))-set(set_list)) ))
            else:
                kill_thread(pid, ''.join(list(set(pid_line.split(','))-set(set_list)) ))

            time.sleep(10)


    else:
        usage()
