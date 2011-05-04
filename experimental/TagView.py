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
		self.connect('row-activated',self.rowActivate)

	def update(self, actor = 'fn'):
		print('TAG UPDATE')
		if self.sys.gui != None:
			print('TAG UPDATE IN IF')
			oldmodel = self.get_model()
			self.model.clear()
			#Dieser Durchgang ist, wenn noch nicht's im TextFeld steht
			if self.get_actTxtInput() == '':
				t = self.sys.db.getAllTags()
				for i in range(len(t)):
					self.model.append(None,[self.getFolderIcon(),'*',[t[i]],t[i]])
				self.set_model(self.model)
				print('vor aufruf1')
				self.historyUpdate(actor)
				self.historySymboleManagement()
				self.updateParentFolderBtn()
				self.completion()
				#Damit diese Funktion abgebrochen wird
				return 0
			#Dieser Durchgang ist, wenn Zeichen im Text Feld stehen
			itemarray = self.get_actTxtInput().split(',')
			for j in range(len(itemarray)):
				oneitem = itemarray[j].strip()
				self.items = self.sys.db.getFilesFromTag(oneitem)
				for i in range(len(self.items)):
					self.items[i].setIsDir(self.sys.u.strBooleanToBoolean(self.items[i].getIsDir()))
					if self.items[i].getIsDir():
						self.model.append(None,[self.getFolderIcon(),self.items[i].getFileName(),self.items[i],', '.join(self.items[i].getTags())])
					else:
						self.model.append(None,[self.getFileIcon(),self.items[i].getFileName(),self.items[i],', '.join(self.items[i].getTags())])
			self.set_model(self.model)
			print('vor aufruf2')
			if len(self.items)>0:
				self.historyUpdate(actor)
			self.historySymboleManagement()
			self.updateParentFolderBtn()
			self.completion()

	def completion(self):
			print('search matched: '+self.get_actTxtInput())
			matched = self.sys.tagmanager.searchMatchTags(self.get_actTxtInput())
			print('matched :'+str(matched))
		#try:
			if self.sys.gui.listcompl != None:
				#try:
					self.sys.gui.listcompl.clear()
				#except:
				#	pass
			for i in range(len(matched)):
				print('for '+str(i)+'matched word: '+str(matched[i]))
				self.sys.gui.listcompl.append([matched[i]])
		#except:
		#	pass


	def updateParentFolderBtn(self):
		self.sys.gui.btnUp.set_sensitive(False)

	def rowActivate(self,treeview, path, user_data):
		f = self.getFObjFromSelectedRow()
		if isinstance(f,list):
			print('f: '+str(f[0]))
			self.sys.gui.txtEntry.set_text(f[0])
			self.sys.gui.updateView()
		else:
			if not f.getIsDir():
				self.sys.filemanager.openFile(f.getFullPath())
			else:
				self.sys.gui.openDirInHirarchical(f.getFullPath())



