## How to Use the `gen-readme` Command in Lazykit

This document explains how to use the `gen-readme` command in Lazykit to quickly generate a professional `README.md` file for your project. It automatically scans your project for metadata in files like `pyproject.toml` and `LICENSE` to populate a standardized template.

### Command Overview

The `lazykit gen-readme` command analyzes your project's structure and metadata files to create a well-formatted `README.md`. It intelligently pulls the project name, description, license, and primary module information to save you from writing common boilerplate. The output is generated from a built-in template.

### Usage

```bash
lazykit gen-readme [OPTIONS]
```

### Options

*   `-c, --context <DIR>`:
    Specifies the root directory of the project to scan.
    **Default:** `.` (current directory).

*   `-o, --output <FILE>`:
    Specifies the name of the output file to be generated. This path is relative to the context directory (`-c`).
    **Default:** `README.md`.

*   `--overwrite`:
    Allows the command to overwrite an existing README file at the output path. If the output file exists and this flag is not provided, the command will exit with a warning.

### Examples

1.  **Basic README Generation:**
    Generate a `README.md` in the current directory by scanning its contents.

    ```bash
    lazykit gen-readme
    ```

2.  **Generate for a Different Project Directory:**
    Scan a project located in a different directory and generate the `README.md` inside that directory.

    ```bash
    lazykit gen-readme -c ../my-other-project
    ```

3.  **Specify a Custom Output File Name:**
    Generate a README file but name it `PROJECT_INFO.md` instead of the default.

    ```bash
    lazykit gen-readme -o PROJECT_INFO.md
    ```

4.  **Overwriting an Existing File:**
    If `README.md` already exists, the command will not replace it by default. Use the `--overwrite` flag to force regeneration.

    ```bash
    lazykit gen-readme --overwrite
    ```

5.  **Combining Options for Advanced Use:**
    Scan the `src` directory but generate the `README.md` file in the parent directory of `src`, overwriting it if it already exists.

    ```bash
    lazykit gen-readme -c ./src -o ../README.md --overwrite
    ```

### How Information is Sourced

The `gen-readme` command populates the README template by extracting metadata from your project in a specific order of priority.

*   **Project Name & Description:**
    *   Primarily sourced from the `name` and `description` fields in the `[project]` section of a `pyproject.toml` file.
    *   Falls back to `name` and `description` in `package.json` if `pyproject.toml` is not found.
    *   If neither is found, it uses placeholder text like "Unknown Project".

*   **License:**
    The license is determined using the following priority:
    1.  **`LICENSE` File:** It first looks for a file named `LICENSE`, `LICENSE.md`, etc., in the project root. If found, it reads the first few lines to identify common licenses (MIT, Apache 2.0, GPL, etc.). This is the most reliable source.
    2.  **`pyproject.toml`:** If no `LICENSE` file is found, it will use the `license` field from `pyproject.toml`.
    3.  **Default:** If no license can be determined, it defaults to a placeholder.

*   **Module Name:**
    This is inferred to provide a basic installation or usage instruction. It's typically derived from the name of the project's root directory.

*   **Project Scanning:**
    The command uses the same underlying project-crawling mechanism as `lazykit tree`. This means it automatically respects ignore rules specified in a `.lazykitignore` file and skips default directories like `.git` and `__pycache__`.
