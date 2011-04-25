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
		self.model = gtk.TreeStore(str)
		
		#1. Spalte
		self.cl1 = gtk.TreeViewColumn('Datei')
		self.append_column(self.cl1)

		#Definition der 1. Spalte
		self.cell1 = gtk.CellRendererText()
		self.cl1.pack_start(self.cell1,True)
		self.cl1.add_attribute(self.cell1,'text',0)

		#Allgemeine Definitionen fuer den Baum
		self.set_search_column(0)
		self.cl1.set_sort_column_id(0)

		self.update()

	def update(self):
		self.show_all()

	def set_actTxtInput(self,text):
		self.acttxtinput = text

	def get_actTxtInput(self):
		print('gettext: '+self.acttxtinput)
		return self.acttxtinput

#Registriert diese Klasse als pygtk-widget
gobject.type_register(View)
