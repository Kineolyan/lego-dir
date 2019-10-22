import json
import os

def read_default(virtual_dir_path, fs):
	return read(os.path.join(virtual_dir_path, '.lego-spec'), fs)

def read(config_file, fs):
	with fs.open(config_file) as file:
		return json.load(file)
