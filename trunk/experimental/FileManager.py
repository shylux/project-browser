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
		try:
			l = os.listdir(path)
			fl = self.createFileList(l)
			return fl
		except:
			return 'error'
	
	def createFileList(self,array):
		a = []
		for i in range(len(array)):
			print(array[i])
			a.append(File(self.getFileName(array[i]),array[i]))
		return a
		

	def getFileName(self,path):
		return os.path.basename(path)
