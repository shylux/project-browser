#!/usr/bin/python

#File:			TagView.py
#Description:		Klasse um die Datein zu einem Tag anzuzeigen
#Author:		Kaleb Tschabold
#Creation Date:		29.3.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		29.3.2011	Grundfunktionalitaeten werden erstellt

from View import *
import gtk

class TagView(View):
	mod = 'tag'
	def __init__(self,sys):
		View.__init__(self,sys)
		self.set_actTxtInput(sys.c.initStrTag)

	def update(self):
		self.items = self.sys.db.getFilesFromTag(self.get_actTxtInput())
		self.model.clear()
		for i in range(len(self.items)):
			if self.items[i].getIsDir():
				self.model.append(None,[self.getFolderIcon(),self.items[i].getFileName(),self.items[i]])
			else:
				self.model.append(None,[self.getFileIcon(),self.items[i].getFileName(),self.items[i]])
		self.set_model(self.model)
