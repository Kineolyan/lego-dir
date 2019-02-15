import os
import sys

class SystemApi:
  def expanduser(self, path):
    return os.path.expanduser(path)
  
  def getcwd(self): 
    return os.getcwd()

  def isdir(self, path): 
    return os.path.isdir(path)

  def listdir(self, path):
    return os.listdir(path)

  def exists(self, path):
    return os.path.exists(path)

  def mkdir(self, path):
    return os.mkdir(path)

  def symlink(self, src, dst):
    return os.symlink(src, dst)

SYSTEM = SystemApi()
