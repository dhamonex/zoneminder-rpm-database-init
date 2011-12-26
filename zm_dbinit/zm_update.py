# -*- coding: utf-8 -*- 

from subprocess import Popen, PIPE
import os

class ZmUpdateError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

class ZmUpdate:
  """ Class for handling zm update command """
  
  def __init__(self, zmUpdatePath):
    self.zmUpdatePath = zmUpdatePath
  
  def updateFromVersion(self, fromVersion):
    process = Popen(self.zmUpdatePath + " -version=" + fromVersion, stderr=PIPE, stdout=PIPE, stdin=PIPE, shell=True)
    print "Comm"
    out, err = process.communicate()
    print out, err, "Hallo"
    #process.wait()
    