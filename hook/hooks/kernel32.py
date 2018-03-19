

# Intercept the API before the actual call is being made to Sleep ('pre' callback)
def hook_Sleep(event):
    thread = event.get_thread()
    process = event.get_process()

    print "Intercepted Sleep call of %d milliseconds"

    # Access first parameter on the stack: EBP + 4
    stack_offset = thread.get_sp() + 4
    # Write the new value at that address (e.g. 0 milliseconds)
    process.write_dword(stack_offset, 0x00)