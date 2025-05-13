import json, sys, subprocess, random
from pathlib import Path

import blinky, linky


if Path("stop").exists(): Path("stop").unlink()

with open("seeds.json", "r") as f:
    seeds = json.load(f)

h = "https://"
for i in range(len(seeds)): seeds[i] = h + seeds[i]
starting_node = sys.argv[1] if len(sys.argv) > 1 else seeds[0]
counter = int(sys.argv[2] if len(sys.argv) > 2 else 0)

if starting_node == seeds[0]:
    counter = 0
    for seed in seeds:
        if seed == starting_node:
            continue
        counter += 1
        try:
            subprocess.Popen(f"python main.py {seed} {counter}", shell=True)
        except Exception as e:
            print(f"Error starting subprocess for {seed} {counter}: {e}")
            continue
    counter = 0

print(f"Starting crawler on {starting_node} (Thread {counter})")

web = {starting_node: []}
extra = []

if Path(f"data/web-{counter}.json").exists():
    with open(f"data/web-{counter}.json", "r") as f:
        old_web = json.load(f)
        web.update(old_web)
        print("Web data loaded and merged successfully.")

class CrawlerState:
    def __init__(self):
        self.saving = False

state = CrawlerState()

def save(state):
    if state.saving:
        return
    state.saving = True
    if Path(f"data/web-{counter}.json").exists():
        with open(f"data/web-{counter}.json", "r") as f:
            old_web = json.load(f)
            web.update(old_web)

    with open(f"data/web-{counter}.json", "w") as f:
        to_dump = web
        json.dump(to_dump, f, indent=4)
    sys.exit(0)

seen_domains = blinky.get_seen_domains(web)

def crawl_node(node, depth=0):
    if Path("stop").exists():
        print(f"Stop file detected. Exiting... (Thread {counter})")
        save(state)
    print(f"{"-"*depth if depth < 30 else "-"*30}x{depth} Crawling: {node}")
    links = linky.get_links(node)
    if not links:
        print(f"No links found on {node}. Skipping...")
        return
    web[node] = links

    for link in links:
        try:
            domain = linky.link_to_domain(link)
            if domain not in seen_domains:
                seen_domains.append(domain)
                web[link] = []
                crawl_node(link, depth + 1)
        except Exception as e:
            print(f"Error processing link '{link}': {e}")
            continue

if __name__ == "__main__":
    # blinky.clean_data()
    try:
        if seen_domains != []:
            crawl_node(random.choice(seen_domains))
        crawl_node(starting_node)
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Saving state...")
        save(state)
    except Exception as e:
        print(f"An error occurred: {e}")
        save(state)
