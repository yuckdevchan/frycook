import json, sys, subprocess, time
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
    "whatsmyip.org",
    "archlinux.org",
    "ubuntu.com",
    "debian.org",
    "fedora.org",
    "centos.org",
    "linuxmint.com",
    "opensuse.org",
    "redhat.com",
    "gentoo.org",
    "slackware.com",
    "freebsd.org",
    "netbsd.org",
    "openbsd.org",
]

print("Started")

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
extra = []

if Path("web.json").exists():
    with open("web.json", "r") as f:
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
    if Path("web.json").exists():
        with open("web.json", "r") as f:
            old_web = json.load(f)
            web.update(old_web)

    with open("web.json", "w") as f:
        to_dump = web
        json.dump(to_dump, f, indent=4)
    sys.exit(0)

seen_domains = blinky.get_seen_domains(web)

def crawl_node(node, depth=0):
    if Path("stop").exists():
        print("Stop file detected. Exiting...")
        time.sleep(counter*0.3)
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
    try:
        crawl_node(starting_node)
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Saving state...")
        save(state)
    except Exception as e:
        print(f"An error occurred: {e}")
        save(state)
