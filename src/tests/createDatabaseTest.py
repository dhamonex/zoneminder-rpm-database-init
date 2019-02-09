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
    prompt = UserPrompt(False)
    
    self.dbinit = DatabaseInit(prompt, self.config)
    
  @patch("os.path.isfile")
  def testLockFile(self, isFileMock):
    isFileMock.return_value = True
    
    self.assertTrue(self.config.zmLockFile() == "/usr/share/zoneminder/lock")
    self.dbinit.checkLockFile()
    
    assert isFileMock is os.path.isfile
    isFileMock.assert_called_once_with("/usr/share/zoneminder/lock")
    
    
if __name__ == "__main__":
  unittest.main()
