# This doesn't work
from win32com.client import Dispatch

# This line will always create a new window
ie = Dispatch("InternetExplorer.Application")

print ie.LocationURL