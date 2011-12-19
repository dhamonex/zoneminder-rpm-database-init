#!/usr/bin/python
# -*- coding: utf-8 -*- 


# zm_database_init version 2.0.0
#
# Author: Monex
# this script is under the same license as the package itself.
#
# Please submit bugfixes or comments to monex@liquid-co.de

import os.path, os, sys
import argparse

from zm_dbinit.userprompt import UserPrompt
from zm_dbinit.zm_config_reader import ZmConfigError, ZmConfigFileHandler
from zm_dbinit.configuration import *
  
def initializeDatabase(config):
  """ The main execute """
  zmcfg = ZmConfigFileHandler(config.zmConfigFile())
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
  
  try:
    print "INFO: when db is correctly installed and you just reinstalled rpm, then answer all questions with 'n'"
    
    with Configuration(args.config_file) as config:
      config.setMysqlHost(args.mysql_host)
      
      if os.path.isfile(config.zmLockFile()):
        run_stuff(database_host)
      else:
        if prompt.okToContinue("no lockfile found, proceed anyway?", False):
          initializeDatabase(config)
  
  except ZmConfigError as e:
    print "Error in ZoneMinder configuration file: ", e
    sys.exit(1)
  
  except ConfigParser.Error as e:
    print "Error in cofniguration file:", e
    sys.exit(2)
  
  except KeyboardInterrupt:
    print "Interrupted exiting"
    sys.exit(0)
  
  except Exception as e:
    print "Error: ", e
    sys.exit(3)
  
if __name__ == "__main__":
  main()