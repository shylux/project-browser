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

class View(gtk.TreeView):
	def __init__(self,sys):
		gtk.TreeView.__init__(self,None)
		self.sys = sys
		self.acttxtinput = ''

		self.createTree()
		pass

	def createTree(self):
		#Objekt fuer den Baum
		self.model = gtk.TreeStore(gtk.gdk.Pixbuf, gobject.TYPE_STRING)
		
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

		#Allgemeine Definitionen fuer den Baum
		self.set_search_column(1)
		self.cl1.set_sort_column_id(1)

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

#Registriert diese Klasse als pygtk-widget
gobject.type_register(View)
