# -*- coding: utf-8 -*- 

from .mysql_configuration import *
from subprocess import Popen, PIPE, check_output

class MySQLCommandError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

class MySQLCommand:
  """ Class for interaction with MySQL """
  
  def __init__(self, userprompt, mysqlbin, mysqlhost, mysqlconfig):
    self.mysqlbin = mysqlbin
    self.mysqlhost = mysqlhost
    self.mysqlconfig = mysqlconfig
    self.userprompt = userprompt
    
  @staticmethod
  def _executeCommand(command):
    process = Popen(command, stderr=PIPE, shell=True)
    _, err = process.communicate()
    # if isinstance(out, bytes):
    #   out = out.decode('utf-8', errors='replace')
      
    if isinstance(err, bytes):
      err = err.decode('utf-8', errors='replace')
    
    if process.returncode != 0:
      raise MySQLCommandError(command + " : " + err)
  
  def _dumpDataIn(self, inputFile):
    command = self.mysqlbin + " < " + inputFile
    self._executeCommand(command)
  
  def _executeStatement(self, command):
    statement = """echo " """ + command + """ " | """ + self.mysqlbin
    self._executeCommand(statement)
  
  def checkConfiguration(self):
    config = MySQLConfiguration(self.userprompt, self.mysqlconfig)
    config.checkFile()
  
  def createDatabase(self, databasefile):
    if self.userprompt.okToContinue("run mysql command to create db as user root?", True, interaction_required=True):
      self._dumpDataIn(databasefile)
  
  def createZmUser(self):
    if self.userprompt.okToContinue("create user zm_admin for zoneminder?", True):
      passwd = self.userprompt.askForPassword("enter new passwd for user zm_admin", True)
      self._executeStatement("GRANT USAGE ON * . * TO 'zm_admin'@'" + self.mysqlhost + "' IDENTIFIED BY '" + passwd + "' WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0; GRANT SELECT , INSERT , UPDATE , DELETE , TRIGGER ON zm . * TO 'zm_admin'@'" + self.mysqlhost + "';")
      
      return passwd
    
    return None
  
  def zmDatabaseExists(self, zmdb):
    result = check_output(self.mysqlbin + """ --skip-column-names -e "SHOW DATABASES LIKE '""" + zmdb + """'" """, shell = True)
    return result.strip().decode() == zmdb
  
  def grantAllPriviligesOnZmDatabase(self, zmdb, zmuser):
    print("grant all priviliges on zm database for user %s" % zmuser)
    self._executeStatement("GRANT ALL PRIVILEGES ON " + zmdb +". * TO '" + zmuser +"'@'" + self.mysqlhost +"';")
  
  def restoreDefaultPriviligesOnZmDatabase(self, zmdb, zmuser):
    print("restoring default priviliges on zm database for user " + zmuser)
    self._executeStatement("REVOKE ALL PRIVILEGES ON " + zmdb +". * FROM '" + zmuser +"'@'" + self.mysqlhost +"'; GRANT SELECT , INSERT , UPDATE , DELETE, TRIGGER ON zm . * TO '" + zmuser + "'@'" + self.mysqlhost + "';")
    
