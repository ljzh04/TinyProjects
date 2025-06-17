"""usage: lazykit gen-license [-h] [-c DIR] [-o FILE] [-t TYPE] [--overwrite]"""
import datetime
import pathlib

from lazykit import utils
from lazykit.core import context, generator


def register(subparsers):
    parser = subparsers.add_parser(
        "gen-license",
        help="Generate a LICENSE file for your project",
        formatter_class=lambda prog: utils.CustomFormatter(prog, max_help_position=36)
    )
    parser.add_argument(
        "-c", "--context",
        metavar="DIR",
        default=".",
        help="Project directory (default: current dir)"
    )
    parser.add_argument(
        "-o", "--output",
        metavar="FILE",
        default="LICENSE",
        help="Output filename (default: LICENSE)"
    )
    parser.add_argument(
        "-t", "--type",
        metavar="TYPE",
        default="mit",
        help="License type (e.g., mit, agpl3, apache) (default: mit)"
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow overwriting existing output file"
    )
    parser.set_defaults(func=handle)


def handle(args):
    tree = context.crawl_project_context(args.context)
    if not tree: # Add a check for None if crawl_project_context returns it
        print(f"[!] Could not crawl project context at '{args.context}'. Exiting.")
        return
    meta = context.get_metadata(tree)

    target_project_root = pathlib.Path(args.context).resolve()
    output_path = target_project_root / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists() and not args.overwrite:
        print(f"[!] File '{output_path}' already exists. Use --overwrite to replace it.")
        return

    template_vars = {
        "project": meta.get("project_name", "UNKNOWN"),
        "year": datetime.datetime.now().year,
        "organization": meta.get("author", meta.get("maintainer", "Your Name")),
    }
    print("[DEBUG] data passed to template:")
    for k, v in template_vars.items():
        print(f"  {k}: {v}")

    license_type = args.type.lower().strip()
    template_name = f"{license_type}.txt"

    generator.generate_from_template(
        template="license/"+template_name,
        output_path=str(args.output),
        context=template_vars,
    )
