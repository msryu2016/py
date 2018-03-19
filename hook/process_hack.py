from winappdbg import Process
import os, sys






def main():


    pid = int(sys.argv[1])
    proc = Process(pid)


    #= info

    print "pid;", proc.get_pid()
    print "is_alive;", proc.is_alive()
    print "is_debugged;", proc.is_debugged()
    print "is_wow;", proc.is_wow64()
    print "arch;", proc.get_arch()
    print "bits;", proc.get_bits()
    print "filename:", proc.get_filename()
    print "exit_time;", proc.get_exit_time()
    print "running_time;", proc.get_running_time()
    print "service;", proc.get_services()
    print "policy;", proc.get_dep_policy()
    print "peb;", proc.get_peb()
    print "main_module;", proc.get_main_module()
    print "peb_address", proc.get_peb_address()
    print "entry_point;", proc.get_entry_point()

    print "image_base;", proc.get_image_base()
    print "image_name;", proc.get_image_name()
    print "command_line;", proc.get_command_line()
    print "environment;", proc.get_environment()
    print "handle;", proc.get_handle()

    print "resume;",proc.resume()
    #print "clean_exit;", proc.clean_exit()


if __name__ == '__main__':
    main()
