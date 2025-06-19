"""usage: `lazykit tree [-h] [-c DIR] [-x [DIR ...]] [-X [FILE ...]] [-n] [-l]`"""
from lazykit import utils
from lazykit.core import context


def register(subparsers):
    parser = subparsers.add_parser(
        "tree",
        help="Show project file tree",
        formatter_class=lambda prog: utils.CustomFormatter(prog, max_help_position=36)
    )

    parser.add_argument(
        "-c", "--context",
        metavar="DIR",
        help="Root directory to scan (default: current directory)",
        default=".",
        dest='context'
    )
    parser.add_argument(
        "-x", "--exclude-dir",
        metavar="DIR",
        nargs="*",
        help="Additional directories to exclude",
        default=[],
        dest='exclude_dir'
    )
    parser.add_argument(
        "-X", "--exclude-file",
        metavar="FILE",
        nargs="*",
        help="Additional files to exclude",
        default=[],
        dest='exclude_file'
    )
    parser.add_argument(
        "-n", "--no-defaults",
        action="store_true",
        help="Don't use builtin exclusions",
        dest='no_defaults'
    )
    parser.add_argument(
        "-l", "--long",
        action="store_true",
        help="Show extended file info",
        dest='long'
    )
    parser.add_argument(
        "-s", "--show-content",
        action="store_true",
        help="Show file preview",
        dest='content')

    parser.set_defaults(func=handle)


def handle(args):
    crawl = context.crawl_project_context
    display = utils.display_project_context if args.long else utils.display_file_tree

    extra_ignore = []

    # Process each exclude directory to match both the directory itself and its contents.
    for pattern in args.exclude_dir:
        normalized = pattern.rstrip("/")
        extra_ignore.append(normalized)         # Matches the directory node (e.g., "__TestProjDir__")
        extra_ignore.append(f"{normalized}/*")    # Matches all items inside

    # Process exclude files similarly (if needed)
    for pattern in args.exclude_file:
        extra_ignore.append(pattern)

    tree = crawl(args.context, extra_ignore_patterns=extra_ignore)
    display(tree, show_content=args.content)
