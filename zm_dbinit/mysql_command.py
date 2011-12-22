# -*- coding: utf-8 -*- 

from mysql_configuration import *
from subprocess import Popen, PIPE

class MySQLCommandError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

class MySQLCommand:
  """ Class for interaction with MySQL """
  
  def __init__(self, userprompt, mysqlbin, mysqlhost):
    config = MySQLConfiguration(userprompt)
    self.mysqlbin = mysqlbin
    self.mysqlhost = mysqlhost
    self.userprompt = userprompt
    
    config.checkFile()
    
  def _executeCommand(self, command):
    process = Popen(command, stderr=PIPE)
    process.wait()
    
    if process.returncode != 0:
      raise MySQLCommandError(process.stderr.read())
  
  def _dumpDataIn(self, inputFile):
    command = self.mysqlbin + " < " + inputFile
    self._executeCommand(command)
  
  def _executeStatement(self, command):
    statement = """echo " """ + command + """ " | """ + self.mysqlbin
    self._executeCommand(command)
  
  def createDatabase(self, databasefile):
    if self.prompt.okToContinue("run mysql command to create db as user root?", True, interaction_required=True):
      self._dumpDataIn(databasefile)
  
  def createZmUser(self):
    if self.prompt.okToContinue("create user zm_admin for zoneminder?", True):
      passwd = self.prompt.askForPassword("enter new passwd for user zm_admin", True)
      self._executeStatement("GRANT USAGE ON * . * TO 'zm_admin'@'" + self.mysqlhost + "' IDENTIFIED BY '" + passwd + "' WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0; GRANT SELECT , INSERT , UPDATE , DELETE ON zm . * TO 'zm_admin'@'" + self.mysqlhost + "';")
  
  def grantAllPriviligesOnZmDatabase(self, zmdb, zmuser):
    self._executeStatement("GRANT ALL PRIVILEGES ON " + zmdb +". * TO '" + zmuser +"'@'" + self.mysqlhost +"';")
  
  def restoreDefaultPriviligesOnZmDatabase(self, zmdb, zmsuser):
    self._executeStatement("REVOKE ALL PRIVILEGES ON " + zmdb +". * TO '" + zmuser +"'@'" + self.mysqlhost +"'; GRANT SELECT , INSERT , UPDATE , DELETE ON zm . * TO '" + zmuser + "'@'" + self.mysqlhost + "';")
    