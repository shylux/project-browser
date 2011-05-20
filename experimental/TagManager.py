#!/usr/bin/python

#File:			TagManager.py
#Description:		Tag Magement
#Author:		Kaleb Tschabold
#Creation Date:		29.3.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		29.3.2011	Grundfunktionalitaeten werden erstellt

class TagManager():
	def __init__(self,sys):
		self.sys = sys
		
	def searchMatchTags(self,name):
		all = self.sys.db.getAllTags()
		matched = []
		a = name.split(',')
		a[len(a)-1].strip()
		for i in range(len(all)):
			if all[i].find(name) == 0:
					matched.append(all[i])
		return matched


	def getBackups(self,tag):
		files = self.sys.db.getFilesFromTag(tag)
		backupArray = []
		for i in range(len(files)):
			backupArray.extend(files[i].getBackups())
		print('founded backups: '+str(backupArray))
		backupArray = self.sys.u.uniqueFiles(backupArray)
		print('founded backups: '+str(backupArray))
		return backupArray

	def makeBackup(self,tag):
		files = self.sys.db.getFilesFromTag(tag)
		for i in range(len(files)):
			files[i].makeBackup()

	def restoreFrom(self,tag,backup):
		files = self.sys.db.getFilesFromTag(tag)
		for f in files:
			fb = f.getBackups()
			for eachBackup in fb:
				if eachBackup.getFileName() == backup.getFileName():
					f.restoreFrom(eachBackup)
