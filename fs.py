import os
import sys

class SystemApi:
  def open(self, path, options = 'r'):
    return open(path, options)

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

  def open(self, path, options = 'r'):
    if options == 'r':
      return open(path)
    else:
      raise RuntimeError("Not implemented")

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
    """
    Adds entries for the given path.
    The entries are returned when calling Api#listdir(<path>).
    """
    self.entries[path] = entries

  def exists(self, path):
    return path in self.files

  def _set_file(self, path):
    """
    Adds a new entry to the list of files and directories existing in this file system.
    """
    self.files.add(path)

  def mkdir(self, path):
    if not path in self.created_dirs:
      self.created_dirs.append(path)

  def symlink(self, src, dst):
    link = (src, dst)
    if not link in self.created_links:
      self.created_links.append(link)

SYSTEM = SystemApi()
