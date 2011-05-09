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
		
		self.history.append('/')
		self.historyCursor = 0
		self.sys = sys
		self.set_actTxtInput(sys.c.initStrHirarchical)
		self.connect('row-activated',self.rowActivate)

	def update(self, actor = 'fn'):
		if self.sys.gui != None:
			if self.get_actTxtInput() == '':
				self.sys.gui.txtEntry.set_text('/')
				return 0
			self.items = self.sys.filemanager.getFilesFromDir(self.acttxtinput) 
			if self.items != 'error':
				#Ordner konnte geoffnet werden
				self.model.clear()
				for i in range(len(self.items)):
					if self.items[i].getIsDir():
						self.model.append(None,[self.getFolderIcon(),self.items[i].getFileName(),self.items[i],', '.join(self.items[i].getTags())])
					else:
						self.model.append(None,[self.getFileIcon(),self.items[i].getFileName(),self.items[i],', '.join(self.items[i].getTags())])
				self.set_model(self.model)
				#Ruft History Verwaltung auf
				if len(self.get_actTxtInput()) > 0:
					if self.get_actTxtInput()[-1] == '/':
						self.historyUpdate(actor)
			self.updateParentFolderBtn()
			self.updateBackupBtn()
			self.historySymboleManagement()
			#Ruft Auto-Completion Update Funktion auf
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

	def updateParentFolderBtn(self):
		parent = self.sys.filemanager.getParentDir(self.get_actTxtInput())
		if parent:
			self.sys.gui.btnUp.set_sensitive(True)
		else:
			self.sys.gui.btnUp.set_sensitive(False)

	def rowActivate(self,treeview, path, user_data):
		f = self.getFObjFromSelectedRow()
		print('fullpath activated in rowActivated: '+f.getFullPath())
		if not f.getIsDir():
			self.sys.filemanager.openFile(f.getFullPath())
		else:
			self.sys.filemanager.openDir(f.getFullPath())




		
