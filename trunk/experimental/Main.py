#!/usr/bin/python

#File:			Main.py
#Description:		Diese Datei ist die Start Datei fuer unser Projekt. Hier werden alle wichtigen Referenzen auf unsere Klassen erstellt.
#Author:		Kaleb Tschabold
#Creation Date:		29.3.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		29.3.2011	Grundfunktionalitaeten werden erstellt
#			0.1		18.3.2011	Wichtigste Prozesse starten

from CLI import *
from DB import *
from FileManager import *
from TagManager import *
from FileSystemListener import *
from GUI import *
from Utility import *
from File import *
from Constante import *

class Main():
	def __init__(self):
		pass

	def start(self):
		#NO() => Neues Objekt(Klasse)
		self.sys = NO()
		globals()['sys'] = self.sys
		self.sys.db = DB()
		self.sys.filemanager = FileManager()
		self.sys.tagmanager = TagManager()
		self.sys.u = Utility()
		self.sys.c = Constante()

		#Array mit allen Thread. Wird gebraucht, dass diese beim beenden des Programmes alle richtig beendet werden
		self.sys.t = []

		#CLI in einem eigenen Thread
		self.sys.cli = CLI(self.sys)
		self.sys.t.append(self.sys.cli)
		#self.sys.cli.start()

		#GUI in einem eigenen Thread
		self.sys.gui = GUI(self.sys)
		self.sys.t.append(self.sys.gui)
		self.sys.gui.start()

		#FileSystemListener in einem eigenen Thread
		self.sys.fslistener = FileSystemListener()
		self.sys.t.append(self.sys.fslistener)
		self.sys.fslistener.start()

if __name__ == "__main__":
	try:
		main = Main()
		main.start()
	except KeyboardInterrupt:
		for t in s.sys.t:
			t.join()
		print('Programm geschlossen')
