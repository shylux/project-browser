#!/usr/bin/python

#File:			CLI.py
#Description:		Mit dieser Klasse kann man ueber die Kommandozeille mit dem Programm interagieren
#Author:		Kaleb Tschabold
#Creation Date:		29.3.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		29.3.2011	Grundfunktionalitaeten werden erstellt
#			0.2		18.4.2011	Thread und Endlos Loop


#Modul um diese Klasse als Seperaten-Prozess zu starten
import threading
import time
import sys

class CLI(threading.Thread):
	def __init__(self,sys):
		threading.Thread.__init__(self)
		self.sys = sys
	
	def run(self):
			print('---')
			print('0 => Ende')
			print('---')
			cli = True
			while cli:
			        time.sleep(self.sys.c.sleep)
				#cmd = raw_input('Befehl: ')
				cmd = sys.stdin.readline()
				if cmd == '0\n':
					#CLI wird beendet
					cli = False
					#sys.exit()
				else:
					print('echo: '+cmd)
