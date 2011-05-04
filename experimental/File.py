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
					self.fileName = match.group(2)+match.group(3)
			else:
				p = re.compile("((?:.*\\\)|(?:.*/))((?:[^/]*)|(?:[^\\\]*))")
				match = p.match(fullPath)
				if not match.group(1) == None and not match.group(2) == None:
					self.path = match.group(1)
					self.fileName = match.group(2)

	def __checkPaths(self):
		# Check wether all paths have / (or \ on Windows) at the end
		#TODO implement
		pass
	
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

	def setFullPath(self, fullPath):
		"""@param fullPath	, Path including filename"""
		this.fullPath	= fullPath

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

	def getFullPath(self):
		"""@return fullPath, String representing the full path to the file, including the file's name"""
		if self.fullPath == None:
			return self.path + self.fileName
		else:
			return self.fullPath
	
	def addTag(self, tag):
	  	"""Adds a single tag (passed as string) to the list of tags.
		uses .append"""
	  	self.tags.append(tag)

	def addTags(self, tags):
	  	"""Adds a list of tags (passed as list) to the list of tags.
		uses .extend"""
	  	self.tags.extend(tags)

	def ex_backup(self):
		print "Backup", self.getPath()

if __name__ == "__main__":
  	print "Starting tests"
	print "=============="
	x = File()
	if x.getFileName() == None:
		print "Test #01: Succeed"
	else:
		print "Test #01: FAIL"

	x.setFileName("test")
	if x.getFileName() == "test":
		print "Test #02: Succeed"
	else:
		print "Test #02: FAIL"

	x.setTags(["test", "tag"])
	if x.getTags() == ["test","tag"]:
		print "Test #03: Succeed"
	else:
	  	print "Test #03: FAIL"

	x.addTag("new tag")
	if x.getTags()[2] == "new tag":
		print "Test #04: Succeed"
	else:
	  	print "Test #04: FAIL"

	x.addTags(["extend","linux","unix"])
	if x.getTags()[3:] == ["extend","linux","unix"]:
		print "Test #05: Succeed"
	else:
	  	print "Test #05: FAIL"
	
	x.setIsDir(True)
	if x.getIsDir():
		print "Test #06: Succeed"
	else:
	  	print "Test #06: FAIL"

	#Testing the path stuff...
	f1 = File(fullPath="/home/niklaus/lol.txt")
	if f1.getPath() == "/home/niklaus/" \
	    and f1.getFileName() == "lol.txt" and f1.getFullPath() == "/home/niklaus/lol.txt":
		print "Test #07: Succeed"
	else:
		print "Test #07: FAIL"

	f2 = File(fullPath="C:\\windows\\system32\\chlous.txt.test")
	if f2.getPath() == "C:\\windows\\system32\\" \
	    and f2.getFileName() == "chlous.txt.test" and f2.getFullPath() == "C:\\windows\\system32\\chlous.txt.test":
		print "Test #08: Succeed"
	else:
	  	print "Test #09: FAIL"

	f3 = File(fullPath="C:\\windows\\system32\\")
	if f3.getPath() == "C:\\windows\\" \
	    and f3.getFileName() == "system32\\" and f3.getFullPath() == "C:\\windows\\system32\\":
		print "Test #10: Succeed"
	else:
	  	print "Test #10: FAIL"
	f4 = File(fullPath="/home/niklaus/Music/")
	if f4.getPath() == "/home/niklaus/" \
	    and f4.getFileName() == "Music/" and f4.getFullPath() == "/home/niklaus/Music/":
		print "Test #11: Succeed"
	else:
	  	print "Test #11: FAIL"

	f5 = File(fileName="document.odt", path="/home/niklaus/Documents/")
	if f5.getFullPath() == "/home/niklaus/Documents/document.odt":
		print "Test #12: Succeed"
	else:
		print "Test #12: FAIL"

	f6 = File(fileName="Videos/", path="/home/niklaus/", isDir=True)
	if f6.getFullPath() == "/home/niklaus/Videos/" and f6.getIsDir() == True:
		print "Test #13: Succeed"
	else:
	  	print "Test #13: FAIL"

	f7 = File(fileName="hosts", path="C:\\windows\\system32\\etc\\")
	if f7.getFullPath() == "C:\\windows\\system32\\etc\\hosts":
		print "Test #14: Succeed"
	else:
		print "Test #14: FAIL"

	f8 = File(fileName="etc\\", path="C:\\windows\\system32\\", isDir=True)
	if f8.getFullPath() == "C:\\windows\\system32\\etc\\" and f8.getIsDir() == True:
		print "Test #15: Succeed"
	else:
	  	print "Test #15: FAIL"

	print File.__init__.__doc__

	#Backup
	b = File()
	b.ex_backup()
