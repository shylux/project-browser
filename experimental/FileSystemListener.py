#!/usr/bin/python

#File:			FileSystemListener.py
#Description:		Diese Klasse ist der Handler fuer Aktivitaeten im FileSystem
#Author:		Lukas Knoepfel
#Creation Date:		14.4.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		14.4.2011	Grundfunktionalitaeten werden erstellt

from FileSystemListener_Linux import *
from FileSystemListener_Mac import *
from FileSystemListener_Windows import *
from Utility import *

class FileSystemListener:
	listener = None 
	def __init__(self):
		util = Utility()
		stros = util.checkOS()
		if stros == "linux":
			print("it's a linux!")
			self.listener = FileSystemListener_Linux(self)

	def add_watch(self, path, rec):
		self.listener.add_watch(path, rec)

	def start(self):
		self.listener.start()

	# Event kommt als String mit dem Dateipfad an. 
	def create_event(self, event):
		print "create_event: ", event
	def delete_event(self, event):
		print "delete_event: ", event
	def modify_event(self, event):
		print "modify_event: ", event
