import json

DEFAULT_EXCLUDED_FILES = [
  '__pycache__', 'venv', 'node_modules', 'dist', 'build', 'static', 'media', 'htmlcov'
]

EXCLUDED_FILES_FILE = 'excluded_files.json'

def load_excluded_files():
  try:
    with open(EXCLUDED_FILES_FILE, 'r') as file:
      return json.load(file)
  except (FileNotFoundError, json.JSONDecodeError):
    return DEFAULT_EXCLUDED_FILES

def save_excluded_files(files):
  with open(EXCLUDED_FILES_FILE, 'w') as file:
    json.dump(files, file)

def add_default_excluded_files(files):
  excluded_files = load_excluded_files()
  excluded_files.extend(files)
  save_excluded_files(excluded_files)

def remove_default_excluded_files(files):
  excluded_files = load_excluded_files()
  for file in files:
    if file in excluded_files:
      excluded_files.remove(file)
  save_excluded_files(excluded_files)
