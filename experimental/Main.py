#!/usr/bin/python

#File:			Main.py
#Description:		Diese Datei ist die Start Datei fuer unser Projekt. Hier werden alle wichtigen Referenzen auf unsere Klassen erstellt.
#Author:		Kaleb Tschabold
#Creation Date:		29.3.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		29.3.2011	Grundfunktionalitaeten werden erstellt
#			0.1		18.3.2011	Wichtigste Prozesse starten
#			0.1		19.3.2011	GUI starten in eine seperate Function gepackt, damit das CLI auch das GUI starten kann.
#Link:
#PyInstaller:
#	http://www.marcogabriel.com/blog/archives/343-Python-Scripte-mit-PyInstaller-als-.exe-verteilen.html


#Unserer Klassen
from CLI import *
from DB import *
from FileManager import *
from TagManager import *
from FileSystemListener import *
from GUI import *
from Utility import *
from File import *
from Constant import *

#Andere Klassen
import sys
import os.path

class Main():
  	db	= None
	dbPath	= None
	gui	= None
	def __init__(self):
		pass

	def start(self,modus):
		self.mod = modus
		self.filemanager = FileManager(self)
		self.tagmanager = TagManager(self)
		self.u = Utility()
		self.c = Constant(self)
		print "path = "+ self.c.dbPath
		if not os.path.exists(self.c.dbPath):
			print "creating path"
			os.makedirs(self.c.dbPath)
		self.db	= DB(self.c.dbPath+"db")

		#Array mit allen Thread. Wird gebraucht, dass diese beim beenden des Programmes alle richtig beendet werden
		self.t = []

		#FileSystemListener in einem eigenen Thread
		self.fslistener = FileSystemListener(self)
		self.fslistener.daemon = True
		self.t.append(self.fslistener)
		self.fslistener.add_watch(os.path.abspath(self.c.home), True)
		self.fslistener.start()

		if modus == 'cli':
			#CLI in einem eigenen Thread
			self.cli = CLI(self)
			#dieser Thread ist dem Main unterordnet. So kann man mit einem KeyInterrupt den Thread beenden
			#self.cli.daemon = True
			self.t.append(self.cli)
			self.cli.start()
		else:
			self.start_gui()

	def start_gui(self):
		#GUI in einem eigenen Thread
		self.gui = GUI(self)
		#self.gui.daemon = True
		#self.t.append(self.gui)
		self.gui.start()

	def stoppall(self):
		#Threads beenden
		#self.fslistener.stop()
		for t in self.t:
			print('close: '+str(t))
			try:
				t.stop()
			except RuntimeError:
				pass

	def getDb(self):
		return self.db

	#Wird gebraucht, dass diese Klasse wie ein Objekt aufgerufen werden kann
	def __call__(self,a,b,c):
		pass

#PROGRAMM START
if __name__ == "__main__":
	main = Main()
	try:
		try:
			cmd = len(sys.argv[1])
			if cmd > 0:
				main.start('cli')
			else:
				main.start('gui')
		except:
				main.start('gui')
	except (KeyboardInterrupt,SystemExit):
		print('Programm geschlossen')
		main.stoppall()
