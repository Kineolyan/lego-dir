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

def format_entry(root, entry, fs):
	if isinstance(entry, str):
		config = entry.strip().split(':')
		if len(config) != 2: raise ValueError(f"Bad configuration: expecting '<base path>:<spec> but got {entry}")

		[path, selection] = config
		expanded = format_location(path, root, fs)

		return {
			"location": expanded,
			"selection": [selection]
		}
	else:
		copy = dict(entry)
		copy['location'] = format_location(entry['location'], root, fs)

		return copy

# def check_entries(entries, fs):
#   for (e, f) in entries:
#     if not fs.isdir(e):
#       raise RuntimeError(f"Base folder {e} is not a directory")

#     if not is_not_selection(f):
#       source_dir = os.path.join(e, f)
#       if not fs.isdir(source_dir):
#         raise RuntimeError(f"Lego entry {source_dir} is not a directory")

# def build_entries(virtual_dir, entries, fs):
#   for (parent_dir, selection) in entries:
#     if is_not_selection(selection):
#       mat.create_not_entries(virtual_dir, parent_dir, selection, fs)
#     else:
#       mat.create_entry(virtual_dir, parent_dir, selection, fs)

def process_structure(virtual_dir_path, structure, fs):
  entries = [format_entry(virtual_dir_path, e, fs) for e in structure]

  # check_entries(entries, fs)
  # build_entries(virtual_dir_path, entries, fs)

def process(virtual_dir_path, config, fs):
	while 'redirect' in config:
		config = read_config(config['redirect'])

	process_structure(virtual_dir_path, config['structure'], fs)
