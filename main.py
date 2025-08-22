import argparse, os, sys,sqlite3
from src.fetch import fetch
from src.build import build
from src.db import setup_tables, clear_database, DB_FILE

parser = argparse.ArgumentParser(prog="app")
subparsers = parser.add_subparsers(dest="command", required=True)

fetch_parser = subparsers.add_parser("fetch")
build_parser = subparsers.add_parser("build")

PROGRAMMES = [
    ("/prog-2025-fsa1ba-programme_annual_blocks", "Bachelier Ingénieur Civil", "#7ed6df"),
    ("/prog-2025-sinf1ba-programme_annual_blocks", "Bachelier Sciences de l'informatique", "#ffbe76"),
    ("/prog-2025-map2m-programme", "Master MAP", "salmon"),
    ("/prog-2025-elec2m-programme", "Master ELEC", "lightblue"),
    ("/prog-2025-info2m-programme", "Master INFO", "lightgreen"),
    ("/prog-2025-gbio2m-programme", "Master GBIO", "orange"),
]


args = parser.parse_args()

if args.command == "build":
    try:
        build(PROGRAMMES)
    except sqlite3.OperationalError:
        print("Invalid database. Please run fetch before.")
if args.command == "fetch":
    clear_database()
    setup_tables()
    fetch(PROGRAMMES)

