#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch, call

from zm_dbinit.configuration import Configuration
from zm_dbinit.databaseinit import DatabaseInit
from zm_dbinit.userprompt import UserPrompt

def getWebPathsSideEffect(option):
  if option == "ZM_PATH_WEB":
    return "/srv/www/htdocs/zm"
  
  elif option == "ZM_PATH_CGI":
    return "/srv/www/cgi-bin"

  raise RuntimeError("Undefined option %s", option)

class CreateDatabaseTestCase(unittest.TestCase):
  
  def setUp(self):
    self.config = Configuration("tests/testConfigs/zm_database_init.conf")
    self.prompt = UserPrompt(True)
    
  def tearDown(self):
    self.config.configModified = False
    
  
  @patch("os.remove")
  @patch("os.path.isfile")
  @patch("zm_dbinit.mysql_command.MySQLCommand", autospec = True)
  def testUpdateDatabaseIsCalled(self, createDatabaseMock, isFileMock, fileRemoveMock):
    with patch.object(DatabaseInit, "updateDatabase") as udpateDatabaseMock, \
         patch.object(DatabaseInit, "checkLockFile") as checkLockFileMock, \
         patch.object(DatabaseInit, "rootUserCheck") as rootUserCheckMock, \
         patch.object(DatabaseInit, "getInstalledVersion") as getInstalledVersionMock, \
         patch.object(DatabaseInit, "restartApache") as restartApacheMock, \
         patch.object(DatabaseInit, "checkWebPath") as checkWebPathMock:
      
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
      
      checkWebPathMock.assert_has_calls([call("ZM_PATH_WEB", self.config.webPath()), 
                                         call("ZM_PATH_CGI", self.config.cgiPath())])
      
      
    
  @patch("zm_dbinit.zm_config_reader.ZmConfigFileHandler", autospec = True)
  def testUpdateConfigPath(self, zmConfigMock):
    zmConfigMock.readOptionValue.side_effect = getWebPathsSideEffect
    
    dbInit = DatabaseInit(self.prompt, self.config)
    dbInit.zmconf = zmConfigMock
    dbInit.checkWebPath("ZM_PATH_WEB", self.config.webPath())
    
    zmConfigMock.changeConfigValue.assert_called_once_with("ZM_PATH_WEB", "/usr/share/zoneminder/www")
    
    
  @patch("zm_dbinit.mysql_command.MySQLCommand", autospec = True)
  def testUpdateDatabase(self, createDatabaseMock):
    with patch.object(DatabaseInit, "checkZmPath") as checkZmPathMock, \
         patch.object(DatabaseInit, "executeZmUpdate") as executeZmUpdateMock, \
         patch.object(DatabaseInit, "symlinkOldEventsDir") as symlinkOldEventsDirMock:
      
      dbInit = DatabaseInit(self.prompt, self.config)
      dbInit.mysql = createDatabaseMock
      
      dbInit.updateDatabase("1.30.1", "1.30.4")
      
      executeZmUpdateMock.assert_called_once()
      symlinkOldEventsDirMock.assert_called_once()
      
      checkZmPathMock.assert_has_calls([call("ZM_PATH_DATA"), call("ZM_PATH_BUILD")])
    
if __name__ == "__main__":
  unittest.main()
