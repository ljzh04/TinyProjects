import re
from pathlib import Path

LICENSE_DIR = Path("./templates/license")
BACKUP_DIR = Path("./templates/license_backup")
BACKUP_DIR.mkdir(exist_ok=True)


def jinja_to_str_format(text: str) -> str:
    # Convert {{ variable }} -> {variable}
    return re.sub(r"\{\{\s*(\w+)\s*\}\}", r"{\1}", text)


for file in LICENSE_DIR.glob("*.txt"):
    content = file.read_text(encoding="utf-8")
    converted = jinja_to_str_format(content)

    # Backup original
    backup_path = BACKUP_DIR / file.name
    backup_path.write_text(content, encoding="utf-8")

    # Overwrite with new format
    file.write_text(converted, encoding="utf-8")
    print(f"Converted: {file.name}")
