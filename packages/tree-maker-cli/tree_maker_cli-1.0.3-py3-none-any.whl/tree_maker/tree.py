import os
from .utils import is_hidden
from .config import DEFAULT_EXCLUDED_FILES

def generate_tree(folder, depth, show_hidden, prefix='', excluded_files=None):
  if excluded_files is None:
    excluded_files = []

  excluded_files.extend(DEFAULT_EXCLUDED_FILES)
  excluded_files = list(set(excluded_files))
  folders, files = sort_directory_contents(folder, excluded_files, show_hidden)
  return build_tree(folder, folders, files, depth, show_hidden, prefix, excluded_files)

def sort_directory_contents(folder, excluded_files, show_hidden):
  folders = []
  files = []
  for item in os.listdir(folder):
    if item in excluded_files or (not show_hidden and is_hidden(item)):
      continue
    if os.path.isdir(os.path.join(folder, item)):
      folders.append(item)
    else:
      files.append(item)
  folders.sort()
  files.sort()
  return folders, files

def build_tree(folder, folders, files, depth, show_hidden, prefix, excluded_files):
  tree = ''
  total_items = folders + files  # Combine folders and files for unified indexing
  for index, item in enumerate(total_items):
    is_last = (index == len(total_items) - 1)
    tree += build_tree_line(item, is_last, prefix, folder, depth, show_hidden, excluded_files)
  return tree

def build_tree_line(item, is_last, prefix, folder, depth, show_hidden, excluded_files):
  line_prefix, new_prefix = get_prefixes(prefix, is_last)
  line = f"{line_prefix}{item}"
  if os.path.isdir(os.path.join(folder, item)):
    line += '/\n'
    if depth is None or depth > 0:
      line += generate_tree(os.path.join(folder, item), depth - 1 if depth is not None else None, show_hidden, new_prefix, excluded_files)
  else:
    line += '\n'
  return line

def get_prefixes(prefix, is_last):
  if prefix == '':
    line_prefix = '└── ' if is_last else '├── '
    new_prefix = '    ' if is_last else '│   '
  else:
    line_prefix = prefix + ('└── ' if is_last else '├── ')
    new_prefix = prefix + ('    ' if is_last else '│   ')
  return line_prefix, new_prefix

