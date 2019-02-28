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

	def test_with_negated_root_entry(self):
		entry = v2.format_entry('../vdir', '~/dd:!f', self.fs)
		self.assertEqual(
			entry,
			{
				"location": f"{self.fs.home}/dd",
				"selection": ['!f']
			})

	def test_with_negated_entry(self):
		entry = v2.format_entry('../vdir', '~/dd:path/to/!f', self.fs)
		self.assertEqual(
			entry,
			{
				"location": f"{self.fs.home}/dd",
				"base": 'path/to',
				"selection": ['!f']
			})

class V2CheckEntryTest(unittest.TestCase):

	def setUp(self):
		home = '/home/user'
		self.fs = TestApi(home = home, cwd = home)

	def test_simple_entry(self):
		self.fs._set_dir('/path/to/a/dir')
		self.fs._set_dir('/path/to/a/dir/file')
		config = {
			'location': '/path/to/a/dir',
			'selection': ['file']
		}
		v2.check_entries([config], self.fs)

	def test_entry_with_base(self):
		self.fs._set_dir('/path/to/a/dir')
		self.fs._set_dir('/path/to/a/dir/d1/d2')
		self.fs._set_dir('/path/to/a/dir/d1/d2/file')
		config = {
			'location': '/path/to/a/dir',
			'base': 'd1/d2',
			'selection': ['file']
		}
		v2.check_entries([config], self.fs)

	def test_multiple_entries(self):
		self.fs._set_dir('/path/to/a/dir')
		self.fs._set_dir('/path/to/a/dir/d1/d2')
		self.fs._set_dir('/path/to/a/dir/d1/d2/f1')
		self.fs._set_dir('/path/to/a/dir/d1/d2/f2')
		config = {
			'location': '/path/to/a/dir',
			'base': 'd1/d2',
			'selection': ['f1', 'f2']
		}
		v2.check_entries([config], self.fs)

	def test_with_negate_entries(self):
		self.fs._set_dir('/path/to/a/dir')
		self.fs._set_dir('/path/to/a/dir/d1/d2')
		config = {
			'location': '/path/to/a/dir',
			'base': 'd1/d2',
			'selection': ['!f1', '!f2']
		}
		v2.check_entries([config], self.fs)

	def test_with_mixed_entries(self):
		self.fs._set_dir('/path/to/a/dir')
		self.fs._set_dir('/path/to/a/dir/d1/d2')
		config = {
			'location': '/path/to/a/dir',
			'base': 'd1/d2',
			'selection': ['!f1', 'f2']
		}
		with self.assertRaises(ValueError):
			v2.check_entries([config], self.fs)

	def test_with_invalid_location(self):
		config = {'location': '/not/a/dir'}
		with self.assertRaises(ValueError):
			v2.check_entries([config], self.fs)

	def test_with_invalid_base(self):
		self.fs._set_dir('/the/real/dir')
		config = {
			'location': '/the/real/dir',
			'base': 'is/wrong'
		}
		with self.assertRaises(ValueError):
			v2.check_entries([config], self.fs)

	def test_with_base_and_invalid_entry(self):
		self.fs._set_dir('/the/real')
		self.fs._set_dir('/the/real/dir')
		self.fs._set_dir('/the/real/dir/valid')
		config = {
			'location': '/the/real',
			'base': 'dir',
			'selection': [
				'valid',
				'invalid'
			]
		}
		with self.assertRaises(ValueError):
			v2.check_entries([config], self.fs)

	def test_multiple_checks(self):
		self.fs._set_dir('/path/to/a/dir')
		self.fs._set_dir('/path/to/a/dir/d1/d2')
		self.fs._set_dir('/path/to/a/dir/d1/d2/f1')
		self.fs._set_dir('/path/to/a/dir/d1/d2/f2')
		self.fs._set_dir('/path/to/a/dir/d3')
		configs = [
			{
				'location': '/path/to/a/dir',
				'base': 'd1/d2',
				'selection': ['f1', 'f2']
			},
			{
				'location': '/path/to/a/dir',
				'base': 'd3',
				'selection': ['!f1', '!f2']
			}
		]
		v2.check_entries(configs, self.fs)

	def test_multiple_with_errors(self):
		self.fs._set_dir('/path/to/a/dir')
		self.fs._set_dir('/path/to/a/dir/d1/d2')
		self.fs._set_dir('/path/to/a/dir/d1/d2/f1')
		self.fs._set_dir('/path/to/a/dir/d1/d2/f2')
		configs = [
			{
				'location': '/path/to/a/dir',
				'base': 'd1/d2',
				'selection': ['f1', 'f2']
			},
			{
				'location': '/path/to/a/dir',
				'base': 'd3',
				'selection': ['!f1', '!f2']
			}
		]
		with self.assertRaises(ValueError):
			v2.check_entries(configs, self.fs)

	def test_not_has_no_path(self):
		self.fs._set_dir('/path/to/a/dir')
		self.fs._set_dir('/path/to/a/dir/d1/d2')
		config = {
			'location': '/path/to/a/dir',
			'base': 'd1/d2',
			'selection': ['!f1/f2']
		}
		with self.assertRaises(ValueError):
			v2.check_entries([config], self.fs)

class V2BuildEntryTest(unittest.TestCase):

	def setUp(self):
		home = '/home/user'
		self.fs = TestApi(home = home, cwd = home)

	def test_for_simple_entry(self):
		structure = [simple_entry('/a/b/dir', 'f1')]
		v2.build_entries('path/to/vdir', structure, self.fs)

		self.assertEqual(
			set(self.fs.created_links),
			set([('/a/b/dir/f1', 'path/to/vdir/f1')]))

	def test_for_simple_entries(self):
		config = {
			'location': '/a/b/dir',
			'selection': ['f1', 'f2']
		}
		v2.build_entries('path/to/vdir', [config], self.fs)

		self.assertEqual(
			set(self.fs.created_links),
			set([
				('/a/b/dir/f1', 'path/to/vdir/f1'),
				('/a/b/dir/f2', 'path/to/vdir/f2')
			]))

	def test_for_simple_entries_with_base(self):
		config = {
			'location': '/a/b',
			'base': 'long/dir',
			'selection': ['f1', 'f2']
		}
		v2.build_entries('path/to/vdir', [config], self.fs)

		self.assertEqual(
			self.fs.created_dirs,
			[
			'path/to/vdir/long',
			'path/to/vdir/long/dir'
			])
		self.assertEqual(
			set(self.fs.created_links),
			set([
				('/a/b/long/dir/f1', 'path/to/vdir/long/dir/f1'),
				('/a/b/long/dir/f2', 'path/to/vdir/long/dir/f2')
			]))

	def test_for_not_entry(self):
		self.fs._set_entries('/path', ['a', 'b', 'not-this', 'c'])
		for e in ['a', 'b', 'c']:
			self.fs._set_dir(f"/path/{e}")

		structure = [simple_entry('/path', '!not-this')]
		v2.build_entries('to/vdir', structure, self.fs)

		self.assertEqual(
			set(self.fs.created_links),
			set([
				('/path/a', 'to/vdir/a'),
				('/path/b', 'to/vdir/b'),
				('/path/c', 'to/vdir/c')
			]))

	def test_for_not_entry_with_base(self):
		self.fs._set_entries('/path/inside/dir', ['a', 'b', 'not-this', 'c'])
		for e in ['a', 'b', 'c']:
			self.fs._set_dir(f"/path/inside/dir/{e}")

		config = {
			'location': '/path',
			'base': 'inside/dir',
			'selection': ['!not-this']
		}
		v2.build_entries('to/vdir', [config], self.fs)

		self.assertEqual(
			self.fs.created_dirs,
			[
				'to/vdir/inside',
				'to/vdir/inside/dir'
			])
		self.assertEqual(
		  set(self.fs.created_links),
		  set([
		    ('/path/inside/dir/a', 'to/vdir/inside/dir/a'),
		    ('/path/inside/dir/b', 'to/vdir/inside/dir/b'),
		    ('/path/inside/dir/c', 'to/vdir/inside/dir/c')
		  ]))

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
		# v2.process('vdir', {"structure": structure}, fs)

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
