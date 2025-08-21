import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from .db import save_cours
from .cours import Cours, fetch_html, BASE_URL
import os

cours = {}

def fetch(PROGRAMMES):
    for (url, program, _) in PROGRAMMES:
        soup = fetch_html(url)
        links = soup.findAll("a")
        links = [l for l in links if "cours-2025" in (l.get("href") or "")]
        print(f"Fetching {len(links)} cours from {url}")
        for l in tqdm(links):
            href = l.get("href")
            if not href in cours.keys():
                cours[href] = Cours.from_link(l)
            cours[href].add_program(program)
    save_cours(cours)

