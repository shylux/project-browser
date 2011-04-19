#!/usr/bin/python

#File:			FileSystemListener_Linux.py
#Description:		Diese Klasse kann auf einem Linux das File System ueberwachen
#Author:		Lukas Knoepfel
#Creation Date:		14.4.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		14.4.2011	Grundgeruest erstellt
#			0.2		18.4.2011	Events werden korrekt abgefangen. TODO: add_watch implementieren und blockierendes .loop() in thread

import pyinotify

class FileSystemListener_Linux(pyinotify.ProcessEvent):
	listener = None
	notifier = None
	parent = None
	mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY # watched events
	def __init__(self, tparent):
		self.parent = tparent
		self.listener = pyinotify.WatchManager()
		self.notifier = pyinotify.Notifier(self.listener, self)
		#self.listener.add_watch('/home/shylux/project-browser', self.mask, rec=True)

	def add_watch(self, path, recur):
		print recur
		self.listener.add_watch(path, self.mask, rec=recur)

	def start(self):
		self.notifier.loop()

	def process_IN_CREATE(self, event):
		self.parent.create_event(event.pathname)
	def process_IN_DELETE(self, event):
		self.parent.delete_event(event.pathname)
	def process_IN_MODIFY(self, event):
		self.parent.modify_event(event.pathname)
