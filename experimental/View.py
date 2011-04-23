#!/usr/bin/python

#File:			View.py
#Description:		Diese Klasse kann die 2 Ansichten(Tag und Hirarchisch) verwalten
#Author:		Kaleb Tschabold
#Creation Date:		14.4.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		14.4.2011	Grundfunktionalitaeten werden erstellt
#			0.2		18.4.2011	Erbt von gtk.Layout

import gtk
import gobject
import os

class View(gtk.Layout):
	def __init__(self,sys):
		gtk.Layout.__init__(self)
		self.sys = sys
		self.acttxtinput = ''
		pass

	def openFile(self,path):
		if self.sys.c.os == 'linux':
			#Funktioniert nur bei Ubuntu
			os.system('/usr/bin/xdg-open '+path)
		elif self.sys.c.os == 'win':
			os.filestart(path)
		else:
			#Da muss noch eine Loesung sein, wenn die Datei nicht gestartet werden kann
			pass

	def update(self):
		self.show_all()

	def set_actTxtInput(self,text):
		self.acttxtinput = text

	def get_actTxtInput(self):
		return self.acttxtinput

#Registriert diese Klasse als pygtk-widget
gobject.type_register(View)
