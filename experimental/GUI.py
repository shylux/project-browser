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

		#Init-Fenster
		self.xml = gtk.glade.XML("gui.glade")
		self.window = self.xml.get_widget("winMain")
		self.window.show()
		#self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("destroy", self.stopploop)

		self.button = self.xml.get_widget('btnHirarchical')
		self.button.connect('clicked', self.on_button1_clicked)

		self.button = self.xml.get_widget('btnTag')
		self.button.connect('clicked', self.on_button2_clicked)

		self.startloop()

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

	def on_button1_clicked(self,event):
		print('hirarchicalview')

	def on_button2_clicked(self,event):
		print('tagview')
