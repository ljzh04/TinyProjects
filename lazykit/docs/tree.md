## How to Use the `tree` Command in Lazykit

This document explains how to use the `tree` command in Lazykit to visualize your project's directory structure, with options for detailed context and exclusions.

### Command Overview

The `lazykit tree` command provides a structured view of your project, similar to the `tree` utility, but with enhanced capabilities to extract and display project-specific metadata and summaries.

### Usage

```bash
lazykit tree [OPTIONS]
```

### Options

* `-c, --context <path>`:
    Specifies the root directory to crawl.
    **Default:** `.` (current directory).

* `-p, --path <path> [<path>...]`:
    One or more directory paths to exclude from the tree.
    This option is ignored if `--exclude` is used.

* `-f, --file <file> [<file>...]`:
    One or more file names to exclude from the tree.
    This option is ignored if `--exclude` is used.

* `-e, --exclude`:
    Activates the default set of exclusions. When this flag is present, any paths or files specified with `-p` or `-f` are ignored.
    **Default Exclusions:**
    * Directories: `.git`, `__pycache__`, `.venv`, `node_modules`, `.mypy_cache`
    * Files: `.DS_Store`

* `-l, --long`:
    Enables "long" format output. This flag triggers a more intensive crawl that extracts and displays additional information for each file, including:
    * File size
    * Inferred programming language
    * A concise summary (e.g., from Python docstrings, `description` in `package.json` or `pyproject.toml`, or `lazykit:description` magic comments).
    * Extracted metadata (e.g., project name, version, authors/author, license from `pyproject.toml` or `package.json`).
    * Magic comments (e.g., `# lazykit:key: value`) from any text file.

### Examples

1.  **Basic Tree View:**
    Display a simple tree structure of the current directory, without any special exclusions or extra details.

    ```bash
    lazykit tree
    ```

2.  **Tree View with Default Exclusions:**
    Show the tree, automatically excluding common directories like `.git`, `node_modules`, `__pycache__`, etc.

    ```bash
    lazykit tree --exclude
    ```

3.  **Tree View Excluding Specific Directories:**
    Display the tree while excluding the `docs` and `tests` directories.

    ```bash
    lazykit tree -p docs tests
    ```

4.  **Tree View Excluding Specific Files:**
    Display the tree while excluding `README.md` and `temp.txt` files.

    ```bash
    lazykit tree -f README.md temp.txt
    ```

5.  **Long Format (Detailed Context):**
    Get a comprehensive view of your project, including file sizes, summaries, and extracted metadata for relevant files. This is particularly useful for understanding the high-level purpose of files and modules.

    ```bash
    lazykit tree --long
    ```

6.  **Long Format with Default Exclusions:**
    Combine detailed output with the default set of directory and file exclusions.

    ```bash
    lazykit tree --long --exclude
    ```

7.  **Long Format and Specific Exclusions from a different context:**
    Crawl the `my_project` directory, show detailed context, and exclude the `dist` directory and any `config.json` files.

    ```bash
    lazykit tree -c my_project --long -p dist -f config.json
    ```

### How Information is Extracted (`--long` format)

* **Python Files (`.py`):** The first line of the module-level docstring is used as the summary.
* **`pyproject.toml`:** Extracts `project_name`, `version`, `description`, `authors`, and `license` from the `[project]` section. The `description` is used as the file summary.
* **`package.json`:** Extracts `name`, `version`, `description`, `author`, and `license`. The `description` is used as the file summary.
* **Magic Comments:** For any text file, comments in the format `# lazykit:key: value` are parsed and added to the file's metadata. Specifically, `# lazykit:description: Your file description.` will override any other parsed summary for that file.
* **File Size:** Automatically included for all files.
* **Language:** Inferred from the file extension (e.g., `.py` -> Python, `.js` -> JavaScript).
