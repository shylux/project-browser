#!/usr/bin/python

#File:			View.py
#Description:		Diese Klasse kann die 2 Ansichten(Tag und Hirarchisch) verwalten
#Author:		Kaleb Tschabold
#Creation Date:		14.4.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		14.4.2011	Grundfunktionalitaeten werden erstellt
#			0.2		18.4.2011	Erbt von gtk.Layout

import gtk
import gobject

class View(gtk.Layout):
	def __init__(self):
		gtk.Layout.__init__(self)
		pass

#Registriert diese Klasse als pygtk-widget
gobject.type_register(View)
