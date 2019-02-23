import os

from config import read as read_config
# import materialize as mat

# def is_not_selection(selection):
#   return '!' in selection

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

  #   if not is_not_selection(f):
  #     source_dir = os.path.join(e, f)
  #     if not fs.isdir(source_dir):
  #       raise RuntimeError(f"Lego entry {source_dir} is not a directory")

# def build_entries(virtual_dir, entries, fs):
#   for (parent_dir, selection) in entries:
#     if is_not_selection(selection):
#       mat.create_not_entries(virtual_dir, parent_dir, selection, fs)
#     else:
#       mat.create_entry(virtual_dir, parent_dir, selection, fs)

def process_structure(virtual_dir_path, structure, fs):
  entries = [format_entry(virtual_dir_path, e, fs) for e in structure]

  check_entries(entries, fs)
  # build_entries(virtual_dir_path, entries, fs)

def process(virtual_dir_path, config, fs):
	while 'redirect' in config:
		config = read_config(config['redirect'])

	process_structure(virtual_dir_path, config['structure'], fs)
