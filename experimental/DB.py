#!/usr/bin/python

#File:			DB.py
#Description:		Zugriff auf die DB
#Author:		Kaleb Tschabold
#Creation Date:		29.3.2011
#
#History: 		--Version--	--Date--	--Activities--
#			0.1		29.03.2011	Grundfunktionalitaeten werden erstellt
#			0.2		21.04.2011	Added a few methods to read some data from the DB

import sqlite3
import File

class DB:
  	connection	= None
	cursor		= None
	dbpath		= None
	def __init__(self, dbpath):
		self.dbpath	= dbpath
		self.establishConnection()

	def establishConnection(self):
	  	self.connection	= sqlite3.connect(self.dbpath)
		self.cursor	= self.connection.cursor()
		print "connection established"
	
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
	  	ret_value	= []
		for row in li:
			tagQuery	= "SELECT tagnames.tagname FROM files LEFT JOIN file_tag_relations, tagnames ON (files.fid = file_tag_relations.fk_fid AND file_tag_relations.fk_tagid = tagnames.tagid) WHERE files.fid = '%d'" % (row[0], )
			self.cursor.execute(tagQuery)
			tagLi		= self.cursor.fetchall()
			tagList		= self.changeList(tagLi)

			fi	= File.File(fileName=row[1], path=row[2], backup=row[3], tags=tagList)
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


if __name__ == "__main__":
   	print "TEST"
	db = DB("/home/niklaus/.project-browser/db")
	db.test(File.File())
	#db.test(1)
	out = db.executeQuerry("SELECT * FROM files")
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
	print db.getAllTags()
