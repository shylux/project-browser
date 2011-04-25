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
			print('if')
			matched = self.searchMatchDir(path)
			print('matched: '+str(matched))
			if len(matched) >= 1:
				array = matched
			else:
				return a
			for i in range(len(array)):
				print('basename: '+self.getDirName(array[i]))
				a.append(File(self.getDirName(array[i]),array[i]))
				a[i].setDir(self.isDir(array[i]))
		else:
			print('else')
			if path == '':
				path = path + '/'
			if path[-1:] != '/':
				path = path + '/'
			array =  os.listdir(path)
			for i in range(len(array)):
				print('dirpath: '+path+', file: '+array[i])
				fullpath = path + array[i]
				print(fullpath)
				a.append(File(array[i],fullpath))
				a[i].setDir(self.isDir(fullpath))
		return a

	def getFileName(self,path):
		return os.path.basename(path)

	def getDirName(self,path):
		s = path.split('/')
		return s[len(s)-2]

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
			os.system('/usr/bin/xdg-open '+path)
		elif self.sys.c.os == 'windows':
			os.system(path)
		else:
			#Da muss noch eine Loesung sein, wenn die Datei nicht gestartet werden kann
			pass

	def openDir(self,path):
		self.sys.gui.txtEntry.set_text(path)
		self.sys.gui.updateView()
		
