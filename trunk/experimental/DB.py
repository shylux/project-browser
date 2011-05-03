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

	def establishConnection(self):
	  	print self.dbpath
	  	self.connection	= sqlite3.connect(self.dbpath,check_same_thread = False)
		self.cursor	= self.connection.cursor()
		print "connection established"
		#Check wether the tables in the DB exist. If they don't, we'll create 'em
		self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='files'")
		if len(self.cursor.fetchall()) != 1:
			print "DB's empty. Creating tables"
			self.createDB()

	def fileInDB(self, fi):
	  	"""Checks wether a files is in the db or not"""
		checkQuery = "SELECT files.filename FROM files WHERE files.filename = '%s' AND files.path = '%s'" % (fi.getFileName(), fi.getPath(), )
		self.cursor.execute(checkQuery)
		value = self.cursor.fetchall()

		if len(value) > 0:
			return True
		else:
		  	return False

	def executeQuerry(self, querry):
		self.cursor.execute(querry)
		return self.cursor.fetchall()

	def __changeList(self, li):
		ret_value	= []
		for row in li:
			ret_value.append(row[0])
		return ret_value

	def __connectTagsToFile(self, tags, fid):
			tags = list(set(tags))	#remove duplicates from list
			for row in tags:
				tagQuery = "INSERT OR IGNORE INTO tagnames (tagname, backup) VALUES ('%s', 'False')" % (row, )
				print tagQuery
				self.cursor.execute(tagQuery)

				idQuery	= "SELECT tagid FROM tagnames WHERE tagname = '%s'" % (row, )
				self.cursor.execute(idQuery)
				res = self.cursor.fetchall()

				relQuery = "INSERT INTO file_tag_relations(fk_fid, fk_tagid) VALUES ('%s', '%s')" % (fid, res[0][0], )
				self.cursor.execute(relQuery)

			self.connection.commit()
	

	def __generateFilesArray(self, li):
	  	"""Takes the result from SELECT * FROM files... statement.
		Then gets for each of the files the corresponding tags, and puts it all together
		into a File.py object"""
	  	ret_value	= []
		for row in li:
			tagQuery	= "SELECT tagnames.tagname FROM files LEFT JOIN file_tag_relations, tagnames ON (files.fid = file_tag_relations.fk_fid AND file_tag_relations.fk_tagid = tagnames.tagid) WHERE files.fid = '%d'" % (row[0], )
			self.cursor.execute(tagQuery)
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
			print old_tags
			new_tags = fi.getTags()
			print new_tags
			for row in old_tags:
				try:
					#remove all occurences of old tags from the new tag array, so only new tags are left
					new_tags = filter (lambda a: a != row, new_tags)
				except:
					print "Error while removing element from old_tags"
			print new_tags
			#Following three lines were moved out of the if statement in order to be able to use fid for the remove thing
			fidQuery = "SELECT files.fid FROM files WHERE files.filename = '%s' AND files.path = '%s'" % (fi.getFileName(), fi.getPath())
			self.cursor.execute(fidQuery)
			fid = self.cursor.fetchall()[0][0]
			if len(new_tags) > 0:
				self.__connectTagsToFile(new_tags, fid)
			else:
				print "No new tags, won't do anything"

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
				print deprecatedTags
				#OK, I know that this is DAMNED UGLY, but I can't see any other way for getthing rid of the god damned stupid u in front of each element of the list
				dT = ""
				for line in deprecatedTags:
					print str(line)
					dT = dT + "'" + line + "'" + ", "
				#remove , and space at the end
				dT = dT[:-2]
				print dT
				delTagQuery = "DELETE FROM file_tag_relations WHERE fk_tagid IN (SELECT tagid FROM tagnames WHERE tagname IN (%s)) AND fk_fid = '%s'" % (dT, fid, )
				print delTagQuery
				self.cursor.execute(delTagQuery)
				self.connection.commit()
		else:
			print "File not yet in DB, will run addFile instead"
			self.addFile(fi)
				
	     	
	def getTagsToFile(self, _file):
		li		= None
	  	query	= "SELECT tagnames.tagname FROM files LEFT JOIN file_tag_relations, tagnames ON (files.fid = file_tag_relations.fk_fid AND file_tag_relations.fk_tagid = tagnames.tagid) WHERE path = '%s' AND filename = '%s'" % (_file.getPath(), _file.getFileName())
		self.cursor.execute(query)
		li	= self.cursor.fetchall()
		return self.__changeList(li)

	def getFilesFromPath(self, path):
		ret_value	= []
		li		= None

		query	= "SELECT * FROM files WHERE path = '%s'" % (path, )
		self.cursor.execute(query)
		li	= self.cursor.fetchall()
		return self.__generateFilesArray(li)

	def getFilesFromTag(self, tag):
		ret_value	= []
		li		= None
		ids		= []

		query	= "SELECT files.* FROM files LEFT JOIN file_tag_relations, tagnames ON (files.fid = file_tag_relations.fk_fid AND file_tag_relations.fk_tagid = tagnames.tagid) WHERE tagnames.tagname = '%s'" % (tag, )
		self.cursor.execute(query)
		li	= self.cursor.fetchall()
		return self.__generateFilesArray(li)

	def getAllTags(self):
		self.cursor.execute("SELECT tagname FROM tagnames")
		li = self.cursor.fetchall()
		return self.__changeList(li)

	def createDB(self):
	  	self.cursor.execute("CREATE TABLE files(fid INTEGER PRIMARY KEY, filename TEXT, path TEXT, backup BOOLEAN, isdir BOOLEAN)")
		self.cursor.execute("CREATE TABLE tagnames(tagid INTEGER PRIMARY KEY, tagname TEXT UNIQUE , backup BOOLEAN)")
		self.cursor.execute("CREATE TABLE file_tag_relations(relid INTEGER PRIMARY KEY, fk_fid INTEGER, fk_tagid INTEGER)")
		self.connection.commit()

	def addFile(self, fi):
		#IMPORTANT: For this to work, the field tagnames.tagname has to be marked as UNIQUE!
		#Otherwise, attempts to insert tags might cause trouble!
		if not self.fileInDB(fi):
			query = "INSERT INTO FILES (filename, path, backup, isdir) VALUES ('%s', '%s', '%s', '%s')" % (fi.getFileName(), fi.getPath(), fi.getBackup(), fi.getIsDir())
			self.cursor.execute(query)
			fid	= self.cursor.lastrowid
			self.connection.commit();
			self.__connectTagsToFile(fi.getTags(), fid)
		else:
			print "File already in DB, won't add it again, will run updateFile instead!"
			self.updateFile(fi)

	def removeFile(self, fi):
		idQuery = "SELECT files.fid FROM files WhERE files.path = '%s' AND files.filename = '%s'" % (fi.getPath(), fi.getFileName())
		self.cursor.execute(idQuery)
		fid = self.cursor.fetchall()[0][0]
		delFileQuery = "DELETE FROM files WHERE files.fid = '%s'" % (fid, )
		self.cursor.execute(delFileQuery)
		self.connection.commit()
		delTagConQuery = "DELETE FROM file_tag_relations WHERE file_tag_relations.fk_fid = '%s'" % (fid, )
		self.cursor.execute(delTagConQuery)
		self.connection.commit()
		delTagQuery = "DELETE FROM tagnames WHERE tagnames.tagid NOT IN (SELECT file_tag_relations.fk_tagid FROM file_tag_relations)"
		self.cursor.execute(delTagQuery)
		self.connection.commit()

	def addTagToFile(self, fi, tag):
		if self.fileInDB(fi):
			idQuery = "SELECT files.fid FROM files WHERE files.filename = '%s' AND files.path = '%s'" % (fi.getFileName(), fi.getPath())
			self.cursor.execute(idQuery)
			fid = self.cursor.fetchall()[0][0]
			self.__connectTagsToFile([tag, ], fid)

	def addTag(self, tag):
		query = "INSERT OR IGNORE INTO tagnames (tagname, backup) VALUES ('%s', 'False')" % (tag, )
		self.cursor.execute(query)
		self.connection.commit()

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
	db = DB("testdb")
	f1 = File.File(fileName="test.txt", path="/home/niklaus/", tags=['test', 'projectbrowser', ])
	f2 = File.File(fileName="cc.ogg", path="/home/niklaus/Music/", tags=['music', 'ogg', 'creative commons', ])
	f3 = File.File(fileName="ozzed.ogg", path="/home/niklaus/Music/", tags=['music', 'ogg', 'creative commons', 'ozzed', '8bit', 'chiptune', ])
	f4 = File.File(fileName="evil.mp3", path="/home/niklaus/Music/", tags=['music', 'mp3', 'proprietary', ])
	f5 = File.File(fileName="documentation.odt", path="/home/niklaus/Documents/", tags=['libreoffice', 'odt', 'test', ])
	db.addFile(f1)
	db.addFile(f2)
	db.addFile(f3)
	db.addFile(f4)
	db.addFile(f5)
	print db.getAllTags()
	for line in db.getFilesFromPath("/home/niklaus/Music/"):
		print line.getFileName()
	f6 = File.File(fileName="documentation.odt", path="/home/niklaus/Documents/", tags=['libreoffice', 'odt', 'test', 'document', 'projectbrowser', 'random', ])
	db.updateFile(f6)
	print db.getAllTags()
	for line in db.getFilesFromPath("/home/niklaus/Music/"):
		print line.getFileName()
	f7 = File.File(fileName="documentation.odt", path="/home/niklaus/Documents/", tags=['libreoffice', 'odt', 'document', 'projectbrowser', ])
	db.updateFile(f7)
	print db.getTagsToFile(f7)
