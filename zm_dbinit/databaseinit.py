# -*- coding: utf-8 -*-

import os.path, posix
from userprompt import UserPrompt
from zm_config_reader import ZmConfigFileHandler
from configuration import *
from mysql_command import MySQLCommand
from zm_update import ZmUpdate, ZmUpdateError

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
      
    if self.config.mysqlHost() != self.zmconf.readOptionValue("ZM_DB_HOST") and \
    self.userprompt.okToContinue("should the config file updated with new db host?", True):
      self.zmconf.changeConfigValue("ZM_DB_HOST", self.config.mysqlHost())
    
    self.zmconf.writeConfigFile()
    
    self.config.setDatabaseInitialized(True)
    
    print "database successfully initialized"
    print "you can now start ZonMinder with rczmstart or systemctl start zm.service"
  
  def checkZmPath(self):
    zmPath = self.zmconf.readOptionValue("ZM_PATH_BUILD")
    if self.config.zmPath() == zmPath:
      return
    
    print "found wrong ZM_PATH_BUILD path in config file could not perform db upgrade"
    if self.userprompt.okToContinue("should it be updated?", True):
      self.zmconf.changeConfigValue("ZM_PATH_BUILD", self.config.zmPath())
      print "ZM_PATH_BUILD set to " + self.config.zmPath()
    else:
      print "WARNING: update may fail when ZM_PATH_BUILD not set to " + self.config.zmPath()
  
  def executeZmUpdate(self, toVersion, fromVersion):
    print "updating config file version string"
    self.zmconf.changeConfigValue("ZM_VERSION", toVersion)
    self.zmconf.writeConfigFile()
    
    update = ZmUpdate(self.config.zmUpdateScriptPath(), self.config.zmUpdateBackupDatabase())
    update.updateFromVersion(fromVersion)
  
  def undoConfigFileVersionUpdate(self, version):
    print "undo config file version string changes"
    self.zmconf.changeConfigValue("ZM_VERSION", version)
    self.zmconf.writeConfigFile()

  def updateDatabase(self, toVersion, fromVersion):
    print "when update fails or you are not upgrading from"
    print "previous rpm version please ensure that the ZM_PATH_BUILD is set to"
    print self.config.zmPath() + " to find the database update skripts\n"
    
    print "when done upgrade using zmupdate.pl before then answer this with n"
    if not self.userprompt.okToContinue("do you want to perform db update?", True):
      return
      
    self.checkZmPath()
    
    zmDbUser = self.zmconf.readOptionValue("ZM_DB_USER")
    zmDb = self.zmconf.readOptionValue("ZM_DB_NAME")
    
    try:
      self.mysql.grantAllPriviligesOnZmDatabase(zmDb, zmDbUser)
    
      # execute zm_update.pl
      self.executeZmUpdate(toVersion, fromVersion)
    
      self.mysql.restoreDefaultPriviligesOnZmDatabase(zmDb, zmDbUser)
    
    except Exception:
      self.undoConfigFileVersionUpdate(fromVersion)
      self.mysql.restoreDefaultPriviligesOnZmDatabase(zmDb, zmDbUser)
      raise
    except KeyboardInterrupt:
      self.undoConfigFileVersionUpdate(fromVersion)
      self.mysql.restoreDefaultPriviligesOnZmDatabase(zmDb, zmDbUser)
      raise
    
    
  def rootUserCheck(self):
    if posix.getuid() != 0 and self.config.rootUserCheck():
      raise RuntimeError("User root needed to execute database init")
  
  def initializeDatabase(self):
    print "INFO: when db is correctly installed and you just reinstalled rpm, then answer all questions with 'n'"
    
    if not self.checkLockFile():
      return
    
    self.rootUserCheck()
    
    self.mysql.checkConfiguration()
    
    zmConfigVersion = self.zmconf.readOptionValue("ZM_VERSION")
    
    if self.getInstalledVersion() == zmConfigVersion:
      self.createDatabase()
    else:
      self.updateDatabase(self.getInstalledVersion(), zmConfigVersion)
      
    if os.path.isfile(self.config.zmLockFile()):
      print "removing lock file"
      os.remove(self.config.zmLockFile())
    
    