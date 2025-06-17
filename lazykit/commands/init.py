"""`lazykit init`"""

import os

from lazykit.core import config


def register(subparsers):
    parser = subparsers.add_parser("init", help="Initialize a lazykit project")
    parser.add_argument(
        "--path", default=".", help="Directory to initialize lazykit in"
    )
    parser.set_defaults(func=handle)


def handle(args):
    path = os.path.abspath(args.path)

    if not os.path.exists(path):
        os.makedirs(path)

    # Create settings file
    config_path = os.path.join(path, "settings.json")
    if not os.path.exists(config_path):
        config.write_default_config(config_path)
        print(f"[i] Created config at {config_path}")
    else:
        print(f"[?] Config already exists at {config_path}")
