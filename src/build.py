from .db import read_cours_from_db
from .cours import Cours

import shutil
from pathlib import Path
from jinja2 import Environment,FileSystemLoader
import re
import unicodedata

def slugify(value):
    value = str(value)
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value

env = Environment(loader=FileSystemLoader("templates"))
env.filters["slugify"] = slugify

list_template = env.get_template("list.jinja2")
index_template = env.get_template("index.jinja2")
cours_template = env.get_template("cours.jinja2")

count = 0

def compile_page(template, data, output_name):
    global count
    count += 1
    r = template.render(data)
    with open(f"dist/{output_name}","w") as f:
        f.write(r)

def build(PROGRAMMES):
    colors = {nom: color for (_, nom, color) in PROGRAMMES}
    folder_path = Path("dist")
    folder_path.mkdir(parents=True, exist_ok=True)
    cours = read_cours_from_db().values()
    cours = sorted(cours, key=lambda x: len(x.programs))
    print("Building...")
    compile_page(list_template, {"cours": cours, "colors": colors}, "all.html")
    compile_page(index_template, {"colors": colors}, "index.html")
    for c in cours:
        compile_page(cours_template, {
                     "cours": c,
                     "colors": colors
                 }, f"{c.code}.html")
    for program in colors.keys():
        compile_page(list_template, {
                     "program": program,
                     "cours": [c for c in cours if program in c.programs]
                 }, f"{slugify(program)}.html")
    print(f"Done ! Built {count} pages inside the dist/ directory.")
        
        
        
