# -*- coding: utf-8 -*-

import os.path, posix
from userprompt import UserPrompt
from zm_config_reader import ZmConfigFileHandler
from configuration import *
from mysql_command import MySQLCommand

class DatabaseInit:
  def __init__(self, userprompt, config):
    self.userprompt = userprompt
    self.config = config
    self.zmconf = ZmConfigFileHandler(config.zmConfigFile())
    self.zmconf.readConfigFile()
    self.mysql = MySQLCommand(self.userprompt, self.config.mysqlBin(), self.config.mysqlHost())
  
  def checkLockFile(self):
    if os.path.isfile(self.config.zmLockFile()):
      return True
    else:
      return self.userprompt.okToContinue("no lockfile found, proceed anyway?", False)
  
  def getInstalledVersion(self):
    version = ""
    with open(self.config.installedZmVersionFile(), "r") as versionFile:
      version = versionFile.read()
    
    return version.strip()
  
  def createDatabase(self):
    if self.config.databaseInitialized():
      print "database is already installed. if you want to recreate the database drop it manually and change the 'database-initialized' configuration option to 'no'"
      return
    
    self.mysql.createDatabase(self.config.createDatabaseSqlFile())
    password = self.mysql.createZmUser()
    
    if self.userprompt.okToContinue("should the config file updated with the new passwd?", True):
      self.zmconf.changeConfigValue("ZM_DB_PASS", password)
      
    if self.configuration.mysqlHost() != self.zmconf.readOptionValue("ZM_DB_HOST") and \
    self.userprompt.okToContinue("should the config file updated with new db host?", True):
      self.zmconf.changeConfigValue("ZM_DB_HOST", self.configuration.mysqlHost())
    
    self.zmconf.writeConfigFile()
    
    print "database successfully initialized"
    print "you can now start ZonMinder with rczmstart or systemctl start zm.service"
    

  def updateDatabase(self):
    pass
    
  def rootUserCheck(self):
    if posix.getuid() != 0 and self.config.rootUserCheck():
      raise RuntimeError("User root needed to execute database init")
  
  def initializeDatabase(self):
    print "INFO: when db is correctly installed and you just reinstalled rpm, then answer all questions with 'n'"
    
    if not self.checkLockFile():
      return
    
    self.rootUserCheck()
    
    self.mysql.checkConfiguration()
    
    if self.getInstalledVersion() == self.zmconf.readOptionValue("ZM_VERSION"):
      self.createDatabase()
    else:
      self.updateDatabase()
    
    