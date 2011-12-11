#!/usr/bin/python
# -*- coding: utf-8 -*- 


# zm_database_init version 2.0.0
#
# Author: Monex
# this script is under the same license as the package itself.
#
# Please submit bugfixes or comments to monex@liquid-co.de

import os.path, os, string
import re, sys, getopt
import posix, shutil, getpass
import argparse

class ZmConfigFileHandler:
  """ Handler for reading writing and checking ZoneMinder configuration files """
  def __init__(self, filename = ""):
    self.filename = filename
    self.filecontent = []
  
  def readConfigFile(self, filename = ""):
    """ read the configuration from file """
    if filename != "":
      self.filename = filename
    
    with open(self.filename, "r") as openfile:
      self.filecontent = openfile.readlines()
  
  def writeConfigFile(self):
    """ writes changes to the original config file """
    with open(self.filename, "w") as openfile:
      openfile.write(string.join(self.filecontent, ""))
  
  def changeConfigValue(self, option, value):
    """ changes the given option in config file to the new given value """
    option_s = re.compile(option)
    if option[-1] != "=": # add '=' when missing
      option += "="
    
    config_copy = self.filecontent
    self.filecontent = []
    
    for line in config_copy:
      line, comment = self._lineWithoutComment(line)
      
      if option_s.search(line):
        line = option + value
      
      self.filecontent.append(line + comment)
  
  @staticmethod
  def _lineWithoutComment(line):
    endpos = line.find("#")
    if endpos >= 0:
      return line[:endpos], line[endpos:]
    
    endpos = line.find(";")
    if endpos >= 0:
      return line[:endpos], line[endpos:]
    
    return line, ""

def main():
  parser = argparse.ArgumentParser(description = "Handles Database installation and update for ZoneMinder Installations")
  parser.add_argument("-m", "--mysql_host", dest = "mysql_host", default = "localhost", metavar = "MYSQL_HOST",
                      help="Specify a different MYSQL_HOST (default: localhost)")
  parser.add_argument("--non-interactive", dest = "non_interactive", 
                      action = "store_true",
                      help = "Run in non interactive mode for upgrades only (default: false)")

  args = parser.parse_args()
  
  zmcfg = ZmConfigFileHandler("zm.conf")
  zmcfg.readConfigFile()
  zmcfg.changeConfigValue("ZM_VERSION", "1.26.0")
  zmcfg.writeConfigFile()
  

if __name__ == "__main__":
  main()