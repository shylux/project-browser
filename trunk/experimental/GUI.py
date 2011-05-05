#!/usr/bin/python

#File:			GUI.py
#Description:		Klasse die die Grafikanzeige verwaltet
#Author:		Kaleb Tschabold
#Creation Date:		29.3.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		29.3.2011	Grundfunktionalitaeten werden erstellt
#			0.2		18.4.2011	Testen mit pygtk Elementen
#			0.3		23.4.2011	Erstellte Event's auf die verschiedenen Elemente
#Link:
#http://zignar.net/page/pygtk-mit-glade			 mit xml(aus glade) Programm Grafische Oberflaeche erstellen

from HirarchicalView import *
from TagView import *
from AddTag import *

import gobject
gobject.threads_init()

#Modul um diese Klasse als Seperaten-Prozess zu starten
import threading
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import sys


#class GUI(threading.Thread):
class GUI():
	def __init__(self,sys):
		#threading.Thread.__init__(self)
		gobject.threads_init()
		self.sys = sys
		self.mod = sys.c.startview
		self.hview = HirarchicalView(self.sys)
		self.tview = TagView(self.sys)
		self.actview = None

	#def run(self):
	def start(self):
		print('run: GUI')

		#Init-Window
		self.xml = gtk.glade.XML("gui.glade")
		self.window = self.xml.get_widget("winMain")
		self.window.set_title(self.sys.c.prgname + ' - Version '  + str(self.sys.c.version))
		#self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("destroy", self.stopploop)

		#Connect Toogle-Buttons
		self.btnHirarchical = self.xml.get_widget('btnHirarchical')
		self.btnHirarchical.connect('toggled', self.showHirarchical)
		self.btnTag = self.xml.get_widget('btnTag')
		self.btnTag.connect('toggled', self.showTag)

		#Connect TextInput Field
		self.txtEntry = self.xml.get_widget('txtEntry')
		#self.txtEntry.connect('key_release_event',self.searchKey)
		self.txtEntry.connect('changed',self.searchKey)
		self.com = gtk.EntryCompletion()
		#com.set_inline_selection(True)
		#com.connect('match-selected',self.searchCompletion)
		self.txtEntry.set_completion(self.com)
		self.listcompl = gtk.ListStore(gobject.TYPE_STRING)
		self.com.set_model(self.listcompl)
		self.com.set_text_column(0)
		self.com.set_popup_set_width(True)
		
		#self.txtEntry.connect('activate',self.searchKey)
		#self.txtEntry.connect('backspace',self.searchKey)

		#Add Menu-Item by 'Ansicht'
		ansichtmenu = gtk.Menu()
		ansicht = self.xml.get_widget('mnuAnsicht')
		ansicht.set_submenu(ansichtmenu)
		self.mnuHirarchical = gtk.RadioMenuItem(None,'Hirarchisch')
		self.mnuHirarchical.connect('toggled',self.showHirarchical)
		ansichtmenu.append(self.mnuHirarchical)
		self.mnuTag = gtk.RadioMenuItem(self.mnuHirarchical,'Tag')
		self.mnuTag.connect('toggled',self.showTag)
		ansichtmenu.append(self.mnuTag)

		#Modify other MenuItems
		self.mnuBeenden = self.xml.get_widget('mnuBeenden')
		self.mnuBeenden.connect('activate',self.stopploop)
		self.mnuNeu = self.xml.get_widget('mnuNeu')
		self.mnuNeu.hide()

		#Init Status Bar
		self.Status = self.xml.get_widget('stsStatusBar')
		self.Status.push(1,'init')
		
		#Init Navigation Buttons
		self.btnBack = self.xml.get_widget('btnBackward')
		self.btnBack.connect('button_press_event',self.historyBack)
		self.btnBack.set_sensitive(False)
		self.btnFor = self.xml.get_widget('btnForward')
		self.btnFor.connect('button_press_event',self.historyFor)
		self.btnFor.set_sensitive(False)
		self.btnUp = self.xml.get_widget('btnUp')
		self.btnUp.connect('button_press_event',self.getParentFolder)
		self.btnUp.set_sensitive(False)
		
		#Init-View
		self.hspView = self.xml.get_widget('hspView')
		self.addTagContent = AddTag(self.sys)
		self.hspView.add(self.addTagContent.getWidget())
		self.view = self.xml.get_widget('View')
		if self.mod == 'hirarchical':
			self.actview = self.hview
			self.txtEntry.set_text(self.actview.get_actTxtInput())
			self.showHirarchical('init')
		elif self.mod == 'tag':
			self.actview = self.tview
			self.txtEntry.set_text(self.actview.get_actTxtInput())
			self.showTag('init')
		else:
			self.actview = self.hview
			self.txtEntry.set_text(self.actview.get_actTxtInput())
			self.showHirarchical('init')
		#self.actview.historyUpdate('user')
			
		#Zeigt alles an
		self.showall()

		#Loop damit das Fenster nicht wieder geschlossen wird
		self.startloop()

		



	#GUI Functionen
	def showHirarchical(self,event):
		#Toggle Function
		if isinstance(event,gtk.RadioMenuItem):
			if self.mnuHirarchical.get_active():
				self.btnHirarchical.set_active(True)
			else:
				self.btnHirarchical.set_active(False)
		else:
			if self.btnHirarchical.get_active():
				self.mnuHirarchical.set_active(True)
			else:
				#Wenn zweimal die gleiche Ansicht gewaehlt wird wird die andere Ansicht aktiviert
				if isinstance(self.actview,HirarchicalView) and event != 'init':
					self.showTag('init')
					return 0
				self.mnuHirarchical.set_active(False)
		if event == 'init':
			self.btnHirarchical.set_active(True)
			self.mnuHirarchical.set_active(True)

		#Init-View	
		self.changeView(self.hview)

	def showTag(self,event):
		#Toggle Function
		if isinstance(event,gtk.RadioMenuItem):
			if self.mnuTag.get_active():
				self.btnTag.set_active(True)
			else:
				self.btnTag.set_active(False)
		else:
			if self.btnTag.get_active():
				self.mnuTag.set_active(True)
			else:
				#Wenn zweimal die gleiche Ansicht gewaehlt wird wird die andere Ansicht aktiviert
				if isinstance(self.actview,TagView) and event != 'init':
					self.showHirarchical('init')
					return 0
				self.mnuTag.set_active(False)
		if event == 'init':
			self.btnTag.set_active(True)
			self.mnuTag.set_active(True)

		#Init-View
		self.changeView(self.tview)
	
	def changeView(self,newview):
		#Speichert Text Input String in der zuschliessenden View
		self.actview.set_actTxtInput(self.txtEntry.get_text())
		self.addTagContent.clearAll()

		#Schliesst die alte View
		#self.view.remove(self.actview)
		if self.actview.get_parent() != None:
			self.view.remove(self.actview)

		#Fuegt die neue View an
		#self.view.add(newview)
		self.view.add(newview)

		#Aender Aktuel View		
		self.mod = newview.mod
		self.actview = newview

		#Text Input aktualisieren
		#self.listcompl.clear()
		self.txtEntry.set_text(self.actview.get_actTxtInput())

		#Fokus auf Text Input
		self.set_focus(self.txtEntry)

		#Update Statusbar
		self.Status.pop(1)
		self.Status.push(1,'Ansicht: '+str(self.mod))
		self.showall()

		#Update-View
		self.actview.update()

	#def searchKey(self,widget,event):
	def searchKey(self,a):
		#if event.keyval != gtk.gdk.keyval_from_name("Down") and event.keyval != gtk.gdk.keyval_from_name("Up"):
		if self.actview.triggeredByNavigation:
			self.updateView()
		else:
			self.updateView('user')
	
	def searchCompletion(self,completion, prefix, user_param1):
		self.updateView()

	def updateView(self,actor='fn'):
		self.actview.set_actTxtInput(self.txtEntry.get_text())
		self.actview.update(actor)
	
	def openDirInHirarchical(self,path):
		self.showHirarchical('init')
		self.actview.set_actTxtInput(path)
		self.listcompl.clear()
		self.txtEntry.set_text(self.actview.get_actTxtInput())
		
	def historyBack(self,widget,event):
		self.actview.triggeredByNavigation = True
		self.actview.historyCursor = self.actview.historyCursor-1
		self.actview.set_actTxtInput(self.actview.history[self.actview.historyCursor])
		self.txtEntry.set_text(self.actview.get_actTxtInput())
		self.actview.triggeredByNavigation = False
		
	def historyFor(self,widget,event):
		self.actview.triggeredByNavigation = True
		self.actview.historyCursor = self.actview.historyCursor+1
		self.actview.set_actTxtInput(self.actview.history[self.actview.historyCursor])
		self.txtEntry.set_text(self.actview.get_actTxtInput())
		self.actview.triggeredByNavigation = False
		
	def getParentFolder(self,widget,event):
		parent=self.sys.filemanager.getParentDir(self.actview.get_actTxtInput())
		self.txtEntry.set_text(parent)
	###





	def set_focus(self,widget):
		self.window.set_focus(widget)

	def showall(self):
		self.window.show_all()

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
