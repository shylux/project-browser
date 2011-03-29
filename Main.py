#!/usr/bin/python

#File:			Main.py
#Description:		Diese Datei ist die Start Datei für unser Projekt. Hier werden alle wichtigen Referenzen auf unsere Klassen erstellt.
#Author:		Kaleb Tschabold
#Creation Date:		29.3.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		29.3.2011	Grundfunktionalitaeten werden erstellt

from CLI import *
from DB import *
from File import *
from FileManger import *
from FileSystemManger import *
from GUI import *
from TagManger import *
from Utility import *


class Main():
	def __init__(self):
		pass

if __name__ == "__main__":
	try:
		main = Main()
	except KeyboardInterrupt:
		print('Programm geschlossen')
