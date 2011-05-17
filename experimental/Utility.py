#!/usr/bin/python

#File:			Utility.py
#Description:		Hier sind alle kleinen Hilfsfunktionen die wir selber programmieren drin
#Author:		Kaleb Tschabold
#Creation Date:		14.4.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		14.4.2011	Grundfunktionalitaeten werden erstellt
#			0.2		18.4.2011	Funktion um ein neues Objekt zu erstellen

import sys
from time import strftime

class Utility:

	def __init__(self):
		self.NO = NO
		pass

	def checkOS(self):
		platform = sys.platform
		if platform.startswith("linux"):
			return "linux"
		elif platform.startswith("win"):
			return "windows"
		elif platform.startswith("darwin"):
			return "mac"

	
	def strBooleanToBoolean(self,s):
		if s == 'False':
			return False
		if s == 'True':
			return True
	def getTime(self):
		return strftime("%Y-%m-%d_%H:%M")

#Dynamisches Objekt, dass fuer normale Objekte gebraucht werden kann
class NO():
	pass
