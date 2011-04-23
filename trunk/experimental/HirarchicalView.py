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
import os

class HirarchicalView(View):
	mod = 'hirarchical'
	def __init__(self,sys):
		View.__init__(self,sys)
		b = gtk.Label('hview')
		self.put(b,100,100)

	def update(self):
		print('Suche ordner/datei: '+self.get_actTxtInput())
	

