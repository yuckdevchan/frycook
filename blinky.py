from pathlib import Path
import json

import linky

def get_seen_domains(web) -> list:
    l = []
    for domain in web.keys():
        try:
            l.append(linky.link_to_domain(domain))
        except IndexError: pass
        for domain_pair in web[domain]:
            try:
                l.append(linky.link_to_domain(domain_pair))
            except IndexError: pass
    l = list(set(l))
    return l

def get_seen_pages(web) -> list:
    l = []
    for branch in web:
        for leaf in branch:
            l.append(leaf)
    return l

def compile_data():
    """
    Compiles the data from the web dictionary parts into a single dictionary.
    """
    web = {}
    for f in Path("data").glob("web*"):
        try:
            with open(f, "r") as f:
                data = json.load(f)
                web.update(data)
        except json.JSONDecodeError:
            pass
        Path(str(f.name)).unlink()
    print("Compiled data into one structure.")
    return web

def write_data(data):
    """
    Writes the compiled data to a JSON file.
    """
    with open(Path("data/web.json"), "w") as f:
        json.dump(data, f, indent=4)
    print("Data written to data/web.json.")

def clean_data():
    for f in Path("data").glob("web-*.json"):
        Path("data/" + str(f.name)).unlink()
    print("Cleaned up old data files.")

if __name__ == "__main__":
    write_data(compile_data())
    with open(Path("data/web.json"), "r") as f:
        web = json.load(f)
    print(len(get_seen_domains(web)))
