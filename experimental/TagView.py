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
		files = self.sys.filemanager.getFilesFromDir(self.acttxtinput) 
		if files != 'error':
			self.model.clear()
			for i in range(len(files)):
				self.model.append(None,[files[i].getFileName()])
			self.set_model(self.model)
			self.show_all()
