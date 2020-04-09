# -*- coding: utf-8 -*- 

from subprocess import Popen, PIPE

class ZmUpdateError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

class ZmUpdate:
  """ Class for handling zm update command """
  
  def __init__(self, zmUpdatePath, backupDatabase):
    self.zmUpdatePath = zmUpdatePath
    self.backup = backupDatabase
  
  def updateFromVersion(self):
    print("invoking zmupdate.pl for database update")
    process = Popen(self.zmUpdatePath, stderr=PIPE, stdout=PIPE, stdin=PIPE, shell=True)
    
    interaction = "\nn\n"
    if self.backup:
      interaction = "\ny\n"
    
    out, err = process.communicate(interaction.encode())
    
    if isinstance(out, bytes):
      out = out.decode('utf-8', errors='replace')
      
    if isinstance(err, bytes):
      err = err.decode('utf-8', errors='replace')
    
    print(out)
    
    if process.returncode != 0:
      raise ZmUpdateError("Could not update database with zmupdate.pl: " + err)
    
