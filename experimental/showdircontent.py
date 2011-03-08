#!/usr/bin/python
import os

path = "/"
files = os.listdir(path)
for item in files:
    if (os.path.isfile(path + item)): 
        print "File: ", item
    if (os.path.isdir(path + item)):
        print "Dir : ", item
