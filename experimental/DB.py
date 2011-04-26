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
	  	self.connection	= sqlite3.connect(self.dbpath)
		self.cursor	= self.connection.cursor()
		print "connection established"
		#Check wether the tables in the DB exist. If they don't, we'll create 'em
		self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='files'")
		if len(self.cursor.fetchall()) != 1:
			print "DB's empty. Creating tables"
			self.createDB()

	def getFilesFromTag(self,tag):
		pass

	def getAllTags(self):
		pass

	def test(self, something):
	  	print something.getTags()
	
	def executeQuerry(self, querry):
		self.cursor.execute(querry)
		return self.cursor.fetchall()

	def changeList(self, li):
		ret_value	= []
		for row in li:
			ret_value.append(row[0])
		return ret_value

	def generateFilesArray(self, li):
	  	"""Takes the result from SELECT * FROM files... statement.
		Then gets for each of the files the corresponding tags, and puts it all together
		into a File.py object"""
	  	ret_value	= []
		for row in li:
			tagQuery	= "SELECT tagnames.tagname FROM files LEFT JOIN file_tag_relations, tagnames ON (files.fid = file_tag_relations.fk_fid AND file_tag_relations.fk_tagid = tagnames.tagid) WHERE files.fid = '%d'" % (row[0], )
			self.cursor.execute(tagQuery)
			tagLi		= self.cursor.fetchall()
			tagList		= self.changeList(tagLi)

			fi	= File.File(fileName=row[1], path=row[2], backup=row[3], isDir=row[4], tags=tagList)
			ret_value.append(fi)
		return ret_value

	     	
	def getTagsToFile(self, _file):
		li		= None

	  	query	= "SELECT tagnames.tagname FROM files LEFT JOIN file_tag_relations, tagnames ON (files.fid = file_tag_relations.fk_fid AND file_tag_relations.fk_tagid = tagnames.tagid) WHERE path = '%s' AND filename = '%s'" % (_file.getPath(), _file.getFileName())
		self.cursor.execute(query)
		li	= self.cursor.fetchall()
		return self.changeList(li)

	def getFilesFromPath(self, path):
		ret_value	= []
		li		= None

		query	= "SELECT * FROM files WHERE path = '%s'" % (path, )
		self.cursor.execute(query)
		li	= self.cursor.fetchall()
		return self.generateFilesArray(li)

	def getFilesFromTag(self, tag):
		ret_value	= []
		li		= None
		ids		= []

		query	= "SELECT files.* FROM files LEFT JOIN file_tag_relations, tagnames ON (files.fid = file_tag_relations.fk_fid AND file_tag_relations.fk_tagid = tagnames.tagid) WHERE tagnames.tagname = '%s'" % (tag, )
		self.cursor.execute(query)
		li	= self.cursor.fetchall()
		return self.generateFilesArray(li)

	def getAllTags(self):
		self.cursor.execute("SELECT tagname FROM tagnames")
		li = self.cursor.fetchall()
		return self.changeList(li)

	def createDB(self):
	  	self.cursor.execute("CREATE TABLE files(fid INTEGER PRIMARY KEY, filename TEXT, path TEXT, backup BOOLEAN, isdir BOOLEAN)")
		self.cursor.execute("CREATE TABLE tagnames(tagid INTEGER PRIMARY KEY, tagname TEXT UNIQUE , backup BOOLEAN)")
		self.cursor.execute("CREATE TABLE file_tag_relations(relid INTEGER PRIMARY KEY, fk_fid INTEGER, fk_tagid INTEGER)")
		self.connection.commit()

	def addFile(self, fi):
		#IMPORTANT: For this to work, the field tagnames.tagname has to be marked as UNIQUE!
		#Otherwise, attempts to insert tags might cause trouble!
		query = "INSERT INTO FILES (filename, path, backup, isdir) VALUES ('%s', '%s', '%s', '%s')" % (fi.getFileName(), fi.getPath(), fi.getBackup(), fi.getIsDir())
		self.cursor.execute(query)
		fid	= self.cursor.lastrowid

		for row in fi.getTags():
			tagQuery = "INSERT OR IGNORE INTO tagnames (tagname, backup) VALUES ('%s', 'false')" % (row, )
			self.cursor.execute(tagQuery)

			idQuery	= "SELECT tagid FROM tagnames WHERE tagname = '%s'" % (row, )
			self.cursor.execute(idQuery)
			res = self.cursor.fetchall()

			relQuery = "INSERT INTO file_tag_relations(fk_fid, fk_tagid) VALUES ('%s', '%s')" % (fid, res[0][0], )
			self.cursor.execute(relQuery)

		self.connection.commit()

	def removeFile(self, fi):
		query = "DELETE FROM files WHERE files.name = '%s' AND files.path = '%s' AND isdir ='%s'" % (fi.getFileName(), fi.getPath(), fi.getIsDir())
		self.cursor.execute(query)
		self.connection.commit()

	def moveFile(self, fi)
		pass

if __name__ == "__main__":
   	print "TEST"
	#db = DB("/home/niklaus/.project-browser/db")
	path = os.path.expanduser("~/.project-browser/db")
	db = DB(path)
	#db.test(File.File())
	#db.test(1)
	fi	= File.File(fileName="name", path="/home/niklaus/", tags=['tag1', 'tag2', 'tagX'], isDir=False)
	#db.addFile(fi)
	li = db.getFilesFromTag("tagX")
	print li[3].getFileName()
	db.removeFile(fi)
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