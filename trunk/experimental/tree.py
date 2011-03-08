#!/usr/bin/python
# -*- coding: latin-1 -*-
import os;
startpath = os.getcwd() 
files = os.listdir(startpath)
deep = 0

def additem(path):
    print "",
    for i in range(deep/2):
        print "│", "",
    print "├─" + path

def listfolder(path):
    global deep
    if (path != startpath):
        additem (os.path.basename(path))
        deep += 2
    if (not path.endswith("/")):
	path += "/"
    tmp = os.listdir(path)
    for i in tmp:
        if (os.path.isdir(path + i)): 
            listfolder(path + i)
        else:
            additem(i)
    if (path != startpath):
        deep -= 2
    

print os.path.basename(startpath)
listfolder(startpath)
