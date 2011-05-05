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
  	connection	= None
	cursor		= None
	dbpath		= None
	def __init__(self, dbpath):
		self.dbpath	= dbpath
		self.establishConnection()
		self.connection.text_factory = str

	def establishConnection(self):
	  	#print self.dbpath
	  	self.connection	= sqlite3.connect(self.dbpath,check_same_thread = False)
		self.cursor	= self.connection.cursor()
		print "connection established"
		#Check wether the tables in the DB exist. If they don't, we'll create 'em
		self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='files'")
		if len(self.cursor.fetchall()) != 1:
			print "DB's empty. Creating tables"
			self.__createDB()

	def fileInDB(self, fi):
	  	"""Checks wether a files is in the db or not"""
		#checkQuery = "SELECT files.filename FROM files WHERE files.filename = '%s' AND files.path = '%s'" % (fi.getFileName(), fi.getPath(), )
		#self.cursor.execute(checkQuery)
		self.cursor.execute("SELECT files.filename FROM files WHERE files.filename = ? AND files.path = ?", (fi.getFileName(), fi.getPath(), ))
		value = self.cursor.fetchall()

		if len(value) > 0:
			return True
		else:
		  	return False

	def executeQuerry(self, query):
		"""Deprecated! Won't be provided anymore for security reasons!"""
		self.cursor.execute(query)
		return self.cursor.fetchall()

	def __changeList(self, li):
		ret_value	= []
		for row in li:
			ret_value.append(row[0])
		return ret_value

	def __cleanupTags(self):
		delTagQuery = "DELETE FROM tagnames WHERE tagnames.tagid NOT IN (SELECT file_tag_relations.fk_tagid FROM file_tag_relations)"
		self.cursor.execute(delTagQuery)
		self.connection.commit()

	def __connectTagsToFile(self, tags, fid):
			tags = list(set(tags))	#remove duplicates from list
			for row in tags:
				#tagQuery = "INSERT OR IGNORE INTO tagnames (tagname, backup) VALUES ('%s', 'False')" % (row, )
				#print tagQuery
				#self.cursor.execute(tagQuery)
				self.cursor.execute("INSERT OR IGNORE INTO tagnames (tagname, backup) VALUES (?, ?)", (row, False))

				#idQuery	= "SELECT tagid FROM tagnames WHERE tagname = '%s'" % (row, )
				#self.cursor.execute(idQuery)
				self.cursor.execute("SELECT tagid FROM tagnames WHERE tagname = ?", (row, ))
				res = self.cursor.fetchall()

				#relQuery = "INSERT INTO file_tag_relations(fk_fid, fk_tagid) VALUES ('%s', '%s')" % (fid, res[0][0], )
				#self.cursor.execute(relQuery)
				self.cursor.execute("INSERT INTO file_tag_relations(fk_fid, fk_tagid) VALUES (?, ?)", (fid, res[0][0]))

			self.connection.commit()
	

	def __generateFilesArray(self, li):
	  	"""Takes the result from SELECT * FROM files... statement.
		Then gets for each of the files the corresponding tags, and puts it all together
		into a File.py object"""
	  	ret_value	= []
		for row in li:
			#tagQuery	= "SELECT tagnames.tagname FROM files LEFT JOIN file_tag_relations, tagnames ON (files.fid = file_tag_relations.fk_fid AND file_tag_relations.fk_tagid = tagnames.tagid) WHERE files.fid = '%d'" % (row[0], )
			#self.cursor.execute(tagQuery)
			self.cursor.execute("SELECT tagnames.tagname FROM files LEFT JOIN file_tag_relations, tagnames ON (files.fid = file_tag_relations.fk_fid AND file_tag_relations.fk_tagid = tagnames.tagid) WHERE files.fid = ?", (row[0], ))
			tagLi		= self.cursor.fetchall()
			tagList		= self.__changeList(tagLi)

			fi	= File.File(fileName=row[1], path=row[2], backup=row[3], isDir=row[4], tags=tagList)
			ret_value.append(fi)
		return ret_value

	def updateFile(self, fi):
	  	new_tags = []	#Tags from file object (ATTENTION! They get filtered later!)
		old_tags = []	#Tags from database
		if self.fileInDB(fi):
			old_tags = self.getTagsToFile(fi)
			new_tags = fi.getTags()
			#print "Tags inside the file: "
			#print new_tags
			for row in old_tags:
				try:
					#remove all occurences of old tags from the new tag array, so only new tags are left
					new_tags = filter (lambda a: a != row, new_tags)
				except:
					print "Error while removing element from old_tags"
			#print new_tags
			#Following three lines were moved out of the if statement in order to be able to use fid for the remove thing
			#fidQuery = "SELECT files.fid FROM files WHERE files.filename = '%s' AND files.path = '%s'" % (fi.getFileName(), fi.getPath())
			#self.cursor.execute(fidQuery)
			self.cursor.execute("SELECT files.fid FROM files WHERE files.filename = ? AND files.path = ?", (fi.getFileName(), fi.getPath(), ))
			fid = self.cursor.fetchall()[0][0]
			if len(new_tags) > 0:
				self.__connectTagsToFile(new_tags, fid)
			else:
				#print "No new tags, won't do anything"
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
				#print "There ae old tags to be removed!"
				#OK, I know that this is DAMNED UGLY, but I can't see any other way for getthing rid of the god damned stupid u in front of each element of the list
				#dT = ""
				#for line in deprecatedTags:
				#	#print str(line)
				#	dT = dT + "'" + line + "'" + ", "
				##remove , and space at the end
				#dT = dT[:-2]
				#print dT
				tagids = []
				for line in deprecatedTags:
					self.cursor.execute("SELECT tagid FROM tagnames WHERE tagname = ?", (line, ))
					tagids.extend(self.cursor.fetchall()[0])
				#delTagQuery = "DELETE FROM file_tag_relations WHERE fk_tagid IN (SELECT tagid FROM tagnames WHERE tagname IN (%s)) AND fk_fid = '%s'" % (dT, fid, )
				#self.cursor.execute(delTagQuery)
				for line in tagids:
					self.cursor.execute("DELETE FROM file_tag_relations WHERE fk_tagid = ? AND fk_fid = ?", (line, fid, ))
				self.connection.commit()
				self.__cleanupTags()
		else:
			print "File not yet in DB, will run addFile instead"
			self.addFile(fi)
				
	     	
	def getTagsToFile(self, _file):
		li		= None
	  	#query	= "SELECT tagnames.tagname FROM files LEFT JOIN file_tag_relations, tagnames ON (files.fid = file_tag_relations.fk_fid AND file_tag_relations.fk_tagid = tagnames.tagid) WHERE path = '%s' AND filename = '%s'" % (_file.getPath(), _file.getFileName())
		#self.cursor.execute(query)
		self.cursor.execute("SELECT tagnames.tagname FROM files LEFT JOIN file_tag_relations, tagnames ON (files.fid = file_tag_relations.fk_fid AND file_tag_relations.fk_tagid = tagnames.tagid) WHERE path = ? AND filename = ?", (_file.getPath(), _file.getFileName()))
		li	= self.cursor.fetchall()
		return self.__changeList(li)

	def getFilesFromPath(self, path):
		ret_value	= []
		li		= None

		#query	= "SELECT * FROM files WHERE path = '%s'" % (path, )
		#self.cursor.execute(query)
		self.cursor.execute("SELECT * FROM files WHERE path = ?", (path, ))
		li	= self.cursor.fetchall()
		return self.__generateFilesArray(li)

	def getFilesFromTag(self, tag):
		ret_value	= []
		li		= None
		ids		= []

		#query	= "SELECT files.* FROM files LEFT JOIN file_tag_relations, tagnames ON (files.fid = file_tag_relations.fk_fid AND file_tag_relations.fk_tagid = tagnames.tagid) WHERE tagnames.tagname = '%s'" % (tag, )
		#self.cursor.execute(query)
		self.cursor.execute("SELECT files.* FROM files LEFT JOIN file_tag_relations, tagnames ON (files.fid = file_tag_relations.fk_fid AND file_tag_relations.fk_tagid = tagnames.tagid) WHERe tagnames.tagname = ?", (tag, ))
		li	= self.cursor.fetchall()
		return self.__generateFilesArray(li)

	def getAllTags(self):
		self.cursor.execute("SELECT tagname FROM tagnames")
		li = self.cursor.fetchall()
		return self.__changeList(li)

	def __createDB(self):
	  	self.cursor.execute("CREATE TABLE files(fid INTEGER PRIMARY KEY, filename TEXT, path TEXT, backup BOOLEAN, isdir BOOLEAN)")
		self.cursor.execute("CREATE TABLE tagnames(tagid INTEGER PRIMARY KEY, tagname TEXT UNIQUE , backup BOOLEAN)")
		self.cursor.execute("CREATE TABLE file_tag_relations(relid INTEGER PRIMARY KEY, fk_fid INTEGER, fk_tagid INTEGER)")
		self.connection.commit()

	def addFile(self, fi):
		#IMPORTANT: For this to work, the field tagnames.tagname has to be marked as UNIQUE!
		#Otherwise, attempts to insert tags might cause trouble!
		if not self.fileInDB(fi):
			#query = "INSERT INTO FILES (filename, path, backup, isdir) VALUES ('%s', '%s', '%s', '%s')" % (fi.getFileName(), fi.getPath(), fi.getBackup(), fi.getIsDir())
			#self.cursor.execute(query)
			self.cursor.execute("INSERT INTO FILES (filename, path, backup, isdir) VALUES (?, ?, ?, ?)", (fi.getFileName(), fi.getPath(), fi.getBackup(), fi.getIsDir()))
			fid	= self.cursor.lastrowid
			self.connection.commit();
			self.__connectTagsToFile(fi.getTags(), fid)
		else:
			print "File already in DB, won't add it again, will run updateFile instead!"
			self.updateFile(fi)

	def removeFile(self, fi):
		#idQuery = "SELECT files.fid FROM files WhERE files.path = '%s' AND files.filename = '%s'" % (fi.getPath(), fi.getFileName())
		#self.cursor.execute(idQuery)
		self.cursor.execute("SELECT files.fid FROM files WhERE files.path = ? AND files.filename = ? ", (fi.getPath(), fi.getFileName()))
		fid = self.cursor.fetchall()[0][0]
		#delFileQuery = "DELETE FROM files WHERE files.fid = '%s'" % (fid, )
		#self.cursor.execute(delFileQuery)
		self.cursor.execute("DELETE FROM files WHERE files.fid = ?", (fid, ))
		self.connection.commit()
		#delTagConQuery = "DELETE FROM file_tag_relations WHERE file_tag_relations.fk_fid = '%s'" % (fid, )
		#self.cursor.execute(delTagConQuery)
		self.cursor.execute("DELETE FROM file_tag_relations WHERE file_tag_relations.fk_fid = ? ", (fid, ))
		self.connection.commit()
		self.__cleanupTags()

	def addTagToFile(self, fi, tag):
		if self.fileInDB(fi):
			idQuery = "SELECT files.fid FROM files WHERE files.filename = '%s' AND files.path = '%s'" % (fi.getFileName(), fi.getPath())
			self.cursor.execute(idQuery)
			fid = self.cursor.fetchall()[0][0]
			self.__connectTagsToFile([tag, ], fid)

	def addTag(self, tag):
		"""DEPRECATED!
		Add a tag to the database without connecting it to a file.
		Does not really make any sense, because we are deleting tags with no relations at several points."""
		query = "INSERT OR IGNORE INTO tagnames (tagname, backup) VALUES ('%s', 'False')" % (tag, )
		self.cursor.execute(query)
		self.connection.commit()
	
	def moveFile(self, f1, f2):
		"""rename/move a file.
		@param f1, File, a File object with the path and the name of the file as it is BEFORE the movement
		@param f2, File, a File object with the path and the name of the file as it is AFTER the movement"""
		#TODO Check if such a file does not exist yet
		#updateQuery = "UPDATE files SET filename='%s', path='%s' WHERE filename='%s' AND path='%s'" % (f2.getFileName(), f2.getPath(), f1.getFileName(), f1.getPath(), )
		#self.cursor.execute(updateQuery)
		self.cursor.execute("UPDATE files SET filename = ?, path = ? WHERE filename = ? AND path = ?", (f2.getFileName(), f2.getPath(), f1.getFileName(), f1.getPath(), ))
		self.connection.commit()
	
	def renameFile(self, f1, f2):
		#Just calling moveFile
		self.moveFile(f1, f2)

if __name__ == "__main__":
   	#print "TEST"
	#db = DB("/home/niklaus/.project-browser/db")
	#path = os.path.expanduser("~/.project-browser/db")
	#db = DB(path)
	#db.test(File.File())
	#db.test(1)
	#fi	= File.File(fileName="name1", path="/home/niklaus/", tags=['tag1', 'tag2', 'tagy', 'tag77'], isDir=False)
	#fi	= File.File(fileName="name2", path="/home/niklaus/", tags=['tag1', 'tagy', 'tagZZ'], isDir=False)
	#db.addFile(fi)
	#db.addTagToFile(fi, "testTag07")
	#db.updateFile(fi)
	#li = db.getFilesFromTag("tagX")
	#print li[1].getFileName()
	#db.removeFile(fi)
	"""out = db.executeQuerry("SELECT * FROM files")
	print out
	f = File.File(fileName="test.txt", path="/home/niklaus/")
	print db.getTagsToFile(f)

	print '='*10
	foo = db.getFilesFromPath("/home/niklaus/")
	for row in foo:
		print row.getFileName()
		print row.getPath()
		print row.getBackup()
		print row.getTags()
	print '='*10
	bar = db.getFilesFromTag("text3")
	for row in bar:
		print '='*5 + row.getFileName() + '='*5
		print row.getPath()
		print row.getBackup()
		print row.getTags()
	print '='*10
	print db.getAllTags()"""
	#print '='*10
	#db.fileInDB(File.File(fileName="name", path="/home/niklaus/"))
	#db.addFile(File.File(fileName="addTagTestFile2.test", path="/home/niklaus/text/", tags=['testTag1', 'testTag2'], isDir=False, backup=False))
	#db.addTagToFile(File.File(fileName="addTagTestFile.test", path="/home/niklaus/text/"), 'testTag3')

	#Let's go and test the new stuff in updateFile!!
	#=================================================
	#db = DB("testdb")
	#f1 = File.File(fileName="test.txt", path="/home/niklaus/", tags=['test', 'projectbrowser', ])
	#f2 = File.File(fileName="cc.ogg", path="/home/niklaus/Music/", tags=['music', 'ogg', 'creative commons', ])
	#f3 = File.File(fileName="ozzed.ogg", path="/home/niklaus/Music/", tags=['music', 'ogg', 'creative commons', 'ozzed', '8bit', 'chiptune', ])
	#f4 = File.File(fileName="evil.mp3", path="/home/niklaus/Music/", tags=['music', 'mp3', 'proprietary', ])
	#f5 = File.File(fileName="documentation.odt", path="/home/niklaus/Documents/", tags=['libreoffice', 'odt', 'test', ])
	#db.addFile(f1)
	#db.addFile(f2)
	#db.addFile(f3)
	#db.addFile(f4)
	#db.addFile(f5)
	#print "Tags in the DB: "
	#print '='*10
	#print db.getAllTags()
	#for line in db.getFilesFromPath("/home/niklaus/Music/"):
	#	print line.getFileName()
	#f6 = File.File(fileName="documentation.odt", path="/home/niklaus/Documents/", tags=['libreoffice', 'odt', 'test', 'document', 'projectbrowser', 'random', ])
	#db.updateFile(f6)
	#print "Tags in the DB: "
	#print '='*10
	#print db.getAllTags()
	#for line in db.getFilesFromPath("/home/niklaus/Music/"):
	#	print line.getFileName()
	#f7 = File.File(fileName="documentation.odt", path="/home/niklaus/Documents/", tags=['libreoffice', 'odt', 'document', 'projectbrowser', ])
	#print db.getTagsToFile(f7)
	#db.updateFile(f7)
	#print db.getTagsToFile(f7)
	#print "Tags in the DB: "
	#print '='*10
	#print db.getAllTags()
	#f8 = File.File(fileName="documentation.tex", path="/home/niklaus/Documents/LaTeX/", tags=['document', 'projectbrowser', 'latex', ])
	#db.renameFile(f7, f8)
	#print '='*10
	#for line in db.getFilesFromPath("/home/niklaus/Documents/LaTeX/"):
	#	print line.getFileName()
	#db.updateFile(f8)
	#print db.getTagsToFile(f8)
	#print '='*10
	#print db.getTagsToFile(f7)


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
	#TODO addTagToFile
