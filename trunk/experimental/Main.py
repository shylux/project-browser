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
from Constante import *

#Andere Klassen
import sys

class Main():
	def __init__(self):
		pass

	def start(self,modus):
		#NO() => Neues Objekt(Klasse)
		self.mod = modus
		#self.db = DB()
		self.filemanager = FileManager()
		self.tagmanager = TagManager()
		self.u = Utility()
		self.c = Constante()

		#Array mit allen Thread. Wird gebraucht, dass diese beim beenden des Programmes alle richtig beendet werden
		self.t = []

		#FileSystemListener in einem eigenen Thread
		self.fslistener = FileSystemListener(self)
		#self.fslistener.daemon = True
		self.t.append(self.fslistener)
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
		self.t.append(self.gui)
		self.gui.start()
		

	def stoppall(self):
		#Threads beenden
		print('stoppall')
		for t in self.t:
			print('close: '+str(t))
			try:
				t.join()
			except RuntimeError:
				pass

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