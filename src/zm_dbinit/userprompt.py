# -*- coding: utf-8 -*- 
import getpass

class UserPrompt:
  """ Helper class for handling user prompt """
  def __init__(self, non_interactive):
    self.non_interactive = non_interactive
    self.failurecount = 0
  
  def okToContinue(self, question, defaultAnswer = True, interaction_required = False):
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
      
      if interaction_required:
        raise RuntimeError("Required user interaction!!")
      
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
    
    if passwd == "":
      print "password is empty please choose a non empty password"
      self.askForPassword(text, retype)
    
    if retype:
      t_pass = getpass.getpass("retype password: ")
    else:
      return passwd
    
    if passwd != t_pass and self.failurecount < 3:
      print "Password mismatch please try again"
      self.askForPassword(text, retype)
    elif passwd != t_pass:
      raise RuntimeError("Too many user interaction errors")
    
    return passwd
    
  def askForUserData(self, text):
    if self.non_interactive:
      raise RuntimeError("Asking for password is not allowed in non interactive mode!!")
    
    return raw_input(text + ": ")
    