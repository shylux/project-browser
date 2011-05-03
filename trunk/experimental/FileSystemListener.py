#!/usr/bin/python

#File:			FileSystemListener.py
#Description:		Diese Klasse ist der Handler fuer Aktivitaeten im FileSystem
#Author:		Lukas Knoepfel
#Creation Date:		14.4.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		14.4.2011	Grundgeruest erstellt
#			0.2		19.4.2011	Grundfunktionalitaet erstellt

try:
	from FileSystemListener_Linux import *
except:
	pass
try:
	from FileSystemListener_Mac import *
except:
	pass
try:
	from FileSystemListener_Windows import *
except:
	pass
import threading

class FileSystemListener(threading.Thread):
	listener = None 
	def __init__(self,sys):
		threading.Thread.__init__(self)
		self.sys = sys

	def run(self):
		stros = self.sys.u.checkOS()
		if stros == "linux":
			print("it's a linux!")
			self.listener = FileSystemListener_Linux(self)
		if stros == "win":
			print("it's a windows!")
			self.listener = FileSystemListener_Windows(self)

	def add_watch(self, path, rec):
		self.listener.add_watch(path, rec)

	def startlistener(self):
		self.listener.start()

	# Event kommt als String mit dem Dateipfad an. 
	def create_event(self, event):
		print "create_event: ", event
	def delete_event(self, event):
		print "delete_event: ", event
	def modify_event(self, event):
		print "modify_event: ", event
