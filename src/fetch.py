import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from .db import save_cours
from .cours import Cours, fetch_html, BASE_URL

URLS = [
    "/prog-2025-map2m-programme",
    "/prog-2025-elec2m-programme",
    "/prog-2025-info2m-programme",
    "/prog-2025-gbio2m-programme",
]

cours = {}

def fetch():
    for url in URLS:
        soup = fetch_html(url)
        links = soup.findAll("a")
        links = [l for l in links if "cours-2025" in (l.get("href") or "")]
        print(f"Fetching {len(links)} cours from {url}")
        for l in tqdm(links):
            if not l.get("href") in cours:
                cours[l.get("href")] = Cours.from_link(l)
    save_cours(cours)

