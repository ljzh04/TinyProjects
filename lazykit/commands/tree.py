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

    parser.set_defaults(func=handle)


def handle(args):
    crawl = context.crawl_project_context
    display = utils.display_project_context if args.long else utils.display_file_tree

    # Apply exclusions
    if args.no_defaults:
        tree = crawl(
            args.context,
            exclude_dirs=set(args.exclude_dir),
            exclude_files=set(args.exclude_file)
        )
    else:
        tree = crawl(args.context)

    display(tree)
