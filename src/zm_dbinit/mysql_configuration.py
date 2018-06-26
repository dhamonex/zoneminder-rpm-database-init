# -*- coding: utf-8 -*- 

import configparser
import os.path, shutil, os

class MySQLConfiguration:
  """ Handles MySQL Configuration file """
  
  ClientSection = "client"
  ConfigFile = ".my.cnf"
  
  def __init__(self, userprompt):
    if "HOME" not in os.environ:
      # fallback if no environment available
      # set HOME environment for subprocess calls
      os.environ["HOME"] = "/root"
    
    self.configfile = os.environ["HOME"] + "/" + MySQLConfiguration.ConfigFile
    
    self.config = configparser.SafeConfigParser()
    self.prompt = userprompt
  
  def readConfigIfExists(self):
    if os.path.isfile(self.configfile):
      self.config.read(self.configfile)
      return True
    
    return False
  
  def backupOldConfigFileIfExists(self):
    if os.path.isfile(self.configfile):
      shutil.copy(self.configfile, os.environ["HOME"] + "/" + MySQLConfiguration.ConfigFile + ".backup")
      print("copied old " + MySQLConfiguration.ConfigFile + " to " + MySQLConfiguration.ConfigFile + ".backup")
  
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
    
    print("generated/updated ~/" + MySQLConfiguration.ConfigFile)
  
