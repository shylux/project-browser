#!/usr/bin/python

#File:			HirarchicalView.py
#Description:		Klasse um die Orderstrucktur anzuzeigen
#Author:		Kaleb Tschabold
#Creation Date:		29.3.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		29.3.2011	Grundfunktionalitaeten werden erstellt
#			0.1		18.3.2011	Erben von View und init Funktion aufrufen

from View import *
import gtk
import os

class HirarchicalView(View):
	mod = 'hirarchical'
	def __init__(self,sys):
		View.__init__(self,sys)
		self.model = gtk.TreeStore(str)
		self.cl1 = gtk.TreeViewColumn('Datei')
		self.append_column(self.cl1)
		self.cell1 = gtk.CellRendererText()
		self.cl1.pack_start(self.cell1,True)
		self.cl1.add_attribute(self.cell1,'text',0)
		self.set_search_column(0)
		self.cl1.set_sort_column_id(0)
		#self.set_reorderable(True)

	def update(self):
		files = self.sys.filemanager.getFilesFromDir(self.acttxtinput) 
		if files != 'error':
			self.model = gtk.TreeStore(str)
			for i in range(len(files)):
				self.model.append(None,[files[i].getFileName()])
			self.set_model(self.model)
			self.show_all()
		#print('Suche ordner/datei: '+self.get_actTxtInput())
	

