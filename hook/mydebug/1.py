from ctypes import *
import time, os

msvcrt = cdll.msvcrt
counter = 0

while 1:
    msvcrt.printf("Loop %d : %d\n", counter, os.getpid())
    time.sleep(2)
    counter += 1