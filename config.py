import json
import os

def read_default(virtual_dir_path):
	return read(os.path.join(virtual_dir_path, '.lego-spec'))

def read(config_file):
	with open(config_file) as file:
		return json.load(file)
