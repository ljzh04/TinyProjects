"""usage: lazykit gen-readme [-h] [-c DIR] [-o FILE] [--overwrite]"""
import os
import pathlib

from lazykit.core import context, generator
from lazykit.core.context import crawl_project_context


def register(subparsers):
    parser = subparsers.add_parser(
        "gen-readme",
        help="Generate a README file",
    )
    parser.add_argument(
        "-c", "--context",
        metavar="DIR",
        help="Project root (default: current directory)",
        default=".",
    )
    parser.add_argument(
        "-o", "--output",
        metavar="FILE",
        help="Path to output README file (default: ./README.md)",
        default="README.md",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow overwriting the output file",
    )

    parser.set_defaults(func=handle)


def handle(args):
    tree = crawl_project_context(args.context)
    if not tree: # Add a check for None if crawl_project_context returns it
        print(f"[!] Could not crawl project context at '{args.context}'. Exiting.")
        return
    project = context.get_metadata(tree)

    # Use pathlib for output_path construction for consistency
    # args.context is the string path provided by the user (e.g., 'lazykit/__TestProjDir__/')
    # pathlib.Path(args.context).resolve() ensures we have an absolute, resolved path to the target directory
    target_project_root = pathlib.Path(args.context).resolve()
    output_path = target_project_root / args.output # Correctly join the absolute root with the output file name

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists() and not args.overwrite:
        print(f"[!] File '{output_path}' already exists. Use --overwrite to replace it.")
        return

    # Fallbacks - These should now correctly get values from the improved get_metadata
    license_text = project.get("license", "MIT License") # Default if get_metadata still fails
    description_text = project.get("description", "A Python project.") # Default if get_metadata still fails

    data = {
        "project_name": project.get("project_name", "MyProject"),
        "description": description_text,
        "module_name": project.get("module_name", "my_module"),
        "license": license_text,
    }
    print("[DEBUG] data passed to template:")
    for k, v in data.items():
        print(f"  {k}: {v}")

    generator.generate_from_template(
        template="readme/readme.md.tpl",
        output_path=str(output_path), # generator likely expects a string
        context=data,
    )

    print(f"[✓] README generated at: {output_path}")
