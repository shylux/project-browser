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
		print('get text: '+self.get_actTxtInput())

	def update(self):
		print('ubdate')
		files = self.sys.filemanager.getFilesFromDir(self.acttxtinput) 
		if files != 'error':
			self.model.clear()
			for i in range(len(files)):
				self.model.append(None,[files[i].getFileName()])
			self.set_model(self.model)
		self.completion()

	
	def completion(self):
		matched = self.sys.filemanager.searchMatchDir(self.get_actTxtInput())
		print('self.sys: '+str(self.sys.filemanager))
		print('mached' + str(matched) + 'act: '+self.get_actTxtInput())
		try:
			if self.sys.gui.listcompl != None:
				try:
					self.sys.gui.listcompl.clear()
				except:
					pass
			for i in range(len(matched)):
				self.sys.gui.listcompl.append([matched[i]])
		except:
			print('error: '+str('a'))
		#	pass
