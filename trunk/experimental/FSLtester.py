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
import os

path = ".";
abspath = os.path.abspath(path)
print abspath
listener = FileSystemListener()
listener.add_watch(abspath, True)
listener.start()
