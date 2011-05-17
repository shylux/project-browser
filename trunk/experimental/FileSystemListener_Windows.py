#!/usr/bin/python

#File:			FileSystemListener_Windows.py
#Description:		Diese Klasse kann auf einem Windows das File System ueberwachen
#Author:		Lukas Knoepfel
#Creation Date:		14.4.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		14.4.2011	Grundgeruest erstellt
#			0.2		19.4.2011	Grundfunktionalitaet erstellt

try:
	import os
	import win32file
	import win32con
except ImportError:
	#shit happens :P
	pass

class FileSystemListener_Windows():
    parent = None
    acpath = None
    hdir = None
    ACTIONS = {
           1 : "Created",
           2 : "Deleted",
           3 : "Modified",
           4 : "Delete",#"Renamed from something"
           5 : "Created"#"Renamed to something"
           }
    FILE_LIST_DIRECTORY = 0x0001

    def __init__(self, tparent):
        self.parent = tparent

    def add_watch(self, path, recur):
        self.acpath = path
        self.hdir = win32file.CreateFile(
            path,
            self.FILE_LIST_DIRECTORY,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
            None,
            win32con.OPEN_EXISTING,
            win32con.FILE_FLAG_BACKUP_SEMANTICS,
            None
            )

    def start(self):
        while 1:
            results = win32file.ReadDirectoryChangesW(
                self.hdir,
                1024,
                True,
                win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                win32con.FILE_NOTIFY_CHANGE_SIZE |
                win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                win32con.FILE_NOTIFY_CHANGE_SECURITY,
                None,
                None
                )

            for action, file in results:
                full_filename = os.path.join(self.acpath, file)
                #print full_filename, self.ACTIONS.get(action, "Unknown")
                if action == 3:
		    self.parent.modify_event(full_filename)
                elif action == 1 or action == 5:
                    self.parent.create_event(full_filename)
                elif action == 2 or action == 4:
                    self.parent.delete_event(full_filename)
