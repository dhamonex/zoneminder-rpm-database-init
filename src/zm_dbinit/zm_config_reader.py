# -*- coding: utf-8 -*- 
import re
import shutil

class ZmConfigError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)
  

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
    """ Writes changes to the original config file. Creates also an backup of old file if write fails """
    self.createConfigFileBackup()
    with open(self.filename, "w") as openfile:
      openfile.write("".join(self.filecontent))
      
  def createConfigFileBackup(self):
    """ Creates an backup of the original config file """
    backupFile = self.filename + ".orig"
    shutil.copyfile(self.filename, backupFile)
  
  def changeConfigValue(self, option, value):
    """ changes the given option in config file to the new given value """
    option_s = re.compile(option)
    option = self._addValueSeparator(option)
    
    config_copy = self.filecontent
    self.filecontent = []
    
    for line in config_copy:
      line, comment = self._lineWithoutComment(line)
      
      if option_s.search(line):
        line = option + value + comment
      
      self.filecontent.append(line + comment + "\n")
      
  def addConfigValue(self, option, value, comment=""):
    """ addes the given option to the config file with option comment """
    self.filecontent.append("\n\n")
    if len(comment) > 0:
      for line in comment.splitlines():
        self.filecontent.append("# " + line)
    
    self.filecontent.append(self._addValueSeparator(option) + value)
      
  def hasConfigOption(self, option):
    """ return true if the configile has the given option """
    value = self.readOptionValue(option, False)
    if value == "":
      return False
    
    return True
  
  def readOptionValue(self, option, raiseException=True):
    """ Searches for the given Option and returns it """
    option_s = re.compile(option + "\s*=\s*(\S+)")
    
    for line in self.filecontent:
      line, comment = self._lineWithoutComment(line)
      
      what = option_s.match(line)
      if what:
        return what.group(1).strip()
    
    if raiseException:
      raise ZmConfigError("Option not found: " + option)
    
    return ""
  
  @staticmethod
  def _addValueSeparator(option):
    if option[-1] != "=": # add '=' when missing
      option += "="
  
    return option
  
  @staticmethod
  def _lineWithoutComment(line):
    """ Splits comment from line """
    endpos = line.find("#")
    if endpos >= 0:
      return line[:endpos].strip(), line[endpos:].strip()
    
    endpos = line.find(";")
    if endpos >= 0:
      return line[:endpos].strip(), line[endpos:].strip()
    
    return line.strip(), ""
 
