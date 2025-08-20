import argparse
from src.fetch import fetch
from src.build import build
from src.db import setup_tables

parser = argparse.ArgumentParser(prog="app")
subparsers = parser.add_subparsers(dest="command", required=True)

fetch_parser = subparsers.add_parser("fetch")
# add_parser.add_argument("x", type=int)
build_parser = subparsers.add_parser("build")


args = parser.parse_args()
setup_tables()

if args.command == "build":
    build()
if args.command == "fetch":
    fetch()

