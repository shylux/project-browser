#!/usr/bin/python
import pyinotify
print "Hy"
wm = pyinotify.WatchManager()  # Watch Manager
mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY | pyinotify.IN_DELETE_SELF | pyinotify.IN_MOVE_SELF #  watched events

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print "Creating:", event.pathname

    def process_IN_DELETE(self, event):
        print "Removing:", event.pathname

    def process_IN_MODIFY(self, event):
	print "Modifying:", event.pathname

    def process_IN_DELETE_SELF(self,event):
        print "Deleting self:",event.pathname

    def process_IN_MOVE_SELF(self,event):
        print "Moving self:",event.pathname

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch('/home/vmadmin/Downloads', mask, rec=True)

print "start loop"
notifier.loop()
print "after loop"
