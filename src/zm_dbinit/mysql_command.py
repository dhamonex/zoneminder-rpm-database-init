# -*- coding: utf-8 -*- 

from .mysql_configuration import *
from subprocess import Popen, PIPE

class MySQLCommandError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

class MySQLCommand:
  """ Class for interaction with MySQL """
  
  def __init__(self, userprompt, mysqlbin, mysqlhost):
    self.mysqlbin = mysqlbin
    self.mysqlhost = mysqlhost
    self.userprompt = userprompt
    
  def _executeCommand(self, command):
    process = Popen(command, stderr=PIPE, shell=True)
    out, err = process.communicate()
    
    if process.returncode != 0:
      raise MySQLCommandError(command + " : " + err)
  
  def _dumpDataIn(self, inputFile):
    command = self.mysqlbin + " < " + inputFile
    self._executeCommand(command)
  
  def _executeStatement(self, command):
    statement = """echo " """ + command + """ " | """ + self.mysqlbin
    self._executeCommand(statement)
  
  def checkConfiguration(self):
    config = MySQLConfiguration(self.userprompt)
    config.checkFile()
  
  def createDatabase(self, databasefile):
    if self.userprompt.okToContinue("run mysql command to create db as user root?", True, interaction_required=True):
      self._dumpDataIn(databasefile)
  
  def createZmUser(self):
    if self.userprompt.okToContinue("create user zm_admin for zoneminder?", True):
      passwd = self.userprompt.askForPassword("enter new passwd for user zm_admin", True)
      self._executeStatement("GRANT USAGE ON * . * TO 'zm_admin'@'" + self.mysqlhost + "' IDENTIFIED BY '" + passwd + "' WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0; GRANT SELECT , INSERT , UPDATE , DELETE ON zm . * TO 'zm_admin'@'" + self.mysqlhost + "';")
      
      return passwd
    
    return None
  
  def grantAllPriviligesOnZmDatabase(self, zmdb, zmuser):
    print("grant all priviliges on zm database for user %s" % zmuser)
    self._executeStatement("GRANT ALL PRIVILEGES ON " + zmdb +". * TO '" + zmuser +"'@'" + self.mysqlhost +"';")
  
  def restoreDefaultPriviligesOnZmDatabase(self, zmdb, zmuser):
    print("restoring default priviliges on zm database for user " + zmuser)
    self._executeStatement("REVOKE ALL PRIVILEGES ON " + zmdb +". * FROM '" + zmuser +"'@'" + self.mysqlhost +"'; GRANT SELECT , INSERT , UPDATE , DELETE ON zm . * TO '" + zmuser + "'@'" + self.mysqlhost + "';")
    
