from .db import read_cours_from_db
from .cours import Cours

import shutil
from pathlib import Path
from jinja2 import Environment,FileSystemLoader


env = Environment(loader=FileSystemLoader("templates"))

index_template = env.get_template("index.jinja2")
cours_template = env.get_template("cours.jinja2")

def compile_page(template, data, output_name):
    r = template.render(data)
    with open(f"dist/{output_name}","w") as f:
        f.write(r)

def build():
    folder_path = Path("dist")
    shutil.rmtree(folder_path, ignore_errors=True);
    folder_path.mkdir(parents=True, exist_ok=True)
    cours = read_cours_from_db()
    print("Building...")
    compile_page(index_template, {"cours": cours.values()}, "index.html")
    for c in cours.values():
        compile_page(cours_template, {"cours": c}, f"{c.code}.html")
        
