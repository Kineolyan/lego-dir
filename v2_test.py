import unittest
import os

import v2
from fs import TestApi

def simple_entry(location, element):
	return {
		"location": location,
		"selection": [element]
	}

class V1FormatEntryTest(unittest.TestCase):

	def setUp(self):
		self.fs = TestApi(cwd = '/a/b/c')

	def test_with_absolute_path(self):
		entry = v2.format_entry('vdir', '/root/some/path:one/dir', self.fs)
		self.assertEqual(entry, simple_entry('/root/some/path', 'one/dir'))

	def test_with_user_home(self):
		entry = v2.format_entry('vdir', '~/my/root:one/dir', self.fs)
		self.assertEqual(entry, simple_entry(f"{self.fs.home}/my/root", 'one/dir'))

	def test_with_relative_path(self):
		entry = v2.format_entry('vdir', 'd:other', self.fs)
		self.assertEqual(entry, simple_entry('/a/b/c/vdir/d', 'other'))

	def test_with_rewinding_path(self):
		entry = v2.format_entry('vdir', '../../and/up/again:other', self.fs)
		self.assertEqual(entry, simple_entry('/a/b/and/up/again', 'other'))

	def test_with_leading_base(self):
		entry = v2.format_entry('to/vdir', '../path:target', self.fs)
		self.assertEqual(entry, simple_entry('/a/b/c/to/path', 'target'))

	def test_with_rewinding_base(self):
		entry = v2.format_entry('../vdir', '../path:target', self.fs)
		self.assertEqual(entry, simple_entry('/a/b/path', 'target'))

	def test_with_complex_entry_and_absolute_path(self):
		config = {
			"location": '/var',
			"base": 'log',
			"selection": ['nginx', 'apache']
		}
		entry = v2.format_entry('vdir', config, self.fs)
		self.assertEqual(entry, config)

	def test_with_complex_entry_and_user_path(self):
		config = {
			"location": '~/my/root',
			"base": 'log',
			"selection": ['nginx', 'apache']
		}
		entry = v2.format_entry('vdir', config, self.fs)
		self.assertEqual(
			entry,
			{
				"location": f"{self.fs.home}/my/root",
				"base": 'log',
				"selection": ['nginx', 'apache']
			})

	def test_with_complex_entry_and_relative_path(self):
		config = {
			"location": 'd',
			"base": 'log',
			"selection": ['nginx', 'apache']
		}
		entry = v2.format_entry('vdir', config, self.fs)
		self.assertEqual(
			entry,
			{
				"location": '/a/b/c/vdir/d',
				"base": 'log',
				"selection": ['nginx', 'apache']
			})

	def test_with_complex_entry_and_rewinding_path(self):
		config = {
			"location": '../../and/up/again',
			"base": 'log',
			"selection": ['nginx', 'apache']
		}
		entry = v2.format_entry('vdir', config, self.fs)
		self.assertEqual(
			entry,
			{
				"location": '/a/b/and/up/again',
				"base": 'log',
				"selection": ['nginx', 'apache']
			})

	def test_with_complex_entry_and_leading_base(self):
		config = {
			"location": '../path',
			"base": 'log',
			"selection": ['nginx', 'apache']
		}
		entry = v2.format_entry('to/vdir', config, self.fs)
		self.assertEqual(
			entry,
			{
				"location": '/a/b/c/to/path',
				"base": 'log',
				"selection": ['nginx', 'apache']
			})

	def test_with_complex_entry_and_rewinding_base(self):
		config = {
			"location": '../path',
			"base": 'log',
			"selection": ['nginx', 'apache']
		}
		entry = v2.format_entry('../vdir', config, self.fs)
		self.assertEqual(
			entry,
			{
				"location": '/a/b/path',
				"base": 'log',
				"selection": ['nginx', 'apache']
			})

# class V1BuildEntryTest(unittest.TestCase):

	# def setUp(self):
	#   home = '/home/user'
	#   self.fs = TestApi(home = home, cwd = home)

	# def test_for_simple_entry(self):
	#   structure = [('/a/b/dir', 'f1')]
	#   v1.build_entries('path/to/vdir', structure, self.fs)

	#   self.assertEqual(
	#     set(self.fs.created_links),
	#     set([('/a/b/dir/f1', 'path/to/vdir/f1')]))

	# def test_for_not_entry(self):
	#   self.fs._set_entries('/path', ['a', 'b', 'not-this', 'c'])
	#   for e in ['a', 'b', 'c']:
	#     self.fs._set_dir(f"/path/{e}")

	#   structure = [('/path', '!not-this')]
	#   v1.build_entries('to/vdir', structure, self.fs)

	#   self.assertEqual(
	#     set(self.fs.created_links),
	#     set([
	#       ('/path/a', 'to/vdir/a'),
	#       ('/path/b', 'to/vdir/b'),
	#       ('/path/c', 'to/vdir/c')
	#     ]))

	# def test_with_structure_to_build(self):
	#   structure = [('/root', 'var/log/syslog')]
	#   v1.build_entries('the/vdir', structure, self.fs)

	#   self.assertEquals(
	#     self.fs.created_dirs,
	#     [
	#       'the/vdir/var',
	#       'the/vdir/var/log'
	#     ])
	#   self.assertEquals(
	#     list(self.fs.created_links),
	#     [('/root/var/log/syslog', 'the/vdir/var/log/syslog')])

	# def test_for_many_entries(self):
	#   self.fs._set_entries('/root', ['a', 'not-this', 'b'])
	#   for e in ['a', 'b', 'c']:
	#     self.fs._set_dir(f"/root/{e}")

	#   structure = [
	#     ('/a/b/dir', 'f1'),
	#     ('/my/home/has/dir', 'f2'),
	#     ('/root', '!not-this')
	#   ]
	#   v1.build_entries('path/to/vdir', structure, self.fs)

	#   self.assertEqual(
	#     set(self.fs.created_links),
	#     set([
	#       ('/a/b/dir/f1', 'path/to/vdir/f1'),
	#       ('/my/home/has/dir/f2', 'path/to/vdir/f2'),
	#       ('/root/a', 'path/to/vdir/a'),
	#       ('/root/b', 'path/to/vdir/b')
	#     ]))

	# def test_with_existing_entry(self):
	#   self.fs._set_file('path/to/vdir/f1')

	#   structure = [('/a/b/dir', 'f1')]
	#   v1.build_entries('path/to/vdir', structure, self.fs)

	#   self.assertEqual(list(self.fs.created_links), [])

class V2Test(unittest.TestCase):

	def test_integration(self):
		fs = TestApi(home = '/home/charlie', cwd = '/usr')
		fs._set_entries('/root', ['a', 'b'])
		for e in ['a', 'b']:
			fs._set_dir(f"/root/{e}")
		for e in ['/home/charlie/dir/f1', '/usr/other/f2', '/root/a', '/root/b']:
			fs._set_dir(os.path.dirname(e))
			fs._set_dir(e)

		structure = [
			'~/dir:f1',
			'../other:f2',
			'/root:!not-this',
			{
				"location": '/var',
				"base": 'log',
				"selection": ['nginx', 'apache']
			},
			{
				"location": '/var',
				"base": 'log',
				"selection": ['nginx', 'apache']
			}
		]
		v2.process('vdir', {"structure": structure}, fs)

		# self.assertEqual(
		#   set(fs.created_links),
		#   set([
		#     ('/home/charlie/dir/f1', 'vdir/f1'),
		#     ('/usr/other/f2', 'vdir/f2'),
		#     ('/root/a', 'vdir/a'),
		#     ('/root/b', 'vdir/b')
		#   ]))

if __name__ == '__main__':
	unittest.main()
