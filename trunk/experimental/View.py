#!/usr/bin/python

#File:			View.py
#Description:		Diese Klasse kann die 2 Ansichten(Tag und Hirarchisch) verwalten
#Author:		Kaleb Tschabold
#Creation Date:		14.4.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		14.4.2011	Grundfunktionalitaeten werden erstellt
#			0.2		18.4.2011	Erbt von gtk.Layout
#
#Link:
#http://www.pygtk.org/pygtk2tutorial/sec-TreeViewDragAndDrop.html 	Bearbeitet selected

#Eigene Klassen
from AddTag import *

#Andere Klassen
import pygtk
pygtk.require('2.0')
import gtk
import gobject
import os

class View(gtk.TreeView):
	def __init__(self,sys):
		gtk.TreeView.__init__(self,None)
		self.sys = sys
		self.acttxtinput = ''
		
		self.history = []
		self.historyCursor = -1

		self.triggeredByNavigation = False
		
		self.createTree()
		self.connect('button_release_event',self.showContext)
		self.connect('cursor-changed',self.updateTagProperties)
		
	def createTree(self):
		#Objekt fuer den Baum
		self.model = gtk.TreeStore(gtk.gdk.Pixbuf, gobject.TYPE_STRING, gobject.TYPE_PYOBJECT, gobject.TYPE_STRING)
		
		#1. Spalte
		self.cl1 = gtk.TreeViewColumn('Datei')
		self.append_column(self.cl1)

		#Definition des Icons der 1. Spalte
		render1 = gtk.CellRendererPixbuf()
       		self.cl1.pack_start(render1, expand=False)
        	self.cl1.add_attribute(render1, 'pixbuf', 0)

		#Definition der Text der 1. Spalte
		render2 = gtk.CellRendererText()
		self.cl1.pack_start(render2,True)
		self.cl1.add_attribute(render2,'text',1)
		
		#2. Spalte
		self.cl2 = gtk.TreeViewColumn("Tag's")
		self.append_column(self.cl2)
		
		#Definition des Textes fuer die 2. Spalte
		render3 = gtk.CellRendererText()
		self.cl2.pack_start(render3,True)
		self.cl2.add_attribute(render3,'text',3)

		#Allgemeine Definitionen fuer den Baum
		self.set_search_column(1)
		self.cl1.set_sort_column_id(0)
		self.cl2.set_sort_column_id(1)

		self.update()

	def get_icon_pixbuf(self, stock):
		return self.render_icon(stock_id=getattr(gtk, stock),
			                size=gtk.ICON_SIZE_MENU,
			                detail=None)
	def getFolderIcon(self):
		return self.get_icon_pixbuf('STOCK_DIRECTORY')

	def getFileIcon(self):
		return self.get_icon_pixbuf('STOCK_FILE')

	def update(self):
		self.show_all()

	def set_actTxtInput(self,text):
		self.acttxtinput = text

	def get_actTxtInput(self):
		return self.acttxtinput

	def getFObjFromSelectedRow(self):
		treeview = self
		selection = treeview.get_selection()
		selection.set_mode(gtk.SELECTION_SINGLE)
		tree_model, tree_iter = selection.get_selected()
		return tree_model.get_value(tree_iter,2)

	def showContext(self, treeview, event):
		if event.button == 3:
			f = self.getFObjFromSelectedRow()
			m = gtk.Menu()
			#m1 = gtk.MenuItem ('Add Tag')
			#m.append(m1)
			m2 = gtk.MenuItem('Properties')
			m.append(m2)
			#m1.connect('button_press_event',self.context_AddTag,f)
			m2.connect('button_press_event',self.context_Properties,f)
			m.show_all()
			m.popup( None, None, None, event.button, event.time)
			return True
		return False

	def context_Properties(self,widget,event,fobj):
		print('properties')

	def updateTagProperties(self,event):
		try:
			self.sys.gui.addTagContent.update(self.getFObjFromSelectedRow())
		except:
			pass
	
	def historyUpdate(self,actor='fn'):
		#Wenn wieder vorwaertz gesprungen wird, werden alle Element nach der aktuelen Position geloescht
		if self.historyCursor > -1:
			if actor == 'user' and self.history[self.historyCursor] != self.get_actTxtInput():
				if self.historyCursor < len(self.history)-1:
					rem = (len(self.history)-1) - self.historyCursor
					l = len(self.history)
					i = 1
					#rem+1 weil die len von history eins mehr ist als der cursor
					while i<rem+1:
						self.history.remove(self.history[l-i])
						i = i + 1
					self.historyCursor = self.historyCursor
				self.historyCursor = self.historyCursor + 1
				self.history.append(self.get_actTxtInput())
				self.historySymboleManagement()
		elif len(self.history) == 0:
			self.historyCursor = self.historyCursor + 1
			self.history.append(self.get_actTxtInput())
			self.historySymboleManagement()
		
	def historySymboleManagement(self):
			h = len(self.history)-1
			c = self.historyCursor
			if h >= c and h != 0 and c > 0:
				self.sys.gui.btnBack.set_sensitive(True)
			if h >= c and h != 0:
				self.sys.gui.btnFor.set_sensitive(True)
			if c <= 0 or h == 0:
				self.sys.gui.btnBack.set_sensitive(False)
			if c == h or h == 0:
				self.sys.gui.btnFor.set_sensitive(False)
	

#Registriert diese Klasse als pygtk-widget
gobject.type_register(View)
