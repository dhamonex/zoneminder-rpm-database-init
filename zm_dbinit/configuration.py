# -*- coding: utf-8 -*- 

import ConfigParser
import os.path

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
    if os.path.isfile(self.filename):
      self.config.read(self.filename)
    else:
      self.setDefaults()
  
  def setDefaults(self):
    self.config.add_section(Configuration.MySection)
    self.config.set(Configuration.MySection, "database-initialized", "no")
    self.config.set(Configuration.MySection, "allow-execution-only-as-root", "yes")
    self.config.set(Configuration.MySection, "mysql-host", "localhost")
    self.config.set(Configuration.MySection, "mysql-bin", "/usr/bin/mysql")
    
    
    self.config.add_section(Configuration.ZmSection)
    self.config.set(Configuration.ZmSection, "lock-file", "/usr/share/zm/lock")
    self.config.set(Configuration.ZmSection, "data-install-path", "/usr/share/zm")
    self.config.set(Configuration.ZmSection, "configuration-file", "/etc/zm.conf")
    
    self.configModified = True
  
  def zmLockFile(self):
    return self.config.get(Configuration.ZmSection, "lock-file")
  
  def zmPath(self):
    return self.config.get(Configuration.ZmSection, "data-install-path")
  
  def zmConfigFile(self):
    return self.config.get(Configuration.ZmSection, "configuration-file")
  
  def databaseInitialized(self):
    return self.config.getboolean(Configuration.MySection, "database-initialized")
  
  def setDatabaseInitialized(self, initialized):
    value = "no"
    if initialized:
      value = "yes"
    self.config.set(Configuration.MySection, "database-initialized", value)
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
  
  def mysqlBin(self):
    return self.config(Configuration.MySection, "mysql-bin")
  
  def checkConfigUpdate(self):
    if self.configModified:
      with open(self.filename, "w") as f:
        self.config.write(f)
      
      self.configModified = False
  
  def __exit__(self, type, value, traceback):
    self.checkConfigUpdate()
  
  def __del__(self):
    self.checkConfigUpdate()
    
    
