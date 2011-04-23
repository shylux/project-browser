#!/usr/bin/python

#File:			GUI.py
#Description:		Klasse die die Grafikanzeige verwaltet
#Author:		Kaleb Tschabold
#Creation Date:		29.3.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		29.3.2011	Grundfunktionalitaeten werden erstellt
#			0.2		18.4.2011	Testen mit pygtk Elementen
#Link:
#http://zignar.net/page/pygtk-mit-glade			 mit xml(aus glade) Programm Grafische Oberflaeche erstellen

from HirarchicalView import *
from TagView import *


#Modul um diese Klasse als Seperaten-Prozess zu starten
import threading
import pygtk
import gtk
import gtk.glade
import gobject
import sys

gtk.gdk.threads_init()

class GUI(threading.Thread):
	def __init__(self,sys):
		threading.Thread.__init__(self)
		print('init')
		self.sys = sys
		self.mod = 'hirarchical'
		self.hview = HirarchicalView()
		self.tview = TagView()

	def run(self):
		print('run: GUI')

		#Init-Window
		self.xml = gtk.glade.XML("gui.glade")
		self.window = self.xml.get_widget("winMain")
		self.window.show()
		#self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("destroy", self.stopploop)

		#Connect Toogle-Buttons
		self.btnHirarchical = self.xml.get_widget('btnHirarchical')
		self.btnHirarchical.connect('toggled', self.showHirarchical)
		self.btnTag = self.xml.get_widget('btnTag')
		self.btnTag.connect('toggled', self.showTag)

		#Connect TextInput Field
		self.txtEntry = self.xml.get_widget('txtEntry')
		self.txtEntry.connect('key_press_event',self.search)
		#self.txtEntry.connect('activate',self.search)
		#self.txtEntry.connect('backspace',self.search)

		self.view = self.xml.get_widget('hbxView')

		#Add Menu-Item by 'Ansicht'
		ansichtmenu = gtk.Menu()
		ansicht = self.xml.get_widget('mnuAnsicht')
		ansicht.set_submenu(ansichtmenu)
		self.mnuHirarchical = gtk.RadioMenuItem(None,'Hirarchisch')
		self.mnuHirarchical.connect('toggled',self.showHirarchical)
		ansichtmenu.append(self.mnuHirarchical)
		self.mnuTag = gtk.RadioMenuItem(self.mnuHirarchical,'Tag')
		self.mnuTag.connect('toggled',self.showTag)
		self.mnuTag.set_active(True)
		ansichtmenu.append(self.mnuTag)

		#Zeigt alles an
		self.window.show_all()

		self.startloop()
		


	#GUI Functionen
	def showHirarchical(self,event):
		if isinstance(event,gtk.RadioMenuItem):
			if self.mnuHirarchical.get_active():
				self.btnHirarchical.set_active(True)
			else:
				self.btnHirarchical.set_active(False)
		else:
			if self.btnHirarchical.get_active():
				self.mnuHirarchical.set_active(True)
			else:
				self.mnuHirarchical.set_active(False)
		print('hirarchicalview')

	def showTag(self,event):
		if isinstance(event,gtk.RadioMenuItem):
			if self.mnuTag.get_active():
				self.btnTag.set_active(True)
			else:
				self.btnTag.set_active(False)
		else:
			if self.btnTag.get_active():
				self.mnuTag.set_active(True)
			else:
				self.mnuTag.set_active(False)
		print('tagview')

	
	def search(self,widget,event):
		print('serach')
		pass
	###


	def terminate(self):
		# must raise the SystemExit type, instead of a SystemExit() instance
		# due to a bug in PyThreadState_SetAsyncExc
		self.raise_exc(SystemExit)
		pass

	def startloop(self):
		gtk.main()

	def stopploop(self,event=''):
		print('quite')
		gtk.main_quit()
		self.sys.stoppall()
