#!/usr/bin/python

#File:			FileSystemListener.py
#Description:		Diese Klasse ist der Handler fuer Aktivitaeten im FileSystem
#Author:		Kaleb Tschabold
#Creation Date:		14.4.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		14.4.2011	Grundfunktionalitaeten werden erstellt

from FileSystemListener_Linux import *
from FileSystemListener_Mac import *
from FileSystemListener_Windows import *

class FileSystemListener:
	def __init__(self):
		
