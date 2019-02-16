import unittest

import v1
from fs import TestApi

class V1Test(unittest.TestCase):

  def test_format_with_absolute_path(self):
    fs = TestApi()

    entry = v1.format_entry('vdir', '/root/some/path:one/dir', fs)
    self.assertEqual(entry, ('/root/some/path', 'one/dir'))

  def test_format_with_user_home(self):
    fs = TestApi()
    entry = v1.format_entry('vdir', '~/my/root:one/dir', fs)
    self.assertEqual(entry, (f"{fs.home}/my/root", 'one/dir'))

  def test_format_with_relative_path(self):
    fs = TestApi(cwd = '/a/b/c') # Have
    entry = v1.format_entry('vdir', 'd:other', fs)
    self.assertEqual(entry, ('/a/b/c/vdir/d', 'other'))

  def test_format_with_rewinding_path(self):
    fs = TestApi(cwd = '/a/b/c') # Have
    entry = v1.format_entry('vdir', '../../and/up/again:other', fs)
    self.assertEqual(entry, ('/a/b/and/up/again', 'other'))

  def test_format_with_leading_base(self):
    fs = TestApi(cwd = '/a/b/c')
    entry = v1.format_entry('to/vdir', '../path:target', fs)
    self.assertEqual(entry, ('/a/b/c/to/path', 'target'))

  def test_format_with_rewinding_base(self):
    fs = TestApi(cwd = '/a/b/c')
    entry = v1.format_entry('../vdir', '../path:target', fs)
    self.assertEqual(entry, ('/a/b/path', 'target'))

if __name__ == '__main__':
  unittest.main()
