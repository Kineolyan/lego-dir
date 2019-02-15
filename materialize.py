#!/usr/bin/env python3

import json
import os
import sys

def create_hierarchy(root_dir, folder, fs):
  current_path = root_dir
  remaining = folder
  while True:
    (head, remaining) = os.path.split(remaining)
    if len(head) == 0: break
    
    current_path = os.path.join(current_path, head)
    if not fs.exists(current_path):
      fs.mkdir(current_path)

def create_entry(virtual_dir, parent_dir, folder, fs):
  target_dir = os.path.join(virtual_dir, folder)
  if fs.exists(target_dir):
    print(f"{target_dir} already present. Skipping ...")
  else:
    base_dir = os.path.dirname(folder)
    if len(base_dir) > 0:
      create_hierarchy(virtual_dir, folder, fs = fs)
    
    source_dir = os.path.join(parent_dir, folder)
    fs.symlink(source_dir, target_dir)

def create_not_entries(virtual_dir, parent_dir, folder, fs):
  unwanted = folder[1:]
  elements = fs.listdir(parent_dir)
  check = lambda e: e != unwanted and e[0] != '.' and os.path.isdir(os.path.join(parent_dir, e))
  for e in elements:
    if check(e):
      create_entry(virtual_dir, parent_dir, folder = e, fs = fs)
