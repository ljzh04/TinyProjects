""" Reads file trees, comments, and metadata for project context. """
# lazykit:description: This is a utility function.
# lazykit:author: Jane Doe
import ast
import fnmatch
import json
import mimetypes
import pathlib
import re

from .extractors import extract_content

# Use tomli for Python < 3.11, tomllib for 3.11+
try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore

# --- Constants ---
DEFAULT_EXCLUDE_DIRS = {'.git', '__pycache__', '.venv', 'node_modules', '.mypy_cache', 'dist', 'build'}
DEFAULT_EXCLUDE_FILES = {'.DS_Store'}
MAGIC_COMMENT_REGEX = re.compile(r"(#|//|<!--)\s*lazykit:(\w+):\s*(.*?)(\s*-->)?")

# --- Main Public Function ---
def crawl_project_context(
    root_path: str,
    extra_ignore_patterns: list[str] | None = None
) -> dict | None:
    # Resolve the root_path to its absolute form right at the beginning
    # This 'root' will be the base for all relative paths in the tree structure
    root = pathlib.Path(root_path).resolve()

    if extra_ignore_patterns is None: extra_ignore_patterns = []
    full_exclude, content_only_exclude = _load_ignore_rules(root, extra_ignore_patterns)

    def _crawl(path: pathlib.Path) -> dict | None:
        # Calculate relative path from the root *once*
        # This will be used for display and ignore pattern matching
        try:
            relative_to_root_str = str(path.relative_to(root)).replace("\\", "/").rstrip("/") #remove trailing slashes

        except ValueError:
            relative_to_root_str = str(path.relative_to(pathlib.Path.cwd())).replace("\\", "/").rstrip("/")

        if any(fnmatch.fnmatch(relative_to_root_str, pattern) for pattern in full_exclude):
            # print(f"[debug] Excluded: {relative_to_root_str}")  # debug - remove
            return None

        if path.name in DEFAULT_EXCLUDE_FILES: return None

        if path.is_dir():
            if path.name in DEFAULT_EXCLUDE_DIRS: return None

            children = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
            processed_children = filter(None, [_crawl(p) for p in children])
            return {
                "type": "directory",
                "name": path.name,
                "path": relative_to_root_str, # Store relative path for display
                "absolute_path": str(path.resolve()), # Store absolute path (resolved)
                "children": list(processed_children)
            }
        else: # It's a file
            mime_type, _ = mimetypes.guess_type(path)
            language = _infer_language(path.suffix, mime_type)

            file_data = {
                "type": "file",
                "name": path.name,
                "path": relative_to_root_str, # Store relative path for display
                "absolute_path": str(path.resolve()), # Store absolute path (resolved)
                "size": path.stat().st_size,
                "language": language,
            }
            # Pass the absolute pathlib.Path object to _extract_file_context
            return _extract_file_context(path, file_data, content_only_exclude)

    # The very top-level dictionary should represent the root itself
    crawled_tree = _crawl(root)
    # Ensure the root's 'path' is empty string and 'absolute_path' is its true resolved path
    if crawled_tree:
        crawled_tree["path"] = "" # The root directory's path relative to itself is empty
        crawled_tree["absolute_path"] = str(root) # The root directory's absolute path
    return crawled_tree


def get_metadata(project_tree: dict) -> dict:
    """Pulls metadata context from the tree / crawler."""
    if not project_tree: # Handle case where crawl_project_context returned None
        return {
            "project_name": "Unknown Project",
            "description": "No description available.",
            "license": "No license specified.",
            "module_name": "my_module",
        }

    root_files = project_tree.get("children", [])
    meta = {
        "project_name": "Unknown Project",
        "description": "No description available.",
        "license": "No license specified.", # Default fallback
        "module_name": pathlib.Path(project_tree.get("path") or ".").name, # This will be '' for the root
    }

    # Correct module_name for the actual project root name
    if project_tree.get("absolute_path"):
        meta["module_name"] = pathlib.Path(project_tree["absolute_path"]).name


    # Try to infer module_name from first .py file (excluding test or init)
    # This loop comes after setting module_name from project_root_abs to allow override
    for child in root_files:
        if child["type"] == "file" and child["name"].endswith(".py") and child["name"] not in {"__init__.py", "setup.py", "conftest.py"}:
            meta["module_name"] = child["name"].removesuffix(".py")
            break

    # --- 1. Process pyproject.toml/package.json for initial metadata (Name, Description, preliminary License) ---
    for child in root_files:
        if child["name"] == "pyproject.toml":
            m = child.get("metadata", {})
            meta["project_name"] = m.get("project_name") or meta["project_name"]
            if m.get("description"):
                meta["description"] = m.get("description")

            # Use license_from_toml if available
            if isinstance(m.get("license_from_toml"), dict):
                meta["license"] = m["license_from_toml"].get("text", m["license_from_toml"].get("file", meta["license"]))
            elif isinstance(m.get("license_from_toml"), str):
                meta["license"] = m.get("license_from_toml", meta["license"])
            break # Found and processed pyproject.toml


    # --- 2. Check for explicit LICENSE file and infer license type (highest priority) ---
    # This will override any license value pulled from pyproject.toml if successful.
    for child in root_files:
        if child["name"].lower().startswith("license") and child["type"] == "file":
            try:
                # Use the 'absolute_path' stored in the child dictionary for file operations
                absolute_license_path = pathlib.Path(child["absolute_path"])

                # Removed the extra print statement here to avoid cluttering debug output

                with open(absolute_license_path, encoding="utf-8") as f:
                    content = f.read(512)

                    # Robust detection with common license phrases
                    if "MIT License" in content or "The MIT License" in content:
                        meta["license"] = "MIT License"
                    elif "Apache License, Version 2.0" in content:
                        meta["license"] = "Apache License 2.0"
                    elif "GNU General Public License" in content:
                        meta["license"] = "GPL"
                    elif "BSD 3-Clause" in content or "New BSD License" in content:
                        meta["license"] = "BSD 3-Clause License"
                    elif "BSD 2-Clause" in content or "FreeBSD License" in content:
                        meta["license"] = "BSD 2-Clause License"
                    elif "Mozilla Public License" in content:
                        meta["license"] = "Mozilla Public License"
                    else:
                        meta["license"] = "Custom License"
                break # Found and processed license file, no need to check other license files

            except FileNotFoundError:
                print(f"[WARN] License file not found at expected path: {absolute_license_path}")
                pass
            except Exception as e:
                print(f"[WARN] Could not read or parse license file {absolute_license_path}: {e}")
                pass

    return meta
# -- todo: separate parsers (esp. license)


# --- Private Helper Functions ---
def _load_ignore_rules(root: pathlib.Path, extra_patterns: list[str]) -> tuple[set[str], set[str]]:
    # (This function is good, no changes needed)
    full_exclude, content_only_exclude = set(), set()
    patterns = extra_patterns[:]
    ignore_file = root / ".lazykitignore"
    if ignore_file.exists():
        try:
            patterns.extend(ignore_file.read_text().splitlines())
        except IOError:
            pass
    for pattern in patterns:
        pattern = pattern.strip()
        if not pattern or pattern.startswith("#"): continue
        if pattern.startswith("!"):
            content_only_exclude.add(pattern[1:].strip())
        else:
            full_exclude.add(pattern)
    return full_exclude, content_only_exclude


def _extract_file_context(path: pathlib.Path, file_data: dict, content_ignore_patterns: set[str], strategy: str = "trimmed") -> dict:
    """Dispatcher to parse a file based on its type and enrich its metadata."""
    file_data['summary'] = None
    file_data['metadata'] = {}

    if any(fnmatch.fnmatch(file_data['path'], pat) for pat in content_ignore_patterns):
        file_data['summary'] = "Content ignored by .lazykitignore pattern."
        return file_data
    if file_data['size'] > 1_000_000:
        file_data['summary'] = "File is too large to parse."
        return file_data

    try:
        content = path.read_text(encoding='utf-8')
    except (UnicodeDecodeError, IOError):
        file_data['summary'] = "File is binary or could not be read."
        return file_data

    if re.search(r"(#|//|<!--)\s*lazykit:ignore", content):
        file_data['summary'] = "File content parsing disabled by magic comment."
        return file_data

    # --- FIX: LOGIC CHANGED TO BE ADDITIVE, NOT OVERRIDING ---

    # 1. Capture the auto-detected summary (e.g., from docstring) first.
    if file_data['language'] == 'Python':
        file_data['summary'] = _get_python_docstring_summary(content)

    # 2. Capture ALL magic comments and add them to metadata.
    #    This ensures `description` is preserved as metadata even if a summary exists.
    magic_comments = {key: value.strip() for _, key, value, _ in MAGIC_COMMENT_REGEX.findall(content)}
    if magic_comments:
        file_data['metadata'].update(magic_comments)

    # 3. Parse file-specific metadata (like pyproject.toml fields), which is additive.
    #    These will only set a summary if one does not already exist from a docstring.
    if file_data['name'] == 'pyproject.toml':
        _parse_pyproject_toml(content, file_data)
    elif file_data['name'] == 'package.json':
        _parse_package_json(content, file_data)

    # Extract trimmed content for LLM-friendly use
    file_data["content"] = extract_content(content, file_data['language'], strategy="trimmed")
    return file_data


def _infer_language(suffix: str, mime_type: str | None) -> str:
    # (This function is good, no changes needed)
    ext = suffix.lower()
    mapping = {".py": "Python", ".pyw": "Python", ".md": "Markdown", ".js": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript", ".ts": "TypeScript", ".tsx": "TypeScript", ".html": "HTML", ".css": "CSS", ".json": "JSON", ".toml": "TOML", ".yaml": "YAML", ".yml": "YAML", ".sh": "Shell", ".bash": "Shell", ".rs": "Rust", ".go": "Go", ".java": "Java", ".c": "C", ".h": "C", ".cpp": "C++", ".hpp": "C++"}
    return mapping.get(ext, mime_type or "unknown")


def _get_python_docstring_summary(content: str) -> str | None:
    """Extracts the first line of a module-level docstring from a Python file."""
    try:
        tree = ast.parse(content)
        docstring = ast.get_docstring(tree)
        if docstring:
            return docstring.strip().split('\n')[0]
    except SyntaxError:
        pass # Ignore syntax errors, just won't get a summary
    return None


def _parse_pyproject_toml(content: str, file_data: dict):
    """Extracts and adds key metadata from a pyproject.toml file."""
    try:
        data = tomllib.loads(content)
        project_meta = data.get('project', {})
        # Add to existing metadata, don't overwrite other magic comments
        file_data['metadata'].update({
            'project_name': project_meta.get('name'),
            'version': project_meta.get('version'),
            'license': project_meta.get('license'),
        })
        # The project description is a great summary for the file itself.
        # This will only be used if no summary (e.g., docstring) was found.
        if not file_data.get('summary') and project_meta.get('description'):
            file_data['summary'] = project_meta.get('description')
    except tomllib.TOMLDecodeError:
        pass


def _parse_package_json(content: str, file_data: dict):
    """Extracts and adds key metadata from a package.json file."""
    try:
        data = json.loads(content)
        file_data['metadata'].update({
            'project_name': data.get('name'),
            'version': data.get('version'),
            'author': data.get('author'),
            'license': data.get('license'),
        })
        if not file_data.get('summary') and data.get('description'):
            file_data['summary'] = data.get('description')
    except json.JSONDecodeError:
        pass
