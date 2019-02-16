import unittest

import v1
from fs import TestApi

class V1FormatEntryTest(unittest.TestCase):

  def setUp(self):
    self.fs = TestApi(cwd = '/a/b/c')

  def test_with_absolute_path(self):
    entry = v1.format_entry('vdir', '/root/some/path:one/dir', self.fs)
    self.assertEqual(entry, ('/root/some/path', 'one/dir'))

  def test_with_user_home(self):
    fs = TestApi()
    entry = v1.format_entry('vdir', '~/my/root:one/dir', self.fs)
    self.assertEqual(entry, (f"{self.fs.home}/my/root", 'one/dir'))

  def test_with_relative_path(self):
    fs = TestApi(cwd = '/a/b/c') # Have
    entry = v1.format_entry('vdir', 'd:other', self.fs)
    self.assertEqual(entry, ('/a/b/c/vdir/d', 'other'))

  def test_with_rewinding_path(self):
    fs = TestApi(cwd = '/a/b/c') # Have
    entry = v1.format_entry('vdir', '../../and/up/again:other', self.fs)
    self.assertEqual(entry, ('/a/b/and/up/again', 'other'))

  def test_with_leading_base(self):
    fs = TestApi(cwd = '/a/b/c')
    entry = v1.format_entry('to/vdir', '../path:target', self.fs)
    self.assertEqual(entry, ('/a/b/c/to/path', 'target'))

  def test_with_rewinding_base(self):
    fs = TestApi(cwd = '/a/b/c')
    entry = v1.format_entry('../vdir', '../path:target', self.fs)
    self.assertEqual(entry, ('/a/b/path', 'target'))

class V1BuildEntryTest(unittest.TestCase):

  def setUp(self):
    home = '/home/user'
    self.fs = TestApi(home = home, cwd = home)

  def test_for_simple_entry(self):
    structure = [
      ('/a/b/dir', 'f1'),
    ]
    v1.build_entries('path/to/vdir', structure, self.fs)

  def test_for_not_entry(self):
    structure = [
      ('/path', '!not-this')
    ]
    v1.build_entries('path/to/vdir', structure, self.fs)

  def test_for_many_entries(self):
    structure = [
      ('/a/b/dir', 'f1'),
      ('/my/home/has/dir', 'f2'),
      ('/path', '!not-this')
    ]
    v1.build_entries('path/to/vdir', structure, self.fs)

  def test_with_existing_entry(self):
    raise RuntimeError('TODO')

class V1Test(unittest.TestCase):

  def test_simple(self):
    fs = TestApi()
    structure = [
      '/a/b/dir:f1',
      '/my/home/has/dir:f2',
      '/path:!not-this'
    ]
    v1.process_structure('path/to/vdir', structure, fs)


if __name__ == '__main__':
  unittest.main()
