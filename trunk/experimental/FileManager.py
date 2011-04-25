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
		#try:
			fl = self.createFileList(path)
			return fl
		#except:
		#	return 'error'
	
	def createFileList(self,path):
		a = []
		if not os.path.exists(path):
			print('path existier nicht' + path)
			path = path.split('/')
			print('len '+str(len(path)))
			path.remove(path[len(path)-1])
			path = '/'.join(path)+'/'
			if path == '':
				path = '/'
			print('new path: '+path)
		else:
			if path[-1:] != '/':
				path = path + '/'
		array =  os.listdir(path)
		for i in range(len(array)):
			fullpath = path +array[i]
			print(fullpath)
			a.append(File(self.getFileName(array[i]),fullpath))
			a[i].setDir(self.isDir(fullpath))
		return a
		

	def getFileName(self,path):
		return os.path.basename(path)

	def isDir(self,path):
		return os.path.isdir(path)

	def searchMatchDir(self,path):
		match = []
		ddf = self.divideDirAndFile(path)
		l = os.listdir(ddf[0])
		for i in range(len(l)):
			if (l[i].find(ddf[1]) >= 0 and os.path.isdir(ddf[0] + '/' + l[i])) or (ddf[1] == '' and os.path.isdir(ddf[0] + '/' + l[i])):
				if ddf[0] == '/':
					match.append(ddf[0] + l[i] + '/')
				else:
					match.append(ddf[0] + '/' + l[i] + '/')
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
		elif self.sys.c.os == 'win':
			os.filestart(path)
		else:
			#Da muss noch eine Loesung sein, wenn die Datei nicht gestartet werden kann
			pass
		
