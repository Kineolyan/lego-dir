#!/usr/bin/env python3

import json
import os
import sys

def create_hierarchy(root_dir, folder, fs):
  current_path = root_dir
  for part in os.path.dirname(folder).split(os.sep):
    current_path = os.path.join(current_path, part)
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
  create_not_entries_with_condition(
    virtual_dir,
    parent_dir,
    None,
    lambda f: f != unwanted,
    fs)

def create_not_entries_with_condition(virtual_dir, parent_dir, folder, predicate, fs):
  base_dir = parent_dir if folder == None else os.path.join(parent_dir, folder)
  elements = fs.listdir(base_dir)
  check = lambda e: e[0] != '.' and fs.isdir(os.path.join(base_dir, e)) and predicate(e)
  for e in elements:
    if check(e):
      create_entry(
        virtual_dir,
        parent_dir,
        folder = e if folder == None else os.path.join(folder, e),
        fs = fs)
