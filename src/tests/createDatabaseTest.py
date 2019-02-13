#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
import os
from unittest.mock import patch

from zm_dbinit.configuration import Configuration
from zm_dbinit.databaseinit import DatabaseInit
from zm_dbinit.userprompt import UserPrompt

class CreateDatabaseTestCase(unittest.TestCase):
  
  def setUp(self):
    self.config = Configuration("tests/testConfigs/zm_database_init.conf")
    self.prompt = UserPrompt(True)
    
    self.dbinit = DatabaseInit(self.prompt, self.config)
    
  @patch("os.path.isfile")
  def testLockFile(self, isFileMock):
    isFileMock.return_value = True
    
    self.assertTrue(self.config.zmLockFile() == "/usr/share/zoneminder/lock")
    self.dbinit.checkLockFile()
    
    assert isFileMock is os.path.isfile
    isFileMock.assert_called_once_with("/usr/share/zoneminder/lock")
    
   
  @patch("zm_dbinit.configuration.Configuration", autospec = True)
  @patch("zm_dbinit.zm_config_reader.ZmConfigFileHandler", autospec = True)
  @patch("zm_dbinit.userprompt.UserPrompt", autospec = True)
  @patch("zm_dbinit.mysql_command.MySQLCommand", autospec = True)
  def testCreateDatabase(self, createDatabaseMock, userPromptMock, zmConfigMock, configMock):
    createDatabaseMock.createZmUser.return_value = "testpass"
    
    userPromptMock.okToContinue.return_value = True
    
    configMock.databaseInitialized.return_value = False
    configMock.createDatabaseSqlFile.return_value = self.config.createDatabaseSqlFile()
    configMock.mysqlHost.return_value = self.config.mysqlHost()
    
    zmConfigMock.readOptionValue.return_value = self.config.mysqlHost()
    
    self.dbinit.mysql = createDatabaseMock
    self.dbinit.userprompt = userPromptMock
    self.dbinit.zmconf = zmConfigMock
    self.dbinit.config = configMock
    
    self.dbinit.createDatabase()
    
    createDatabaseMock.createDatabase.assert_called_once_with(self.config.createDatabaseSqlFile())
    createDatabaseMock.createZmUser.assert_called_once()
    
    zmConfigMock.changeConfigValue.assert_called_once_with("ZM_DB_PASS", "testpass")
    zmConfigMock.writeConfigFile.assert_called_once()
    
    configMock.setDatabaseInitialized.assert_called_once_with(True)
    
    
if __name__ == "__main__":
  unittest.main()
