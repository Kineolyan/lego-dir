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

class TestApi:

  def __init__(self, **kwargs):
    self.home = kwargs.get('home', os.path.join('/', 'home', 'charlie'))
    self.cwd = kwargs.get('cwd', os.path.join(self.home, 'working', 'in'))
    self.clear()

  def clear(self):
    self.dirs = set()
    self.entries = {}
    self.files = set()
    self.created_dirs = []
    self.created_links = []

  def expanduser(self, path):
    if path.startswith('~'):
      return f"{self.home}{path[1:]}"
    else:
      return path

  def getcwd(self):
    return self.cwd

  def isdir(self, path):
    return path in self.dirs

  def _set_dir(self, path):
    self.dirs.add(path)

  def listdir(self, path):
    return self.entries[path]

  def _set_entries(self, path, entries):
    self.entries[path] = entries

  def exists(self, path):
    return path in self.files

  def _set_file(self, path):
    self.files.add(path)

  def mkdir(self, path):
    self.created_dirs.add(path)

  def symlink(self, src, dst):
    self.created_links.add((src, dst))

SYSTEM = SystemApi()
