#!/usr/bin/python

#File:			Constant.py
#Description:		Hier sind alle Wichtigen Konstanten fuers Programm an einer zentrallen Stelle gespeichert.
#Author:		Kaleb Tschabold
#Creation Date:		16.4.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		16.4.2011	Grundfunktionalitaeten werden erstellt
import os.path

class Constant():
  	sleep	= None
	prgname	= None
	version	= None
	dbPath	= None
	def __init__(self):
		#time to sleep in a endlos loop
		self.sleep	= 0.1
		self.prgname	= "Project Browser"
		self.version	= 0.1
		self.dbPath	= os.path.expanduser("~/.project-browser/")
		self.startview = 'hirarchical'
