"""Generates files based from a template"""
import os
from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent.parent / "templates"


def generate_from_template(template: str, output_path: str, context: dict):
    """Generate a file from a template path relative to the templates/ folder."""
    base_dir = os.path.dirname(os.path.dirname(__file__))  # gets the lazykit/ root
    template_path = os.path.join(base_dir, "templates", template)

    with open(template_path, "r", encoding="utf-8") as f:
        template_str = f.read()

    rendered = template_str.format(**context)

    with open(output_path, "w", encoding="utf-8") as out:
        out.write(rendered)


def get_template_path():
    return TEMPLATE_DIR


def load_template(name: str | Path) -> str:
    """Loads template content by name or path."""
    path = Path(name)
    if not path.exists():
        # Load from built-in templates
        path = TEMPLATE_DIR / f"{name}.md.tpl"
    return path.read_text()


def write_output(path: Path, content: str, overwrite: bool = False) -> bool:
    if path.exists() and not overwrite:
        return False
    path.write_text(content)
    return True
