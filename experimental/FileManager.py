#!/usr/bin/python

#File:			FileManager.py
#Description:		Ist fuer den Dateizugriff zustaendig
#Author:		Kaleb Tschabold
#Creation Date:		14.4.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		14.4.2011	Grundfunktionalitaeten werden erstellt
#			0.1		23.4.2011	Erste Funktionen um Dateilisten zu laden

#Unsere Klassen
from File import *

#andere Klassen
import os

class FileManager:
	def __init__(self,sys):
		self.sys = sys
		pass
	
	def getFilesFromDir(self,path):
		a = []
		if not os.path.exists(path):
			matched = self.searchMatchDir(path)
			if len(matched) >= 1:
				array = matched
			else:
				return a
			for i in range(len(array)):
				a.append(File(fullPath=array[i],isDir=self.isDir(array[i])))
				a[i].setTags(self.sys.db.getTagsToFile(a[i]))
		else:
			if path == '':
				path = path + '/'
			if path[-1:] != '/':
				path = path + '/'
			array =  os.listdir(path)
			for i in range(len(array)):
				fullpath = path + array[i]
				if self.isDir(fullpath):
					fullpath = fullpath + '/'
				a.append(File(fullPath=fullpath,isDir=self.isDir(fullpath)))
				a[i].setTags(self.sys.db.getTagsToFile(a[i]))
		return a

	def getFileName(self,path):
		return os.path.basename(path)

	def getDirName(self,path):
		s = path.split('/')
		return s[len(s)-2]

	def getParentDir(self,path):
		s = path.split('/')
		l = len(s)
		print('l'+str(l))
		if l >= 3:
			s.remove(s[l-2])
			return '/'.join(s)
		else:
			return False

	def isDir(self,path):
		return os.path.isdir(path)

	def searchMatchDir(self,path):
		match = []
		try:
			ddf = self.divideDirAndFile(path)
			l = os.listdir(ddf[0])
			for i in range(len(l)):
				if (l[i].find(ddf[1]) >= 0 and os.path.isdir(ddf[0] + '/' + l[i])) or (ddf[1] == '' and os.path.isdir(ddf[0] + '/' + l[i])):
					if ddf[0] == '/':
						match.append(ddf[0] + l[i] + '/')
					else:
						match.append(ddf[0] + '/' + l[i] + '/')
		except:
			pass
		return match

	def divideDirAndFile(self,dirandfile):
		dir = ''
		file = ''
		if dirandfile.find('/') >= 0:
			dir = dirandfile[0:dirandfile.rfind('/')]
			if dir.strip() == '':
				dir = '/'
			file = dirandfile[dirandfile.rfind('/')+1:(len(dirandfile))]
		else:
			dir = '/'
			file = dirandfile[1:]
		divided = []
		divided.append(dir)
		divided.append(file)
		return divided


	def openFile(self,path):
		if self.sys.c.os == 'linux':
			#Funktioniert nur bei Ubuntu
			os.system('/usr/bin/xdg-open '+path.replace(chr(32),'\ '))
		elif self.sys.c.os == 'windows':
			os.system(path)
		elif self.sys.c.os == 'mac':
			os.system('open '+path.replace(chr(32),'\ '))
		else:
			#Da muss noch eine Loesung sein, wenn die Datei nicht gestartet werden kann
			pass

	def openDir(self,path):
		self.sys.gui.txtEntry.set_text(path)
		self.sys.gui.updateView()
		
