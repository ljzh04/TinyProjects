""" CLI parser: maps commands to handlers"""
# ────────── Purpose ──────────
# Top-level commands
# Argument parsing
# Plugin registration
# Command dispatching
import argparse

from lazykit.commands import gen_license, gen_readme, tree

# from lazykit.plugins import load_plugins


def main():
    parser = argparse.ArgumentParser(prog="lazykit")
    subparsers = parser.add_subparsers(dest="command")

    # ───── Built-in Commands ─────
    gen_readme.register(subparsers)
    gen_license.register(subparsers)
    tree.register(subparsers)

    # ───── Plugin Commands ─────
    # load_plugins(subparsers)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
