# Tree Maker CLI

[![codecov](https://codecov.io/gh/tecz/tree_maker_cli/graph/badge.svg?token=3MCL0EZ179)](https://codecov.io/gh/tecz/tree_maker_cli)

A command-line tool to generate a tree structure of a folder and its contents, useful for when you need to add context to your GPT prompts.

## Features

- Generates a visual representation of a directory's structure
- Supports customizable depth limiting
- Allows excluding specific files and directories
- Provides options to include or exclude hidden files
- Output can be saved to a file or copied to the clipboard

## Usage

### Installation

Install via `pip`:

```sh
pip install tree-maker-cli
```

### Using this tool

Once installed, you can call the tool with the command

```sh
tree-maker [options] [directory]
```

If called without arguments, it will print the tree structure from the current folder. If called with a valid folder path, it will print the tree structure from that location.

```sh
tree-maker /path/to/folder
```

#### Arguments

The following arguments are available:
 + `--depth`: Sets the depth of the tree structure to print
 + `--clipboard` (or `-c`): Copy the tree to the clipboard
 + `--output` (or `-o`): Set the output file path
 + `--exclude`: Files and/or folders to exclude from the tree
 + `--show-hidden`: Show hidden files in the tree structure
 + `--show-excluded`: Show a list of the files/folders excluded from the tree by default
 + `--add-excluded`: Add files or folders to the list of files and folders excluded by default
 + `--remove-excluded`: Remove files or folders from the list of files/folders excluded by default

For example, to print a tree of depth two with hidden files and excluding the folders `public`, `tmp`, and `log` and then copy it to the clipboard:

```sh
tree-maker --depth=2 -c --show-hidden /path/to/your/app --exclude public tmp log
```

To save to a text file:

```sh
tree-maker [arguments] --output path/to/output.txt
```

## License

This project is licensed under the [MIT License](LICENSE).
