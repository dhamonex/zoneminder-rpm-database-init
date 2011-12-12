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

########## important settings ################
VERSION = "1.25.0"# current version of zm

ZM_PATH ="/usr/share/zm" # path to zm shared dir

ZM_CONFIG = "/etc/zm.conf"
########## /important settings ###############

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
  
  def readOptionValue(self, option):
    """ Searches for the given Option and returns it """
    option_s = re.compile(option + "\s*=\s*(\S+)")
    
    for line in self.filecontent:
      line, comment = self._lineWithoutComment(line)
      
      what = option_s.match(line)
      if what:
        return what.group(1).strip()
    
    raise NameError("Option not found: " + option)
  
  @staticmethod
  def _lineWithoutComment(line):
    """ Splits comment from line """
    endpos = line.find("#")
    if endpos >= 0:
      return line[:endpos], line[endpos:]
    
    endpos = line.find(";")
    if endpos >= 0:
      return line[:endpos], line[endpos:]
    
    return line, ""

class UserPrompt:
  """ Helper class for handling user prompt """
  def __init__(self, non_interactive):
    self.non_interactive = non_interactive
    self.failurecount = 0
  
  def okToContinue(self, question, defaultAnswer = True):
    """ asks the user if it is OK to continue """
    
    if defaultAnswer:
      selection = " [Y/n]: "
    else:
      selection = " [y/N]: "
    
    if self.non_interactive:
      if defaultAnswer:
        answer = "Y"
      else:
        answer = "N"
        
      print question + selection + " " + answer
      return defaultAnswer
      
    proceed = raw_input(question + selection)
    
    if proceed == "":
      return defaultAnswer
    elif proceed.lower() == "y" or proceed.lower() == "yes":
      return True
    
    return False
  
  def askForPassword(self, text, retype = False):
    """ Asks the user for password input """
    if self.non_interactive:
      raise RuntimeError("Asking for password is not allowed in non interactive mode!!")
    
    passwd = getpass.getpass(text + ": ")
    
    if retype:
      t_pass = getpass.getpass("retype password: ")
    else:
      return passwd
    
    if passwd != t_pass and self.failurecount < 3:
      print "Password mismatch please try again"
      self.askForPassword(text, retype)
    else:
      raise RuntimeError("Too many user interaction errors")
    
    return passwd
    
  
def initializeDatabase(database_host):
  """ The main execute """
  pass
    
def main():
  parser = argparse.ArgumentParser(description = "Handles Database installation and update for ZoneMinder Installations")
  parser.add_argument("-m", "--mysql_host", dest = "mysql_host", default = "localhost", metavar = "MYSQL_HOST",
                      help="Specify a different MYSQL_HOST (default: localhost)")
  parser.add_argument("--non-interactive", dest = "non_interactive", 
                      action = "store_true",
                      help = "Run in non interactive mode for upgrades only (default: false)")

  args = parser.parse_args()
  prompt = UserPrompt(args.non_interactive)
  
  try:
    print "INFO: when db is correctly installed and you just reinstalled rpm, then answer all questions with 'n'"
  
    if os.path.isfile(ZM_PATH + "/lock"):
      run_stuff(database_host)
    else:
      if prompt.okToContinue("no lockfile found, proceed anyway?", False):
        initializeDatabase(database_host)
  
  except RuntimeError as e:
    print e
    print "exiting"
    sys.exit(0)
  
  except KeyboardInterrupt:
    print "Interrupted exiting"
    sys.exit(0)
  
  zmcfg = ZmConfigFileHandler("zm.conf")
  zmcfg.readConfigFile()
  print zmcfg.readOptionValue("ZM_VERSION")
  

if __name__ == "__main__":
  main()