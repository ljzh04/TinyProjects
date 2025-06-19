## How to Use the `gen-license` Command in Lazykit

This document explains how to use the `gen-license` command in Lazykit to generate a standard LICENSE file for your project. You can choose from several common license templates, and the command will automatically fill in details like the current year and author's name.

### Command Overview

The `lazykit gen-license` command provides a quick and standardized way to add a license to your project. It uses pre-defined templates for popular open-source licenses (like MIT, AGPL-3.0, Apache, etc.) and populates them with metadata discovered in your project, such as the author's name found in `pyproject.toml`.

### Usage

```bash
lazykit gen-license [OPTIONS]
```

### Options

*   `-c, --context <DIR>`:
    Specifies the root directory of the project to scan for metadata (like author name).
    **Default:** `.` (current directory).

*   `-o, --output <FILE>`:
    Specifies the name of the output file to be generated. This path is relative to the context directory (`-c`).
    **Default:** `LICENSE`.

*   `-t, --type <TYPE>`:
    Specifies the type of license to generate. The value should correspond to a template name.
    **Examples:** `mit`, `apache`, `agpl-3.0`
    **Default:** `mit`.

*   `--overwrite`:
    Allows the command to overwrite an existing LICENSE file at the output path. If the file exists and this flag is not provided, the command will exit with a warning.

### Examples

1.  **Generate a Default MIT License:**
    Create a standard `LICENSE` file using the default MIT license template in the current directory.

    ```bash
    lazykit gen-license
    ```

2.  **Generate an Apache License:**
    Use the `-t` flag to specify a different license type, such as the Apache 2.0 license.

    ```bash
    lazykit gen-license -t apache
    ```

3.  **Generate a License for a Different Project:**
    Target a different project directory to scan its metadata and place the `LICENSE` file within it.

    ```bash
    lazykit gen-license -c ../my-other-project
    ```

4.  **Overwrite an Existing License File:**
    If a `LICENSE` file already exists, use the `--overwrite` flag to force its replacement.

    ```bash
    lazykit gen-license -t mit --overwrite
    ```

5.  **Complex Example: Custom Type, Path, and Output Name:**
    Generate an AGPL-3.0 license for a project in the `./backend` directory and save it as `COPYING` instead of `LICENSE`.

    ```bash
    lazykit gen-license -c ./backend -t agpl-3.0 -o COPYING
    ```

### How Information is Sourced

The `gen-license` command populates the license template with automatically discovered information.

*   **License Template:** The value passed to the `--type` flag (e.g., `mit`) is used to select a corresponding template file (e.g., `license/mit.txt.tpl`) from Lazykit's internal templates.

*   **Template Variables:** The selected template is populated with the following data:
    *   **`{year}`:** Automatically filled with the current year.
    *   **`{organization}`:** Filled with the author or maintainer's name. This information is sourced by scanning for metadata in files like `pyproject.toml`. If no author is found, it falls back to a placeholder.

*   **Project Scanning:**
    The command uses the same underlying project-crawling mechanism as `lazykit tree` and `lazykit gen-readme`. This allows it to automatically find project metadata to use in the license file.
