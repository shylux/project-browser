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

class HirarchicalView(View):
	mod = 'hirarchical'
	def __init__(self,sys):
		View.__init__(self,sys)
		self.set_actTxtInput(sys.c.initStrHirarchical)

	def update(self):
		files = self.sys.filemanager.getFilesFromDir(self.acttxtinput) 
		if files != 'error':
			self.model.clear()
			for i in range(len(files)):
				if files[i].isDir:
					self.model.append(None,[self.getFolderIcon(),files[i].getFileName()])
				else:
					self.model.append(None,[self.getFileIcon(),files[i].getFileName()])
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
