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
import pygtk
pygtk.require('2.0')
import gtk

class HirarchicalView(View):
	mod = 'hirarchical'
	def __init__(self,sys):
		View.__init__(self,sys)

		self.set_actTxtInput(sys.c.initStrHirarchical)
		self.connect('row-activated',self.rowActivate)

	def update(self):
		self.items = self.sys.filemanager.getFilesFromDir(self.acttxtinput) 
		if self.items != 'error':
			self.model.clear()
			for i in range(len(self.items)):
				if self.items[i].getIsDir():
					self.model.append(None,[self.getFolderIcon(),self.items[i].getFileName(),self.items[i]])
				else:
					self.model.append(None,[self.getFileIcon(),self.items[i].getFileName(),self.items[i]])
			self.set_model(self.model)
		self.completion()

	
	def completion(self):
		matched = self.sys.filemanager.searchMatchDir(self.get_actTxtInput())
		try:
			if self.sys.gui.listcompl != None:
				try:
					self.sys.gui.listcompl.clear()
				except:
					pass
			for i in range(len(matched)):
				self.sys.gui.listcompl.append([matched[i]])
		except:
			pass


	def rowActivate(self,treeview, path, user_data):
		f = self.getFObjFromSelectedRow()
		if not f.getIsDir():
			self.sys.filemanager.openFile(f.getPath())
		else:
			self.sys.filemanager.openDir(f.getPath())
