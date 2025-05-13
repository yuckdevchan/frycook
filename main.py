import pickle, sys, subprocess, time
from pathlib import Path

import blinky, linky

seeds = [
    "google.com",
    "wikipedia.org",
    "github.com",
    "stackoverflow.com",
    "yahoo.com",
    "x.com",
    "reddit.com",
    "quora.com",
    "bing.com",
    "duckduckgo.com",
    "baidu.com",
    "yandex.com",
    "amazon.com",
    "ebay.com",
    "craigslist.org",
    "bestbuy.com",
    "target.com",
    "walmart.com",
    "costco.com",
    "homeDepot.com",
    "lowes.com",
    "alibaba.com",
    "taobao.com",
    "jd.com",
    "weibo.com",
    "qq.com",
    "tencent.com",
]

if Path("stop").exists(): Path("stop").unlink()

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

web = {starting_node: []}
seen_domains = []
extra = []

if Path("web.pickle").exists():
    with open("web.pickle", "rb") as f:
        loaded_file = pickle.load(f)
        old_web, old_seen_domains, old_extra = loaded_file[0], loaded_file[1], loaded_file[2]
        web.update(old_web)
        seen_domains = list(set(seen_domains + old_seen_domains))
        extra = list(set(extra + old_extra))
        print("Web data loaded and merged successfully.")

def crawl_node(node, depth=0):
    if Path("stop").exists():
        print("Stop file found. Exiting...")
        return
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

try:
    crawl_node(starting_node)
except KeyboardInterrupt:
    print("\n\nCrawling interrupted. Saving progress...")

time.sleep(counter * 0.5)

if Path("web.pickle").exists():
    with open("web.pickle", "rb") as f:
        loaded_file = pickle.load(f)
        old_web, old_seen_domains, old_extra = loaded_file[0], loaded_file[1], loaded_file[2]
        web.update(old_web)
        seen_domains = list(set(seen_domains + old_seen_domains))
        extra = list(set(extra + old_extra))

with open("web.pickle", "wb") as f:
    to_dump = [web, seen_domains, extra]
    pickle.dump(to_dump, f)
    print("Progress saved.")

blinky.present_data()
