#!/usr/bin/python
# -*- coding: utf-8 -*- 


# zm_database_init version 2.0.0
#
# Author: Monex
# this script is under the same license as the package itself.
#
# Please submit bugfixes or comments to monex@liquid-co.de

import os.path, os
import argparse

from zm_dbinit.userprompt import UserPrompt
from zm_dbinit.zm_config_reader import ZmConfigError, ZmConfigFileHandler

########## important settings ################
VERSION = "1.25.0"# current version of zm

ZM_PATH ="/usr/share/zm" # path to zm shared dir

ZM_CONFIG = "/etc/zm.conf"
########## /important settings ###############
    
  
def initializeDatabase(database_host):
  """ The main execute """
  zmcfg = ZmConfigFileHandler("zm.conf")
  zmcfg.readConfigFile()
  print zmcfg.readOptionValue("ZM_VERSION")
    
def main():
  parser = argparse.ArgumentParser(description = "Handles Database installation and update for ZoneMinder Installations")
  parser.add_argument("-m", "--mysql_host", dest = "mysql_host", default = "localhost", metavar = "MYSQL_HOST",
                      help="Specify a different MYSQL_HOST (default: localhost)")
  parser.add_argument("-f", "--config-file", dest = "config_file", default = "/etc/zm_database_init.conf", 
                      metavar = "FILE",
                      help="Specify a different config FILE (default: /etc/zm_database_init.conf)")
  parser.add_argument("--non-interactive", dest = "non_interactive", 
                      action = "store_true",
                      help = "Run in non interactive mode for upgrades only (default: false)")

  args = parser.parse_args()
  prompt = UserPrompt(args.non_interactive)
  database_host = args.mysql_host
  
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
    sys.exit(1)
  
  except ZmConfigError as e:
    print "Error", e
    sys.exit(1)
  
  except KeyboardInterrupt:
    print "Interrupted exiting"
    sys.exit(0)
  

if __name__ == "__main__":
  main()