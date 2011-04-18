#!/usr/bin/python

#File:			HirarchicalView.py
#Description:		Klasse um die Orderstrucktur anzuzeigen
#Author:		Kaleb Tschabold
#Creation Date:		29.3.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		29.3.2011	Grundfunktionalitaeten werden erstellt
#			0.1		18.3.2011	Erben von View und init Funktion aufrufen

from View import *
import gtk

class HirarchicalView(View):
	def __init__(self):
		View.__init__(self)
		pass
