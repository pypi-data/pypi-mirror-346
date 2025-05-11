import argparse
import os
from tree_maker.tree import generate_tree
from tree_maker.config import load_excluded_files, add_default_excluded_files, remove_default_excluded_files

def main():
  parser = argparse.ArgumentParser(description='Generate a tree structure of a folder.')
  parser.add_argument('folder_path', metavar='folder_path', type=str, nargs='?', default='.', help='Path to the folder for generating the tree structure (default: current folder)')
  parser.add_argument('--depth', type=int, help='Maximum depth of the tree structure (default: unlimited)')
  parser.add_argument('--exclude', nargs='*', default=[], help='Additional files to exclude from the tree structure')
  parser.add_argument('--show-hidden', action='store_true', help='Show hidden files in the tree structure')
  parser.add_argument('--output', '-o', type=str, help='Output the tree to a file located at the OUTPUT file path')
  parser.add_argument('--clipboard', '-c', action='store_true', help='Copy the tree to the clipboard')
  parser.add_argument('--add-excluded', nargs='*', default=[], help='Add files/folders to the list of default excluded files and folders')
  parser.add_argument('--remove-excluded', nargs='*', default=[], help='Remove files/folders from the list of default excluded files and folders')
  parser.add_argument('--show-excluded', action='store_true', help='Show the current list of default excluded files and folders')

  args = parser.parse_args()

  add_excluded_files = args.add_excluded
  remove_excluded_files = args.remove_excluded
  show_excluded_files = args.show_excluded

  if show_excluded_files:
    print("Current default excluded files/folders:")
    for file in load_excluded_files():
      print(file)
    return

  if add_excluded_files:
    add_default_excluded_files(add_excluded_files)
    print("Added to default excluded files/folders:")
    for file in add_excluded_files:
      print(file)
    return

  if remove_excluded_files:
    remove_default_excluded_files(remove_excluded_files)
    print("Removed from default excluded files/folders:")
    for file in remove_excluded_files:
      print(file)
    return

  folder_path = args.folder_path
  depth = args.depth
  excluded_files = load_excluded_files() + args.exclude
  show_hidden = args.show_hidden

  tree_structure = generate_tree(folder_path, depth, show_hidden, excluded_files=excluded_files)
  root_folder_name = os.path.basename(os.path.abspath(folder_path))

  output = f"{root_folder_name}\n{tree_structure}"

  if args.output:
    with open(args.output, 'w') as file:
      file.write(output)
    print(f"Tree saved to {args.output}")
  elif args.clipboard:
    try:
      import pyperclip
      pyperclip.copy(output)
      print("Tree copied to the clipboard")
    except Exception as e:
      print(f"Error copying tree to clipboard: {e}")
  else:
    print(output)

if __name__ == '__main__':
  main()
