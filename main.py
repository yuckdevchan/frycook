from pathlib import Path
import pickle

import linky


h = "https://"
starting_node = h + "supersonic.software"

if Path("web.pickle").exists():
    with open("web.pickle", "rb") as f:
        loaded_file = pickle.load(f)
        web, seen_domains = loaded_file[0], loaded_file[1]
        print("Web data loaded successfully.")
else:
    web = {starting_node: []}
seen_domains = []

def crawl_node(node, depth=0):
    print(f"{"-"*depth if depth < 30 else "-"*30}x{depth} Crawling: {node}")
    links = linky.get_links(node)
    web[node] = links

    for link in links:
        try:
            domain = link.split("/")[2]
            if domain not in seen_domains:
                seen_domains.append(domain)
                web[link] = []
                if link not in web:
                    print(f"{"-"*depth}x{depth} Crawling: {link}")
                crawl_node(link, depth + 1)
        except Exception as e:
            print(f"Error processing link {link}: {e}")
            continue

try:
    crawl_node(starting_node)
except KeyboardInterrupt:
    print("\n\nCrawling interrupted. Saving progress...")
    with open("web.pickle", "wb") as f:
        to_dump = [web, seen_domains]
        pickle.dump(to_dump, f)
        print("Progress saved.")
