import unittest
import os

import v1
from fs import TestApi

class V1FormatEntryTest(unittest.TestCase):

  def setUp(self):
    self.fs = TestApi(cwd = '/a/b/c')

  def test_with_absolute_path(self):
    entry = v1.format_entry('vdir', '/root/some/path:one/dir', self.fs)
    self.assertEqual(entry, ('/root/some/path', 'one/dir'))

  def test_with_user_home(self):
    entry = v1.format_entry('vdir', '~/my/root:one/dir', self.fs)
    self.assertEqual(entry, (f"{self.fs.home}/my/root", 'one/dir'))

  def test_with_relative_path(self):
    entry = v1.format_entry('vdir', 'd:other', self.fs)
    self.assertEqual(entry, ('/a/b/c/vdir/d', 'other'))

  def test_with_rewinding_path(self):
    entry = v1.format_entry('vdir', '../../and/up/again:other', self.fs)
    self.assertEqual(entry, ('/a/b/and/up/again', 'other'))

  def test_with_leading_base(self):
    entry = v1.format_entry('to/vdir', '../path:target', self.fs)
    self.assertEqual(entry, ('/a/b/c/to/path', 'target'))

  def test_with_rewinding_base(self):
    entry = v1.format_entry('../vdir', '../path:target', self.fs)
    self.assertEqual(entry, ('/a/b/path', 'target'))

class V1BuildEntryTest(unittest.TestCase):

  def setUp(self):
    home = '/home/user'
    self.fs = TestApi(home = home, cwd = home)

  def test_for_simple_entry(self):
    structure = [('/a/b/dir', 'f1')]
    v1.build_entries('path/to/vdir', structure, self.fs)

    self.assertEqual(
      set(self.fs.created_links),
      set([('/a/b/dir/f1', 'path/to/vdir/f1')]))

  def test_for_not_entry(self):
    entries = ['a', 'b', 'not-this', 'c']
    self.fs._set_entries('/path', entries)
    for e in entries:
      self.fs._set_dir(f"/path/{e}")

    structure = [('/path', '!not-this')]
    v1.build_entries('to/vdir', structure, self.fs)

    self.assertEqual(
      set(self.fs.created_links),
      set([
        ('/path/a', 'to/vdir/a'),
        ('/path/b', 'to/vdir/b'),
        ('/path/c', 'to/vdir/c')
      ]))

  def test_with_structure_to_build(self):
    structure = [('/root', 'var/log/syslog')]
    v1.build_entries('the/vdir', structure, self.fs)

    self.assertEqual(
      self.fs.created_dirs,
      [
        'the/vdir/var',
        'the/vdir/var/log'
      ])
    self.assertEqual(
      list(self.fs.created_links),
      [('/root/var/log/syslog', 'the/vdir/var/log/syslog')])

  def test_for_many_entries(self):
    entries = ['a', 'not-this', 'b']
    self.fs._set_entries('/root', entries)
    for e in entries:
      self.fs._set_dir(f"/root/{e}")

    structure = [
      ('/a/b/dir', 'f1'),
      ('/my/home/has/dir', 'f2'),
      ('/root', '!not-this')
    ]
    v1.build_entries('path/to/vdir', structure, self.fs)

    self.assertEqual(
      set(self.fs.created_links),
      set([
        ('/a/b/dir/f1', 'path/to/vdir/f1'),
        ('/my/home/has/dir/f2', 'path/to/vdir/f2'),
        ('/root/a', 'path/to/vdir/a'),
        ('/root/b', 'path/to/vdir/b')
      ]))

  def test_with_existing_entry(self):
    self.fs._set_file('path/to/vdir/f1')

    structure = [('/a/b/dir', 'f1')]
    v1.build_entries('path/to/vdir', structure, self.fs)

    self.assertEqual(list(self.fs.created_links), [])

class V1Test(unittest.TestCase):

  def test_integration(self):
    fs = TestApi(home = '/home/charlie', cwd = '/usr')
    entries = ['a', 'b', 'not-this']
    fs._set_entries('/root', entries)
    for e in entries:
      fs._set_dir(f"/root/{e}")
    for e in ['/home/charlie/dir/f1', '/usr/other/f2', '/root/a', '/root/b']:
      fs._set_dir(os.path.dirname(e))
      fs._set_dir(e)

    structure = [
      '~/dir:f1',
      '../other:f2',
      '/root:!not-this'
    ]
    v1.process_structure('vdir', structure, fs)

    self.assertEqual(
      set(fs.created_links),
      set([
        ('/home/charlie/dir/f1', 'vdir/f1'),
        ('/usr/other/f2', 'vdir/f2'),
        ('/root/a', 'vdir/a'),
        ('/root/b', 'vdir/b')
      ]))

if __name__ == '__main__':
  unittest.main()
