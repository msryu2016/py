import winappdbg

# If no arguments, print running processes
system = winappdbg.System()

# We can reuse example 02 from the docs
# https://winappdbg.readthedocs.io/en/latest/Instrumentation.html#example-2-enumerating-running-processes
table = winappdbg.Table("\t")
table.addRow("", "")

header = ("pid", "process")
table.addRow(*header)

table.addRow("----", "----------")

processes = {}

# Add all processes to a dictionary then sort them by pid
for process in system:
    processes[process.get_pid()] = process.get_filename()

# Iterate through processes sorted by pid
for key in sorted(processes.iterkeys()):
    table.addRow(key, processes[key])

print table.getOutput()