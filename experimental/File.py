#!/usr/bin/python

#File:			File.py
#Description:		Jede Datei die im Programm bearbeitet wird wir in einer solchen Klasse referenziert
#Author:		Kaleb Tschabold
#Creation Date:		14.4.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		14.04.2011	Grundfunktionalitaeten werden erstellt
#			0.9		21.04.2011	Created methods and functionality. Added __doc__s. added test (bottom)

import re

class File:
  	"""represents a file on the filesysem"""
  	fileName	= None
	path		= None
	isDir		= None
	tags		= None
	backup		= None
	fullPath	= None
	def __init__(self, fileName=None, path=None, tags=[], backup=False, isDir=False, fullPath=None):
	  	"""Constructor
		@param	fileName, string	, optional 
		@param	path	, string	, optional
		@param	tags	, list		, optional
		@param	backup	, boolean	, optional
		"""
		self.fileName	= fileName
		self.path	= path
		self.tags	= tags
		self.backup	= backup
		self.isDir	= isDir
		self.fullPath	= fullPath

		if not fullPath == None:
			if fullPath.endswith("/") or fullPath.endswith("\\"):
				p = re.compile("((?:.*\\\)|(?:.*/))((?:[^/]*)|(?:[^\\\]*))([/|\\\])")
				match = p.match(fullPath)
				if not match.group(1) == None and not match.group(2) == None:
					self.path = match.group(1)
					print self.path
					self.fileName = match.group(2)+match.group(3)
					print self.fileName
			else:
				p = re.compile("((?:.*\\\)|(?:.*/))((?:[^/]*)|(?:[^\\\]*))")
				match = p.match(fullPath)
				if not match.group(1) == None and not match.group(2) == None:
					self.path = match.group(1)
					print self.path
					self.fileName = match.group(2)
					print self.fileName

	
	def setFileName(self, fileName):
	  	"""@param	filename	, string"""
		self.fileName	= fileName

	def setPath(self, path):
	  	"""@param	path	, string"""
	  	self.path	= path

	def setIsDir(self,b):
		"""@param	b	, boolean """
		self.isDir = b

	def setTags(self, tags):
	  	"""@param	tags	, list"""
	  	self.tags	= tags

	def setBackup(self, backup):
	  	"""@param backup	, boolean"""
	  	self.backup	= backup

	def getFileName(self):
	  	"""@return fileName, string"""
	  	return self.fileName

	def getPath(self):
	  	"""@return path, string"""
	  	return self.path

	def getIsDir(self):
		"""@return isDir, boolean """
		return self.isDir

	def getTags(self):
	  	"""@return tags, list"""
	  	return self.tags

	def getBackup(self):
	  	"""@return backup, boolean"""
	  	return self.backup
	
	def addTag(self, tag):
	  	"""Adds a single tag (passed as string) to the list of tags.
		uses .append"""
	  	self.tags.append(tag)

	def addTags(self, tags):
	  	"""Adds a list of tags (passed as list) to the list of tags.
		uses .extend"""
	  	self.tags.extend(tags)

if __name__ == "__main__":
  	print "Starting tests"
	print "=============="
	x = File()
	if x.getFileName() == None:
		print "Test #1: Succeed"
	else:
		print "Test #1: FAIL"

	x.setFileName("test")
	if x.getFileName() == "test":
		print "Test #2: Succeed"
	else:
		print "Test #2: FAIL"

	x.setTags(["test", "tag"])
	if x.getTags() == ["test","tag"]:
		print "Test #3: Succeed"
	else:
	  	print "Test #3: FAIL"

	x.addTag("new tag")
	if x.getTags()[2] == "new tag":
		print "Test #4: Succeed"
	else:
	  	print "Test #4: FAIL"

	x.addTags(["extend","linux","unix"])
	if x.getTags()[3:] == ["extend","linux","unix"]:
		print "Test #5: Succeed"
	else:
	  	print "Test #5: FAIL"
	
	x.setIsDir(True)
	if x.getIsDir():
		print "Test #6: Succeed"
	else:
	  	print "Test #6: FAIL"

	test = File(fullPath="/home/niklaus/lol.txt")
	test2 = File(fullPath="C:\\windows\\system32\\chlous.txt.test")
	test3 = File(fullPath="C:\\windows\\system32\\")
	test4 = File(fullPath="/home/niklaus/Music/")
	print File.__init__.__doc__
