import json, sys, subprocess, random, threading
from pathlib import Path

import blinky, linky

h = "https://"

web = {}
extra = []

if Path(f"data/web.json").exists():
    with open(f"data/web.json", "r") as f:
        old_web = json.load(f)
        web.update(old_web)
        print("Web data loaded and merged successfully.")

def start():
    """Start the crawler"""
    
    if Path("stop").exists(): Path("stop").unlink()

    if not Path("data").exists():
        Path("data").mkdir()

    with open("seeds.json", "r") as f:
        seeds = json.load(f)

    for i in range(len(seeds)): seeds[i] = h + seeds[i]
    starting_node = sys.argv[1] if len(sys.argv) > 1 else ""

    seen_domains = blinky.get_seen_domains(web)
    num_threads = 1
    threads = []
    starting_counter = 0

    def get_starting_node() -> str:
        if seen_domains != []:
            thread_starting_node = h + random.choice(seen_domains)
        elif seeds != []:
            thread_starting_node = random.choice(seeds)
            seeds.remove(thread_starting_node)
            thread_starting_node = h + thread_starting_node
        else: thread_starting_node = None
        return thread_starting_node

    starting_node = get_starting_node()
    web[starting_node] = []

    for i in range(num_threads - 1):
        thread_starting_node = get_starting_node()
        if thread_starting_node == None:
            print("No more seeds or seen domains to crawl. Exiting...")
            break
        thread = threading.Thread(crawl_node(thread_starting_node, i))
        threads.append(thread)
    for thread in threads:
        thread.start()

    return seen_domains, web, starting_node

class CrawlerState:
    def __init__(self):
        self.saving = False

state = CrawlerState()

def save(state, thread_number):
    if state.saving:
        return
    state.saving = True
    if Path(f"data/web-{thread_number}.json").exists():
        with open(f"data/web-{thread_number}.json", "r") as f:
            old_web = json.load(f)
            web.update(old_web)

    with open(f"data/web-{thread_number}.json", "w") as f:
        to_dump = web
        json.dump(to_dump, f, indent=4)
    sys.exit(0)

def crawl_node(node: str, thread_number: int, depth=0):
    """Recursively crawl the web starting from the given node"""
    print(f"thread number >>>>> {thread_number}")
    if depth > 15:
        return
    if Path("stop").exists():
        print(f"Stop file detected. Exiting...")
        save(state, thread_number)
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
                crawl_node(link, thread_number, depth + 1)
        except Exception as e:
            print(f"Error processing link '{link}': {e}")
            continue

if __name__ == "__main__":
    # blinky.clean_data()
    try:
        seen_domains, web, starting_node = start()
        crawl_node(starting_node, 0)
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Saving state...")
        save(state, 0)
    except Exception as e:
        print(f"An error occurred: {e}")
        save(state, 0)
