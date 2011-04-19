#!/usr/bin/python

#File:			CLI.py
#Description:		Mit dieser Klasse kann man ueber die Kommandozeille mit dem Programm interagieren
#Author:		Kaleb Tschabold
#Creation Date:		29.3.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		29.3.2011	Grundfunktionalitaeten werden erstellt
#			0.1		18.4.2011	Thread und Endlos Loop
#			0.1		19.4.2011	Erste Option implementiert (modus,verbos)


#Modul um diese Klasse als Seperaten-Prozess zu starten
import threading
import time
import sys
import os
from optparse import *

class CLI(threading.Thread):
	def __init__(self,sys):
		threading.Thread.__init__(self)
		self.sys = sys
	
	def run(self):
			usage = "usage: %prog [options] arg"
			version = (self.sys.c.prgname)+" "+str(self.sys.c.version)
			option_list =	[
				    		make_option("-m", "--modus", dest="modus", help="Start a inline 'commandprompt'"),
						make_option("-v", "--verbose", dest="verbose", help="Zeigt alle Ausgaben", action="store_true"),
						make_option("-q", "--quite", dest="verbose", help="Zeigt keine Ausgaben", action="store_false", default=True),
			    		]
    			parser = OptionParser(usage,version=version,option_list=option_list)
			a = (options,args) = parser.parse_args()
			if options.verbose:
				self.verbose()
			if not options.verbose:
				self.no_verbose()
			if options.modus:
				if options.modus == 'gui':
					self.sys.start_gui()
				if options.modus == 'inline':
					self.inline()
	def verbose(self):
		sys.settrace(self.sys)

	def no_verbose(self):
		#sys.stdout = os.devnull
		sys.stderr = os.devnull
		#sys.stdwrn = os.devnull
		pass

	def inline(self):
			print('--- INLINE COMMAND PROMPT ---')
			print('0 => Ende')
			cli = True
			while cli:
			        time.sleep(self.sys.c.sleep)
				cmd = raw_input('>>> ')
				#cmd = sys.stdin.readline()
				#if cmd == '0\n':
				if cmd == '0':
					#CLI wird beendet
					cli = False
					self.sys.stoppall()
				if cmd == 'v' or cmd == 'verbose':
					self.verbose()
				if cmd == 'q' or cmd == 'verbose quit':
					self.no_verbose()
				if cmd == 'm' or cmd == 'modus':
					print('gui=> Graphics Interface')
					tmp = raw_input('  modus >>> ')
					if tmp == 'gui':
						self.sys.start_gui()
						break
					
