#!/usr/bin/python

#File:			Main.py
#Description:		Diese Datei ist die Start Datei fuer unser Projekt. Hier werden alle wichtigen Referenzen auf unsere Klassen erstellt.
#Author:		Kaleb Tschabold
#Creation Date:		29.3.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		29.3.2011	Grundfunktionalitaeten werden erstellt
#			0.1		18.3.2011	Wichtigste Prozesse starten

#Unserer Klassen
from CLI import *
from DB import *
from FileManager import *
from TagManager import *
from FileSystemListener import *
from GUI import *
from Utility import *
from File import *
from Constante import *

#Andere Klassen
import sys

class Main():
	def __init__(self):
		pass

	def start(self,modus):
		#NO() => Neues Objekt(Klasse)
		self.mod = modus
		self.db = DB()
		self.filemanager = FileManager()
		self.tagmanager = TagManager()
		self.u = Utility()
		self.c = Constante()

		#Array mit allen Thread. Wird gebraucht, dass diese beim beenden des Programmes alle richtig beendet werden
		self.t = []

		if modus == 'cli':
			#CLI in einem eigenen Thread
			self.cli = CLI(self)
			self.cli.daemon = True
			self.t.append(self.cli)
			self.cli.start()
		else:
			#GUI in einem eigenen Thread
			self.gui = GUI(self)
			self.gui.daemon = True
			self.t.append(self.gui)
			self.gui.start()

		#FileSystemListener in einem eigenen Thread
		self.fslistener = FileSystemListener()
		self.t.append(self.fslistener)
		self.fslistener.start()

	def stoppall(self):
		#GUI beenden
		#self.gui.stopploop()
		#Thread beenden
		print('stoppall')
		for t in self.t:
			print('close: '+str(t))
			try:
				t.join()
			except:
				pass
		sys.exit()
		

if __name__ == "__main__":
	main = Main()
	try:
		try:
			cmd = sys.argv[1].lower()
			if cmd == 'cli':
				main.start('cli')
			elif cmd == 'gui':
				main.start('gui')
			else:
				main.start('gui')
		except:
				main.start('gui')
	except (KeyboardInterrupt,SystemExit):
		print('Programm geschlossen')
		main.stoppall()
