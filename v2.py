import os

from config import read as read_config
import materialize as mat

def is_not_selection(selection):
  return '!' in selection

def format_location(path, root, fs):
	expanded = fs.expanduser(path)
	if not os.path.isabs(expanded):
		expanded = os.path.normpath(os.path.join(fs.getcwd(), root, expanded))

	return expanded

def format_selection(value):
	if '/!' in value:
		split_index = value.index('/!')
		base = value[:split_index]
		selection = value[(split_index + 1):] # inc index to remove the '/'
		return (base, selection)
	else:
		return (None, value)

def format_entry(root, entry, fs):
	if isinstance(entry, str):
		config = entry.strip().split(':')
		if len(config) != 2: raise ValueError(f"Bad configuration: expecting '<base path>:<spec> but got {entry}")

		[path, rest] = config
		expanded = format_location(path, root, fs)
		(base, selection) = format_selection(rest)

		converted_entry = {
			"location": expanded,
			"selection": [selection]
		}
		if base != None: converted_entry['base'] = base

		return converted_entry
	else:
		copy = dict(entry)
		copy['location'] = format_location(entry['location'], root, fs)

		return copy

def check_entries(entries, fs):
	for entry in entries:
		location = entry['location']
		if not fs.isdir(location):
			raise ValueError(f"Location folder {location} is not a directory")

		base = entry.get('base', None)
		if base != None:
			base_path = os.path.join(location, base)
			if not fs.isdir(base_path):
				raise ValueError(f"Base folder {base_path} is not a directory")
		else:
			base_path = location

		## Entries must be all not values or values
		all_not = all(is_not_selection(e) for e in entry['selection'])
		all_basic = all(not is_not_selection(e) for e in entry['selection'])
		if not (all_basic or all_not):
			raise ValueError(f"Selection must be either values or a list of not entries")

		for source in entry['selection']:
			if is_not_selection(source):
				if os.sep in source:
					raise ValueError(f"Lego negative entry {source} cannot be a path")
			else:
				source_dir = os.path.join(base_path, source)
				if not fs.isdir(source_dir):
					raise ValueError(f"Lego entry {source_dir} is not a directory")

def build_entries(virtual_dir, entries, fs):
	for entry in entries:
		parent_dir = entry['location']
		base = entry.get('base', None)
		operate_not = is_not_selection(entry['selection'][0])
		if operate_not:
			selection = [s[1:] for s in entry['selection']]
			mat.create_not_entries_with_condition(
				virtual_dir,
				parent_dir,
				base,
				lambda f: not f in selection,
				fs)
		else:
			for s in entry['selection']:
				selection = s if base == None else os.path.join(base, s)
				mat.create_entry(virtual_dir, parent_dir, selection, fs)

def process_structure(virtual_dir_path, structure, fs):
  entries = [format_entry(virtual_dir_path, e, fs) for e in structure]

  check_entries(entries, fs)
  build_entries(virtual_dir_path, entries, fs)

def process(virtual_dir_path, config, fs):
	while 'redirect' in config:
		config = read_config(config['redirect'], fs)

	process_structure(virtual_dir_path, config['structure'], fs)

def create_redirection(config_file, virtual_dir_path, fs):
	if not fs.exists(virtual_dir_path):
		fs.mkdir(virtual_dir_path)

	dir_path = fs.expanduser(virtual_dir_path)
	if not os.path.isabs(dir_path):
		dir_path = os.path.normpath(os.path.join(fs.getcwd(), dir_path))

	spec_path = os.path.join(dir_path, '.lego-spec')
	with fs.open(spec_path, 'w') as file:
		target_config = fs.expanduser(config_file)
		if not os.path.isabs(target_config):
			target_config = os.path.normpath(os.path.join(fs.getcwd(), target_config))
			
		file.write(f"""
{{
  "version": 2,
  "redirect": "{target_config}"
}}
""")

