# -*- coding: utf-8 -*- 

import ConfigParser

class Configuration:
  """ Configuration reader and writer for zm_database_init script """
  
  # static members
  MySection = "ZmDatabaseInit"
  ZmSection = "ZoneMinder"
  
  def __init__(self, filename):
    self.filename = filename
    self.config = ConfigParser.SafeConfigParser()
    self.configModified = False
    
    self.readConfiguration()
  
  def __enter__(self):
    return self
  
  def readConfiguration(self):
    self.config.read(self.filename)
  
  def zmLockFile(self):
    return self.config.get(Configuration.ZmSection, "lock-file")
  
  def zmPath(self):
    return self.config.get(Configuration.ZmSection, "data-install-path")
  
  def zmConfigFile(self):
    return self.config.get(Configuration.ZmSection, "configuration-file")
  
  def databaseInitialized(self):
    self.config.getboolean(Configuration.MySection, "database-initialized")
  
  def setDatabaseInitialized(self, initialized):
    self.config.set(MySection, "database-initialized", initialized)
    self.configModified = True
  
  def rootUserCheck(self):
    return self.config.getboolean(Configuration.MySection, "allow-execution-only-as-root")
  
  def mysqlHost(self):
    return self.config.get(Configuration.MySection, "mysql-host")
  
  def setMysqlHost(self, hostname):
    if self.mysqlHost() == hostname:
      return
    
    self.config.set(MySection, "mysql-host", hostname)
    self.configModified = True
  
  def checkConfigUpdate(self):
    if self.configModified:
      with open(self.filename, "w") as f:
        self.config.write(f)
      
      self.configModified = False
  
  def __exit__(self, type, value, traceback):
    self.checkConfigUpdate()
  
  def __del__(self):
    self.checkConfigUpdate()
    
    
