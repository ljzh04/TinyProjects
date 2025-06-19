## How to Use the `tree` Command in Lazykit

This document explains how to use the `tree` command in Lazykit to visualize your project's directory structure, with options for detailed context and exclusions.

### Command Overview

The `lazykit tree` command provides a structured view of your project, similar to the `tree` utility, but with enhanced capabilities to extract and display project-specific metadata and summaries.

### Usage

```bash
lazykit tree [OPTIONS]
```

### Options

*   `-c, --context <DIR>`:
    Specifies the root directory to scan.
    **Default:** `.` (current directory).

*   `-x, --exclude-dir <DIR> [<DIR>...]`:
    One or more additional directory names to exclude from the tree. These are applied in addition to the default exclusions.

*   `-X, --exclude-file <FILE> [<FILE>...]`:
    One or more additional file names to exclude from the tree. These are applied in addition to the default exclusions.

*   `-n, --no-defaults`:
    Disables the default set of built-in exclusions. When this flag is present, directories like `.git` and `__pycache__` will be included in the output unless they are manually excluded with `-x`.
    **Default Exclusions (hidden by default):**
    *   **Directories:** `.git`, `__pycache__`, `.venv`, `node_modules`, `.mypy_cache`, `dist`, `build`
    *   **Files:** `.DS_Store`

*   `-l, --long`:
    Enables "long" format output. This flag triggers a more intensive crawl that extracts and displays additional information for each file, including file size, inferred language, summaries (from docstrings, `lazykit:description` magic comments, etc.), and other extracted metadata.

### Examples

1.  **Basic Tree View:**
    Display a tree structure of the current directory. This automatically uses the default exclusions, hiding directories like `.git` and `node_modules`.

    ```bash
    lazykit tree
    ```

2.  **Tree View Without Default Exclusions:**
    Show the complete, unfiltered tree, including normally hidden directories like `__pycache__` and `.git`.

    ```bash
    lazykit tree -n
    ```

3.  **Tree View with Additional Exclusions:**
    Display the tree while excluding the `docs` and `tests` directories in addition to the built-in defaults.

    ```bash
    lazykit tree -x docs tests
    ```

4.  **Tree View Excluding Specific Files:**
    Display the tree while excluding `README.md` and any `temp.txt` files, in addition to the built-in defaults.

    ```bash
    lazykit tree -X README.md temp.txt
    ```

5.  **Long Format (Detailed Context):**
    Get a comprehensive view of your project, including file sizes and summaries. This still uses the default exclusions.

    ```bash
    lazykit tree --long
    ```

6.  **Long Format with Additional Exclusions:**
    Combine detailed output with an additional directory exclusion.

    ```bash
    lazykit tree --long -x build
    ```

7.  **Long Format from a Different Context with Custom Exclusions:**
    Crawl the `my_project` directory, show detailed context, and exclude the `dist` directory and any `config.json` files.

    ```bash
    lazykit tree -c my_project --long -x dist -X config.json
    ```

### How Information is Extracted (`--long` format)

*   **Python Files (`.py`):** The first line of the module-level docstring is used as the summary.
*   **`pyproject.toml`:** Extracts `project_name`, `version`, `description`, `authors`, and `license` from the `[project]` section. The `description` is used as the file summary.
*   **`package.json`:** Extracts `name`, `version`, `description`, `author`, and `license`. The `description` is used as the file summary.
*   **Magic Comments:** For any text file, comments in the format `# lazykit:key: value` are parsed and added to the file's metadata. For example, `# lazykit:description: Your file description.` will append to the file's information.
*   **File Size:** Automatically included for all files.
*   **Language:** Inferred from the file extension (e.g., `.py` -> Python, `.js` -> JavaScript).
