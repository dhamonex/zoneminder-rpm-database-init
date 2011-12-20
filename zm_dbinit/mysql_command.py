# -*- coding: utf-8 -*- 

from mysql_configuration import *

class MySQLCommand:
  """ Class for interaction with MySQL """
  
  def __init__(self):
    self.config = MySQLConfiguration()
    