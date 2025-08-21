import requests
from bs4 import BeautifulSoup

BASE_URL = "https://uclouvain.be/"

def fetch_html(url):
        # print(f"{BASE_URL}{url}")
        r = requests.get(f"{BASE_URL}{url}")
        if (r.status_code != 200):
            raise Exception((url, r))
        soup = BeautifulSoup(r.text, "html.parser")
        return soup


class Cours:
    def __init__(self, name, url, code=None, description=None, content=None, programs=None, teachers=None):
        self.name = name
        self.url = url
        self.code = code if code else self.url.split("-")[-1].upper()
        self.description = description
        self.content = content
        self.teachers = teachers
        self.programs = programs
        if self.programs == None:
            self.programs = []

    @classmethod
    def from_link(cls, name, url):
        instance = cls(name, url)
        instance.fetch_info()
        return instance

    def add_program(self, program):
        if not program in self.programs:
            self.programs.append(program)

    def parse_info(self, soup, name):
        try:
            div = soup.find("div", string=lambda t: name in t)
            return div.find_next_sibling("div").text.strip()
        except:
            return None
        

    def fetch_info(self):
        soup = fetch_html(self.url)
        self.description = self.parse_info(soup, "Thèmes abordés")
        self.content = self.parse_info(soup, "Contenu")
        self.teachers = self.parse_info(soup, "Enseignants")


