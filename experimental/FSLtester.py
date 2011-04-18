#!/usr/bin/python

#File:			FileSystemListener.py
#Description:		Diese Klasse ist der Handler fuer Aktivitaeten im FileSystem
#Author:		Kaleb Tschabold
#Creation Date:		14.4.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		14.4.2011	Grundfunktionalitaeten werden erstellt

from FileSystemListener import *
from Utility import *

listener = FileSystemListener()
listener.add_watch('/home/shylux/project-browser', True)
listener.start()
