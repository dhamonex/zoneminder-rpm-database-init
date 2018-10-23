# -*- coding: utf-8 -*- 

import configparser
import os.path, shutil, os

class MySQLConfiguration:
  """ Handles MySQL Configuration file """
  
  ClientSection = "client"
  
  def __init__(self, userprompt, mysqlConfigFile):
    self.configfile = mysqlConfigFile
    
    self.config = configparser.SafeConfigParser()
    self.prompt = userprompt
  
  def readConfigIfExists(self):
    if os.path.isfile(self.configfile):
      self.config.read(self.configfile)
      return True
    
    return False
  
  def backupOldConfigFileIfExists(self):
    if os.path.isfile(self.configfile):
      shutil.copy(self.configfile, self.configfile + ".backup")
      print("copied old " + self.configfile + " to " + self.configfile + ".backup")
  
  def checkFile(self):
    if not self.readConfigIfExists():
      self.createConfigFile()
    
    try:
      user = self.config.get(MySQLConfiguration.ClientSection, "user")
      password = self.config.get(MySQLConfiguration.ClientSection, "password")
      
      if user == "" or password == "":
        self.createConfigFile()
      
    except configparser.Error:
      self.createConfigFile()
    
  def createConfigFile(self):
    self.readConfigIfExists()
    self.backupOldConfigFileIfExists()
    
    self.config.add_section(MySQLConfiguration.ClientSection)
    self.config.set(MySQLConfiguration.ClientSection, "user", "root")
    self.config.set(MySQLConfiguration.ClientSection, "password", self.prompt.askForPassword("Enter mysql root password"))
    
    with open(self.configfile, "w") as openFile:
      self.config.write(openFile)
    
    print("generated/updated " + self.configfile)
  
