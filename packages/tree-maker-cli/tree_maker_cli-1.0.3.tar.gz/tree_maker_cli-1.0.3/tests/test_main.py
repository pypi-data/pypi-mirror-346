import argparse
import os
import pytest
from unittest.mock import patch, mock_open
from tree_maker.__main__ import main
from tree_maker.tree import generate_tree
from tree_maker.config import EXCLUDED_FILES_FILE, load_excluded_files, save_excluded_files, DEFAULT_EXCLUDED_FILES

def setup_function():
  # Reset the excluded files to the default before each test
  save_excluded_files(DEFAULT_EXCLUDED_FILES.copy())

def teardown_function():
  # Remove the excluded files file after each test
  if os.path.exists(EXCLUDED_FILES_FILE):
    os.remove(EXCLUDED_FILES_FILE)

def test_main_default_args():
  with patch('tree_maker.tree.generate_tree', return_value="tree structure") as mock_generate_tree:
    with patch('builtins.print') as mock_print:
      with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(
          folder_path='.', depth=None, exclude=[], show_hidden=False, output=None, clipboard=False,
          add_excluded=[], remove_excluded=[], show_excluded=False
      )):
        main()
        # mock_generate_tree.assert_called_once_with('.', None, False, '│   ', DEFAULT_EXCLUDED_FILES)
        mock_print.assert_called_once_with('tree_maker_cli\n├── tests/\ntree structure├── tree_maker/\ntree structure├── tree_maker_cli.egg-info/\ntree structure├── LICENSE\n├── README.md\n├── excluded_files.json\n├── requirements.txt\n└── setup.py\n')

def test_main_output_to_file():
  with patch('tree_maker.config.open', mock_open(read_data='[]')) as mock_config_file:
    with patch('tree_maker.tree.generate_tree', return_value="tree structure") as mock_generate_tree:
      with patch('builtins.open', mock_open()) as mock_output_file:
        with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(
            folder_path='.', depth=None, exclude=[], show_hidden=False, output='output.txt', clipboard=False,
            add_excluded=[], remove_excluded=[], show_excluded=False
        )):
          main()
          mock_config_file.assert_called_once_with(EXCLUDED_FILES_FILE, 'r')
          mock_output_file.assert_called_once_with('output.txt', 'w')
          mock_output_file().write.assert_called_once_with('tree_maker_cli\n├── tests/\ntree structure├── tree_maker/\ntree structure├── tree_maker_cli.egg-info/\ntree structure├── LICENSE\n├── README.md\n├── excluded_files.json\n├── requirements.txt\n└── setup.py\n')

def test_main_clipboard():
  with patch('tree_maker.tree.generate_tree', return_value="tree structure") as mock_generate_tree:
    with patch('pyperclip.copy') as mock_copy:
      with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(
          folder_path='.', depth=None, exclude=[], show_hidden=False, output=None, clipboard=True,
          add_excluded=[], remove_excluded=[], show_excluded=False
      )):
        main()
        mock_copy.assert_called_once_with('tree_maker_cli\n├── tests/\ntree structure├── tree_maker/\ntree structure├── tree_maker_cli.egg-info/\ntree structure├── LICENSE\n├── README.md\n├── excluded_files.json\n├── requirements.txt\n└── setup.py\n')

def test_main_clipboard_exception():
  with patch('tree_maker.tree.generate_tree', return_value="tree structure") as mock_generate_tree:
    with patch('pyperclip.copy', side_effect=Exception("Clipboard error")) as mock_copy:
      with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(
          folder_path='.', depth=None, exclude=[], show_hidden=False, output=None, clipboard=True,
          add_excluded=[], remove_excluded=[], show_excluded=False
      )):
        with patch('builtins.print') as mock_print:
          main()
          mock_copy.assert_called_once_with('tree_maker_cli\n├── tests/\ntree structure├── tree_maker/\ntree structure├── tree_maker_cli.egg-info/\ntree structure├── LICENSE\n├── README.md\n├── excluded_files.json\n├── requirements.txt\n└── setup.py\n')

def test_remove_excluded_files(tmpdir):
  # Add some excluded files first
  with patch('sys.argv', ['tree_maker', '--add-excluded', 'file1', 'file2']):
    main()

  # Then test removing some of the excluded files
  with patch('sys.argv', ['tree_maker', '--remove-excluded', 'venv', 'dist', 'file1']):
    main()
  assert load_excluded_files() == ['__pycache__', 'node_modules', 'build', 'static', 'media', 'htmlcov', 'file2']

def test_show_excluded_files(capsys):
  with patch('sys.argv', ['tree_maker', '--show-excluded']):
    main()
  captured = capsys.readouterr()
  assert 'Current default excluded files/folders:' in captured.out
  assert '__pycache__' in captured.out
  assert 'node_modules' in captured.out
  assert 'build' in captured.out
  assert 'static' in captured.out
  assert 'media' in captured.out

