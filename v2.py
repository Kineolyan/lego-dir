import os

from config import read as read_config
# import materialize as mat

# def is_not_selection(selection):
#   return '!' in selection

# def format_entry(root, entry, fs):
#   config = entry.split(':')
#   if len(config) != 2: raise ValueError(f"Bad configuration: expecting '<base path>:<spec> but got {entry}")

#   [path, selection] = config
#   expanded = fs.expanduser(path)
#   if not os.path.isabs(expanded):
#     expanded = os.path.normpath(os.path.join(fs.getcwd(), root, expanded))

#   return (expanded, selection)

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
	pass

def process(virtual_dir_path, structure, fs):
	pass

  # entries = [format_entry(virtual_dir_path, e.strip(), fs) for e in structure]

  # check_entries(entries, fs)
  # build_entries(virtual_dir_path, entries, fs)
