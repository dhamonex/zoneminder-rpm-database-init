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
    
  def tearDown(self):
    self.config.configModified = False
    
  
  @patch("os.remove")
  @patch("os.path.isfile")
  @patch("zm_dbinit.mysql_command.MySQLCommand", autospec = True)
  def testUpdateDatabaseisCalled(self, createDatabaseMock, isFileMock, fileRemoveMock):
    with patch.object(DatabaseInit, "updateDatabase") as udpateDatabaseMock, \
         patch.object(DatabaseInit, "getInstalledVersion") as getInstallaedVersionMock, \
         patch.object(DatabaseInit, "checkLockFile") as checkLockFileMock, \
         patch.object(DatabaseInit, "rootUserCheck") as rootUserCheckMock, \
         patch.object(DatabaseInit, "getInstalledVersion") as getInstalledVersionMock, \
         patch.object(DatabaseInit, "restartApache") as restartApacheMock:
      getInstallaedVersionMock.return_value = "1.30.4"
      checkLockFileMock.return_value = True
      getInstalledVersionMock.return_value = "1.30.1"
      isFileMock.return_value = True
      
      dbInit = DatabaseInit(self.prompt, self.config)
      dbInit.mysql = createDatabaseMock
      
      #from pudb import set_trace; set_trace()
      dbInit.initializeDatabase()
      
      isFileMock.assert_called_once_with(self.config.zmLockFile())
      fileRemoveMock.assert_called_once_with(self.config.zmLockFile())
      udpateDatabaseMock.assert_called_once_with("1.30.1", "1.30.4")
      restartApacheMock.assert_called_once()
    
    
if __name__ == "__main__":
  unittest.main()
