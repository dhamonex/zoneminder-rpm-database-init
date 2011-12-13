# -*- coding: utf-8 -*- 

import ConfigParser

class Configuration:
  """ Configuration reader and writer for zm_database_init script """
  def __init__(self, filename):
    self.filename = filename
    self.config = ConfigParser.SafeConfigParser
  
  def readConfiguration(self):
    self.config.read(filename)
    
