#!/usr/bin/python

#File:			DB.py
#Description:		Zugriff auf die DB
#Author:		Kaleb Tschabold
#Creation Date:		29.3.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		29.03.2011	Grundfunktionalitaeten werden erstellt
#			0.2		21.04.2011	Added a few methods to read some data from the DB
#			0.3		23.04.2011	Will now autocreate tables if nonexistance

import sqlite3
import os.path
import File

class DB:
  	#TODO setBackup
  	connection	= None
	cursor		= None
	dbpath		= None
	def __init__(self, dbpath):
		self.dbpath	= dbpath
		self.__establishConnection()
		self.connection.text_factory = str

	def __establishConnection(self):
	  	#print self.dbpath
	  	self.connection	= sqlite3.connect(self.dbpath,check_same_thread = False)
		self.cursor	= self.connection.cursor()
		print "connection established"
		#Check wether the tables in the DB exist. If they don't, we'll create 'em
		self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='files'")
		if len(self.cursor.fetchall()) != 1:
			print "DB's empty. Creating tables"
			self.__createDB()

	def __createDB(self):
	  	self.cursor.execute("CREATE TABLE files(fid INTEGER PRIMARY KEY, filename TEXT, path TEXT, backup BOOLEAN, isdir BOOLEAN)")
		self.cursor.execute("CREATE TABLE tagnames(tagid INTEGER PRIMARY KEY, tagname TEXT UNIQUE , backup BOOLEAN)")
		self.cursor.execute("CREATE TABLE file_tag_relations(relid INTEGER PRIMARY KEY, fk_fid INTEGER, fk_tagid INTEGER)")
		self.connection.commit()

	def __changeList(self, li):
		ret_value	= []
		for row in li:
			ret_value.append(row[0])
		return ret_value

	def __cleanupTags(self):
	  	"""Delete old tags from database. This is tags that are not connected to any file"""
		delTagQuery = "DELETE FROM tagnames WHERE tagnames.tagid NOT IN (SELECT file_tag_relations.fk_tagid FROM file_tag_relations)"
		self.cursor.execute(delTagQuery)
		self.connection.commit()

	def __connectTagsToFile(self, tags, fid):
	  	"""Insert tags to db and connect them up with the file
		@param tags, List, list of tags you want to connect to the file
		@param fid, integer, the id of the file you want to connect the tags to"""
		tags = list(set(tags))	#remove duplicates from list
		for row in tags:
			self.cursor.execute("INSERT OR IGNORE INTO tagnames (tagname, backup) VALUES (?, ?)", (row, False))
			self.cursor.execute("SELECT tagid FROM tagnames WHERE tagname = ?", (row, ))
			res = self.cursor.fetchall()
			self.cursor.execute("INSERT INTO file_tag_relations(fk_fid, fk_tagid) VALUES (?, ?)", (fid, res[0][0]))

		self.connection.commit()
	

	def __generateFilesArray(self, li):
	  	"""Takes the result from SELECT * FROM files... statement.
		Then gets for each of the files the corresponding tags, and puts it all together
		into a File.py object"""
	  	ret_value	= []
		for row in li:
			self.cursor.execute("SELECT tagnames.tagname FROM files LEFT JOIN file_tag_relations, tagnames ON (files.fid = file_tag_relations.fk_fid AND file_tag_relations.fk_tagid = tagnames.tagid) WHERE files.fid = ?", (row[0], ))
			tagLi		= self.cursor.fetchall()
			tagList		= self.__changeList(tagLi)

			fi	= File.File(fileName=row[1], path=row[2], backup=row[3], isDir=row[4], tags=tagList)
			ret_value.append(fi)
		return ret_value

	def updateFile(self, fi):
	  	#TODO update backup state!
		"""Updates The tags of a file. Updating the backup value is planned and coming soon
		@param fi, File, The file you want to update. The path and filename have to be the same as on the DB
		You can not use this to move a file, there is moveFile() for that.
		If the file you pass does not exist on the DB yet, addFile will be called instead
		Make sure not to pass a File object with no tags, except if you want to wipe out all tags of that file on DB level"""
	  	new_tags = []	#Tags from file object (ATTENTION! They get filtered later!)
		old_tags = []	#Tags from database
		if self.fileInDB(fi):
			old_tags = self.getTagsToFile(fi)
			new_tags = fi.getTags()
			for row in old_tags:
				try:
					#remove all occurences of old tags from the new tag array, so only new tags are left
					new_tags = filter (lambda a: a != row, new_tags)
				except:
					print "Error while removing element from old_tags"
			self.cursor.execute("SELECT files.fid FROM files WHERE files.filename = ? AND files.path = ?", (fi.getFileName(), fi.getPath(), ))
			fid = self.cursor.fetchall()[0][0]
			if len(new_tags) > 0:
				self.__connectTagsToFile(new_tags, fid)
			else:
				pass

			#Remove old tags from database
			deprecatedTags = old_tags
			for row in fi.getTags():
				try:
					#Remove all tags tags of the file object from the array of tags that are in the database
					#This leaves us with just the tags that are in the database but that are NOT in the file object
					deprecatedTags = filter(lambda a: a != row, deprecatedTags)
				except:
					print ""
			if len(deprecatedTags) > 0:
				tagids = []
				for line in deprecatedTags:
					self.cursor.execute("SELECT tagid FROM tagnames WHERE tagname = ?", (line, ))
					tagids.extend(self.cursor.fetchall()[0])
				for line in tagids:
					self.cursor.execute("DELETE FROM file_tag_relations WHERE fk_tagid = ? AND fk_fid = ?", (line, fid, ))
				self.connection.commit()
				self.__cleanupTags()
		else:
			self.addFile(fi)
				
	     	
	def fileInDB(self, fi):
	  	"""Checks wether a files is in the db or not
		@param fi, File, The The file which's presence in the DB you want to check. Only name and path are needed"""
		self.cursor.execute("SELECT files.filename FROM files WHERE files.filename = ? AND files.path = ?", (fi.getFileName(), fi.getPath(), ))
		value = self.cursor.fetchall()

		if len(value) > 0:
			return True
		else:
		  	return False

#	def executeQuerry(self, query):
#		"""Deprecated! Won't be provided anymore for security reasons!"""
#		self.cursor.execute(query)
#		return self.cursor.fetchall()

	def getTagsToFile(self, _file):
	  	"""Returns all tags that are connected to the passed file
		@param _file, File, The file whichs tags you want (just fileName and path are important)
		@retur List, List with the Tags of the file"""
		li		= None
		self.cursor.execute("SELECT tagnames.tagname FROM files LEFT JOIN file_tag_relations, tagnames ON (files.fid = file_tag_relations.fk_fid AND file_tag_relations.fk_tagid = tagnames.tagid) WHERE path = ? AND filename = ?", (_file.getPath(), _file.getFileName()))
		li	= self.cursor.fetchall()
		return self.__changeList(li)

	def getFilesFromPath(self, path):
		"""Get all Files that are in a specific directory. Files will be returned containing all tags 'n' stuff
		@param path, String, the Path you want to get files from (make sure to include / or \ at the end)
		@return List, list of Files that are in the specified path"""
		ret_value	= []
		li		= None

		self.cursor.execute("SELECT * FROM files WHERE path = ?", (path, ))
		li	= self.cursor.fetchall()
		return self.__generateFilesArray(li)

	def getFilesFromTag(self, tag):
	  	"""Gets you all files that 'have' a specific tag
		@param tag, String, The tag you want to get the corresponding files to"""
		ret_value	= []
		li		= None
		ids		= []

		self.cursor.execute("SELECT files.* FROM files LEFT JOIN file_tag_relations, tagnames ON (files.fid = file_tag_relations.fk_fid AND file_tag_relations.fk_tagid = tagnames.tagid) WHERe tagnames.tagname = ?", (tag, ))
		li	= self.cursor.fetchall()
		return self.__generateFilesArray(li)

	def getAllTags(self):
	  	"""Returns all tags in the form of strings
		@return List, list of all tags"""
		self.cursor.execute("SELECT tagname FROM tagnames")
		li = self.cursor.fetchall()
		return self.__changeList(li)

	def addFile(self, fi):
	  	"""Adds a file to the database
		@param, fi, File, Fileobject that you want to add"""
		#IMPORTANT: For this to work, the field tagnames.tagname has to be marked as UNIQUE!
		#Otherwise, attempts to insert tags might cause trouble!
		if not self.fileInDB(fi):
			self.cursor.execute("INSERT INTO FILES (filename, path, backup, isdir) VALUES (?, ?, ?, ?)", (fi.getFileName(), fi.getPath(), fi.getBackup(), fi.getIsDir()))
			fid	= self.cursor.lastrowid
			self.connection.commit();
			self.__connectTagsToFile(fi.getTags(), fid)
		else:
			self.updateFile(fi)

	def removeFile(self, fi):
		"""Removes a file from the Database.
		@param fi, File, Fileobject representing the file you want to remove (only fileName and path are important)"""
		self.cursor.execute("SELECT files.fid FROM files WhERE files.path = ? AND files.filename = ? ", (fi.getPath(), fi.getFileName()))
		fid = self.cursor.fetchall()[0][0]
		self.cursor.execute("DELETE FROM files WHERE files.fid = ?", (fid, ))
		self.connection.commit()
		self.cursor.execute("DELETE FROM file_tag_relations WHERE file_tag_relations.fk_fid = ? ", (fid, ))
		self.connection.commit()
		self.__cleanupTags()

	def addTagToFile(self, fi, tag):
	  	"""Adds a single tag to a file.
		@param fi, File Fileobject that represents the file you want to add the tag to (only fileName and path are important)
		@tag, String, the tag you want to add to the file"""
		if self.fileInDB(fi):
			idQuery = "SELECT files.fid FROM files WHERE files.filename = '%s' AND files.path = '%s'" % (fi.getFileName(), fi.getPath())
			self.cursor.execute(idQuery)
			fid = self.cursor.fetchall()[0][0]
			self.__connectTagsToFile([tag, ], fid)

#	def addTag(self, tag):
#		"""DEPRECATED!
#		Add a tag to the database without connecting it to a file.
#		Does not really make any sense, because we are deleting tags with no relations at several points."""
#		query = "INSERT OR IGNORE INTO tagnames (tagname, backup) VALUES ('%s', 'False')" % (tag, )
#		self.cursor.execute(query)
#		self.connection.commit()
	
	def moveFile(self, f1, f2):
		"""rename/move a file.
		@param f1, File, a File object with the path and the name of the file as it is BEFORE the movement
		@param f2, File, a File object with the path and the name of the file as it is AFTER the movement"""
		if not self.fileInDB(f2):
			self.cursor.execute("UPDATE files SET filename = ?, path = ? WHERE filename = ? AND path = ?", (f2.getFileName(), f2.getPath(), f1.getFileName(), f1.getPath(), ))
			self.connection.commit()
		else:
			print "file '" + f2.getFullPath +"' exists, can't move!"
	
	def renameFile(self, f1, f2):
		#Just calling moveFile
		self.moveFile(f1, f2)

	def getFile(self, fi):
	  	"""Gets all the details to a file (tags, backup state, ....
		@param fi, File, A file object with the filename and the path of the file whichs details you want to get"""
		self.cursor.execute("SELECT * from files WHERE filename = ? and path = ?", (fi.getFileName(), fi.getPath()))	
		f2 = self.cursor.fetchall()
		f3 = self.__generateFilesArray(f2)[0]
		return f3

	def copyFile(self, f1, f2):
		"""Copy a file (including all tags, backup stae 'n' stuff).
		@param f1, File, the file you want to copy
		@param f2, File, a File object with the name and the path of the copy"""
		if not self.fileInDB(f2):
			f3 = self.getFile(f1)
			f3.setFileName(f2.getFileName())
			f3.setPath(f2.getPath())
			self.addFile(f3)

if __name__ == "__main__":
	#Modul tests:
	#==========================================
	print 'Mdule tests start'
	db = DB("testdb")
	f1 = File.File(fileName="documentation.tex", path="/home/niklaus/Documents/", tags=['LaTeX', 'documentation', 'filebrowser', 'project', 'school', 'test', ])
	db.addFile(f1)
	if len(db.getAllTags()) == 6:
		print "Test 01: Succeed"
	else:
		print "Test 01: FAIL"

	f2 = File.File(fileName="Music/", path="/home/niklaus/", tags=['music', 'multimedia', 'entertainment', 'test',])
	db.addFile(f2)
	if len(db.getAllTags()) == 9:
		print "Test 02: Succeed"
	else:
		print "Test 02: FAIL"

	if len(db.getTagsToFile(f2)) == 4:
		print "Test 03: Succeed"
	else:
		print "Test 03: FAIL"

	f3 = File.File(fileName="Music/", path="/home/niklaus/", tags=['music', 'multimedia', 'entertainment',])
	db.updateFile(f3)
	if len(db.getAllTags()) == 9 and len(db.getTagsToFile(f3)) == 3:
		print "Test 04: Succeed"
	else:
		print "Test 04: FAIL"

	f4 = File.File(fileName="documentation.tex", path="/home/niklaus/Documents/", tags=['LaTeX', 'documentation', 'filebrowser', 'project', 'school', ])
	db.addFile(f4)
	if len(db.getAllTags()) == 8 and len (db.getTagsToFile(f4)) == 5:
		print "Test 05: Succeed"
	else:
		print "Test 05: FAIL"
	
	f5 = File.File(fileName="documentation.tex", path="/home/niklaus/Documents", tags=['LaTeX', 'documentation', 'filebrowser', 'project', 'school', 'dbtest', 'modultest', ])
	db.updateFile(f5)
	if len(db.getAllTags()) == 10 and len(db.getTagsToFile(f5)) == 7:
		print "Test 06: Succeed"
	else:
		print "Test 06: FAIL"
	
	db.removeFile(f5)
	if len(db.getFilesFromPath("/home/niklaus/Documents/")) == 0 and len(db.getAllTags()) == 3:
		print "Test 07: Succeed"
	else:
		print "Test 07:FAIL"

	f6 = File.File(path="/home/niklaus/Videos/", fileName="Movies/", isDir=True, tags=['entertainment', 'multimedia', 'movie'])
	db.updateFile(f6)
	fTest = db.getFilesFromPath("/home/niklaus/Videos/")[0]
	if fTest.getFileName() == "Movies/" and fTest.getPath() == "/home/niklaus/Videos/" and fTest.getIsDir() == True and fTest.getTags() == ['movie', 'multimedia', 'entertainment', ]:
		print "Test 08: Succeed"
	else:
		print "Test 08: FAIL"

	f7 = File.File(path="/home/niklaus/doku/", fileName="projektantrag.tex", tags=['LaTeX', 'projectexplorer', 'berufsschule',], backup=True)
	f8 = File.File(path="/home/niklaus/", fileName="doku/", isDir=True, tags=['projectexplorer', 'brufsschule', ])
	f9 = File.File(path="/home/niklaus/doku/", fileName="projektantrag.pdf", tags=['projectexplorer', 'berufsschule'])
	f10 = File.File(path="/home/niklaus/doku/", fileName="projektplan.tex", tags=['LaTeX', 'projectexplorer', 'berufsschule',], backup=True)
	f11 = File.File(path="/home/niklaus/doku/", fileName="projektplan.pdf", tags=['projectexplorer', 'berufsschule'])
	db.addFile(f7)
	db.addFile(f8)
	db.addFile(f9)
	db.addFile(f10)
	db.addFile(f11)
	if len(db.getFilesFromPath("/home/niklaus/doku/")) == 4 and db.getFilesFromTag("LaTeX")[0].getBackup() == True:
		print "Test 09: Succeed"
	else:
		print "Test 09: FAIL"

	f12 = File.File(path="/home/niklaus/doku/projektplan/", fileName="projektplan.tex", tags=['LaTeX', 'projectexplorer', 'berufsschule',], backup=True)
	f13 = File.File(path="/home/niklaus/doku/projektplan/", fileName="projektplan01.pdf", tags=['projectexplorer', 'berufsschule'])
	db.moveFile(f10, f12)
	db.renameFile(f11, f13)
	if len(db.getFilesFromPath("/home/niklaus/doku/")) == 2 and len(db.getFilesFromPath("/home/niklaus/doku/projektplan/")) == 2:
		print "Test 10: Succeed"
	else:
		print "Test 10: FAIL"

	if db.getFilesFromPath("/home/niklaus/doku/projektplan/")[1].getFileName()=="projektplan01.pdf" or db.getFilesFromPath("/home/niklaus/doku/projektplan/")[0].getFileName()=="projektplan01.pdf":
		print "Test 11: Succeed"
	else:
	  	print "Test 11: FAIL"

	if db.getFilesFromPath("/home/niklaus/doku/projektplan/")[1].getFileName()=="projektplan.tex" or db.getFilesFromPath("/home/niklaus/doku/projektplan/")[0].getFileName()=="projektplan.tex":
		print "Test 12: Succeed"
	else:
	  	print "Test 12: FAIL"

	if db.fileInDB(f13):
		print "Test 13: Succeed"
	else:
	  	print "Test 13: FAIL"
	
	if not db.fileInDB(f10):
		print "Test 14: Succeed"
	else:
	  	print "Test 14: FAIL"

	f14 = File.File(path="/home/niklaus/test/", fileName="test.txt", tags=['foo', 'bar', ])
	f15 = File.File(path="/home/niklaus/test/", fileName="test.txt", tags=['foo', 'bar', ])
	db.addFile(f14)
	db.addFile(f15)
	if len(db.getFilesFromPath("/home/niklaus/test/")) == 1:
		print "Test 15: Succeed"
	else:
		print "Test 15: FAIL"
	
	f16 = File.File(path="/home/niklaus/test/", fileName="test.txt", tags=['foo', 'bar', 'muh', ])
	db.addFile(f16)
	if len(db.getFilesFromPath("/home/niklaus/test/")) == 1 and db.getFilesFromPath("/home/niklaus/test/")[0].getTags() == ['foo', 'bar', 'muh', ]:
		print "Test 16: Succeed"
	else:
	  	print "Test 16: FAIL"

	f17 = File.File(path="/home/project/", fileName="heroes", tags=['shylux', 'tschabold', 'bash.vi'])
	db.addFile(f17)
	if len(db.getTagsToFile(f17)) == 3:
		print "Test 17: Succeed"
	else:
	  	print "Test 17: FAIL"

	f18 = File.File(path="/home/project/", fileName="heroes", tags=['shylux', 'tschabold', 'bash.vi', 'heroes', 'project'])
	db.updateFile(f18)
	if len(db.getTagsToFile(f17)) == 5:
		print "Test 18: Succeed"
	else:
	  	print "Test 18: FAIL"
	
	f19 = File.File(path="/home/project/", fileName="heroes", tags=['tschabold', ])
	db.updateFile(f19)
	if len(db.getTagsToFile(f17)) == 1:
		print "Test 19: Succeed"
	else:
	  	print "Test 19: FAIL"

	f20 = db.getFile(f18)
	if len(f20.getTags()) == 1 and f20.getTags()[0] == 'tschabold':
		print "Test 20: Succeed"
	else:
		print "Test 20: FAIL"

	f21 = File.File(path="/home/niklaus/copy/", fileName="copy.text", tags=['copy', 'test', 'projectexplorer'])
	f22 = File.File(path="/home/test/copy/", fileName="copy.tested")
	db.addFile(f21)
	db.copyFile(f21, f22)
	f23 = db.getFile(f22)
	if f23.getFileName() == "copy.tested" and f23.getPath()=="/home/test/copy/" and len(f23.getTags()) == 3:
		print "Test 21: Succeed"
	else:
	  	print "Test 21: FAIL"
	#TODO addTagToFile
	print "="*20
	db.getFile(f18)
