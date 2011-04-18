#!/usr/bin/python

#File:			Utility.py
#Description:		Hier sind alle kleinen Hilfsfunktionen die wir selber programmieren drin
#Author:		Kaleb Tschabold
#Creation Date:		14.4.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		14.4.2011	Grundfunktionalitaeten werden erstellt
import sys

class Utility:
	def __init__(self):
		pass
	def checkOS(self):
		platform = sys.platform
		if platform.startswith("linux"):
			 return "linux"
