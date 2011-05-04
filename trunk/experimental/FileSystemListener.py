#!/usr/bin/python

#File:			FileSystemListener.py
#Description:		Diese Klasse ist der Handler fuer Aktivitaeten im FileSystem
#Author:		Lukas Knoepfel
#Creation Date:		14.4.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		14.4.2011	Grundgeruest erstellt
#			0.2		19.4.2011	Grundfunktionalitaet erstellt

from FileSystemListener_Linux import *
from FileSystemListener_Mac import *
from FileSystemListener_Windows import *
import threading
from File import *

class FileSystemListener(threading.Thread):
	listener = None 
	db = None
	def __init__(self,sys):
		threading.Thread.__init__(self)
		self.sys = sys
		self.db = sys.getDb()
		stros = self.sys.u.checkOS()
		if stros == "linux":
			print("it's a linux!")
			self.listener = FileSystemListener_Linux(self)
			return
		if stros == "win":
			print("it's a windows!")
			self.listener = FileSystemListener_Windows(self)
			return
		print "Can't initialize FileSystemListener."

	def add_watch(self, path, rec):
		self.listener.add_watch(path, rec)

	def run(self):
		self.listener.start()

	def stop(self):
		self.listener.stop()

	# Event kommt als String mit dem Dateipfad an. 
	def create_event(self, event):
		self.sys.gui.actview.update()
		print "create_event: ", event
		
	def delete_event(self, event):
		f = File(event)
		self.db.removeFile(f)
		print "delete_event: ", event
	def modify_event(self, event):
		print "modify_event: ", event