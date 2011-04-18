#!/usr/bin/python

#File:			GUI.py
#Description:		Klasse die die Grafikanzeige verwaltet
#Author:		Kaleb Tschabold
#Creation Date:		29.3.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		29.3.2011	Grundfunktionalitaeten werden erstellt
#			0.2		18.4.2011	Testen mit pygtk Elementen

from HirarchicalView import *
from TagView import *


#Modul um diese Klasse als Seperaten-Prozess zu starten
import threading
import gtk

gtk.gdk.threads_init()

class GUI(threading.Thread):
	def __init__(self,sys):
		threading.Thread.__init__(self)
		print('init')
		self.sys = sys
		self.mod = 'hirarchical'
		self.hview = HirarchicalView()
		self.tview = TagView()

		#Bottom-Container
		#self.bottomC = gtk.VBox()
		#self.bottomC.show()
		#self.content.pack_start(self.bottomC,True,True,0)

		#Left-Side
		#self.leftC = gtk.VBox()
		#self.leftC.show()
		#self.bottom.pack_start(self.leftC,True,True,0)

		#Right-Side
		#self.rightC = HirarchicalView()
		#self.rightC.show()
		#self.bottom.pack_start(self.rightC,True,True,0)

		#self.rightC.put(self.button3,3,3)

	# Destroy method causes appliaction to exit
	# when main window closed

	def run(self):
		print('run: GUI')
		#Init-Fenster
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("destroy", gtk.main_quit)

		#Window-Properties
		self.window.set_size_request(700, 350)
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.set_title('Project-Browser')
		self.window.show()

		#Main-Container
		self.content = gtk.VBox()
		self.content.show()
		self.window.add(self.content)
		
		#Menu-Container
		self.menu = gtk.Label("Menu")
		self.menu.show()
		self.menuC = gtk.Fixed()
		self.menuC.show()
		self.menuC.put(self.menu,100,100)
		self.content.pack_start(self.menuC,False,False,0)

		self.inputC = gtk.Entry()
		self.inputC.show()
		self.content.pack_start(self.inputC,False,False,0)

		self.button3 = gtk.Button("Hello World")
		self.button3.connect('clicked',self.hello)
		self.button3.show()
		self.content.pack_start(self.button3,False,False,0)
		
		#Wird nicht gebraucht, weil das CLI automatisch eine Schleife macht
		gtk.main()


	def hello(self,widget,data=None):
		widget.set_label('geklickt')
		print('event: '+str(widget)+', '+str(data))

	def count_in_thread(self, maximum):
		Thread(target=self.count_up, args=(maximum,)).start()
