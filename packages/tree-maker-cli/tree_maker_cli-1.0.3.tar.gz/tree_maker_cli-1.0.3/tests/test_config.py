import os
import json
from tree_maker.config import (
  DEFAULT_EXCLUDED_FILES,
  EXCLUDED_FILES_FILE,
  load_excluded_files,
  save_excluded_files,
  add_default_excluded_files,
  remove_default_excluded_files,
)

def test_load_excluded_files(tmpdir):
  # Test loading excluded files when the file doesn't exist
  assert load_excluded_files() == DEFAULT_EXCLUDED_FILES

  # Test loading excluded files from a file
  excluded_files = ['file1', 'file2']
  with open(EXCLUDED_FILES_FILE, 'w') as file:
    json.dump(excluded_files, file)
  assert load_excluded_files() == excluded_files
  os.remove(EXCLUDED_FILES_FILE)

def test_save_excluded_files(tmpdir):
  excluded_files = ['file1', 'file2']
  save_excluded_files(excluded_files)
  with open(EXCLUDED_FILES_FILE, 'r') as file:
    assert json.load(file) == excluded_files
  os.remove(EXCLUDED_FILES_FILE)

def test_add_default_excluded_files(tmpdir):
  save_excluded_files(DEFAULT_EXCLUDED_FILES.copy())  # Save a copy of the default excluded files
  add_default_excluded_files(['file3', 'file4'])
  assert load_excluded_files() == DEFAULT_EXCLUDED_FILES + ['file3', 'file4']
  os.remove(EXCLUDED_FILES_FILE)

def test_remove_default_excluded_files(tmpdir):
  excluded_files = DEFAULT_EXCLUDED_FILES.copy() + ['file3', 'file4']  # Create a copy and add extra files
  save_excluded_files(excluded_files)

  # Test removing files that exist in excluded_files
  remove_default_excluded_files(['file3', 'file4'])
  assert load_excluded_files() == DEFAULT_EXCLUDED_FILES

  # Test removing a file that doesn't exist in excluded_files
  remove_default_excluded_files(['file5'])
  assert load_excluded_files() == DEFAULT_EXCLUDED_FILES

  os.remove(EXCLUDED_FILES_FILE)

