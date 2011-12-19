# -*- coding: utf-8 -*- 

import ConfigParser

class Configuration:
  """ Configuration reader and writer for zm_database_init script """
  
  # static members
  MySection = "ZmDatabaseInit"
  ZmSection = "ZoneMinder"
  
  def __init__(self, filename):
    self.filename = filename
    self.config = ConfigParser.SafeConfigParser
    self.configModified = False
    
    self.readConfiguration()
  
  def readConfiguration(self):
    self.config.read(filename)
  
  def zmLockFile(self):
    return self.config.get(ZmSection, "lock-file")
  
  def zmPath(self):
    return self.config.get(ZmSection, "data-install-path")
  
  def zmConfigFile(self):
    return self.config.get(ZmSection, "configuration-file")
  
  def databaseInitialized(self):
    self.config.getboolean(MySection, "database-initialized")
  
  def setDatabaseInitialized(self, initialized):
    self.config.set(MySection, "database-initialized", initialized)
    self.configModified = True
  
  def rootUserCheck(self):
    return self.config.getboolean(MySection, "allow-execution-only-as-root")
  
  def mysqlHost(self):
    return self.config.get(MySection, "mysql-host")
  
  def setMysqlHost(self, hostname):
    self.config.set(MySection, "mysql-host", hostname)
    self.configModified = True
  
  def checkConfigUpdate(self):
    if self.configModified:
      with open(self.filename, "w") as f:
        self.config.write(f)
  
  def __del__(self):
    self.checkConfigUpdate()
    
    
